#!/bin/sh
# framework_upgrade.sh - Upgrade Quickstart Agent-Augmented Development Framework
#
# This script upgrades an existing framework installation while preserving
# local customizations and detecting conflicts.
#
# Usage: ./framework_upgrade.sh [OPTIONS] RELEASE_DIR TARGET_DIR
#
# Options:
#   --dry-run          Show upgrade plan without making changes
#   --plan             Generate upgrade plan for Framework Guardian
#   --verbose          Enable detailed output
#   --no-backup        Skip creating .bak backups of conflicted files
#   --help             Display this help message
#   --version          Display script version
#
# Requirements:
#   - POSIX-compliant shell
#   - Existing framework installation (.framework_meta.yml must exist)
#   - Standard utilities: find, cp, sha256sum (or shasum), date
#
# Exit codes:
#   0 - Success (may have conflicts requiring manual resolution)
#   1 - Invalid arguments or missing directories
#   2 - Invalid release artifact or no existing installation
#   3 - Upgrade failed
#
# References:
#   - ADR-013: Zip-Based Framework Distribution
#   - ADR-014: Framework Guardian Agent
#   - docs/architecture/design/distribution_of_releases_technical_design.md

set -e  # Exit on error (but we'll handle some errors)
set -u  # Error on undefined variables

# Script version
SCRIPT_VERSION="1.0.0"

# Color codes for output
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    MAGENTA='\033[0;35m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    MAGENTA=''
    NC=''
fi

# Counters
NEW_COUNT=0
UNCHANGED_COUNT=0
CONFLICT_COUNT=0
ERROR_COUNT=0
SKIPPED_LOCAL_COUNT=0

# Flags
DRY_RUN=0
PLAN_MODE=0
VERBOSE=0
NO_BACKUP=0

# Report file
REPORT_FILE=""

# Functions

print_usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] RELEASE_DIR TARGET_DIR

Upgrade an existing framework installation to a new version.

Arguments:
  RELEASE_DIR    Path to extracted release artifact (containing framework_core/, scripts/, META/)
  TARGET_DIR     Path to target repository with existing framework installation

Options:
  --dry-run      Show upgrade plan without making changes
  --plan         Generate upgrade plan for Framework Guardian consumption
  --verbose      Enable detailed output
  --no-backup    Skip creating .bak backups of conflicted files
  --help         Display this help message
  --version      Display script version

Upgrade Behavior:
  NEW        - File missing in target, will be copied
  UNCHANGED  - File identical to release (checksum match), no action
  CONFLICT   - File differs from release, creates .framework-new file
  PROTECTED  - File in local/ directory, never modified

Examples:
  # Dry run to preview upgrade
  ./framework_upgrade.sh --dry-run ./quickstart-framework-1.1.0 .

  # Perform actual upgrade
  ./framework_upgrade.sh ./quickstart-framework-1.1.0 /path/to/repo

  # Generate plan for Framework Guardian
  ./framework_upgrade.sh --plan ./quickstart-framework-1.1.0 /path/to/repo

  # Verbose mode with backup disabled
  ./framework_upgrade.sh --verbose --no-backup ./quickstart-framework-1.1.0 /path/to/repo

After Upgrade:
  - Review upgrade-report.txt for summary
  - Check .framework-new files for conflicts
  - Use Framework Guardian agent to resolve conflicts
  - Review backups (.bak.TIMESTAMP) if manual merge needed

Exit Codes:
  0 - Success (check for conflicts in report)
  1 - Invalid arguments or missing directories
  2 - No existing installation or invalid artifact
  3 - Upgrade failed

For more information, see:
  - docs/architecture/adrs/ADR-013-zip-distribution.md
  - docs/architecture/adrs/ADR-014-framework-guardian-agent.md
  - docs/HOW_TO_USE/framework_install.md
EOF
}

log_info() {
    echo "${BLUE}ℹ${NC} $*"
}

log_success() {
    echo "${GREEN}✓${NC} $*"
}

log_warning() {
    echo "${YELLOW}⚠${NC} $*"
}

log_error() {
    echo "${RED}✗${NC} $*" >&2
}

log_conflict() {
    echo "${MAGENTA}⚡${NC} $*"
}

log_verbose() {
    if [[ "${VERBOSE}" = "1" ]]; then
        echo "  $*"
    fi
}

# Calculate SHA256 checksum (cross-platform)
calculate_sha256() {
    local file="$1"
    
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "${file}" | awk '{print $1}'
    elif command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "${file}" | awk '{print $1}'
    else
        log_error "Neither sha256sum nor shasum found. Cannot verify checksums."
        exit 3
    fi
}

# Validate release artifact structure
validate_release_structure() {
    local release_dir="$1"
    
    log_info "Validating release artifact structure..."
    
    if [[ ! -d "${release_dir}/framework_core" ]] || \
       [[ ! -d "${release_dir}/META" ]] || \
       [[ ! -f "${release_dir}/META/MANIFEST.yml" ]]; then
        log_error "Invalid release artifact structure"
        return 2
    fi
    
    log_success "Release artifact structure validated"
    return 0
}

# Check for existing installation
check_existing_installation() {
    local target_dir="$1"
    
    if [[ ! -f "${target_dir}/.framework_meta.yml" ]]; then
        log_error "No existing framework installation found in ${target_dir}"
        log_error "Missing .framework_meta.yml file"
        log_error "For clean installation, use framework_install.sh instead"
        return 2
    fi
    
    log_success "Existing framework installation detected"
    return 0
}

# Get current framework version
get_current_version() {
    local target_dir="$1"
    local meta_file="${target_dir}/.framework_meta.yml"
    
    if [[ -f "${meta_file}" ]]; then
        grep "^framework_version:" "${meta_file}" | head -1 | sed 's/^framework_version: *//' | tr -d "\"'"
    else
        echo "unknown"
    fi
}

# Get version from manifest
get_version_from_manifest() {
    local manifest_file="$1"
    
    grep "^version:" "${manifest_file}" | head -1 | sed 's/^version: *//' | tr -d "\"'"
}

# Check if path is in protected local directory
is_local_path() {
    local path="$1"
    
    case "${path}" in
        local/*|./local/*)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Create backup of file
create_backup() {
    local file="$1"
    
    if [[ "${NO_BACKUP}" = "1" ]]; then
        return 0
    fi
    
    if [[ ! -f "${file}" ]]; then
        return 0
    fi
    
    local timestamp
    timestamp=$(date -u +"%Y%m%d_%H%M%S")
    local backup_file="${file}.bak.${timestamp}"
    
    if [[ "${DRY_RUN}" = "1" ]]; then
        log_verbose "Would create backup: ${backup_file}"
        return 0
    fi
    
    if cp -p "${file}" "${backup_file}"; then
        log_verbose "Backup created: ${backup_file}"
        return 0
    else
        log_warning "Failed to create backup: ${backup_file}"
        return 1
    fi
}

# Process a single file upgrade
process_file() {
    local src_file="$1"
    local dest_file="$2"
    local rel_path="$3"
    local temp_counts="$4"
    
    # Read current counts
    read new_c unch_c conf_c err_c local_c < "${temp_counts}"
    
    # Check if in local/ directory (protected)
    if is_local_path "${rel_path}"; then
        log_verbose "PROTECTED: ${rel_path} (in local/ directory)"
        local_c=$((local_c + 1))
        echo "PROTECTED|${rel_path}|local directory never modified" >> "${REPORT_FILE}"
        echo "${new_c} ${unch_c} ${conf_c} ${err_c} ${local_c}" > "${temp_counts}"
        return 0
    fi
    
    # File doesn't exist in target - NEW
    if [[ ! -f "${dest_file}" ]]; then
        if [[ "${DRY_RUN}" = "1" ]]; then
            log_verbose "NEW: ${rel_path} (would be copied)"
        else
            # Create parent directory if needed
            dest_dir=$(dirname "${dest_file}")
            if [[ ! -d "${dest_dir}" ]]; then
                mkdir -p "${dest_dir}"
            fi
            
            if cp -p "${src_file}" "${dest_file}"; then
                log_verbose "NEW: ${rel_path}"
            else
                log_error "Failed to copy: ${rel_path}"
                err_c=$((err_c + 1))
                echo "ERROR|${rel_path}|copy failed" >> "${REPORT_FILE}"
                echo "${new_c} ${unch_c} ${conf_c} ${err_c} ${local_c}" > "${temp_counts}"
                return 1
            fi
        fi
        new_c=$((new_c + 1))
        echo "NEW|${rel_path}|copied from release" >> "${REPORT_FILE}"
        echo "${new_c} ${unch_c} ${conf_c} ${err_c} ${local_c}" > "${temp_counts}"
        return 0
    fi
    
    # File exists - check if identical
    local src_checksum
    local dest_checksum
    
    src_checksum=$(calculate_sha256 "${src_file}")
    dest_checksum=$(calculate_sha256 "${dest_file}")
    
    if [[ "${src_checksum}" = "${dest_checksum}" ]]; then
        # Identical - UNCHANGED
        log_verbose "UNCHANGED: ${rel_path}"
        unch_c=$((unch_c + 1))
        echo "UNCHANGED|${rel_path}|identical to release" >> "${REPORT_FILE}"
        echo "${new_c} ${unch_c} ${conf_c} ${err_c} ${local_c}" > "${temp_counts}"
        return 0
    else
        # Different - CONFLICT
        if [[ "${DRY_RUN}" = "1" ]]; then
            log_verbose "CONFLICT: ${rel_path} (would create .framework-new)"
        else
            # Create backup of existing file
            create_backup "${dest_file}"
            
            # Create .framework-new file with new version
            local new_file="${dest_file}.framework-new"
            if cp -p "${src_file}" "${new_file}"; then
                log_conflict "CONFLICT: ${rel_path} (created .framework-new)"
            else
                log_error "Failed to create .framework-new for: ${rel_path}"
                err_c=$((err_c + 1))
                echo "ERROR|${rel_path}|failed to create .framework-new" >> "${REPORT_FILE}"
                echo "${new_c} ${unch_c} ${conf_c} ${err_c} ${local_c}" > "${temp_counts}"
                return 1
            fi
        fi
        conf_c=$((conf_c + 1))
        echo "CONFLICT|${rel_path}|differs from release - manual merge needed" >> "${REPORT_FILE}"
        echo "${new_c} ${unch_c} ${conf_c} ${err_c} ${local_c}" > "${temp_counts}"
        return 0
    fi
}

# Upgrade framework files
upgrade_framework_files() {
    local release_dir="$1"
    local target_dir="$2"
    
    log_info "Processing framework files..."
    
    local core_dir="${release_dir}/framework_core"
    local temp_counts
    temp_counts=$(mktemp)
    echo "0 0 0 0 0" > "${temp_counts}"
    
    # Process all files in framework_core (POSIX-compliant)
    find "${core_dir}" -type f | while IFS= read -r src_file; do
        # Calculate relative path
        rel_path="${src_file#${core_dir}/}"
        dest_file="${target_dir}/${rel_path}"
        
        process_file "${src_file}" "${dest_file}" "${rel_path}" "${temp_counts}"
    done
    
    # Read final counts
    read NEW_COUNT UNCHANGED_COUNT CONFLICT_COUNT ERROR_COUNT SKIPPED_LOCAL_COUNT < "${temp_counts}"
    rm -f "${temp_counts}"
    
    log_success "Framework files processed"
}

# Update .framework_meta.yml
update_framework_meta() {
    local target_dir="$1"
    local version="$2"
    local source_release="$3"
    local old_version="$4"
    
    if [[ "${DRY_RUN}" = "1" ]]; then
        log_info "Would update .framework_meta.yml (${old_version} -> ${version})"
        return 0
    fi
    
    local meta_file="${target_dir}/.framework_meta.yml"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Backup old meta file
    if [[ -f "${meta_file}" ]]; then
        cp "${meta_file}" "${meta_file}.backup"
    fi
    
    cat > "${meta_file}" << EOF
# Framework Installation Metadata
# Updated by framework_upgrade.sh v${SCRIPT_VERSION}
# Previous version: ${old_version}

framework_version: ${version}
installed_at: ${timestamp}
source_release: ${source_release}
installer_version: ${SCRIPT_VERSION}
upgraded_from: ${old_version}
upgrade_date: ${timestamp}
EOF
    
    log_success "Updated .framework_meta.yml (${old_version} -> ${version})"
}

# Generate upgrade report
generate_upgrade_report() {
    local target_dir="$1"
    local old_version="$2"
    local new_version="$3"
    
    local report_path="${target_dir}/upgrade-report.txt"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
    
    if [[ "${DRY_RUN}" = "1" ]]; then
        report_path="${target_dir}/upgrade-report-dryrun.txt"
    fi
    
    cat > "${report_path}" << EOF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework Upgrade Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated: ${timestamp}
Script Version: ${SCRIPT_VERSION}

Upgrade Details:
  From Version: ${old_version}
  To Version:   ${new_version}
  Mode:         $([[ "${DRY_RUN}" = "1" ]] && echo "DRY RUN" || echo "LIVE")

Summary:
  NEW:       ${NEW_COUNT} files (copied from release)
  UNCHANGED: ${UNCHANGED_COUNT} files (identical to release)
  CONFLICT:  ${CONFLICT_COUNT} files (manual merge required)
  PROTECTED: ${SKIPPED_LOCAL_COUNT} files (in local/ directory)
  ERRORS:    ${ERROR_COUNT}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF
    
    # Append detailed file list
    if [[ -f "${REPORT_FILE}" ]]; then
        while IFS='|' read -r status path description; do
            printf "%-12s %s\n" "[${status}]" "${path}" >> "${report_path}"
            if [[ "${VERBOSE}" = "1" ]]; then
                printf "             %s\n" "${description}" >> "${report_path}"
            fi
        done < "${REPORT_FILE}"
    fi
    
    cat >> "${report_path}" << EOF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF
    
    if [[ "${CONFLICT_COUNT}" -gt 0 ]]; then
        cat >> "${report_path}" << EOF
⚡ CONFLICTS DETECTED (${CONFLICT_COUNT} files)

For each conflict, a .framework-new file has been created with the
new version. The original file remains unchanged.

To resolve conflicts:
  1. Review each .framework-new file
  2. Compare with original file to identify changes
  3. Manually merge changes or replace original with .framework-new
  4. Use Framework Guardian agent for automated conflict analysis:
     - Run in Audit mode for detailed analysis
     - Run in Upgrade mode for merge recommendations
  5. Delete .framework-new files after resolution

Find conflicts:
  find . -name "*.framework-new" -type f

EOF
    fi
    
    if [[ "${NEW_COUNT}" -gt 0 ]]; then
        cat >> "${report_path}" << EOF
✓ NEW FILES ADDED (${NEW_COUNT} files)

These files were added to your repository from the new release.
Review them to understand new features and capabilities.

EOF
    fi
    
    if [[ "${DRY_RUN}" = "1" ]]; then
        cat >> "${report_path}" << EOF
ℹ DRY RUN MODE

No changes were made to your repository.
Run without --dry-run to perform the actual upgrade.

EOF
    else
        cat >> "${report_path}" << EOF
✓ UPGRADE COMPLETE

The framework has been upgraded successfully.
Review conflicts and consult documentation for next steps.

EOF
    fi
    
    cat >> "${report_path}" << EOF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For more information:
  - Framework Guardian: .github/agents/framework-guardian.agent.md
  - Installation Guide: docs/HOW_TO_USE/framework_install.md
  - ADR-013: docs/architecture/adrs/ADR-013-zip-distribution.md
  - ADR-014: docs/architecture/adrs/ADR-014-framework-guardian-agent.md

EOF
    
    if [[ "${DRY_RUN}" = "1" ]]; then
        log_info "Dry run report saved: ${report_path}"
    else
        log_success "Upgrade report saved: ${report_path}"
    fi
}

# Print summary to console
print_summary() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Framework Upgrade Summary"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [[ "${DRY_RUN}" = "1" ]]; then
        echo "Mode: DRY RUN (no changes made)"
    else
        echo "Mode: LIVE"
    fi
    
    echo ""
    echo "Results:"
    echo "  ${GREEN}NEW:${NC}        ${NEW_COUNT} files"
    echo "  ${BLUE}UNCHANGED:${NC}  ${UNCHANGED_COUNT} files"
    echo "  ${MAGENTA}CONFLICT:${NC}   ${CONFLICT_COUNT} files"
    echo "  ${YELLOW}PROTECTED:${NC}  ${SKIPPED_LOCAL_COUNT} files"
    
    if [[ "${ERROR_COUNT}" -gt 0 ]]; then
        echo "  ${RED}ERRORS:${NC}     ${ERROR_COUNT}"
    fi
    
    echo ""
    
    if [[ "${CONFLICT_COUNT}" -gt 0 ]]; then
        echo "${MAGENTA}⚡${NC} Manual conflict resolution required for ${CONFLICT_COUNT} files"
        echo "   Review .framework-new files and merge changes manually"
        echo "   See upgrade-report.txt for details"
        echo ""
    fi
    
    if [[ "${DRY_RUN}" = "1" ]]; then
        echo "To perform actual upgrade, run without --dry-run flag"
    elif [[ "${ERROR_COUNT}" -eq 0 ]]; then
        echo "${GREEN}✓${NC} Upgrade completed successfully!"
        echo ""
        echo "Next steps:"
        echo "  1. Review upgrade-report.txt for detailed results"
        if [[ "${CONFLICT_COUNT}" -gt 0 ]]; then
            echo "  2. Resolve conflicts in .framework-new files"
            echo "  3. Use Framework Guardian agent for merge assistance"
        fi
        echo "  4. Test your repository with the upgraded framework"
        echo "  5. Consult docs/HOW_TO_USE/ for new features"
    else
        echo "${RED}✗${NC} Upgrade completed with errors"
        echo "Please review error messages and upgrade-report.txt"
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Main function
main() {
    # Parse command line arguments
    RELEASE_DIR=""
    TARGET_DIR=""
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --help|-h)
                print_usage
                exit 0
                ;;
            --version)
                echo "framework_upgrade.sh version ${SCRIPT_VERSION}"
                exit 0
                ;;
            --dry-run)
                DRY_RUN=1
                shift
                ;;
            --plan)
                PLAN_MODE=1
                DRY_RUN=1  # Plan mode implies dry-run
                shift
                ;;
            --verbose|-v)
                VERBOSE=1
                shift
                ;;
            --no-backup)
                NO_BACKUP=1
                shift
                ;;
            -*)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
            *)
                if [[ -z "${RELEASE_DIR}" ]]; then
                    RELEASE_DIR="$1"
                elif [[ -z "${TARGET_DIR}" ]]; then
                    TARGET_DIR="$1"
                else
                    log_error "Too many arguments"
                    print_usage
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Validate arguments
    if [[ -z "${RELEASE_DIR}" ]] || [[ -z "${TARGET_DIR}" ]]; then
        log_error "Missing required arguments"
        print_usage
        exit 1
    fi
    
    # Convert to absolute paths
    RELEASE_DIR=$(cd "${RELEASE_DIR}" && pwd)
    TARGET_DIR=$(cd "${TARGET_DIR}" && pwd)
    
    # Validate directories exist
    if [[ ! -d "${RELEASE_DIR}" ]]; then
        log_error "Release directory not found: ${RELEASE_DIR}"
        exit 1
    fi
    
    if [[ ! -d "${TARGET_DIR}" ]]; then
        log_error "Target directory not found: ${TARGET_DIR}"
        exit 1
    fi
    
    # Create temp report file
    REPORT_FILE=$(mktemp)
    
    # Print banner
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Framework Upgrade"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Release:  ${RELEASE_DIR}"
    echo "Target:   ${TARGET_DIR}"
    if [[ "${DRY_RUN}" = "1" ]]; then
        echo "Mode:     DRY RUN"
    fi
    if [[ "${PLAN_MODE}" = "1" ]]; then
        echo "Output:   PLAN (for Framework Guardian)"
    fi
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Validate release structure
    validate_release_structure "${RELEASE_DIR}" || exit 2
    
    # Check for existing installation
    check_existing_installation "${TARGET_DIR}" || exit 2
    
    # Get versions
    old_version=$(get_current_version "${TARGET_DIR}")
    new_version=$(get_version_from_manifest "${RELEASE_DIR}/META/MANIFEST.yml")
    
    log_info "Current version: ${old_version}"
    log_info "New version:     ${new_version}"
    
    if [[ "${old_version}" = "${new_version}" ]]; then
        log_warning "Target already at version ${new_version}"
        log_warning "Proceeding with upgrade (will detect changes)"
    fi
    
    # Upgrade framework files
    upgrade_framework_files "${RELEASE_DIR}" "${TARGET_DIR}"
    
    # Update framework metadata
    if [[ "${CONFLICT_COUNT}" -eq 0 ]] && [[ "${ERROR_COUNT}" -eq 0 ]]; then
        source_release=$(basename "${RELEASE_DIR}")
        update_framework_meta "${TARGET_DIR}" "${new_version}" "${source_release}" "${old_version}"
    else
        if [[ "${DRY_RUN}" != "1" ]]; then
            log_warning "Skipping .framework_meta.yml update due to conflicts/errors"
            log_warning "Resolve conflicts and run upgrade again to complete"
        fi
    fi
    
    # Generate upgrade report
    generate_upgrade_report "${TARGET_DIR}" "${old_version}" "${new_version}"
    
    # Print summary
    print_summary
    
    # Cleanup
    rm -f "${REPORT_FILE}"
    
    # Exit with appropriate code
    if [[ "${ERROR_COUNT}" -gt 0 ]]; then
        exit 3
    else
        exit 0
    fi
}

# Run main function
main "$@"
