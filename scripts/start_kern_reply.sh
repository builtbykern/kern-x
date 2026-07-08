#!/usr/bin/env bash
# Start KERN-Reply with your Google Chrome (CDP) + daemon (browser stays open).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PORT="${X_CDP_PORT:-9222}"
CDP_URL="http://127.0.0.1:${PORT}"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE="${X_CHROME_PROFILE:-$HOME/.kern-x-chrome}"

mkdir -p logs

# Ensure .env has CDP URL
if [[ -f .env ]]; then
  if grep -q '^X_CDP_URL=' .env; then
    sed -i '' "s|^X_CDP_URL=.*|X_CDP_URL=${CDP_URL}|" .env 2>/dev/null || \
      sed -i "s|^X_CDP_URL=.*|X_CDP_URL=${CDP_URL}|" .env
  else
    echo "X_CDP_URL=${CDP_URL}" >> .env
  fi
else
  cat > .env <<EOF
CURSOR_API_KEY=
OPENAI_API_KEY=
X_CDP_URL=${CDP_URL}
EOF
fi

export X_CDP_URL="${CDP_URL}"
export X_USE_DAEMON=1
set -a
source .env
set +a

if ! curl -sf "${CDP_URL}/json/version" >/dev/null 2>&1; then
  echo "Chrome not on port ${PORT}. Starting in background..."
  mkdir -p "$PROFILE"
  nohup "$CHROME" \
    --remote-debugging-port="$PORT" \
    --user-data-dir="$PROFILE" \
    "https://x.com/home" \
    >> logs/chrome-cdp.log 2>&1 &
  for i in $(seq 1 30); do
    if curl -sf "${CDP_URL}/json/version" >/dev/null 2>&1; then
      echo "Chrome CDP ready."
      break
    fi
    sleep 1
  done
  if ! curl -sf "${CDP_URL}/json/version" >/dev/null 2>&1; then
    echo "ERROR: Chrome did not start. Run: ./scripts/x_chrome_cdp.sh"
    exit 1
  fi
  echo "Log in as @builtbykern in the Chrome window, then re-run this script."
  open -a "Google Chrome" "https://x.com/home" 2>/dev/null || true
  exit 0
fi

echo "Using Chrome CDP at ${CDP_URL}"
echo "Daemon starting (Ctrl+C to stop; Chrome stays open)."
mkdir -p logs
exec python3 scripts/x_reply_daemon.py 2>&1 | tee -a logs/x-cycle.log
