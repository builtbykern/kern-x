# Accio Skill — engagement cycle (DEPRECATED for cron)

> **Use instead:** [`runtime/reply-cycle.RUN.md`](runtime/reply-cycle.RUN.md)  
> Cron payload: see [`builtbykern-reply-guy-agent.md`](builtbykern-reply-guy-agent.md).

This file kept as human-readable summary only. Do not paste into Accio jobs (too many tokens).

## Summary

- Account: `@builtbykern`, English only, replies only, no links.
- Read state: `Accio/state/daily-caps.json`, `cooldown-handles.json`, `query-rotation.json`, `week-current.json`.
- One search query per cycle; max 3 replies; 45–120s between replies.
- Dedup via JSON logs, not full `with_replies` unless conflict.
- Output: 6 lines per `reply-cycle.RUN.md`.

## Caps

See `daily-caps.json` (`cap_replies` default 32).

## Voice

[`voice-compact.txt`](voice-compact.txt)
