#!/usr/bin/env bash
# Generic issue creation engine - reads YAML definitions and creates GitHub issues
# Uses 3-tier architecture: API (this) -> Logic (definitions) -> Helpers (github-helpers)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC2034
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
DEFINITIONS_DIR="${SCRIPT_DIR}/agent-scripts/issue-definitions"
GITHUB_HELPER="${SCRIPT_DIR}/github-helpers/create-github-issue.sh"

REPO="${REPO:-sddevelopment-be/quickstart_agent-augmented-development}"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ${NC} $*"
}

log_success() {
    echo -e "${GREEN}✓${NC} $*"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $*"
}

log_error() {
    echo -e "${RED}✗${NC} $*"
}

usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Create GitHub issues from YAML definitions.

OPTIONS:
    --taskset <name>    Only create issues for specific taskset(s) (comma-separated)
    --dry-run           Show what would be created without actually creating
    --repo <owner/name> Override repository (default: from REPO env or hardcoded)
    --list-tasksets     List available tasksets and exit
    -h, --help          Show this help message

EXAMPLES:
    # Create all issues
    $0

    # Create only housekeeping issues
    $0 --taskset housekeeping

    # Create multiple tasksets
    $0 --taskset housekeeping,documentation

    # Dry run to preview
    $0 --taskset housekeeping --dry-run

    # List available tasksets
    $0 --list-tasksets

DEFINITIONS:
    Issue definitions are YAML files in: ${DEFINITIONS_DIR}

    Each definition file should contain:
    - type: "epic" or "issue"
    - taskset: category/grouping
    - title: issue title
    - labels: comma-separated labels
    - body: issue body (can be multiline)
    - epic_ref: (for issues) reference to parent epic definition file

EOF
}

list_tasksets() {
    log_info "Scanning for tasksets in: ${DEFINITIONS_DIR}"
    echo ""

    grep -h "^taskset:" "${DEFINITIONS_DIR}"/*.yml 2>/dev/null | \
        sed 's/taskset: *//' | sed 's/^ *//' | sort -u | while read -r ts; do
        echo "  - ${ts}"
    done
}

parse_yaml_field() {
    local file="$1"
    local key="$2"

    if [[ "${key}" = "body" ]]; then
        # Extract body content (multiline after "body: |")
        awk '/^body: \|/ {flag=1; next} /^[a-z_]+:/ {flag=0} flag' "${file}"
    else
        # Extract simple field value and trim newlines/whitespace
        grep "^${key}:" "${file}" | head -1 | sed "s/^${key}: *//" | sed 's/^"\(.*\)"$/\1/' | sed "s/^ *//" | tr -d '\n\r'
    fi
}

create_issue_from_definition() {
    local file="$1"
    local filter_tasksets="$2"
    local dry_run="$3"
    local epic_numbers_file="$4"

    # Determine if this is a multi-document YAML (array) or single document
    local is_array=0
    if grep -q "^- type:" "${file}"; then
        is_array=1
    fi

    if [[ ${is_array} -eq 1 ]]; then
        # Multi-document: process each item in the array
        # Split file into individual items and process each
        local tmp_dir="/tmp/yaml_split_$$"
        mkdir -p "${tmp_dir}"

        # Split the array into separate files
        # Each item starts with "- type:" and continues until the next "- type:" or EOF
        awk -v outdir="${tmp_dir}" '
            /^- type:/ {
                if (outfile) close(outfile)
                filenum++
                outfile = outdir "/item_" filenum ".yml"
                # Remove the leading "- " to make it a valid YAML document
                sub(/^- /, "")
                print > outfile
                next
            }
            outfile && /^  / {
                # Indented lines belong to the current item, remove 2-space indent
                sub(/^  /, "")
                print > outfile
            }
            END { if (outfile) close(outfile) }
        ' "${file}"

        # Process each split file
        for item_file in "${tmp_dir}"/item_*.yml; do
            [[ -f "${item_file}" ]] || continue
            # Add YAML header to each item
            echo "---" > "${tmp_dir}/temp.yml"
            cat "${item_file}" >> "${tmp_dir}/temp.yml"
            process_yaml_item "${tmp_dir}/temp.yml" "${filter_tasksets}" "${dry_run}" "${epic_numbers_file}"
        done

        # Cleanup
        rm -rf "${tmp_dir}"
    else
        # Single document
        process_yaml_item "${file}" "${filter_tasksets}" "${dry_run}" "${epic_numbers_file}"
    fi
}

process_yaml_item() {
    local file="$1"
    local filter_tasksets="$2"
    local dry_run="$3"
    local epic_numbers_file="$4"

    local type taskset title labels body assignee priority epic_ref

    # Parse fields using grep/awk
    type=$(parse_yaml_field "${file}" "type")
    taskset=$(parse_yaml_field "${file}" "taskset")
    title=$(parse_yaml_field "${file}" "title")
    labels=$(parse_yaml_field "${file}" "labels")
    body=$(parse_yaml_field "${file}" "body")
    assignee=$(parse_yaml_field "${file}" "assignee")
    priority=$(parse_yaml_field "${file}" "priority")
    epic_ref=$(parse_yaml_field "${file}" "epic_ref")

    # Skip if no type or title (empty item)
    if [[ -z "${type}" ]] || [[ -z "${title}" ]]; then
        return
    fi

    # Filter by taskset if specified
    if [[ -n "${filter_tasksets}" ]]; then
        local matched=0
        IFS=',' read -ra SETS <<< "${filter_tasksets}"
        for set in "${SETS[@]}"; do
            set=$(echo "${set}" | xargs)  # Trim whitespace
            if [[ "${taskset}" = "${set}" ]]; then
                matched=1
                break
            fi
        done
        if [[ ${matched} -eq 0 ]]; then
            return
        fi
    fi

    # Replace epic_ref if this is a child issue
    if [[ -n "${epic_ref}" ]] && [[ -f "${epic_numbers_file}" ]]; then
        local epic_number
        epic_number=$(grep "^${epic_ref}=" "${epic_numbers_file}" 2>/dev/null | cut -d= -f2)
        if [[ -n "${epic_number}" ]]; then
            body="${body}"$'\n\n'"Parent Epic: #${epic_number}"
        fi
    fi

    if [[ "${dry_run}" = "true" ]]; then
        echo ""
        log_info "[DRY RUN] Would create ${type}: ${title}"
        echo "  Taskset: ${taskset}"
        echo "  Labels: ${labels}"
        [[ -n "${assignee}" ]] && echo "  Assignee: ${assignee}"
        [[ -n "${priority}" ]] && echo "  Priority: ${priority}"
        return
    fi

    echo ""
    log_info "Creating ${type}: ${title}"

    local -a cmd_args=()
    cmd_args+=(--repo "${REPO}")
    cmd_args+=(--title "${title}")

    if [[ -n "${labels}" ]]; then
        IFS=',' read -ra LBLS <<< "${labels}"
        for lbl in "${LBLS[@]}"; do
            cmd_args+=(--label "$(echo "${lbl}" | xargs)")
        done
    fi

    [[ -n "${assignee}" ]] && cmd_args+=(--assignee "${assignee}")

    local issue_url
    issue_url=$(echo "${body}" | bash "${GITHUB_HELPER}" "${cmd_args[@]}" 2>&1 | tee /dev/tty | grep -oP 'https://github.com/[^ ]+' | head -1)

    # Extract issue number and save epic reference
    if [[ "${type}" = "epic" ]] && [[ -n "${issue_url}" ]]; then
        local issue_number
        issue_number=$(echo "${issue_url}" | grep -oP '/issues/\K[0-9]+')
        if [[ -n "${issue_number}" ]]; then
            local basename
            basename=$(basename "${file}" .yml)
            echo "${basename}=${issue_number}" >> "${epic_numbers_file}"
            log_success "Epic created: #${issue_number}"
        fi
    fi
}

main() {
    local filter_tasksets=""
    local dry_run=false
    local list_only=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --taskset)
                filter_tasksets="$2"
                shift 2
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
            --repo)
                REPO="$2"
                shift 2
                ;;
            --list-tasksets)
                list_only=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done

    if [[ "${list_only}" = true ]]; then
        list_tasksets
        exit 0
    fi

    if [[ ! -d "${DEFINITIONS_DIR}" ]]; then
        log_error "Definitions directory not found: ${DEFINITIONS_DIR}"
        exit 1
    fi

    if [[ ! -f "${GITHUB_HELPER}" ]]; then
        log_error "GitHub helper not found: ${GITHUB_HELPER}"
        exit 1
    fi

    # Create temp file for epic number tracking
    local epic_numbers_file
    epic_numbers_file=$(mktemp)
    trap 'rm -f ${epic_numbers_file}' EXIT

    echo "════════════════════════════════════════════════════════════"
    log_info "GitHub Issue Creation Engine"
    echo "════════════════════════════════════════════════════════════"
    [[ -n "${filter_tasksets}" ]] && log_info "Filtering tasksets: ${filter_tasksets}"
    [[ "${dry_run}" = true ]] && log_warning "DRY RUN MODE - No issues will be created"
    echo ""

    # Phase 1: Create epics first
    log_info "Phase 1: Creating epics..."
    for file in "${DEFINITIONS_DIR}"/*-epic.yml; do
   [[ -f "${file}" ]] || continue
        log_info "Processing epic file: $(basename "${file}")"
        create_issue_from_definition "${file}" "${filter_tasksets}" "${dry_run}" "${epic_numbers_file}" || {
            log_error "Failed to process: ${file}"
            continue
        }
    done

    # Phase 2: Create regular issues
    log_info "Phase 2: Creating issues..."
    for file in "${DEFINITIONS_DIR}"/*.yml; do
        [[ -f "${file}" ]] || continue
        [[ "${file}" == *-epic.yml ]] && continue  # Skip epics
        log_info "Processing issue file: $(basename "${file}")"
        create_issue_from_definition "${file}" "${filter_tasksets}" "${dry_run}" "${epic_numbers_file}" || {
            log_error "Failed to process: ${file}"
            continue
        }
    done

    echo ""
    echo "════════════════════════════════════════════════════════════"
    if [[ "${dry_run}" = true ]]; then
        log_success "Dry run complete"
    else
        log_success "Issue creation complete"
        log_info "View issues at: https://github.com/${REPO}/issues"
    fi
    echo "════════════════════════════════════════════════════════════"
}

main "$@"

