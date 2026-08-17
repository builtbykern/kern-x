#!/usr/bin/env python3
"""One-shot reply cycle. Prefer the reply daemon for all-day one-tab reuse.

With --storage, browser stays open by default (one tab). CDP reuses Chrome.
Only create a page when the context has zero tabs (get_work_page).
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from x_cycle_core import run_cycle, run_reply_back_and_followups  # noqa: E402
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
    ap.add_argument(
        "--storage",
        action="store_true",
        help="Use Playwright storage state instead of X_CDP_URL",
    )
    args = ap.parse_args()

    keep = args.keep_browser or os.environ.get("X_KEEP_BROWSER", "").strip() in (
        "1",
        "true",
        "yes",
    )
    # Default: keep the storage browser open so we don't spawn a new window/tab each cycle
    if args.storage and os.environ.get("X_KEEP_BROWSER", "").strip() == "":
        keep = True

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Install: pip install -r requirements-browser.txt", file=sys.stderr)
        sys.exit(1)

    if args.storage:
        os.environ.pop("X_CDP_URL", None)
        cdp = None
    else:
        cdp = os.environ.get("X_CDP_URL")
        if cdp is not None and not str(cdp).strip():
            cdp = None

    with sync_playwright() as p:
        context, browser, mode = launch_context(p, cdp_url=cdp)
        # One tab only — reuse for the whole cycle / day
        page = get_work_page(context)
        # Close any accidental extra tabs from prior runs
        for extra in list(context.pages):
            if extra is page:
                continue
            try:
                if not extra.is_closed():
                    extra.close()
            except Exception:
                pass
        code = run_cycle(
            page,
            dry_run=args.dry_run,
            no_compose=args.no_compose,
            max_replies=args.max_replies,
        )
        if not args.no_compose:
            try:
                rb = run_reply_back_and_followups(page, dry_run=args.dry_run)
                fus = rb.get("followups_posted") or []
                if fus:
                    print(f"[cycle] followups posted: {len(fus)}", flush=True)
            except Exception as e:
                print(f"[cycle] reply-back/followup failed: {e}", file=sys.stderr)
        if not keep and mode != "cdp":
            settle_before_browser_close(page)
            browser.close()
        elif mode == "cdp":
            print("[cycle] left Chrome open (CDP)", flush=True)
        else:
            print("[cycle] left browser open (one-tab / --keep-browser)", flush=True)
        sys.exit(code)


if __name__ == "__main__":
    main()
