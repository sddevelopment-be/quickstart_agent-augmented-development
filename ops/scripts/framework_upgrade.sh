#!/bin/sh
# framework_upgrade.sh - Upgrade agent framework in an existing installation
#
# Purpose: Safely upgrade framework files without destroying local customizations
# Compliant: POSIX sh (works with dash, bash, sh, ash)
# Author: DevOps Danny (Build Automation Specialist)
# Related: ADR-013 (Zip-Based Framework Distribution)
#
# Exit Codes:
#   0 - Success (upgrade completed or dry-run completed)
#   1 - Framework not installed (no .framework_meta.yml found)
#   2 - Missing required parameter (PROJECT_ROOT)
#   3 - framework_core/ directory not found
#   4 - META/MANIFEST.yml not found
#   5 - Failed to create directories
#   6 - Failed to copy files
#   7 - Failed to create/update metadata or report
#
# Usage:
#   framework_upgrade.sh [--dry-run] PROJECT_ROOT
#
# Arguments:
#   --dry-run       Report actions without executing (optional)
#   PROJECT_ROOT    Target directory with existing framework installation (required)
#
# Environment:
#   FRAMEWORK_SOURCE  Override framework_core location (default: ./framework_core)
#   MANIFEST_PATH     Override manifest location (default: ./META/MANIFEST.yml)
#
# Behavior:
#   For each file in framework_core/:
#     - Missing in PROJECT_ROOT → copy and mark NEW
#     - Identical (SHA256 match) → skip and mark UNCHANGED
#     - Different → write <file>.framework-new and mark CONFLICT
#   Never touches local/ directory
#   Generates upgrade-report.txt with summary
#   Updates .framework_meta.yml (unless --dry-run)
#
# Output Format (parsable by Framework Guardian):
#   DRY RUN MODE (if applicable)
#   NEW: N files
#   UNCHANGED: N files
#   CONFLICT: N files
#   Upgrade complete: VERSION at TIMESTAMP
#

set -e  # Exit on error

# Configuration defaults
DRY_RUN=0
NEW_COUNT=0
UNCHANGED_COUNT=0
CONFLICT_COUNT=0
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
Usage: framework_upgrade.sh [--dry-run] PROJECT_ROOT

Upgrade agent framework in an existing installation.

Arguments:
  PROJECT_ROOT    Target directory with existing framework installation

Options:
  --dry-run       Report actions without executing
  -h, --help      Show this help message

Exit Codes:
  0 - Success
  1 - Framework not installed
  2 - Invalid parameters
  3 - framework_core/ not found
  4 - META/MANIFEST.yml not found
  5 - Failed to create directories
  6 - Failed to copy files
  7 - Failed to create/update metadata or report

File Status:
  NEW        - File added from new framework version
  UNCHANGED  - File identical in both versions (checksum match)
  CONFLICT   - File differs; creates .framework-new for review

Example:
  framework_upgrade.sh /path/to/my-project
  framework_upgrade.sh --dry-run /path/to/my-project
EOF
}

# Check if framework is installed
check_existing_installation() {
    if [ ! -f "$PROJECT_ROOT/.framework_meta.yml" ]; then
        echo "ERROR: Framework not installed in $PROJECT_ROOT" >&2
        echo "No .framework_meta.yml file found" >&2
        echo "Use framework_install.sh for first-time installation" >&2
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
    FRAMEWORK_VERSION=$(grep '^  version:' "$MANIFEST_FILE" | sed 's/.*version: *"\(.*\)".*/\1/' | head -n 1)
    if [ -z "$FRAMEWORK_VERSION" ]; then
        FRAMEWORK_VERSION="unknown"
    fi
    
    # Read current version from metadata
    if [ -f "$PROJECT_ROOT/.framework_meta.yml" ]; then
        CURRENT_VERSION=$(grep '^framework_version:' "$PROJECT_ROOT/.framework_meta.yml" | sed 's/.*framework_version: *"\(.*\)".*/\1/' | head -n 1)
        if [ -z "$CURRENT_VERSION" ]; then
            CURRENT_VERSION="unknown"
        fi
    else
        CURRENT_VERSION="unknown"
    fi
}

# Compute SHA256 checksum for a file
compute_checksum() {
    filepath="$1"
    
    if ! test -f "$filepath"; then
        echo ""
        return 1
    fi
    
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$filepath" | cut -d' ' -f1
    elif command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$filepath" | cut -d' ' -f1
    else
        echo "ERROR: No SHA256 checksum tool available (sha256sum or shasum)" >&2
        exit 6
    fi
}

# Upgrade framework files
upgrade_framework_files() {
    echo "Scanning framework_core for files to upgrade..."
    
    # Save current directory
    original_dir=$(pwd)
    
    # Initialize report file
    REPORT_FILE="$PROJECT_ROOT/upgrade-report.txt"
    if [ $DRY_RUN -eq 0 ]; then
        : > "$REPORT_FILE"  # Truncate file
    fi
    
    # Change to framework_core directory
    cd "$FRAMEWORK_CORE" || exit 6
    
    # Create a temporary file to store file list
    tmpfile="${TMPDIR:-/tmp}/framework_upgrade_$$"
    find . -type f -print > "$tmpfile"
    
    # Process each file
    while IFS= read -r source_file; do
        # Remove leading ./
        relative_path="${source_file#./}"
        
        # Skip files under local/ directory (never upgrade these)
        case "$relative_path" in
            local/*)
                continue
                ;;
        esac
        
        # Use current-directory-relative path for source (we're in framework_core)
        source_rel="$relative_path"
        target_file="$PROJECT_ROOT/$relative_path"
        target_dir=$(dirname "$target_file")
        
        # Determine file status
        if [ ! -f "$target_file" ]; then
            # File is NEW - doesn't exist in target
            if [ $DRY_RUN -eq 1 ]; then
                echo "[DRY RUN] Would copy: $relative_path (NEW)"
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
                
                # Copy new file (we're in framework_core, use relative path)
                cp -p "$source_rel" "$target_file" || {
                    echo "ERROR: Failed to copy file: $relative_path" >&2
                    rm -f "$tmpfile"
                    exit 6
                }
                
                NEW_COUNT=$((NEW_COUNT + 1))
                echo "NEW: $relative_path"
                echo "NEW: $relative_path" >> "$REPORT_FILE"
            fi
        else
            # File exists - compare checksums
            source_checksum=$(compute_checksum "$source_rel")
            target_checksum=$(compute_checksum "$target_file")
            
            if [ "$source_checksum" = "$target_checksum" ]; then
                # Files are UNCHANGED (identical)
                UNCHANGED_COUNT=$((UNCHANGED_COUNT + 1))
                if [ $DRY_RUN -eq 0 ]; then
                    echo "UNCHANGED: $relative_path" >> "$REPORT_FILE"
                fi
            else
                # Files are different - CONFLICT
                if [ $DRY_RUN -eq 1 ]; then
                    echo "[DRY RUN] Would create: ${relative_path}.framework-new (CONFLICT)"
                    CONFLICT_COUNT=$((CONFLICT_COUNT + 1))
                else
                    # Write new version to .framework-new file
                    framework_new_file="${target_file}.framework-new"
                    cp -p "$source_rel" "$framework_new_file" || {
                        echo "ERROR: Failed to create .framework-new file: $relative_path" >&2
                        rm -f "$tmpfile"
                        exit 6
                    }
                    
                    CONFLICT_COUNT=$((CONFLICT_COUNT + 1))
                    echo "CONFLICT: $relative_path (see ${relative_path}.framework-new)"
                    echo "CONFLICT: $relative_path" >> "$REPORT_FILE"
                fi
            fi
        fi
    done < "$tmpfile"
    
    # Clean up
    rm -f "$tmpfile"
    cd "$original_dir" || exit 6
}

# Write upgrade report summary
write_upgrade_report() {
    if [ $DRY_RUN -eq 1 ]; then
        return 0
    fi
    
    REPORT_FILE="$PROJECT_ROOT/upgrade-report.txt"
    
    # Prepend summary to existing report
    tmpfile="${TMPDIR:-/tmp}/upgrade_report_summary_$$"
    cat > "$tmpfile" <<EOF
=== Framework Upgrade Report ===
Date: $(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u)
From version: $CURRENT_VERSION
To version: $FRAMEWORK_VERSION

=== Summary ===
NEW: $NEW_COUNT files
UNCHANGED: $UNCHANGED_COUNT files
CONFLICT: $CONFLICT_COUNT files

=== File Details ===
EOF
    
    # Append existing details if report exists
    if [ -f "$REPORT_FILE" ]; then
        cat "$REPORT_FILE" >> "$tmpfile"
    fi
    
    # Replace report with new version
    mv "$tmpfile" "$REPORT_FILE" || {
        echo "ERROR: Failed to write upgrade report" >&2
        rm -f "$tmpfile"
        exit 7
    }
    
    echo "Created: upgrade-report.txt"
}

# Update .framework_meta.yml with new version
update_metadata_file() {
    if [ $DRY_RUN -eq 1 ]; then
        echo "[DRY RUN] Would update .framework_meta.yml"
        return 0
    fi
    
    # Generate ISO 8601 timestamp
    UPGRADED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%S+00:00")
    
    # Determine source release name
    if [ -n "${SOURCE_RELEASE:-}" ]; then
        SOURCE_NAME="$SOURCE_RELEASE"
    else
        CURRENT_DIR=$(basename "$(pwd)")
        if [ -n "$CURRENT_DIR" ]; then
            SOURCE_NAME="$CURRENT_DIR"
        else
            SOURCE_NAME="unknown"
        fi
    fi
    
    # Write updated metadata file
    cat > "$PROJECT_ROOT/.framework_meta.yml" <<EOF
# Framework Installation Metadata
# Generated by framework_upgrade.sh
# DO NOT EDIT MANUALLY - managed by framework tools

framework_version: "$FRAMEWORK_VERSION"
installed_at: "$UPGRADED_AT"
source_release: "$SOURCE_NAME"

# Previous version
previous_version: "$CURRENT_VERSION"

# Upgrade summary
files_new: $NEW_COUNT
files_unchanged: $UNCHANGED_COUNT
files_conflict: $CONFLICT_COUNT
EOF
    
    if ! test -f "$PROJECT_ROOT/.framework_meta.yml"; then
        echo "ERROR: Failed to update .framework_meta.yml" >&2
        exit 7
    fi
    
    echo "Updated: .framework_meta.yml"
}

# Print upgrade summary
print_summary() {
    echo ""
    echo "=== Upgrade Summary ==="
    
    if [ $DRY_RUN -eq 1 ]; then
        echo "MODE: DRY RUN (no changes made)"
    fi
    
    echo "NEW: $NEW_COUNT files"
    echo "UNCHANGED: $UNCHANGED_COUNT files"
    echo "CONFLICT: $CONFLICT_COUNT files"
    
    if [ $CONFLICT_COUNT -gt 0 ]; then
        echo ""
        echo "⚠️  CONFLICTS DETECTED"
        echo "Review .framework-new files and resolve conflicts manually."
        echo "See upgrade-report.txt for details."
    fi
    
    echo ""
    echo "From version: $CURRENT_VERSION"
    echo "To version:   $FRAMEWORK_VERSION"
    echo "Target:       $PROJECT_ROOT"
    
    if [ $DRY_RUN -eq 0 ]; then
        echo "Upgrade complete at $(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u)"
    fi
}

# Main execution
main() {
    if [ $DRY_RUN -eq 1 ]; then
        echo "=== DRY RUN MODE ==="
        echo "Actions will be reported but not executed"
        echo ""
    fi
    
    echo "Framework Upgrade Script"
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
    upgrade_framework_files
    write_upgrade_report
    update_metadata_file
    print_summary
    
    exit 0
}

# Execute main with all arguments
main "$@"
