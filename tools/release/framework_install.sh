#!/bin/sh
# framework_install.sh - Install Quickstart Agent-Augmented Development Framework
#
# This script performs a clean installation of the framework into a target repository.
# It respects existing files and never overwrites local customizations.
#
# Usage: ./framework_install.sh [OPTIONS] RELEASE_DIR TARGET_DIR
#
# Options:
#   --dry-run          Show what would be installed without making changes
#   --verbose          Enable detailed output
#   --help             Display this help message
#   --version          Display script version
#
# Requirements:
#   - POSIX-compliant shell
#   - Standard utilities: find, cp, sha256sum (or shasum), date
#
# Exit codes:
#   0 - Success
#   1 - Invalid arguments or missing directories
#   2 - Invalid release artifact structure
#   3 - Installation failed
#
# References:
#   - ADR-013: Zip-Based Framework Distribution
#   - ADR-014: Framework Guardian Agent
#   - docs/architecture/design/distribution_of_releases_technical_design.md

set -e  # Exit on error
set -u  # Error on undefined variables

# Script version
SCRIPT_VERSION="1.0.0"

# Color codes for output (if terminal supports it)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

# Counters
NEW_COUNT=0
SKIPPED_COUNT=0
ERROR_COUNT=0

# Flags
DRY_RUN=0
VERBOSE=0

# Functions

print_usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] RELEASE_DIR TARGET_DIR

Install the Quickstart Agent-Augmented Development Framework into a target repository.

Arguments:
  RELEASE_DIR    Path to extracted release artifact (containing framework_core/, scripts/, META/)
  TARGET_DIR     Path to target repository where framework will be installed

Options:
  --dry-run      Show what would be installed without making changes
  --verbose      Enable detailed output
  --help         Display this help message
  --version      Display script version

Examples:
  # Install framework into current directory
  ./framework_install.sh ./quickstart-framework-1.0.0 .

  # Dry run to see what would be installed
  ./framework_install.sh --dry-run ./quickstart-framework-1.0.0 /path/to/repo

  # Verbose mode for detailed output
  ./framework_install.sh --verbose ./quickstart-framework-1.0.0 /path/to/repo

Exit Codes:
  0 - Success
  1 - Invalid arguments or missing directories
  2 - Invalid release artifact structure
  3 - Installation failed

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
    
    local required_dirs="framework_core scripts META"
    local required_files="META/MANIFEST.yml"
    local missing=""
    
    for dir in ${required_dirs}; do
        if [[ ! -d "${release_dir}/${dir}" ]]; then
            missing="${missing} ${dir}/"
        fi
    done
    
    for file in ${required_files}; do
        if [[ ! -f "${release_dir}/${file}" ]]; then
            missing="${missing} ${file}"
        fi
    done
    
    if [[ -n "${missing}" ]]; then
        log_error "Invalid release artifact structure. Missing:${missing}"
        log_error "Expected structure:"
        log_error "  framework_core/  - Core framework files"
        log_error "  scripts/         - Installation scripts"
        log_error "  META/            - Metadata and manifest"
        log_error "    MANIFEST.yml   - File inventory with checksums"
        return 2
    fi
    
    log_success "Release artifact structure validated"
    return 0
}

# Check if framework is already installed
check_existing_installation() {
    local target_dir="$1"
    
    if [[ -f "${target_dir}/.framework_meta.yml" ]]; then
        log_warning "Framework appears to be already installed in ${target_dir}"
        log_warning "Found existing .framework_meta.yml"
        log_warning "To upgrade an existing installation, use framework_upgrade.sh instead"
        return 1
    fi
    
    return 0
}

# Parse YAML manifest (simple parser for our specific format)
parse_manifest() {
    local manifest_file="$1"
    
    if [[ ! -f "${manifest_file}" ]]; then
        log_error "Manifest file not found: ${manifest_file}"
        return 2
    fi
    
    # Check for valid YAML (basic validation)
    if ! grep -q "^version:" "${manifest_file}"; then
        log_error "Invalid manifest format: missing version field"
        return 2
    fi
    
    return 0
}

# Install a single file
install_file() {
    local src_file="$1"
    local dest_file="$2"
    local expected_checksum="$3"
    
    # Check if destination already exists
    if [[ -f "${dest_file}" ]]; then
        log_verbose "SKIP: ${dest_file} (already exists)"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        return 0
    fi
    
    # Validate checksum if provided
    if [[ -n "${expected_checksum}" ]] && [[ "${expected_checksum}" != "null" ]]; then
        local actual_checksum
        actual_checksum=$(calculate_sha256 "${src_file}")
        
        if [[ "${actual_checksum}" != "${expected_checksum}" ]]; then
            log_warning "Checksum mismatch for ${src_file}"
            log_verbose "  Expected: ${expected_checksum}"
            log_verbose "  Actual:   ${actual_checksum}"
            ERROR_COUNT=$((ERROR_COUNT + 1))
            return 1
        fi
    fi
    
    if [[ "${DRY_RUN}" = "1" ]]; then
        log_verbose "WOULD INSTALL: ${dest_file}"
        NEW_COUNT=$((NEW_COUNT + 1))
        return 0
    fi
    
    # Create parent directory if needed
    dest_dir=$(dirname "${dest_file}")
    if [[ ! -d "${dest_dir}" ]]; then
        mkdir -p "${dest_dir}"
    fi
    
    # Copy file preserving permissions
    if cp -p "${src_file}" "${dest_file}"; then
        log_verbose "NEW: ${dest_file}"
        NEW_COUNT=$((NEW_COUNT + 1))
        return 0
    else
        log_error "Failed to copy ${src_file} to ${dest_file}"
        ERROR_COUNT=$((ERROR_COUNT + 1))
        return 1
    fi
}

# Install framework files
install_framework_files() {
    local release_dir="$1"
    local target_dir="$2"
    local manifest_file="${release_dir}/META/MANIFEST.yml"
    
    log_info "Installing framework files..."
    
    # Find all files in framework_core
    local core_dir="${release_dir}/framework_core"
    local temp_counts
    temp_counts=$(mktemp)
    echo "0 0 0" > "${temp_counts}"
    
    # Use find to iterate over all files (POSIX-compliant)
    find "${core_dir}" -type f | while IFS= read -r src_file; do
        # Calculate relative path
        rel_path="${src_file#${core_dir}/}"
        dest_file="${target_dir}/${rel_path}"
        
        # Read current counts
        read new_count skip_count err_count < "${temp_counts}"
        
        # Check if destination already exists
        if [[ -f "${dest_file}" ]]; then
            log_verbose "SKIP: ${dest_file} (already exists)"
            skip_count=$((skip_count + 1))
        else
            if [[ "${DRY_RUN}" = "1" ]]; then
                log_verbose "WOULD INSTALL: ${dest_file}"
                new_count=$((new_count + 1))
            else
                # Create parent directory if needed
                dest_dir=$(dirname "${dest_file}")
                if [[ ! -d "${dest_dir}" ]]; then
                    mkdir -p "${dest_dir}"
                fi
                
                # Copy file preserving permissions
                if cp -p "${src_file}" "${dest_file}"; then
                    log_verbose "NEW: ${dest_file}"
                    new_count=$((new_count + 1))
                else
                    log_error "Failed to copy ${src_file} to ${dest_file}"
                    err_count=$((err_count + 1))
                fi
            fi
        fi
        
        # Write updated counts
        echo "${new_count} ${skip_count} ${err_count}" > "${temp_counts}"
    done
    
    # Read final counts
    read NEW_COUNT SKIPPED_COUNT ERROR_COUNT < "${temp_counts}"
    rm -f "${temp_counts}"
    
    log_success "Framework files processed"
}

# Create .framework_meta.yml
create_framework_meta() {
    local target_dir="$1"
    local version="$2"
    local source_release="$3"
    
    if [[ "${DRY_RUN}" = "1" ]]; then
        log_info "Would create .framework_meta.yml"
        return 0
    fi
    
    local meta_file="${target_dir}/.framework_meta.yml"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    cat > "${meta_file}" << EOF
# Framework Installation Metadata
# Generated by framework_install.sh v${SCRIPT_VERSION}
# Do not edit manually

framework_version: ${version}
installed_at: ${timestamp}
source_release: ${source_release}
installer_version: ${SCRIPT_VERSION}
EOF
    
    log_success "Created ${meta_file}"
}

# Extract version from manifest
get_version_from_manifest() {
    local manifest_file="$1"
    
    # Simple grep-based extraction (works for simple YAML)
    grep "^version:" "${manifest_file}" | head -1 | sed 's/^version: *//' | tr -d "\"'"
}

# Print installation summary
print_summary() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Framework Installation Summary"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [[ "${DRY_RUN}" = "1" ]]; then
        echo "Mode: DRY RUN (no changes made)"
    else
        echo "Mode: LIVE"
    fi
    
    echo ""
    echo "Results:"
    echo "  ${GREEN}NEW:${NC}      ${NEW_COUNT} files"
    echo "  ${YELLOW}SKIPPED:${NC}  ${SKIPPED_COUNT} files (already exist)"
    
    if [[ "${ERROR_COUNT}" -gt 0 ]]; then
        echo "  ${RED}ERRORS:${NC}   ${ERROR_COUNT}"
    fi
    
    echo ""
    
    if [[ "${DRY_RUN}" = "1" ]]; then
        echo "To perform actual installation, run without --dry-run flag"
    elif [[ "${ERROR_COUNT}" -eq 0 ]]; then
        echo "${GREEN}✓${NC} Installation completed successfully!"
        echo ""
        echo "Next steps:"
        echo "  1. Review installed files in your repository"
        echo "  2. Check .framework_meta.yml for installation details"
        echo "  3. Consult docs/HOW_TO_USE/ for framework usage guides"
        echo "  4. For upgrades, use framework_upgrade.sh"
    else
        echo "${RED}✗${NC} Installation completed with errors"
        echo "Please review error messages above and retry"
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
                echo "framework_install.sh version ${SCRIPT_VERSION}"
                exit 0
                ;;
            --dry-run)
                DRY_RUN=1
                shift
                ;;
            --verbose|-v)
                VERBOSE=1
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
    
    # Print banner
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Framework Installation"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Release:  ${RELEASE_DIR}"
    echo "Target:   ${TARGET_DIR}"
    if [[ "${DRY_RUN}" = "1" ]]; then
        echo "Mode:     DRY RUN"
    fi
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Validate release structure
    validate_release_structure "${RELEASE_DIR}" || exit 2
    
    # Check for existing installation
    if ! check_existing_installation "${TARGET_DIR}"; then
        log_error "Installation aborted"
        exit 1
    fi
    
    # Parse manifest
    manifest_file="${RELEASE_DIR}/META/MANIFEST.yml"
    parse_manifest "${manifest_file}" || exit 2
    
    # Get version from manifest
    version=$(get_version_from_manifest "${manifest_file}")
    log_info "Installing framework version: ${version}"
    
    # Install framework files
    install_framework_files "${RELEASE_DIR}" "${TARGET_DIR}"
    
    # Create framework metadata
    source_release=$(basename "${RELEASE_DIR}")
    create_framework_meta "${TARGET_DIR}" "${version}" "${source_release}"
    
    # Print summary
    print_summary
    
    # Exit with appropriate code
    if [[ "${ERROR_COUNT}" -gt 0 ]]; then
        exit 3
    else
        exit 0
    fi
}

# Run main function
main "$@"
