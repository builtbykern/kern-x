#!/usr/bin/env python3
"""Append a post to logs/posts.json and bump daily-caps.posts."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "logs" / "posts.json"
CAPS_PATH = ROOT / "state" / "daily-caps.json"
MAX_ENTRIES = 50


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True)
    p.add_argument("--type", required=True)
    p.add_argument("--component", default="")
    p.add_argument("--had-link", choices=["true", "false"], required=True)
    p.add_argument("--text", required=True)
    args = p.parse_args()

    log = {"entries": []}
    if LOG_PATH.is_file():
        log = json.loads(LOG_PATH.read_text(encoding="utf-8"))

    entry = {
        "date": date.today().isoformat(),
        "post_url": args.url,
        "type": args.type,
        "component": args.component or None,
        "had_link": args.had_link == "true",
        "text": args.text,
    }
    log.setdefault("entries", []).append(entry)
    log["entries"] = log["entries"][-MAX_ENTRIES:]
    LOG_PATH.write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8")

    caps = json.loads(CAPS_PATH.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    if caps.get("date") != today:
        caps["date"] = today
        caps["posts"] = 0
        caps["replies"] = caps.get("replies", 0)
    caps["posts"] = int(caps.get("posts", 0)) + 1
    CAPS_PATH.write_text(json.dumps(caps, indent=2) + "\n", encoding="utf-8")
    print(f"recorded post posts={caps['posts']}")


if __name__ == "__main__":
    main()
