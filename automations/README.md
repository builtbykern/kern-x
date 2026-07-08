# Cursor Automations — kern-x

## KERN-Reply (ready)

| Asset | Purpose |
|-------|---------|
| [`kern-reply.workflow.json`](kern-reply.workflow.json) | Workflow spec (cron, prompt, repo, browser) |
| [`kern-reply.prefill.url`](kern-reply.prefill.url) | **One-click** open Automations form (prefilled) |
| [`KERN-REPLY-SETUP.md`](KERN-REPLY-SETUP.md) | Checklist: GitHub repo, browser, TZ |
| [`kern-reply.prompt.md`](kern-reply.prompt.md) | Full prompt reference |
| [`../scripts/schedule_reply_loop.sh`](../scripts/schedule_reply_loop.sh) | Accio jitter 75–105m local loop |

### Create in UI (recommended)

1. Open [`kern-reply.prefill.url`](kern-reply.prefill.url) in browser (or paste URL in Cursor).
2. Attach **GitHub repo** `kern-x` (push repo first — see SETUP).
3. Enable **Browser** tool. Memory **off**.
4. Confirm cron `0 8-22 * * *` timezone **America/New_York** (change if needed).
5. Save automation.

`create_automation` MCP may reject proto fields; prefill URL matches what the UI expects.

### Local parity (X login)

Cloud may lack @builtbykern session. Fallback:

```text
/loop 90m Run runtime/reply-cycle.RUN.md per prompts/cron-reply-jitter.txt. Browser @builtbykern.
```

Or background: `scripts/schedule_reply_loop.sh` (75–105m jitter).

## KERN-Post (daily)

- Cron `0 9 * * *` — prompt `prompts/cron-post.txt` — context `runtime/post.RUN.md`
- Prefill: build from `kern-reply.workflow.json` pattern when needed.

## Privacy

Automations need storage-eligible privacy mode.
