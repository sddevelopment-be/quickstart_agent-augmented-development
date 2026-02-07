# File-Based Collaboration Approach

## Overview

The file-based collaboration approach enables asynchronous, transparent, Git-native multi-agent coordination through YAML task files that move through a defined lifecycle.

**Core Principle:** All inter-agent coordination happens through YAML task files in `${WORKSPACE_ROOT}/collaboration/`.

## Task Lifecycle

```
new → assigned → in_progress → done → archive
                     ↓
                   error
```

## Approach Steps

When working within the file-based orchestration system, load only the step relevant to your current phase:

| Step                | File                                                   | When to Load                              |
|---------------------|--------------------------------------------------------|-------------------------------------------|
| 1. Check for Work   | [01_check_assigned_work.md](01_check_assigned_work.md) | Upon initialization or awaiting direction |
| 2. Prioritize Tasks | [02_prioritize_tasks.md](02_prioritize_tasks.md)       | When multiple tasks are assigned          |
| 3. Process Tasks    | [03_process_tasks.md](03_process_tasks.md)             | Actively working on a task                |
| 4. Delegate Work    | [04_delegate_work.md](04_delegate_work.md)             | Encountering out-of-scope work            |
| 5. Create Tasks     | [05_create_tasks.md](05_create_tasks.md)               | Need to create new tasks (not delegation) |
| 6. Handle Errors    | [06_error_handling.md](06_error_handling.md)           | Task cannot be completed                  |
| 7. Log Work         | [07_log_work.md](07_log_work.md)                       | After completing any task                 |

## Automation Scripts

- `ops/scripts/orchestration/agent_orchestrator.py` - Assigns tasks, creates follow-ups, monitors timeouts
- `ops/scripts/orchestration/agent_base.py` - Base class for agent implementations
- Task validation: `validation/validate-task-schema.py`

## Quick Reference

- **Inbox**: `${WORKSPACE_ROOT}/collaboration/inbox/` - New tasks
- **Assigned**: `${WORKSPACE_ROOT}/collaboration/assigned/<agent>/` - Your tasks
- **Done**: `${WORKSPACE_ROOT}/collaboration/done/<agent>/` - Completed work
- **Logs**: `work/reports/logs/<agent>/` - Execution logs

## Related Documentation

- `${WORKSPACE_ROOT}/collaboration/README.md` - Collaboration directory guide
- `work/README.md` - Complete work directory documentation
- `${DOC_ROOT}/templates/task-descriptor.yaml` - Task YAML schema
