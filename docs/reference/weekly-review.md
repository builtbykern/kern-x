# Weekly review — @builtbykern X (manual, not Accio)

Run **Sunday** after `python3 scripts/accio_build_week.py`. Use Cursor or spreadsheet — do not burn Accio tokens on this.

## Data to collect

### Posts (Lane A)

- Total originals posted by day
- Impressions / engagements per post (if visible)
- Link clicks on spotlight/launch days
- Top 3 post URLs
- Worst post (lowest engagement)

### Replies (Lane B)

- Total replies by day (from `Accio/state/daily-caps.json` history or logs)
- Replies with author replies back
- New followers (Framer/design/marketplace fit)
- Top 10 reply URLs
- Zero-response patterns

### Safety

- X warnings, captcha, login prompts, reach drops

## Scoring

### Keep / expand

- Queries in `query-rotation.json` that yield media-rich Framer posts
- Post types (clip, spotlight) with above-average engagement
- Wording close to `voice-anchors.md`

### Cut / reduce

- Queries pulling hustle/finance
- Praise-only replies (`thanks`, `solid`, etc.)
- Handles appearing too often — extend cooldown
- Flat engagement for 7 days on a post type

## Volume adjustment (`daily-caps.json`)

| Signal | Action |
|--------|--------|
| No warnings + strong engagement | `cap_replies` +4 (max 50) |
| Soft warning / captcha | −40% caps for 48h |
| Reach drop | Pause replies 24h, then previous safe tier |
| Active #FramerChallenge | ensure pool includes tag; max 12 challenge replies/day |

## Posts calendar tune

Edit [`content-calendar-template.md`](content-calendar-template.md) overrides, re-run `accio_build_week.py`.

## Tune prompt (Cursor)

```text
Review last week @builtbykern X activity from kern_posts.json and kern_replies.json.

Report:
1. Posts per day and top 3 by engagement.
2. Replies per day and top 10 reply URLs.
3. Best query-rotation strings and post types to keep.
4. Phrases and handles to cool down.
5. Next week cap_replies and any launch overrides.

Keep focus: Framer code components, marketplace, motion, ecosystem support.
English only. No commercial/finance replies.
```

## Decision log

```text
Week:
Posts published:
cap_replies next week:
Best post type:
Best reply themes:
Themes to cut:
Voice fixes:
Safety notes:
```
