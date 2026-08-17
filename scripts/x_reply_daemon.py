#!/usr/bin/env python3
"""
Keep browser open; run reply cycles every 60–90m (recommended scheduler target).

  python3 scripts/x_reply_daemon.py
  # or Chrome always open:
  ./scripts/x_chrome_cdp.sh   # terminal 1
  export X_CDP_URL=http://127.0.0.1:9222
  python3 scripts/x_reply_daemon.py
"""

from __future__ import annotations

import os
import random
import signal
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from x_cycle_core import run_cycle  # noqa: E402
from x_playwright import get_work_page, launch_context, load_dotenv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
_running = True


def _ensure_chrome_cdp(cdp_url: str) -> None:
    import subprocess
    import urllib.parse

    port = urllib.parse.urlparse(cdp_url).port or 9222
    check = subprocess.run(
        ["curl", "-sf", f"http://127.0.0.1:{port}/json/version"],
        capture_output=True,
    )
    if check.returncode == 0:
        return
    profile = os.environ.get("X_CHROME_PROFILE", str(Path.home() / ".kern-x-chrome"))
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    print(f"[daemon] starting Chrome CDP on {port}", flush=True)
    subprocess.Popen(
        [
            chrome,
            f"--remote-debugging-port={port}",
            f"--user-data-dir={profile}",
            "https://x.com/home",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(30):
        time.sleep(1)
        if subprocess.run(
            ["curl", "-sf", f"http://127.0.0.1:{port}/json/version"],
            capture_output=True,
        ).returncode == 0:
            time.sleep(2)
            return
    raise RuntimeError(f"Chrome CDP not available on port {port}")


def _stop(signum=None, _frame=None) -> None:
    global _running
    print(f"[daemon] signal {signum} received, stopping", flush=True)
    _running = False


def _sleep_jitter() -> int:
    lo, hi = 60 * 60, 90 * 60
    return lo + random.randint(0, hi - lo)


def main() -> None:
    load_dotenv()
    if os.environ.get("X_REPLY_ENABLED", "1").strip().lower() in ("0", "false", "no", "off"):
        print("[daemon] X_REPLY_ENABLED=0 — idle (no reply cycles)", flush=True)
        while True:
            time.sleep(3600)
        return
    if os.environ.get("X_FORCE_STORAGE", "").strip() in ("1", "true", "yes"):
        os.environ.pop("X_CDP_URL", None)
    env_file = ROOT / ".env"
    if env_file.is_file() and not os.environ.get("X_FORCE_STORAGE", "").strip():
        os.environ.setdefault("X_CDP_URL", "http://127.0.0.1:9222")
    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("pip install -r requirements-browser.txt && playwright install chromium", file=sys.stderr)
        sys.exit(1)

    cdp_raw = os.environ.get("X_CDP_URL")
    cdp = cdp_raw.strip() if cdp_raw and str(cdp_raw).strip() else None
    if cdp:
        os.environ["X_CDP_URL"] = cdp
    min_sec = int(os.environ.get("X_LOOP_MIN_SEC", str(60 * 60)))
    max_sec = int(os.environ.get("X_LOOP_MAX_SEC", str(90 * 60)))

    print(f"[daemon] browser stays open — CDP={cdp or 'off'}", flush=True)
    if cdp:
        try:
            _ensure_chrome_cdp(cdp)
        except Exception as e:
            print(f"[daemon] CDP unavailable ({e}); falling back to storage state", flush=True)
            os.environ.pop("X_CDP_URL", None)
            cdp = None

    with sync_playwright() as p:
        context, browser, mode = launch_context(p, cdp_url=cdp)
        page = get_work_page(context)
        print(f"[daemon] mode={mode} url={page.url!r}", flush=True)

        while _running:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[daemon] cycle start {ts}", flush=True)
            max_replies = int(os.environ.get("X_MAX_REPLIES_PER_CYCLE", "1"))
            code = run_cycle(page, max_replies=max(1, max_replies))
            print(f"[daemon] cycle exit {code} max_replies={max_replies}", flush=True)

            if not _running:
                break

            try:
                from x_cycle_core import followups_enabled, run_reply_back_and_followups

                rb = run_reply_back_and_followups(page)
                if rb.get("checked"):
                    print(
                        f"[daemon] reply-back check: {rb['reply_backs']}/{rb['checked']} "
                        f"replies got author response",
                        flush=True,
                    )
                fus = rb.get("followups_posted") or []
                if fus:
                    print(f"[daemon] followups posted: {len(fus)}", flush=True)
                elif not followups_enabled():
                    print(
                        "[daemon] followups off (one reply per post; set X_REPLY_FOLLOWUPS=1 to enable)",
                        flush=True,
                    )
            except Exception as e:
                print(f"[daemon] reply-back/followup failed: {e}", flush=True)

            if not _running:
                break
            sleep_sec = min_sec + random.randint(0, max(0, max_sec - min_sec))
            print(f"[daemon] sleep {sleep_sec}s (~{sleep_sec // 60}m)", flush=True)
            for _ in range(sleep_sec):
                if not _running:
                    break
                time.sleep(1)

        # CDP: disconnect only — Chrome stays open
        if mode == "cdp":
            print("[daemon] disconnected (Chrome still running)", flush=True)
        else:
            browser.close()
            print("[daemon] browser closed", flush=True)


if __name__ == "__main__":
    main()
