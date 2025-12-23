#!/usr/bin/env bash
# generate_manifest.sh
# Generates MANIFEST.yml by scanning repository structure
# Used by: Framework Guardian, install/upgrade scripts
# Follows: ADR-013 (Zip-Based Distribution), ADR-014 (Framework Guardian)

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================

# Default values
VERSION=""
DRY_RUN=false
OUTPUT_PATH="META/MANIFEST.yml"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Framework name
FRAMEWORK_NAME="quickstart-agent-augmented-development"

# Core paths to include (directory-level entries)
# Format: path:mode:description
CORE_PATHS=(
    ".github/agents:sync-always:Core agent profiles, directives, and guidelines"
    "docs/templates:sync-always:Canonical templates for agent tasks, architecture, checklists"
    "validation:sync-always:Validation schemas, test framework, and audit protocols"
    "work/README.md:copy-once:File-based asynchronous orchestration guide"
    "AGENTS.md:sync-always:Agent Specification Document (localized framework entry point)"
    "REPO_MAP.md:copy-once:Repository structure overview"
)

# Specific files to include with explicit metadata
# Format: path:mode:description
SPECIFIC_FILES=(
    ".github/agents/framework-guardian.agent.md:sync-always:Framework Guardian Agent definition"
    ".github/agents/GLOSSARY.md:sync-always:Standardized terminology reference"
    ".github/agents/aliases.md:sync-always:Command aliases and shorthand reference"
    "ops/scripts/framework_install.sh:sync-always:Framework installation script"
    "ops/scripts/framework_upgrade.sh:sync-always:Framework upgrade script"
)

# Paths to exclude from scanning
EXCLUDE_PATTERNS=(
    "work/collaboration"
    "work/planning"
    "work/notes"
    "work/articles"
    "work/prompts"
    "work/reports"
    "tmp/"
    "local/"
    ".git"
    "__pycache__"
    "*.pyc"
    ".pytest_cache"
    ".coverage"
    "*.egg-info"
)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

log_info() {
    echo "[INFO] $*" >&2
}

log_error() {
    echo "[ERROR] $*" >&2
}

show_usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Generate MANIFEST.yml by scanning framework repository structure.

OPTIONS:
    --version VERSION    Set framework version (default: auto-detect from pyproject.toml)
    --output PATH        Output file path (default: META/MANIFEST.yml)
    --dry-run            Output to stdout instead of file
    -h, --help           Show this help message

EXAMPLES:
    # Generate manifest with auto-detected version
    $(basename "$0")
    
    # Generate manifest with specific version
    $(basename "$0") --version 1.2.0
    
    # Preview output without writing file
    $(basename "$0") --dry-run
    
    # Generate to custom location
    $(basename "$0") --output /tmp/manifest.yml --version 1.0.0

EOF
}

# Calculate SHA256 checksum (cross-platform)
calculate_checksum() {
    local file="$1"
    
    if [ ! -f "${file}" ]; then
        log_error "File not found: ${file}"
        return 1
    fi
    
    # Try sha256sum first (Linux), then shasum (macOS)
    if command -v sha256sum &> /dev/null; then
        sha256sum "${file}" | awk '{print $1}'
    elif command -v shasum &> /dev/null; then
        shasum -a 256 "${file}" | awk '{print $1}'
    else
        log_error "No SHA256 tool available (sha256sum or shasum)"
        return 1
    fi
}

# Auto-detect version from pyproject.toml
detect_version() {
    local pyproject="${REPO_ROOT}/pyproject.toml"
    
    if [ -f "${pyproject}" ]; then
        grep -E "^version" "${pyproject}" | head -1 | sed 's/version = //g' | tr -d '"' | tr -d ' '
    else
        echo "0.0.0"
    fi
}

# Get current date in ISO format
get_release_date() {
    date +%Y-%m-%d
}

# Check if path should be excluded
is_excluded() {
    local path="$1"
    
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        if [[ "${path}" == *"${pattern}"* ]]; then
            return 0
        fi
    done
    
    return 1
}

# Escape YAML special characters
yaml_escape() {
    local str="$1"
    # Add quotes if string contains special YAML characters
    if [[ "${str}" =~ [:\{\}\[\],\&\*\#\?\|\-\<\>\=\!\%\@\`] ]]; then
        echo "\"${str}\""
    else
        echo "${str}"
    fi
}

# ============================================================================
# MANIFEST GENERATION FUNCTIONS
# ============================================================================

generate_header() {
    cat <<EOF
# META/MANIFEST.yml
# Describes the framework core contents for this release.
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
# Used by:
# - framework_install.sh / framework_upgrade.sh
# - Framework Guardian Agent
# - Any tools that need to know "what belongs to the framework"

framework:
  name: ${FRAMEWORK_NAME}
  version: "${VERSION}"
  release_date: "$(get_release_date)"
  description: "Core files for the agent-augmented development framework."

compatibility:
  min_python_version: "3.10"
  notes:
    - "Projects older than 1.0.0 may require manual migration."

# Define how files/directories are treated.
# mode:
#   - sync-always: should track framework updates closely
#   - copy-once: initial scaffold; safe to diverge locally
#   - reference-only: for docs that describe framework but not enforced
#   - ignore: present in bundle but not managed (rare)

EOF
}

generate_paths_section() {
    echo "paths:"
    
    for entry in "${CORE_PATHS[@]}"; do
        IFS=':' read -r path mode description <<< "${entry}"
        
        # Skip if path doesn't exist
        local full_path="${REPO_ROOT}/${path}"
        if [ ! -e "${full_path}" ]; then
            log_info "Skipping non-existent path: ${path}"
            continue
        fi
        
        cat <<EOF
  - path: "${path}"
    mode: ${mode}
    description: $(yaml_escape "${description}")

EOF
    done
}

generate_files_section() {
    echo "files:"
    
    # Process specific files with metadata
    for entry in "${SPECIFIC_FILES[@]}"; do
        IFS=':' read -r path mode description <<< "${entry}"
        
        local full_path="${REPO_ROOT}/${path}"
        if [ ! -f "${full_path}" ]; then
            log_info "Skipping non-existent file: ${path}"
            continue
        fi
        
        local checksum=$(calculate_checksum "${full_path}")
        
        cat <<EOF
  - path: "${path}"
    checksum: "sha256:${checksum}"
    mode: ${mode}
    description: $(yaml_escape "${description}")

EOF
    done
    
    # Scan and include individual files from core directories
    scan_directory_files ".github/agents" "sync-always"
    scan_directory_files "docs/templates" "sync-always"
    scan_directory_files "validation" "sync-always"
}

scan_directory_files() {
    local dir="$1"
    local mode="$2"
    local base_dir="${REPO_ROOT}/${dir}"
    
    if [ ! -d "${base_dir}" ]; then
        return
    fi
    
    # Find all files in directory, excluding common patterns
    while IFS= read -r -d '' file; do
        local rel_path="${file#${REPO_ROOT}/}"
        
        # Skip if excluded
        if is_excluded "${rel_path}"; then
            continue
        fi
        
        # Skip if already in specific files list
        local skip=false
        for entry in "${SPECIFIC_FILES[@]}"; do
            local specific_path="${entry%%:*}"
            if [ "${rel_path}" = "${specific_path}" ]; then
                skip=true
                break
            fi
        done
        
        if [ "${skip}" = true ]; then
            continue
        fi
        
        # Calculate checksum and add to manifest
        local checksum=$(calculate_checksum "${file}")
        local description="Framework core file"
        
        # Determine description based on file type
        case "${rel_path}" in
            *.md)
                description="Framework documentation"
                ;;
            *.py)
                description="Framework Python module"
                ;;
            *.sh)
                description="Framework shell script"
                ;;
            *.yml|*.yaml)
                description="Framework configuration"
                ;;
        esac
        
        cat <<EOF
  - path: "${rel_path}"
    checksum: "sha256:${checksum}"
    mode: ${mode}
    description: $(yaml_escape "${description}")

EOF
    done < <(find "${base_dir}" -type f \( ! -name "*.pyc" ! -name ".DS_Store" \) -print0 | sort -z)
}

generate_tooling_section() {
    cat <<EOF
tooling:
  - script: "ops/scripts/framework_install.sh"
    purpose: "First-time installation of framework into a project"
    mode: sync-always

  - script: "ops/scripts/framework_upgrade.sh"
    purpose: "Upgrade existing framework installation to new version"
    mode: sync-always

  - script: "ops/scripts/generate_manifest.sh"
    purpose: "Generate or update MANIFEST.yml from repository structure"
    mode: sync-always
EOF
}

generate_manifest() {
    {
        generate_header
        generate_paths_section
        generate_files_section
        generate_tooling_section
    }
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    # Parse command line arguments
    while [ $# -gt 0 ]; do
        case "$1" in
            --version)
                VERSION="$2"
                shift 2
                ;;
            --output)
                OUTPUT_PATH="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Auto-detect version if not provided
    if [ -z "${VERSION}" ]; then
        VERSION=$(detect_version)
        log_info "Auto-detected version: ${VERSION}"
    fi
    
    # Generate manifest
    log_info "Generating manifest for ${FRAMEWORK_NAME} v${VERSION}..."
    
    if [ "${DRY_RUN}" = true ]; then
        log_info "Dry run mode: outputting to stdout"
        generate_manifest
    else
        # Ensure output directory exists
        local output_dir=$(dirname "${OUTPUT_PATH}")
        if [ ! -d "${output_dir}" ]; then
            mkdir -p "${output_dir}"
            log_info "Created output directory: ${output_dir}"
        fi
        
        # Generate manifest to file
        generate_manifest > "${OUTPUT_PATH}"
        log_info "Manifest generated successfully: ${OUTPUT_PATH}"
        
        # Validate YAML syntax (if tools available)
        if command -v python3 &> /dev/null; then
            if python3 -c "import yaml; yaml.safe_load(open('${OUTPUT_PATH}'))" 2>/dev/null; then
                log_info "✅ YAML validation passed"
            else
                log_error "⚠️  YAML validation failed"
                return 1
            fi
        fi
    fi
    
    return 0
}

# Run main function
main "$@"
