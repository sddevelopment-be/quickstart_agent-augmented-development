# Task Management Scripts

Simple Python scripts for managing task lifecycle and location. These scripts are designed to be used by agents, orchestrators, and automated workflows.

## Scripts Overview

### 1. `list_open_tasks.py` - List Open Tasks

Lists all tasks that are not in terminal states (done/error).

**Usage:**
```bash
python list_open_tasks.py [OPTIONS]

# Examples
python list_open_tasks.py                           # List all open tasks
python list_open_tasks.py --status assigned         # Filter by status
python list_open_tasks.py --agent python-pedro      # Filter by agent
python list_open_tasks.py --priority high           # Filter by priority
python list_open_tasks.py --format json             # Output as JSON
```

**Options:**
- `--work-dir PATH`: Work collaboration directory (default: `work/collaboration`)
- `--status {assigned,in_progress,blocked,new,inbox}`: Filter by task status
- `--agent AGENT`: Filter by agent name
- `--priority {low,medium,high,critical}`: Filter by priority level
- `--format {table,json}`: Output format (default: table)

---

### 2. `start_task.py` - Start Task

Marks a task as `in_progress` by updating its status and adding a `started_at` timestamp. The task remains in the `assigned/{agent}/` directory.

**Usage:**
```bash
python start_task.py TASK_ID [OPTIONS]

# Example
python start_task.py 2026-02-09T2033-python-pedro-test-task
```

**Options:**
- `--work-dir PATH`: Work collaboration directory (default: `work/collaboration`)

**Requirements:**
- Task must be in `assigned` status
- Task file must exist in `assigned/{agent}/` directory

**Behavior:**
- Updates `status` from `assigned` to `in_progress`
- Adds `started_at` timestamp in ISO8601 format with Z suffix
- Task remains in same location

---

### 3. `complete_task.py` - Complete Task

Marks a task as `done` and moves it from `assigned/{agent}/` to `done/{agent}/`.

**Usage:**
```bash
python complete_task.py TASK_ID [OPTIONS]

# Examples
python complete_task.py 2026-02-09T2033-python-pedro-test-task
python complete_task.py 2026-02-09T2033-python-pedro-test-task --force
```

**Options:**
- `--work-dir PATH`: Work collaboration directory (default: `work/collaboration`)
- `--force`: Skip result validation and complete anyway

**Requirements:**
- Task must have a `result` block (unless `--force` is used)
- Task must exist in `assigned/{agent}/` directory

**Behavior:**
- Updates `status` to `done`
- Adds `completed_at` timestamp
- Moves task from `assigned/{agent}/` to `done/{agent}/`
- Validates `result` block exists (can be skipped with `--force`)

---

### 4. `freeze_task.py` - Freeze Task

Moves a task to the `fridge/` directory (pause/defer) with a freeze reason and timestamp.

**Usage:**
```bash
python freeze_task.py TASK_ID --reason REASON [OPTIONS]

# Example
python freeze_task.py 2026-02-09T2033-python-pedro-test-task --reason "Blocked on dependency XYZ"
```

**Options:**
- `--reason REASON`: Reason for freezing the task (required)
- `--work-dir PATH`: Work collaboration directory (default: `work/collaboration`)

**Requirements:**
- Task must exist in `assigned/{agent}/` directory
- Reason must be provided and non-empty

**Behavior:**
- Adds `frozen_at` timestamp
- Adds `freeze_reason` field
- Preserves original `status`
- Moves task from `assigned/{agent}/` to `fridge/`

---

## Architecture & Design

### Related ADRs
- **ADR-042**: Shared Task Domain Model
- **ADR-043**: Status Enumeration Standard

### Dependencies
- `src/common/task_schema.py`: Task file I/O operations
- `src/common/types.py`: TaskStatus enum and validation

### Status Flow
```
NEW → INBOX → ASSIGNED → IN_PROGRESS → DONE
                    ↓
                BLOCKED
```

**Terminal States:** `done`, `error`  
**Active States:** `assigned`, `in_progress`, `blocked`  
**Pending States:** `new`, `inbox`

### Directory Structure
```
work/collaboration/
├── assigned/
│   ├── python-pedro/
│   ├── backend-dev/
│   └── ...
├── done/
│   ├── python-pedro/
│   ├── backend-dev/
│   └── ...
└── fridge/
```

---

## Testing

Comprehensive acceptance tests are available in `tests/integration/test_task_management_scripts.py`.

**Run tests:**
```bash
pytest tests/integration/test_task_management_scripts.py -v
```

**Test coverage:**
- All scripts have 16 acceptance tests
- Tests verify CLI interface, error handling, and data integrity
- Tests use isolated temporary directories

---

## Error Handling

All scripts provide clear error messages:

- **Task not found**: Returns exit code 1 with descriptive message
- **Invalid state**: Returns exit code 1 explaining required state
- **Missing fields**: Returns exit code 1 with field requirements
- **Validation errors**: Returns exit code 1 with validation details

**Exit codes:**
- `0`: Success
- `1`: Error (with stderr message)

---

## Development Guidelines

These scripts follow Python Pedro's development standards:

✅ **ATDD/TDD**: Acceptance tests written first, then implementation  
✅ **Type Safety**: Full type hints with mypy validation  
✅ **Code Quality**: ruff linting, PEP 8 compliance  
✅ **Documentation**: Comprehensive docstrings and CLI help  
✅ **Locality of Change**: Minimal file operations, preserves data integrity

**Directive Compliance:**
- 016 (ATDD): Acceptance criteria defined as executable tests
- 017 (TDD): RED-GREEN-REFACTOR cycle applied
- 021 (Locality): Minimal changes, single responsibility

---

## Integration Examples

### Orchestrator Integration

```python
import subprocess
import json

# List tasks for agent
result = subprocess.run(
    ["python", "tools/scripts/list_open_tasks.py", "--agent", "python-pedro", "--format", "json"],
    capture_output=True,
    text=True
)
tasks = json.loads(result.stdout)

# Start first assigned task
for task in tasks:
    if task["status"] == "assigned":
        subprocess.run(["python", "tools/scripts/start_task.py", task["id"]])
        break
```

### Bash Automation

```bash
#!/bin/bash
# Complete all tasks with results

for task in work/collaboration/assigned/python-pedro/*.yaml; do
    task_id=$(basename "$task" .yaml)
    
    # Check if task has result
    if grep -q "^result:" "$task"; then
        python tools/scripts/complete_task.py "$task_id"
        echo "Completed: $task_id"
    fi
done
```

---

## Future Enhancements

Potential improvements (not yet implemented):

- [ ] Batch operations (complete multiple tasks)
- [ ] Task filtering by date range
- [ ] Task statistics and reporting
- [ ] Unfreeze task operation
- [ ] Task assignment transfer
- [ ] Dry-run mode for testing

---

**Maintained by:** Python Pedro  
**Last Updated:** 2026-02-10  
**Version:** 1.0.0
