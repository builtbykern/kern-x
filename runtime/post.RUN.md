# post.RUN — @builtbykern daily original (token-minimal)

ALLOWLIST: `state/week-current.json`, `state/daily-caps.json`, `voice/voice-compact.txt`, `logs/posts.json` (last 7 entries only). No other files. No repo search.

## Steps

1. Read `state/daily-caps.json`. If `posts >= cap_posts` → output `status: capped` and stop.
2. Read `state/week-current.json` → `today` (type, component, link, hook, price_launch, thread_allowed).
3. Read `voice/voice-compact.txt`.
4. Read last 7 entries of `logs/posts.json`. Skip if same `component` or same `hook` in last 7 days → `status: dup_skip`.
5. Compose **one English tweet** from `today`:
   - `clip` / `before_after`: hook + optional media attach
   - `insight`: 1 tweet OR thread max 3 only if `thread_allowed: true`
   - `spotlight` / `launch`: component + one concrete benefit + `today.link` if set
   - `ecosystem` / `recap` / `take`: no sell on Sat; no link unless `today.link` set
6. Open `https://x.com/builtbykern` — confirm not duplicate topic visually.
7. Post. Append to `logs/posts.json`: `{date, post_url, type, component, had_link, text}`.
8. Set `daily-caps.posts` += 1.

Optional helper (same effect as steps 7–8): `python3 scripts/record_post.py --url ... --type ... --component ... --had-link true|false --text "..."`

## Output (exactly 4 lines, no more)

```
status: posted|dup_skip|capped|error
url: <post url or none>
component: <name or none>
chars: <n>
```

## Stop

Login, captcha, verification, suspicious activity → `status: error` and stop. Do not retry.
