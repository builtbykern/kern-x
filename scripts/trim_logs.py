#!/usr/bin/env python3
"""Trim logs to max entries; --check validates JSON structure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_ENTRIES = 50


def trim_file(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    if not isinstance(entries, list):
        raise ValueError(f"{path}: entries must be a list")
    n = len(entries)
    if n > MAX_ENTRIES:
        data["entries"] = entries[-MAX_ENTRIES:]
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        return n - MAX_ENTRIES
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate only, no writes")
    args = parser.parse_args()

    ok = True
    for name in ("posts.json", "replies.json"):
        path = ROOT / "logs" / name
        if not path.is_file():
            print(f"MISSING {path}")
            ok = False
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
            print(f"OK {path}")
            if not args.check:
                trimmed = trim_file(path)
                if trimmed:
                    print(f"  trimmed {trimmed} entries")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"FAIL {path}: {e}")
            ok = False

    for name in (
        "week-current.json",
        "daily-caps.json",
        "cooldown-handles.json",
        "query-rotation.json",
    ):
        path = ROOT / "state" / name
        if not path.is_file():
            print(f"MISSING {path}")
            ok = False
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
            print(f"OK {path}")
        except json.JSONDecodeError as e:
            print(f"FAIL {path}: {e}")
            ok = False

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
