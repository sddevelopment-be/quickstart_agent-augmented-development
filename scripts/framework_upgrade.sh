#!/bin/sh
# Framework Upgrade Script
# Version: 1.0.0
# Purpose: Upgrade agent-augmented development framework with conflict detection
# Requirements: POSIX-compliant shell, cp, find, sha256sum

set -e

# Configuration
DRY_RUN=0
TARGET_DIR=""
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Determine package directory
if [ -d "./framework_core" ]; then
    PACKAGE_DIR="$(pwd)"
elif [ -d "${SCRIPT_DIR}/../framework_core" ]; then
    PACKAGE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
else
    PACKAGE_DIR="$(pwd)"
fi

FRAMEWORK_CORE="${PACKAGE_DIR}/framework_core"

# Counters
NEW_COUNT=0
UNCHANGED_COUNT=0
CONFLICT_COUNT=0
ERROR_COUNT=0

# Colors for output
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    GREEN=''
    YELLOW=''
    RED=''
    BLUE=''
    NC=''
fi

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        *)
            if [ -z "${TARGET_DIR}" ]; then
                TARGET_DIR="$1"
            fi
            shift
            ;;
    esac
done

# Default to current directory if not specified
if [ -z "${TARGET_DIR}" ]; then
    TARGET_DIR="."
fi

# Convert TARGET_DIR to absolute path
TARGET_DIR="$(cd "${TARGET_DIR}" && pwd)"

# Now set file paths after TARGET_DIR is determined
META_FILE="${TARGET_DIR}/.framework_meta.yml"
REPORT_FILE="${TARGET_DIR}/framework-upgrade-report.txt"

echo "🔄 Framework Upgrade Script"
if [ ${DRY_RUN} -eq 1 ]; then
    echo "${BLUE}[DRY-RUN MODE]${NC}"
fi
echo "Target: ${TARGET_DIR}"
echo "Source: ${PACKAGE_DIR}"
echo ""

# Validate target directory
if [ ! -d "${TARGET_DIR}" ]; then
    echo "${RED}❌ Error: Target directory does not exist: ${TARGET_DIR}${NC}"
    exit 1
fi

# Check if framework_core exists
if [ ! -d "${FRAMEWORK_CORE}" ]; then
    echo "${RED}❌ Error: framework_core/ not found in package${NC}"
    echo "Expected: ${FRAMEWORK_CORE}"
    exit 1
fi

# Check for existing installation
if [ ! -f "${META_FILE}" ]; then
    echo "${RED}❌ Error: No framework installation found${NC}"
    echo "Meta file missing: ${META_FILE}"
    echo ""
    echo "Use framework_install.sh for first-time installation"
    exit 1
fi

# Read current version
if [ -f "${META_FILE}" ]; then
    CURRENT_VERSION=$(grep "^framework_version:" "${META_FILE}" | cut -d' ' -f2 || echo "unknown")
else
    CURRENT_VERSION="unknown"
fi

# Read new version from package
MANIFEST="${PACKAGE_DIR}/META/MANIFEST.yml"
if [ -f "${MANIFEST}" ]; then
    NEW_VERSION=$(grep "^framework_version:" "${MANIFEST}" | cut -d' ' -f2 || echo "unknown")
else
    NEW_VERSION="unknown"
fi

echo "Current version: ${CURRENT_VERSION}"
echo "New version: ${NEW_VERSION}"
echo ""

# Initialize report
cat > "${REPORT_FILE}" << EOF
Framework Upgrade Report
Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Target: ${TARGET_DIR}
Source: ${PACKAGE_DIR}
Current Version: ${CURRENT_VERSION}
New Version: ${NEW_VERSION}
Mode: $([ ${DRY_RUN} -eq 1 ] && echo "DRY-RUN" || echo "APPLY")

Status Summary:
EOF

echo "📦 Analyzing upgrade..."
echo ""

# Create temp file for results
TEMP_RESULTS="/tmp/framework-upgrade-$$-results.txt"
echo "0 0 0 0" > "${TEMP_RESULTS}"

# Process files from framework_core
cd "${FRAMEWORK_CORE}"
find . -type f | sort | while IFS= read -r file
do
    # Remove leading ./
    clean_path="${file#./}"
    target_file="${TARGET_DIR}/${clean_path}"
    source_file="${file}"
    
    # Skip files in local/** directories
    case "${clean_path}" in
        local/*|*/local/*)
            continue
            ;;
    esac
    
    # Read current counts
    read -r new unchanged conflict err < "${TEMP_RESULTS}"
    
    # Check if file exists in target
    if [ ! -f "${target_file}" ]; then
        # File is NEW
        echo "  ${BLUE}🆕 NEW:${NC} ${clean_path}"
        new=$((new + 1))
        echo "NEW: ${clean_path}" >> "${REPORT_FILE}"
        
        if [ ${DRY_RUN} -eq 0 ]; then
            target_dir="$(dirname "${target_file}")"
            mkdir -p "${target_dir}"
            cp -p "${source_file}" "${target_file}"
        fi
    else
        # File exists - compare checksums
        source_checksum=$(sha256sum "${source_file}" | cut -d' ' -f1)
        target_checksum=$(sha256sum "${target_file}" | cut -d' ' -f1)
        
        if [ "${source_checksum}" = "${target_checksum}" ]; then
            # Files are UNCHANGED
            echo "  ✅ UNCHANGED: ${clean_path}"
            unchanged=$((unchanged + 1))
            echo "UNCHANGED: ${clean_path}" >> "${REPORT_FILE}"
        else
            # Files are different - CONFLICT
            echo "  ${YELLOW}⚠️  CONFLICT:${NC} ${clean_path}"
            conflict=$((conflict + 1))
            echo "CONFLICT: ${clean_path}" >> "${REPORT_FILE}"
            
            if [ ${DRY_RUN} -eq 0 ]; then
                # Create backup of existing file
                backup_file="${target_file}.bak.$(date +%Y%m%d%H%M%S)"
                cp -p "${target_file}" "${backup_file}"
                
                # Write new version with .framework-new extension
                framework_new_file="${target_file}.framework-new"
                cp -p "${source_file}" "${framework_new_file}"
                
                echo "    Backup: ${backup_file##*/}"
                echo "    New version: ${framework_new_file##*/}"
            else
                echo "    [Would create: ${target_file}.framework-new]"
            fi
        fi
    fi
    
    # Write updated counts
    echo "${new} ${unchanged} ${conflict} ${err}" > "${TEMP_RESULTS}"
done

# Read final counts
read -r NEW_COUNT UNCHANGED_COUNT CONFLICT_COUNT ERROR_COUNT < "${TEMP_RESULTS}"
rm -f "${TEMP_RESULTS}"

# Update metadata (only in non-dry-run mode)
if [ ${DRY_RUN} -eq 0 ]; then
    echo ""
    echo "📝 Updating framework metadata..."
    
    # Preserve existing metadata and update version
    if [ -f "${META_FILE}" ]; then
        # Create temporary file with updated version
        sed "s/^framework_version:.*/framework_version: ${NEW_VERSION}/" "${META_FILE}" > "${META_FILE}.tmp"
        
        # Add upgrade timestamp
        if ! grep -q "^last_upgraded_at:" "${META_FILE}"; then
            echo "last_upgraded_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")" >> "${META_FILE}.tmp"
        else
            sed -i "s/^last_upgraded_at:.*/last_upgraded_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")/" "${META_FILE}.tmp"
        fi
        
        # Add upgrade history entry
        echo "" >> "${META_FILE}.tmp"
        echo "# Upgrade history" >> "${META_FILE}.tmp"
        echo "# - ${CURRENT_VERSION} -> ${NEW_VERSION} at $(date -u +"%Y-%m-%dT%H:%M:%SZ")" >> "${META_FILE}.tmp"
        
        mv "${META_FILE}.tmp" "${META_FILE}"
        echo "${GREEN}✅${NC} Updated: .framework_meta.yml"
    fi
fi

# Finalize report
cat >> "${REPORT_FILE}" << EOF

Upgrade Statistics:
- Files added (NEW): ${NEW_COUNT}
- Files unchanged (UNCHANGED): ${UNCHANGED_COUNT}
- Files with conflicts (CONFLICT): ${CONFLICT_COUNT}
- Errors encountered: ${ERROR_COUNT}

New Version: ${NEW_VERSION}
$([ ${DRY_RUN} -eq 0 ] && echo "Meta file updated: .framework_meta.yml" || echo "Meta file NOT updated (dry-run)")
EOF

# Summary
echo ""
echo "📊 Upgrade Summary:"
echo "  ${BLUE}🆕 NEW:${NC} ${NEW_COUNT} files"
echo "  ✅ UNCHANGED: ${UNCHANGED_COUNT} files"
if [ "${CONFLICT_COUNT}" -gt 0 ]; then
    echo "  ${YELLOW}⚠️  CONFLICT:${NC} ${CONFLICT_COUNT} files"
fi
if [ "${ERROR_COUNT}" -gt 0 ]; then
    echo "  ${RED}❌ ERROR:${NC} ${ERROR_COUNT} files"
fi
echo ""
echo "📄 Report saved: framework-upgrade-report.txt"

if [ ${DRY_RUN} -eq 1 ]; then
    echo ""
    echo "${BLUE}ℹ️  DRY-RUN MODE - No changes were made${NC}"
    echo "Run without --dry-run to apply changes"
fi

if [ "${CONFLICT_COUNT}" -gt 0 ]; then
    echo ""
    if [ ${DRY_RUN} -eq 0 ]; then
        echo "${YELLOW}⚠️  Conflicts detected${NC}"
        echo "Review .framework-new files and resolve conflicts manually"
        echo ""
        echo "Next steps:"
        echo "  1. Review each .framework-new file"
        echo "  2. Decide: accept framework version or keep local changes"
        echo "  3. Run Framework Guardian for assistance:"
        echo "     python3 work/scripts/framework_guardian.py --mode upgrade --target ."
    else
        echo "${YELLOW}⚠️  Conflicts would be detected${NC}"
        echo "Run without --dry-run to create .framework-new files"
    fi
    exit 0
fi

if [ "${ERROR_COUNT}" -gt 0 ]; then
    echo ""
    echo "${RED}⚠️  Upgrade completed with errors${NC}"
    exit 1
fi

echo ""
if [ ${DRY_RUN} -eq 0 ]; then
    echo "${GREEN}✅ Upgrade complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Test the upgraded framework"
    echo "  2. Run audit: python3 work/scripts/framework_guardian.py --mode audit --target ."
    echo "  3. Commit changes to version control"
else
    echo "${GREEN}✅ Dry-run complete!${NC}"
    echo "Review the report and run without --dry-run to apply"
fi

exit 0
