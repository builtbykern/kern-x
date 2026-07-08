#!/usr/bin/env python3
"""Build state/week-current.json from marketplace listings (Sunday job)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import CONFIG_DIR, STATE_DIR, load_config

DAY_KEYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
DAY_TYPES = {
    "mon": "clip",
    "tue": "insight",
    "wed": "spotlight",
    "thu": "take",
    "fri": "before_after",
    "sat": "ecosystem",
    "sun": "recap",
}

DEFAULT_HOOKS = {
    "clip": "one control that fixes scroll jank in framer",
    "insight": "shared colors as source of truth across code components",
    "take": "marketplace reviews reward depth over preset count",
    "before_after": "before/after: inertia grid vs static gallery",
    "ecosystem": "sustained shipping beats one-off launches in the creator ecosystem",
    "recap": "week in framer components: what shipped and what broke",
}

CAPS_PATH = STATE_DIR / "daily-caps.json"


def iso_week_id(d: date) -> str:
    return f"{d.isocalendar().year}-W{d.isocalendar().week:02d}"


def parse_listing(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if path.name.startswith("_"):
        return None
    component = path.stem.replace("_Listing", "")
    title_match = re.search(r"^#\s+(.+)$", text, re.M)
    if title_match and "Kern_" in title_match.group(1):
        kern_m = re.search(r"(Kern_\w+)", title_match.group(1))
        if kern_m:
            component = kern_m.group(1)
    launch_m = re.search(r"Launch Price.*?\*\*\s*\$?([\d.]+)", text, re.I)
    final_m = re.search(r"Final Price.*?\*\*\s*\$?([\d.]+)", text, re.I)
    link_m = re.search(r"https?://[^\s\)>]+framer[^\s\)>]*", text, re.I)
    tagline_m = re.search(r"^## Tagline\s*\n+(.+)$", text, re.M)
    return {
        "component": component,
        "listing_file": path.name,
        "launch_price": float(launch_m.group(1)) if launch_m else 2.5,
        "final_price": float(final_m.group(1)) if final_m else 5.0,
        "link": link_m.group(0) if link_m else "",
        "tagline": tagline_m.group(1).strip() if tagline_m else "",
    }


def load_components(listings_dir: Path) -> list[dict]:
    items: list[dict] = []
    if not listings_dir.is_dir():
        return items
    for path in sorted(listings_dir.glob("*.md")):
        parsed = parse_listing(path)
        if parsed:
            items.append(parsed)
    return items


def build_day_plan(day_key: str, components: list[dict], comp_index: int) -> dict:
    day_type = DAY_TYPES[day_key]
    comp = components[comp_index % len(components)] if components else None
    plan: dict = {
        "type": day_type,
        "component": None,
        "link": False,
        "hook": DEFAULT_HOOKS.get(day_type, "framer craft note"),
        "thread_allowed": day_key == "tue",
        "forbid_mention_in_replies": False,
    }
    if day_type == "spotlight" and comp:
        plan["component"] = comp["component"]
        plan["link"] = comp["link"] or False
        plan["price_launch"] = comp["launch_price"]
        plan["price_final"] = comp["final_price"]
        plan["hook"] = comp["tagline"] or plan["hook"]
        plan["forbid_mention_in_replies"] = True
    elif day_type in ("clip", "before_after") and comp:
        plan["component"] = comp["component"]
        plan["hook"] = f"{comp['component']}: {plan['hook']}"
    return plan


def main() -> None:
    parser = argparse.ArgumentParser(description="Build kern-x week state JSON")
    parser.add_argument("--week", help="ISO week id e.g. 2026-W21 (default: current)")
    parser.add_argument("--start", help="Week start date YYYY-MM-DD (Monday)")
    parser.add_argument(
        "--keep-counters",
        action="store_true",
        help="Do not reset daily-caps or query-rotation.cycle_index",
    )
    args = parser.parse_args()

    cfg = load_config()
    listings_dir = Path(cfg.get("listings_dir", ""))
    if not listings_dir.is_dir():
        print(
            f"ERROR: listings_dir not found: {listings_dir}\n"
            f"Copy config/local.example.json → config/local.json and set listings_dir.",
            file=sys.stderr,
        )
        sys.exit(1)

    today = date.today()
    monday = today - timedelta(days=today.weekday())
    if args.start:
        monday = date.fromisoformat(args.start)
    week_id = args.week or iso_week_id(monday)

    components = load_components(listings_dir)
    days: dict[str, dict] = {}
    for i, key in enumerate(DAY_KEYS):
        days[key] = build_day_plan(key, components, i)

    today_key = DAY_KEYS[today.weekday()]
    today_plan = days[today_key].copy()

    payload = {
        "week": week_id,
        "built_at": today.isoformat(),
        "challenge_mode": False,
        "days": days,
        "today_key": today_key,
        "today": today_plan,
    }

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = STATE_DIR / "week-current.json"
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if not args.keep_counters:
        rotation_path = STATE_DIR / "query-rotation.json"
        if rotation_path.is_file():
            rot = json.loads(rotation_path.read_text(encoding="utf-8"))
            rot["cycle_index"] = 0
            rotation_path.write_text(json.dumps(rot, indent=2) + "\n", encoding="utf-8")

        if CAPS_PATH.is_file():
            caps = json.loads(CAPS_PATH.read_text(encoding="utf-8"))
            if caps.get("date") != today.isoformat():
                caps["date"] = today.isoformat()
                caps["posts"] = 0
                caps["replies"] = 0
                CAPS_PATH.write_text(json.dumps(caps, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {out_path} (week={week_id}, today={today_key}, components={len(components)})")


if __name__ == "__main__":
    main()
