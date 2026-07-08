"""Playwright helpers for kern-x X automation."""

from __future__ import annotations

import json
import os
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
    """Reuse an open X tab when attached to the user's Chrome (CDP)."""
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


def current_query(bundle: dict) -> str:
    rot = bundle["rotation"]
    pool = rot.get("pool") or []
    if not pool:
        return "framer code component"
    idx = int(rot.get("cycle_index", 0)) % len(pool)
    return pool[idx]


def filter_candidates(
    candidates: list[dict],
    skip: set[str],
    max_n: int = 5,
    *,
    forbid_component: str | None = None,
) -> list[dict]:
    out: list[dict] = []
    comp = (forbid_component or "").lower()
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
        normed = {**c, "handle": key if key.startswith("@") else f"@{key}"}
        if "post_url" not in normed and "url" in normed:
            normed["post_url"] = normed.pop("url")
        out.append(normed)
        if len(out) >= max_n:
            break
    return out


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
