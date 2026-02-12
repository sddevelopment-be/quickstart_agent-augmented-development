# Task Validation Guide

This guide explains how to use the task validation functionality in the domain layer.

## Quick Start

### Basic Validation

```python
from src.domain.collaboration import validate_task, read_task

# Read a task file (handles multi-document YAML, auto-migrates old format)
task = read_task(Path("work/collaboration/inbox/my-task.yaml"))

# Validate the task structure
errors = validate_task(task)

if errors:
    for error in errors:
        print(f"Validation error: {error}")
else:
    print("Task is valid!")
```

### Validation with Filename Check

```python
from pathlib import Path
from src.domain.collaboration import validate_task, read_task

task_path = Path("work/collaboration/inbox/my-task.yaml")
task = read_task(task_path)

# Validate including filename/id alignment
errors = validate_task(task, filename_stem=task_path.stem)

if errors:
    for error in errors:
        print(f"Error: {error}")
```

## CLI Usage

The command-line validator is a thin wrapper around the domain validation:

```bash
# Validate one or more task files
python tools/validators/validate-task-schema.py work/collaboration/inbox/*.yaml

# Exit code 0 = valid, 1 = validation errors
```

## Validation Rules

### Required Fields

Every task must have:
- `id` - Task identifier (must match filename stem)
- `agent` - Agent assigned to the task
- `status` - Task status (must be valid TaskStatus enum value)
- `artefacts` or `artifacts` - List of artifact paths (can be empty)

### Optional Fields

- `mode` - Task mode (must be valid TaskMode enum value)
- `priority` - Task priority (must be valid TaskPriority enum value)
- `context` - Additional context (must be a dict)
- `created_at`, `assigned_at`, `started_at`, `completed_at` - Timestamps (ISO8601 with Z)
- `artefacts_not_created` - List of intentionally omitted artifacts

### Status-Dependent Rules

#### When status is "done"

Must have a `result` block with:
- `summary` - Description of what was accomplished (string)
- `artefacts` or `artifacts` - List of created artifact paths (list of strings)
- `completed_at` - Optional completion timestamp (ISO8601 with Z)

Example:
```yaml
status: done
result:
  summary: "Created task validator domain service"
  artefacts:
    - src/domain/collaboration/task_validator.py
    - tests/unit/domain/collaboration/test_task_validator.py
  completed_at: "2026-02-12T10:30:00Z"
```

#### When status is "error"

Must have an `error` block with:
- `message` - Error description (string)
- `timestamp` - Optional error timestamp (ISO8601 with Z)

Example:
```yaml
status: error
error:
  message: "Failed to parse YAML: invalid syntax"
  timestamp: "2026-02-12T10:30:00Z"
```

### Timestamp Format

All timestamps must be ISO8601 format with UTC suffix:
- Valid: `"2026-02-12T10:30:00Z"`
- Invalid: `"2026-02-12 10:30:00"` (space instead of T)
- Invalid: `"2026-02-12T10:30:00+00:00"` (offset instead of Z)
- Invalid: `"2026-02-12T10:30:00"` (missing Z)

The validator provides helpful suggestions for common timestamp errors:
```
created_at must be ISO8601 with Z suffix
  Current: 2026-02-12 10:30:00+00:00
  Suggested: 2026-02-12T10:30:00Z
```

### British vs American Spelling

Both spellings are supported for artifact-related fields:
- `artefacts` (British) or `artifacts` (American)
- `artefacts_not_created` (British) or `artifacts_not_created` (American)

Be consistent within a single task file.

## Advanced Usage

### Custom Validation in Scripts

```python
from src.domain.collaboration import validate_task

def validate_and_fix(task: dict) -> tuple[dict, list[str]]:
    """Validate task and attempt automatic fixes."""
    errors = validate_task(task)

    # Auto-fix timestamp format if needed
    if any("must be ISO8601" in e for e in errors):
        from src.domain.collaboration.task_validator import suggest_timestamp_fix
        for field in ["created_at", "assigned_at", "started_at", "completed_at"]:
            if field in task and task[field]:
                task[field] = suggest_timestamp_fix(str(task[field]))

    # Re-validate after fixes
    errors = validate_task(task)
    return task, errors
```

### Using in Tests

```python
import pytest
from src.domain.collaboration import validate_task

def test_my_task_generation():
    """Test that generated task is valid."""
    task = generate_task()  # Your task generation logic

    errors = validate_task(task)
    assert len(errors) == 0, f"Generated task is invalid: {errors}"
```

## Error Messages

The validator provides clear, actionable error messages:

```
missing required field: id
missing required field: agent
invalid status 'invalid', expected one of ['assigned', 'blocked', 'done', 'error', 'in_progress', 'inbox', 'new']
artefacts/artifacts must be a list
result block required for completed tasks
error.message is required when error block is present
```

## Common Validation Failures

### Missing Required Field

```yaml
# INVALID - missing agent
id: my-task
status: new
artefacts: []
```

Fix: Add all required fields
```yaml
id: my-task
agent: python-pedro
status: new
artefacts: []
```

### Invalid Timestamp

```yaml
# INVALID - timestamp format
id: my-task
created_at: 2026-02-12 10:30:00  # Missing T and Z
```

Fix: Use ISO8601 with Z suffix
```yaml
id: my-task
created_at: "2026-02-12T10:30:00Z"
```

### ID/Filename Mismatch

```yaml
# File: my-task.yaml
# INVALID - id doesn't match filename
id: different-task
```

Fix: Ensure id matches filename stem
```yaml
# File: my-task.yaml
id: my-task
```

### Result Block Without Done Status

```yaml
# INVALID - result block present but status is not "done"
id: my-task
status: in_progress
result:
  summary: "Not done yet"
```

Fix: Only include result block when status is "done"
```yaml
id: my-task
status: done
result:
  summary: "Task completed"
  artefacts: []
```

## Related Documentation

- `src/domain/collaboration/task_validator.py` - Validation implementation
- `src/domain/collaboration/task_schema.py` - Task I/O operations
- `src/domain/collaboration/types.py` - Task enums and types
- ADR-042: Shared Task Domain Model
- ADR-043: Status Enumeration Standard
