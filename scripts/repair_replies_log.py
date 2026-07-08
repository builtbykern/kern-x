#!/usr/bin/env python3
"""Repair kern_replies.json / logs/replies.json with duplicate JSON roots."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "logs" / "replies.json"
MAX_ENTRIES = 50


def extract_objects(raw: str) -> list[dict]:
    pattern = re.compile(
        r'\{\s*"date"\s*:\s*"[^"]+"\s*,\s*"handle"\s*:\s*"[^"]+"\s*,\s*"post_url"\s*:\s*"[^"]+"\s*,\s*"reply_text"\s*:\s*"(?:[^"\\]|\\.)*"\s*\}',
        re.DOTALL,
    )
    entries: list[dict] = []
    for m in pattern.finditer(raw):
        try:
            entries.append(json.loads(m.group(0)))
        except json.JSONDecodeError:
            continue
    return entries


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else LOG_PATH
    raw = path.read_text(encoding="utf-8")
    entries = extract_objects(raw)
    if not entries:
        print("No entries found", file=sys.stderr)
        sys.exit(1)
    # dedupe by post_url + handle
    seen: set[tuple[str, str]] = set()
    unique: list[dict] = []
    for e in entries:
        key = (e.get("post_url", ""), e.get("handle", ""))
        if key in seen:
            continue
        seen.add(key)
        unique.append(e)
    unique = unique[-MAX_ENTRIES:]
    path.write_text(
        json.dumps({"entries": unique}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Repaired {path}: {len(unique)} entries")


if __name__ == "__main__":
    main()
