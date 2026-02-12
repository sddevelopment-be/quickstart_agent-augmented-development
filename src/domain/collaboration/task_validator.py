"""
Task validation domain service.

Provides centralized validation logic for task structure, field requirements,
and state-dependent rules. This is the single source of truth for task validation
rules across all tools and services.

Related ADRs:
- ADR-042: Shared Task Domain Model
- ADR-043: Status Enumeration Standard
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .types import TaskMode, TaskPriority, TaskStatus


class TaskValidationError(Exception):
    """Raised when task validation fails."""

    pass


def is_iso8601_utc(timestamp: str) -> bool:
    """
    Check if timestamp is valid ISO8601 with Z (UTC) suffix.

    Args:
        timestamp: Timestamp string to validate

    Returns:
        True if valid ISO8601 with Z suffix, False otherwise

    Example:
        >>> is_iso8601_utc("2025-11-30T12:00:00Z")
        True
        >>> is_iso8601_utc("2025-11-30 12:00:00")
        False
    """
    if not isinstance(timestamp, str):
        return False
    if not timestamp.endswith("Z"):
        return False
    # Must contain 'T' separator (ISO8601 format requirement)
    if "T" not in timestamp:
        return False
    try:
        datetime.fromisoformat(timestamp[:-1])
        return True
    except ValueError:
        return False


def suggest_timestamp_fix(timestamp: str) -> str:
    """
    Suggest a fix for common timestamp format issues.

    Args:
        timestamp: Timestamp string with potential formatting issues

    Returns:
        Corrected timestamp string in ISO8601 UTC format

    Example:
        >>> suggest_timestamp_fix("2026-02-09 04:40:00+00:00")
        "2026-02-09T04:40:00Z"
    """
    timestamp = str(timestamp)

    # Case 1: Space instead of T (e.g., "2026-02-09 04:40:00+00:00")
    if " " in timestamp and "T" not in timestamp:
        timestamp = timestamp.replace(" ", "T", 1)

    # Case 2: Timezone offset instead of Z (e.g., "2026-02-09T04:40:00+00:00")
    if timestamp.endswith("+00:00") or timestamp.endswith("-00:00"):
        timestamp = timestamp[:-6] + "Z"

    # Case 3: Missing Z suffix (e.g., "2026-02-09T04:40:00")
    if (
        not timestamp.endswith("Z")
        and "+" not in timestamp
        and "-" not in timestamp[-6:]
    ):
        timestamp = timestamp + "Z"

    return timestamp


def validate_task(task: dict[str, Any], filename_stem: str | None = None) -> list[str]:
    """
    Validate task structure and field requirements.

    This function encapsulates all task validation rules:
    - Required fields (id, agent, status, artefacts)
    - Optional fields with type constraints
    - Status-dependent validation (result for done, error for error)
    - Timestamp format validation (ISO8601 with Z suffix)
    - Enum value validation (status, mode, priority)

    Args:
        task: Task dictionary to validate
        filename_stem: Optional filename stem to validate against task id

    Returns:
        List of validation error messages (empty if valid)

    Example:
        >>> task = {"id": "test-1", "agent": "bob", "status": "new", "artefacts": []}
        >>> errors = validate_task(task)
        >>> len(errors)
        0
    """
    errors: list[str] = []

    # Allowed values from domain enums (single source of truth)
    allowed_statuses = {status.value for status in TaskStatus}
    allowed_modes = {mode.value for mode in TaskMode}
    allowed_priorities = {priority.value for priority in TaskPriority}

    # ========================================================================
    # Required Fields
    # ========================================================================

    # Validate id field
    task_id = task.get("id")
    if not task_id:
        errors.append("missing required field: id")
    elif filename_stem and task_id != filename_stem:
        errors.append(f"id '{task_id}' does not match filename '{filename_stem}'")

    # Validate agent field
    agent = task.get("agent")
    if not agent:
        errors.append("missing required field: agent")

    # Validate status field (must be valid enum value)
    status = task.get("status")
    if status not in allowed_statuses:
        errors.append(
            f"invalid status '{status}', expected one of {sorted(allowed_statuses)}"
        )

    # Validate artefacts field (accept both British and American spelling)
    # Use explicit None check to handle empty lists correctly
    artefacts = task.get("artefacts")
    if artefacts is None:
        artefacts = task.get("artifacts")

    if artefacts is None:
        # artefacts field is required (even if empty list)
        errors.append("missing required field: artefacts/artifacts")
    elif not isinstance(artefacts, list):
        errors.append("artefacts/artifacts must be a list")
    elif not all(isinstance(item, str) for item in artefacts):
        errors.append("artefacts/artifacts entries must be strings")

    # ========================================================================
    # Optional Fields with Type Constraints
    # ========================================================================

    # Validate mode field (optional, must be valid enum value)
    mode = task.get("mode")
    if mode is not None and mode not in allowed_modes:
        errors.append(f"invalid mode '{mode}', expected one of {sorted(allowed_modes)}")

    # Validate priority field (optional, must be valid enum value)
    priority = task.get("priority")
    if priority is not None and priority not in allowed_priorities:
        errors.append(
            f"invalid priority '{priority}', expected one of {sorted(allowed_priorities)}"
        )

    # Validate context field (optional, must be dict)
    context = task.get("context")
    if context is not None and not isinstance(context, dict):
        errors.append("context must be a mapping when provided")

    # Validate artefacts_not_created field (optional, list of dicts)
    # Use explicit None check to handle empty lists correctly
    artefacts_not_created = task.get("artefacts_not_created")
    if artefacts_not_created is None:
        artefacts_not_created = task.get("artifacts_not_created")
    if artefacts_not_created is not None:
        if not isinstance(artefacts_not_created, list):
            errors.append("artefacts_not_created/artifacts_not_created must be a list")
        else:
            for item in artefacts_not_created:
                if not isinstance(item, dict):
                    errors.append(
                        "artefacts_not_created entries must be objects with 'name' and 'rationale' fields"
                    )
                    break
                if "name" not in item or not isinstance(item["name"], str):
                    errors.append(
                        "artefacts_not_created entries must have a 'name' field (string)"
                    )
                if "rationale" not in item or not isinstance(item["rationale"], str):
                    errors.append(
                        "artefacts_not_created entries must have a 'rationale' field (string)"
                    )

    # ========================================================================
    # Timestamp Validation
    # ========================================================================

    for ts_field in ["created_at", "assigned_at", "started_at", "completed_at"]:
        if ts_field in task and task[ts_field] is not None:
            timestamp = str(task[ts_field])
            if not is_iso8601_utc(timestamp):
                suggestion = suggest_timestamp_fix(timestamp)
                errors.append(
                    f"{ts_field} must be ISO8601 with Z suffix\n"
                    f"  Current: {timestamp}\n"
                    f"  Suggested: {suggestion}"
                )

    # ========================================================================
    # Status-Dependent Validation
    # ========================================================================

    result = task.get("result")
    error_block = task.get("error")

    # When status is "done", require result block with summary and artefacts
    if status == "done":
        if not isinstance(result, dict):
            errors.append(
                "result block required for completed tasks\n"
                "  Expected structure:\n"
                "    result:\n"
                '      summary: "Description of what was accomplished"\n'
                "      artefacts:  # or 'artifacts'\n"
                "        - path/to/file1.py\n"
                "        - path/to/file2.md"
            )
        else:
            # Validate result.summary
            if not result.get("summary"):
                errors.append("result.summary is required when result is present")

            # Validate result.artefacts (accept both spellings)
            # Use explicit None check to handle empty lists correctly
            result_artefacts = result.get("artefacts")
            if result_artefacts is None:
                result_artefacts = result.get("artifacts")
            if not isinstance(result_artefacts, list) or not all(
                isinstance(a, str) for a in result_artefacts
            ):
                # Check if user mistakenly used "artifacts_created" or other field
                hint = ""
                if "artifacts_created" in result or "artefacts_created" in result:
                    hint = "\n  Hint: Use 'artefacts' or 'artifacts', not 'artifacts_created'"
                errors.append(
                    f"result.artefacts/artifacts must be a list of strings{hint}"
                )

            # Validate result.completed_at timestamp if present
            if "completed_at" in result and not is_iso8601_utc(
                str(result["completed_at"])
            ):
                suggestion = suggest_timestamp_fix(str(result["completed_at"]))
                errors.append(
                    f"result.completed_at must be ISO8601 with Z suffix when present\n"
                    f"  Current: {result['completed_at']}\n"
                    f"  Suggested: {suggestion}"
                )
    elif result is not None:
        errors.append("result block should only be present when status is 'done'")

    # When status is "error", require error block with message
    if status == "error":
        if not isinstance(error_block, dict):
            errors.append("error block required when status is 'error'")
        else:
            # Validate error.message
            if not error_block.get("message"):
                errors.append("error.message is required when error block is present")

            # Validate error.timestamp if present
            if "timestamp" in error_block and not is_iso8601_utc(
                str(error_block["timestamp"])
            ):
                suggestion = suggest_timestamp_fix(str(error_block["timestamp"]))
                errors.append(
                    f"error.timestamp must be ISO8601 with Z suffix when present\n"
                    f"  Current: {error_block['timestamp']}\n"
                    f"  Suggested: {suggestion}"
                )
    elif error_block is not None:
        errors.append("error block should only be present when status is 'error'")

    return errors
