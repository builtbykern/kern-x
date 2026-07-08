#!/usr/bin/env bash
# Prefer daemon (browser stays open). One-shot fallback: x_reply_cycle.py per tick.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p logs

if [[ -f .env ]]; then set -a; source .env; set +a; fi

if [[ "${X_USE_DAEMON:-1}" == "1" ]]; then
  echo "[schedule] starting x_reply_daemon.py (browser stays open)"
  exec python3 scripts/x_reply_daemon.py >> logs/x-cycle.log 2>> logs/x-cycle.err
fi

MIN_SEC=$((60 * 60))
MAX_SEC=$((90 * 60))
RANGE=$((MAX_SEC - MIN_SEC))

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a logs/x-cycle.log; }

log "KERN-Reply one-shot loop (opens/closes browser each tick)"
while true; do
  SLEEP_SEC=$((MIN_SEC + RANDOM % (RANGE + 1)))
  log "running x_reply_cycle.py"
  python3 scripts/x_reply_cycle.py >> logs/x-cycle.log 2>> logs/x-cycle.err || log "cycle failed"
  log "sleep ${SLEEP_SEC}s"
  sleep "$SLEEP_SEC"
done
