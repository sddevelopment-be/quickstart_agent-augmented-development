#!/bin/sh
# Framework Installation Script
# Version: 1.0.0
# Purpose: Install agent-augmented development framework in target repository
# Requirements: POSIX-compliant shell, cp, find

set -e

# Configuration
TARGET_DIR="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Determine package directory:
# When extracted from package: current working directory contains framework_core/
# When run from repo: SCRIPT_DIR/.. contains framework_core/
if [ -d "./framework_core" ]; then
    PACKAGE_DIR="$(pwd)"
elif [ -d "${SCRIPT_DIR}/../framework_core" ]; then
    PACKAGE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
else
    # Last resort: assume current directory
    PACKAGE_DIR="$(pwd)"
fi

FRAMEWORK_CORE="${PACKAGE_DIR}/framework_core"
META_FILE="${TARGET_DIR}/.framework_meta.yml"
REPORT_FILE="${TARGET_DIR}/framework-install-report.txt"

# Counters
NEW_COUNT=0
SKIPPED_COUNT=0
ERROR_COUNT=0

# Colors for output (if terminal supports it)
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    NC='\033[0m'
else
    GREEN=''
    YELLOW=''
    RED=''
    NC=''
fi

echo "🚀 Framework Installation Script"
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
if [ -f "${META_FILE}" ]; then
    echo "${YELLOW}⚠️  Warning: Framework already installed${NC}"
    echo "Meta file found: ${META_FILE}"
    echo ""
    cat "${META_FILE}"
    echo ""
    echo "To upgrade, use framework_upgrade.sh instead"
    exit 1
fi

# Initialize report
cat > "${REPORT_FILE}" << EOF
Framework Installation Report
Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Target: ${TARGET_DIR}
Source: ${PACKAGE_DIR}

Status Summary:
EOF

echo "📦 Installing framework files..."
echo ""

# Copy files from framework_core to target
cd "${FRAMEWORK_CORE}"

# Create temp file for results to work around subshell issue
TEMP_RESULTS="/tmp/framework-install-$$-results.txt"
echo "0 0 0" > "${TEMP_RESULTS}"

find . -type f | sort | while IFS= read -r file
do
    # Remove leading ./
    clean_path="${file#./}"
    target_file="${TARGET_DIR}/${clean_path}"
    
    # Read current counts
    read -r new skip err < "${TEMP_RESULTS}"
    
    # Check if file already exists
    if [ -f "${target_file}" ]; then
        echo "  ⏭️  SKIP: ${clean_path} (already exists)"
        skip=$((skip + 1))
        echo "SKIPPED: ${clean_path}" >> "${REPORT_FILE}"
    else
        # Create parent directory if needed
        target_dir="$(dirname "${target_file}")"
        mkdir -p "${target_dir}"
        
        # Copy file preserving permissions
        if cp -p "${file}" "${target_file}"; then
            echo "  ${GREEN}✅${NC} NEW: ${clean_path}"
            new=$((new + 1))
            echo "NEW: ${clean_path}" >> "${REPORT_FILE}"
        else
            echo "  ${RED}❌${NC} ERROR: ${clean_path}"
            err=$((err + 1))
            echo "ERROR: ${clean_path}" >> "${REPORT_FILE}"
        fi
    fi
    
    # Write updated counts
    echo "${new} ${skip} ${err}" > "${TEMP_RESULTS}"
done

# Read final counts
read -r NEW_COUNT SKIPPED_COUNT ERROR_COUNT < "${TEMP_RESULTS}"
rm -f "${TEMP_RESULTS}"

# Extract version from META/MANIFEST.yml if available
MANIFEST="${PACKAGE_DIR}/META/MANIFEST.yml"
if [ -f "${MANIFEST}" ]; then
    VERSION=$(grep "^framework_version:" "${MANIFEST}" | cut -d' ' -f2 || echo "unknown")
else
    VERSION="unknown"
fi

# Create .framework_meta.yml
echo ""
echo "📝 Creating framework metadata..."

cat > "${META_FILE}" << EOF
# Framework Installation Metadata
# This file tracks the installed framework version
# DO NOT edit manually - managed by framework scripts

framework_version: ${VERSION}
installed_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
source_package: $(basename "${PACKAGE_DIR}")
installation_method: framework_install.sh
target_directory: $(cd "${TARGET_DIR}" && pwd)

# Installation statistics
files_installed: ${NEW_COUNT}
files_skipped: ${SKIPPED_COUNT}
files_errored: ${ERROR_COUNT}
EOF

echo "${GREEN}✅${NC} Created: .framework_meta.yml"

# Finalize report
cat >> "${REPORT_FILE}" << EOF

Installation Statistics:
- Files installed (NEW): ${NEW_COUNT}
- Files skipped (already exist): ${SKIPPED_COUNT}
- Errors encountered: ${ERROR_COUNT}

Framework Version: ${VERSION}
Meta file created: .framework_meta.yml
EOF

# Summary
echo ""
echo "📊 Installation Summary:"
echo "  ${GREEN}✅ NEW:${NC} ${NEW_COUNT} files"
echo "  ⏭️  SKIP: ${SKIPPED_COUNT} files"
if [ "${ERROR_COUNT}" -gt 0 ]; then
    echo "  ${RED}❌ ERROR:${NC} ${ERROR_COUNT} files"
fi
echo ""
echo "📄 Report saved: framework-install-report.txt"
echo "📄 Metadata saved: .framework_meta.yml"
echo ""

if [ "${ERROR_COUNT}" -gt 0 ]; then
    echo "${RED}⚠️  Installation completed with errors${NC}"
    exit 1
else
    echo "${GREEN}✅ Installation complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review installed files in your repository"
    echo "  2. Commit changes to version control"
    echo "  3. See docs/HOW_TO_USE/ for framework usage"
    exit 0
fi
