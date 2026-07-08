#!/usr/bin/env bash
# Print KERN-Reply automation prefill URL (requires Cursor MCP or manual import).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WF="$ROOT/automations/kern-reply.workflow.json"
echo "Workflow: $WF"
echo "Setup doc: $ROOT/automations/KERN-REPLY-SETUP.md"
echo "Open Cursor → Automations → New → paste prompt from automations/kern-reply.prompt.md"
echo "Cron: 0 8-22 * * * (hourly 8am-10pm, set your timezone in UI)"
