#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd -- "$SCRIPT_DIR/../.." && pwd)
cd "$REPO_ROOT"

missing=0
required_dirs=(
  "work/inbox"
  "work/assigned"
  "work/done"
  "work/archive"
  "work/collaboration"
)

for dir in "${required_dirs[@]}"; do
  if [[ ! -d "$dir" ]]; then
    echo "❗️ Missing required directory: $dir"
    missing=1
  fi
done

for profile in .github/agents/*.agent.md; do
  [[ -e "$profile" ]] || continue
  agent_name=$(basename "$profile" .agent.md)
  if [[ ! -d "work/assigned/$agent_name" ]]; then
    echo "⚠️ Agent '$agent_name' missing directory under work/assigned/"
  fi
done

if [[ "$missing" -ne 0 ]]; then
  echo "❌ Work directory structure invalid"
  exit 1
fi

echo "✅ Work directory structure valid"
