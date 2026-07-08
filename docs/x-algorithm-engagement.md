# X algorithm — engagement notes (kern-x)

Reference for reply strategy. Not used during cron allowlist runs unless added to RUN.

## Elon / xAI — May 15, 2026

Musk posted that the latest X recommendation algorithm was published open source:

- Repo: [github.com/xai-org/x-algorithm](https://github.com/xai-org/x-algorithm)
- Commit: large May 15 update (~187 files) — runnable Phoenix pipeline, mini model weights, Grox content layer
- Cadence: xAI committed to ~4-week public updates

## What matters for replies (directional)

From the open repo + community analysis (2023 weights redacted in 2026 release but still treated as directional):

| Signal | Implication for @builtbykern |
|--------|------------------------------|
| **Author replies back to your reply** | Very high value — often cited as ~150× a like (unconfirmed exact weight today) |
| Likes alone | Weak compared to real conversation |
| Repost, click, dwell | Positive but secondary to dialogue |
| Mute, block, report | Strong negative — avoid spammy or tone-deaf replies |
| Author diversity | Same account cannot dominate a feed refresh — spread replies across handles |

## Query pool (2026)

High-yield Framer queries first; `framer vs webflow`, `framer wordpress` for referral-fit posts. No hosting queries (Framer auto-hosts). Pool order in `state/query-rotation.json`. Each cycle tries queries until candidates appear (no extra LLM cost on empty searches).

## Practical playbook

1. **Start conversations, not lectures** — short reaction + optional tiny question so the author might reply back.
2. **One observable detail** — proves you read the post; fits Framer/craft niche.
3. **Empathy on hard posts** — slow sales weeks, rejections, burnout, “silence phase” — validate without fixing or coaching.
4. **No engagement bait** — banned voice words; no “thoughts?” spam.
5. **Referrals** — max 1 link/cycle (Cursor, Framer, or Hostinger — see `config/default.json` and voice-compact for when each fits).

## Sources

- [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) README (May 2026)
- Tech press summaries of May 15, 2026 release (Phoenix pipeline, two-way reply weight discussion)
