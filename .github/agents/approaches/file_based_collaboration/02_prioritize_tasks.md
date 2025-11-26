# Step 2: Prioritize Tasks

## When to Use

When multiple tasks are assigned to you.

## Priority Levels

Process tasks in this order:

1. **Critical** - System failures, blocking issues
2. **High** - Time-sensitive deliverables
3. **Normal** - Standard workflow items
4. **Low** - Nice-to-have improvements

**Default:** If priority is not specified in the task YAML, treat as **normal**.

## Implementation

```bash
# List tasks with priority field visible
grep -l "priority: critical" work/collaboration/assigned/<agent>/*.yaml
grep -l "priority: high" work/collaboration/assigned/<agent>/*.yaml
```

## Next Steps

Load [03_process_tasks.md](03_process_tasks.md) for the selected task.
