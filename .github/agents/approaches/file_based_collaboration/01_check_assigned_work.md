# Step 1: Check for Assigned Work

## When to Use

- Upon agent initialization
- When awaiting direction
- Before asking humans for tasks

## Procedure

1. Check `${WORKSPACE_ROOT}/collaboration/assigned/<your-agent-name>/` for task YAML files
2. If tasks exist, proceed to Step 2 (Prioritize Tasks)
3. If no tasks exist, await human instruction or request clarification

## Example

```bash
ls ${WORKSPACE_ROOT}/collaboration/assigned/curator/*.yaml
```

If files are present, you have assigned work to process.

## Next Steps

- **Tasks found**: Load [02_prioritize_tasks.md](02_prioritize_tasks.md)
- **No tasks**: Await human guidance or check inbox status
