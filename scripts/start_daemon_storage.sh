#!/usr/bin/env bash
# Start KERN-Reply daemon using Playwright storage (no CDP). Survives when LaunchAgent hits EX_CONFIG on Desktop paths.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p logs
pkill -f 'scripts/x_reply_daemon.py' 2>/dev/null || true
sleep 1
export X_FORCE_STORAGE=1
export X_HEADLESS="${X_HEADLESS:-1}"
nohup /usr/bin/python3 scripts/x_reply_daemon.py >> logs/x-cycle.log 2>> logs/x-cycle.err &
echo "started pid=$!"
echo "logs: logs/x-cycle.log logs/x-cycle.err"
