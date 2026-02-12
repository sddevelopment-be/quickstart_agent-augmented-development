#!/usr/bin/env python3
"""
Test suite for agent-friendly error reporting system.

Tests the error summary generator with various error formats
and validates JSON/Markdown output structure.

Context: Directive 016 (ATDD), Directive 017 (TDD)
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

# Add repo root to path
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(REPO_ROOT / "tools" / "scripts"))

# Import needs to be after path setup, and we need to import the module properly
import importlib.util
import sys

spec = importlib.util.spec_from_file_location(
    "generate_error_summary",
    REPO_ROOT / "tools" / "scripts" / "generate-error-summary.py",
)
generate_error_summary = importlib.util.module_from_spec(spec)
# FIX: Register module in sys.modules BEFORE executing to avoid dataclass errors
sys.modules[spec.name] = generate_error_summary
spec.loader.exec_module(generate_error_summary)

from generate_error_summary import (
    ErrorLocation,
    ErrorParser,
    ErrorSuggestion,
    ErrorSummary,
    ValidationError,
)


def test_error_location_dataclass():
    """Test ErrorLocation dataclass creation."""
    location = ErrorLocation(
        file_path="work/test.yaml",
        line_number=5,
        column_number=10,
        context_lines=["status: foo"],
    )

    assert location.file_path == "work/test.yaml"
    assert location.line_number == 5
    assert location.column_number == 10
    assert len(location.context_lines) == 1


def test_error_suggestion_dataclass():
    """Test ErrorSuggestion dataclass creation."""
    suggestion = ErrorSuggestion(
        description="Update status field",
        diff=None,
        command="vim work/test.yaml",
    )

    assert suggestion.description == "Update status field"
    assert suggestion.command == "vim work/test.yaml"


def test_validation_error_creation():
    """Test ValidationError creation with all fields."""
    location = ErrorLocation(file_path="work/test.yaml", line_number=5)
    suggestion = ErrorSuggestion(description="Fix status field")

    error = ValidationError(
        error_id="test_001",
        error_type="validation_failure",
        severity="error",
        message="Invalid status value",
        validator="task-schema",
        timestamp="2025-02-11T20:00:00Z",
        location=location,
        suggestions=[suggestion],
        raw_output="❌ work/test.yaml: invalid status",
    )

    assert error.error_id == "test_001"
    assert error.severity == "error"
    assert error.location.file_path == "work/test.yaml"
    assert len(error.suggestions) == 1


def test_validation_error_to_dict():
    """Test ValidationError serialization to dict."""
    location = ErrorLocation(file_path="work/test.yaml", line_number=5)
    error = ValidationError(
        error_id="test_001",
        error_type="validation_failure",
        severity="error",
        message="Invalid status",
        validator="task-schema",
        timestamp="2025-02-11T20:00:00Z",
        location=location,
    )

    error_dict = error.to_dict()

    assert error_dict["error_id"] == "test_001"
    assert error_dict["location"]["file_path"] == "work/test.yaml"
    assert error_dict["location"]["line_number"] == 5


def test_validation_error_to_github_annotation():
    """Test GitHub Actions annotation format."""
    location = ErrorLocation(file_path="work/test.yaml", line_number=5)
    error = ValidationError(
        error_id="test_001",
        error_type="validation_failure",
        severity="error",
        message="Invalid status",
        validator="task-schema",
        timestamp="2025-02-11T20:00:00Z",
        location=location,
    )

    annotation = error.to_github_annotation()

    assert "::error" in annotation
    assert "file=work/test.yaml" in annotation
    assert "line=5" in annotation
    assert "Invalid status" in annotation


def test_validation_error_to_markdown():
    """Test Markdown formatting."""
    location = ErrorLocation(file_path="work/test.yaml", line_number=5)
    suggestion = ErrorSuggestion(
        description="Update status field",
        command="vim work/test.yaml",
    )
    error = ValidationError(
        error_id="test_001",
        error_type="validation_failure",
        severity="error",
        message="Invalid status",
        validator="task-schema",
        timestamp="2025-02-11T20:00:00Z",
        location=location,
        suggestions=[suggestion],
    )

    markdown = error.to_markdown()

    assert "❌" in markdown
    assert "validation_failure" in markdown
    assert "work/test.yaml" in markdown
    assert "Line 5" in markdown
    assert "Update status field" in markdown


def test_error_summary_creation():
    """Test ErrorSummary creation and error aggregation."""
    summary = ErrorSummary(
        workflow="Test Workflow",
        job="test-job",
        run_id="12345",
    )

    error = ValidationError(
        error_id="test_001",
        error_type="validation_failure",
        severity="error",
        message="Test error",
        validator="test-validator",
        timestamp="2025-02-11T20:00:00Z",
    )

    summary.add_error(error)

    assert summary.error_count() == 1
    assert summary.warning_count() == 0
    assert len(summary.errors) == 1


def test_error_summary_counts():
    """Test error and warning counting."""
    summary = ErrorSummary(workflow="Test", job="test")

    # Add 2 errors
    for i in range(2):
        summary.add_error(
            ValidationError(
                error_id=f"error_{i}",
                error_type="error",
                severity="error",
                message=f"Error {i}",
                validator="test",
                timestamp="2025-02-11T20:00:00Z",
            )
        )

    # Add 1 warning
    summary.add_error(
        ValidationError(
            error_id="warning_1",
            error_type="warning",
            severity="warning",
            message="Warning 1",
            validator="test",
            timestamp="2025-02-11T20:00:00Z",
        )
    )

    assert summary.error_count() == 2
    assert summary.warning_count() == 1


def test_error_summary_to_json():
    """Test JSON serialization."""
    summary = ErrorSummary(workflow="Test", job="test")
    summary.add_error(
        ValidationError(
            error_id="test_001",
            error_type="validation_failure",
            severity="error",
            message="Test error",
            validator="test",
            timestamp="2025-02-11T20:00:00Z",
        )
    )

    json_str = summary.to_json()
    parsed = json.loads(json_str)

    assert parsed["workflow"] == "Test"
    assert parsed["job"] == "test"
    assert parsed["summary"]["total_errors"] == 1
    assert len(parsed["errors"]) == 1


def test_error_summary_to_markdown():
    """Test Markdown summary generation."""
    summary = ErrorSummary(workflow="Test", job="test")
    summary.add_error(
        ValidationError(
            error_id="test_001",
            error_type="validation_failure",
            severity="error",
            message="Test error",
            validator="test",
            timestamp="2025-02-11T20:00:00Z",
        )
    )

    markdown = summary.to_markdown()

    assert "# 🔍 Error Summary: Test" in markdown
    assert "**Job:** test" in markdown
    assert "❌ **Errors:** 1" in markdown
    assert "## Issues by Validator" in markdown


def test_error_parser_basic_line():
    """Test parsing basic error line."""
    line = "❌ work/test.yaml: invalid status 'foo'"
    error = ErrorParser.parse_validation_line(line, "test-validator")

    assert error is not None
    assert error.severity == "error"
    assert "invalid status" in error.message
    assert error.validator == "test-validator"


def test_error_parser_warning_line():
    """Test parsing warning line."""
    line = "⚠️ Agent 'test' missing directory"
    error = ErrorParser.parse_validation_line(line, "test-validator")

    assert error is not None
    assert error.severity == "warning"
    assert "missing directory" in error.message


def test_error_parser_with_file_path():
    """Test parsing error with file path."""
    # Create a temporary file to test path detection
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        temp_path = f.name
        line = f"❌ {temp_path}: invalid field"

        error = ErrorParser.parse_validation_line(line, "test-validator")

        # Cleanup
        Path(temp_path).unlink()

        assert error is not None
        assert error.location is not None


def test_error_parser_python_output():
    """Test parsing Python validator output."""
    output = """
❌ work/test1.yaml: invalid status 'foo'
❌ work/test2.yaml: missing required field: agent
⚠️ work/test3.yaml: deprecated field usage
    """

    errors = ErrorParser.parse_python_validator_output(output, "task-schema")

    assert len(errors) == 3
    assert errors[0].severity == "error"
    assert errors[2].severity == "warning"


def test_error_parser_shell_output():
    """Test parsing shell validator output."""
    output = """
❗️ Missing required directory: work/collaboration
❗️ Missing required directory: work/reports
    """

    errors = ErrorParser.parse_shell_validator_output(output, "work-structure")

    assert len(errors) == 2
    assert all(e.severity == "error" for e in errors)
    assert all(e.validator == "work-structure" for e in errors)


def test_end_to_end_cli():
    """Test complete CLI execution."""
    # Create test input
    test_input = "❌ work/test.yaml: invalid status 'foo'\n⚠️ Test warning"

    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.txt"
        json_file = Path(tmpdir) / "output.json"
        md_file = Path(tmpdir) / "output.md"

        input_file.write_text(test_input)

        # Run CLI
        script_path = REPO_ROOT / "tools" / "scripts" / "generate-error-summary.py"
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--workflow",
                "Test",
                "--job",
                "test",
                "--validator",
                "test-validator",
                "--input",
                str(input_file),
                "--output-json",
                str(json_file),
                "--output-markdown",
                str(md_file),
            ],
            capture_output=True,
            text=True,
        )

        # Verify files created
        assert json_file.exists(), f"JSON file not created. stderr: {result.stderr}"
        assert md_file.exists(), "Markdown file not created"

        # Verify JSON structure
        with open(json_file) as f:
            data = json.load(f)

        assert data["workflow"] == "Test"
        assert data["summary"]["total_errors"] == 1
        assert data["summary"]["total_warnings"] == 1

        # Verify Markdown content
        md_content = md_file.read_text()
        assert "Error Summary" in md_content
        assert "test-validator" in md_content


def run_tests():
    """Run all tests."""
    tests = [
        test_error_location_dataclass,
        test_error_suggestion_dataclass,
        test_validation_error_creation,
        test_validation_error_to_dict,
        test_validation_error_to_github_annotation,
        test_validation_error_to_markdown,
        test_error_summary_creation,
        test_error_summary_counts,
        test_error_summary_to_json,
        test_error_summary_to_markdown,
        test_error_parser_basic_line,
        test_error_parser_warning_line,
        test_error_parser_with_file_path,
        test_error_parser_python_output,
        test_error_parser_shell_output,
        test_end_to_end_cli,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"💥 {test.__name__}: {e}")
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Tests: {passed + failed} | Passed: {passed} | Failed: {failed}")
    print(f"{'=' * 60}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
