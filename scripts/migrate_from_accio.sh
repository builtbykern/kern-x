#!/usr/bin/env bash
# Full migration from BuiltByKern Accio → kern-x (state, logs, reference, repair).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BBK="${BBK_ROOT:-$ROOT/../BuiltByKern}"
ACCIO="$BBK/Accio"
WORK="$BBK/Automation/accio-work"

if [[ ! -d "$ACCIO" ]]; then
  echo "ERROR: Accio not found at $ACCIO (set BBK_ROOT)"
  exit 1
fi

echo "==> state + logs"
cp -f "$ACCIO/state/"*.json "$ROOT/state/"
cp -f "$ACCIO/kern_replies.json" "$ROOT/logs/replies.json"
cp -f "$ACCIO/kern_posts.json" "$ROOT/logs/posts.json"

echo "==> repair replies JSON (Accio + kern-x)"
python3 "$ROOT/scripts/repair_replies_log.py" "$ROOT/logs/replies.json"
[[ -f "$ACCIO/kern_replies.json" ]] && python3 "$ROOT/scripts/repair_replies_log.py" "$ACCIO/kern_replies.json"

echo "==> reference docs + browser helpers"
mkdir -p "$ROOT/docs/reference" "$ROOT/tools/x-browser" "$ROOT/schedule"
cp -f "$WORK/"*.md "$ROOT/docs/reference/" 2>/dev/null || true
[[ -f "$WORK/runtime/README.md" ]] && cp -f "$WORK/runtime/README.md" "$ROOT/docs/reference/runtime-README.md"
cp -f "$WORK/"*.js "$ROOT/tools/x-browser/" 2>/dev/null || true
[[ -f "$ACCIO/.accio/cron/jobs.json" ]] && cp -f "$ACCIO/.accio/cron/jobs.json" "$ROOT/schedule/accio-cron-export.json"

echo "==> week plan from listings (keep caps + rotation)"
cp -f "$ROOT/state/daily-caps.json" /tmp/kern-x-daily-caps.json
cp -f "$ROOT/state/query-rotation.json" /tmp/kern-x-query-rotation.json
python3 "$ROOT/scripts/build_week.py" --keep-counters
cp -f /tmp/kern-x-daily-caps.json "$ROOT/state/daily-caps.json"
cp -f /tmp/kern-x-query-rotation.json "$ROOT/state/query-rotation.json"

python3 "$ROOT/scripts/trim_logs.py" --check
echo "==> done. Open $ROOT in Cursor. See docs/setup-cursor.md"
