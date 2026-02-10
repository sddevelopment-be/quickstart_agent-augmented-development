# Task Schema Validation Infrastructure

## Overview

This directory contains validation tools for the asynchronous agent orchestration system's task files. The validation infrastructure ensures task files are consistent, complete, and follow the established schema standards.

## Architecture

### Single Source of Truth (ADR-043)

All validators use the **TaskStatus enum** from `src/common/types.py` as the single source of truth for status values. This ensures:
- No drift between validation and runtime code
- Type-safe status handling
- Consistent status lifecycle management

### Validation Layers

```
┌─────────────────────────────────────────┐
│  Shell Wrapper (validate-task.sh)      │
│  - User-facing CLI                       │
│  - Batch file validation                 │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Python Validator (validate-task-schema)│
│  - Core validation logic                 │
│  - Enum-based status validation          │
│  - ISO8601 timestamp checks              │
│  - Result/error block alignment          │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Shared Types (src/common/types.py)     │
│  - TaskStatus enum (ADR-043)             │
│  - FeatureStatus enum                    │
│  - AgentIdentity validation              │
└─────────────────────────────────────────┘
```

## Validation Rules

### Required Fields

- **id**: Must match filename (stem without extension)
- **agent**: Agent identifier
- **status**: Must be a valid TaskStatus enum value
- **artefacts/artifacts**: List of file paths (accepts both spellings)

### Status-Based Rules

| Status     | Requirements                                                                 |
|------------|------------------------------------------------------------------------------|
| `new`      | No result/error blocks                                                       |
| `inbox`    | No result/error blocks                                                       |
| `assigned` | No result/error blocks                                                       |
| `in_progress` | No result/error blocks                                                    |
| `blocked`  | No result/error blocks                                                       |
| `done`     | **Requires result block** with summary and artefacts/artifacts (list)       |
| `error`    | **Requires error block** with message field                                  |

### Timestamp Validation

All timestamp fields must be **ISO8601 format with Z suffix** (UTC timezone):

✅ **Valid**: `2026-02-09T04:40:00Z`
❌ **Invalid**: 
- `2026-02-09 04:40:00+00:00` (space instead of T, timezone offset instead of Z)
- `2026-02-09T04:40:00` (missing Z suffix)
- `2026-02-09T04:40:00+00:00` (timezone offset instead of Z)

**Validated fields**:
- `created_at`
- `assigned_at`
- `started_at`
- `completed_at`
- `result.completed_at` (when present)
- `error.timestamp` (when present)

### Result Block Structure (status="done")

```yaml
result:
  summary: "Brief description of what was accomplished"
  artefacts:  # or "artifacts" (both accepted)
    - path/to/file1.py
    - path/to/file2.md
  completed_at: "2026-02-09T04:50:42Z"  # optional
  metrics: {}  # optional
```

### Error Block Structure (status="error")

```yaml
error:
  message: "Description of what went wrong"
  timestamp: "2026-02-09T04:50:42Z"  # optional
  details: {}  # optional
```

### Artefacts Not Created (Optional)

For documenting intentionally omitted artifacts:

```yaml
artefacts_not_created:  # or "artifacts_not_created"
  - name: "proposed-file.py"
    rationale: "Decided to consolidate into existing module"
  - name: "another-file.md"
    rationale: "Already documented in parent spec"
```

## Usage

### Command Line

```bash
# Validate single file
./tools/scripts/validate-task.sh work/collaboration/done/curator/task.yaml

# Validate multiple files
./tools/scripts/validate-task.sh work/collaboration/done/curator/*.yaml

# Direct Python invocation
python tools/validators/validate-task-schema.py path/to/task.yaml
```

### CI/CD Integration

```yaml
# Example GitHub Actions workflow
- name: Validate Task Files
  run: |
    find work/collaboration/done -name "*.yaml" -type f | \
    xargs ./tools/scripts/validate-task.sh
```

### Exit Codes

- `0`: All validations passed
- `1`: One or more validation errors found

## Common Validation Errors

### 1. Timestamp Format Issues

**Error**: `assigned_at must be ISO8601 with Z suffix`

**Cause**: Timestamp uses space or timezone offset instead of required format

**Fix**:
```yaml
# ❌ Before
assigned_at: 2026-02-09 04:40:00+00:00

# ✅ After
assigned_at: 2026-02-09T04:40:00Z
```

### 2. Missing Result Block

**Error**: `result block required for completed tasks`

**Cause**: Task has `status: done` but no result block

**Fix**:
```yaml
status: done
result:
  summary: "Task completed successfully"
  artefacts:
    - path/to/created/file.py
```

### 3. Invalid Result Artefacts Structure

**Error**: `result.artefacts/artifacts must be a list of strings`

**Cause**: Using nested structure or non-list format

**Fix**:
```yaml
# ❌ Before
result:
  summary: "Done"
  artifacts_created:
    - file1.py

# ✅ After
result:
  summary: "Done"
  artifacts:
    - file1.py
```

### 4. Invalid Status Value

**Error**: `invalid status 'complete', expected one of ['assigned', 'blocked', 'done', 'error', 'inbox', 'in_progress', 'new']`

**Cause**: Using a status value not defined in TaskStatus enum

**Fix**: Use only valid TaskStatus enum values (see table above)

## Validator Maintenance

### Adding New Validation Rules

1. **Update `validate-task-schema.py`**: Add validation logic
2. **Update this README**: Document the new rule
3. **Add test cases**: Create test fixtures in `tests/fixtures/tasks/`
4. **Update CHANGELOG**: Document the validation change

### Extending Enum Values

1. **Update `src/common/types.py`**: Add new enum value
2. **Validator automatically picks up new values** (single source of truth)
3. **Update documentation**: Document new status in this README
4. **Add migration path**: If needed, create migration script

## Related Documentation

- **ADR-043**: Status Enumeration Standard
- **ADR-042**: Shared Task Domain Model
- **Task Schema**: `src/common/task_schema.py`
- **Type Definitions**: `src/common/types.py`

## Testing

### Running Tests

```bash
# Unit tests for validator logic
pytest tests/unit/validators/test_task_validator.py

# Integration tests with real task files
pytest tests/integration/validators/test_task_validation.py
```

### Test Fixtures

Test fixtures are located in `tests/fixtures/tasks/`:
- `valid/` - Examples of correct task files
- `invalid/` - Examples of common errors

## Troubleshooting

### Validator Not Found

If you see `❌ Validator not found: validation/validate-task-schema.py`:

**Solution**: The validator has been moved to `tools/validators/`. Update your scripts or use the wrapper at `tools/scripts/validate-task.sh`.

### Import Errors

If you see `ModuleNotFoundError: No module named 'common'`:

**Solution**: The validator automatically adds `src/` to Python path. Ensure you're running from the repository root.

### Performance Issues

For large batches of files:

```bash
# Parallel validation (if GNU parallel installed)
find work/collaboration/done -name "*.yaml" | \
  parallel -j 4 python tools/validators/validate-task-schema.py {}
```

## Contact

For validator issues or enhancement requests:
- **DevOps Danny**: Build automation and validation infrastructure
- **Python Pedro**: Python implementation and testing
- **Curator Claire**: Task file maintenance and cleanup
