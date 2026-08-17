#!/usr/bin/env python3
"""Check recent replies for author reply-backs (no LLM, DOM-only)."""

from __future__ import annotations

import json
import re
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "logs" / "replies.json"
STATS_PATH = ROOT / "state" / "reply-back-stats.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Don't follow up on replies posted in the last N seconds (avoids same-cycle false positives)
FOLLOWUP_MIN_AGE_SEC = 30 * 60


def status_id_from_url(url: str) -> int:
    m = re.search(r"/status/(\d+)", url or "")
    return int(m.group(1)) if m else 0


def _pending_followups(entries: list[dict]) -> list[dict]:
    """Entries where author replied and we have not followed up yet."""
    now = time.time()
    pending = []
    for e in entries:
        if not e.get("author_replied"):
            continue
        if e.get("followup_url") or e.get("is_followup"):
            continue
        if not e.get("author_reply_url") and not e.get("post_url"):
            continue
        # Require a real author reply status newer than the original post
        origin_id = status_id_from_url(e.get("post_url", ""))
        reply_id = status_id_from_url(e.get("author_reply_url", ""))
        if not reply_id or not origin_id or reply_id <= origin_id:
            continue
        # Age gate: prefer recorded_at; fall back to skipping same-day brand-new without timestamp
        recorded_at = e.get("recorded_at")
        if recorded_at:
            try:
                if now - float(recorded_at) < FOLLOWUP_MIN_AGE_SEC:
                    continue
            except (TypeError, ValueError):
                pass
        pending.append(e)
    return pending


def write_reply_back_stats(log_entries: list[dict], results: dict) -> None:
    """Persist rolling reply-back rate for weekly review."""
    scored = [e for e in log_entries if e.get("author_replied") is not None and not e.get("is_followup")]
    backs = sum(1 for e in scored if e.get("author_replied"))
    rate = (backs / len(scored)) if scored else 0.0
    pending = _pending_followups(log_entries)
    stats = {
        "updated_at": date.today().isoformat(),
        "scored_n": len(scored),
        "reply_backs": backs,
        "rate": round(rate, 3),
        "target_rate": 0.25,
        "last_check": {
            "checked": results.get("checked", 0),
            "reply_backs": results.get("reply_backs", 0),
            "handles": results.get("handles", []),
        },
        "pending_followups": len(pending),
    }
    STATS_PATH.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")


def _article_author_handle(article) -> str:
    """Best-effort primary author handle from a tweet article."""
    try:
        user = article.locator('[data-testid="User-Name"]').first
        if user.count():
            links = user.locator("a").all()
            for link in links:
                href = link.get_attribute("href") or ""
                if href.startswith("/") and href.count("/") == 1:
                    return href.strip("/").lower()
                text = (link.inner_text() or "").strip()
                if text.startswith("@"):
                    return text[1:].lower()
    except Exception:
        pass
    try:
        for link in article.locator("a").all()[:8]:
            href = (link.get_attribute("href") or "").strip()
            if re.fullmatch(r"/[A-Za-z0-9_]+", href):
                return href.strip("/").lower()
    except Exception:
        pass
    return ""


def _article_status_url(article) -> str | None:
    try:
        time_a = article.locator("time").locator("xpath=..").first
        if not time_a.count():
            return None
        href = time_a.get_attribute("href") or ""
        if href.startswith("/"):
            href = "https://x.com" + href.split("?")[0]
        return href if "/status/" in href else None
    except Exception:
        return None


def check_reply_backs(page, recent: int = 20) -> dict:
    """Visit recent reply URLs and check if the original author replied to us."""
    from x_playwright import nav_timeout_ms, page_settle_sec

    log = json.loads(LOG_PATH.read_text(encoding="utf-8")) if LOG_PATH.is_file() else {}
    entries = log.get("entries", [])[-recent:]
    results = {
        "checked": 0,
        "reply_backs": 0,
        "handles": [],
        "pending_followups": [],
    }

    for entry in entries:
        if entry.get("is_followup"):
            continue
        if entry.get("author_replied") is False:
            continue
        if entry.get("author_replied") is True and entry.get("author_reply_url"):
            # Re-validate stale false positives (author_reply older than origin)
            origin_id = status_id_from_url(entry.get("post_url", ""))
            reply_id = status_id_from_url(entry.get("author_reply_url", ""))
            if reply_id > origin_id:
                continue
            # fall through to re-check
            entry.pop("author_replied", None)
            entry.pop("author_reply_url", None)

        post_url = entry.get("post_url", "")
        if not post_url:
            continue
        origin_id = status_id_from_url(post_url)

        try:
            page.goto(post_url, wait_until="load", timeout=nav_timeout_ms())
            time.sleep(page_settle_sec())

            our_handle = "builtbykern"
            articles = page.locator("article").all()
            found_us = False
            author_replied_after = False
            author_reply_url = None
            original_handle = entry.get("handle", "").lower().replace("@", "")

            for article in articles:
                handle_text = _article_author_handle(article)
                status_href = _article_status_url(article)

                if our_handle in handle_text:
                    found_us = True
                    continue

                if found_us and handle_text and original_handle and original_handle == handle_text:
                    sid = status_id_from_url(status_href or "")
                    if sid and origin_id and sid > origin_id:
                        author_replied_after = True
                        author_reply_url = status_href
                        break

            entry["author_replied"] = author_replied_after
            if author_reply_url:
                entry["author_reply_url"] = author_reply_url
            elif author_replied_after is False:
                entry.pop("author_reply_url", None)
            results["checked"] += 1
            if author_replied_after:
                results["reply_backs"] += 1
                results["handles"].append(entry.get("handle", ""))

        except Exception as e:
            print(f"[reply-back] error checking {post_url}: {e}", file=sys.stderr)
            continue

    all_entries = json.loads(LOG_PATH.read_text(encoding="utf-8")) if LOG_PATH.is_file() else {}
    for i, stored in enumerate(all_entries.get("entries", [])):
        for checked in entries:
            if stored.get("post_url") == checked.get("post_url") and not stored.get("is_followup"):
                if "author_replied" in checked:
                    all_entries["entries"][i]["author_replied"] = checked["author_replied"]
                if checked.get("author_reply_url"):
                    all_entries["entries"][i]["author_reply_url"] = checked["author_reply_url"]
                elif checked.get("author_replied") is False:
                    all_entries["entries"][i].pop("author_reply_url", None)
                    all_entries["entries"][i].pop("followup_url", None)

    LOG_PATH.write_text(json.dumps(all_entries, indent=2) + "\n", encoding="utf-8")
    results["pending_followups"] = _pending_followups(all_entries.get("entries", []))
    write_reply_back_stats(all_entries.get("entries", []), results)
    return results


def main() -> None:
    import argparse
    import os

    from playwright.sync_api import sync_playwright

    from x_playwright import get_work_page, launch_context, load_dotenv

    load_dotenv()

    p = argparse.ArgumentParser()
    p.add_argument("--recent", type=int, default=20)
    args = p.parse_args()

    cdp = os.environ.get("X_CDP_URL")
    if cdp is not None and not str(cdp).strip():
        cdp = None

    with sync_playwright() as pw:
        context, browser, mode = launch_context(pw, cdp_url=cdp)
        page = get_work_page(context)
        results = check_reply_backs(page, recent=args.recent)
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
