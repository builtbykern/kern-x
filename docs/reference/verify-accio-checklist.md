# Accio verification checklist — BuiltByKern X v2

Run once after setup, then spot-check weekly.

## Sunday build

- [ ] `python3 scripts/accio_build_week.py` exits 0
- [ ] `Accio/state/week-current.json` has `today` matching weekday
- [ ] `daily-caps.json` date is today, counters 0

## Agent setup

- [ ] `KERN-Post` context = full `runtime/post.RUN.md` only
- [ ] `KERN-Reply` context = full `runtime/reply-cycle.RUN.md` only
- [ ] Cron post job: 1-line payload (no master prompt wall)
- [ ] Cron reply job: 1-line payload

## Dry run — post (Lane A)

- [ ] Accio reads only allowlisted files
- [ ] Output is exactly 4 lines (`status`, `url`, `component`, `chars`)
- [ ] `kern_posts.json` gains one entry
- [ ] `daily-caps.posts` increments
- [ ] Tweet is English, no emoji, no `!`

## Dry run — reply (Lane B)

- [ ] One search query only (from `query-rotation.json`)
- [ ] Output is exactly 6 lines
- [ ] Max 3 replies per cycle
- [ ] `kern_replies.json` + `cooldown-handles.json` updated
- [ ] No links in replies
- [ ] No banned words (`thanks`, `solid`, `deserved`, etc.)

## Coordination

- [ ] On spotlight day, `today.forbid_mention_in_replies` is true
- [ ] Reply agent skips posts mentioning spotlight component

## Token sanity

- [ ] Cron message under 200 characters
- [ ] No `ESTRATEGIA_10` or listing files opened in run log
- [ ] Estimated daily Accio usage under ~12k tokens

## Troubleshooting

- [ ] If `cron agent runner is not initialized` → see `runtime/README.md`
