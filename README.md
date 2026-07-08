# kern-x

Cursor-native X automation for **@builtbykern**. Replaces Accio Work runtime with the same dual-lane system, state files, and token-minimal RUN specs.

BuiltByKern marketplace data is read from a sibling repo path (configurable).

## Lanes

| Lane | Runtime | Schedule |
|------|---------|----------|
| **A — Originals** | `runtime/post.RUN.md` | 1×/day morning |
| **B — Replies** | `runtime/reply-cycle.RUN.md` | every 60–90 min, ~14–20 cycles/day (cap 32 replies) |

**English only.** Links only when `state/week-current.json` → `today.link` is set.

## Quick start

1. Copy config: `cp config/local.example.json config/local.json` and set `listings_dir`.
2. `python3 scripts/build_week.py` (Sunday or any day).
3. **Automated replies (Google Chrome):** `./scripts/start_kern_reply.sh` — see [`docs/chrome-setup.md`](docs/chrome-setup.md).
4. Daily post: Cursor agent or future `x_post_cycle.py` — see `docs/setup-cursor.md`.

Full automation architecture: [`docs/automation-architecture.md`](docs/automation-architecture.md).

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

Full re-sync (state, logs, reference, week rebuild, JSON repair):

```bash
./scripts/migrate_from_accio.sh
```

See `MIGRATION.md`.

## Verification

```bash
python3 scripts/build_week.py
python3 scripts/trim_logs.py --check
```

See `docs/verify-checklist.md`.

## Related

Strategy reference (human): `docs/strategy.md` (from BuiltByKern `ESTRATEGIA_10`).
