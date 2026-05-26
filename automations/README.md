# Cursor Automations (draft)

Create in [cursor.com/automations](https://cursor.com/automations) with workspace root = **kern-x**.

## KERN-Post (daily)

- **Trigger:** Schedule cron `0 9 * * *` (adjust TZ)
- **Model:** fast/cheaper OK (allowlist is small)
- **Prompt:** file `prompts/cron-post.txt`
- **Rules:** enable repo `cursor/rules/kern-x-runtime.mdc`

## KERN-Reply (recurring)

- **Trigger:** Schedule every 75m OR manual chain (“after run, note next run in 75–105m”)
- **Prompt:** `prompts/cron-reply.txt`
- **Jitter:** vary 45–90m between cycles in automation description

## Privacy

Automations need storage-eligible privacy mode. Browser X login is **local** unless you use cloud browser — prefer local IDE + `/loop` if cloud cannot hold X session.

## Prefill

Use Cursor MCP `build_automation_prefill_url` after you finalize workflow JSON in the UI once, then store a copy under `automations/` for version control (optional).
