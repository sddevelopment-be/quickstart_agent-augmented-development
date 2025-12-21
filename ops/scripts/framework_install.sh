#!/bin/sh
# framework_install.sh - Install agent framework into a target repository
#
# Purpose: Copy framework core files into a downstream project for first-time setup
# Compliant: POSIX sh (works with dash, bash, sh, ash)
# Author: DevOps Danny (Build Automation Specialist)
# Related: ADR-013 (Zip-Based Framework Distribution)
#
# Exit Codes:
#   0 - Success
#   1 - Framework already installed (detected .framework_meta.yml)
#   2 - Missing required parameter (PROJECT_ROOT)
#   3 - framework_core/ directory not found
#   4 - META/MANIFEST.yml not found
#   5 - Failed to create directories
#   6 - Failed to copy files
#   7 - Failed to create metadata file
#
# Usage:
#   framework_install.sh [--dry-run] PROJECT_ROOT
#
# Arguments:
#   --dry-run       Report actions without executing (optional)
#   PROJECT_ROOT    Target directory for framework installation (required)
#
# Environment:
#   FRAMEWORK_SOURCE  Override framework_core location (default: ./framework_core)
#   MANIFEST_PATH     Override manifest location (default: ./META/MANIFEST.yml)
#
# Output Format (parsable by Framework Guardian):
#   DRY RUN MODE (if applicable)
#   NEW: N files
#   SKIPPED: N files
#   Installation complete: VERSION at TIMESTAMP
#

set -e  # Exit on error

# Configuration defaults
DRY_RUN=0
NEW_COUNT=0
SKIPPED_COUNT=0
PROJECT_ROOT=""

# Parse command line arguments
parse_args() {
    while [ $# -gt 0 ]; do
        case "$1" in
            --dry-run)
                DRY_RUN=1
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            -*)
                echo "ERROR: Unknown option: $1" >&2
                show_usage
                exit 2
                ;;
            *)
                if [ -z "${PROJECT_ROOT:-}" ]; then
                    PROJECT_ROOT="$1"
                else
                    echo "ERROR: Multiple PROJECT_ROOT values provided" >&2
                    show_usage
                    exit 2
                fi
                shift
                ;;
        esac
    done
    
    # Validate required parameter
    if [ -z "${PROJECT_ROOT:-}" ]; then
        echo "ERROR: PROJECT_ROOT parameter is required" >&2
        show_usage
        exit 2
    fi
}

show_usage() {
    cat <<'EOF'
Usage: framework_install.sh [--dry-run] PROJECT_ROOT

Install agent framework into a target repository.

Arguments:
  PROJECT_ROOT    Target directory for framework installation

Options:
  --dry-run       Report actions without executing
  -h, --help      Show this help message

Exit Codes:
  0 - Success
  1 - Framework already installed
  2 - Invalid parameters
  3 - framework_core/ not found
  4 - META/MANIFEST.yml not found
  5 - Failed to create directories
  6 - Failed to copy files
  7 - Failed to create metadata file

Example:
  framework_install.sh /path/to/my-project
  framework_install.sh --dry-run /path/to/my-project
EOF
}

# Check if framework is already installed
check_existing_installation() {
    if [ -f "$PROJECT_ROOT/.framework_meta.yml" ]; then
        echo "ERROR: Framework already installed in $PROJECT_ROOT" >&2
        echo "Found existing .framework_meta.yml file" >&2
        echo "Use framework_upgrade.sh to update an existing installation" >&2
        exit 1
    fi
}

# Validate environment
validate_environment() {
    # Determine framework source location
    if [ -n "${FRAMEWORK_SOURCE:-}" ]; then
        FRAMEWORK_CORE="$FRAMEWORK_SOURCE"
    else
        # Default: framework_core in current directory
        FRAMEWORK_CORE="./framework_core"
    fi
    
    # Check framework_core exists
    if [ ! -d "$FRAMEWORK_CORE" ]; then
        echo "ERROR: framework_core directory not found at: $FRAMEWORK_CORE" >&2
        echo "Please run this script from the framework distribution directory" >&2
        exit 3
    fi
    
    # Determine manifest location
    if [ -n "${MANIFEST_PATH:-}" ]; then
        MANIFEST_FILE="$MANIFEST_PATH"
    else
        MANIFEST_FILE="./META/MANIFEST.yml"
    fi
    
    # Check manifest exists
    if [ ! -f "$MANIFEST_FILE" ]; then
        echo "ERROR: META/MANIFEST.yml not found at: $MANIFEST_FILE" >&2
        echo "Please ensure framework distribution is complete" >&2
        exit 4
    fi
    
    # Extract framework version from manifest
    # Simple grep-based extraction (POSIX-compliant)
    FRAMEWORK_VERSION=$(grep '^  version:' "$MANIFEST_FILE" | sed 's/.*version: *"\(.*\)".*/\1/' | head -n 1)
    if [ -z "$FRAMEWORK_VERSION" ]; then
        FRAMEWORK_VERSION="unknown"
    fi
}

# Create target directory if needed
ensure_project_root() {
    if [ ! -d "$PROJECT_ROOT" ]; then
        if [ $DRY_RUN -eq 1 ]; then
            echo "[DRY RUN] Would create directory: $PROJECT_ROOT"
        else
            mkdir -p "$PROJECT_ROOT" || {
                echo "ERROR: Failed to create PROJECT_ROOT: $PROJECT_ROOT" >&2
                exit 5
            }
        fi
    fi
}

# Copy framework files to project (only new files)
install_framework_files() {
    echo "Scanning framework_core for files to install..."
    
    # Save current directory
    original_dir=$(pwd)
    
    # Change to framework_core directory
    cd "$FRAMEWORK_CORE" || exit 6
    
    # Create a temporary file to store file list
    tmpfile="${TMPDIR:-/tmp}/framework_install_$$"
    find . -type f -print > "$tmpfile"
    
    # Process each file
    while IFS= read -r source_file; do
        # Remove leading ./
        relative_path="${source_file#./}"
        target_file="$PROJECT_ROOT/$relative_path"
        target_dir=$(dirname "$target_file")
        
        # Check if file already exists in target
        if [ -f "$target_file" ]; then
            SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
            echo "SKIP: $relative_path (already exists)"
            continue
        fi
        
        # File is new - copy it
        if [ $DRY_RUN -eq 1 ]; then
            echo "[DRY RUN] Would copy: $relative_path"
            NEW_COUNT=$((NEW_COUNT + 1))
        else
            # Create target directory if needed
            if [ ! -d "$target_dir" ]; then
                mkdir -p "$target_dir" || {
                    echo "ERROR: Failed to create directory: $target_dir" >&2
                    rm -f "$tmpfile"
                    exit 5
                }
            fi
            
            # Copy file preserving permissions
            cp -p "$source_file" "$target_file" || {
                echo "ERROR: Failed to copy file: $relative_path" >&2
                rm -f "$tmpfile"
                exit 6
            }
            
            NEW_COUNT=$((NEW_COUNT + 1))
            echo "NEW: $relative_path"
        fi
    done < "$tmpfile"
    
    # Clean up
    rm -f "$tmpfile"
    cd "$original_dir" || exit 6
}

# Create .framework_meta.yml with installation metadata
create_metadata_file() {
    if [ $DRY_RUN -eq 1 ]; then
        echo "[DRY RUN] Would create .framework_meta.yml"
        return 0
    fi
    
    # Generate ISO 8601 timestamp
    INSTALLED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%S+00:00")
    
    # Determine source release name (from current directory or environment)
    if [ -n "${SOURCE_RELEASE:-}" ]; then
        SOURCE_NAME="$SOURCE_RELEASE"
    else
        # Try to infer from current directory name
        CURRENT_DIR=$(basename "$(pwd)")
        if [ -n "$CURRENT_DIR" ]; then
            SOURCE_NAME="$CURRENT_DIR"
        else
            SOURCE_NAME="unknown"
        fi
    fi
    
    # Write metadata file
    cat > "$PROJECT_ROOT/.framework_meta.yml" <<EOF
# Framework Installation Metadata
# Generated by framework_install.sh
# DO NOT EDIT MANUALLY - managed by framework tools

framework_version: "$FRAMEWORK_VERSION"
installed_at: "$INSTALLED_AT"
source_release: "$SOURCE_NAME"

# Installation summary
files_installed: $NEW_COUNT
files_skipped: $SKIPPED_COUNT
EOF
    
    if ! test -f "$PROJECT_ROOT/.framework_meta.yml"; then
        echo "ERROR: Failed to create .framework_meta.yml" >&2
        exit 7
    fi
    
    echo "Created: .framework_meta.yml"
}

# Print installation summary
print_summary() {
    echo ""
    echo "=== Installation Summary ==="
    
    if [ $DRY_RUN -eq 1 ]; then
        echo "MODE: DRY RUN (no changes made)"
    fi
    
    echo "NEW: $NEW_COUNT files"
    echo "SKIPPED: $SKIPPED_COUNT files"
    echo "Framework version: $FRAMEWORK_VERSION"
    echo "Target: $PROJECT_ROOT"
    
    if [ $DRY_RUN -eq 0 ]; then
        echo "Installation complete at $(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u)"
    fi
}

# Main execution
main() {
    if [ $DRY_RUN -eq 1 ]; then
        echo "=== DRY RUN MODE ==="
        echo "Actions will be reported but not executed"
        echo ""
    fi
    
    echo "Framework Installation Script"
    echo "Version: 1.0.0"
    echo ""
    
    parse_args "$@"
    
    # Convert PROJECT_ROOT to absolute path before any cd operations
    case "$PROJECT_ROOT" in
        /*)
            # Already absolute
            ;;
        *)
            # Make it absolute
            PROJECT_ROOT="$(pwd)/$PROJECT_ROOT"
            ;;
    esac
    
    check_existing_installation
    validate_environment
    ensure_project_root
    install_framework_files
    create_metadata_file
    print_summary
    
    exit 0
}

# Execute main with all arguments
main "$@"
