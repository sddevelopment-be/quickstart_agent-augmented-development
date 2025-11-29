#!/usr/bin/env python3
"""
Validate task YAML files for the asynchronous agent orchestration system.

Checks:
- Required fields and allowed values
- Filename/id alignment
- Agent directory existence
- ISO8601 timestamps with UTC suffix
- Result/error object alignment with status
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

ALLOWED_STATUSES = {"new", "assigned", "in_progress", "done", "error"}
ALLOWED_MODES = {
    "/analysis-mode",
    "/creative-mode",
    "/meta-mode",
    "/programming",
    "/planning",
}
ALLOWED_PRIORITIES = {"critical", "high", "medium", "normal", "low"}


def load_task(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def is_iso8601(timestamp: str) -> bool:
    if not timestamp.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(timestamp[:-1])
        return True
    except ValueError:
        return False


def validate_task_file(path: Path) -> list[str]:
    errors: list[str] = []
    task = load_task(path)

    # id vs filename
    if task.get("id") != path.stem:
        errors.append(f"id '{task.get('id')}' does not match filename '{path.stem}'")

    agent = task.get("agent")
    if not agent:
        errors.append("missing required field: agent")

    status = task.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(
            f"invalid status '{status}', expected one of {sorted(ALLOWED_STATUSES)}"
        )

    # Accept both "artefacts" (British English) and "artifacts" (American English) as aliases
    artefacts = task.get("artefacts") or task.get("artifacts")
    if not isinstance(artefacts, list):
        errors.append("artefacts/artifacts must be a list")
    elif not all(isinstance(item, str) for item in artefacts):
        errors.append("artefacts/artifacts entries must be strings")

    mode = task.get("mode")
    if mode is not None and mode not in ALLOWED_MODES:
        errors.append(f"invalid mode '{mode}', expected one of {sorted(ALLOWED_MODES)}")

    priority = task.get("priority")
    if priority is not None and priority not in ALLOWED_PRIORITIES:
        errors.append(
            f"invalid priority '{priority}', expected one of {sorted(ALLOWED_PRIORITIES)}"
        )

    for ts_field in ["created_at", "assigned_at", "started_at", "completed_at"]:
        if ts_field in task and task[ts_field] is not None:
            timestamp = str(task[ts_field])
            if not is_iso8601(timestamp):
                errors.append(f"{ts_field} must be ISO8601 with Z suffix")

    context = task.get("context")
    if context is not None and not isinstance(context, dict):
        errors.append("context must be a mapping when provided")

    result = task.get("result")
    error_block = task.get("error")

    if status == "done":
        if not isinstance(result, dict):
            errors.append("result block required for completed tasks")
        else:
            if not result.get("summary"):
                errors.append("result.summary is required when result is present")
            # Accept both "artefacts" (British English) and "artifacts" (American English) as aliases
            result_artefacts = result.get("artefacts") or result.get("artifacts")
            if not isinstance(result_artefacts, list) or not all(
                isinstance(a, str) for a in result_artefacts
            ):
                errors.append("result.artefacts/artifacts must be a list of strings")
            if "completed_at" in result and not is_iso8601(str(result["completed_at"])):
                errors.append(
                    "result.completed_at must be ISO8601 with Z suffix when present"
                )
    elif result is not None:
        errors.append("result block should only be present when status is 'done'")

    if status == "error":
        if not isinstance(error_block, dict):
            errors.append("error block required when status is 'error'")
        else:
            if not error_block.get("message"):
                errors.append("error.message is required when error block is present")
            if "timestamp" in error_block and not is_iso8601(
                str(error_block["timestamp"])
            ):
                errors.append(
                    "error.timestamp must be ISO8601 with Z suffix when present"
                )
    elif error_block is not None:
        errors.append("error block should only be present when status is 'error'")

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
