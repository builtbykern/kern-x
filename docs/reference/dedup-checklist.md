# Dedup checklist for Accio Work (REFERENCE)

> **Runtime:** prefer `Accio/state/cooldown-handles.json` + last 20 lines of `Accio/kern_replies.json` per [`runtime/reply-cycle.RUN.md`](runtime/reply-cycle.RUN.md). Use this file for manual fallback.

Purpose: prevent `@builtbykern` from looking automated by replying too often to the same person or same thread.

## Required check before every reply

1. Open `https://x.com/builtbykern/with_replies`.
2. Search or visually inspect recent replies for the candidate author handle.
3. Skip candidate if `@builtbykern` replied to that handle in the last **48 hours**.
4. Open the candidate post URL.
5. Skip candidate if `@builtbykern` already replied anywhere in that same root thread.
6. If the browser cannot confirm either condition, skip the candidate.

## What counts as duplicate

- Same exact post URL.
- Same root thread, even if the candidate is a nested reply.
- Same author within 48 hours.
- Same sentence skeleton already used today.

## Recommended local log

Accio should keep this per-cycle log in its own workspace:

```text
date:
cycle_start:
cycle_end:
candidate_url:
candidate_handle:
decision: posted | skipped
reason_if_skipped: dup_handle | dup_thread | thin | off_topic | risky | browser_error
reply_url:
reply_text:
```

## Escalation

Stop the cycle and report if:

- X shows a suspicious activity warning.
- X asks for verification.
- The profile switches to a different account.
- The browser cannot load `with_replies`.
