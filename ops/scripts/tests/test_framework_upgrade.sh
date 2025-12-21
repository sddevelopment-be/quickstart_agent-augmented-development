#!/bin/sh
# Test suite for framework_upgrade.sh
# Follows ATDD (Directive 016) and TDD (Directive 017) requirements
# Tests must pass before implementation is considered complete

set -e

# Resolve script path once at the beginning before any directory changes
SCRIPT_PATH="$(cd "$(dirname "$0")/.." && pwd)/framework_upgrade.sh"

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
    TEST_DIR="${TMPDIR:-/tmp}/framework_upgrade_test_$$"
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
  version: "1.1.0"
  release_date: "2025-12-21"
  description: "Test framework upgrade"
EOF

    # Create minimal metadata file in project (simulating prior installation)
    cat > "$PROJECT_ROOT/.framework_meta.yml" <<'EOF'
framework_version: "1.0.0"
installed_at: "2025-12-20T00:00:00Z"
source_release: "quickstart-framework-1.0.0.zip"
files_installed: 5
files_skipped: 0
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

# Helper to compute SHA256 checksum portably
compute_checksum() {
    filepath="$1"
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$filepath" | cut -d' ' -f1
    elif command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$filepath" | cut -d' ' -f1
    else
        echo "ERROR: No SHA256 tool available" >&2
        return 1
    fi
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

# Test: No framework metadata (should refuse upgrade)
test_no_metadata_refuses_upgrade() {
    printf "\n${YELLOW}Test Suite: Metadata Validation${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Remove metadata file
    rm -f "$PROJECT_ROOT/.framework_meta.yml"
    
    # Try to upgrade
    cd "$TEST_DIR"
    set +e
    output=$("$SCRIPT_PATH" "$PROJECT_ROOT" 2>&1)
    exit_code=$?
    set -e
    
    # Should refuse to upgrade
    assert_equals "1" "$exit_code" "Upgrade refuses when no metadata found"
    assert_contains "$output" "not installed" "Error message mentions missing installation"
    
    cleanup_test_env
}

# Test: All files unchanged (identical checksums)
test_all_files_unchanged() {
    printf "\n${YELLOW}Test Suite: All Files Unchanged${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create identical files in framework_core and project
    mkdir -p "$FRAMEWORK_CORE/.github/agents"
    echo "test content" > "$FRAMEWORK_CORE/.github/agents/test.md"
    
    mkdir -p "$PROJECT_ROOT/.github/agents"
    echo "test content" > "$PROJECT_ROOT/.github/agents/test.md"
    
    # Run upgrade
    cd "$TEST_DIR"
    set +e
    output=$("$SCRIPT_PATH" "$PROJECT_ROOT" 2>&1)
    exit_code=$?
    set -e
    
    # Verify exit code
    assert_equals "0" "$exit_code" "Upgrade succeeds with no changes"
    
    # Verify output mentions UNCHANGED
    assert_contains "$output" "UNCHANGED:" "Output contains UNCHANGED count"
    
    # Verify no .framework-new files created
    assert_file_not_exists "$PROJECT_ROOT/.github/agents/test.md.framework-new" "No .framework-new file for identical file"
    
    # Verify upgrade-report.txt created
    assert_file_exists "$PROJECT_ROOT/upgrade-report.txt" "upgrade-report.txt created"
    
    # Verify metadata updated
    if [ -f "$PROJECT_ROOT/.framework_meta.yml" ]; then
        meta_content=$(cat "$PROJECT_ROOT/.framework_meta.yml")
        assert_contains "$meta_content" '1.1.0' "Metadata updated to new version"
    fi
    
    cleanup_test_env
}

# Test: New files added
test_new_files_added() {
    printf "\n${YELLOW}Test Suite: New Files Added${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create new file in framework_core only
    mkdir -p "$FRAMEWORK_CORE/docs/templates"
    echo "new template content" > "$FRAMEWORK_CORE/docs/templates/new.md"
    
    # Run upgrade
    cd "$TEST_DIR"
    output=$("$SCRIPT_PATH" "$PROJECT_ROOT" 2>&1) || true
    
    # Verify file was copied
    assert_file_exists "$PROJECT_ROOT/docs/templates/new.md" "New file copied to project"
    
    # Verify content matches
    if [ -f "$PROJECT_ROOT/docs/templates/new.md" ]; then
        actual_content=$(cat "$PROJECT_ROOT/docs/templates/new.md")
        assert_equals "new template content" "$actual_content" "New file content matches"
    fi
    
    # Verify output mentions NEW
    assert_contains "$output" "NEW:" "Output contains NEW count"
    
    cleanup_test_env
}

# Test: Conflicting files create .framework-new
test_conflicting_files_create_framework_new() {
    printf "\n${YELLOW}Test Suite: Conflicting Files${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create different content in framework_core vs project
    mkdir -p "$FRAMEWORK_CORE/.github/agents"
    echo "new version content" > "$FRAMEWORK_CORE/.github/agents/conflict.md"
    
    mkdir -p "$PROJECT_ROOT/.github/agents"
    echo "local customization" > "$PROJECT_ROOT/.github/agents/conflict.md"
    
    # Run upgrade
    cd "$TEST_DIR"
    output=$("$SCRIPT_PATH" "$PROJECT_ROOT" 2>&1) || true
    
    # Verify original file unchanged
    if [ -f "$PROJECT_ROOT/.github/agents/conflict.md" ]; then
        actual_content=$(cat "$PROJECT_ROOT/.github/agents/conflict.md")
        assert_equals "local customization" "$actual_content" "Original file not modified"
    fi
    
    # Verify .framework-new created with new content
    assert_file_exists "$PROJECT_ROOT/.github/agents/conflict.md.framework-new" ".framework-new file created for conflict"
    
    if [ -f "$PROJECT_ROOT/.github/agents/conflict.md.framework-new" ]; then
        new_content=$(cat "$PROJECT_ROOT/.github/agents/conflict.md.framework-new")
        assert_equals "new version content" "$new_content" ".framework-new contains new version"
    fi
    
    # Verify output mentions CONFLICT
    assert_contains "$output" "CONFLICT:" "Output contains CONFLICT count"
    
    cleanup_test_env
}

# Test: Dry-run mode (no modifications)
test_dry_run_mode() {
    printf "\n${YELLOW}Test Suite: Dry-Run Mode${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create new file in framework_core
    mkdir -p "$FRAMEWORK_CORE/docs"
    echo "new doc" > "$FRAMEWORK_CORE/docs/newfile.md"
    
    # Create conflict
    mkdir -p "$FRAMEWORK_CORE/.github/agents"
    echo "new version" > "$FRAMEWORK_CORE/.github/agents/test.md"
    mkdir -p "$PROJECT_ROOT/.github/agents"
    echo "old version" > "$PROJECT_ROOT/.github/agents/test.md"
    
    # Run upgrade in dry-run mode
    cd "$TEST_DIR"
    output=$("$SCRIPT_PATH" --dry-run "$PROJECT_ROOT" 2>&1) || true
    
    # Verify no files copied
    assert_file_not_exists "$PROJECT_ROOT/docs/newfile.md" "Dry-run does not copy new files"
    
    # Verify no .framework-new files created
    assert_file_not_exists "$PROJECT_ROOT/.github/agents/test.md.framework-new" "Dry-run does not create .framework-new"
    
    # Verify metadata not updated
    if [ -f "$PROJECT_ROOT/.framework_meta.yml" ]; then
        meta_content=$(cat "$PROJECT_ROOT/.framework_meta.yml")
        assert_contains "$meta_content" '1.0.0' "Metadata not updated in dry-run"
    fi
    
    # Verify output indicates dry-run
    assert_contains "$output" "DRY RUN" "Output indicates dry-run mode"
    assert_contains "$output" "Would copy" "Output describes actions without executing"
    
    cleanup_test_env
}

# Test: Local directory never touched
test_local_directory_untouched() {
    printf "\n${YELLOW}Test Suite: Local Directory Protection${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create file in framework_core local directory (should be filtered)
    mkdir -p "$FRAMEWORK_CORE/local/custom"
    echo "custom content" > "$FRAMEWORK_CORE/local/custom/agent.md"
    
    # Create existing local file in project
    mkdir -p "$PROJECT_ROOT/local/custom"
    echo "protected content" > "$PROJECT_ROOT/local/custom/agent.md"
    
    # Run upgrade
    cd "$TEST_DIR"
    output=$("$SCRIPT_PATH" "$PROJECT_ROOT" 2>&1) || true
    
    # Verify local file unchanged
    if [ -f "$PROJECT_ROOT/local/custom/agent.md" ]; then
        actual_content=$(cat "$PROJECT_ROOT/local/custom/agent.md")
        assert_equals "protected content" "$actual_content" "Local file not touched by upgrade"
    fi
    
    # Verify no .framework-new created for local files
    assert_file_not_exists "$PROJECT_ROOT/local/custom/agent.md.framework-new" "No .framework-new for local files"
    
    cleanup_test_env
}

# Test: Upgrade report format
test_upgrade_report_format() {
    printf "\n${YELLOW}Test Suite: Upgrade Report Format${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create mix of scenarios
    mkdir -p "$FRAMEWORK_CORE/docs"
    echo "new" > "$FRAMEWORK_CORE/docs/new.md"
    echo "unchanged" > "$FRAMEWORK_CORE/docs/unchanged.md"
    echo "new version" > "$FRAMEWORK_CORE/docs/conflict.md"
    
    mkdir -p "$PROJECT_ROOT/docs"
    echo "unchanged" > "$PROJECT_ROOT/docs/unchanged.md"
    echo "old version" > "$PROJECT_ROOT/docs/conflict.md"
    
    # Run upgrade
    cd "$TEST_DIR"
    "$SCRIPT_PATH" "$PROJECT_ROOT" >/dev/null 2>&1 || true
    
    # Verify upgrade-report.txt exists
    assert_file_exists "$PROJECT_ROOT/upgrade-report.txt" "upgrade-report.txt created"
    
    # Verify report content structure
    if [ -f "$PROJECT_ROOT/upgrade-report.txt" ]; then
        report_content=$(cat "$PROJECT_ROOT/upgrade-report.txt")
        assert_contains "$report_content" "NEW:" "Report contains NEW count"
        assert_contains "$report_content" "UNCHANGED:" "Report contains UNCHANGED count"
        assert_contains "$report_content" "CONFLICT:" "Report contains CONFLICT count"
        assert_contains "$report_content" "docs/new.md" "Report lists specific files"
    fi
    
    cleanup_test_env
}

# Test: Checksum accuracy
test_checksum_accuracy() {
    printf "\n${YELLOW}Test Suite: Checksum Comparison${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create file with same content
    mkdir -p "$FRAMEWORK_CORE/test"
    echo "identical content" > "$FRAMEWORK_CORE/test/file.txt"
    
    mkdir -p "$PROJECT_ROOT/test"
    echo "identical content" > "$PROJECT_ROOT/test/file.txt"
    
    # Compute checksums manually
    checksum1=$(compute_checksum "$FRAMEWORK_CORE/test/file.txt")
    checksum2=$(compute_checksum "$PROJECT_ROOT/test/file.txt")
    
    # Verify checksums match
    assert_equals "$checksum1" "$checksum2" "Identical files have identical checksums"
    
    # Run upgrade
    cd "$TEST_DIR"
    "$SCRIPT_PATH" "$PROJECT_ROOT" >/dev/null 2>&1 || true
    
    # Verify file marked as UNCHANGED
    if [ -f "$PROJECT_ROOT/upgrade-report.txt" ]; then
        report=$(cat "$PROJECT_ROOT/upgrade-report.txt")
        assert_contains "$report" "UNCHANGED: 1" "Identical file detected by checksum"
    fi
    
    cleanup_test_env
}

# Test: Special characters in filenames
test_special_characters_in_filenames() {
    printf "\n${YELLOW}Test Suite: Special Characters${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create files with spaces and special chars
    mkdir -p "$FRAMEWORK_CORE/docs"
    echo "content" > "$FRAMEWORK_CORE/docs/file with spaces.md"
    echo "content" > "$FRAMEWORK_CORE/docs/file-with-dashes.md"
    
    # Run upgrade
    cd "$TEST_DIR"
    set +e
    "$SCRIPT_PATH" "$PROJECT_ROOT" >/dev/null 2>&1
    exit_code=$?
    set -e
    
    # Verify files copied correctly
    assert_file_exists "$PROJECT_ROOT/docs/file with spaces.md" "File with spaces handled"
    assert_file_exists "$PROJECT_ROOT/docs/file-with-dashes.md" "File with dashes handled"
    
    assert_equals "0" "$exit_code" "Script handles special characters"
    
    cleanup_test_env
}

# Test: Nested directory structure
test_nested_directory_structure() {
    printf "\n${YELLOW}Test Suite: Nested Directories${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create deeply nested structure
    mkdir -p "$FRAMEWORK_CORE/a/b/c/d"
    echo "deep content" > "$FRAMEWORK_CORE/a/b/c/d/deep.md"
    
    # Run upgrade
    cd "$TEST_DIR"
    "$SCRIPT_PATH" "$PROJECT_ROOT" >/dev/null 2>&1 || true
    
    # Verify nested file copied
    assert_file_exists "$PROJECT_ROOT/a/b/c/d/deep.md" "Deeply nested file copied"
    
    # Verify content
    if [ -f "$PROJECT_ROOT/a/b/c/d/deep.md" ]; then
        actual=$(cat "$PROJECT_ROOT/a/b/c/d/deep.md")
        assert_equals "deep content" "$actual" "Nested file content correct"
    fi
    
    cleanup_test_env
}

# Test: Empty directories not created
test_empty_directories_not_created() {
    printf "\n${YELLOW}Test Suite: Empty Directories${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create empty directory in framework_core
    mkdir -p "$FRAMEWORK_CORE/empty_dir"
    
    # Create file in another directory
    mkdir -p "$FRAMEWORK_CORE/docs"
    echo "content" > "$FRAMEWORK_CORE/docs/file.md"
    
    # Run upgrade
    cd "$TEST_DIR"
    "$SCRIPT_PATH" "$PROJECT_ROOT" >/dev/null 2>&1 || true
    
    # Verify empty directory not created
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ ! -d "$PROJECT_ROOT/empty_dir" ]; then
        printf "${GREEN}✓${NC} Empty directory not created\n"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        printf "${RED}✗${NC} Empty directory not created\n"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    
    cleanup_test_env
}

# Test: Multiple conflicts in single run
test_multiple_conflicts() {
    printf "\n${YELLOW}Test Suite: Multiple Conflicts${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Create multiple conflicts
    mkdir -p "$FRAMEWORK_CORE/docs"
    echo "new1" > "$FRAMEWORK_CORE/docs/file1.md"
    echo "new2" > "$FRAMEWORK_CORE/docs/file2.md"
    echo "new3" > "$FRAMEWORK_CORE/docs/file3.md"
    
    mkdir -p "$PROJECT_ROOT/docs"
    echo "old1" > "$PROJECT_ROOT/docs/file1.md"
    echo "old2" > "$PROJECT_ROOT/docs/file2.md"
    echo "old3" > "$PROJECT_ROOT/docs/file3.md"
    
    # Run upgrade
    cd "$TEST_DIR"
    "$SCRIPT_PATH" "$PROJECT_ROOT" >/dev/null 2>&1 || true
    
    # Verify all .framework-new files created
    assert_file_exists "$PROJECT_ROOT/docs/file1.md.framework-new" "Conflict 1 creates .framework-new"
    assert_file_exists "$PROJECT_ROOT/docs/file2.md.framework-new" "Conflict 2 creates .framework-new"
    assert_file_exists "$PROJECT_ROOT/docs/file3.md.framework-new" "Conflict 3 creates .framework-new"
    
    # Verify report shows correct count
    if [ -f "$PROJECT_ROOT/upgrade-report.txt" ]; then
        report=$(cat "$PROJECT_ROOT/upgrade-report.txt")
        assert_contains "$report" "CONFLICT: 3" "Report shows 3 conflicts"
    fi
    
    cleanup_test_env
}

# Test: Help flag displays usage
test_help_flag() {
    printf "\n${YELLOW}Test Suite: Help Documentation${NC}\n"
    
    set +e
    output=$("$SCRIPT_PATH" --help 2>&1)
    exit_code=$?
    set -e
    
    # Verify help displays and exits 0
    assert_equals "0" "$exit_code" "Help flag exits with code 0"
    assert_contains "$output" "Usage:" "Help shows usage information"
    assert_contains "$output" "--dry-run" "Help documents dry-run option"
}

# Test: Invalid parameters
test_invalid_parameters() {
    printf "\n${YELLOW}Test Suite: Parameter Validation${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Test missing PROJECT_ROOT
    set +e
    output=$("$SCRIPT_PATH" 2>&1)
    exit_code=$?
    set -e
    
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ "$exit_code" -ne 0 ]; then
        printf "${GREEN}✓${NC} Missing PROJECT_ROOT causes non-zero exit\n"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        printf "${RED}✗${NC} Missing PROJECT_ROOT causes non-zero exit\n"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    
    assert_contains "$output" "required" "Error message mentions required parameter"
    
    cleanup_test_env
}

# Test: Exit codes are correct
test_exit_codes() {
    printf "\n${YELLOW}Test Suite: Exit Codes${NC}\n"
    
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Test successful upgrade (exit 0)
    mkdir -p "$FRAMEWORK_CORE/docs"
    echo "content" > "$FRAMEWORK_CORE/docs/test.md"
    
    cd "$TEST_DIR"
    set +e
    "$SCRIPT_PATH" "$PROJECT_ROOT" >/dev/null 2>&1
    exit_code=$?
    set -e
    
    assert_equals "0" "$exit_code" "Successful upgrade exits with code 0"
    
    cleanup_test_env
}

# Run all tests
run_all_tests() {
    echo "========================================"
    echo "Framework Upgrade Script - Test Suite"
    echo "========================================"
    
    test_script_exists
    test_no_metadata_refuses_upgrade
    test_all_files_unchanged
    test_new_files_added
    test_conflicting_files_create_framework_new
    test_dry_run_mode
    test_local_directory_untouched
    test_upgrade_report_format
    test_checksum_accuracy
    test_special_characters_in_filenames
    test_nested_directory_structure
    test_empty_directories_not_created
    test_multiple_conflicts
    test_help_flag
    test_invalid_parameters
    test_exit_codes
    
    # Print summary
    echo ""
    echo "========================================"
    echo "Test Summary"
    echo "========================================"
    printf "Total tests:  %d\n" "$TESTS_RUN"
    printf "${GREEN}Passed:       %d${NC}\n" "$TESTS_PASSED"
    printf "${RED}Failed:       %d${NC}\n" "$TESTS_FAILED"
    echo "========================================"
    
    if [ $TESTS_FAILED -gt 0 ]; then
        exit 1
    fi
    
    exit 0
}

# Execute tests
run_all_tests
