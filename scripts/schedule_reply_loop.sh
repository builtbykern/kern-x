#!/usr/bin/env bash
# Prefer daemon (browser stays open). Python loads .env itself via load_dotenv().
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p logs

export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:${PATH:-}"
export HOME="${HOME:-/Users/noel}"

PYTHON_BIN="/usr/bin/python3"
if [[ -x /opt/homebrew/bin/python3 ]]; then
  PYTHON_BIN="/opt/homebrew/bin/python3"
elif [[ -x /usr/local/bin/python3 ]]; then
  PYTHON_BIN="/usr/local/bin/python3"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [schedule] starting via ${PYTHON_BIN}" >> logs/x-cycle.log

if [[ "${X_USE_DAEMON:-1}" == "1" ]]; then
  exec "${PYTHON_BIN}" scripts/x_reply_daemon.py >> logs/x-cycle.log 2>> logs/x-cycle.err
fi

MIN_SEC=$((60 * 60))
MAX_SEC=$((90 * 60))
RANGE=$((MAX_SEC - MIN_SEC))

while true; do
  SLEEP_SEC=$((MIN_SEC + RANDOM % (RANGE + 1)))
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] running x_reply_cycle.py --storage" >> logs/x-cycle.log
  "${PYTHON_BIN}" scripts/x_reply_cycle.py --storage >> logs/x-cycle.log 2>> logs/x-cycle.err || true
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] sleep ${SLEEP_SEC}s" >> logs/x-cycle.log
  sleep "$SLEEP_SEC"
done
