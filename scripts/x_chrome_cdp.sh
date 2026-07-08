#!/usr/bin/env bash
# Google Chrome for kern-x (remote debugging). Uses a dedicated profile so your
# daily Chrome can stay open — log in as @builtbykern once in THIS window.
set -euo pipefail

PORT="${X_CDP_PORT:-9222}"
PROFILE="${X_CHROME_PROFILE:-$HOME/.kern-x-chrome}"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

if [[ ! -x "$CHROME" ]]; then
  echo "ERROR: Google Chrome not found at $CHROME"
  exit 1
fi

mkdir -p "$PROFILE"

if curl -sf "http://127.0.0.1:${PORT}/json/version" >/dev/null 2>&1; then
  echo "Chrome CDP already listening on port $PORT"
  open -a "Google Chrome" "https://x.com/home" 2>/dev/null || true
  exit 0
fi

echo "Starting Chrome (port $PORT)"
echo "Profile: $PROFILE"
echo "→ Log in as @builtbykern in this window (once)."
echo "→ Leave this Chrome open; run ./scripts/start_kern_reply.sh in another terminal."

exec "$CHROME" \
  --remote-debugging-port="$PORT" \
  --user-data-dir="$PROFILE" \
  "https://x.com/home"
