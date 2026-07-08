# X automation architecture — kern-x

## Why Cursor Browser MCP fails

| | Cursor IDE browser | Your Chrome |
|--|-------------------|-------------|
| Process | Cursor webview | Google Chrome |
| Session | Empty / fragile | @builtbykern logged in |
| Agent access | Yes (MCP) | **No** |

Full automation cannot rely on Cursor’s browser tab.

## Recommended stack (local Mac)

```
launchd / schedule_reply_loop.sh
        ↓
scripts/x_reply_daemon.py   ← browser stays open between cycles
        ↓
scripts/x_cycle_core.py     ← one search + replies per tick
```

**Why not close Chrome each cycle?** Each `x_reply_cycle.py` run used to launch and tear down Playwright — slow, flaky on X’s SPA, and felt like “closing too early”. The **daemon** keeps one tab warm; only disconnects on CDP (Chrome keeps running).

One-shot (legacy): `scripts/x_reply_cycle.py` still opens/closes unless `X_KEEP_BROWSER=1` or `X_CDP_URL`.

```
launchd / cron (legacy one-shot)
        ↓
scripts/x_reply_cycle.py   ← Playwright (persistent session)
        ↓
tools/x-browser/*.js       ← extract candidates (Accio parity)
        ↓
compose (OPENAI_API_KEY or CURSOR_API_KEY) + voice-compact.txt
        ↓
Playwright post reply + record_reply.py
```

**One-time:** `python3 scripts/x_login.py` → log in as @builtbykern → saves `state/.x-storage-state.json`.

**Each cycle:** `python3 scripts/x_reply_cycle.py` (add `--dry-run` to test without posting).

## Alternatives

### A — Playwright persistent profile (default in repo)

- Pros: Stable, headless-capable, no Cursor browser, same state/logs/RUN rules.
- Cons: One-time login; X DOM changes may need selector updates.

### B — Attach to Chrome via CDP

Start Chrome once:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --user-data-dir="$HOME/.kern-x-chrome"
```

Set `X_CDP_URL=http://127.0.0.1:9222` and use `x_reply_cycle.py --cdp` (future flag). Uses your normal Chrome engine; profile dir should be dedicated.

### C — X API v2

- Pros: No browser, best for CI.
- Cons: Developer app, OAuth, paid tier for write; rewrite posting flow.

### D — Accio desktop (legacy)

Still valid if Accio cron + browser work on your machine; kern-x state format is compatible (`migrate_from_accio.sh`).

## Scheduling

Keep jitter loop; point tick at script instead of “open Cursor browser”:

```bash
# launchd or manual
cd /path/to/kern-x && python3 scripts/x_reply_cycle.py
```

Or `/loop` with prompt: “Run `python3 scripts/x_reply_cycle.py` only; no browser MCP.”

## Env

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | Compose replies (default model `gpt-4o-mini`) |
| `CURSOR_API_KEY` | Optional: compose via Cursor SDK |
| `X_CDP_URL` | Optional: attach to Chrome remote debugging |
| `X_HEADLESS` | `1` for headless Playwright |
| `X_PAGE_SETTLE_SEC` | Pause after each navigation (default `8`) |
| `X_SEARCH_FEED_WAIT_SEC` | Max wait for search tweets to render (default `50`) |
| `X_BROWSER_CLOSE_DELAY_SEC` | Pause before closing browser (default `5`) |
| `X_NAV_TIMEOUT_MS` | Navigation timeout (default `120000`) |

## Reply voice (engagement + referral)

`voice/voice-compact.txt` drives compose:

- Encourage Framer templates, components, marketplace ships, and `#FramerChallenge` progress (specific craft, no hype words).
- Optional **Cursor referral** (`config` → `cursor_referral_url`): max 1 per cycle, only when the post is about AI tooling or Framer custom code — peer tone, not an ad.

## Token budget

Browser + compose happen in Python; Cursor agent only needed for exceptions or Sunday `build_week.py`.
