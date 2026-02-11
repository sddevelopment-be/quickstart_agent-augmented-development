#!/usr/bin/env python3
"""
Unit Tests for validate-task-schema.py

Tests task schema validation including:
- Required fields
- Optional fields like artefacts_not_created
- Status-dependent validation
- ISO8601 timestamp validation
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

# Add validation directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "validators"))

# Import from validate-task-schema.py by loading it as a module
import importlib.util
spec = importlib.util.spec_from_file_location(
    "validate_task_schema",
    Path(__file__).parent.parent / "tools" / "validators" / "validate-task-schema.py"
)
validate_task_schema = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_task_schema)
validate_task_file = validate_task_schema.validate_task_file

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def temp_task_dir(tmp_path: Path) -> Path:
    """Create isolated test directory for task files."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    return task_dir


@pytest.fixture
def valid_task() -> dict:
    """Create minimal valid task dictionary."""
    return {
        "id": "2025-11-30T1200-test-agent-sample-task",
        "agent": "test-agent",
        "status": "new",
        "title": "Sample test task",
        "artefacts": ["test/output/sample.md"],
        "created_at": "2025-11-30T12:00:00Z",
        "created_by": "test-harness",
    }


# ============================================================================
# artefacts_not_created Field Tests
# ============================================================================


def test_artefacts_not_created_valid_structure(
    temp_task_dir: Path, valid_task: dict
) -> None:
    """Test that valid artefacts_not_created field passes validation."""
    # Arrange
    valid_task["artefacts_not_created"] = [
        {
            "name": "optional-diagram.png",
            "rationale": "Task was rejected, diagram would contradict recommendation",
        }
    ]
    task_file = temp_task_dir / f"{valid_task['id']}.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(valid_task, f, default_flow_style=False, sort_keys=False)

    # Act
    errors = validate_task_file(task_file)

    # Assert
    assert len(errors) == 0, f"Expected no errors, got: {errors}"


def test_artefacts_not_created_british_spelling(
    temp_task_dir: Path, valid_task: dict
) -> None:
    """Test that British spelling 'artefacts_not_created' is accepted."""
    # Arrange
    valid_task["artefacts_not_created"] = [
        {"name": "example.yaml", "rationale": "Pattern rejected by architect"}
    ]
    task_file = temp_task_dir / f"{valid_task['id']}.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(valid_task, f, default_flow_style=False, sort_keys=False)

    # Act
    errors = validate_task_file(task_file)

    # Assert
    assert len(errors) == 0


def test_artifacts_not_created_american_spelling(
    temp_task_dir: Path, valid_task: dict
) -> None:
    """Test that American spelling 'artifacts_not_created' is accepted."""
    # Arrange
    valid_task["artifacts_not_created"] = [
        {"name": "example.yaml", "rationale": "Pattern rejected by architect"}
    ]
    task_file = temp_task_dir / f"{valid_task['id']}.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(valid_task, f, default_flow_style=False, sort_keys=False)

    # Act
    errors = validate_task_file(task_file)

    # Assert
    assert len(errors) == 0


def test_artefacts_not_created_multiple_items(
    temp_task_dir: Path, valid_task: dict
) -> None:
    """Test that multiple artefacts_not_created entries are valid."""
    # Arrange
    valid_task["artefacts_not_created"] = [
        {"name": "diagram.png", "rationale": "Not needed for this task"},
        {"name": "example.yaml", "rationale": "Would contradict recommendation"},
    ]
    task_file = temp_task_dir / f"{valid_task['id']}.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(valid_task, f, default_flow_style=False, sort_keys=False)

    # Act
    errors = validate_task_file(task_file)

    # Assert
    assert len(errors) == 0


def test_artefacts_not_created_invalid_not_list(
    temp_task_dir: Path, valid_task: dict
) -> None:
    """Test that artefacts_not_created must be a list."""
    # Arrange
    valid_task["artefacts_not_created"] = {
        "name": "example.yaml",
        "rationale": "Invalid format",
    }
    task_file = temp_task_dir / f"{valid_task['id']}.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(valid_task, f, default_flow_style=False, sort_keys=False)

    # Act
    errors = validate_task_file(task_file)

    # Assert
    assert len(errors) > 0
    assert any("must be a list" in e for e in errors)


def test_artefacts_not_created_missing_name(
    temp_task_dir: Path, valid_task: dict
) -> None:
    """Test that artefacts_not_created entries must have 'name' field."""
    # Arrange
    valid_task["artefacts_not_created"] = [
        {"rationale": "Missing name field"}
    ]
    task_file = temp_task_dir / f"{valid_task['id']}.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(valid_task, f, default_flow_style=False, sort_keys=False)

    # Act
    errors = validate_task_file(task_file)

    # Assert
    assert len(errors) > 0
    assert any("'name' field" in e for e in errors)


def test_artefacts_not_created_missing_rationale(
    temp_task_dir: Path, valid_task: dict
) -> None:
    """Test that artefacts_not_created entries must have 'rationale' field."""
    # Arrange
    valid_task["artefacts_not_created"] = [
        {"name": "example.yaml"}
    ]
    task_file = temp_task_dir / f"{valid_task['id']}.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(valid_task, f, default_flow_style=False, sort_keys=False)

    # Act
    errors = validate_task_file(task_file)

    # Assert
    assert len(errors) > 0
    assert any("'rationale' field" in e for e in errors)


def test_artefacts_not_created_invalid_entry_type(
    temp_task_dir: Path, valid_task: dict
) -> None:
    """Test that artefacts_not_created entries must be objects."""
    # Arrange
    valid_task["artefacts_not_created"] = ["string-entry-not-allowed"]
    task_file = temp_task_dir / f"{valid_task['id']}.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(valid_task, f, default_flow_style=False, sort_keys=False)

    # Act
    errors = validate_task_file(task_file)

    # Assert
    assert len(errors) > 0
    assert any("must be objects" in e for e in errors)


# ============================================================================
# Basic Validation Tests (ensure existing functionality still works)
# ============================================================================


def test_valid_task_passes(temp_task_dir: Path, valid_task: dict) -> None:
    """Test that a minimal valid task passes validation."""
    # Arrange
    task_file = temp_task_dir / f"{valid_task['id']}.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(valid_task, f, default_flow_style=False, sort_keys=False)

    # Act
    errors = validate_task_file(task_file)

    # Assert
    assert len(errors) == 0


def test_missing_agent_field(temp_task_dir: Path, valid_task: dict) -> None:
    """Test that missing 'agent' field is caught."""
    # Arrange
    del valid_task["agent"]
    task_file = temp_task_dir / f"{valid_task['id']}.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(valid_task, f, default_flow_style=False, sort_keys=False)

    # Act
    errors = validate_task_file(task_file)

    # Assert
    assert len(errors) > 0
    assert any("missing required field: agent" in e for e in errors)


def test_invalid_status(temp_task_dir: Path, valid_task: dict) -> None:
    """Test that invalid status values are caught."""
    # Arrange
    valid_task["status"] = "invalid-status"
    task_file = temp_task_dir / f"{valid_task['id']}.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(valid_task, f, default_flow_style=False, sort_keys=False)

    # Act
    errors = validate_task_file(task_file)

    # Assert
    assert len(errors) > 0
    assert any("invalid status" in e for e in errors)
