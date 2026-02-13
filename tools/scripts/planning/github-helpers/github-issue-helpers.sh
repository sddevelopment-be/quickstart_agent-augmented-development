#!/usr/bin/env bash
# Shared helper functions for GitHub issue automation.
# Source this script from other tooling to standardize how issues are created.

set -euo pipefail

# Emit message to stderr
_github_issue::log() {
  printf 'github-issue: %s\n' "$*" >&2
}

# Ensure GitHub CLI is available before attempting any operation
_github_issue::require_cli() {
  if ! command -v gh >/dev/null 2>&1; then
    _github_issue::log "GitHub CLI (gh) not found in PATH"
    return 1
  fi
}

# Trim leading/trailing whitespace and remove all quotes
_github_issue::trim() {
  local value="${1-}"
  # shellcheck disable=SC2001
  # Remove leading/trailing whitespace, then remove all single and double quotes
  value="$(printf '%s' "${value}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e 's/["'\'']//g')"
  printf '%s' "${value}"
}

# Read issue body from a file path.
# Arguments:
#   $1 - Path to file containing the body
_github_issue::body_from_file() {
  local file_path="${1-}"
  if [[ -z "${file_path}" ]]; then
    _github_issue::log "body_from_file: path is required"
    return 1
  fi
  if [[ ! -f "${file_path}" ]]; then
    _github_issue::log "body_from_file: no such file: ${file_path}"
    return 1
  fi
  cat "${file_path}"
}

# Return the file contents if present, otherwise fallback to provided text.
# Arguments:
#   $1 - Fallback body text
#   $2 - Optional file path containing the canonical body
_github_issue::body_from_source() {
  local fallback="${1-}"
  local file_path="${2-}"
  if [[ -n "${file_path}" && -f "${file_path}" ]]; then
    cat "${file_path}"
  else
    printf '%s' "${fallback}"
  fi
}

# Create a GitHub issue using the GitHub CLI.
# Arguments:
#   $1 - repository (owner/name)
#   $2 - title
#   $3 - body text
#   $4 - comma-separated labels (optional)
#   $5 - comma-separated assignees (optional)
#   $6 - milestone number or title (optional)
#   $7 - draft flag (true/false, optional)
_github_issue::create() {
  if [[ $# -lt 3 ]]; then
    _github_issue::log "create: repo, title, and body are required"
    return 1
  fi

  local repo="$1"
  local title="$2"
  local body="$3"
  local labels="${4-}"
  local assignees="${5-}"
  local milestone="${6-}"
  local draft="${7:-false}"

  _github_issue::require_cli

  local -a cmd
  cmd=("gh" "issue" "create" "--repo" "${repo}" "--title" "${title}" "--body" "${body}")

  if [[ -n "${labels}" ]]; then
    IFS=',' read -ra _labels <<< "${labels}"

    local -a requested_labels=()
    for raw_label in "${_labels[@]}"; do
      local trimmed="$(_github_issue::trim "${raw_label}")"
      [[ -n "${trimmed}" ]] && requested_labels+=("${trimmed}")
    done

    if ((${#requested_labels[@]})); then
      local -a repo_labels=()
      if mapfile -t repo_labels < <(gh label list --repo "${repo}" --limit 400 --json name --jq '.[].name' 2>/dev/null); then
        declare -A repo_label_map=()
        for repo_label in "${repo_labels[@]}"; do
          local key
          key="$(printf '%s' "${repo_label}" | tr '[:upper:]' '[:lower:]')"
          repo_label_map["${key}"]=1
        done

        local -a missing_labels=()
        for label in "${requested_labels[@]}"; do
          local lookup
          lookup="$(printf '%s' "${label}" | tr '[:upper:]' '[:lower:]')"
          if [[ -n "${repo_label_map[${lookup}]:-}" ]]; then
            cmd+=("--label" "${label}")
          else
            missing_labels+=("${label}")
          fi
        done

        if ((${#missing_labels[@]})); then
          _github_issue::log "warning: labels missing in ${repo} -> ${missing_labels[*]}"
          _github_issue::log "warning: sync repository labels (e.g., run the upcoming gh label sync helper) before re-running."
        fi
      else
        _github_issue::log "warning: unable to verify labels for ${repo} (gh label list failed); continuing without validation."
        for label in "${requested_labels[@]}"; do
          cmd+=("--label" "${label}")
        done
      fi
    fi
  fi

  if [[ -n "${assignees}" ]]; then
    IFS=',' read -ra _assignees <<< "${assignees}"
    for user in "${_assignees[@]}"; do
      user=$(_github_issue::trim ${user})
      # Only add assignee if non-empty after trimming
      if [[ -n "${user}" ]]; then
#        _github_issue::log "TRIMMED ASSIGNEE: '${user}'"
        cmd+=("--assignee" "${user}")
      fi
    done
  fi

  if [[ -n "${milestone}" ]]; then
    milestone="$(_github_issue::trim "${milestone}")"
    if [[ -n "${milestone}" ]]; then
      cmd+=("--milestone" "${milestone}")
    fi
  fi

  if [[ "${draft}" == "true" ]]; then
    cmd+=("--draft")
  fi

  _github_issue::log "Creating issue '${title}' in ${repo}"
#  _github_issue::log "COMMAND: ${cmd[*]}"
  "${cmd[@]}"
}
