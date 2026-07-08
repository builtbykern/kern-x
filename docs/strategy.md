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
| B — Replies | `reply-cycle.RUN.md` | 14–20 cycles/day (60–90 min jitter), max 3 replies/cycle | Never |

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

## Phoenix-aware engagement (May 2026)

Based on xAI's open-source X algorithm release. See [`docs/x-algorithm-engagement.md`](x-algorithm-engagement.md) for full notes.

**Core insight:** an author replying back to your reply carries ~150× the weight of a like in the Phoenix ranking model. Two-way threads are the #1 signal.

**Reply strategy:**
- Write so the author might reply back — short reaction + optional tiny question
- Empathy on struggle posts (validate, no advice, no questions)
- Referral max 1 link/cycle (Cursor or Framer only — when the post topic matches; see voice-compact), never combined with a question
- Implicit tease of own work (1st person, no link) max 1/cycle
- 7-day cooldown per handle (Phoenix author diversity penalty)

**Originals strategy:**
- Thu/Sat/Sun posts end with an open question to invite builder replies
- Mon/Wed/Fri focus on craft observation, no forced question
- Wednesday spotlight enters "warm" — Mon/Tue replies already boosted the profile

**Metrics:**
- Author reply-back rate (target ≥ 25%, tracked by `scripts/x_reply_back_check.py`)
- Referrals/day (tracked in `state/daily-caps.json`, cap: 2)

## Launch sync

On launch day set `today.type` to `launch` in `week-current.json` after `build_week.py`. Lane B must not mention listing that day (`forbid_mention_in_replies`).
