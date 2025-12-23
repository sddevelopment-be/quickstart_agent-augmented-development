#!/usr/bin/env bash
# test_manifest_generation.sh
# Acceptance and unit tests for generate_manifest.sh
# Follows ATDD (directive 016) and TDD (directive 017) approach

set -euo pipefail

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Setup test environment
TEST_DIR=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GENERATE_SCRIPT="${SCRIPT_DIR}/generate_manifest.sh"

# Utility functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $*"
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $*"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

setup_test_env() {
    TEST_DIR=$(mktemp -d)
    log_info "Test environment created: ${TEST_DIR}"
}

teardown_test_env() {
    if [ -n "${TEST_DIR}" ] && [ -d "${TEST_DIR}" ]; then
        rm -rf "${TEST_DIR}"
        log_info "Test environment cleaned up"
    fi
}

assert_file_exists() {
    local file="$1"
    local test_name="$2"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    
    if [ -f "${file}" ]; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        log_success "${test_name}: File exists"
        return 0
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        log_error "${test_name}: File does not exist: ${file}"
        return 1
    fi
}

assert_contains() {
    local file="$1"
    local pattern="$2"
    local test_name="$3"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    
    if grep -q "${pattern}" "${file}"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        log_success "${test_name}: Pattern found"
        return 0
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        log_error "${test_name}: Pattern not found: ${pattern}"
        return 1
    fi
}

assert_yaml_valid() {
    local file="$1"
    local test_name="$2"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    
    # Check if yq is available for YAML validation
    if command -v yq &> /dev/null; then
        if yq eval '.' "${file}" > /dev/null 2>&1; then
            TESTS_PASSED=$((TESTS_PASSED + 1))
            log_success "${test_name}: Valid YAML"
            return 0
        else
            TESTS_FAILED=$((TESTS_FAILED + 1))
            log_error "${test_name}: Invalid YAML"
            return 1
        fi
    else
        # Fallback: basic YAML structure check
        if python3 -c "import yaml; yaml.safe_load(open('${file}'))" 2>/dev/null; then
            TESTS_PASSED=$((TESTS_PASSED + 1))
            log_success "${test_name}: Valid YAML (Python)"
            return 0
        else
            TESTS_FAILED=$((TESTS_FAILED + 1))
            log_error "${test_name}: Invalid YAML"
            return 1
        fi
    fi
}

assert_checksum_valid() {
    local checksum="$1"
    local test_name="$2"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    
    # SHA256 checksum is 64 hex characters
    if echo "${checksum}" | grep -qE "^sha256:[a-f0-9]{64}$"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        log_success "${test_name}: Valid checksum format"
        return 0
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        log_error "${test_name}: Invalid checksum format: ${checksum}"
        return 1
    fi
}

# ============================================================================
# ACCEPTANCE TESTS (High-level behavior tests - ATDD)
# ============================================================================

test_acceptance_script_exists() {
    log_info "Running: test_acceptance_script_exists"
    assert_file_exists "${GENERATE_SCRIPT}" "Generate script exists"
}

test_acceptance_script_executable() {
    log_info "Running: test_acceptance_script_executable"
    TESTS_RUN=$((TESTS_RUN + 1))
    
    if [ -x "${GENERATE_SCRIPT}" ]; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        log_success "Generate script is executable"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        log_error "Generate script is not executable"
    fi
}

test_acceptance_generates_manifest() {
    log_info "Running: test_acceptance_generates_manifest"
    
    local output="${TEST_DIR}/manifest_output.yml"
    
    # Run generation script
    if "${GENERATE_SCRIPT}" --output "${output}" --version "1.0.0-test" > /dev/null 2>&1; then
        assert_file_exists "${output}" "Manifest file generated"
    else
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        log_error "Failed to generate manifest"
    fi
}

test_acceptance_manifest_structure() {
    log_info "Running: test_acceptance_manifest_structure"
    
    local output="${TEST_DIR}/manifest_structure.yml"
    "${GENERATE_SCRIPT}" --output "${output}" --version "1.0.0-test" > /dev/null 2>&1
    
    # Check for required sections
    assert_contains "${output}" "framework:" "Has framework section"
    assert_contains "${output}" "paths:" "Has paths section"
    assert_contains "${output}" "files:" "Has files section"
    assert_contains "${output}" "name:" "Has framework name"
    assert_contains "${output}" "version:" "Has framework version"
}

test_acceptance_includes_core_paths() {
    log_info "Running: test_acceptance_includes_core_paths"
    
    local output="${TEST_DIR}/manifest_paths.yml"
    "${GENERATE_SCRIPT}" --output "${output}" --version "1.0.0-test" > /dev/null 2>&1
    
    # Check for core framework paths
    assert_contains "${output}" ".github/agents" "Includes .github/agents"
    assert_contains "${output}" "docs/templates" "Includes docs/templates"
    assert_contains "${output}" "validation" "Includes validation"
}

test_acceptance_checksums_present() {
    log_info "Running: test_acceptance_checksums_present"
    
    local output="${TEST_DIR}/manifest_checksums.yml"
    "${GENERATE_SCRIPT}" --output "${output}" --version "1.0.0-test" > /dev/null 2>&1
    
    assert_contains "${output}" "checksum:" "Has checksum entries"
    assert_contains "${output}" "sha256:" "Uses SHA256 checksums"
}

test_acceptance_modes_assigned() {
    log_info "Running: test_acceptance_modes_assigned"
    
    local output="${TEST_DIR}/manifest_modes.yml"
    "${GENERATE_SCRIPT}" --output "${output}" --version "1.0.0-test" > /dev/null 2>&1
    
    assert_contains "${output}" "mode: sync-always" "Has sync-always mode"
    assert_contains "${output}" "mode: copy-once" "Has copy-once mode"
}

test_acceptance_dry_run_mode() {
    log_info "Running: test_acceptance_dry_run_mode"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    
    # Dry run should output to stdout (stderr has INFO messages, so capture both and check)
    local output=$("${GENERATE_SCRIPT}" --dry-run --version "1.0.0-test" 2>&1)
    if echo "${output}" | grep -q "framework:"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        log_success "Dry run outputs to stdout"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        log_error "Dry run does not output valid manifest"
    fi
}

test_acceptance_idempotency() {
    log_info "Running: test_acceptance_idempotency"
    
    local output1="${TEST_DIR}/manifest_run1.yml"
    local output2="${TEST_DIR}/manifest_run2.yml"
    
    "${GENERATE_SCRIPT}" --output "${output1}" --version "1.0.0-test" > /dev/null 2>&1
    sleep 1
    "${GENERATE_SCRIPT}" --output "${output2}" --version "1.0.0-test" > /dev/null 2>&1
    
    TESTS_RUN=$((TESTS_RUN + 1))
    
    # Compare outputs (ignoring release_date and Generated timestamp which may differ)
    if diff <(grep -v "release_date:" "${output1}" | grep -v "# Generated:") \
            <(grep -v "release_date:" "${output2}" | grep -v "# Generated:") > /dev/null 2>&1; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        log_success "Script is idempotent"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        log_error "Script produces different output on subsequent runs"
    fi
}

# ============================================================================
# UNIT TESTS (Detailed component tests - TDD)
# ============================================================================

test_unit_yaml_validity() {
    log_info "Running: test_unit_yaml_validity"
    
    local output="${TEST_DIR}/manifest_yaml.yml"
    "${GENERATE_SCRIPT}" --output "${output}" --version "1.0.0-test" > /dev/null 2>&1
    
    assert_yaml_valid "${output}" "Generated YAML is valid"
}

test_unit_checksum_format() {
    log_info "Running: test_unit_checksum_format"
    
    local output="${TEST_DIR}/manifest_checksum_format.yml"
    "${GENERATE_SCRIPT}" --output "${output}" --version "1.0.0-test" > /dev/null 2>&1
    
    # Extract first checksum and validate format
    local checksum=$(grep -m 1 "checksum:" "${output}" | awk '{print $2}' | tr -d '"')
    
    if [ -n "${checksum}" ]; then
        assert_checksum_valid "${checksum}" "Checksum format"
    else
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        log_error "No checksums found in manifest"
    fi
}

test_unit_version_parameter() {
    log_info "Running: test_unit_version_parameter"
    
    local output="${TEST_DIR}/manifest_version.yml"
    "${GENERATE_SCRIPT}" --output "${output}" --version "9.8.7-test" > /dev/null 2>&1
    
    assert_contains "${output}" "9.8.7-test" "Custom version applied"
}

test_unit_excludes_work_files() {
    log_info "Running: test_unit_excludes_work_files"
    
    local output="${TEST_DIR}/manifest_excludes.yml"
    "${GENERATE_SCRIPT}" --output "${output}" --version "1.0.0-test" > /dev/null 2>&1
    
    TESTS_RUN=$((TESTS_RUN + 1))
    
    # Should NOT include work task files (except README.md)
    if ! grep -q "work/collaboration" "${output}" && ! grep -q "work/planning" "${output}"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        log_success "Excludes work task files"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        log_error "Includes unwanted work files"
    fi
}

test_unit_includes_work_readme() {
    log_info "Running: test_unit_includes_work_readme"
    
    local output="${TEST_DIR}/manifest_work_readme.yml"
    "${GENERATE_SCRIPT}" --output "${output}" --version "1.0.0-test" > /dev/null 2>&1
    
    assert_contains "${output}" "work/README.md" "Includes work/README.md"
}

test_unit_framework_scripts_included() {
    log_info "Running: test_unit_framework_scripts_included"
    
    local output="${TEST_DIR}/manifest_scripts.yml"
    "${GENERATE_SCRIPT}" --output "${output}" --version "1.0.0-test" > /dev/null 2>&1
    
    assert_contains "${output}" "framework_install.sh" "Includes install script"
    assert_contains "${output}" "framework_upgrade.sh" "Includes upgrade script"
}

# ============================================================================
# TEST RUNNER
# ============================================================================

run_all_tests() {
    log_info "=========================================="
    log_info "Starting Manifest Generation Test Suite"
    log_info "=========================================="
    echo
    
    setup_test_env
    
    # Acceptance Tests (ATDD)
    log_info "=== ACCEPTANCE TESTS ==="
    test_acceptance_script_exists
    test_acceptance_script_executable
    test_acceptance_generates_manifest
    test_acceptance_manifest_structure
    test_acceptance_includes_core_paths
    test_acceptance_checksums_present
    test_acceptance_modes_assigned
    test_acceptance_dry_run_mode
    test_acceptance_idempotency
    echo
    
    # Unit Tests (TDD)
    log_info "=== UNIT TESTS ==="
    test_unit_yaml_validity
    test_unit_checksum_format
    test_unit_version_parameter
    test_unit_excludes_work_files
    test_unit_includes_work_readme
    test_unit_framework_scripts_included
    echo
    
    teardown_test_env
    
    # Summary
    log_info "=========================================="
    log_info "Test Summary"
    log_info "=========================================="
    log_info "Tests run:    ${TESTS_RUN}"
    log_success "Tests passed: ${TESTS_PASSED}"
    if [ "${TESTS_FAILED}" -gt 0 ]; then
        log_error "Tests failed: ${TESTS_FAILED}"
    else
        log_info "Tests failed: ${TESTS_FAILED}"
    fi
    echo
    
    if [ "${TESTS_FAILED}" -eq 0 ]; then
        log_success "✅ All tests passed!"
        return 0
    else
        log_error "❌ Some tests failed"
        return 1
    fi
}

# Cleanup on exit
trap teardown_test_env EXIT

# Run tests
run_all_tests
exit $?
