# External Memory

This directory provides a shared space for agents to swap information in and out of their active context.

## Purpose

Agents have limited context windows and may need to:
- Offload working notes temporarily
- Share intermediate artifacts with other agents
- Store partial results for later retrieval
- Preserve state across multiple invocations

## Usage Guidelines

1. **File Naming**: Use descriptive names with timestamps: `YYYY-MM-DDTHHMM-agent-description.{ext}`
2. **Organization**: Create agent-specific subdirectories when storing multiple artifacts
3. **Cleanup**: Remove artifacts after they are no longer needed
4. **Documentation**: Include a brief note in each file explaining its purpose and lifecycle

## Examples

```
external_memory/
  architect/
    2025-11-26T1030-design-draft-v1.md
    2025-11-26T1045-stakeholder-feedback.json
  synthesizer/
    2025-11-26T1100-aggregation-checkpoint.yaml
```

## Related Directories

- `work/reports/` - Final agent outputs and reports
- `work/collaboration/` - Orchestration and task coordination
- `work/notes/` - Persistent project notes and planning artifacts
