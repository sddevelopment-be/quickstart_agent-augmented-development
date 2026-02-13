#!/bin/sh
# deploy_framework.sh - Deploy/upgrade the SDD Agent Framework from upstream releases
#
# This script fetches the latest (or specified) release from the upstream repository
# and installs or upgrades the framework in the current repository.
#
# Usage:
#   ./deploy_framework.sh [OPTIONS]
#
# Options:
#   --version VERSION    Install specific version (e.g., 1.0.0). Default: latest
#   --upgrade            Upgrade existing installation (default: fresh install)
#   --dry-run            Show what would be done without making changes
#   --skip-guardian      Skip the Guardian verification reminder
#   --help               Show this help message
#
# Requirements:
#   - curl or wget
#   - unzip
#   - GitHub CLI (gh) for private repos, or curl for public repos
#
# Exit codes:
#   0 - Success
#   1 - Invalid arguments
#   2 - Download failed
#   3 - Installation failed
#
# References:
#   - ADR-013: Zip-Based Framework Distribution
#   - ADR-014: Framework Guardian Agent

set -e
set -u

# Configuration
UPSTREAM_REPO="sddevelopment-be/quickstart_agent-augmented-development"
UPSTREAM_URL="https://github.com/${UPSTREAM_REPO}"
API_URL="https://api.github.com/repos/${UPSTREAM_REPO}"
SCRIPT_VERSION="1.0.0"

# Color codes
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    CYAN=''
    NC=''
fi

# Defaults
VERSION="latest"
MODE="install"
DRY_RUN=0
SKIP_GUARDIAN=0
TARGET_DIR="."

print_usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Deploy or upgrade the SDD Agent Framework from upstream releases.

Options:
  --version VERSION    Install specific version (e.g., 1.0.0). Default: latest
  --upgrade            Upgrade existing installation instead of fresh install
  --target DIR         Target directory (default: current directory)
  --dry-run            Show what would be done without making changes
  --skip-guardian      Skip the Framework Guardian verification reminder
  --help               Show this help message

Examples:
  # Install latest version
  ./deploy_framework.sh

  # Install specific version
  ./deploy_framework.sh --version 1.0.0

  # Upgrade existing installation
  ./deploy_framework.sh --upgrade

  # Dry run to preview changes
  ./deploy_framework.sh --upgrade --dry-run

Environment Variables:
  GITHUB_TOKEN         GitHub token for API access (optional, for private repos)

Exit Codes:
  0 - Success
  1 - Invalid arguments
  2 - Download failed
  3 - Installation failed

For more information:
  ${UPSTREAM_URL}
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

log_step() {
    echo "${CYAN}▶${NC} $*"
}

# Check for required tools
check_requirements() {
    local missing=""

    if ! command -v unzip >/dev/null 2>&1; then
        missing="${missing} unzip"
    fi

    if ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
        missing="${missing} curl/wget"
    fi

    if [[ -n "${missing}" ]]; then
        log_error "Missing required tools:${missing}"
        log_error "Please install them and try again."
        exit 1
    fi
}

# Fetch data from URL (uses curl or wget)
fetch_url() {
    local url="$1"
    local output="$2"
    local auth_header=""

    # Add auth header if token is available
    if [[ -n "${GITHUB_TOKEN:-}" ]]; then
        auth_header="Authorization: token ${GITHUB_TOKEN}"
    fi

    if command -v curl >/dev/null 2>&1; then
        if [[ -n "${auth_header}" ]]; then
            curl -fsSL -H "${auth_header}" -o "${output}" "${url}"
        else
            curl -fsSL -o "${output}" "${url}"
        fi
    elif command -v wget >/dev/null 2>&1; then
        if [[ -n "${auth_header}" ]]; then
            wget -q --header="${auth_header}" -O "${output}" "${url}"
        else
            wget -q -O "${output}" "${url}"
        fi
    else
        log_error "Neither curl nor wget available"
        return 1
    fi
}

# Fetch JSON from API
fetch_api() {
    local endpoint="$1"
    local tmp_file
    tmp_file=$(mktemp)

    if ! fetch_url "${API_URL}${endpoint}" "${tmp_file}" 2>/dev/null; then
        rm -f "${tmp_file}"
        return 1
    fi

    cat "${tmp_file}"
    rm -f "${tmp_file}"
}

# Get latest release version
get_latest_version() {
    local release_info
    release_info=$(fetch_api "/releases/latest" 2>/dev/null) || {
        log_error "Failed to fetch latest release info"
        log_error "Check if the repository has any releases: ${UPSTREAM_URL}/releases"
        return 1
    }

    # Extract tag_name (simple grep-based parsing)
    echo "${release_info}" | grep -o '"tag_name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"tag_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' | sed 's/^v//'
}

# Get download URL for a version
get_download_url() {
    local version="$1"
    local release_info
    local tag="v${version}"

    release_info=$(fetch_api "/releases/tags/${tag}" 2>/dev/null) || {
        log_error "Failed to fetch release info for version ${version}"
        return 1
    }

    # Look for the framework zip asset
    local asset_url
    asset_url=$(echo "${release_info}" | grep -o '"browser_download_url"[[:space:]]*:[[:space:]]*"[^"]*quickstart-framework[^"]*\.zip"' | head -1 | sed 's/.*"browser_download_url"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')

    if [[ -z "${asset_url}" ]]; then
        log_error "No framework artifact found in release ${version}"
        return 1
    fi

    echo "${asset_url}"
}

# Download and extract release
download_release() {
    local version="$1"
    local work_dir="$2"

    log_step "Fetching download URL for version ${version}..."
    local download_url
    download_url=$(get_download_url "${version}") || return 2

    local artifact_name="quickstart-framework-${version}.zip"
    local artifact_path="${work_dir}/${artifact_name}"

    log_step "Downloading ${artifact_name}..."
    if [[ "${DRY_RUN}" = "1" ]]; then
        log_info "[DRY RUN] Would download from: ${download_url}"
        return 0
    fi

    if ! fetch_url "${download_url}" "${artifact_path}"; then
        log_error "Failed to download release artifact"
        return 2
    fi

    log_success "Downloaded ${artifact_name}"

    # Extract
    log_step "Extracting artifact..."
    if ! unzip -q "${artifact_path}" -d "${work_dir}"; then
        log_error "Failed to extract artifact"
        return 2
    fi

    log_success "Extracted to ${work_dir}/quickstart-framework-${version}"

    # Return the extracted directory path
    echo "${work_dir}/quickstart-framework-${version}"
}

# Run installation
run_install() {
    local release_dir="$1"
    local target_dir="$2"

    log_step "Running framework installation..."

    local install_script="${release_dir}/scripts/framework_install.sh"

    if [[ ! -f "${install_script}" ]]; then
        log_error "Installation script not found: ${install_script}"
        return 3
    fi

    local install_args=""
    if [[ "${DRY_RUN}" = "1" ]]; then
        install_args="--dry-run"
    fi

    if ! sh "${install_script}" ${install_args} "${release_dir}" "${target_dir}"; then
        log_error "Installation failed"
        return 3
    fi

    log_success "Installation completed"
}

# Run upgrade
run_upgrade() {
    local release_dir="$1"
    local target_dir="$2"

    log_step "Running framework upgrade..."

    local upgrade_script="${release_dir}/scripts/framework_upgrade.sh"

    if [[ ! -f "${upgrade_script}" ]]; then
        log_error "Upgrade script not found: ${upgrade_script}"
        return 3
    fi

    local upgrade_args=""
    if [[ "${DRY_RUN}" = "1" ]]; then
        upgrade_args="--dry-run"
    fi

    if ! sh "${upgrade_script}" ${upgrade_args} "${release_dir}" "${target_dir}"; then
        log_error "Upgrade failed"
        return 3
    fi

    log_success "Upgrade completed"
}

# Show Guardian reminder
show_guardian_reminder() {
    if [[ "${SKIP_GUARDIAN}" = "1" ]]; then
        return
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "${CYAN}Framework Guardian Verification Recommended${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "The Framework Guardian agent can verify your installation and help"
    echo "resolve any conflicts or issues. It is recommended to run:"
    echo ""
    echo "  ${GREEN}1. Audit Mode${NC} - Verify framework integrity against manifest"
    echo "     Check for missing, outdated, or misplaced framework files."
    echo ""
    echo "  ${GREEN}2. Upgrade Mode${NC} - Resolve any .framework-new conflicts"
    echo "     Get recommendations for merging changes safely."
    echo ""
    echo "To use Framework Guardian:"
    echo "  - Invoke the framework-guardian agent in your AI assistant"
    echo "  - Or check: .github/agents/framework-guardian.agent.md"
    echo ""
    echo "Documentation:"
    echo "  - docs/HOW_TO_USE/framework_install.md"
    echo "  - docs/architecture/adrs/ADR-014-framework-guardian-agent.md"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Main function
main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --help|-h)
                print_usage
                exit 0
                ;;
            --version)
                shift
                if [[ $# -eq 0 ]]; then
                    log_error "--version requires an argument"
                    exit 1
                fi
                VERSION="$1"
                shift
                ;;
            --upgrade)
                MODE="upgrade"
                shift
                ;;
            --target)
                shift
                if [[ $# -eq 0 ]]; then
                    log_error "--target requires an argument"
                    exit 1
                fi
                TARGET_DIR="$1"
                shift
                ;;
            --dry-run)
                DRY_RUN=1
                shift
                ;;
            --skip-guardian)
                SKIP_GUARDIAN=1
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done

    # Banner
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "SDD Agent Framework Deployment"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Source:  ${UPSTREAM_URL}"
    echo "  Target:  ${TARGET_DIR}"
    echo "  Mode:    ${MODE}"
    if [[ "${DRY_RUN}" = "1" ]]; then
        echo "  Dry Run: YES"
    fi
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Check requirements
    check_requirements

    # Resolve version
    if [[ "${VERSION}" = "latest" ]]; then
        log_step "Resolving latest version..."
        VERSION=$(get_latest_version) || exit 2
        log_success "Latest version: ${VERSION}"
    fi

    # Validate target directory
    if [[ ! -d "${TARGET_DIR}" ]]; then
        log_error "Target directory does not exist: ${TARGET_DIR}"
        exit 1
    fi

    TARGET_DIR=$(cd "${TARGET_DIR}" && pwd)

    # Check for existing installation if not upgrading
    if [[ "${MODE}" = "install" ]] && [[ -f "${TARGET_DIR}/.framework_meta.yml" ]]; then
        log_warning "Framework already installed in ${TARGET_DIR}"
        log_warning "Use --upgrade to upgrade existing installation"
        log_info "Current version: $(grep 'framework_version:' "${TARGET_DIR}/.framework_meta.yml" | sed 's/.*: *//')"
        exit 1
    fi

    # Check for missing installation if upgrading
    if [[ "${MODE}" = "upgrade" ]] && [[ ! -f "${TARGET_DIR}/.framework_meta.yml" ]]; then
        log_warning "No existing framework installation found in ${TARGET_DIR}"
        log_warning "Use without --upgrade for fresh installation"
        exit 1
    fi

    # Create temp working directory
    WORK_DIR=$(mktemp -d)
    trap 'rm -rf "${WORK_DIR}"' EXIT

    # Download and extract
    RELEASE_DIR=$(download_release "${VERSION}" "${WORK_DIR}") || exit $?

    if [[ "${DRY_RUN}" = "1" ]]; then
        log_info "[DRY RUN] Would extract to: ${WORK_DIR}/quickstart-framework-${VERSION}"
        RELEASE_DIR="${WORK_DIR}/quickstart-framework-${VERSION}"
    fi

    # Run install or upgrade
    if [[ "${MODE}" = "install" ]]; then
        run_install "${RELEASE_DIR}" "${TARGET_DIR}" || exit $?
    else
        run_upgrade "${RELEASE_DIR}" "${TARGET_DIR}" || exit $?
    fi

    # Show Guardian reminder
    show_guardian_reminder

    echo ""
    log_success "Framework deployment completed successfully!"
    echo ""
}

main "$@"
