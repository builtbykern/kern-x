# reply-cycle.RUN — @builtbykern engagement (token-minimal)

ALLOWLIST: `state/daily-caps.json`, `state/cooldown-handles.json`, `state/query-rotation.json`, `state/week-current.json`, `voice/voice-compact.txt`, `logs/replies.json` (last 20 entries), `state/reply-back-stats.json`. No other files. No repo search.

## Steps

1. Read `state/daily-caps.json`. If `date` is not **today** (`YYYY-MM-DD`), set `date` to today, `posts` to 0, `replies` to 0, `referrals_today` to 0, and write the file. Then if `replies >= cap_replies` → output `posted_n: 0` / `skipped_n: cap` and stop.
2. Read `state/week-current.json` → `today.forbid_mention_in_replies`, `today.component`.
3. Read `voice/voice-compact.txt`.
4. Read `state/query-rotation.json`. Search from `pool[cycle_index]`; if thin, try next queries in pool (last **4h** only). Stop at first batch with candidates. Prefer **conversation** (questions, builder-choice, shipping) over media-only posts.
5. Shortlist max **5** candidates (conversation-first, media as tiebreaker, then craft detail).
6. Dedup each candidate:
   - handle in `state/cooldown-handles.json` (within `until`) → skip `dup`
   - handle in last 20 `logs/replies.json` entries → skip `dup`
   - **post_url already in `logs/replies.json`** (any entry / follow-up) → skip `dup` — **max 1 reply per post**
   - if `forbid_mention_in_replies` and post mentions `today.component` → skip `coord`
7. Post max **1** reply per cycle (quality > volume; `X_MAX_REPLIES_PER_CYCLE`). English only. 1 sentence (voice-compact). Cool mood — never critical/pedantic/echo. React, don't paraphrase the post. Empathy on struggle posts — validate, no advice.
8. Referral link (max **1** per cycle): **Framer only** (`framer_referral_url` — builder choice posts). Cursor referral program ended — never paste `cursor.com/referral` links. No Hostinger / no Framer hosting searches (Framer auto-hosts). Only when voice-compact fits. Never on empathy posts.
9. Never: emoji, `!`, other links, self-promo, `@builtbykern` plug, banned words from voice-compact.
10. Wait 45–120s between replies.
11. Append each to `logs/replies.json`. Add handle to `cooldown-handles` (+7d). Increment `daily-caps.replies`. Increment `query-rotation.cycle_index`.
12. After new replies: run reply-back check (`scripts/x_reply_back_check.py` / daemon helper). Update `state/reply-back-stats.json`.
13. **Follow-ups off by default** (one reply per post — looks less automated). Only if `X_REPLY_FOLLOWUPS=1`: when `author_replied: true` and no `followup_url`, post **max 1** follow-up on the author's reply. One short continue — **no link, no bait question, no referral**. Record with `--followup-of <original_post_url> --no-cooldown`. Counts toward `cap_replies`.

Optional helpers per reply: `python3 scripts/record_reply.py ...` (last new reply of cycle: add `--bump-rotation`).

## Output (exactly 6 lines)

```
posted_n: <0-4>
urls: <comma-separated or none>
skipped_n: <n>
reasons: <dup|thin|cap|coord counts>
replies_total: <daily total>
next_query: <string searched next cycle>
```

## Stop

Login, captcha, verification, warnings → `posted_n: 0`, `reasons: error`, stop.

## Zero-quality rule

If no strong candidate after trying all queries in pool → `posted_n: 0`, `reasons: thin:N`.
