#!/usr/bin/env bash
# Loader Script: load_directives.sh
# Purpose: On-demand inclusion of externalized directive markdown blocks to reduce default context size.
# Usage:
#   ./load_directives.sh 001 006
#   ./load_directives.sh --list
#   source <(./load_directives.sh 001 003)  # if emitting export commands later
# Notes:
# - Accepts numeric codes matching files in .github/agents/directives/XXX_name.md
# - Outputs concatenated markdown to STDOUT; wrap or redirect as needed.
# - Intentional small footprint: concatenates markdown only (no side effects).

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIR="${SCRIPT_DIR}/directives"

usage() {
  cat <<'USAGE' >&2
Usage: load_directives.sh [--list] <directive-codes...>

Examples:
  load_directives.sh 001 006
  load_directives.sh --list
USAGE
}

if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

if [[ "$1" == "--list" ]]; then
  printf "Available directives (code : filename)\n"
  find "${DIR}" -maxdepth 1 -type f -name '*_*' -printf "%f\n" | sort | while read -r f; do
    code=${f%%_*}
    printf "  %s : %s\n" "${code}" "${f}"
  done
  exit 0
fi

for code in "$@"; do
  # shellcheck disable=SC2125
  file="${DIR}/${code}_"*
  # shellcheck disable=SC2206
  match=( ${file} )
  if [[ ${#match[@]} -eq 0 ]]; then
    echo "[WARN] No directive found for code ${code}" >&2
    continue
  fi
  # Expect single match
  printf "\n<!-- Directive %s Begin -->\n" "${code}"
  cat "${match[0]}"
  printf "\n<!-- Directive %s End -->\n" "${code}"
done

