# X algorithm — engagement notes (kern-x)

Reference for reply + original strategy. Not used during cron allowlist runs unless added to RUN.

**Last review:** 2026-08-17 (For You defaults in `home-mixer/params/param.rs`, last sync 2026-08-12). Official drop: [X Open Source, Aug 13](https://x.com/XOpenSource/status/2087951962004230428).

## Source of truth

- Repo: [github.com/xai-org/x-algorithm](https://github.com/xai-org/x-algorithm)
- Brain: **Phoenix** predicts per-viewer action probabilities on each candidate
- Arithmetic: `RankingScorer` in `home-mixer/scorers/ranking_scorer.rs`
- Defaults: `home-mixer/params/param.rs` (feature switches can override in prod)

`Final Score ≈ Σ (weight_i × P(action_i))` then author-diversity decay / OON offsets.

## How to read the weights

Weights multiply **predicted probability** (or a continuous value like dwell seconds). They do **not** multiply raw counts.

Wrong: “1 report cancels 468 likes.”  
Right: P(report) is ~1000× rarer than P(like), so the −234 exists so that prediction can move the score at all. Mass-report raids are also limited because ranking is personalized to the viewer.

Only actions on a post **served in Home** count. Dropping a link in a group chat and having people open it does nothing.

## Defaults (Aug 2026)

Boosts that matter for @builtbykern:

| Action | Weight | Notes |
|--------|--------|--------|
| Copy link | **20.0** | Highest positive. Paste into Slack / Discord / notes. |
| Reply (mutuals) | **20.0** | `ReplyWeight` 5 + `BidirectionalFollowReplyWeightBoost` 15 |
| Reply / quote / share via DM | **5.0** | 10× a like |
| Follow from the post | **4.0** | Niche signal |
| Share (sheet) | **2.0** | |
| Repost | **1.0** | |
| Like | **0.5** | Noise. Do not optimize for this. |
| Click | **0.4** | In-post click |
| Open link | **0.2** | |
| Photo expand / video open / VQV | **0.05** | VQV only if video ≥ `MinVideoDurationMs` (**10s** default) |
| Continuous dwell | **0.004** | |
| Binary dwell | **0.0** | Unused |
| Profile click | **0.0** | Bio / profile taps do not move For You |

Penalties (same “P(action)” caveat):

| Action | Weight |
|--------|--------|
| Report | −234 |
| Mute | −58.8 |
| Not interested | −43.2 |
| Block | −31.2 |
| Not dwelled | −0.02 |

## What we were over-indexing

| Old playbook | Code |
|--------------|------|
| Demo MP4 for VQV / dwell | VQV 0.05, binary dwell 0. Profile click 0. Video is craft proof + copy-link bait, not a ranking hack. |
| “Click my profile” / self-reply as algo | Self-reply marketplace link is **conversion**, not For You. |
| Media-first reply candidates | Media is a weak ranking head. Conversation (reply / quote / copy-link) is the product. |
| Likes as a health metric | 0.5. Ignore. |

## Author diversity + OON

Repeated authors in one candidate set are attenuated. **1 original/day.** Never blast 2–3 originals in minutes.

Out-of-network posts need stronger predicted engagement than in-network to surface — which is why copy-link and mutual replies matter more than another like from a follower.

## What this means for @builtbykern

| Signal | Lane A — originals | Lane B — replies |
|--------|--------------------|------------------|
| Copy link (20) | Pasteable posts: named controls, short recipes, numbered notes, stills people save. Demo video when it *is* the product. | Reply on posts people will save — not a ranking play for us; relationship play. |
| Mutual reply (20) | Be present 30–60 min after posting. Reply on **your** thread. Follow people who talk Framer craft so they become mutuals. | One human reply that can get a reply-back. Mutuals > strangers. Max 1 reply per post. |
| Reply / quote / DM (5) | Thu/Sat/Sun: one natural question. No “thoughts?”. | Short reaction + optional tiny question. Follow-ups off unless `X_REPLY_FOLLOWUPS=1`. |
| Follow (4) | Clear niche (motion / Framer craft). | Don’t pitch. |
| Like (0.5) | Ignore. | Ignore. |
| Profile click (0) | Soft `framer.link` in a **self-reply** for buyers, not ranking. | Rare Framer referral only when voice rules fit. |
| Video / dwell | Attach ≥10s demo when the asset exists. Skip 1–2s flashes. Do not chase VQV. | Conversation-first; media is a tiebreaker. Last 4h only. |
| Negatives | No bait, no hashtag walls, no accidental Paid. | No generic praise. One concrete detail (`voice/voice-compact.txt`). |

## Practical playbook (Aug 2026)

1. **Copy-link > conversation > follows > everything else.** Likes, dwell, VQV, profile clicks are not the job.
2. **Own-post presence** — after a spotlight/clip, stay and reply to commenters (especially mutuals). Distinct from daemon follow-ups on *others’* posts (`X_REPLY_FOLLOWUPS` off by default).
3. **One observable detail** in every foreign reply — proves you read it.
4. **Conversation-first candidates** — questions, builder-choice, shipping posts. Media is a tiebreaker, not a gate. Last 4h.
5. **Empathy** on struggle posts — validate, no advice, no questions.
6. **Referrals** — max 1 link/cycle, **Framer only**; never on empathy; never with a question. No Cursor referral URLs.
7. **Cadence** — `cap_posts: 1`. Same-day second original only if spaced (≥4–6h) and intentional.
8. **Self-reply CTA** — marketplace / `framer.link` after the post ships. Conversion, not algo.
9. **Don’t look automated** — one reply per foreign post; human voice; 7-day handle cooldown.
10. **No engagement pods.** Home-only scoring. Don’t coordinate clicks/likes off-platform.

## Query pool

High-yield Framer / Marketplace / creator queries, plus builder-choice (`framer vs webflow`, `should I use framer`, `framer wordpress`). No hosting queries (Framer auto-hosts). Pool: `state/query-rotation.json`.

## Sources

- [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) README + `home-mixer/params/param.rs` + `ranking_scorer.rs`
- [X Open Source, Aug 13 2026](https://x.com/XOpenSource/status/2087951962004230428)
