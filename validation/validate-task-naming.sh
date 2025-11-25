#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd -- "$SCRIPT_DIR/../.." && pwd)
cd "$REPO_ROOT"

shopt -s nullglob
invalid=0
# Pattern updated 2025-11-24: Allow flexible slug structure for orchestrator-generated follow-up tasks
# Format: YYYY-MM-DDTHHMM-<slug>.yaml
# Slug rules:
#   - Must start with lowercase letter
#   - Can contain: lowercase letters, digits, hyphens
#   - Can embed ISO timestamps (T followed by exactly 4 digits, e.g., T1738)
#   - Must end with alphanumeric character or embedded timestamp (no trailing hyphen)
#   - Examples: "architect-poc3", "diagrammer-followup-2025-11-23T1738-architect-poc3-multi-agent-chain"
pattern='^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{4}-[a-z](([a-z0-9-]|T[0-9]{4})*([a-z0-9]|T[0-9]{4}))?\.yaml$'

target_sets=(work/inbox/*.yaml work/assigned/*/*.yaml work/done/*.yaml)

for task in "${target_sets[@]}"; do
  [[ -e "$task" ]] || continue
  filename=$(basename "$task")
  if [[ ! $filename =~ $pattern ]]; then
    echo "⚠️ Invalid task filename: $task"
    invalid=1
  fi
done

if [[ "$invalid" -ne 0 ]]; then
  echo "❌ Task naming validation failed"
  exit 1
fi

echo "✅ Task naming validation complete"
