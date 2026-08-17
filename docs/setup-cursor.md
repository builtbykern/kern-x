# Cursor setup — kern-x

Open **`/Users/noel/Desktop/kern-x`** as its own Cursor workspace (File → Open Folder).

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

**Recommended (full automation):** Playwright + persistent session — see [`automation-architecture.md`](automation-architecture.md).

```bash
pip install -r requirements-browser.txt && playwright install chromium
python3 scripts/x_login.py
export OPENAI_API_KEY=...   # or CURSOR_API_KEY
python3 scripts/x_reply_cycle.py --storage
```

**Daemon (Lane B, 60–90m):**

```bash
bash scripts/install_launchd.sh   # TCC-safe: mirrors runtime to ~/Library/Application Support
```

Re-sync after editing scripts/state: `bash scripts/sync_launchd_runtime.sh` then kickstart the agent.

Manual headless (no launchd): `./scripts/start_daemon_storage.sh`

CDP Chrome (visible window): `./scripts/start_kern_reply.sh`

**Legacy:** Cursor Browser MCP or manual post + `record_post.py` / `record_reply.py`.

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
