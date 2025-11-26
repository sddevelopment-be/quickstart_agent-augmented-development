#!/usr/bin/env bash
# Scaffolding script to orchestrate GitHub issue creation from agent-generated scripts
# Created by: DevOps Danny
# Date: 2025-11-26

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
AGENT_SCRIPTS_DIR="$SCRIPT_DIR/agent-scripts"

# Source shared helpers
# shellcheck disable=SC1091
source "$REPO_ROOT/ops/scripts/github-issue-helpers.sh"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
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

# Print header
print_header() {
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "  GitHub Issues Creation Scaffold"
    echo "════════════════════════════════════════════════════════════"
    echo ""
}

# Print usage
usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Orchestrates GitHub issue creation from agent-generated scripts.

OPTIONS:
    --all               Create all issues from all agent scripts
    --housekeeping      Create housekeeping and refactoring issues only
    --tasks             Create issues for all open/assigned tasks
    --script <name>     Run a specific agent script by name
    --list              List available agent scripts
    --dry-run           Show what would be executed without running
    -h, --help          Show this help message

ENVIRONMENT:
    GH_TOKEN            GitHub token with repo access (required)

EXAMPLES:
    # Create all issues
    export GH_TOKEN="your_token"
    $(basename "$0") --all

    # Create only housekeeping issues
    $(basename "$0") --housekeeping

    # Dry run to see what would execute
    $(basename "$0") --all --dry-run

    # List available scripts
    $(basename "$0") --list

NOTES:
    - This script requires GH_TOKEN environment variable
    - Scripts are executed from: $AGENT_SCRIPTS_DIR
    - Shared helpers are loaded from: $REPO_ROOT/ops/scripts/
    - See agent-scripts/README-housekeeping-issues.md for more details

EOF
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if [ -z "${GH_TOKEN:-}" ]; then
        log_error "GH_TOKEN environment variable is not set"
        log_info "Set it with: export GH_TOKEN=\"your_token\""
        log_info "Or authenticate with: gh auth login"
        return 1
    fi
    
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) is not installed"
        log_info "Install from: https://cli.github.com/"
        return 1
    fi
    
    log_success "Prerequisites check passed"
    return 0
}

# List available agent scripts
list_agent_scripts() {
    log_info "Available agent scripts in $AGENT_SCRIPTS_DIR:"
    echo ""
    
    local count=0
    for script in "$AGENT_SCRIPTS_DIR"/*.sh; do
        if [ -f "$script" ]; then
            count=$((count + 1))
            local basename=$(basename "$script")
            local description=$(grep -m1 "^# " "$script" | sed 's/^# //' || echo "No description")
            printf "  %d. %-40s %s\n" "$count" "$basename" "$description"
        fi
    done
    
    if [ "$count" -eq 0 ]; then
        log_warning "No agent scripts found"
    fi
    echo ""
}

# Execute an agent script
execute_script() {
    local script_path="$1"
    local script_name=$(basename "$script_path")
    
    log_info "Executing: $script_name"
    
    if [ ! -f "$script_path" ]; then
        log_error "Script not found: $script_path"
        return 1
    fi
    
    if [ ! -x "$script_path" ]; then
        log_warning "Script is not executable, making it executable..."
        chmod +x "$script_path"
    fi
    
    # Execute the script
    if bash "$script_path"; then
        log_success "Completed: $script_name"
        return 0
    else
        log_error "Failed: $script_name"
        return 1
    fi
}

# Main execution
main() {
    print_header
    
    # Parse arguments
    local mode=""
    local dry_run=false
    local specific_script=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --all)
                mode="all"
                shift
                ;;
            --housekeeping)
                mode="housekeeping"
                shift
                ;;
            --tasks)
                mode="tasks"
                shift
                ;;
            --script)
                mode="specific"
                specific_script="$2"
                shift 2
                ;;
            --list)
                list_agent_scripts
                exit 0
                ;;
            --dry-run)
                dry_run=true
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
    
    # Default to --all if no mode specified
    if [ -z "$mode" ]; then
        mode="all"
        log_info "No mode specified, defaulting to --all"
    fi
    
    # Check prerequisites unless dry-run or list
    if [ "$dry_run" = false ]; then
        if ! check_prerequisites; then
            exit 1
        fi
    fi
    
    echo ""
    
    # Execute based on mode
    case $mode in
        all)
            log_info "Mode: Create ALL issues from all agent scripts"
            if [ "$dry_run" = true ]; then
                log_info "[DRY RUN] Would execute:"
                log_info "  - $AGENT_SCRIPTS_DIR/create_housekeeping_issues.sh"
                log_info "  - $AGENT_SCRIPTS_DIR/create_all_task_issues.sh"
            else
                execute_script "$AGENT_SCRIPTS_DIR/create_housekeeping_issues.sh"
                echo ""
                execute_script "$AGENT_SCRIPTS_DIR/create_all_task_issues.sh"
            fi
            ;;
            
        housekeeping)
            log_info "Mode: Create housekeeping and refactoring issues"
            if [ "$dry_run" = true ]; then
                log_info "[DRY RUN] Would execute: $AGENT_SCRIPTS_DIR/create_housekeeping_issues.sh"
            else
                execute_script "$AGENT_SCRIPTS_DIR/create_housekeeping_issues.sh"
            fi
            ;;
            
        tasks)
            log_info "Mode: Create issues for all open/assigned tasks"
            if [ "$dry_run" = true ]; then
                log_info "[DRY RUN] Would execute: $AGENT_SCRIPTS_DIR/create_all_task_issues.sh"
            else
                execute_script "$AGENT_SCRIPTS_DIR/create_all_task_issues.sh"
            fi
            ;;
            
        specific)
            log_info "Mode: Execute specific script: $specific_script"
            local script_path="$AGENT_SCRIPTS_DIR/$specific_script"
            if [ ! -f "$script_path" ]; then
                # Try with .sh extension
                script_path="$AGENT_SCRIPTS_DIR/${specific_script}.sh"
            fi
            
            if [ "$dry_run" = true ]; then
                log_info "[DRY RUN] Would execute: $script_path"
            else
                execute_script "$script_path"
            fi
            ;;
    esac
    
    echo ""
    log_success "GitHub issues creation process completed"
    echo ""
    log_info "Next steps:"
    log_info "  1. Review created issues at https://github.com/sddevelopment-be/quickstart_agent-augmented-development/issues"
    log_info "  2. Agents can process tasks from work/collaboration/"
    log_info "  3. Update issue status as work progresses"
    echo ""
}

# Execute main function
main "$@"
