# Step 5: Create Tasks

## When to Use

When you need to create a new task that is NOT a delegation (for delegation, use Step 4).

## Task Creation Steps

1. Create YAML file in `work/collaboration/inbox/`
2. Name: `YYYY-MM-DDTHHMM-<agent>-<slug>.yaml`
3. Include required fields:
   - `id`: Matches filename without extension
   - `agent`: Target agent name
   - `status`: Set to `"new"`
   - `artefacts`: List of files to create/modify
   - `title`: Human-readable description
   - `created_at`: ISO 8601 timestamp
   - `created_by`: Your agent name

## Optional Fields

- `priority`: `critical` | `high` | `normal` | `low`
- `mode`: Reasoning mode (`/analysis-mode`, `/creative-mode`, etc.)
- `context`: Additional information, notes, references

## Example

```yaml
id: 2025-11-26T1030-curator-review-templates
agent: curator
status: new
title: "Review and update template structure"
priority: normal
artefacts:
  - docs/templates/README.md
  - docs/templates/architecture/
context:
  repo: "sddevelopment-be/quickstart_agent-augmented-development"
  notes:
    - "Check for consistency with new work structure"
    - "Update references to work/collaboration paths"
created_at: "2025-11-26T10:30:00Z"
created_by: "architect"
```

## Template Reference

See `docs/templates/task-descriptor.yaml` for complete schema documentation.

## Next Steps

The Agent Orchestrator will automatically assign the task to the specified agent.
