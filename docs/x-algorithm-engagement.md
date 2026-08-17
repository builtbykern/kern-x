# X algorithm — engagement notes (kern-x)

Reference for reply + original strategy. Not used during cron allowlist runs unless added to RUN.

**Last review:** 2026-08-10 (Phoenix / xai-org/x-algorithm, May 2026 release + creator analyses).

## Source of truth

Musk / xAI open-sourced the For You stack:

- Repo: [github.com/xai-org/x-algorithm](https://github.com/xai-org/x-algorithm)
- Brain: **Phoenix** (Grok-based transformer) predicts per-post engagement probabilities
- Serving: Home Mixer weighted scorer + author diversity + OON + safety/Grox layers
- Cadence: xAI committed to ~4-week public updates (largest drop historically cited: May 15, 2026)

## Scoring spine (verified in code)

`Final Score ≈ Σ (weight_i × P(action_i))` then diversity / offsets.

Phoenix predicts **~19 action heads**. WeightedScorer combines them (`home-mixer/scorers/weighted_scorer.rs`), including:

| Head (examples) | Gesture |
|-----------------|---------|
| `favorite` | like |
| `reply` | compose a reply |
| `quote` / `quoted_click` | quote tweet / click into quote |
| `retweet` | repost |
| `photo_expand` | expand image |
| `click` | click (in-post / card) |
| `profile_click` | open author profile |
| `vqv` (video quality view) | video play past a **min duration** gate |
| `share` / DM / copy-link | share variants |
| `dwell` + continuous dwell time | pause / time on post in feed |
| `follow_author` | follow from the post |
| `not_interested` / `block` / `mute` / `report` | **negative** weights |

### Weight caveat (critical)

**Numeric weights are not in the open-source tree** (params like `FAVORITE_WEIGHT` are loaded at runtime / redacted).  

Ignore viral tables (“reply = 150× like”, etc.) as **unverified** against current production. Direction still holds: **dialogue + attention beat empty likes**; negatives can wipe positives.

### Video gate

`vqv_weight_eligibility`: if video is missing or shorter than `MIN_VIDEO_DURATION_MS` (secret), **VQV contributes 0**. Short autoplay loops may not earn video credit — demos in the ~8–21s range are safer than 1–2s flashes.

### Author diversity

Repeated authors in one feed candidate set are **attenuated** (first post full score; later posts decay toward a floor). Practical rule for @builtbykern: **1 original/day**; never blast 2–3 originals in minutes.

### OON

Out-of-network posts need stronger predicted engagement than in-network to surface.

## What this means for @builtbykern

| Signal | Lane A — originals | Lane B — replies |
|--------|--------------------|------------------|
| Reply / thread | Write so people answer; **be present 30–60 min** after posting and reply on your own thread | One human reply that invites author reply-back; **max 1 reply per post** (no double-tap / follow-up spam by default) |
| Dwell | Demo MP4 + craft copy; avoid link-only OG cards as sole media | Prefer media-rich candidates (last 4h) |
| VQV | Attach listing demos that clear a real watch threshold | Engage posts that already have video when possible |
| Profile click | Soft buy/preview link in **self-reply**, not the first tweet | Rare Framer referral only when voice rules fit |
| Follow | Clear niche signal (motion / Framer craft) | Don’t pitch; curiosity from the reaction |
| Negatives | No bait (“thoughts?”), no Paid disclosure by accident, no hashtag walls | No generic bot praise — concrete detail only (`voice/voice-compact.txt`) |

## Practical playbook (Aug 2026)

1. **Conversations > likes** — short reaction + optional natural question; never engagement bait.
2. **Own-post presence** — after a spotlight/clip, stay and reply to commenters (author continuity on *your* thread). Distinct from daemon follow-ups on *others’* posts (`X_REPLY_FOLLOWUPS` off by default).
3. **One observable detail** — proves you read the post; Framer/craft niche.
4. **Media first** — video/photo for originals; media-first candidate filter in reply cycles.
5. **Empathy** on struggle posts — validate, no advice, no questions.
6. **Referrals** — max 1 link/cycle, **Framer only**; never on empathy; never with a question. No Cursor referral URLs.
7. **Cadence** — `cap_posts: 1`. Same-day second original only if spaced (≥4–6h) and intentional.
8. **Self-reply soft CTA** — marketplace / `framer.link` after the video post ships.
9. **Don’t look automated** — one reply per foreign post; human voice; 7-day handle cooldown.

## Query pool

High-yield Framer / Marketplace / creator queries first; `framer vs webflow`, `framer wordpress` for referral-fit. No hosting queries (Framer auto-hosts). Pool: `state/query-rotation.json`.

## Sources

- [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) README + `weighted_scorer.rs`
- [xDoctor — May 2026 update](https://xdoctor.app/learn/updates/2026-05) (weights still redacted)
- [VoiceMoat — 19 engagement heads](https://voicemoat.com/blog/x-algorithm/phoenix-19-engagement-heads-creator-guide) (structure verified; numeric legacy tables = historical)
