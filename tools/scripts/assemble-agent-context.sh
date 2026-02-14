#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: assemble-agent-context.sh [--agent <name|path>] [--mode minimal|full] [--directives <code1 code2 ...>] [--no-aliases]

Emits a compact, ready-to-paste agent context to STDOUT.
- --mode minimal (default) prints the runtime sheet + specialist profile (if provided) and optional directives.
- --mode full additionally inlines general + operational guidelines for high-stakes tasks.
- --directives accepts space-separated directive codes (e.g., 001 006) that map to .github/agents/directives/XXX_*.md.
- --agent may be a basename like "backend-dev" or a direct path to an agent profile.
- --no-aliases skips including .github/agents/aliases.md.
USAGE
}

MODE="minimal"
DIRECTIVES=()
AGENT=""
INCLUDE_ALIASES=1

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent)
      AGENT=${2-}
      [[ -z "${AGENT}" ]] && { echo "[ERROR] --agent requires a value" >&2; exit 1; }
      shift 2
      ;;
    --mode)
      MODE=${2-}
      [[ -z "${MODE}" ]] && { echo "[ERROR] --mode requires a value" >&2; exit 1; }
      shift 2
      ;;
    --directives)
      shift
      while [[ $# -gt 0 && $1 != --* ]]; do
        DIRECTIVES+=("$1")
        shift
      done
      ;;
    --no-aliases)
      INCLUDE_ALIASES=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[WARN] Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENTS_DIR="${REPO_ROOT}/.github/agents"
RUNTIME_SHEET="${AGENTS_DIR}/guidelines/runtime_sheet.md"
GENERAL="${AGENTS_DIR}/guidelines/general_guidelines.md"
OPERATIONAL="${AGENTS_DIR}/guidelines/operational_guidelines.md"
ALIASES="${AGENTS_DIR}/aliases.md"
LOADER="${AGENTS_DIR}/load_directives.sh"

[[ -f "${RUNTIME_SHEET}" ]] || { echo "[ERROR] Missing runtime sheet at ${RUNTIME_SHEET}" >&2; exit 1; }
[[ -x "${LOADER}" ]] || { echo "[WARN] load_directives.sh not executable; attempting to continue" >&2; }

resolve_agent_path() {
  local input="$1"
  if [[ -z "${input}" ]]; then
    return 1
  fi
  if [[ -f "${input}" ]]; then
    echo "${input}"
    return 0
  fi
  local basename="${input%.agent.md}"
  local candidate="${AGENTS_DIR}/${basename}.agent.md"
  if [[ -f "${candidate}" ]]; then
    echo "${candidate}"
    return 0
  fi
  return 1
}

AGENT_PATH=""
if [[ -n "${AGENT}" ]]; then
  if AGENT_PATH=$(resolve_agent_path "${AGENT}"); then
    :
  else
    echo "[ERROR] Agent profile not found for '${AGENT}'" >&2
    exit 1
  fi
fi

print_section() {
  local title="$1"; shift
  local file="$1"
  [[ -f "${file}" ]] || { echo "[WARN] Skipping missing file: ${file}" >&2; return; }
  printf "\n<!-- %s -->\n" "${title}"
  cat "${file}"
}

echo "<!-- Assembled agent context: ${MODE} mode -->"
print_section "Runtime Sheet" "${RUNTIME_SHEET}"

if [[ -n "${AGENT_PATH}" ]]; then
  print_section "Agent Profile" "${AGENT_PATH}"
fi

if [[ "${INCLUDE_ALIASES}" -eq 1 ]]; then
  print_section "Aliases" "${ALIASES}"
fi

if [[ ${#DIRECTIVES[@]} -gt 0 ]]; then
  printf "\n<!-- Directives -->\n"
  "${LOADER}" "${DIRECTIVES[@]}"
fi

if [[ "${MODE}" == "full" ]]; then
  print_section "General Guidelines" "${GENERAL}"
  print_section "Operational Guidelines" "${OPERATIONAL}"
fi
