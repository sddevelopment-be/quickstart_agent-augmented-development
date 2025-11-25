#!/bin/sh
# Test Suite for framework_install.sh
# Version: 1.0.0

set -e

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_SCRIPT="${SCRIPT_DIR}/../framework_install.sh"
TEST_DIR="/tmp/framework-install-tests"
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

setup_test_package() {
    mkdir -p "${TEST_DIR}/package/framework_core/.github"
    mkdir -p "${TEST_DIR}/package/META"
    echo "test file" > "${TEST_DIR}/package/framework_core/.github/test.txt"
    cat > "${TEST_DIR}/package/META/MANIFEST.yml" << 'EOF'
framework_version: 1.0.0-test
packaged_at: 2025-11-24T20:00:00Z
EOF
}

# Test suite
echo "🧪 Framework Install Script Test Suite"
echo "======================================"

# Clean start
cleanup

# Test 1: New installation
test_start "New installation in empty directory"
setup_test_package
mkdir -p "${TEST_DIR}/target1"
cd "${TEST_DIR}/package"

if ! sh "${INSTALL_SCRIPT}" "${TEST_DIR}/target1" > /dev/null 2>&1; then
    test_fail "Script exited with error"
elif [ ! -f "${TEST_DIR}/target1/.framework_meta.yml" ]; then
    test_fail "Meta file not created"
elif [ ! -f "${TEST_DIR}/target1/.github/test.txt" ]; then
    test_fail "File not copied"
else
    test_pass
fi

# Test 2: Detect existing installation
test_start "Reject installation when already installed"
if ! sh "${INSTALL_SCRIPT}" "${TEST_DIR}/target1" > /dev/null 2>&1; then
    test_pass
else
    test_fail "Should reject re-installation"
fi

# Test 3: Skip existing files
test_start "Skip files that already exist"
setup_test_package
mkdir -p "${TEST_DIR}/target2/.github"
echo "existing file" > "${TEST_DIR}/target2/.github/test.txt"
cd "${TEST_DIR}/package"
if sh "${INSTALL_SCRIPT}" "${TEST_DIR}/target2" > /dev/null 2>&1; then
    content=$(cat "${TEST_DIR}/target2/.github/test.txt")
    if [ "${content}" = "existing file" ]; then
        test_pass
    else
        test_fail "Existing file was overwritten"
    fi
else
    test_fail "Script exited with error"
fi

# Test 4: Create parent directories
test_start "Create parent directories as needed"
setup_test_package
mkdir -p "${TEST_DIR}/package/framework_core/deep/nested/path"
echo "deep file" > "${TEST_DIR}/package/framework_core/deep/nested/path/file.txt"
mkdir -p "${TEST_DIR}/target3"
cd "${TEST_DIR}/package"

if ! sh "${INSTALL_SCRIPT}" "${TEST_DIR}/target3" > /dev/null 2>&1; then
    test_fail "Script exited with error"
elif [ ! -f "${TEST_DIR}/target3/deep/nested/path/file.txt" ]; then
    test_fail "Deep file not created"
else
    test_pass
fi

# Test 5: Report file generation
test_start "Generate installation report"
setup_test_package
mkdir -p "${TEST_DIR}/target4"
cd "${TEST_DIR}/package"
if sh "${INSTALL_SCRIPT}" "${TEST_DIR}/target4" > /dev/null 2>&1; then
    if [ -f "${TEST_DIR}/target4/framework-install-report.txt" ]; then
        if grep -q "Installation Statistics" "${TEST_DIR}/target4/framework-install-report.txt"; then
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

# Test 6: Invalid target directory
test_start "Reject invalid target directory"
setup_test_package
cd "${TEST_DIR}/package"
if ! sh "${INSTALL_SCRIPT}" "${TEST_DIR}/nonexistent" > /dev/null 2>&1; then
    test_pass
else
    test_fail "Should reject invalid directory"
fi

# Test 7: Missing framework_core
test_start "Reject installation without framework_core"
mkdir -p "${TEST_DIR}/empty-package"
mkdir -p "${TEST_DIR}/target5"
cd "${TEST_DIR}/empty-package"
if ! sh "${INSTALL_SCRIPT}" "${TEST_DIR}/target5" > /dev/null 2>&1; then
    test_pass
else
    test_fail "Should reject missing framework_core"
fi

# Cleanup
cleanup

# Summary
echo ""
echo "======================================"
echo "📊 Test Summary:"
echo "  Total: ${TEST_COUNT}"
echo "  ${GREEN}Pass: ${PASS_COUNT}${NC}"
if [ ${FAIL_COUNT} -gt 0 ]; then
    echo "  ${RED}Fail: ${FAIL_COUNT}${NC}"
    echo ""
    echo "${RED}❌ Tests failed${NC}"
    exit 1
else
    echo ""
    echo "${GREEN}✅ All tests passed${NC}"
    exit 0
fi
