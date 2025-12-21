#!/bin/sh
# Test suite for framework_install.sh
# Follows ATDD (Directive 016) and TDD (Directive 017) requirements
# Tests must pass before implementation is considered complete

set -e

# Resolve script path once at the beginning before any directory changes
SCRIPT_PATH="$(cd "$(dirname "$0")/.." && pwd)/framework_install.sh"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
setup_test_env() {
    TEST_DIR="${TMPDIR:-/tmp}/framework_install_test_$$"
    FRAMEWORK_CORE="$TEST_DIR/framework_core"
    PROJECT_ROOT="$TEST_DIR/project"
    MANIFEST_DIR="$TEST_DIR/META"
    
    mkdir -p "$FRAMEWORK_CORE"
    mkdir -p "$PROJECT_ROOT"
    mkdir -p "$MANIFEST_DIR"
    
    # Create a minimal MANIFEST.yml for testing
    cat > "$MANIFEST_DIR/MANIFEST.yml" <<'EOF'
framework:
  name: quickstart_agent-augmented-development
  version: "1.0.0"
  release_date: "2025-12-21"
  description: "Test framework"
EOF
}

cleanup_test_env() {
    if [ -n "$TEST_DIR" ] && [ -d "$TEST_DIR" ]; then
        rm -rf "$TEST_DIR"
    fi
}

assert_equals() {
    TESTS_RUN=$((TESTS_RUN + 1))
    expected="$1"
    actual="$2"
    test_name="$3"
    
    if [ "$expected" = "$actual" ]; then
        printf "${GREEN}✓${NC} %s\n" "$test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        printf "${RED}✗${NC} %s\n" "$test_name"
        printf "  Expected: %s\n" "$expected"
        printf "  Actual:   %s\n" "$actual"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_file_exists() {
    TESTS_RUN=$((TESTS_RUN + 1))
    filepath="$1"
    test_name="$2"
    
    if [ -f "$filepath" ]; then
        printf "${GREEN}✓${NC} %s\n" "$test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        printf "${RED}✗${NC} %s\n" "$test_name"
        printf "  File does not exist: %s\n" "$filepath"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_file_not_exists() {
    TESTS_RUN=$((TESTS_RUN + 1))
    filepath="$1"
    test_name="$2"
    
    if [ ! -f "$filepath" ]; then
        printf "${GREEN}✓${NC} %s\n" "$test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        printf "${RED}✗${NC} %s\n" "$test_name"
        printf "  File should not exist: %s\n" "$filepath"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_contains() {
    TESTS_RUN=$((TESTS_RUN + 1))
    haystack="$1"
    needle="$2"
    test_name="$3"
    
    case "$haystack" in
        *"$needle"*)
            printf "${GREEN}✓${NC} %s\n" "$test_name"
            TESTS_PASSED=$((TESTS_PASSED + 1))
            return 0
            ;;
        *)
            printf "${RED}✗${NC} %s\n" "$test_name"
            printf "  Expected to contain: %s\n" "$needle"
            printf "  Actual content: %s\n" "$haystack"
            TESTS_FAILED=$((TESTS_FAILED + 1))
            return 1
            ;;
    esac
}

# Test: Script exists and is executable
test_script_exists() {
    printf "\n${YELLOW}Test Suite: Script Validation${NC}\n"
    
    
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ -f "$SCRIPT_PATH" ]; then
        printf "${GREEN}✓${NC} Script file exists\n"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        printf "${RED}✗${NC} Script file exists\n"
        printf "  Expected at: %s\n" "$SCRIPT_PATH"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
    
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ -x "$SCRIPT_PATH" ]; then
        printf "${GREEN}✓${NC} Script is executable\n"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        printf "${RED}✗${NC} Script is executable\n"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Test: First-time installation
test_first_time_install() {
    printf "\n${YELLOW}Test Suite: First-Time Installation${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create test files in framework_core
    mkdir -p "$FRAMEWORK_CORE/.github/agents"
    echo "test content" > "$FRAMEWORK_CORE/.github/agents/test.md"
    mkdir -p "$FRAMEWORK_CORE/docs/templates"
    echo "template" > "$FRAMEWORK_CORE/docs/templates/sample.md"
    
    # Resolve script path to absolute before cd
    cd "$TEST_DIR"
    set +e
    output=$("$SCRIPT_PATH" "$PROJECT_ROOT" 2>&1)
    exit_code=$?
    set -e
    
    # Verify exit code
    assert_equals "0" "$exit_code" "Installation exits with code 0"
    
    # Verify files were copied
    assert_file_exists "$PROJECT_ROOT/.github/agents/test.md" "Framework file copied to project"
    assert_file_exists "$PROJECT_ROOT/docs/templates/sample.md" "Template file copied to project"
    
    # Verify metadata file created
    assert_file_exists "$PROJECT_ROOT/.framework_meta.yml" "Metadata file created"
    
    # Verify metadata content
    if [ -f "$PROJECT_ROOT/.framework_meta.yml" ]; then
        meta_content=$(cat "$PROJECT_ROOT/.framework_meta.yml")
        assert_contains "$meta_content" "framework_version" "Metadata contains version"
        assert_contains "$meta_content" "installed_at" "Metadata contains timestamp"
    fi
    
    # Verify summary output
    assert_contains "$output" "NEW:" "Output contains NEW count"
    assert_contains "$output" "Installation complete" "Output contains success message"
    
    cleanup_test_env
}

# Test: Existing installation detection
test_existing_installation_detected() {
    printf "\n${YELLOW}Test Suite: Existing Installation Detection${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create existing metadata file
    cat > "$PROJECT_ROOT/.framework_meta.yml" <<'EOF'
framework_version: "0.9.0"
installed_at: "2025-12-20T00:00:00Z"
EOF
    
    # Try to run installation again
    cd "$TEST_DIR"
    set +e
    output=$("$SCRIPT_PATH" "$PROJECT_ROOT" 2>&1)
    exit_code=$?
    set -e
    
    # Should refuse to install
    assert_equals "1" "$exit_code" "Installation fails when framework already exists"
    assert_contains "$output" "already installed" "Output warns about existing installation"
    
    cleanup_test_env
}

# Test: Skip existing files
test_skip_existing_files() {
    printf "\n${YELLOW}Test Suite: Skip Existing Files${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create test files in framework_core
    mkdir -p "$FRAMEWORK_CORE/.github/agents"
    echo "new content" > "$FRAMEWORK_CORE/.github/agents/test.md"
    
    # Create existing file with different content
    mkdir -p "$PROJECT_ROOT/.github/agents"
    echo "existing content" > "$PROJECT_ROOT/.github/agents/test.md"
    
    # Run installation
    cd "$TEST_DIR"
    output=$("$SCRIPT_PATH" "$PROJECT_ROOT" 2>&1) || true
    
    # Verify existing file was not overwritten
    actual_content=$(cat "$PROJECT_ROOT/.github/agents/test.md")
    assert_equals "existing content" "$actual_content" "Existing file not overwritten"
    
    # Verify output mentions skipped file
    assert_contains "$output" "SKIPPED:" "Output contains SKIPPED count"
    
    cleanup_test_env
}

# Test: Dry-run mode
test_dry_run_mode() {
    printf "\n${YELLOW}Test Suite: Dry-Run Mode${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create test files in framework_core
    mkdir -p "$FRAMEWORK_CORE/.github/agents"
    echo "test content" > "$FRAMEWORK_CORE/.github/agents/test.md"
    
    # Run in dry-run mode
    cd "$TEST_DIR"
    set +e
    output=$("$SCRIPT_PATH" --dry-run "$PROJECT_ROOT" 2>&1)
    exit_code=$?
    set -e
    
    # Verify exit code
    assert_equals "0" "$exit_code" "Dry-run exits with code 0"
    
    # Verify no files were actually copied
    assert_file_not_exists "$PROJECT_ROOT/.github/agents/test.md" "Files not copied in dry-run"
    assert_file_not_exists "$PROJECT_ROOT/.framework_meta.yml" "Metadata not created in dry-run"
    
    # Verify output indicates dry-run
    assert_contains "$output" "DRY RUN" "Output indicates dry-run mode"
    assert_contains "$output" "Would copy" "Output describes intended actions"
    
    cleanup_test_env
}

# Test: Directory creation
test_directory_creation() {
    printf "\n${YELLOW}Test Suite: Directory Creation${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create nested directory structure in framework_core
    mkdir -p "$FRAMEWORK_CORE/deep/nested/structure"
    echo "deep file" > "$FRAMEWORK_CORE/deep/nested/structure/file.txt"
    
    # Run installation
    cd "$TEST_DIR"
    set +e
    "$SCRIPT_PATH" "$PROJECT_ROOT" > /dev/null 2>&1
    set -e
    
    # Verify nested directory was created
    assert_file_exists "$PROJECT_ROOT/deep/nested/structure/file.txt" "Nested directories created"
    
    cleanup_test_env
}

# Test: Handling filenames with spaces
test_filenames_with_spaces() {
    printf "\n${YELLOW}Test Suite: Filenames with Spaces${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create file with spaces in name
    mkdir -p "$FRAMEWORK_CORE/docs"
    echo "content" > "$FRAMEWORK_CORE/docs/file with spaces.md"
    
    # Run installation
    cd "$TEST_DIR"
    set +e
    "$SCRIPT_PATH" "$PROJECT_ROOT" > /dev/null 2>&1
    set -e
    
    # Verify file with spaces was copied
    assert_file_exists "$PROJECT_ROOT/docs/file with spaces.md" "File with spaces copied correctly"
    
    cleanup_test_env
}

# Test: Missing PROJECT_ROOT parameter
test_missing_parameter() {
    printf "\n${YELLOW}Test Suite: Parameter Validation${NC}\n"
    
    set +e
    output=$("$SCRIPT_PATH" 2>&1)
    exit_code=$?
    set -e
    
    # Should fail with non-zero exit code
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ "$exit_code" -ne 0 ]; then
        printf "${GREEN}✓${NC} Missing parameter causes failure\n"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        printf "${RED}✗${NC} Missing parameter causes failure\n"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    
    assert_contains "$output" "Usage:" "Output shows usage message"
}

# Test: POSIX compliance (no bashisms)
test_posix_compliance() {
    printf "\n${YELLOW}Test Suite: POSIX Compliance${NC}\n"
    
    
    # Check shebang
    TESTS_RUN=$((TESTS_RUN + 1))
    first_line=$(head -n 1 "$SCRIPT_PATH")
    if [ "$first_line" = "#!/bin/sh" ] || [ "$first_line" = "#!/usr/bin/env sh" ]; then
        printf "${GREEN}✓${NC} Script uses POSIX shebang\n"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        printf "${RED}✗${NC} Script uses POSIX shebang\n"
        printf "  Found: %s\n" "$first_line"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    
    # Check for bashisms (basic patterns)
    TESTS_RUN=$((TESTS_RUN + 1))
    if grep -q '\[\[' "$SCRIPT_PATH" 2>/dev/null; then
        printf "${RED}✗${NC} Script avoids [[ ]] bashism\n"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    else
        printf "${GREEN}✓${NC} Script avoids [[ ]] bashism\n"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    fi
    
    TESTS_RUN=$((TESTS_RUN + 1))
    if grep -q 'function ' "$SCRIPT_PATH" 2>/dev/null; then
        printf "${RED}✗${NC} Script avoids 'function' keyword\n"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    else
        printf "${GREEN}✓${NC} Script avoids 'function' keyword\n"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    fi
}

# Test: Summary report format
test_summary_report_format() {
    printf "\n${YELLOW}Test Suite: Summary Report Format${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create mixed scenario: some new, some existing
    mkdir -p "$FRAMEWORK_CORE/docs"
    echo "new1" > "$FRAMEWORK_CORE/docs/new1.md"
    echo "new2" > "$FRAMEWORK_CORE/docs/new2.md"
    
    mkdir -p "$PROJECT_ROOT/docs"
    echo "existing" > "$PROJECT_ROOT/docs/existing.md"
    echo "same" > "$FRAMEWORK_CORE/docs/existing.md"
    
    # Run installation
    cd "$TEST_DIR"
    set +e
    output=$("$SCRIPT_PATH" "$PROJECT_ROOT" 2>&1)
    set -e
    
    # Verify summary format
    assert_contains "$output" "NEW:" "Summary includes NEW count"
    assert_contains "$output" "SKIPPED:" "Summary includes SKIPPED count"
    
    cleanup_test_env
}

# Main execution
main() {
    printf "${YELLOW}=== Framework Install Script Test Suite ===${NC}\n"
    printf "Following ATDD (Directive 016) and TDD (Directive 017)\n"
    
    # Run all test suites
    test_script_exists
    test_missing_parameter
    test_posix_compliance
    test_first_time_install
    test_existing_installation_detected
    test_skip_existing_files
    test_dry_run_mode
    test_directory_creation
    test_filenames_with_spaces
    test_summary_report_format
    
    # Print summary
    printf "\n${YELLOW}=== Test Summary ===${NC}\n"
    printf "Total tests run:    %d\n" "$TESTS_RUN"
    printf "${GREEN}Tests passed:       %d${NC}\n" "$TESTS_PASSED"
    if [ "$TESTS_FAILED" -gt 0 ]; then
        printf "${RED}Tests failed:       %d${NC}\n" "$TESTS_FAILED"
        exit 1
    else
        printf "Tests failed:       %d\n" "$TESTS_FAILED"
        printf "\n${GREEN}All tests passed!${NC}\n"
        exit 0
    fi
}

# Run tests
main "$@"
