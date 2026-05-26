# Cursor setup — kern-x

Open **`/Users/noel_/Desktop/kern-x`** as its own Cursor workspace (File → Open Folder).

## 1. Config

```bash
cp config/local.example.json config/local.json
python3 scripts/build_week.py
python3 scripts/trim_logs.py --check
```

## 2. Two agents (recommended)

Create **two** Cursor Automations or saved Agent profiles:

| Name | System / permanent context | User message each run |
|------|---------------------------|------------------------|
| **KERN-Post** | Paste full `runtime/post.RUN.md` | Contents of `prompts/cron-post.txt` |
| **KERN-Reply** | Paste full `runtime/reply-cycle.RUN.md` | Contents of `prompts/cron-reply.txt` |

Do not attach BuiltByKern repo. Only this workspace.

## 3. X session (browser)

Execution uses **browser** (Cursor Browser MCP or manual):

1. Log in as **@builtbykern** in the browser Cursor controls.
2. Agent searches/posts per RUN steps.
3. After each action, run `record_post.py` / `record_reply.py` from repo root.

Without a logged-in session, runs must stop with `error` — no retries.

## 4. Scheduling

### Option A — Cursor Automations (cloud)

- **Post:** once daily ~09:00 local, model fast, workspace = kern-x, message = `cron-post.txt`
- **Reply:** every 60–90 min (or chain: automation ends with “schedule next in 75m”), message = `cron-reply.txt`

Draft workflow shapes: `automations/README.md`

### Option B — `/loop` (local, Mac awake)

```text
/loop 75m Run runtime/reply-cycle.RUN.md per prompts/cron-reply.txt. Browser X @builtbykern.
```

Morning one-shot post (no loop):

```text
Run runtime/post.RUN.md per prompts/cron-post.txt
```

## 5. Sunday

```bash
python3 scripts/build_week.py
```

Then optional `docs/weekly-review.md` (manual, not cron).

## 6. Token budget

Target ~9–10k tokens/day: allowlist only, no `docs/strategy.md` in cron.
