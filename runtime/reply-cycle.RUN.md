# reply-cycle.RUN — @builtbykern engagement (token-minimal)

ALLOWLIST: `state/daily-caps.json`, `state/cooldown-handles.json`, `state/query-rotation.json`, `state/week-current.json`, `voice/voice-compact.txt`, `logs/replies.json` (last 20 entries). No other files. No repo search.

## Steps

1. Read `state/daily-caps.json`. If `replies >= cap_replies` → output `posted_n: 0` / `skipped_n: cap` and stop.
2. Read `state/week-current.json` → `today.forbid_mention_in_replies`, `today.component`.
3. Read `voice/voice-compact.txt`.
4. Read `state/query-rotation.json`. Search from `pool[cycle_index]`; if thin, try next queries in pool (last 4h only). Stop at first batch with candidates.
5. Shortlist max **5** candidates (media or specific craft detail preferred).
6. Dedup each candidate:
   - handle in `state/cooldown-handles.json` (within `until`) → skip `dup`
   - handle in last 20 `logs/replies.json` entries → skip `dup`
   - if `forbid_mention_in_replies` and post mentions `today.component` → skip `coord`
7. Post max **3** replies. English only. 1 sentence (voice-compact). Name one observable detail; optional short question if it invites author reply-back (X algo favors two-way threads). Empathy on struggle posts (slow sales, rejection, burnout) — validate, no advice. Encourage template/component/challenge ships per voice-compact.
8. Referral link (max **1** per cycle): Cursor (`https://cursor.com/referral?code=WHBU5CRP1XKF` exactly) or Framer (`framer_referral_url` — builder choice posts). No Hostinger / no Framer hosting searches (Framer auto-hosts). Only when voice-compact fits. Never on empathy posts.
9. Never: emoji, `!`, other links, self-promo, `@builtbykern` plug, banned words from voice-compact.
10. Wait 45–120s between replies.
11. Append each to `logs/replies.json`. Add handle to `cooldown-handles` (+7d). Increment `daily-caps.replies`. Increment `query-rotation.cycle_index`.
12. After cycle completes, run `scripts/x_reply_back_check.py --recent 10` to detect author reply-backs (no LLM cost).

Optional helpers per reply: `python3 scripts/record_reply.py ...` (last reply of cycle: add `--bump-rotation`).

## Output (exactly 6 lines)

```
posted_n: <0-3>
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
