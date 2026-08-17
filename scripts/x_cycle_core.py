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
    dedup_post_urls,
    extract_candidates,
    filter_candidates,
    is_logged_in,
    load_state_bundle,
    normalize_status_url,
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


def record_reply(
    handle: str,
    post_url: str,
    text: str,
    bump: bool,
    *,
    followup_of: str = "",
    no_cooldown: bool = False,
) -> None:
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
    if followup_of:
        cmd.extend(["--followup-of", followup_of])
    if no_cooldown:
        cmd.append("--no-cooldown")
    subprocess.run(cmd, check=True, cwd=ROOT)


FOLLOWUP_FALLBACKS = [
    "yeah that part is what makes it land",
    "fair — that's usually the fiddly bit",
    "makes sense, the small motion details carry it",
    "yeah the settle timing sells it",
]


def pick_followup_text(author_snippet: str = "") -> str:
    """Short continue for reply-back threads. No links, no bait questions."""
    import hashlib

    seed = (author_snippet or "default").encode("utf-8")
    idx = int(hashlib.md5(seed).hexdigest(), 16) % len(FOLLOWUP_FALLBACKS)
    return FOLLOWUP_FALLBACKS[idx]


def post_pending_followups(page, *, max_n: int = 1, dry_run: bool = False) -> list[str]:
    """Post up to max_n follow-ups for pending author reply-backs."""
    from x_reply_back_check import _pending_followups

    log_path = ROOT / "logs" / "replies.json"
    if not log_path.is_file():
        return []
    log = json.loads(log_path.read_text(encoding="utf-8"))
    pending = _pending_followups(log.get("entries", []))
    if not pending:
        return []

    bundle = load_state_bundle()
    caps = bundle["caps"]
    today = date.today().isoformat()
    if caps.get("date") != today:
        replies_total = 0
    else:
        replies_total = int(caps.get("replies", 0))
    cap = int(caps.get("cap_replies", 32))
    slots = max(0, min(max_n, cap - replies_total))
    if slots < 1:
        return []

    posted: list[str] = []
    for entry in pending[:slots]:
        handle = entry.get("handle", "")
        target = entry.get("author_reply_url") or entry.get("post_url", "")
        origin = entry.get("post_url", "")
        if not target or not handle:
            continue
        text = pick_followup_text(entry.get("reply_text", ""))
        # Strip any accidental punctuation bait
        text = text.replace("?", ".").strip()
        if dry_run:
            print(json.dumps({"followup": True, "handle": handle, "target": target, "text": text}))
            posted.append(target)
            continue
        try:
            post_reply(page, target, text)
        except Exception as e:
            print(f"followup failed @{handle}: {e}", file=sys.stderr)
            break
        record_reply(
            handle,
            target,
            text,
            bump=False,
            followup_of=origin,
            no_cooldown=True,
        )
        posted.append(target)
        if len(posted) < slots:
            time.sleep(random.randint(45, 90))
    return posted


def followups_enabled() -> bool:
    """Second replies look automated — off unless X_REPLY_FOLLOWUPS=1."""
    return os.environ.get("X_REPLY_FOLLOWUPS", "").strip().lower() in (
        "1",
        "true",
        "yes",
    )


def run_reply_back_and_followups(page, *, dry_run: bool = False) -> dict:
    """Detect author reply-backs; follow-ups only if X_REPLY_FOLLOWUPS=1."""
    from x_reply_back_check import check_reply_backs

    rb = check_reply_backs(page, recent=10)
    if followups_enabled():
        followups = post_pending_followups(page, max_n=1, dry_run=dry_run)
    else:
        followups = []
        rb["followups_skipped"] = "one_reply_per_post"
    rb["followups_posted"] = followups
    return rb


def has_compose_key() -> bool:
    from x_compose_replies import resolve_compose_backend

    return resolve_compose_backend() is not None


def _is_framer_referral_url(url: str) -> bool:
    u = url.lower()
    return "framer.link/builtbykern" in u or "framer.link/" in u


def _is_cursor_referral_url(url: str) -> bool:
    u = url.lower()
    return "cursor.com/referral" in u or "whbu5crp1xkf" in u


def _strip_sentence_questions(text: str, url_re: re.Pattern[str]) -> str:
    """Turn sentence '?' into '.' without breaking URL query strings (e.g. referral?code=)."""
    import re as _re

    urls = url_re.findall(text)
    masked = text
    for i, u in enumerate(urls):
        masked = masked.replace(u, f"\0URL{i}\0")
    if "?" not in masked:
        return text
    masked = masked.replace("?", ".")
    masked = _re.sub(r"\.\.+", ".", masked).strip()
    if masked.endswith("."):
        pass
    else:
        masked = masked.rstrip(". ") + "."
    for i, u in enumerate(urls):
        masked = masked.replace(f"\0URL{i}\0", u)
    return masked


def _token_set(text: str) -> set[str]:
    import re

    stop = {
        "a", "an", "the", "to", "for", "of", "on", "in", "at", "and", "or", "is", "are",
        "was", "were", "be", "been", "this", "that", "it", "my", "your", "you", "i",
        "after", "before", "with", "from", "just", "made", "got", "get", "have", "has",
        "check", "out", "below", "more", "come", "finally",
    }
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {w for w in words if len(w) > 1 and w not in stop}


def _is_echo_reply(reply: str, source: str) -> bool:
    """True when reply mostly restates the original post (bot paraphrase)."""
    import re

    r = (reply or "").strip().lower()
    s = (source or "").strip().lower()
    if not r or not s:
        return False
    # Exact / near-substring echo
    r_compact = re.sub(r"[^a-z0-9\s]", "", r)
    s_compact = re.sub(r"[^a-z0-9\s]", "", s)
    if len(r_compact) >= 12 and r_compact in s_compact:
        return True
    rw, sw = _token_set(r), _token_set(s)
    if not rw:
        return True
    overlap = len(rw & sw) / max(1, len(rw))
    # Almost all reply content words already in the post → paraphrase
    if overlap >= 0.55 and len(rw) <= 8:
        return True
    if overlap >= 0.72 and len(rw) <= 12:
        return True
    if overlap >= 0.85:
        return True
    return False


def _sanitize_drafts(drafts: list[dict], source_by_url: dict[str, str] | None = None) -> list[dict]:
    """Enforce voice rules that the LLM might miss."""
    import re

    from _config import text_has_referral_link
    from x_playwright import normalize_status_url

    # Trailing punctuation often sticks to model URLs
    url_re = re.compile(r"https?://[^\s\]\)\"']+")
    # Cursor ended referrals — strip any invented cursor.com/referral URLs
    cursor_ref_re = re.compile(
        r"https?://(?:www\.)?cursor\.com/referral(?:\.code=|\?code=)[A-Za-z0-9]+",
        re.I,
    )
    # Uncanny / try-hard / pedantic patterns
    creepy_re = re.compile(
        r"(#\s*\d+.*(parked|next to|vs\.?|#\s*\d+))"
        r"|(entire caption)"
        r"|(parked next to)"
        r"|(as an actual hiring)"
        r"|(catches me off guard)"
        r"|(generous drop)"
        r"|(mixed bag)"
        r"|(useful setup for)"
        r"|(still being the default)"
        r"|(weirdly scarce)"
        r"|(outdated code)"
        r"|(\bsomehow\b)"
        r"|(\bas a\b)"  # "chatassist as a chatbot saas site"
        r"|(went fully free)"
        r"|(on the marketplace already)",
        re.I,
    )
    # Label-speak / product noun-phrase with no real reaction
    label_re = re.compile(
        r"^(oh\s+)?[a-z0-9][\w./-]{1,24}\s+(for|on|as|from|with)\s+",
        re.I,
    )
    sources = source_by_url or {}
    referral_seen = False
    out = []
    for d in drafts:
        text = d.get("reply_text", "")
        tone = d.get("tone", "neutral")
        post_url = normalize_status_url(str(d.get("post_url") or ""))

        text = cursor_ref_re.sub("", text)
        text = re.sub(r"\s+\.", ".", text)
        text = re.sub(r"  +", " ", text).strip()
        text = text.strip(" .")

        if creepy_re.search(text):
            print(f"sanitize drop creepy @{d.get('handle')}: {text[:80]}", flush=True)
            continue

        if label_re.search(text) and "?" not in text:
            # Allow if it has a clear chill reaction token
            if not re.search(
                r"\b(sick|wild|nice|damn|love|hits|feels|stings|suck|curious|wait)\b",
                text,
                re.I,
            ):
                print(f"sanitize drop label @{d.get('handle')}: {text[:80]}", flush=True)
                continue

        source = sources.get(post_url) or d.get("source_text") or ""
        # Fuzzy match source if URL key missed
        if not source:
            for u, t in sources.items():
                if u and post_url and (u.endswith(post_url.split("/")[-1]) or post_url.endswith(u.split("/")[-1])):
                    source = t
                    break
        if source and _is_echo_reply(text, source):
            print(f"sanitize drop echo @{d.get('handle')}: {text[:80]}", flush=True)
            continue

        urls = url_re.findall(text)
        for u in urls:
            raw = u
            u = u.rstrip(".,;:!?")
            if raw != u:
                text = text.replace(raw, u)
            if "hostinger.com" in u.lower():
                text = text.replace(u, "").strip()
                continue
            if _is_cursor_referral_url(u):
                # Program ended — never keep these links
                text = text.replace(u, "").strip()
                continue
            if _is_framer_referral_url(u):
                if tone == "empathy" or referral_seen:
                    text = text.replace(u, "").strip()
                else:
                    referral_seen = True
            else:
                text = text.replace(u, "").strip()

        # No questions on empathy replies (preserve URL query '?')
        if tone == "empathy":
            text = _strip_sentence_questions(text, url_re)

        # No referral link + sentence question in same reply
        if text_has_referral_link(text):
            text = _strip_sentence_questions(text, url_re)

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
    max_replies: int = 1,
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
    skip_urls = dedup_post_urls(bundle)
    pool = bundle["rotation"].get("pool") or ["framer code component"]
    start_idx = int(bundle["rotation"].get("cycle_index", 0)) % len(pool)

    candidates = []
    raw = []
    tried_queries = []
    dup_url_n = 0
    for offset in range(len(pool)):
        q = pool[(start_idx + offset) % len(pool)]
        tried_queries.append(q)
        search_latest(page, q)
        raw = extract_candidates(page)
        before_urls = {
            normalize_status_url(str(c.get("post_url") or c.get("url") or ""))
            for c in raw
        }
        candidates = filter_candidates(
            raw,
            skip,
            max_n=5,
            forbid_component=comp_block,
            skip_post_urls=skip_urls,
        )
        dup_url_n = max(0, len([u for u in before_urls if u and u in skip_urls]))
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
    from x_playwright import normalize_status_url

    url_text = {
        normalize_status_url(str(c.get("post_url") or c.get("url") or "")): c.get("text", "")
        for c in candidates
    }
    url_text = {k: v for k, v in url_text.items() if k}
    for d in drafts:
        d["tone"] = _tone_hint(url_text.get(normalize_status_url(str(d.get("post_url") or "")), ""))

    drafts = _sanitize_drafts(drafts, source_by_url=url_text)
    if not drafts:
        print_run_output(0, [], len(raw), "thin:echo", replies_total, peek_next_query(bundle))
        return 0

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
        nu = normalize_status_url(post_url)
        if nu:
            skip_urls.add(nu)
        if i < len(drafts) - 1:
            time.sleep(random.randint(45, 120))

    bundle2 = load_state_bundle()
    replies_total = int(bundle2["caps"].get("replies", replies_total))
    reasons = f"dup:{dup_url_n}" if dup_url_n else "dup:0"
    print_run_output(
        len(posted_urls),
        posted_urls,
        max(0, len(raw) - len(candidates)),
        reasons,
        replies_total,
        current_query(bundle2),
    )
    return 0
