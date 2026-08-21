"""Playwright helpers for kern-x X automation."""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state"
TOOLS_DIR = ROOT / "tools" / "x-browser"
STORAGE_PATH = STATE_DIR / ".x-storage-state.json"
PROFILE_DIR = STATE_DIR / ".chrome-profile"


def _int_env(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def nav_timeout_ms() -> int:
    return _int_env("X_NAV_TIMEOUT_MS", 120_000)


def page_settle_sec() -> float:
    return _int_env("X_PAGE_SETTLE_SEC", 8)


def search_feed_wait_sec() -> float:
    return _int_env("X_SEARCH_FEED_WAIT_SEC", 50)


def browser_close_delay_sec() -> float:
    return _int_env("X_BROWSER_CLOSE_DELAY_SEC", 5)


def storage_path() -> Path:
    return STORAGE_PATH


def headless() -> bool:
    return os.environ.get("X_HEADLESS", "").strip() in ("1", "true", "yes")


def load_extract_js(name: str = "extract_technical_candidates.js") -> str:
    return (TOOLS_DIR / name).read_text(encoding="utf-8")


def get_work_page(context):
    """Reuse the existing browser tab — never open extras if one exists.

    Policy: one X tab for the day. Prefer an open x.com page; otherwise any
    live page; only create a page when the context has zero tabs.
    """
    for page in context.pages:
        try:
            if page.is_closed():
                continue
            if "x.com" in (page.url or ""):
                return page
        except Exception:
            continue
    for page in context.pages:
        try:
            if not page.is_closed():
                return page
        except Exception:
            continue
    page = context.new_page()
    page.goto("https://x.com/home", wait_until="load", timeout=nav_timeout_ms())
    time.sleep(page_settle_sec())
    return page


def launch_context(playwright, *, cdp_url: str | None = None):
    if cdp_url is not None and not str(cdp_url).strip():
        cdp_url = None
    if cdp_url:
        browser = playwright.chromium.connect_over_cdp(cdp_url)
        if browser.contexts:
            return browser.contexts[0], browser, "cdp"
        return browser.new_context(), browser, "cdp"

    if STORAGE_PATH.is_file():
        browser = playwright.chromium.launch(headless=headless())
        context = browser.new_context(storage_state=str(STORAGE_PATH))
        return context, browser, "storage"

    browser = playwright.chromium.launch_persistent_context(
        str(PROFILE_DIR),
        channel="chrome",
        headless=headless(),
        args=["--disable-blink-features=AutomationControlled"],
    )
    return browser, browser, "persistent"


def save_storage(context) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(STORAGE_PATH))


def _goto(page, url: str) -> None:
    page.goto(url, wait_until="load", timeout=nav_timeout_ms())
    time.sleep(page_settle_sec())


def is_logged_in(page) -> bool:
    _goto(page, "https://x.com/home")
    if "/login" in page.url or "/flow/login" in page.url:
        return False
    try:
        page.wait_for_selector(
            '[data-testid="SideNav_NewTweet_Button"]',
            timeout=nav_timeout_ms(),
        )
        time.sleep(page_settle_sec())
        return True
    except Exception:
        return False


def wait_for_search_feed(page, min_articles: int = 3) -> None:
    """Scroll and wait until X search timeline has rendered tweets."""
    deadline = time.time() + search_feed_wait_sec()
    best = 0
    while time.time() < deadline:
        count = page.locator("article").count()
        best = max(best, count)
        if count >= min_articles:
            time.sleep(page_settle_sec())
            return
        page.evaluate("window.scrollBy(0, 700)")
        time.sleep(2.5)
    time.sleep(page_settle_sec())


def search_latest(page, query: str) -> None:
    from urllib.parse import quote

    url = f"https://x.com/search?q={quote(query)}&src=typed_query&f=live"
    _goto(page, url)
    try:
        page.wait_for_selector('[data-testid="primaryColumn"]', timeout=nav_timeout_ms())
    except Exception:
        pass
    wait_for_search_feed(page)


def extract_candidates(page) -> list[dict]:
    js = load_extract_js()
    for attempt in range(4):
        raw = page.evaluate(js)
        if isinstance(raw, list) and raw:
            return raw
        if attempt < 3:
            page.evaluate("window.scrollBy(0, 900)")
            time.sleep(3)
            wait_for_search_feed(page, min_articles=1)
    return raw if isinstance(raw, list) else []


def _save_fail_screenshot(page, label: str) -> None:
    from datetime import datetime

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = ROOT / "logs" / f"reply-fail-{label}-{ts}.png"
    try:
        page.screenshot(path=str(path), full_page=False)
    except Exception:
        pass


def _open_reply_box(page):
    """Click reply and wait for the compose textbox. Returns the textbox locator or None."""
    # Strategy 1: click the reply button on the tweet detail page
    reply_btn = page.locator('[data-testid="reply"], [aria-label*="Reply"], [aria-label*="Responder"]').first
    try:
        reply_btn.wait_for(state="visible", timeout=30_000)
        reply_btn.click(timeout=15_000)
        time.sleep(page_settle_sec())
    except Exception:
        pass

    # Wait for dialog / inline compose to appear
    try:
        page.wait_for_selector(
            '[role="dialog"], [data-testid="tweetTextarea0"]',
            timeout=15_000,
        )
    except Exception:
        pass

    # Strategy 2: press 'r' shortcut if textbox still not visible
    box = page.locator('div[role="textbox"][contenteditable="true"]').first
    try:
        box.wait_for(state="visible", timeout=5_000)
        return box
    except Exception:
        page.keyboard.press("r")
        time.sleep(page_settle_sec())

    box = page.locator('div[role="textbox"][contenteditable="true"]').first
    try:
        box.wait_for(state="visible", timeout=15_000)
        return box
    except Exception:
        return None


def post_reply(page, post_url: str, text: str) -> str:
    _goto(page, post_url)

    box = _open_reply_box(page)
    if box is None:
        _save_fail_screenshot(page, "no-textbox")
        raise RuntimeError(f"reply textbox not found on {post_url}")

    box.click()
    time.sleep(0.5)
    box.fill(text)
    time.sleep(2)

    send = page.locator(
        '[data-testid="tweetButton"], [data-testid="tweetButtonInline"]'
    ).first
    try:
        send.wait_for(state="visible", timeout=15_000)
        send.click(timeout=15_000)
    except Exception:
        _save_fail_screenshot(page, "no-send-btn")
        raise RuntimeError(f"send button not found on {post_url}")

    time.sleep(page_settle_sec())
    return page.url


def settle_before_browser_close(page) -> None:
    time.sleep(browser_close_delay_sec())


def load_state_bundle() -> dict:
    caps = json.loads((STATE_DIR / "daily-caps.json").read_text(encoding="utf-8"))
    rotation = json.loads((STATE_DIR / "query-rotation.json").read_text(encoding="utf-8"))
    week = json.loads((STATE_DIR / "week-current.json").read_text(encoding="utf-8"))
    cooldown = json.loads((STATE_DIR / "cooldown-handles.json").read_text(encoding="utf-8"))
    replies = json.loads((ROOT / "logs" / "replies.json").read_text(encoding="utf-8"))
    voice = (ROOT / "voice" / "voice-compact.txt").read_text(encoding="utf-8").strip()
    return {
        "caps": caps,
        "rotation": rotation,
        "week": week,
        "cooldown": cooldown,
        "replies": replies,
        "voice": voice,
    }


def normalize_status_url(url: str) -> str:
    """Canonicalize an X status URL for one-reply-per-post dedup."""
    u = (url or "").strip().split("?")[0].rstrip("/")
    if not u:
        return ""
    # x.com and twitter.com are the same post
    u = u.replace("https://twitter.com/", "https://x.com/")
    u = u.replace("http://x.com/", "https://x.com/")
    u = u.replace("http://twitter.com/", "https://x.com/")
    return u.lower()


def dedup_handles(bundle: dict) -> tuple[set[str], set[str]]:
    now = time.time()
    cd = {
        h["handle"].lower()
        for h in bundle["cooldown"].get("handles", [])
        if h.get("until", 0) > now
    }
    recent = {
        e["handle"].lower()
        for e in bundle["replies"].get("entries", [])[-20:]
    }
    return cd, recent


def dedup_post_urls(bundle: dict) -> set[str]:
    """Every status we already touched — never reply twice to the same post."""
    seen: set[str] = set()
    for e in bundle["replies"].get("entries", []):
        for key in ("post_url", "followup_of", "author_reply_url", "followup_url"):
            u = normalize_status_url(str(e.get(key) or ""))
            if u:
                seen.add(u)
    return seen


def current_query(bundle: dict) -> str:
    rot = bundle["rotation"]
    pool = rot.get("pool") or []
    if not pool:
        return "framer code component"
    idx = int(rot.get("cycle_index", 0)) % len(pool)
    return pool[idx]


def _age_hours_from_label(label: str | None) -> float | None:
    """Parse X relative age labels. Returns hours, or None if unknown/too old format."""
    import re

    t = (label or "").strip()
    if not t:
        return None
    if re.search(r"just now", t, re.I):
        return 0.0
    if re.search(r"\d{4}", t) or re.search(
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", t, re.I
    ):
        return None
    m = re.search(r"(\d+)\s*([dhms])", t, re.I)
    if not m:
        return None
    n = int(m.group(1))
    u = m.group(2).lower()
    if u == "s":
        return n / 3600.0
    if u == "m":
        return n / 60.0
    if u == "h":
        return float(n)
    if u == "d":
        return float(n) * 24.0
    return None


def filter_candidates(
    candidates: list[dict],
    skip: set[str],
    max_n: int = 5,
    *,
    forbid_component: str | None = None,
    max_age_hours: float = 4.0,
    prefer_media: bool = True,
    skip_post_urls: set[str] | None = None,
) -> list[dict]:
    out: list[dict] = []
    comp = (forbid_component or "").lower()
    seen_urls = skip_post_urls or set()
    for c in candidates:
        handle = (c.get("handle") or "").strip()
        if not handle:
            continue
        key = handle.lower() if handle.startswith("@") else f"@{handle}".lower()
        if key in skip or key.lstrip("@") in {s.lstrip("@") for s in skip}:
            continue
        if "builtbykern" in key:
            continue
        text = (c.get("text") or "").lower()
        if comp and comp in text:
            continue
        age = _age_hours_from_label(c.get("age_label"))
        if age is not None and age > max_age_hours:
            continue
        # If extract already filtered but label missing, keep; if label present and unparsable → drop
        if c.get("age_label") and age is None:
            continue
        normed = {**c, "handle": key if key.startswith("@") else f"@{key}"}
        if "post_url" not in normed and "url" in normed:
            normed["post_url"] = normed["url"]
        status = normalize_status_url(str(normed.get("post_url") or ""))
        if status and status in seen_urls:
            continue
        normed["has_media"] = bool(normed.get("has_media"))
        out.append(normed)

    def _conversation_last(c: dict) -> tuple:
        text = c.get("text") or ""
        is_q = "?" in text or bool(
            re.search(
                r"\b(how do i|should i|vs |versus |worth it|anyone know|help with)\b",
                text,
                re.I,
            )
        )
        return (not is_q, not c.get("has_media") if prefer_media else False, c.get("age_label") or "")

    out.sort(key=_conversation_last)

    return out[:max_n]


def load_dotenv() -> None:
    env_path = ROOT / ".env"
    if not env_path.is_file():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip("'\"")
        if k and (k not in os.environ or not os.environ.get(k)):
            os.environ[k] = v
