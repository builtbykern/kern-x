# post.RUN — @builtbykern daily original (token-minimal)

ALLOWLIST: `state/week-current.json`, `state/daily-caps.json`, `voice/voice-compact.txt`, `logs/posts.json` (last 7 entries only). No other files. No repo search.

## Steps

1. Read `state/daily-caps.json`. If `date` is not **today** (`YYYY-MM-DD`), set `date` to today, `posts` to 0, `replies` to 0, `referrals_today` to 0, and write the file. Then if `posts >= cap_posts` → output `status: capped` and stop.
2. Read `state/week-current.json`. If `week` is not **today's ISO week** (`YYYY-Www`, e.g. 2026-W34) → output `status: stale_week` and stop. Do not compose. Do not post leftover `today.copy` / warmup.
3. Read `today` (type, component, link, hook, price_launch, thread_allowed).
4. Read `voice/voice-compact.txt`.
5. Read last 7 entries of `logs/posts.json`. Skip if same `component` or same `hook` in last 7 days → `status: dup_skip`.
6. Compose **one English tweet** from `today`:
   - If `today.copy` is set (e.g. Arbour warmup), prefer that text verbatim (still English only). Ensure it ends with **1–2** Framer discovery hashtags if missing (`#Framer` + `#FramerTemplate` / `#FramerMarketplace` / `#FramerChallenge` when true). Optional one `@framer` if natural — no hashtag walls. WIP templates: **never** append live preview / template URLs unless `today.link` is an explicit URL string (launch-ready).
   - `clip` / `before_after`: hook + **attach demo video** when available (required if asset exists). Prefer ≥10s — it is the product people copy, not a VQV play.
   - `insight`: 1 tweet OR thread max 3 only if `thread_allowed: true`. Write as a **pasteable** list or named recipe (copy-link is the top For You weight).
   - `spotlight` / `launch`: component + one concrete benefit + **attach demo video** when available. Do **not** post a Marketplace / `framer.link` URL as the only media (OG cards show static listing thumbs). Optional: soft listing link in a reply to self after the video post — **conversion, not ranking** (profile click weight is 0).
   - `ecosystem` / `recap` / `take`: no sell on Sat; no link unless `today.link` set. `take` should be copyable in one screenshot.
7. Media lookup (human / agent with filesystem):
   - If `today.media` is a non-empty list of absolute paths, attach the first existing file (prefer `.mp4`; else up to 2 stills).
   - Else if listings path in `config/local.json` has `*_demo*.mp4` matching `today.component`, attach that file.
   - Prefer MP4 ≤ ~15s.
8. Open `https://x.com/builtbykern` — confirm not duplicate topic visually.
9. Post (with video attached when step 7 found an asset). Append to `logs/posts.json`: `{date, post_url, type, component, had_link, had_video, text}`.
10. Set `daily-caps.posts` += 1.

Optional helper (same effect as steps 9–10): `python3 scripts/record_post.py --url ... --type ... --component ... --had-link true|false --text "..."`

## Output (exactly 4 lines, no more)

```
status: posted|dup_skip|capped|stale_week|error
url: <post url or none>
component: <name or none>
chars: <n>
```

## Stop

Login, captcha, verification, suspicious activity → `status: error` and stop. Do not retry.
