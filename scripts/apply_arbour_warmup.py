#!/usr/bin/env python3
"""Overlay Arbour warmup slots onto state/week-current.json.

Run after scripts/build_week.py so Marketplace defaults do not wipe WIP media days.
Human / Sunday helper — not invoked by cron.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import ROOT, STATE_DIR

QUEUE_PATH = STATE_DIR / "arbour-warmup-queue.json"
WEEK_PATH = STATE_DIR / "week-current.json"
DAY_KEYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def resolve_media(media_root: Path, rels: list[str] | None) -> list[str]:
    out: list[str] = []
    for rel in rels or []:
        p = media_root / rel
        out.append(str(p.resolve()))
    return out


def slot_to_day_plan(slot: dict, media_root: Path) -> dict:
    media_abs = resolve_media(media_root, slot.get("media"))
    stills_abs = resolve_media(media_root, slot.get("stills_optional"))
    # WIP: never inject preview URL unless link_url is an explicit non-empty string
    # and slot.link is true (launch-ready). Default false — no arbour.framer.website on X.
    link_val: bool | str = False
    url = slot.get("link_url")
    if slot.get("link") and isinstance(url, str) and url.strip():
        link_val = url.strip()
    plan: dict = {
        "type": slot["type"],
        "component": slot.get("component") or "Arbour",
        "link": link_val,
        "hook": slot.get("hook") or "Arbour WIP",
        "thread_allowed": bool(slot.get("thread_allowed")),
        "forbid_mention_in_replies": bool(slot.get("forbid_mention_in_replies")),
        "arbour_slot_id": slot.get("id"),
        "arbour_pill": slot.get("pill"),
        "media": media_abs,
        "stills_optional": stills_abs,
        "copy": slot.get("copy") or "",
    }
    if slot.get("alt_media"):
        plan["alt_media"] = resolve_media(media_root, slot["alt_media"])
    if slot.get("alt_copy"):
        plan["alt_copy"] = slot["alt_copy"]
    return plan


def week_monday(week_id: str | None, fallback: date) -> date:
    """Resolve Monday for an ISO week id like 2026-W31."""
    if week_id:
        try:
            year_s, week_s = week_id.split("-W")
            return date.fromisocalendar(int(year_s), int(week_s), 1)
        except (ValueError, TypeError):
            pass
    return fallback - timedelta(days=fallback.weekday())


def apply_queue(
    week: dict,
    queue: dict,
    *,
    only_pending: bool,
    target_date: date | None,
    all_weeks: bool,
) -> list[str]:
    media_root = Path(queue["media_root"])
    applied: list[str] = []
    days = week.setdefault("days", {})
    today = date.today()
    monday = week_monday(week.get("week"), today)
    sunday = monday + timedelta(days=6)

    for slot in queue.get("slots", []):
        if only_pending and slot.get("status") not in (None, "pending"):
            continue
        slot_date = date.fromisoformat(slot["date"])
        if target_date is not None and slot_date != target_date:
            continue
        if not all_weeks and target_date is None:
            if slot_date < monday or slot_date > sunday:
                continue
        day_key = slot.get("day_key") or DAY_KEYS[slot_date.weekday()]
        plan = slot_to_day_plan(slot, media_root)
        days[day_key] = plan
        applied.append(f"{slot['date']} {day_key} → {slot.get('id')}")

    today_key = DAY_KEYS[today.weekday()]
    week["today_key"] = today_key
    # Prefer the queue slot whose date is literally today (avoids cross-week day_key collisions).
    today_slot = None
    for slot in queue.get("slots", []):
        if slot.get("date") == today.isoformat():
            if only_pending and slot.get("status") not in (None, "pending"):
                break
            today_slot = slot
            break
    if today_slot is not None:
        week["today"] = slot_to_day_plan(today_slot, media_root)
        days[today_key] = dict(week["today"])
    elif today_key in days:
        week["today"] = dict(days[today_key])
    week["arbour_warmup_applied_at"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    return applied


def mark_posted(queue: dict, date_str: str, url: str | None) -> str | None:
    for slot in queue.get("slots", []):
        if slot.get("date") != date_str:
            continue
        slot["status"] = "posted"
        slot["posted_at"] = date.today().isoformat()
        slot["post_url"] = url
        return slot.get("id")
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply Arbour warmup queue into week-current.json"
    )
    parser.add_argument(
        "--date",
        help="Only apply the slot for this YYYY-MM-DD (default: all pending in queue)",
    )
    parser.add_argument(
        "--include-posted",
        action="store_true",
        help="Also re-apply slots already marked posted",
    )
    parser.add_argument(
        "--mark-posted",
        metavar="DATE",
        help="Mark queue slot for DATE as posted (does not post to X)",
    )
    parser.add_argument("--url", help="Post URL when using --mark-posted")
    parser.add_argument(
        "--all-weeks",
        action="store_true",
        help="Apply every pending slot (unsafe across weeks — day_keys collide). Prefer default.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without writing files",
    )
    args = parser.parse_args()

    if not QUEUE_PATH.is_file():
        print(f"ERROR: missing {QUEUE_PATH}", file=sys.stderr)
        sys.exit(1)
    if not WEEK_PATH.is_file():
        print(
            f"ERROR: missing {WEEK_PATH} — run python3 scripts/build_week.py first",
            file=sys.stderr,
        )
        sys.exit(1)

    queue = load_json(QUEUE_PATH)
    week = load_json(WEEK_PATH)

    if args.mark_posted:
        slot_id = mark_posted(queue, args.mark_posted, args.url)
        if not slot_id:
            print(f"ERROR: no slot for date {args.mark_posted}", file=sys.stderr)
            sys.exit(1)
        if not args.dry_run:
            write_json(QUEUE_PATH, queue)
        print(f"Marked posted: {slot_id} ({args.mark_posted})")
        if args.url:
            print(f"url: {args.url}")
        return

    target = date.fromisoformat(args.date) if args.date else None
    applied = apply_queue(
        week,
        queue,
        only_pending=not args.include_posted,
        target_date=target,
        all_weeks=bool(args.all_weeks),
    )

    if not applied:
        print("No matching pending Arbour slots to apply.")
        return

    if args.dry_run:
        print("Dry run — would apply:")
        for line in applied:
            print(f"  {line}")
        print(f"today → {week.get('today_key')}: {week.get('today', {}).get('hook')}")
        return

    write_json(WEEK_PATH, week)
    print(f"Updated {WEEK_PATH.relative_to(ROOT)} ({len(applied)} day(s)):")
    for line in applied:
        print(f"  {line}")
    today = week.get("today", {})
    print(
        f"today={week.get('today_key')} type={today.get('type')} "
        f"component={today.get('component')} media={len(today.get('media') or [])}"
    )


if __name__ == "__main__":
    main()
