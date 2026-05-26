# kern-x

Cursor-native X automation for **@builtbykern**. Replaces Accio Work runtime with the same dual-lane system, state files, and token-minimal RUN specs.

BuiltByKern marketplace data is read from a sibling repo path (configurable).

## Lanes

| Lane | Runtime | Schedule |
|------|---------|----------|
| **A — Originals** | `runtime/post.RUN.md` | 1×/day morning |
| **B — Replies** | `runtime/reply-cycle.RUN.md` | every 45–90 min, 10–14×/day |

**English only.** Links only when `state/week-current.json` → `today.link` is set.

## Quick start

1. Copy config: `cp config/local.example.json config/local.json` and set `listings_dir` to your BuiltByKern listings folder.
2. Sunday (or any day): `python3 scripts/build_week.py`
3. Open this folder as a **separate Cursor workspace**.
4. Cursor Automations or `/loop` — see `docs/setup-cursor.md`.
5. Cron prompts: `prompts/cron-post.txt`, `prompts/cron-reply.txt`.

## Layout

```
kern-x/
  config/           # local.json (gitignored) + default.json
  state/            # week plan, caps, cooldown, query rotation
  logs/             # posts.json, replies.json
  runtime/          # post.RUN.md, reply-cycle.RUN.md (allowlist)
  voice/            # voice-compact.txt
  scripts/          # build_week, record_post, record_reply, trim_logs
  prompts/          # 1-line cron payloads for Cursor
  cursor/rules/     # repo agent contract
  docs/             # setup, strategy, weekly review
```

## Migrate from Accio (BuiltByKern)

Optional copy of live state/logs:

```bash
cp ../BuiltByKern/Accio/state/week-current.json state/  # or re-run build_week.py
cp ../BuiltByKern/Accio/kern_replies.json logs/replies.json
cp ../BuiltByKern/Accio/kern_posts.json logs/posts.json
cp ../BuiltByKern/Accio/state/cooldown-handles.json state/
```

## Verification

```bash
python3 scripts/build_week.py
python3 scripts/trim_logs.py --check
```

See `docs/verify-checklist.md`.

## Related

Strategy reference (human): `docs/strategy.md` (from BuiltByKern `ESTRATEGIA_10`).
