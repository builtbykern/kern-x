# Post dedup checklist — @builtbykern originals

Runtime: handled in [`runtime/post.RUN.md`](runtime/post.RUN.md). Use this for manual checks.

## Before every original post

1. Read last **7** entries in [`Accio/kern_posts.json`](../../Accio/kern_posts.json).
2. Skip if same `component` or same `hook` in last 7 days.
3. Open `https://x.com/builtbykern` — confirm topic not already posted this week.
4. If unsure, skip.

## What counts as duplicate

- Same component name within 7 days.
- Same hook string within 7 days.
- Same launch URL within 14 days.

## After posting

Append one entry:

```json
{
  "date": "YYYY-MM-DD",
  "post_url": "https://x.com/builtbykern/status/...",
  "type": "spotlight",
  "component": "Kern_InertiaGrid",
  "had_link": true,
  "text": "..."
}
```

Keep max **50** entries (delete oldest).

## Coordination with replies

If `week-current.json` → `today.forbid_mention_in_replies: true`, reply agent must not mention that component today.
