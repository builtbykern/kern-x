# kern-x — Agent instructions

Standalone repo for @builtbykern X automation. Do not treat BuiltByKern component code as in-scope unless `config/local.json` paths are explicitly needed for `build_week.py`.

## Authority

1. `runtime/post.RUN.md` and `runtime/reply-cycle.RUN.md` — cron/runtime allowlist and steps
2. `voice/voice-compact.txt` — voice contract
3. `state/*.json` — mutable runtime state
4. `docs/strategy.md` — humans/Sunday only; **not** for cron

## Cron agents (Cursor)

| Agent | Context | Message |
|-------|---------|---------|
| KERN-Post | Full `runtime/post.RUN.md` | `prompts/cron-post.txt` |
| KERN-Reply | Full `runtime/reply-cycle.RUN.md` | `prompts/cron-reply.txt` |

## Hard rules

- English only on X output
- Read only allowlisted files per RUN spec
- No repo-wide search during cron runs
- After post/reply: run `scripts/record_post.py` or `scripts/record_reply.py` OR update state/logs exactly as RUN specifies
- Stop on login/captcha/verification — `status: error`, no retry
- Browser execution: user must be logged in as @builtbykern (see `docs/setup-cursor.md`)

## Sunday (human)

```bash
python3 scripts/build_week.py
```

Optional: `docs/weekly-review.md`
