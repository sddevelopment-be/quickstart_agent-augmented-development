#!/bin/sh
# assemble_framework_package.sh - Package framework core into distributable zip
#
# Purpose: Create quickstart-framework-<version>.zip for distribution per ADR-013
# Compliant: POSIX sh (works with dash, bash, sh, ash)
# Author: DevOps Danny (Build Automation Specialist)
# Related: ADR-013 (Zip-Based Framework Distribution)
#
# Exit Codes:
#   0 - Success
#   1 - Missing required parameter (VERSION)
#   2 - MANIFEST.yml not found or invalid
#   3 - Required source files/directories not found
#   4 - Failed to create build directory
#   5 - Failed to copy files
#   6 - Failed to create zip archive
#
# Usage:
#   assemble_framework_package.sh [OPTIONS] VERSION
#
# Arguments:
#   VERSION         Framework version (e.g., 1.0.0)
#
# Options:
#   --output-dir DIR   Build directory (default: ./build)
#   --dry-run          Report actions without executing
#   --help             Display this help message
#
# Environment:
#   REPO_ROOT          Override repository root (default: auto-detect)
#
# Output:
#   build/quickstart-framework-<version>.zip
#   build/SHA256SUMS
#

set -e  # Exit on error

# Configuration defaults
DRY_RUN=0
OUTPUT_DIR="./build"
VERSION=""
REPO_ROOT=""

# Color codes for output (only if terminal supports it)
if [ -t 1 ]; then
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

# Logging functions
log_info() {
    printf "${BLUE}[INFO]${NC} %s\n" "$1"
}

log_success() {
    printf "${GREEN}[SUCCESS]${NC} %s\n" "$1"
}

log_warn() {
    printf "${YELLOW}[WARN]${NC} %s\n" "$1"
}

log_error() {
    printf "${RED}[ERROR]${NC} %s\n" "$1" >&2
}

# Display help message
show_help() {
    sed -n '2,30p' "$0" | sed 's/^# \?//'
    exit 0
}

# Parse command line arguments
parse_args() {
    while [ $# -gt 0 ]; do
        case "$1" in
            --dry-run)
                DRY_RUN=1
                shift
                ;;
            --output-dir)
                if [ -z "$2" ] || [ "${2#-}" != "$2" ]; then
                    log_error "Option --output-dir requires an argument"
                    exit 1
                fi
                OUTPUT_DIR="$2"
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

    # Fallback to current directory
    REPO_ROOT="$(pwd)"
}

# Validate source files exist
validate_sources() {
    log_info "Validating source files..."

    if [ ! -f "$REPO_ROOT/META/MANIFEST.yml" ]; then
        log_error "META/MANIFEST.yml not found in $REPO_ROOT"
        exit 2
    fi

    # Check critical directories
    for dir in ".github/agents" "docs/templates" "validation" "ops/scripts"; do
        if [ ! -d "$REPO_ROOT/$dir" ]; then
            log_error "Required directory not found: $dir"
            exit 3
        fi
    done

    # Check critical scripts
    for script in "ops/scripts/framework_install.sh" "ops/scripts/framework_upgrade.sh"; do
        if [ ! -f "$REPO_ROOT/$script" ]; then
            log_error "Required script not found: $script"
            exit 3
        fi
    done

    log_success "Source validation complete"
}

# Create clean build directory
prepare_build_dir() {
    log_info "Preparing build directory: $OUTPUT_DIR"

    if [ $DRY_RUN -eq 1 ]; then
        log_info "[DRY-RUN] Would create/clean: $OUTPUT_DIR"
        return
    fi

    # Remove old build if exists
    if [ -d "$OUTPUT_DIR" ]; then
        rm -rf "$OUTPUT_DIR" || {
            log_error "Failed to remove existing build directory"
            exit 4
        }
    fi

    # Create fresh structure
    mkdir -p "$OUTPUT_DIR/framework_core" || {
        log_error "Failed to create build directory"
        exit 4
    }
    mkdir -p "$OUTPUT_DIR/scripts"
    mkdir -p "$OUTPUT_DIR/META"

    log_success "Build directory prepared"
}

# Copy framework core directories
copy_framework_core() {
    log_info "Copying framework_core directories..."

    # Define core paths to include (from ADR-013 and MANIFEST.yml)
    core_paths=".github/agents docs/templates validation work/README.md AGENTS.md REPO_MAP.md"

    for path in $core_paths; do
        src="$REPO_ROOT/$path"
        
        if [ ! -e "$src" ]; then
            log_warn "Skipping missing path: $path"
            continue
        fi

        if [ $DRY_RUN -eq 1 ]; then
            log_info "[DRY-RUN] Would copy: $path -> framework_core/"
            continue
        fi

        # Create parent directory if needed
        parent_dir="$OUTPUT_DIR/framework_core/$(dirname "$path")"
        if [ "$parent_dir" != "$OUTPUT_DIR/framework_core/." ]; then
            mkdir -p "$parent_dir" 2>/dev/null || true
        fi

        # Copy file or directory
        if [ -d "$src" ]; then
            # Exclude local/ directories and hidden files except .github
            if [ "$path" = ".github/agents" ]; then
                # Special handling for .github/agents - exclude local overrides
                cp -r "$src" "$OUTPUT_DIR/framework_core/.github/" || {
                    log_error "Failed to copy $path"
                    exit 5
                }
            else
                cp -r "$src" "$OUTPUT_DIR/framework_core/$path" || {
                    log_error "Failed to copy $path"
                    exit 5
                }
            fi
            log_info "Copied directory: $path"
        elif [ -f "$src" ]; then
            cp "$src" "$OUTPUT_DIR/framework_core/$path" || {
                log_error "Failed to copy $path"
                exit 5
            }
            log_info "Copied file: $path"
        fi
    done

    # Ensure work directory structure exists
    if [ $DRY_RUN -eq 0 ]; then
        mkdir -p "$OUTPUT_DIR/framework_core/work/collaboration/inbox"
        mkdir -p "$OUTPUT_DIR/framework_core/work/collaboration/done"
        mkdir -p "$OUTPUT_DIR/framework_core/work/agents"
        echo "# Work Directory" > "$OUTPUT_DIR/framework_core/work/README.md"
    fi

    log_success "Framework core copied"
}

# Copy installation scripts
copy_scripts() {
    log_info "Copying installation scripts..."

    if [ $DRY_RUN -eq 1 ]; then
        log_info "[DRY-RUN] Would copy scripts to scripts/"
        return
    fi

    cp "$REPO_ROOT/ops/scripts/framework_install.sh" "$OUTPUT_DIR/scripts/" || {
        log_error "Failed to copy framework_install.sh"
        exit 5
    }
    chmod +x "$OUTPUT_DIR/scripts/framework_install.sh"

    cp "$REPO_ROOT/ops/scripts/framework_upgrade.sh" "$OUTPUT_DIR/scripts/" || {
        log_error "Failed to copy framework_upgrade.sh"
        exit 5
    }
    chmod +x "$OUTPUT_DIR/scripts/framework_upgrade.sh"

    log_success "Scripts copied"
}

# Generate/copy META files
generate_meta() {
    log_info "Generating META files..."

    if [ $DRY_RUN -eq 1 ]; then
        log_info "[DRY-RUN] Would generate META files"
        return
    fi

    # Copy MANIFEST.yml
    cp "$REPO_ROOT/META/MANIFEST.yml" "$OUTPUT_DIR/META/" || {
        log_error "Failed to copy MANIFEST.yml"
        exit 5
    }

    # Update version in MANIFEST.yml
    if command -v sed >/dev/null 2>&1; then
        sed -i.bak "s/version: \"[^\"]*\"/version: \"$VERSION\"/" "$OUTPUT_DIR/META/MANIFEST.yml" 2>/dev/null || true
        sed -i.bak "s/release_date: \"[^\"]*\"/release_date: \"$(date +%Y-%m-%d)\"/" "$OUTPUT_DIR/META/MANIFEST.yml" 2>/dev/null || true
        rm -f "$OUTPUT_DIR/META/MANIFEST.yml.bak"
    fi

    # Generate RELEASE_NOTES.md (will be enhanced by generate_release_notes.sh)
    cat > "$OUTPUT_DIR/META/RELEASE_NOTES.md" <<EOF_NOTES
# Release Notes: Version $VERSION

**Release Date:** $(date +%Y-%m-%d)

## Overview

This release of the quickstart-agent-augmented-development framework includes core agent profiles, directives, templates, and automation scripts for agent-augmented development workflows.

## Installation

\`\`\`bash
# Extract the archive
unzip quickstart-framework-$VERSION.zip

# Install into your project
cd quickstart-framework-$VERSION
./scripts/framework_install.sh /path/to/your/project
\`\`\`

## Upgrading

\`\`\`bash
# Extract the archive
unzip quickstart-framework-$VERSION.zip

# Upgrade existing installation
cd quickstart-framework-$VERSION
./scripts/framework_upgrade.sh /path/to/your/project
\`\`\`

## What's Included

- **Framework Core:** Agent profiles, directives, guidelines
- **Templates:** Architecture, documentation, task templates
- **Validation:** Schema validation and testing framework
- **Scripts:** Installation and upgrade automation

## Documentation

See \`framework_core/AGENTS.md\` for the Agent Specification Document.
See \`framework_core/docs/templates/\` for template usage.

## Support

For issues or questions, please refer to the project repository.
EOF_NOTES

    log_success "META files generated"
}

# Validate package structure
validate_package() {
    log_info "Validating package structure..."

    if [ $DRY_RUN -eq 1 ]; then
        log_info "[DRY-RUN] Would validate package structure"
        return
    fi

    # Check required directories exist
    for dir in "framework_core" "scripts" "META"; do
        if [ ! -d "$OUTPUT_DIR/$dir" ]; then
            log_error "Missing required directory in package: $dir"
            exit 3
        fi
    done

    # Check required files exist
    if [ ! -f "$OUTPUT_DIR/META/MANIFEST.yml" ]; then
        log_error "Missing META/MANIFEST.yml in package"
        exit 3
    fi

    if [ ! -f "$OUTPUT_DIR/scripts/framework_install.sh" ]; then
        log_error "Missing framework_install.sh in package"
        exit 3
    fi

    if [ ! -f "$OUTPUT_DIR/scripts/framework_upgrade.sh" ]; then
        log_error "Missing framework_upgrade.sh in package"
        exit 3
    fi

    # Verify no sensitive data patterns (basic check)
    if grep -r "password\|secret\|token\|api.key" "$OUTPUT_DIR" 2>/dev/null | grep -v "META/RELEASE_NOTES.md" >/dev/null; then
        log_warn "Potential sensitive data detected in package - manual review recommended"
    fi

    log_success "Package structure validated"
}

# Create zip archive with deterministic compression
create_archive() {
    log_info "Creating zip archive..."

    if [ $DRY_RUN -eq 1 ]; then
        log_info "[DRY-RUN] Would create: quickstart-framework-$VERSION.zip"
        return
    fi

    archive_name="quickstart-framework-$VERSION.zip"
    
    # Change to build directory for cleaner zip structure
    cd "$OUTPUT_DIR" || exit 6

    # Create deterministic zip (sorted entries, no timestamps for reproducibility)
    # Use -X to exclude extra file attributes, -r for recursive
    if command -v zip >/dev/null 2>&1; then
        find framework_core scripts META -type f | sort | zip -q -X -@ "$archive_name" || {
            log_error "Failed to create zip archive"
            exit 6
        }
    else
        log_error "zip command not found - please install zip utility"
        exit 6
    fi

    log_success "Archive created: $archive_name"

    # Calculate SHA256 checksum
    log_info "Calculating checksum..."
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$archive_name" > SHA256SUMS
        log_success "Checksum: $(cat SHA256SUMS)"
    elif command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$archive_name" > SHA256SUMS
        log_success "Checksum: $(cat SHA256SUMS)"
    else
        log_warn "sha256sum not available - skipping checksum"
    fi
}

# Main execution
main() {
    parse_args "$@"
    
    if [ $DRY_RUN -eq 1 ]; then
        log_warn "DRY RUN MODE - No changes will be made"
    fi

    detect_repo_root
    log_info "Repository root: $REPO_ROOT"
    log_info "Framework version: $VERSION"

    validate_sources
    prepare_build_dir
    copy_framework_core
    copy_scripts
    generate_meta
    validate_package
    create_archive

    log_success "Package assembly complete!"
    if [ $DRY_RUN -eq 0 ]; then
        log_info "Output: $OUTPUT_DIR/quickstart-framework-$VERSION.zip"
    fi
}

# Run main function
main "$@"
