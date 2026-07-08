#!/usr/bin/env bash
# Install macOS LaunchAgent for KERN-Reply (60–90m jitter via companion daemon).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLIST_SRC="$ROOT/schedule/com.builtbykern.kern-reply.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.builtbykern.kern-reply.plist"
LOG_DIR="$ROOT/logs"

mkdir -p "$LOG_DIR"
sed -e "s|__KERN_X_ROOT__|$ROOT|g" -e "s|__HOME__|$HOME|g" "$PLIST_SRC" > "$PLIST_DST"

launchctl bootout "gui/$(id -u)/com.builtbykern.kern-reply" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_DST"
launchctl enable "gui/$(id -u)/com.builtbykern.kern-reply"

echo "Installed: $PLIST_DST"
echo "Logs: $LOG_DIR/x-cycle.log $LOG_DIR/x-cycle.err"
echo "Unload: launchctl bootout gui/$(id -u)/com.builtbykern.kern-reply"
