# kern-x — Agent instructions

Standalone repo for @builtbykern X automation. Do not treat BuiltByKern component code as in-scope unless `config/local.json` paths are explicitly needed for `build_week.py`.

## Authority

1. `runtime/post.RUN.md` and `runtime/reply-cycle.RUN.md` — cron/runtime allowlist and steps
2. `voice/voice-compact.txt` — voice contract
3. `state/*.json` — mutable runtime state
4. `docs/strategy.md` — humans/Sunday only; **not** for cron
5. `.cursor/skills/` — humans only (positioning). Hub `builtbykern` may auto-invoke in human chats. Channel skills (`x-originals`, `framer-community`, `contra`, `instagram-explore`) are explicit. **Never** load skills during KERN-Post / KERN-Reply.
6. `state/positioning.json` — this week's next beat per channel. Humans/skills only; **not** for cron.
7. `.agents/skills/` + `.agents/product-marketing.md` — marketing (copywriting, marketing-ideas, marketing-psychology, launch). Grok Bot and human chats. Read product-marketing.md first. **Never** during KERN-Post / KERN-Reply.

## Cron agents (Cursor)

| Agent | Context | Message |
|-------|---------|---------|
| KERN-Post | Full `runtime/post.RUN.md` | `prompts/cron-post.txt` |
| KERN-Reply | Full `runtime/reply-cycle.RUN.md` | `prompts/cron-reply.txt` |

## Hard rules

- English only on X output
- Read only allowlisted files per RUN spec
- No repo-wide search during cron runs
- After post/reply: run `scripts/record_post.py` or `scripts/record_reply.py` OR update state/logs exactly as RUN specifies
- Stop on login/captcha/verification — `status: error`, no retry
- Browser execution: user must be logged in as @builtbykern (see `docs/setup-cursor.md`)
- **One X tab only** — never open a new browser/tab for posts or replies. Reuse the daemon session (`com.builtbykern.kern-reply`) or `get_work_page`; `--storage` one-shots default to keep-browser. Do not spawn ad-hoc Chromium windows.
- **Engagement is proactive** — do not ask when to run reply cycles. Goal: max useful engagement in Framer + design. Stay within daily caps; prefer Framer/marketplace/design accounts; keep going when compose/browser is healthy.

## Sunday (human)

```bash
python3 scripts/build_week.py
python3 scripts/positioning_status.py
```

Optional: `docs/weekly-review.md`

Positioning: agent drafts paste kits from `.cursor/skills/` + `state/positioning.json`. Noel OKs and pastes. Agent never publishes. KERN-Post must `status: stale_week` when `week-current.json` is not today's ISO week. Replies cron only if Noel asks.

## Marketing (Grok Bot and human chats)

If the task is copy, ideas, psychology, or a launch, read `.agents/product-marketing.md` first, then the matching skill in `.agents/skills/`. Do not paste those files into the session. Do not use them on cron.

## Framer Community (human)

Post copy and queue: `docs/framer-community/`, `state/framer-community-catalog.json`, `state/framer-community-queue.json`.
Arbour WIP warmup (stills, offset from X): `docs/framer-community/arbour-warmup.md`, `state/arbour-community-queue.json`.
Regenerate component posts: `python3 scripts/sync_framer_community_posts.py`. Not for cron agents.

## Arbour template warmup (human)

WIP multi-day X schedule (no launch): `docs/arbour-warmup.md`, `state/arbour-warmup-queue.json`. After Sunday `build_week.py`, overlay with `python3 scripts/apply_arbour_warmup.py`. Not for cron agents unless `week-current` already has Arbour `today.copy` / `today.media`.
