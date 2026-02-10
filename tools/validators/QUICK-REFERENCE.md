# Task Validation Quick Reference Card

## One-Line Commands

### Validate Single File
```bash
python tools/validators/validate-task-schema.py work/collaboration/done/agent/task.yaml
```

### Validate All Tasks in Directory
```bash
python tools/validators/validate-task-schema.py work/collaboration/done/agent/*.yaml
```

### Validate All Done Tasks
```bash
find work/collaboration/done -name "*.yaml" -type f | xargs python tools/validators/validate-task-schema.py
```

### Using Shell Wrapper
```bash
./tools/scripts/validate-task.sh work/collaboration/done/agent/*.yaml
```

---

## Common Fixes

### Fix Timestamp Format
```yaml
# Before: assigned_at: 2026-02-09 04:40:00+00:00
# After:
assigned_at: 2026-02-09T04:40:00Z
```

### Add Result Block (status="done")
```yaml
status: done
result:
  summary: "Task completed successfully"
  artefacts:
    - path/to/file.py
```

### Fix Result Artefacts
```yaml
# Before: result.artifacts_created
# After:
result:
  artefacts:  # or 'artifacts'
    - file1.py
    - file2.md
```

---

## Valid TaskStatus Values

✅ `new` | `inbox` | `assigned` | `in_progress` | `blocked` | `done` | `error`

---

## Quick Help

**Full Documentation**: `tools/validators/README.md`  
**Fix Procedures**: `tools/validators/RUNBOOK-task-validation-fixes.md`  
**Support**: DevOps Danny, Python Pedro, Curator Claire
