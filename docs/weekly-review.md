# Weekly review — @builtbykern X (manual)

Run **Sunday** after `python3 scripts/build_week.py`. Use Cursor chat in kern-x workspace — not a cron job.

## Metrics

- Posts published vs `cap_posts` (7/week target)
- Replies vs `cap_replies` ramp
- `dup` / `thin` / `coord` skip rates from cycle outputs
- Handles in `state/cooldown-handles.json` growth

## Adjust

- `cap_replies` in `state/daily-caps.json` per strategy table
- `state/query-rotation.json` pool if search quality drops
- Listing spotlight day: edit `state/week-current.json` `days.wed` if needed

## Rebuild week

```bash
python3 scripts/build_week.py
python3 scripts/trim_logs.py
```
