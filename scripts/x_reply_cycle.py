#!/usr/bin/env python3
"""One-shot reply cycle (opens browser, runs once, closes unless X_KEEP_BROWSER=1 / CDP)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from x_cycle_core import run_cycle  # noqa: E402
from x_playwright import (  # noqa: E402
    get_work_page,
    launch_context,
    load_dotenv,
    settle_before_browser_close,
)


def main() -> None:
    load_dotenv()
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-replies", type=int, default=3)
    ap.add_argument("--no-compose", action="store_true")
    ap.add_argument(
        "--keep-browser",
        action="store_true",
        help="Do not close browser after cycle (same as X_KEEP_BROWSER=1)",
    )
    args = ap.parse_args()

    keep = args.keep_browser or os.environ.get("X_KEEP_BROWSER", "").strip() in (
        "1",
        "true",
        "yes",
    )

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Install: pip install -r requirements-browser.txt", file=sys.stderr)
        sys.exit(1)

    cdp = os.environ.get("X_CDP_URL")

    with sync_playwright() as p:
        context, browser, mode = launch_context(p, cdp_url=cdp)
        page = get_work_page(context)
        code = run_cycle(
            page,
            dry_run=args.dry_run,
            no_compose=args.no_compose,
            max_replies=args.max_replies,
        )
        if not keep and mode != "cdp":
            settle_before_browser_close(page)
            browser.close()
        elif mode == "cdp":
            print("[cycle] left Chrome open (CDP)", flush=True)
        else:
            print("[cycle] left browser open (--keep-browser)", flush=True)
        sys.exit(code)


if __name__ == "__main__":
    main()
