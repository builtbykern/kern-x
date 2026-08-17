#!/usr/bin/env bash
# Thin launcher outside ~/Desktop so launchd can spawn without TCC Desktop blocks.
set -euo pipefail
ROOT="${KERN_X_ROOT:?KERN_X_ROOT not set}"
cd "$ROOT"
mkdir -p logs
export PATH="${HOME}/.local/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:${PATH:-}"
export X_FORCE_STORAGE="${X_FORCE_STORAGE:-1}"
export X_HEADLESS="${X_HEADLESS:-1}"
unset X_CDP_URL || true
if ! command -v node >/dev/null 2>&1; then
  echo "[launcher] ERROR: node not on PATH (need CURSOR_API_KEY compose)" >&2
  exit 1
fi
exec /usr/bin/python3 scripts/x_reply_daemon.py
