#!/bin/sh
# Test Suite for framework_upgrade.sh
# Version: 1.0.0

set -e

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
UPGRADE_SCRIPT="${SCRIPT_DIR}/../framework_upgrade.sh"
TEST_DIR="/tmp/framework-upgrade-tests"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0;0m'

# Helper functions
test_start() {
    TEST_COUNT=$((TEST_COUNT + 1))
    echo ""
    echo "${YELLOW}Test ${TEST_COUNT}: $1${NC}"
}

test_pass() {
    PASS_COUNT=$((PASS_COUNT + 1))
    echo "${GREEN}✅ PASS${NC}"
}

test_fail() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "${RED}❌ FAIL: $1${NC}"
}

cleanup() {
    if [ -d "${TEST_DIR}" ]; then
        rm -rf "${TEST_DIR}"
    fi
}

setup_package_v1() {
    mkdir -p "${TEST_DIR}/package-v1/framework_core/.github"
    mkdir -p "${TEST_DIR}/package-v1/META"
    echo "version 1 content" > "${TEST_DIR}/package-v1/framework_core/.github/test.txt"
    cat > "${TEST_DIR}/package-v1/META/MANIFEST.yml" << 'EOF'
framework_version: 1.0.0
packaged_at: 2025-11-24T20:00:00Z
EOF
}

setup_package_v2() {
    mkdir -p "${TEST_DIR}/package-v2/framework_core/.github"
    mkdir -p "${TEST_DIR}/package-v2/META"
    echo "version 2 content" > "${TEST_DIR}/package-v2/framework_core/.github/test.txt"
    echo "new file" > "${TEST_DIR}/package-v2/framework_core/.github/new-file.txt"
    cat > "${TEST_DIR}/package-v2/META/MANIFEST.yml" << 'EOF'
framework_version: 2.0.0
packaged_at: 2025-11-24T21:00:00Z
EOF
}

# Test suite
echo "🧪 Framework Upgrade Script Test Suite"
echo "========================================"

# Clean start
cleanup

# Test 1: Dry-run mode
test_start "Dry-run mode does not modify files"
setup_package_v1
mkdir -p "${TEST_DIR}/target1/.github"
echo "version 1 content" > "${TEST_DIR}/target1/.github/test.txt"
cat > "${TEST_DIR}/target1/.framework_meta.yml" << 'EOF'
framework_version: 1.0.0
installed_at: 2025-11-24T20:00:00Z
EOF
setup_package_v2
cd "${TEST_DIR}/package-v2"
if sh "${UPGRADE_SCRIPT}" --dry-run "${TEST_DIR}/target1" > /dev/null 2>&1; then
    # Check that no .framework-new files were created
    if [ ! -f "${TEST_DIR}/target1/.github/test.txt.framework-new" ]; then
        test_pass
    else
        test_fail ".framework-new file created in dry-run"
    fi
else
    test_fail "Script exited with error"
fi

# Test 2: Detect unchanged files
test_start "Detect unchanged files correctly"
setup_package_v1
mkdir -p "${TEST_DIR}/target2/.github"
echo "version 1 content" > "${TEST_DIR}/target2/.github/test.txt"
cat > "${TEST_DIR}/target2/.framework_meta.yml" << 'EOF'
framework_version: 1.0.0
installed_at: 2025-11-24T20:00:00Z
EOF
cd "${TEST_DIR}/package-v1"
if sh "${UPGRADE_SCRIPT}" "${TEST_DIR}/target2" > /dev/null 2>&1; then
    if grep -q "UNCHANGED" "${TEST_DIR}/target2/framework-upgrade-report.txt"; then
        test_pass
    else
        test_fail "Unchanged files not detected"
    fi
else
    test_fail "Script exited with error"
fi

# Test 3: Detect conflicts
test_start "Detect and create .framework-new for conflicts"
setup_package_v1
mkdir -p "${TEST_DIR}/target3/.github"
echo "modified content" > "${TEST_DIR}/target3/.github/test.txt"
cat > "${TEST_DIR}/target3/.framework_meta.yml" << 'EOF'
framework_version: 1.0.0
installed_at: 2025-11-24T20:00:00Z
EOF
setup_package_v2
cd "${TEST_DIR}/package-v2"
if sh "${UPGRADE_SCRIPT}" "${TEST_DIR}/target3" > /dev/null 2>&1; then
    if [ -f "${TEST_DIR}/target3/.github/test.txt.framework-new" ]; then
        if [ -f "${TEST_DIR}/target3/.github/test.txt.bak"* ]; then
            test_pass
        else
            test_fail "Backup file not created"
        fi
    else
        test_fail ".framework-new file not created"
    fi
else
    test_fail "Script exited with error"
fi

# Test 4: Add new files
test_start "Add new files during upgrade"
setup_package_v1
mkdir -p "${TEST_DIR}/target4/.github"
echo "version 1 content" > "${TEST_DIR}/target4/.github/test.txt"
cat > "${TEST_DIR}/target4/.framework_meta.yml" << 'EOF'
framework_version: 1.0.0
installed_at: 2025-11-24T20:00:00Z
EOF
setup_package_v2
cd "${TEST_DIR}/package-v2"
if sh "${UPGRADE_SCRIPT}" "${TEST_DIR}/target4" > /dev/null 2>&1; then
    if [ -f "${TEST_DIR}/target4/.github/new-file.txt" ]; then
        test_pass
    else
        test_fail "New file not added"
    fi
else
    test_fail "Script exited with error"
fi

# Test 5: Reject upgrade without existing installation
test_start "Reject upgrade when no installation exists"
setup_package_v2
mkdir -p "${TEST_DIR}/target5"
cd "${TEST_DIR}/package-v2"
if ! sh "${UPGRADE_SCRIPT}" "${TEST_DIR}/target5" > /dev/null 2>&1; then
    test_pass
else
    test_fail "Should reject upgrade without existing installation"
fi

# Test 6: Update metadata file
test_start "Update .framework_meta.yml with new version"
setup_package_v1
mkdir -p "${TEST_DIR}/target6/.github"
echo "version 1 content" > "${TEST_DIR}/target6/.github/test.txt"
cat > "${TEST_DIR}/target6/.framework_meta.yml" << 'EOF'
framework_version: 1.0.0
installed_at: 2025-11-24T20:00:00Z
EOF
setup_package_v2
cd "${TEST_DIR}/package-v2"
if sh "${UPGRADE_SCRIPT}" "${TEST_DIR}/target6" > /dev/null 2>&1; then
    if grep -q "framework_version: 2.0.0" "${TEST_DIR}/target6/.framework_meta.yml"; then
        test_pass
    else
        test_fail "Metadata not updated"
    fi
else
    test_fail "Script exited with error"
fi

# Test 7: Generate upgrade report
test_start "Generate comprehensive upgrade report"
setup_package_v1
mkdir -p "${TEST_DIR}/target7/.github"
echo "version 1 content" > "${TEST_DIR}/target7/.github/test.txt"
cat > "${TEST_DIR}/target7/.framework_meta.yml" << 'EOF'
framework_version: 1.0.0
installed_at: 2025-11-24T20:00:00Z
EOF
setup_package_v2
cd "${TEST_DIR}/package-v2"
if sh "${UPGRADE_SCRIPT}" "${TEST_DIR}/target7" > /dev/null 2>&1; then
    if [ -f "${TEST_DIR}/target7/framework-upgrade-report.txt" ]; then
        if grep -q "Upgrade Statistics" "${TEST_DIR}/target7/framework-upgrade-report.txt"; then
            test_pass
        else
            test_fail "Report missing statistics"
        fi
    else
        test_fail "Report not created"
    fi
else
    test_fail "Script exited with error"
fi

# Cleanup
cleanup

# Summary
echo ""
echo "========================================"
echo "📊 Test Summary:"
echo "  Total: ${TEST_COUNT}"
echo "  ${GREEN}Pass: ${PASS_COUNT}${NC}"
if [ "${FAIL_COUNT}" -gt 0 ]; then
    echo "  ${RED}Fail: ${FAIL_COUNT}${NC}"
    echo ""
    echo "${RED}❌ Tests failed${NC}"
    exit 1
else
    echo ""
    echo "${GREEN}✅ All tests passed${NC}"
    exit 0
fi
