#!/usr/bin/env bash
# Full automated reply cycle (Playwright). Use from cron/launchd instead of Cursor browser MCP.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
exec python3 scripts/x_reply_cycle.py "$@"
