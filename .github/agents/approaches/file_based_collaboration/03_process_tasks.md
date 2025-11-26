# Step 3: Process Tasks

## When to Use

When actively working on an assigned task.

## Processing Steps

1. **Read task YAML** from `work/collaboration/assigned/<your-agent-name>/<task-file>.yaml`
2. **Update status** to `in_progress` and set `started_at` timestamp (ISO 8601 format)
3. **Perform specialized work** according to task description and artifacts
4. **Create/modify artifacts** listed in the `artefacts` field
5. **Add result block** with:
   - `summary`: Brief description of work completed
   - `artefacts`: List of files created/modified
   - `next_agent` (optional): If delegating follow-up work
   - `next_task_title` (optional): Description of follow-up
   - `next_artefacts` (optional): Files for next agent
   - `next_task_notes` (optional): Context for next agent
6. **Update status** to `done` and set `completed_at` timestamp
7. **Move task file** to `work/collaboration/done/<your-agent-name>/`

## Result Block Example

```yaml
result:
  summary: "Completed directive refactoring"
  artefacts:
    - .github/agents/directives/019_file_based_collaboration.md
    - .github/agents/approaches/file_based_collaboration/
  completed_at: "2025-11-26T06:30:00Z"
```

## Next Steps

- Load [07_log_work.md](07_log_work.md) to document your work
- If delegation needed, load [04_delegate_work.md](04_delegate_work.md) before completing
- If errors occur, load [06_error_handling.md](06_error_handling.md)
