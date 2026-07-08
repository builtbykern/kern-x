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
from x_reply_back_check import check_reply_backs  # noqa: E402

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
    env_file = ROOT / ".env"
    if env_file.is_file():
        os.environ.setdefault("X_CDP_URL", "http://127.0.0.1:9222")
    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("pip install -r requirements-browser.txt && playwright install chromium", file=sys.stderr)
        sys.exit(1)

    cdp = os.environ.get("X_CDP_URL", "http://127.0.0.1:9222")
    os.environ["X_CDP_URL"] = cdp
    min_sec = int(os.environ.get("X_LOOP_MIN_SEC", str(60 * 60)))
    max_sec = int(os.environ.get("X_LOOP_MAX_SEC", str(90 * 60)))

    print(f"[daemon] browser stays open — CDP={cdp}", flush=True)
    _ensure_chrome_cdp(cdp)

    with sync_playwright() as p:
        context, browser, mode = launch_context(p, cdp_url=cdp)
        page = get_work_page(context)
        print(f"[daemon] mode={mode} url={page.url!r}", flush=True)

        while _running:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[daemon] cycle start {ts}", flush=True)
            code = run_cycle(page)
            print(f"[daemon] cycle exit {code}", flush=True)

            if not _running:
                break

            try:
                rb = check_reply_backs(page, recent=10)
                if rb["checked"]:
                    print(f"[daemon] reply-back check: {rb['reply_backs']}/{rb['checked']} replies got author response", flush=True)
            except Exception as e:
                print(f"[daemon] reply-back check failed: {e}", flush=True)

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
