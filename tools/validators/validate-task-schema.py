#!/usr/bin/env python3
"""
Validate task YAML files for the asynchronous agent orchestration system.

This is a thin CLI wrapper around the domain-level task validator,
delegating all validation logic to src.domain.collaboration.task_validator
for consistency across tools and services.

Checks:
- Required fields and allowed values
- Filename/id alignment
- ISO8601 timestamps with UTC suffix
- Result/error object alignment with status

Note: All validation rules are defined in the domain layer (ADR-042, ADR-043)
for single source of truth.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add src/ to path for importing domain layer
# __file__ = tools/validators/validate-task-schema.py
# parent = tools/validators/
# parent.parent = tools/
# parent.parent.parent = repo_root/
repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(repo_root / "src"))

# ruff: noqa: E402 - Module level import after sys.path modification (required)
from domain.collaboration.task_schema import TaskIOError, read_task
from domain.collaboration.task_validator import validate_task


def validate_task_file(path: Path) -> list[str]:
    """
    Validate a single task file.

    This function loads the task using read_task() from the domain layer,
    which provides better error handling (multi-document detection, auto-migration)
    than raw YAML loading.

    Args:
        path: Path to task YAML file

    Returns:
        List of validation error messages (empty if valid)
    """
    errors: list[str] = []

    # Load task using domain layer (handles multi-document YAML, auto-migration)
    try:
        task = read_task(path)
    except TaskIOError as e:
        # Convert I/O errors to validation errors
        errors.append(str(e))
        return errors  # Can't validate structure if we can't load it
    except Exception as e:
        errors.append(f"Failed to load task: {e}")
        return errors

    # Delegate validation to domain layer
    validation_errors = validate_task(task, filename_stem=path.stem)
    errors.extend(validation_errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate orchestration task YAML files"
    )
    parser.add_argument("task_files", nargs="+", help="Paths to task YAML files")
    args = parser.parse_args()

    all_errors: list[str] = []

    for task_path_str in args.task_files:
        task_path = Path(task_path_str)
        if not task_path.exists():
            all_errors.append(f"File not found: {task_path}")
            continue

        errors = validate_task_file(task_path)
        if errors:
            all_errors.extend([f"{task_path}: {error}" for error in errors])

    if all_errors:
        for err in all_errors:
            print(f"❌ {err}", file=sys.stderr)
        return 1

    print("✅ Task schema validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
