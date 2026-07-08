# Accio Runtime (token-minimal)

Accio Work runs **only** these files per job. Do not load `ESTRATEGIA_10`, listings, or full agent REFERENCE docs in cron.

## Agents (Accio UI)

| Agent name | Permanent context | Cron message |
|------------|-------------------|--------------|
| `KERN-Post` | Paste full `post.RUN.md` | `Run Automation/accio-work/runtime/post.RUN.md. State: Accio/state/. Log: Accio/kern_posts.json. No other files.` |
| `KERN-Reply` | Paste full `reply-cycle.RUN.md` | `Run Automation/accio-work/runtime/reply-cycle.RUN.md. State: Accio/state/. Log: Accio/kern_replies.json. No other files.` |

## Token budget (target)

| Run | Per day | Tokens/run |
|-----|---------|------------|
| post.RUN | 1 | ~800–1.2k |
| reply-cycle.RUN | ~12 | ~600–900 |
| **Total** | | **~9–10k/day** |

## Sunday setup (human / Cursor)

```bash
python3 scripts/accio_build_week.py
```

Optional: `python3 scripts/accio_build_week.py --week 2026-W20`

## State files (`Accio/state/`)

| File | Purpose |
|------|---------|
| `week-current.json` | Today's slot + week plan |
| `daily-caps.json` | posts/replies counters |
| `cooldown-handles.json` | 48h handle dedup |
| `query-rotation.json` | 1 search query per cycle |

## Logs (`Accio/`)

- `kern_posts.json` — max 50 entries (trim oldest)
- `kern_replies.json` — max 50 entries (trim oldest)

## Troubleshooting

**`cron agent runner is not initialized`** — enable Accio cron runner in desktop app; ensure `@builtbykern` logged in browser; workspace `Accio/`.

**Accio reads wrong files** — cron payload must be 1-liner above; agent context = RUN file only.

**Duplicate replies** — run `accio_build_week.py` to reset week; check `cooldown-handles.json`.

## Reference (not for cron)

- `../builtbykern-original-poster-agent.md`
- `../builtbykern-reply-guy-agent.md`
- `../../Core/Framer/ESTRATEGIA_10_X_Social_Launch.md`
