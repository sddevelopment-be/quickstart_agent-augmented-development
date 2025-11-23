#!/usr/bin/env bash
# Initialize work directory structure for multi-agent orchestration

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WORK_DIR="$ROOT_DIR/work"
cd "$ROOT_DIR"

echo "Initializing work directory structure under ${WORK_DIR}..."

lifecycle_dirs=(inbox done archive logs collaboration scripts schemas assigned notes)
for dir in "${lifecycle_dirs[@]}"; do
  mkdir -p "$WORK_DIR/$dir"
done

agents=(
  architect
  backend-dev
  bootstrap-bill
  build-automation
  coordinator
  curator
  diagrammer
  frontend
  lexical
  manager
  planning
  researcher
  structural
  synthesizer
  translator
  writer-editor
)

for agent in "${agents[@]}"; do
  mkdir -p "$WORK_DIR/assigned/$agent"
done

# Add .gitkeep files so directories remain tracked when empty
find "$WORK_DIR" -type d -not -path "*/.git" -exec sh -c 'test -f "$1/.gitkeep" || touch "$1/.gitkeep"' _ {} \;

ensure_file() {
  local path="$1"
  local content="$2"
  if [[ ! -f "$path" ]]; then
    printf "%s" "$content" > "$path"
    echo "Created $path"
  else
    echo "Preserved existing $path"
  fi
}

AGENT_STATUS_CONTENT=$(cat <<'CONTENT'
# Agent Status Dashboard

_Last updated: Never_

No agent activity recorded yet.

## How to Read This Dashboard

- **Status**: Current agent state (Idle, In Progress, Error)
- **Current task**: Task ID if agent is working
- **Last seen**: Timestamp of most recent activity
- **Tasks completed today**: Count of completed tasks since midnight
CONTENT
)

HANDOFFS_CONTENT=$(cat <<'CONTENT'
# Agent Handoff Log

This log records agent-to-agent transitions for traceability.

## Format

Each handoff entry includes:
- Date and time
- Source agent → Destination agent
- Artifacts passed
- Reason for handoff
- Task ID
- Status

## Handoff History

_No handoffs recorded yet._
CONTENT
)

WORKFLOW_LOG_CONTENT=$(cat <<'CONTENT'
# Workflow Orchestration Log

This log records system-wide orchestration events.

## Log Entries

_No workflow events recorded yet._
CONTENT
)

README_CONTENT=$(cat <<'CONTENT'
# Work Directory - Multi-Agent Orchestration

This directory contains the file-based orchestration system for coordinating multiple specialized agents.

For full documentation, see docs/architecture/design/async_orchestration_technical_design.md.
CONTENT
)

ensure_file "$WORK_DIR/collaboration/AGENT_STATUS.md" "$AGENT_STATUS_CONTENT"
ensure_file "$WORK_DIR/collaboration/HANDOFFS.md" "$HANDOFFS_CONTENT"
ensure_file "$WORK_DIR/collaboration/WORKFLOW_LOG.md" "$WORKFLOW_LOG_CONTENT"
ensure_file "$WORK_DIR/README.md" "$README_CONTENT"

echo "✅ Work directory structure initialized successfully"

echo ""
echo "Next steps:"
echo "1. Review work/README.md"
echo "2. Create task YAML schema in docs/templates/agent-tasks/ if missing"
echo "3. Implement Agent Orchestrator in work/scripts/agent_orchestrator.py"
echo "4. Review docs/architecture/design/async_orchestration_technical_design.md"
