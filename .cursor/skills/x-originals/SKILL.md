---
name: x-originals
description: Draft @builtbykern X originals as paste kits (tweets, threads, launches, warmup, own-thread replies). Agent prepares copy; Noel OKs and pastes. Never post from the browser or x_post_original.py. Do not use for KERN-Post/KERN-Reply cron.
disable-model-invocation: true
---

# X originals — human lane

Replies to strangers = cron (`runtime/reply-cycle.RUN.md`). This skill is **originals + own-thread paste**. Never publish.

## Default posture

- **1 original / day.** Do not burst 2–3 originals in minutes.
- Output a paste block. Wait for OK. Noel pastes on x.com. Do not run `x_post_original.py` or KERN-Post.
- Cron `post.RUN.md` must `status: stale_week` when `week` is not today's ISO week. Do not treat cron as the publisher.
- After Noel pastes: they stay 45–60 min on the tweet. Agent can draft own-thread replies as extra paste if someone lands.
- English only. Voice for *originals* is punch + named move — not the one-line reply voice. Discovery tags still follow `voice/voice-compact.txt`.

## Compose checklist

1. Read `state/positioning.json` → `x.next`. If `status` is `pending` and `date` is today (or the next unshipped original), use that copy/media. Board beats `week-current.json`.
2. Else read `state/week-current.json` → `today`. If `week` is not the current ISO week, **stop** — week is stale. Do not invent a burst; do not run `build_week.py` mid-launch. Ask Noel or wait for Sunday.
3. Read last 7 `logs/posts.json` — skip same component/hook (7-day dup). If launch tweet is missing from logs, confirm on the profile before posting another original the same day.
4. Studio thesis: world + named move. Not a feature dump. Not a listing OG card as the only media.
5. Attach demo video when the asset exists (`clip` / `before_after` / `spotlight` / `launch`). Prefer ≥10s; shorter launch clips are still the product — attach anyway.
6. **No URL in the original** unless the board / `today.link` is an explicit launch URL. Marketplace / `framer.link` goes in a **self-reply** (conversion; profile-click weight is 0).
7. End with **1–2** tags when Framer-relevant: `#Framer` + `#FramerTemplate` (WIP) / `#FramerMarketplace` (live) / `#FramerChallenge` (only if true). Optional one `@framer`. No hashtag walls.
8. WIP templates: never append live preview / template URL.

## Types

| `today.type` | Shape |
|--------------|--------|
| `clip` / `before_after` | Hook + attach demo. Mon/Fri craft observation, no forced question. |
| `insight` | Pasteable list or named recipe (copy-link). Thread max 3 only if `thread_allowed`. |
| `take` | One screenshot-copyable take. Thu: end with an open builder question. |
| `spotlight` / `launch` | Named world + one concrete benefit + video. Self-reply link. |
| `ecosystem` | Sat: no sell. |
| `recap` | Sun: optional soft CTA. Open question ok. |

Copy-link and mutual replies beat likes. Do not optimize for VQV or like count. Details: `docs/x-algorithm-engagement.md` (human).

## Own-thread replies (after you post)

Stay on the tweet. Short English. No `@builtbykern` plug.

| They… | You… |
|--------|------|
| Like the look / motion | One craft beat (what took time), no lecture |
| Ask remix / how | Duplicate + what to retint / which CMS |
| Ask price / where | The `framer.link` only |
| Struggle / “congrats” | Validate; no advice, no pitch |

If nobody lands in 10 min: do not quote-tweet yourself, do not add extra bait replies.

## After Noel pastes

Noel sends the post URL. Then record only (no browser):

```bash
python3 scripts/record_post.py --url 'https://x.com/…' --type <type> --component <name> --had-link true|false --had-video true|false --text "$(cat <<'EOF'
PASTE_TWEET
EOF
)"
```

`had-link false` if the URL lives only in the self-reply.

## Week + warmup (Sunday / overlay)

```bash
python3 scripts/build_week.py
python3 scripts/apply_arbour_warmup.py   # only during template WIP warmup
```

Warmup spec: `docs/arbour-warmup.md` + `state/arbour-warmup-queue.json`. Launch paste kit: `docs/arbour-launch.md`.

Catch-up (missed slot): post **alone**, or ≥4–6h from today’s original. Never stack two Arbour beats the same morning.

## Do not

- Run a reply-cycle search from this skill
- Open a new Chromium window
- Burst Marketplace extras on top of an Arbour morning post
- Treat likes or video views as health
- Load this skill during KERN-Post cron
