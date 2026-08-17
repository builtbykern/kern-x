#!/usr/bin/env python3
"""Post one original to X with optional media. Uses kern-x Playwright session."""

from __future__ import annotations

import argparse
import os
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from x_playwright import (  # noqa: E402
    _save_fail_screenshot,
    get_work_page,
    is_logged_in,
    launch_context,
    load_dotenv,
    nav_timeout_ms,
    page_settle_sec,
    save_storage,
    settle_before_browser_close,
)


def _textbox(page):
    return page.locator(
        '[data-testid="tweetTextarea_0"], [data-testid="tweetTextarea0"], '
        'div[role="textbox"][data-testid="tweetTextarea_0"]'
    ).first


def _wait_media_ready(page, timeout_sec: float = 120) -> None:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        processing = page.locator("text=/Processing media|Uploading|processing/i").count()
        send = page.locator('[data-testid="tweetButton"]').first
        disabled = True
        try:
            if send.count():
                disabled = send.get_attribute("aria-disabled") not in (None, "false")
        except Exception:
            disabled = True
        has_attach = page.locator('[data-testid="attachments"]').count() > 0
        has_remove = page.locator('[aria-label*="Remove"]').count() > 0
        if (has_attach or has_remove) and processing == 0 and not disabled:
            time.sleep(2)
            return
        time.sleep(1.5)
    raise RuntimeError("media upload did not become ready in time")


def post_original(page, text: str, media: list[str] | None = None) -> str:
    page.goto("https://x.com/builtbykern", wait_until="load", timeout=nav_timeout_ms())
    time.sleep(page_settle_sec())
    before = page.evaluate(
        r"""() => [...document.querySelectorAll('article a[href*="/status/"]')]
            .map(a => a.href.split('?')[0])
            .filter(h => /\/status\/\d+/.test(h))"""
    )

    page.goto("https://x.com/compose/post", wait_until="load", timeout=nav_timeout_ms())
    time.sleep(page_settle_sec())

    box = _textbox(page)
    try:
        box.wait_for(state="visible", timeout=30_000)
    except Exception:
        page.goto("https://x.com/home", wait_until="load", timeout=nav_timeout_ms())
        time.sleep(page_settle_sec())
        page.locator('[data-testid="SideNav_NewTweet_Button"]').first.click(timeout=15_000)
        time.sleep(2)
        box = _textbox(page)
        box.wait_for(state="visible", timeout=30_000)

    box.click()
    time.sleep(0.4)
    box.fill("")
    page.keyboard.type(text, delay=12)
    time.sleep(1)

    paths = [p for p in (media or []) if p and Path(p).is_file()]
    if paths:
        file_input = page.locator('input[data-testid="fileInput"], input[type="file"]').first
        file_input.set_input_files(paths[:4])
        _wait_media_ready(page)

    send = page.locator('[data-testid="tweetButton"]').first
    send.wait_for(state="visible", timeout=30_000)
    for _ in range(60):
        if send.get_attribute("aria-disabled") in (None, "false"):
            break
        time.sleep(1)

    page.keyboard.press("Escape")
    time.sleep(0.3)
    box.click()
    time.sleep(0.2)

    try:
        send.click(timeout=10_000, force=True)
    except Exception:
        page.keyboard.press("Meta+Enter")

    deadline = time.time() + 45
    confirmed = False
    while time.time() < deadline:
        if page.locator("text=/Your post was sent/i").count():
            confirmed = True
            break
        if "compose/post" not in page.url:
            confirmed = True
            break
        time.sleep(1)

    time.sleep(page_settle_sec())
    page.goto("https://x.com/builtbykern", wait_until="load", timeout=nav_timeout_ms())
    time.sleep(page_settle_sec())

    links = page.evaluate(
        r"""() => [...document.querySelectorAll('article a[href*="/status/"]')]
            .map(a => a.href.split('?')[0])
            .filter(h => /\/status\/\d+/.test(h))"""
    )
    seen = set()
    uniq = []
    for h in links:
        if h not in seen:
            seen.add(h)
            uniq.append(h)

    before_set = set(before or [])
    new_urls = [u for u in uniq if u not in before_set]
    if new_urls:
        return new_urls[0]

    _save_fail_screenshot(page, "post-unconfirmed")
    raise RuntimeError(
        f"post not confirmed (toast={confirmed}); no new status vs before={list(before_set)[:3]}"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--media", action="append", default=[])
    ap.add_argument("--cdp", default=None)
    args = ap.parse_args()

    load_dotenv()
    cdp = args.cdp if args.cdp is not None else os.environ.get("X_CDP_URL")
    if cdp:
        try:
            urllib.request.urlopen(cdp.rstrip("/") + "/json/version", timeout=2)
        except Exception:
            print("CDP unavailable — using storage session")
            cdp = None

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        context, browser, mode = launch_context(p, cdp_url=cdp)
        print(f"mode={mode}")
        page = get_work_page(context)
        if not is_logged_in(page):
            print("ERROR: not logged in as @builtbykern", file=sys.stderr)
            sys.exit(2)
        handle = page.evaluate(
            r"""() => {
              const a = document.querySelector('[data-testid="AppTabBar_Profile_Link"]');
              return a ? a.getAttribute('href') : null;
            }"""
        )
        print(f"profile_link={handle}")
        url = post_original(page, args.text, args.media)
        print(f"posted_url={url}")
        if mode == "storage":
            save_storage(context)
        settle_before_browser_close(page)
        if mode == "storage":
            browser.close()


if __name__ == "__main__":
    main()
