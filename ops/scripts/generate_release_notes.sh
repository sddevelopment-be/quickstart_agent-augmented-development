#!/bin/sh
# generate_release_notes.sh - Generate release notes from repository artifacts
#
# Purpose: Extract version-specific changes and format for GitHub Release
# Compliant: POSIX sh (works with dash, bash, sh, ash)
# Author: DevOps Danny (Build Automation Specialist)
# Related: ADR-013 (Zip-Based Framework Distribution)
#
# Exit Codes:
#   0 - Success
#   1 - Missing required parameter (VERSION)
#   2 - Repository root not found
#   3 - No ADRs or changelog found
#
# Usage:
#   generate_release_notes.sh [OPTIONS] VERSION
#
# Arguments:
#   VERSION         Framework version to generate notes for (e.g., 1.0.0)
#
# Options:
#   --output FILE      Output file (default: stdout)
#   --previous VERSION Previous version for comparison
#   --help             Display this help message
#
# Environment:
#   REPO_ROOT          Override repository root (default: auto-detect)
#

set -e  # Exit on error

# Configuration defaults
VERSION=""
PREVIOUS_VERSION=""
OUTPUT_FILE=""
REPO_ROOT=""

# Logging functions
log_info() {
    printf "[INFO] %s\n" "$1" >&2
}

log_error() {
    printf "[ERROR] %s\n" "$1" >&2
}

# Display help message
show_help() {
    sed -n '2,24p' "$0" | sed 's/^# \?//'
    exit 0
}

# Parse command line arguments
parse_args() {
    while [ $# -gt 0 ]; do
        case "$1" in
            --output)
                if [ -z "$2" ] || [ "${2#-}" != "$2" ]; then
                    log_error "Option --output requires an argument"
                    exit 1
                fi
                OUTPUT_FILE="$2"
                shift 2
                ;;
            --previous)
                if [ -z "$2" ] || [ "${2#-}" != "$2" ]; then
                    log_error "Option --previous requires an argument"
                    exit 1
                fi
                PREVIOUS_VERSION="$2"
                shift 2
                ;;
            --help|-h)
                show_help
                ;;
            -*)
                log_error "Unknown option: $1"
                show_help
                ;;
            *)
                if [ -z "$VERSION" ]; then
                    VERSION="$1"
                else
                    log_error "Unexpected argument: $1"
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # Validate required arguments
    if [ -z "$VERSION" ]; then
        log_error "VERSION is required"
        show_help
    fi
}

# Detect repository root
detect_repo_root() {
    if [ -n "$REPO_ROOT" ]; then
        return
    fi

    # Try to find .git directory
    current_dir="$(pwd)"
    while [ "$current_dir" != "/" ]; do
        if [ -d "$current_dir/.git" ]; then
            REPO_ROOT="$current_dir"
            return
        fi
        current_dir="$(dirname "$current_dir")"
    done

    log_error "Could not detect repository root"
    exit 2
}

# Output function (to file or stdout)
output() {
    if [ -n "$OUTPUT_FILE" ]; then
        printf "%s\n" "$1" >> "$OUTPUT_FILE"
    else
        printf "%s\n" "$1"
    fi
}

# Extract changelog section for version
extract_changelog() {
    changelog_file="$REPO_ROOT/CHANGELOG.md"
    
    if [ ! -f "$changelog_file" ]; then
        log_info "No CHANGELOG.md found, skipping changelog section"
        return
    fi

    log_info "Extracting changelog for version $VERSION"
    
    # Try to find version section in changelog
    # This is a simple extraction - adjust based on actual CHANGELOG format
    if grep -q "## \[*$VERSION" "$changelog_file" 2>/dev/null; then
        output "## Changes"
        output ""
        # Extract section between this version and next version marker
        sed -n "/## \[*$VERSION/,/## \[/p" "$changelog_file" | sed '$d' | tail -n +2
        output ""
    else
        log_info "No specific changelog entry found for version $VERSION"
    fi
}

# List new or modified ADRs
list_adrs() {
    adr_dir="$REPO_ROOT/docs/architecture/adrs"
    
    if [ ! -d "$adr_dir" ]; then
        log_info "No ADR directory found, skipping ADR section"
        return
    fi

    log_info "Listing ADRs"
    
    output "## Architecture Decision Records"
    output ""
    
    # If previous version specified, try to find new/modified ADRs
    if [ -n "$PREVIOUS_VERSION" ] && command -v git >/dev/null 2>&1; then
        # Try to find ADRs added or modified since previous tag
        prev_tag="v$PREVIOUS_VERSION"
        if git rev-parse "$prev_tag" >/dev/null 2>&1; then
            log_info "Comparing with previous version: $prev_tag"
            
            new_adrs=$(git diff --name-only "$prev_tag" HEAD -- "$adr_dir" 2>/dev/null | grep "\.md$" || true)
            
            if [ -n "$new_adrs" ]; then
                output "### New or Updated ADRs:"
                output ""
                for adr in $new_adrs; do
                    adr_name=$(basename "$adr" .md)
                    output "- **$adr_name**"
                done
                output ""
            fi
        fi
    fi
    
    # List all current ADRs
    output "### All ADRs in this Release:"
    output ""
    
    adr_count=0
    for adr_file in "$adr_dir"/ADR-*.md; do
        if [ -f "$adr_file" ]; then
            adr_name=$(basename "$adr_file" .md)
            # Extract title from first heading if available
            title=$(grep "^#" "$adr_file" | head -1 | sed 's/^#* *//' || echo "")
            if [ -n "$title" ]; then
                output "- **$adr_name**: $title"
            else
                output "- **$adr_name**"
            fi
            adr_count=$((adr_count + 1))
        fi
    done
    
    if [ $adr_count -eq 0 ]; then
        output "_No ADRs found_"
    fi
    
    output ""
}

# Generate installation instructions
generate_installation_section() {
    output "## Installation"
    output ""
    output "### New Installation"
    output ""
    output '```bash'
    output "# Extract the archive"
    output "unzip quickstart-framework-$VERSION.zip"
    output ""
    output "# Install into your project"
    output "cd quickstart-framework-$VERSION"
    output "./scripts/framework_install.sh /path/to/your/project"
    output '```'
    output ""
    output "### Upgrading from Previous Version"
    output ""
    output '```bash'
    output "# Extract the archive"
    output "unzip quickstart-framework-$VERSION.zip"
    output ""
    output "# Upgrade existing installation (safe - creates .framework-new for conflicts)"
    output "cd quickstart-framework-$VERSION"
    output "./scripts/framework_upgrade.sh /path/to/your/project"
    output '```'
    output ""
}

# Generate what's included section
generate_contents_section() {
    output "## What's Included"
    output ""
    output "This release includes:"
    output ""
    output "- **Agent Profiles**: Core agent definitions and directives"
    output "- **Templates**: Architecture, documentation, and task templates"
    output "- **Validation**: Schema validation and testing framework"
    output "- **Scripts**: Installation and upgrade automation"
    output "- **Documentation**: Complete framework specification and guides"
    output ""
}

# Generate main release notes
generate_release_notes() {
    # Clear output file if it exists
    if [ -n "$OUTPUT_FILE" ]; then
        > "$OUTPUT_FILE"
    fi
    
    # Header
    output "# Quickstart Framework Release $VERSION"
    output ""
    output "**Release Date**: $(date +%Y-%m-%d)"
    output ""
    
    # Overview
    output "## Overview"
    output ""
    output "This release of the quickstart-agent-augmented-development framework provides the"
    output "core infrastructure for agent-augmented development workflows. It includes agent"
    output "profiles, directives, templates, and automation scripts designed for reproducible,"
    output "traceable development processes."
    output ""
    
    # Changelog section
    extract_changelog
    
    # ADR section
    list_adrs
    
    # Installation section
    generate_installation_section
    
    # Contents section
    generate_contents_section
    
    # Footer
    output "## Verification"
    output ""
    output "Verify the package integrity using the provided checksum:"
    output ""
    output '```bash'
    output "sha256sum -c SHA256SUMS"
    output '```'
    output ""
    output "## Documentation"
    output ""
    output "- **Agent Specification**: See \`framework_core/AGENTS.md\`"
    output "- **Templates**: See \`framework_core/docs/templates/\`"
    output "- **Validation**: See \`framework_core/validation/README.md\`"
    output ""
    output "## Support"
    output ""
    output "For questions, issues, or contributions, please refer to the project repository:"
    output "https://github.com/sddevelopment-be/quickstart_agent-augmented-development"
    output ""
}

# Main execution
main() {
    parse_args "$@"
    detect_repo_root
    
    log_info "Generating release notes for version $VERSION"
    if [ -n "$OUTPUT_FILE" ]; then
        log_info "Output file: $OUTPUT_FILE"
    else
        log_info "Output: stdout"
    fi
    
    generate_release_notes
    
    log_info "Release notes generation complete"
}

# Run main function
main "$@"
