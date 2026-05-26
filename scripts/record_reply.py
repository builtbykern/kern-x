#!/usr/bin/env python3
"""Append reply, cooldown handle (+48h), bump caps and query rotation."""

from __future__ import annotations

import argparse
import json
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "logs" / "replies.json"
CAPS_PATH = ROOT / "state" / "daily-caps.json"
COOLDOWN_PATH = ROOT / "state" / "cooldown-handles.json"
ROTATION_PATH = ROOT / "state" / "query-rotation.json"
MAX_ENTRIES = 50
COOLDOWN_SECONDS = 48 * 3600


def normalize_handle(handle: str) -> str:
    h = handle.strip()
    if not h.startswith("@"):
        h = f"@{h}"
    return h


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--handle", required=True)
    p.add_argument("--post-url", required=True)
    p.add_argument("--text", required=True)
    p.add_argument(
        "--bump-rotation",
        action="store_true",
        help="Increment query-rotation.cycle_index once per cycle (use on last reply only)",
    )
    args = p.parse_args()

    handle = normalize_handle(args.handle)
    until = int(time.time()) + COOLDOWN_SECONDS

    log = {"entries": []}
    if LOG_PATH.is_file():
        log = json.loads(LOG_PATH.read_text(encoding="utf-8"))
    log.setdefault("entries", []).append(
        {
            "date": date.today().isoformat(),
            "handle": handle,
            "post_url": args.post_url,
            "reply_text": args.text,
        }
    )
    log["entries"] = log["entries"][-MAX_ENTRIES:]
    LOG_PATH.write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8")

    cooldown = {"handles": []}
    if COOLDOWN_PATH.is_file():
        cooldown = json.loads(COOLDOWN_PATH.read_text(encoding="utf-8"))
    handles = [h for h in cooldown.get("handles", []) if h.get("handle") != handle]
    handles.append({"handle": handle, "until": until})
    cooldown["handles"] = handles[-500:]
    COOLDOWN_PATH.write_text(json.dumps(cooldown, indent=2) + "\n", encoding="utf-8")

    caps = json.loads(CAPS_PATH.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    if caps.get("date") != today:
        caps["date"] = today
        caps["posts"] = caps.get("posts", 0)
        caps["replies"] = 0
    caps["replies"] = int(caps.get("replies", 0)) + 1
    CAPS_PATH.write_text(json.dumps(caps, indent=2) + "\n", encoding="utf-8")

    if args.bump_rotation and ROTATION_PATH.is_file():
        rot = json.loads(ROTATION_PATH.read_text(encoding="utf-8"))
        rot["cycle_index"] = int(rot.get("cycle_index", 0)) + 1
        ROTATION_PATH.write_text(json.dumps(rot, indent=2) + "\n", encoding="utf-8")

    print(f"recorded reply @{handle.lstrip('@')} replies={caps['replies']}")


if __name__ == "__main__":
    main()
