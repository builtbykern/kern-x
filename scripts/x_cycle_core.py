"""Shared KERN-Reply cycle logic (browser stays open when driven by daemon)."""

from __future__ import annotations

import json
import os
import random
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from x_playwright import (  # noqa: E402
    current_query,
    dedup_handles,
    extract_candidates,
    filter_candidates,
    is_logged_in,
    load_state_bundle,
    post_reply,
    search_latest,
)


def print_run_output(
    posted_n: int,
    urls: list[str],
    skipped_n: int,
    reasons: str,
    replies_total: int,
    next_query: str,
) -> None:
    print(f"posted_n: {posted_n}")
    print(f"urls: {','.join(urls) if urls else 'none'}")
    print(f"skipped_n: {skipped_n}")
    print(f"reasons: {reasons}")
    print(f"replies_total: {replies_total}")
    print(f"next_query: {next_query}")


def peek_next_query(bundle: dict) -> str:
    rot = bundle["rotation"]
    pool = rot.get("pool") or ["framer code component"]
    idx = (int(rot.get("cycle_index", 0)) + 1) % len(pool)
    return pool[idx]


def _normalize_handle(h: str) -> str:
    h = h.strip()
    while h.startswith("@@"):
        h = h[1:]
    if not h.startswith("@"):
        h = f"@{h}"
    return h


def record_reply(handle: str, post_url: str, text: str, bump: bool) -> None:
    handle = _normalize_handle(handle)
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "record_reply.py"),
        "--handle",
        handle,
        "--post-url",
        post_url,
        "--text",
        text,
    ]
    if bump:
        cmd.append("--bump-rotation")
    subprocess.run(cmd, check=True, cwd=ROOT)


def has_compose_key() -> bool:
    from x_compose_replies import resolve_compose_backend

    return resolve_compose_backend() is not None


def _is_framer_referral_url(url: str) -> bool:
    u = url.lower()
    return "framer.link/builtbykern" in u or "framer.link/" in u


def _is_cursor_referral_url(url: str) -> bool:
    u = url.lower()
    return "cursor.com/referral" in u or "whbu5crp1xkf" in u


def _sanitize_drafts(drafts: list[dict]) -> list[dict]:
    """Enforce voice rules that the LLM might miss."""
    import re

    from _config import cursor_referral_url, text_has_referral_link

    canonical_cursor = cursor_referral_url()
    url_re = re.compile(r"https?://\S+")
    referral_seen = False
    out = []
    for d in drafts:
        text = d.get("reply_text", "")
        tone = d.get("tone", "neutral")

        urls = url_re.findall(text)
        for u in urls:
            if "hostinger.com" in u.lower():
                text = text.replace(u, "").strip()
                continue
            if _is_cursor_referral_url(u):
                if tone == "empathy" or referral_seen or not canonical_cursor:
                    text = text.replace(u, "").strip()
                else:
                    referral_seen = True
                    text = text.replace(u, canonical_cursor).strip()
                continue
            if _is_framer_referral_url(u):
                if tone == "empathy" or referral_seen:
                    text = text.replace(u, "").strip()
                else:
                    referral_seen = True
            else:
                text = text.replace(u, "").strip()

        # No questions on empathy replies
        if tone == "empathy" and "?" in text:
            text = text.replace("?", ".").rstrip(". ") + "."

        # No referral link + question in same reply
        if text_has_referral_link(text) and "?" in text:
            text = text.replace("?", ".").rstrip(". ") + "."

        text = re.sub(r"  +", " ", text).strip()
        d["reply_text"] = text
        d["handle"] = _normalize_handle(d.get("handle", ""))
        out.append(d)
    return out


def compose_replies(candidates: list[dict], bundle: dict, max_n: int) -> list[dict]:
    tmp = ROOT / "state" / ".compose-candidates.json"
    tmp.write_text(json.dumps(candidates, indent=2), encoding="utf-8")
    today = bundle["week"].get("today", {})
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "x_compose_replies.py"),
        "--candidates",
        str(tmp),
        "--voice-file",
        str(ROOT / "voice" / "voice-compact.txt"),
        "--today-json",
        json.dumps(today),
        "--max",
        str(max_n),
    ]
    out = subprocess.check_output(cmd, cwd=ROOT, text=True)
    return json.loads(out)


def run_cycle(
    page,
    *,
    dry_run: bool = False,
    no_compose: bool = False,
    max_replies: int = 3,
) -> int:
    """Run one reply cycle on an already-open page. Returns exit code 0/1."""
    bundle = load_state_bundle()
    caps = bundle["caps"]
    today = date.today().isoformat()
    if caps.get("date") != today:
        caps["date"] = today
        caps["replies"] = 0
    replies_total = int(caps.get("replies", 0))
    cap = int(caps.get("cap_replies", 32))
    query = current_query(bundle)

    if replies_total >= cap:
        print_run_output(0, [], 0, "cap:1", replies_total, peek_next_query(bundle))
        return 0

    if not is_logged_in(page):
        print_run_output(0, [], 0, "error", replies_total, query)
        print("Session lost — run: python3 scripts/x_login.py", file=sys.stderr)
        return 1

    today_cfg = bundle["week"].get("today", {})
    forbid = today_cfg.get("forbid_mention_in_replies") and today_cfg.get("component")
    comp_block = str(today_cfg.get("component") or "") if forbid else None

    cd, recent = dedup_handles(bundle)
    skip = cd | recent
    pool = bundle["rotation"].get("pool") or ["framer code component"]
    start_idx = int(bundle["rotation"].get("cycle_index", 0)) % len(pool)

    candidates = []
    raw = []
    tried_queries = []
    for offset in range(len(pool)):
        q = pool[(start_idx + offset) % len(pool)]
        tried_queries.append(q)
        search_latest(page, q)
        raw = extract_candidates(page)
        candidates = filter_candidates(raw, skip, max_n=5, forbid_component=comp_block)
        if candidates:
            query = q
            break
        time.sleep(2)
    else:
        query = tried_queries[0]

    if not candidates:
        print_run_output(0, [], len(raw), f"thin:{len(tried_queries)}", replies_total, peek_next_query(bundle))
        return 0

    slots_left = max(0, cap - replies_total)
    compose_max = min(max_replies, slots_left, len(candidates))
    if compose_max < 1:
        print_run_output(0, [], 0, "cap:1", replies_total, peek_next_query(bundle))
        return 0

    if no_compose:
        print(json.dumps(candidates, indent=2))
        return 0

    if dry_run:
        drafts = []
        if has_compose_key():
            try:
                drafts = compose_replies(candidates, bundle, compose_max)
            except subprocess.CalledProcessError:
                pass
        print(json.dumps({"query": query, "candidates": candidates, "drafts": drafts}, indent=2))
        return 0

    if not has_compose_key():
        print_run_output(0, [], 0, "error:no_api_key", replies_total, peek_next_query(bundle))
        print(
            "Add CURSOR_API_KEY or OPENAI_API_KEY to .env",
            file=sys.stderr,
        )
        print(json.dumps(candidates, indent=2))
        return 0

    try:
        drafts = compose_replies(candidates, bundle, compose_max)
    except subprocess.CalledProcessError as e:
        print_run_output(0, [], 0, "error", replies_total, query)
        print(e, file=sys.stderr)
        return 1

    from x_compose_replies import _tone_hint

    url_text = {
        (c.get("post_url") or c.get("url", "")): c.get("text", "")
        for c in candidates
    }
    for d in drafts:
        d["tone"] = _tone_hint(url_text.get(d.get("post_url", ""), ""))

    drafts = _sanitize_drafts(drafts)

    posted_urls: list[str] = []
    for i, d in enumerate(drafts):
        text = d["reply_text"]
        post_url = d["post_url"]
        handle = d["handle"]
        try:
            post_reply(page, post_url, text)
        except Exception as e:
            print(f"post failed @{handle}: {e}", file=sys.stderr)
            break
        record_reply(handle, post_url, text, bump=(i == len(drafts) - 1))
        posted_urls.append(post_url)
        if i < len(drafts) - 1:
            time.sleep(random.randint(45, 120))

    bundle2 = load_state_bundle()
    replies_total = int(bundle2["caps"].get("replies", replies_total))
    print_run_output(
        len(posted_urls),
        posted_urls,
        max(0, len(raw) - len(candidates)),
        "dup:0",
        replies_total,
        current_query(bundle2),
    )
    return 0
