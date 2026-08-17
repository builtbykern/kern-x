#!/usr/bin/env bash
# Sync kern-x runtime into ~/Library/Application Support so LaunchAgent
# does not touch ~/Desktop (macOS TCC → Operation not permitted / EX_CONFIG).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SUPPORT_DIR="${HOME}/Library/Application Support/builtbykern-kern-x"
APP_ROOT="${SUPPORT_DIR}/runtime"

mkdir -p "$APP_ROOT" "$SUPPORT_DIR/logs"

rsync -a --delete \
  --exclude '.chrome-profile/' \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude '.git/' \
  "$ROOT/scripts/" "$APP_ROOT/scripts/"

rsync -a --delete "$ROOT/voice/" "$APP_ROOT/voice/"
rsync -a --delete "$ROOT/tools/" "$APP_ROOT/tools/"
rsync -a --delete "$ROOT/runtime/" "$APP_ROOT/runtime/"
rsync -a --delete "$ROOT/config/" "$APP_ROOT/config/"

# Node compose deps (@cursor/sdk) — required for CURSOR_API_KEY path under launchd
if [[ -f "$ROOT/package.json" ]]; then
  cp "$ROOT/package.json" "$APP_ROOT/package.json"
  if [[ -f "$ROOT/package-lock.json" ]]; then
    cp "$ROOT/package-lock.json" "$APP_ROOT/package-lock.json"
  fi
  if [[ -d "$ROOT/node_modules/@cursor" ]]; then
    mkdir -p "$APP_ROOT/node_modules"
    rsync -a --delete "$ROOT/node_modules/@cursor/" "$APP_ROOT/node_modules/@cursor/"
    # Copy direct dependency tree used by the SDK (best-effort)
    if [[ -d "$ROOT/node_modules" ]]; then
      # Prefer full node_modules sync when reasonably small; else npm install
      SIZE_KB="$(du -sk "$ROOT/node_modules" 2>/dev/null | awk '{print $1}')"
      if [[ -n "${SIZE_KB:-}" && "$SIZE_KB" -lt 512000 ]]; then
        rsync -a --delete "$ROOT/node_modules/" "$APP_ROOT/node_modules/"
      else
        (cd "$APP_ROOT" && npm install --omit=dev --no-fund --no-audit) || true
      fi
    fi
  else
    (cd "$APP_ROOT" && npm install --omit=dev --no-fund --no-audit) || true
  fi
fi

# State + secrets: update from workspace, keep Support-only files
mkdir -p "$APP_ROOT/state" "$APP_ROOT/logs"
rsync -a "$ROOT/state/" "$APP_ROOT/state/"
# Do not wipe Support logs with desktop logs; only ensure dirs exist
mkdir -p "$SUPPORT_DIR/logs" "$APP_ROOT/logs"

if [[ -f "$ROOT/.env" ]]; then
  # Strip X_CDP_URL so launchd storage mode is not overridden by .env
  grep -v '^X_CDP_URL=' "$ROOT/.env" > "$APP_ROOT/.env" || cp "$ROOT/.env" "$APP_ROOT/.env"
  if ! grep -q '^X_FORCE_STORAGE=' "$APP_ROOT/.env" 2>/dev/null; then
    echo 'X_FORCE_STORAGE=1' >> "$APP_ROOT/.env"
  fi
  if ! grep -q '^X_HEADLESS=' "$APP_ROOT/.env" 2>/dev/null; then
    echo 'X_HEADLESS=1' >> "$APP_ROOT/.env"
  fi
fi

# Point convenience symlinks from workspace logs → launchd logs
ln -sfn "$SUPPORT_DIR/logs/x-cycle.log" "$ROOT/logs/x-cycle.launchd.log"
ln -sfn "$SUPPORT_DIR/logs/x-cycle.err" "$ROOT/logs/x-cycle.launchd.err"

# Record where this mirror came from
printf '%s\n' "$ROOT" > "$SUPPORT_DIR/source_repo_path.txt"
echo "Synced runtime → $APP_ROOT"
