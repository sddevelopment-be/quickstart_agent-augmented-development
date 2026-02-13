#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd -- "${SCRIPT_DIR}/../.." && pwd)
cd "${REPO_ROOT}"

missing=0
warnings=0
required_dirs=(
  "work/collaboration"
  "work/collaboration/inbox"
  "work/collaboration/assigned"
  "work/collaboration/done"
  "work/collaboration/archive"
  "work/reports"
)

for dir in "${required_dirs[@]}"; do
  if [[ ! -d "${dir}" ]]; then
    echo "❗️ Missing required directory: ${dir}"
    missing=1
  fi
done

for profile in .github/agents/*.agent.md; do
  [[ -e "${profile}" ]] || continue
  agent_name=$(basename "${profile}" .agent.md)
  if [[ ! -d "work/collaboration/assigned/${agent_name}" ]]; then
    echo "⚠️ Agent '${agent_name}' missing directory under work/collaboration/assigned/"
    warnings=$((warnings + 1))
  fi
done

if [[ "${missing}" -ne 0 ]]; then
  echo "❌ Work directory structure invalid"
  exit 1
fi

if [[ "${warnings}" -gt 0 ]]; then
  echo "⚠️ Work directory structure valid with ${warnings} warnings"
else
  echo "✅ Work directory structure valid"
fi
