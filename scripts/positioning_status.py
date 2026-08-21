#!/usr/bin/env python3
"""Print the human positioning board vs live repo state. Does not post."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import ROOT, STATE_DIR, LOGS_DIR  # noqa: E402

DAY_KEYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def iso_week_id(d: date) -> str:
    cal = d.isocalendar()
    return f"{cal.year}-W{cal.week:02d}"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def exists_line(path_str: str) -> str:
    if not path_str or path_str.startswith("docs/") or "lummi.ai" in path_str:
        return path_str
    p = Path(path_str)
    if p.is_file():
        return f"ok  {path_str}"
    return f"MISSING  {path_str}"


def main() -> int:
    today = date.today()
    want_week = iso_week_id(today)
    pos_path = STATE_DIR / "positioning.json"
    week_path = STATE_DIR / "week-current.json"
    posts_path = LOGS_DIR / "posts.json"
    skills_dir = ROOT / ".cursor" / "skills"

    pos = load_json(pos_path)
    week = load_json(week_path)
    posts = load_json(posts_path).get("entries", [])
    last = posts[-1] if posts else {}

    week_id = week.get("week")
    stale = week_id != want_week
    print(f"today        {today.isoformat()} {DAY_KEYS[today.weekday()]} {want_week}")
    print(f"week-current {week_id} today_key={week.get('today_key')} stale={stale}")
    print(f"board        {pos.get('iso_week')} updated={pos.get('updated')}")
    print(f"last X log   {last.get('date')} {last.get('type')} {last.get('component')}")
    print(f"launch in logs {pos.get('launch', {}).get('x_launch_recorded_in_logs')}")
    if stale:
        print("KERN-Post    must status: stale_week (do not ship leftover warmup)")

    expected = (
        "builtbykern",
        "x-originals",
        "framer-community",
        "contra",
        "instagram-explore",
    )
    print("skills")
    missing_skills = False
    for name in expected:
        skill = skills_dir / name / "SKILL.md"
        ok = skill.is_file()
        print(f"  {'ok' if ok else 'MISSING'}  {skill.relative_to(ROOT)}")
        missing_skills = missing_skills or not ok

    print("next")
    x = pos.get("x", {}).get("next", {})
    print(f"  X           {x.get('status')} {x.get('date')} {x.get('type')}")
    c = pos.get("community", {}).get("next", {})
    print(f"  Community   {c.get('status')} {c.get('date')} {c.get('window')} {c.get('id')}")
    k = pos.get("contra", {}).get("next", {})
    print(f"  Contra      {k.get('status')} {k.get('date')} {k.get('surface')}")
    print("  Instagram   explore first_batch (human)")

    ig_batch = pos.get("instagram", {}).get("first_batch") or []
    ig1 = ig_batch[0].get("source") if ig_batch else None
    ig3 = ig_batch[2].get("source") if len(ig_batch) > 2 else None
    print("media")
    for label, path in (
        ("community video", c.get("video")),
        ("letterroll video", pos.get("community", {}).get("after_that", {}).get("video")),
        ("ig reel 1", ig1),
        ("ig reel 3", ig3),
    ):
        if path:
            print(f"  {label:18} {exists_line(str(path))}")
    for still in c.get("stills_optional") or []:
        print(f"  {'still':18} {exists_line(still)}")

    if missing_skills:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
