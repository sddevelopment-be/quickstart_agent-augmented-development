#!/usr/bin/env bash
# Loader Script: load_directives.sh
# Purpose: On-demand inclusion of externalized directive markdown blocks to reduce default context size.
# Usage:
#   ./load_directives.sh 001 006
#   source <(./load_directives.sh 001 003)  # if emitting export commands later
# Notes:
# - Accepts numeric codes matching files in .github/agents/directives/XXX_name.md
# - Outputs concatenated markdown to STDOUT; wrap or redirect as needed.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIR="$SCRIPT_DIR/directives"

if [[ $# -eq 0 ]]; then
  echo "Provide one or more directive codes (e.g. 001 004 006)" >&2
  exit 1
fi

for code in "$@"; do
  file="$DIR/${code}_"*
  match=( $file )
  if [[ ${#match[@]} -eq 0 ]]; then
    echo "[WARN] No directive found for code $code" >&2
    continue
  fi
  # Expect single match
  echo "\n<!-- Directive $code Begin -->"
  cat "${match[0]}"
  echo "\n<!-- Directive $code End -->"
done

