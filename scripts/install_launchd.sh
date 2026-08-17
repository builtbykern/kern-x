#!/usr/bin/env bash
# Install macOS LaunchAgent for KERN-Reply (TCC-safe: no Desktop paths at runtime).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SUPPORT_DIR="${HOME}/Library/Application Support/builtbykern-kern-x"
APP_ROOT="${SUPPORT_DIR}/runtime"
LAUNCHER="${SUPPORT_DIR}/launchd_reply_daemon.sh"
PLIST_SRC="$ROOT/schedule/com.builtbykern.kern-reply.plist"
PLIST_DST="${HOME}/Library/LaunchAgents/com.builtbykern.kern-reply.plist"

chmod +x "$ROOT/scripts/sync_launchd_runtime.sh" "$ROOT/scripts/launchd_reply_daemon.sh"
bash "$ROOT/scripts/sync_launchd_runtime.sh"

mkdir -p "$SUPPORT_DIR/logs" "${HOME}/Library/LaunchAgents"
cp "$ROOT/scripts/launchd_reply_daemon.sh" "$LAUNCHER"
chmod +x "$LAUNCHER"
xattr -c "$LAUNCHER" 2>/dev/null || true
touch "$SUPPORT_DIR/logs/x-cycle.log" "$SUPPORT_DIR/logs/x-cycle.err"

python3 - "$PLIST_SRC" "$PLIST_DST" "$APP_ROOT" "$HOME" "$SUPPORT_DIR" "$LAUNCHER" <<'PY'
import sys
from pathlib import Path
src, dst, root, home, support, launcher = sys.argv[1:]
text = Path(src).read_text(encoding="utf-8")
for k, v in {
    "__KERN_X_ROOT__": root,
    "__HOME__": home,
    "__SUPPORT_DIR__": support,
    "__LAUNCHER__": launcher,
}.items():
    text = text.replace(k, v)
Path(dst).write_text(text, encoding="utf-8")
print(f"wrote {dst}")
PY

plutil -lint "$PLIST_DST" >/dev/null

pkill -f 'scripts/x_reply_daemon.py' 2>/dev/null || true
pkill -f 'x_reply_daemon.py' 2>/dev/null || true
sleep 1

launchctl bootout "gui/$(id -u)/com.builtbykern.kern-reply" 2>/dev/null || true
sleep 2
launchctl bootstrap "gui/$(id -u)" "$PLIST_DST"
launchctl enable "gui/$(id -u)/com.builtbykern.kern-reply"
sleep 1
launchctl kickstart "gui/$(id -u)/com.builtbykern.kern-reply" 2>/dev/null || true

sleep 4
PRINT="$(launchctl print "gui/$(id -u)/com.builtbykern.kern-reply" 2>&1 || true)"
echo "$PRINT" | grep -E 'state =|pid =|last exit code|runs =' | head -20 || true

echo ""
echo "Installed: $PLIST_DST"
echo "Runtime:   $APP_ROOT  (synced from $ROOT)"
echo "Logs:      $SUPPORT_DIR/logs/x-cycle.log"
echo "Re-sync after script/state edits: bash scripts/sync_launchd_runtime.sh && launchctl kickstart gui/$(id -u)/com.builtbykern.kern-reply"

if echo "$PRINT" | grep -q 'last exit code = 78'; then
  echo "ERROR: EX_CONFIG" >&2
  exit 1
fi

for _ in 1 2 3 4 5 6 7 8; do
  if pgrep -f 'x_reply_daemon.py' >/dev/null; then
    echo "OK: daemon running (pid $(pgrep -f 'x_reply_daemon.py' | tr '\n' ' '))"
    tail -5 "$SUPPORT_DIR/logs/x-cycle.log" || true
    exit 0
  fi
  sleep 1
done

echo "ERROR: daemon did not start" >&2
tail -30 "$SUPPORT_DIR/logs/x-cycle.err" || true
tail -30 "$SUPPORT_DIR/logs/x-cycle.log" || true
exit 1
