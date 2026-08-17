# post.RUN — @builtbykern daily original (token-minimal)

ALLOWLIST: `state/week-current.json`, `state/daily-caps.json`, `voice/voice-compact.txt`, `logs/posts.json` (last 7 entries only). No other files. No repo search.

## Steps

1. Read `state/daily-caps.json`. If `posts >= cap_posts` → output `status: capped` and stop.
2. Read `state/week-current.json` → `today` (type, component, link, hook, price_launch, thread_allowed).
3. Read `voice/voice-compact.txt`.
4. Read last 7 entries of `logs/posts.json`. Skip if same `component` or same `hook` in last 7 days → `status: dup_skip`.
5. Compose **one English tweet** from `today`:
   - If `today.copy` is set (e.g. Arbour warmup), prefer that text verbatim (still English only). Ensure it ends with **1–2** Framer discovery hashtags if missing (`#Framer` + `#FramerTemplate` / `#FramerMarketplace` / `#FramerChallenge` when true). Optional one `@framer` if natural — no hashtag walls. WIP templates: **never** append live preview / template URLs unless `today.link` is an explicit URL string (launch-ready).
   - `clip` / `before_after`: hook + **attach demo video** when available (required if asset exists)
   - `insight`: 1 tweet OR thread max 3 only if `thread_allowed: true`
   - `spotlight` / `launch`: component + one concrete benefit + **attach demo video** when available. Do **not** post a Marketplace / `framer.link` URL as the only media (OG cards show static listing thumbs). Optional: soft listing link in a reply to self after the video post.
   - `ecosystem` / `recap` / `take`: no sell on Sat; no link unless `today.link` set
6. Media lookup (human / agent with filesystem):
   - If `today.media` is a non-empty list of absolute paths, attach the first existing file (prefer `.mp4`; else up to 2 stills).
   - Else if listings path in `config/local.json` has `*_demo*.mp4` matching `today.component`, attach that file.
   - Prefer MP4 ≤ ~15s.
7. Open `https://x.com/builtbykern` — confirm not duplicate topic visually.
8. Post (with video attached when step 6 found an asset). Append to `logs/posts.json`: `{date, post_url, type, component, had_link, had_video, text}`.
9. Set `daily-caps.posts` += 1.

Optional helper (same effect as steps 8–9): `python3 scripts/record_post.py --url ... --type ... --component ... --had-link true|false --text "..."`

## Output (exactly 4 lines, no more)

```
status: posted|dup_skip|capped|error
url: <post url or none>
component: <name or none>
chars: <n>
```

## Stop

Login, captcha, verification, suspicious activity → `status: error` and stop. Do not retry.
