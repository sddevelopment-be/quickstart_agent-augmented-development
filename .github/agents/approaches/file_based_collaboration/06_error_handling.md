# Step 6: Error Handling

## When to Use

When a task cannot be completed due to errors, blockers, or issues beyond your capability.

## Error Handling Steps

1. Update `status` to `"error"` in the task YAML
2. Add `error` block with:
   - `message`: Clear description of the problem
   - `details`: Technical specifics, stack traces, or context
   - `failed_at`: ISO 8601 timestamp
3. Leave task in `work/collaboration/assigned/<your-agent-name>/`
4. Log detailed error information in `work/reports/logs/<your-agent-name>/`

## Example

```yaml
id: 2025-11-26T1030-curator-review-templates
agent: curator
status: error
title: "Review and update template structure"
# ... other fields ...
error:
  message: "Template directory structure conflicts with existing standards"
  details: |
    Found inconsistency in docs/templates/architecture/ naming conventions.
    Expected: ADR-XXX-description.md
    Found: adr-XXX-description.md (lowercase)
    Requires human decision on canonical format.
  failed_at: "2025-11-26T10:45:00Z"
```

## Important

- **Human intervention required** for error-state tasks
- **Do not delete or move** error tasks
- **Document thoroughly** to help humans resolve the issue
- **Escalate blockers** that affect other agents

## Next Steps

After documenting the error, proceed to [07_log_work.md](07_log_work.md) to create a work log explaining what was attempted and why it failed.
