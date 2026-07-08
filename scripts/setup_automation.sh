#!/usr/bin/env bash
# One-shot setup for Playwright X automation (replies lane).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Python deps"
python3 -m pip install -q -r requirements-browser.txt
python3 -m playwright install chromium

if command -v npm >/dev/null 2>&1; then
  echo "==> Node deps (Cursor compose)"
  npm install --silent
fi

if [[ ! -f .env ]]; then
  if [[ -n "${CURSOR_API_KEY:-}" ]]; then
    cat > .env <<EOF
CURSOR_API_KEY=$CURSOR_API_KEY
OPENAI_API_KEY=
X_CDP_URL=http://127.0.0.1:9222
X_LOOP_MIN_SEC=3600
X_LOOP_MAX_SEC=5400
X_COMPOSE_MODEL=gemini-3.5-flash
EOF
    echo "==> Wrote .env from environment"
  else
    cat > .env <<'EOF'
# Cursor API key (crsr_...) — compose replies via Cursor SDK
CURSOR_API_KEY=
# Or OpenAI key (sk-...) — alternative compose backend
OPENAI_API_KEY=
X_CDP_URL=http://127.0.0.1:9222
# Daemon cycle interval (seconds): 60–90 min between reply cycles
X_LOOP_MIN_SEC=3600
X_LOOP_MAX_SEC=5400
EOF
    echo "==> Created .env — add CURSOR_API_KEY or OPENAI_API_KEY"
  fi
fi

mkdir -p logs
touch logs/x-cycle.log

if [[ -f state/.x-storage-state.json ]]; then
  echo "==> Session file exists"
else
  echo "==> Login (browser window opens)"
  python3 scripts/x_login.py
fi

echo "==> Dry-run test"
python3 scripts/x_reply_cycle.py --dry-run || true

echo ""
echo "Done. Recommended (your Google Chrome, stays open):"
echo "  ./scripts/start_kern_reply.sh"
echo "Or install launchd:"
echo "  ./scripts/install_launchd.sh"
echo "See docs/chrome-setup.md"
