#!/usr/bin/env bash
# Thin wrapper around _github_issue helpers to create GitHub issues from scripts or CI.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/github-issue-helpers.sh"

usage() {
  cat <<'USAGE'
Usage: ops/scripts/create-github-issue.sh --repo <owner/name> --title <text> \
       [--body "text" | --body-file path] [--label label]... [--assignee user]... \
       [--milestone value] [--draft]

Options:
  --repo           GitHub repository in owner/name format (required)
  --title          Issue title (required)
  --body           Issue body as a single argument (mutually exclusive with --body-file)
  --body-file      Path to file containing the issue body
  --label          Issue label (can be passed multiple times)
  --assignee       GitHub username to assign (can be passed multiple times)
  --milestone      Milestone name or number
  --draft          Create the issue as a draft
  -h, --help       Show this message

If neither --body nor --body-file are supplied, the script reads the body from STDIN.
USAGE
}

REPO=""
TITLE=""
BODY=""
BODY_FILE=""
LABELS=""
ASSIGNEES=""
MILESTONE=""
DRAFT="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      REPO="$2"
      shift 2
      ;;
    --title)
      TITLE="$2"
      shift 2
      ;;
    --body)
      BODY="$2"
      shift 2
      ;;
    --body-file)
      BODY_FILE="$2"
      shift 2
      ;;
    --label)
      LABELS="${LABELS:+$LABELS,}$2"
      shift 2
      ;;
    --assignee)
      ASSIGNEES="${ASSIGNEES:+$ASSIGNEES,}$2"
      shift 2
      ;;
    --milestone)
      MILESTONE="$2"
      shift 2
      ;;
    --draft)
      DRAFT="true"
      shift 1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$REPO" || -z "$TITLE" ]]; then
  usage >&2
  exit 1
fi

if [[ -n "$BODY_FILE" && -n "$BODY" ]]; then
  _github_issue::log "--body and --body-file are mutually exclusive"
  exit 1
fi

if [[ -n "$BODY_FILE" ]]; then
  BODY="$(_github_issue::body_from_file "$BODY_FILE")"
elif [[ -z "$BODY" ]]; then
  if [[ -t 0 ]]; then
    _github_issue::log "Either --body, --body-file, or STDIN input is required"
    exit 1
  fi
  BODY="$(cat)"
fi

_github_issue::create "$REPO" "$TITLE" "$BODY" "$LABELS" "$ASSIGNEES" "$MILESTONE" "$DRAFT"
