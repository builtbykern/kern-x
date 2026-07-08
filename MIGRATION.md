# Migration from Accio (BuiltByKern)

Completed migration sources:

- `BuiltByKern/Accio/state/*.json`
- `BuiltByKern/Accio/kern_posts.json` → `logs/posts.json`
- `BuiltByKern/Accio/kern_replies.json` → `logs/replies.json` (repaired duplicate JSON root)
- `BuiltByKern/Automation/accio-work/*` → `docs/reference/`, `tools/x-browser/`

## Path map

| Accio | kern-x |
|-------|--------|
| `Accio/state/` | `state/` |
| `Accio/kern_posts.json` | `logs/posts.json` |
| `Accio/kern_replies.json` | `logs/replies.json` |
| `Automation/accio-work/voice-compact.txt` | `voice/voice-compact.txt` |
| `Automation/accio-work/runtime/*.RUN.md` | `runtime/*.RUN.md` |
| `scripts/accio_build_week.py` | `scripts/build_week.py` |

## Re-sync anytime

```bash
./scripts/migrate_from_accio.sh
```

## BuiltByKern

Sunday week build in monorepo now delegates to kern-x — see `BuiltByKern/scripts/accio_build_week.py`.
