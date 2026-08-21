# Strategy — @builtbykern X (human / Sunday)

> Cron agents do **not** load this file. Runtime: `runtime/*.RUN.md` + `state/*.json`.
>
> Multi-channel positioning (X originals, Community, Contra, Instagram): `.cursor/skills/builtbykern/SKILL.md` (human chats). This file stays X-only.

## Account

- **Handle:** `@builtbykern`
- **Niche:** Framer code components, Marketplace craft, motion
- **Language:** English only

## Dual lanes

| Lane | Runtime | Frequency | Links |
|------|---------|-----------|-------|
| A — Originals | `post.RUN.md` | 1/day | Copy-linkable craft; demo video when it is the product (≥10s); listing URL only as self-reply CTA |
| B — Replies | `reply-cycle.RUN.md` | 14–20 cycles/day (60–90 min jitter), max 1 reply/cycle | Never (except allowed referral max 1/cycle) |

## Weekly calendar

| Day | Type | Link |
|-----|------|------|
| Mon | clip | No (video attach) |
| Tue | insight (thread max 3 if allowed) | No |
| Wed | spotlight | Video attach; listing URL optional in reply to self, not as sole media |
| Thu | take | No |
| Fri | before_after | No (video attach) |
| Sat | ecosystem | No sell |
| Sun | recap | Optional soft CTA |

Built by `scripts/build_week.py` from BuiltByKern listings path in `config/local.json`.

Demo MP4s (when present): Framer listings path `docs/projects/listings/*_demo*.mp4` (see `config/local.json`).

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

## For You scoring (Aug 2026 defaults)

Based on [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) `param.rs`. Full table + caveats: [`docs/x-algorithm-engagement.md`](x-algorithm-engagement.md).

**Core insight:** copy-link (20) and mutual replies (20) dwarf likes (0.5). Profile click and binary dwell are **0**. VQV is 0.05. Weights multiply *P(action)* for that viewer, not raw counts. Only Home-served engagement counts.

**Reply strategy:**
- Write so the author might reply back — short reaction + optional tiny question. Mutuals are 4× a stranger reply.
- Follow-ups off by default (`X_REPLY_FOLLOWUPS`). If on: **one** short continue when `author_replied` (no link, no bait) — max 1/cycle
- Empathy on struggle posts (validate, no advice, no questions)
- Referral max 1 link/cycle (**Framer only** — builder-choice posts; see voice-compact). Cursor referral program ended — no cursor.com/referral links. Never combine referral + question
- Implicit tease of own work (1st person, no link) max 1/cycle
- Conversation-first candidates (questions, builder-choice, shipping); media is a tiebreaker. Last 4h only
- 7-day cooldown per handle (author diversity)

**Originals strategy:**
- **Cadence: 1 original/day** (`cap_posts: 1`). Do **not** burst 2–3 originals in minutes — same-author reach decays and buries the weaker posts.
- Catch-up (missed Arbour slot): post **alone**, or ≥**4–6h** away from today’s original — never Arbour+Arbour+component in one blast.
- Same-day Arbour WIP **+** one Marketplace drop is OK **rarely** (see Aug 1) — space them; never stack two Arbour beats the same morning.
- During Arbour warmup: daily slot = Arbour from queue. Marketplace extras (Hold Confirm, Morph Dropdown, …) = other day **or** late offset, not on top of the Arbour post in the same burst.
- **Copy-link first:** `insight` / `take` / `ecosystem` as pasteable lists or named recipes. People save those.
- `clip` / `before_after` / `spotlight`: attach demo video when the asset exists (≥10s if possible) because it *is* the product — not for VQV. Never link-only Marketplace OG as the only media.
- After posting, **stay 30–60 min** and reply on your own thread (human; not cron).
- Discovery tags (light): end originals with **1–2** hashtags when Framer-relevant — prefer `#Framer` plus one of `#FramerTemplate` / `#FramerMarketplace` / `#FramerChallenge` (only if true). Optional soft `@framer` once when natural — never tag spam, never bait.
- Thu/Sat/Sun posts end with an open question to invite builder replies
- Mon/Wed/Fri focus on craft observation, no forced question
- Wednesday spotlight enters "warm" — Mon/Tue replies already boosted the profile
- If a burst already shipped: leave posts up; resume **1/day** next — don’t delete to “fix”

**Metrics:**
- Author reply-back rate (target ≥ 25%, tracked by `scripts/x_reply_back_check.py` → `state/reply-back-stats.json`) — this is the 20-weight mutual-reply loop
- Copy-link proxies: quotes, “saved this”, people repeating the list
- Referrals/day (tracked in `state/daily-caps.json`, cap: 2)
- Do **not** use likes or video-view counts as For You health

## Launch sync

On launch day set `today.type` to `launch` in `week-current.json` after `build_week.py`. Lane B must not mention listing that day (`forbid_mention_in_replies`).

## Arbour template warmup (WIP)

Multi-day media + copy schedule (no launch posts): [`docs/arbour-warmup.md`](arbour-warmup.md) + `state/arbour-warmup-queue.json`. After `build_week.py`, run `python3 scripts/apply_arbour_warmup.py` so day slots keep Arbour clips/stills and paste-ready English copy. **Do not post** the live preview / template URL (`arbour.framer.website`) until launch — video/stills + tags only.
