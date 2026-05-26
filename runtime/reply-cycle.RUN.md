# reply-cycle.RUN — @builtbykern engagement (token-minimal)

ALLOWLIST: `state/daily-caps.json`, `state/cooldown-handles.json`, `state/query-rotation.json`, `state/week-current.json`, `voice/voice-compact.txt`, `logs/replies.json` (last 20 entries). No other files. No repo search.

## Steps

1. Read `state/daily-caps.json`. If `replies >= cap_replies` → output `posted_n: 0` / `skipped_n: cap` and stop.
2. Read `state/week-current.json` → `today.forbid_mention_in_replies`, `today.component`.
3. Read `voice/voice-compact.txt`.
4. Read `state/query-rotation.json`. Search X **only** `pool[cycle_index % len(pool)]`, last 4 hours.
5. Shortlist max **5** candidates (media or specific craft detail preferred).
6. Dedup each candidate:
   - handle in `state/cooldown-handles.json` (within `until`) → skip `dup`
   - handle in last 20 `logs/replies.json` entries → skip `dup`
   - if `forbid_mention_in_replies` and post mentions `today.component` → skip `coord`
7. Post max **3** replies. English only. 1–2 sentences. Name one observable detail. ~25% use a short technical question.
8. Never: emoji, `!`, links, self-promo, `@builtbykern` plug, banned words from voice-compact.
9. Wait 45–120s between replies.
10. After each reply run:
    `python3 scripts/record_reply.py --handle <@user> --post-url <url> --text "<reply>"`
    On the **last** reply of the cycle add `--bump-rotation`.
    (updates cooldown, caps, log; rotation once per cycle)

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

If no strong candidate after one search → `posted_n: 0`, do not run a second search.
