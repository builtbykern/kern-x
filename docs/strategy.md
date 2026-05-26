# Strategy — @builtbykern X (human / Sunday)

> Cron agents do **not** load this file. Runtime: `runtime/*.RUN.md` + `state/*.json`.

## Account

- **Handle:** `@builtbykern`
- **Niche:** Framer code components, Marketplace craft, motion
- **Language:** English only

## Dual lanes

| Lane | Runtime | Frequency | Links |
|------|---------|-----------|-------|
| A — Originals | `post.RUN.md` | 1/day | When `today.link` set |
| B — Replies | `reply-cycle.RUN.md` | 10–14 cycles/day, max 3 replies/cycle | Never |

## Weekly calendar

| Day | Type | Link |
|-----|------|------|
| Mon | clip | No |
| Tue | insight (thread max 3 if allowed) | No |
| Wed | spotlight | Yes if listing URL |
| Thu | take | No |
| Fri | before_after | No |
| Sat | ecosystem | No sell |
| Sun | recap | Optional soft CTA |

Built by `scripts/build_week.py` from BuiltByKern listings path in `config/local.json`.

## Reply caps (edit `state/daily-caps.json`)

| Phase | `cap_replies` |
|-------|----------------|
| Days 1–3 | 24 |
| Days 4–10 | 32 |
| Steady | 36 |
| Ceiling | 50 |

## Voice

- `voice/voice-compact.txt` (runtime)
- Full examples: port from BuiltByKern `Automation/accio-work/voice-anchors.md` if needed

## Launch sync

On launch day set `today.type` to `launch` in `week-current.json` after `build_week.py`. Lane B must not mention listing that day (`forbid_mention_in_replies`).
