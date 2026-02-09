"""
Unit tests for TaskAssignmentHandler.

Tests YAML update, comment preservation, validation, and optimistic locking
for orphan task assignment feature.

Related:
- Specification: specifications/initiatives/dashboard-enhancements/orphan-task-assignment.md
- ADR-035: Dashboard Task Priority Editing (patterns reused)
"""

from datetime import datetime, timezone

import pytest
from ruamel.yaml import YAML

from src.llm_service.dashboard.task_assignment_handler import (
    ConcurrentModificationError,
    InvalidSpecificationError,
    TaskAssignmentHandler,
    TaskNotEditableError,
)


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory for testing."""
    work_dir = tmp_path / "work" / "collaboration"
    inbox = work_dir / "inbox"
    inbox.mkdir(parents=True)
    return work_dir


@pytest.fixture
def temp_repo_root(tmp_path):
    """Create temporary repository root with specifications."""
    spec_dir = tmp_path / "specifications" / "llm-service"
    spec_dir.mkdir(parents=True)

    # Create valid specification file
    spec_file = spec_dir / "api-hardening.md"
    spec_content = """---
id: SPEC-API-HARDENING
title: API Hardening
---

# API Hardening

## Features

### Rate Limiting
Rate limiting feature.
"""
    spec_file.write_text(spec_content, encoding="utf-8")

    return tmp_path


@pytest.fixture
def handler(temp_work_dir, temp_repo_root):
    """Create TaskAssignmentHandler instance."""
    return TaskAssignmentHandler(
        work_dir=str(temp_work_dir), repo_root=str(temp_repo_root)
    )


@pytest.fixture
def orphan_task_file(temp_work_dir):
    """Create orphan task YAML file with comments."""
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False

    task_id = "2026-02-09T2000-test-task"
    task_file = temp_work_dir / "inbox" / f"{task_id}.yaml"

    task_data = {
        "id": task_id,
        "agent": "python-pedro",
        "status": "pending",
        "priority": "high",
        "title": "Test task",
        "description": "Test description",
        "created": "2026-02-09 20:00:00+00:00",
        "created_by": "planning-petra",
    }

    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(task_data, f)

    # Add comment
    content = task_file.read_text(encoding="utf-8")
    content = "# Test task comment\n" + content
    task_file.write_text(content, encoding="utf-8")

    return task_file, task_id


class TestTaskAssignmentHandler:
    """Unit tests for TaskAssignmentHandler."""

    def test_validate_specification_path_valid(self, handler):
        """Test validation of valid specification paths."""
        valid_paths = [
            "specifications/llm-service/api-hardening.md",
            "specifications/dashboard/features.md",
            "specifications/deep/nested/spec.md",
        ]

        for path in valid_paths:
            # Should not raise exception
            handler.validate_specification_path(path)

    def test_validate_specification_path_rejects_traversal(self, handler):
        """Test rejection of path traversal attempts."""
        invalid_paths = [
            "../../../etc/passwd",
            "specifications/../../../etc/passwd",
            "specifications/../../secrets.txt",
            "/etc/passwd",
            "C:\\Windows\\System32\\config\\sam",
        ]

        for path in invalid_paths:
            with pytest.raises(InvalidSpecificationError) as exc_info:
                handler.validate_specification_path(path)
            assert "Invalid specification path" in str(exc_info.value)

    def test_validate_specification_path_rejects_non_markdown(self, handler):
        """Test rejection of non-markdown files."""
        invalid_paths = [
            "specifications/config.yaml",
            "specifications/script.py",
            "specifications/data.json",
        ]

        for path in invalid_paths:
            with pytest.raises(InvalidSpecificationError) as exc_info:
                handler.validate_specification_path(path)
            assert "must be a .md file" in str(exc_info.value).lower()

    def test_check_specification_exists_valid(self, handler, temp_repo_root):
        """Test checking existence of valid specification file."""
        spec_path = "specifications/llm-service/api-hardening.md"

        # Should not raise exception
        handler.check_specification_exists(spec_path)

    def test_check_specification_exists_missing(self, handler):
        """Test checking non-existent specification file."""
        spec_path = "specifications/nonexistent.md"

        with pytest.raises(InvalidSpecificationError) as exc_info:
            handler.check_specification_exists(spec_path)
        assert "not found" in str(exc_info.value).lower()

    def test_is_task_editable_pending(self, handler, orphan_task_file):
        """Test that pending tasks are editable."""
        task_file, task_id = orphan_task_file

        yaml = YAML()
        with open(task_file, encoding="utf-8") as f:
            task_data = yaml.load(f)

        task_data["status"] = "pending"
        assert handler.is_task_editable(task_data) is True

    def test_is_task_editable_assigned(self, handler, orphan_task_file):
        """Test that assigned tasks are editable."""
        task_file, task_id = orphan_task_file

        yaml = YAML()
        with open(task_file, encoding="utf-8") as f:
            task_data = yaml.load(f)

        task_data["status"] = "assigned"
        assert handler.is_task_editable(task_data) is True

    def test_is_task_editable_in_progress(self, handler, orphan_task_file):
        """Test that in_progress tasks are not editable."""
        task_file, task_id = orphan_task_file

        yaml = YAML()
        with open(task_file, encoding="utf-8") as f:
            task_data = yaml.load(f)

        task_data["status"] = "in_progress"
        assert handler.is_task_editable(task_data) is False

    def test_is_task_editable_done(self, handler, orphan_task_file):
        """Test that done tasks are not editable."""
        task_file, task_id = orphan_task_file

        yaml = YAML()
        with open(task_file, encoding="utf-8") as f:
            task_data = yaml.load(f)

        task_data["status"] = "done"
        assert handler.is_task_editable(task_data) is False

    def test_update_task_specification_success(
        self, handler, orphan_task_file, temp_repo_root
    ):
        """Test successful task specification update."""
        task_file, task_id = orphan_task_file

        # Update task
        updated_task = handler.update_task_specification(
            task_id=task_id,
            specification="specifications/llm-service/api-hardening.md",
            feature="Rate Limiting",
        )

        # Verify return value
        assert (
            updated_task["specification"]
            == "specifications/llm-service/api-hardening.md"
        )
        assert updated_task["feature"] == "Rate Limiting"
        assert "last_modified" in updated_task

        # Verify file was updated
        yaml = YAML()
        with open(task_file, encoding="utf-8") as f:
            file_data = yaml.load(f)

        assert (
            file_data["specification"] == "specifications/llm-service/api-hardening.md"
        )
        assert file_data["feature"] == "Rate Limiting"

    def test_update_task_specification_preserves_comments(
        self, handler, orphan_task_file, temp_repo_root
    ):
        """Test that YAML comments are preserved during update."""
        task_file, task_id = orphan_task_file

        # Read original content
        original_content = task_file.read_text(encoding="utf-8")
        assert "# Test task comment" in original_content

        # Update task
        handler.update_task_specification(
            task_id=task_id, specification="specifications/llm-service/api-hardening.md"
        )

        # Verify comments preserved
        updated_content = task_file.read_text(encoding="utf-8")
        assert "# Test task comment" in updated_content

    def test_update_task_specification_without_feature(
        self, handler, orphan_task_file, temp_repo_root
    ):
        """Test updating specification without feature (feature is optional)."""
        task_file, task_id = orphan_task_file

        # Update task without feature
        updated_task = handler.update_task_specification(
            task_id=task_id, specification="specifications/llm-service/api-hardening.md"
        )

        # Verify specification set, feature not set
        assert (
            updated_task["specification"]
            == "specifications/llm-service/api-hardening.md"
        )
        assert "feature" not in updated_task or updated_task.get("feature") is None

    def test_update_task_specification_rejects_in_progress(
        self, handler, orphan_task_file, temp_repo_root
    ):
        """Test that in_progress tasks cannot be assigned."""
        task_file, task_id = orphan_task_file

        # Set task to in_progress
        yaml = YAML()
        with open(task_file, encoding="utf-8") as f:
            task_data = yaml.load(f)
        task_data["status"] = "in_progress"
        with open(task_file, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f)

        # Try to update
        with pytest.raises(TaskNotEditableError) as exc_info:
            handler.update_task_specification(
                task_id=task_id,
                specification="specifications/llm-service/api-hardening.md",
            )
        assert "cannot assign" in str(exc_info.value).lower()

    def test_update_task_specification_optimistic_locking(
        self, handler, orphan_task_file, temp_repo_root
    ):
        """Test optimistic locking with last_modified timestamp."""
        task_file, task_id = orphan_task_file

        # Add last_modified to task
        yaml = YAML()
        with open(task_file, encoding="utf-8") as f:
            task_data = yaml.load(f)
        old_timestamp = "2026-02-09T20:00:00Z"
        task_data["last_modified"] = old_timestamp
        with open(task_file, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f)

        # Simulate concurrent modification
        with open(task_file, encoding="utf-8") as f:
            task_data = yaml.load(f)
        new_timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        task_data["last_modified"] = new_timestamp
        with open(task_file, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f)

        # Try to update with old timestamp
        with pytest.raises(ConcurrentModificationError) as exc_info:
            handler.update_task_specification(
                task_id=task_id,
                specification="specifications/llm-service/api-hardening.md",
                last_modified=old_timestamp,
            )
        assert "modified" in str(exc_info.value).lower()

    def test_update_task_specification_atomic_write(
        self, handler, orphan_task_file, temp_repo_root
    ):
        """Test that file writes are atomic (no partial writes on error)."""
        task_file, task_id = orphan_task_file

        # Read original content
        original_content = task_file.read_text(encoding="utf-8")

        # Try to update with invalid specification path
        # This should fail validation before writing
        with pytest.raises(InvalidSpecificationError):
            handler.update_task_specification(
                task_id=task_id, specification="../../../etc/passwd"
            )

        # Verify file unchanged
        current_content = task_file.read_text(encoding="utf-8")
        assert current_content == original_content

    def test_update_task_specification_updates_last_modified(
        self, handler, orphan_task_file, temp_repo_root
    ):
        """Test that last_modified timestamp is updated."""
        task_file, task_id = orphan_task_file

        before = datetime.now(timezone.utc)

        # Update task
        updated_task = handler.update_task_specification(
            task_id=task_id, specification="specifications/llm-service/api-hardening.md"
        )

        after = datetime.now(timezone.utc)

        # Verify last_modified is recent
        assert "last_modified" in updated_task
        last_modified_str = updated_task["last_modified"]

        # Parse timestamp (handle 'Z' timezone notation)
        last_modified = datetime.fromisoformat(last_modified_str.replace("Z", "+00:00"))

        # Verify timestamp is between before and after
        assert before <= last_modified <= after
