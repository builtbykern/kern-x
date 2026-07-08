#!/usr/bin/env python3
"""One-time (or refresh) login: saves state/.x-storage-state.json for Playwright."""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from x_playwright import is_logged_in, launch_context, load_dotenv, save_storage


def main() -> None:
    load_dotenv()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Install: pip install -r requirements-browser.txt && playwright install chromium")
        sys.exit(1)

    cdp = __import__("os").environ.get("X_CDP_URL")

    with sync_playwright() as p:
        context, browser, mode = launch_context(p, cdp_url=cdp)
        page = context.pages[0] if context.pages else context.new_page()

        if is_logged_in(page):
            print("Already logged in.")
        else:
            page.goto("https://x.com/i/flow/login", wait_until="domcontentloaded")
            print("Log in as @builtbykern in the browser window, then press Enter here...")
            input()

        if not is_logged_in(page):
            print("ERROR: still not logged in")
            sys.exit(1)

        if mode != "cdp":
            save_storage(context)
            print(f"Saved session → {Path(__file__).resolve().parents[1] / 'state' / '.x-storage-state.json'}")
        else:
            print("CDP mode: session lives in Chrome profile (no storage export).")

        time.sleep(1)
        if mode == "storage":
            browser.close()
        elif mode == "persistent":
            browser.close()


if __name__ == "__main__":
    main()
