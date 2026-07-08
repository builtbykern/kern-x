# KERN-Reply — Cursor Automation setup

## 1. Push repo (required for cloud Automation)

```bash
cd /Users/noel/Desktop/kern-x
git add -A && git commit -m "kern-x: X automation runtime"
# Create GitHub repo kern-x, then:
git remote add origin git@github.com:YOUR_USER/kern-x.git
git push -u origin main
```

Update `automations/kern-reply.workflow.json` → `gitConfig.repositories[0].url` to your repo.

## 2. Create automation in Cursor

**Option A — Prefill URL (fastest)**

Open the URL from:

```bash
# Agent can regenerate via MCP build_automation_prefill_url using kern-reply.workflow.json
```

Or open: [cursor.com/automations/new](https://cursor.com/automations/new) and import `kern-reply.workflow.json` fields manually.

**Option B — MCP create**

Agent calls `create_automation` with `kern-reply.workflow.json` → confirm in Cursor UI.

## 3. Automation settings checklist

| Setting | Value |
|---------|--------|
| Name | `KERN-Reply` |
| Repo | `kern-x` branch `main` |
| Model | `composer-2.5` (or fast variant) |
| Schedule | Cron `0 8-22 * * *` TZ **America/New_York** (edit to your TZ) |
| Memory | **Off** |
| Browser tool | **On** (required) |
| Rules | Load from repo `cursor/rules/kern-x-runtime.mdc` if UI supports project rules |

## 4. X login (critical)

Cloud agents usually **do not** have your desktop X cookies.

| Environment | Works for posting replies? |
|-------------|----------------------------|
| Cloud Automation | Only if Browser tool + persistent session (often **fails**) |
| **Desktop** workspace `kern-x` + Browser MCP | **Yes** — log in @builtbykern once |
| `/loop` in kern-x workspace | **Yes** — Accio parity |

**Fallback (recommended for replies):**

```text
/loop 90m Run runtime/reply-cycle.RUN.md per prompts/cron-reply-jitter.txt. Browser: @builtbykern on X.
```

Keep cloud Automation for state/script maintenance or disable until X session works in cloud.

## 5. Jitter (Accio 75–105m)

Hourly cron ≈ 15 runs/day (8am–10pm). Accio used 10–14 cycles with jitter.

Tighter schedule examples:

- Every 90m (manual): use `/loop 90m` instead of hourly cron
- Cron `30 8-21/2 * * *` — odd hours + :30 (fewer runs)

## 6. Verify one cycle

```bash
python3 scripts/trim_logs.py --check
```

In Cursor (kern-x folder): paste `prompts/cron-reply.txt` with `runtime/reply-cycle.RUN.md` as context. Confirm 6-line output and `logs/replies.json` updates.

## 7. Disable Accio duplicate

Turn off `builtbykern-engagement-jitter` in Accio desktop cron after KERN-Reply is green.
