#!/usr/bin/env bash
# Quick wrapper for validating task YAML files
# Usage: ./ops/scripts/validate-task.sh <task-file.yaml> [<task-file2.yaml> ...]

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VALIDATOR="${REPO_ROOT}/validation/validate-task-schema.py"

if [ ! -f "$VALIDATOR" ]; then
    echo "❌ Validator not found: $VALIDATOR" >&2
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Usage: $0 <task-file.yaml> [<task-file2.yaml> ...]" >&2
    echo "" >&2
    echo "Examples:" >&2
    echo "  $0 work/collaboration/done/curator/2026-02-07T1400-task.yaml" >&2
    echo "  $0 work/collaboration/done/curator/*.yaml" >&2
    exit 1
fi

python "$VALIDATOR" "$@"
