# Step 4: Delegate Work

## When to Use

When encountering work outside your core competency or specialization.

## Delegation Principle

You are a **specialist** with defined expertise:

- **DO NOT** attempt work beyond your specialization
- **DO** identify the appropriate specialist agent
- **DO** delegate through task creation

## How to Delegate

Add a `result` block to your task with delegation fields:

- `next_agent`: Name of the specialist agent
- `next_task_title`: Clear description of delegated work
- `next_artefacts`: Files the next agent should create/modify
- `next_task_notes`: Context, constraints, or guidance

### Example

```yaml
result:
  summary: "Completed initial architecture design"
  artefacts:
    - ${DOC_ROOT}/architecture/design.md
  next_agent: "diagrammer"
  next_task_title: "Create architecture diagram from design document"
  next_artefacts:
    - ${DOC_ROOT}/architecture/diagrams/system-overview.puml
  next_task_notes:
    - "Focus on component interactions"
    - "Use PlantUML C4 model notation"
  completed_at: "2025-11-26T10:30:00Z"
```

The Agent Orchestrator automatically creates the follow-up task in `${WORKSPACE_ROOT}/collaboration/inbox/`.

## Common Delegation Patterns

| When You Need...       | Delegate To...            |
|------------------------|---------------------------|
| Architecture decisions | `architect`               |
| Code implementation    | `backend-dev`, `frontend` |
| Diagram creation       | `diagrammer`              |
| Documentation writing  | `writer-editor`           |
| Structural consistency | `curator`                 |
| Data aggregation       | `synthesizer`             |
| Terminology validation | `lexical`                 |
| Repository mapping     | `bootstrap-bill`          |

## Next Steps

Return to [03_process_tasks.md](03_process_tasks.md) to complete your task with the delegation included.
