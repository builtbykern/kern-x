# Cursor scheduling (Accio parity)

Accio used desktop cron + jitter reschedule. Equivalent in Cursor:

## Lane A — daily post (~09:00)

One-shot or Automation schedule. Message: `prompts/cron-post.txt`  
Context: full `runtime/post.RUN.md`

## Lane B — reply cycles (10–14/day)

**Local `/loop` (recommended while X session is in IDE browser):**

```text
/loop 90m Run runtime/reply-cycle.RUN.md per prompts/cron-reply-jitter.txt. Logged in as @builtbykern on X.
```

Jitter: vary loop interval **75–105m** by editing sleep between 4500–6300s when restarting loop.

**Accio export:** `schedule/accio-cron-export.json` (historical job definition).

## Payload parity

| Accio agent | kern-x prompt |
|-------------|---------------|
| KERN-Post | `prompts/cron-post.txt` |
| KERN-Reply | `prompts/cron-reply.txt` |
| Jitter engagement | `prompts/cron-reply-jitter.txt` |

## Token budget

~9–10k/day — do not attach `docs/reference/*` to cron; only RUN + allowlist files.
