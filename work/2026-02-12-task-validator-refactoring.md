# Task Schema Validator Refactoring

**Date:** 2026-02-12
**Agent:** Python Pedro (Sonnet 4.5)
**Status:** Complete

## Objective

Refactor the task schema validator at `tools/validators/validate-task-schema.py` to better integrate with the domain layer in `src/domain/collaboration/`.

## Changes Implemented

### 1. Created Domain-Level Task Validator

**File:** `src/domain/collaboration/task_validator.py`

Created a new domain service that encapsulates all task validation logic:
- Validation of required fields (id, agent, status, artefacts)
- Validation of optional fields (mode, priority, context, artefacts_not_created)
- Status-dependent validation (result block for "done", error block for "error")
- Timestamp validation (ISO8601 with Z suffix)
- British/American spelling support (artefacts/artifacts)

**Key Functions:**
- `validate_task(task, filename_stem)` - Main validation function
- `is_iso8601_utc(timestamp)` - Timestamp format validation
- `suggest_timestamp_fix(timestamp)` - Helpful fix suggestions

### 2. Refactored CLI Validator Script

**File:** `tools/validators/validate-task-schema.py`

Converted the script from a monolithic validator to a thin CLI wrapper:
- Uses `read_task()` from `src/domain/collaboration/task_schema` for loading (better error handling)
- Delegates all validation logic to `validate_task()` from domain layer
- Maintains existing CLI interface (backward compatible)
- Reduced from ~210 lines to ~60 lines

### 3. Updated Domain Package Exports

**File:** `src/domain/collaboration/__init__.py`

Added exports for:
- Task I/O functions: `read_task`, `write_task`, `load_task_safe`
- Validation function: `validate_task`
- Type enums: `TaskStatus`, `TaskMode`, `TaskPriority`
- Exceptions: `TaskSchemaError`, `TaskIOError`, `TaskValidationError`

### 4. Comprehensive Unit Tests

**File:** `tests/unit/domain/collaboration/test_task_validator.py`

Created 42 unit tests covering:
- Timestamp validation helpers
- Required field validation
- Filename/id alignment
- Optional field validation
- Status-dependent validation rules
- artefacts_not_created field validation
- Timestamp field validation
- British/American spelling support

## Key Improvements

### Better Error Handling

The refactored validator now uses `read_task()` which provides:
- Multi-document YAML detection with helpful error messages
- Auto-migration from old `task_id` format to new `id` format
- Better validation of required fields before parsing

### Single Source of Truth

All validation rules are now centralized in the domain layer:
- No duplicate validation logic between tools
- Enum values derived from domain types (ADR-043)
- Consistent validation across all tools and services

### Maintainability

- Validation logic is now testable independently of CLI
- Clear separation between CLI concerns and business logic
- Domain layer has no dependencies on validator tools
- Easier to extend with new validation rules

### Correct Handling of Empty Lists

Fixed a subtle bug in the original `or` logic:
```python
# OLD (buggy with empty lists)
artefacts = task.get("artefacts") or task.get("artifacts")

# NEW (correct)
artefacts = task.get("artefacts")
if artefacts is None:
    artefacts = task.get("artifacts")
```

This ensures that `artefacts: []` is treated as a valid value, not falsy.

## Test Results

All tests passing:

```
tests/test_validate_task_schema.py ............. 11 passed
tests/test_task_loading_bugs.py ................ 7 passed (1 skipped)
tests/unit/domain/collaboration/test_task_validator.py ... 42 passed
tests/ -k "task_schema or validate" ............ 103 passed, 11 skipped
```

## Benefits

1. **Reusability:** Other tools can now use `validate_task()` without duplicating logic
2. **Consistency:** All task validation uses the same domain rules
3. **Testability:** Validation logic can be unit tested independently
4. **Maintainability:** Changes to validation rules only need to be made in one place
5. **Better UX:** Improved error messages from `read_task()` with multi-document detection

## Files Modified

- `src/domain/collaboration/task_validator.py` - NEW (domain validator)
- `src/domain/collaboration/__init__.py` - UPDATED (added exports)
- `tools/validators/validate-task-schema.py` - REFACTORED (now uses domain layer)
- `tests/unit/domain/collaboration/test_task_validator.py` - NEW (comprehensive tests)
- `tests/unit/domain/collaboration/__init__.py` - NEW (test package)

## Constraints Maintained

- CLI interface unchanged (accepts file paths, prints errors, exits 0/1)
- Validator usable from CI (GitHub Actions compatibility maintained)
- Domain layer does not depend on validator (correct dependency direction)
- Code style follows black formatting and ruff linting rules

## Related ADRs

- ADR-042: Shared Task Domain Model
- ADR-043: Status Enumeration Standard

## Next Steps

Future improvements could include:
- Consider creating a `TaskValidationResult` class with structured error reporting
- Add validation for task state transitions (e.g., can only go from "assigned" to "in_progress")
- Add validation for cross-field dependencies (e.g., "completed_at" must be after "created_at")
