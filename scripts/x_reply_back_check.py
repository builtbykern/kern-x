#!/usr/bin/env python3
"""Check recent replies for author reply-backs (no LLM, DOM-only)."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "logs" / "replies.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))


def check_reply_backs(page, recent: int = 20) -> dict:
    """Visit recent reply URLs and check if the original author replied to us."""
    from x_playwright import nav_timeout_ms, page_settle_sec

    log = json.loads(LOG_PATH.read_text(encoding="utf-8")) if LOG_PATH.is_file() else {}
    entries = log.get("entries", [])[-recent:]
    results = {"checked": 0, "reply_backs": 0, "handles": []}

    for entry in entries:
        if entry.get("author_replied") is not None:
            continue

        post_url = entry.get("post_url", "")
        if not post_url:
            continue

        try:
            page.goto(post_url, wait_until="load", timeout=nav_timeout_ms())
            time.sleep(page_settle_sec())

            our_handle = "builtbykern"
            articles = page.locator("article").all()
            found_us = False
            author_replied_after = False

            for article in articles:
                text_el = article.locator('[data-testid="tweetText"]').first
                handle_links = article.locator("a").all()
                handle_text = ""
                for link in handle_links[:3]:
                    try:
                        inner = link.inner_text()
                        if "@" in inner:
                            handle_text = inner.lower().replace("@", "")
                            break
                    except Exception:
                        continue

                if our_handle in handle_text:
                    found_us = True
                    continue

                if found_us and handle_text:
                    original_handle = entry.get("handle", "").lower().replace("@", "")
                    if original_handle and original_handle in handle_text:
                        author_replied_after = True
                        break

            entry["author_replied"] = author_replied_after
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
            if stored.get("post_url") == checked.get("post_url") and "author_replied" in checked:
                all_entries["entries"][i]["author_replied"] = checked["author_replied"]

    LOG_PATH.write_text(json.dumps(all_entries, indent=2) + "\n", encoding="utf-8")
    return results


def main() -> None:
    import argparse

    from x_playwright import get_work_page, launch_context, load_dotenv

    load_dotenv()

    p = argparse.ArgumentParser()
    p.add_argument("--recent", type=int, default=20)
    args = p.parse_args()

    import os

    from playwright.sync_api import sync_playwright

    cdp = os.environ.get("X_CDP_URL", "http://127.0.0.1:9222")

    with sync_playwright() as pw:
        context, browser, mode = launch_context(pw, cdp_url=cdp)
        page = get_work_page(context)
        results = check_reply_backs(page, recent=args.recent)
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
