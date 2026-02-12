"""
Unit tests for task validator domain service.

Tests the validation logic in src.domain.collaboration.task_validator,
ensuring all validation rules are properly enforced.
"""

from __future__ import annotations

from src.domain.collaboration.task_validator import (
    is_iso8601_utc,
    suggest_timestamp_fix,
    validate_task,
)


class TestTimestampValidation:
    """Test timestamp validation helpers."""

    def test_is_iso8601_utc_valid(self):
        """Test that valid ISO8601 UTC timestamps are accepted."""
        assert is_iso8601_utc("2025-11-30T12:00:00Z") is True
        assert is_iso8601_utc("2026-02-12T08:30:15Z") is True

    def test_is_iso8601_utc_missing_z_suffix(self):
        """Test that timestamps without Z suffix are rejected."""
        assert is_iso8601_utc("2025-11-30T12:00:00") is False
        assert is_iso8601_utc("2025-11-30T12:00:00+00:00") is False

    def test_is_iso8601_utc_invalid_format(self):
        """Test that invalid timestamp formats are rejected."""
        # Space instead of T separator
        assert is_iso8601_utc("2025-11-30 12:00:00Z") is False
        # Invalid string
        assert is_iso8601_utc("not-a-timestamp") is False
        # Empty string
        assert is_iso8601_utc("") is False

    def test_is_iso8601_utc_non_string(self):
        """Test that non-string values are rejected."""
        assert is_iso8601_utc(12345) is False
        assert is_iso8601_utc(None) is False

    def test_suggest_timestamp_fix_space_to_t(self):
        """Test fixing space separator to T."""
        result = suggest_timestamp_fix("2026-02-09 04:40:00+00:00")
        assert result == "2026-02-09T04:40:00Z"

    def test_suggest_timestamp_fix_offset_to_z(self):
        """Test fixing timezone offset to Z."""
        result = suggest_timestamp_fix("2026-02-09T04:40:00+00:00")
        assert result == "2026-02-09T04:40:00Z"

    def test_suggest_timestamp_fix_missing_z(self):
        """Test adding missing Z suffix."""
        result = suggest_timestamp_fix("2026-02-09T04:40:00")
        assert result == "2026-02-09T04:40:00Z"


class TestRequiredFields:
    """Test validation of required task fields."""

    def test_valid_minimal_task(self):
        """Test that minimal valid task passes validation."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
        }
        errors = validate_task(task)
        assert len(errors) == 0

    def test_missing_id_field(self):
        """Test that missing id field is caught."""
        task = {
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
        }
        errors = validate_task(task)
        assert any("missing required field: id" in e for e in errors)

    def test_missing_agent_field(self):
        """Test that missing agent field is caught."""
        task = {
            "id": "test-task-1",
            "status": "new",
            "artefacts": [],
        }
        errors = validate_task(task)
        assert any("missing required field: agent" in e for e in errors)

    def test_invalid_status_value(self):
        """Test that invalid status values are rejected."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "invalid-status",
            "artefacts": [],
        }
        errors = validate_task(task)
        assert any("invalid status" in e for e in errors)

    def test_artefacts_not_list(self):
        """Test that artefacts must be a list."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": "not-a-list",
        }
        errors = validate_task(task)
        assert any("artefacts/artifacts must be a list" in e for e in errors)

    def test_artefacts_non_string_entries(self):
        """Test that artefacts entries must be strings."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": ["valid.md", 123, "another.md"],
        }
        errors = validate_task(task)
        assert any("artefacts/artifacts entries must be strings" in e for e in errors)


class TestFilenameValidation:
    """Test filename/id alignment validation."""

    def test_id_matches_filename_stem(self):
        """Test that matching id and filename passes."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
        }
        errors = validate_task(task, filename_stem="test-task-1")
        assert len(errors) == 0

    def test_id_mismatch_filename_stem(self):
        """Test that mismatched id and filename is caught."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
        }
        errors = validate_task(task, filename_stem="different-task")
        assert any(
            "does not match filename" in e for e in errors
        ), f"Expected filename mismatch error, got: {errors}"


class TestOptionalFields:
    """Test validation of optional task fields."""

    def test_valid_mode_value(self):
        """Test that valid mode values are accepted."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
            "mode": "/analysis-mode",
        }
        errors = validate_task(task)
        assert len(errors) == 0

    def test_invalid_mode_value(self):
        """Test that invalid mode values are rejected."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
            "mode": "invalid-mode",
        }
        errors = validate_task(task)
        assert any("invalid mode" in e for e in errors)

    def test_valid_priority_value(self):
        """Test that valid priority values are accepted."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
            "priority": "high",
        }
        errors = validate_task(task)
        assert len(errors) == 0

    def test_invalid_priority_value(self):
        """Test that invalid priority values are rejected."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
            "priority": "invalid-priority",
        }
        errors = validate_task(task)
        assert any("invalid priority" in e for e in errors)

    def test_context_must_be_dict(self):
        """Test that context field must be a dict."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
            "context": "not-a-dict",
        }
        errors = validate_task(task)
        assert any("context must be a mapping" in e for e in errors)


class TestStatusDependentValidation:
    """Test validation rules that depend on task status."""

    def test_done_status_requires_result_block(self):
        """Test that status=done requires result block."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "done",
            "artefacts": [],
        }
        errors = validate_task(task)
        assert any("result block required" in e for e in errors)

    def test_done_status_requires_result_summary(self):
        """Test that result block requires summary."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "done",
            "artefacts": [],
            "result": {"artefacts": []},
        }
        errors = validate_task(task)
        assert any("result.summary is required" in e for e in errors)

    def test_done_status_requires_result_artefacts(self):
        """Test that result block requires artefacts list."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "done",
            "artefacts": [],
            "result": {"summary": "Done", "artefacts": "not-a-list"},
        }
        errors = validate_task(task)
        assert any("result.artefacts/artifacts must be a list" in e for e in errors)

    def test_done_status_valid_result_block(self):
        """Test that valid result block passes for done status."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "done",
            "artefacts": ["output.md"],
            "result": {"summary": "Task completed", "artefacts": ["output.md"]},
        }
        errors = validate_task(task)
        assert len(errors) == 0

    def test_result_block_forbidden_when_not_done(self):
        """Test that result block is forbidden for non-done status."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "in_progress",
            "artefacts": [],
            "result": {"summary": "Not done yet", "artefacts": []},
        }
        errors = validate_task(task)
        assert any(
            "result block should only be present when status is 'done'" in e
            for e in errors
        )

    def test_error_status_requires_error_block(self):
        """Test that status=error requires error block."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "error",
            "artefacts": [],
        }
        errors = validate_task(task)
        assert any("error block required when status is 'error'" in e for e in errors)

    def test_error_status_requires_error_message(self):
        """Test that error block requires message field."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "error",
            "artefacts": [],
            "error": {},
        }
        errors = validate_task(task)
        assert any("error.message is required" in e for e in errors)

    def test_error_status_valid_error_block(self):
        """Test that valid error block passes for error status."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "error",
            "artefacts": [],
            "error": {"message": "Task failed"},
        }
        errors = validate_task(task)
        assert len(errors) == 0

    def test_error_block_forbidden_when_not_error(self):
        """Test that error block is forbidden for non-error status."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "in_progress",
            "artefacts": [],
            "error": {"message": "Should not be here"},
        }
        errors = validate_task(task)
        assert any(
            "error block should only be present when status is 'error'" in e
            for e in errors
        )


class TestArtefactsNotCreated:
    """Test validation of artefacts_not_created field."""

    def test_valid_artefacts_not_created(self):
        """Test that valid artefacts_not_created passes."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
            "artefacts_not_created": [
                {"name": "diagram.png", "rationale": "Not needed"}
            ],
        }
        errors = validate_task(task)
        assert len(errors) == 0

    def test_artefacts_not_created_american_spelling(self):
        """Test that American spelling is accepted."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
            "artifacts_not_created": [
                {"name": "diagram.png", "rationale": "Not needed"}
            ],
        }
        errors = validate_task(task)
        assert len(errors) == 0

    def test_artefacts_not_created_not_list(self):
        """Test that artefacts_not_created must be a list."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
            "artefacts_not_created": {"name": "invalid", "rationale": "format"},
        }
        errors = validate_task(task)
        assert any("must be a list" in e for e in errors)

    def test_artefacts_not_created_missing_name(self):
        """Test that entries must have name field."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
            "artefacts_not_created": [{"rationale": "Missing name"}],
        }
        errors = validate_task(task)
        assert any("'name' field" in e for e in errors)

    def test_artefacts_not_created_missing_rationale(self):
        """Test that entries must have rationale field."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
            "artefacts_not_created": [{"name": "diagram.png"}],
        }
        errors = validate_task(task)
        assert any("'rationale' field" in e for e in errors)


class TestTimestampFields:
    """Test validation of timestamp fields."""

    def test_valid_timestamps(self):
        """Test that valid ISO8601 timestamps pass."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
            "created_at": "2025-11-30T12:00:00Z",
            "assigned_at": "2025-11-30T12:05:00Z",
        }
        errors = validate_task(task)
        assert len(errors) == 0

    def test_invalid_timestamp_format(self):
        """Test that invalid timestamp formats are caught."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
            "created_at": "2025-11-30 12:00:00",  # Missing T and Z
        }
        errors = validate_task(task)
        assert any("created_at must be ISO8601 with Z suffix" in e for e in errors)

    def test_timestamp_suggestion_provided(self):
        """Test that timestamp fix suggestions are provided."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": [],
            "created_at": "2025-11-30 12:00:00+00:00",
        }
        errors = validate_task(task)
        assert any("Suggested: 2025-11-30T12:00:00Z" in e for e in errors)

    def test_result_completed_at_timestamp(self):
        """Test that result.completed_at timestamp is validated."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "done",
            "artefacts": [],
            "result": {
                "summary": "Done",
                "artefacts": [],
                "completed_at": "invalid-timestamp",
            },
        }
        errors = validate_task(task)
        assert any("result.completed_at must be ISO8601" in e for e in errors)

    def test_error_timestamp_validation(self):
        """Test that error.timestamp is validated."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "error",
            "artefacts": [],
            "error": {"message": "Failed", "timestamp": "invalid-timestamp"},
        }
        errors = validate_task(task)
        assert any("error.timestamp must be ISO8601" in e for e in errors)


class TestBritishAmericanSpellings:
    """Test that both British and American spellings are accepted."""

    def test_artefacts_british_spelling(self):
        """Test British spelling 'artefacts' is accepted."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artefacts": ["output.md"],
        }
        errors = validate_task(task)
        assert len(errors) == 0

    def test_artifacts_american_spelling(self):
        """Test American spelling 'artifacts' is accepted."""
        task = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "new",
            "artifacts": ["output.md"],
        }
        errors = validate_task(task)
        assert len(errors) == 0

    def test_result_artefacts_both_spellings(self):
        """Test both spellings in result block."""
        task_british = {
            "id": "test-task-1",
            "agent": "test-agent",
            "status": "done",
            "artefacts": [],
            "result": {"summary": "Done", "artefacts": ["output.md"]},
        }
        errors = validate_task(task_british)
        assert len(errors) == 0

        task_american = {
            "id": "test-task-2",
            "agent": "test-agent",
            "status": "done",
            "artifacts": [],
            "result": {"summary": "Done", "artifacts": ["output.md"]},
        }
        errors = validate_task(task_american)
        assert len(errors) == 0
