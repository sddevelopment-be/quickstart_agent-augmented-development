#!/bin/bash
# Agent-Friendly Error Summary Generator - Shell Wrapper
#
# Usage:
#   bash generate-error-summary.sh \
#     --workflow "Work Validation" \
#     --job "validate" \
#     --validator "task-schema" \
#     < validation_output.txt
#
# Or pipe directly:
#   python validate-task-schema.py file.yaml 2>&1 | \
#     bash generate-error-summary.sh --workflow "..." --job "..." --validator "..."

set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd -- "${SCRIPT_DIR}/../.." && pwd)

# Default output paths
OUTPUT_DIR="${GITHUB_WORKSPACE:-${REPO_ROOT}}/output/error-reports"
mkdir -p "${OUTPUT_DIR}"

TIMESTAMP=$(date -u +"%Y%m%d_%H%M%S")
JSON_OUTPUT="${OUTPUT_DIR}/errors_${TIMESTAMP}.json"
MARKDOWN_OUTPUT="${OUTPUT_DIR}/errors_${TIMESTAMP}.md"

# Parse arguments
WORKFLOW=""
JOB=""
VALIDATOR="unknown"
INPUT_FILE=""
EMIT_ANNOTATIONS="false"
FAIL_ON_ERRORS="false"

while [[ $# -gt 0 ]]; do
  case $1 in
    --workflow)
      WORKFLOW="$2"
      shift 2
      ;;
    --job)
      JOB="$2"
      shift 2
      ;;
    --validator)
      VALIDATOR="$2"
      shift 2
      ;;
    --input)
      INPUT_FILE="$2"
      shift 2
      ;;
    --emit-annotations)
      EMIT_ANNOTATIONS="true"
      shift
      ;;
    --fail-on-errors)
      FAIL_ON_ERRORS="true"
      shift
      ;;
    --output-json)
      JSON_OUTPUT="$2"
      shift 2
      ;;
    --output-markdown)
      MARKDOWN_OUTPUT="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "${WORKFLOW}" ]] || [[ -z "${JOB}" ]]; then
  echo "Error: --workflow and --job are required" >&2
  echo "Usage: $0 --workflow NAME --job NAME [--validator NAME] [options]" >&2
  exit 1
fi

# Build Python command
PYTHON_CMD=(
  python3
  "${SCRIPT_DIR}/generate-error-summary.py"
  --workflow "${WORKFLOW}"
  --job "${JOB}"
  --validator "${VALIDATOR}"
  --output-json "${JSON_OUTPUT}"
  --output-markdown "${MARKDOWN_OUTPUT}"
)

if [[ -n "${INPUT_FILE}" ]]; then
  PYTHON_CMD+=(--input "${INPUT_FILE}")
fi

if [[ "${EMIT_ANNOTATIONS}" == "true" ]]; then
  PYTHON_CMD+=(--emit-annotations)
fi

if [[ "${FAIL_ON_ERRORS}" == "true" ]]; then
  PYTHON_CMD+=(--fail-on-errors)
fi

# Execute
"${PYTHON_CMD[@]}"

exit_code=$?

# Always report artifact locations for agent retrieval
echo "" >&2
echo "📦 Artifacts:" >&2
echo "  JSON: ${JSON_OUTPUT}" >&2
echo "  Markdown: ${MARKDOWN_OUTPUT}" >&2

# Add to GitHub Actions step summary if available
if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
  cat "${MARKDOWN_OUTPUT}" >> "${GITHUB_STEP_SUMMARY}"
fi

exit ${exit_code}
