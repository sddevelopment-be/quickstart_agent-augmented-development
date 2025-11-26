<!-- The following information is to be interpreted literally -->
# 019 File-Based Collaboration Framework Directive

Purpose: Guide agents in participating in the asynchronous file-based orchestration system for multi-agent collaboration.

## 1. Framework Overview

The `work/collaboration/` directory implements a task-based workflow where agents coordinate through file movements, enabling transparent, Git-native, asynchronous collaboration.

**Core Principle:** All inter-agent coordination happens through YAML task files that move through a defined lifecycle.

## 2. Task Lifecycle

Tasks progress through these states:

```
new → assigned → in_progress → done → archive
                     ↓
                   error
```

- **new**: Tasks await assignment in `work/collaboration/inbox/`
- **assigned**: Tasks are routed to `work/collaboration/assigned/<agent-name>/`
- **in_progress**: Agent actively working on the task
- **done**: Completed tasks move to `work/collaboration/done/<agent-name>/`
- **error**: Failed tasks requiring human intervention
- **archive**: Old completed tasks in `work/collaboration/archive/`

## 3. Agent Responsibilities

### 3.1 Check for Assigned Work

Upon invocation or when awaiting direction:

1. Check `work/collaboration/assigned/<your-agent-name>/` for task YAML files
2. If tasks exist, process them according to priority
3. If no tasks exist, await human instruction or request clarification

### 3.2 Prioritize Tasks

When multiple tasks are assigned:

1. **Critical** priority first (system failures, blocking issues)
2. **High** priority second (time-sensitive deliverables)
3. **Normal** priority third (standard workflow items)
4. **Low** priority last (nice-to-have improvements)

**Default:** If priority is not specified, treat as **normal**.

### 3.3 Process Tasks

For each task:

1. **Read task YAML** from `work/collaboration/assigned/<your-agent-name>/<task-file>.yaml`
2. **Update status** to `in_progress` and set `started_at` timestamp
3. **Perform specialized work** according to task description and artifacts
4. **Create/modify artifacts** listed in the `artefacts` field
5. **Add result block** with summary, artifacts created, and optional next agent
6. **Update status** to `done` and set `completed_at` timestamp
7. **Move task file** to `work/collaboration/done/<your-agent-name>/`

### 3.4 Log Work

Create execution logs in `work/reports/logs/<your-agent-name>/` documenting:

- Task processing decisions
- Work performed
- Reasoning and trade-offs
- Any issues encountered

## 4. Specialization & Delegation

### 4.1 Recognize Your Limits

You are a **specialist** with defined expertise. When encountering work outside your core competency:

- **DO NOT** attempt work beyond your specialization
- **DO** identify the appropriate specialist agent
- **DO** delegate through task creation

### 4.2 Delegate Through Tasks

To delegate work to another agent:

1. Add a `result` block to your task with:
   - `next_agent`: Name of the specialist agent
   - `next_task_title`: Clear description of delegated work
   - `next_artefacts`: Files the next agent should create/modify
   - `next_task_notes`: Context, constraints, or guidance

2. Example:
   ```yaml
   result:
     summary: "Completed initial architecture design"
     artefacts:
       - docs/architecture/design.md
     next_agent: "diagrammer"
     next_task_title: "Create architecture diagram from design document"
     next_artefacts:
       - docs/architecture/diagrams/system-overview.puml
     next_task_notes:
       - "Focus on component interactions"
       - "Use PlantUML C4 model notation"
     completed_at: "2025-11-26T10:30:00Z"
   ```

3. The Agent Orchestrator will automatically create the follow-up task in `work/collaboration/inbox/`

### 4.3 Common Delegation Patterns

| When You Need... | Delegate To... |
|------------------|----------------|
| Architecture decisions | `architect` |
| Code implementation | `backend-dev`, `frontend` |
| Diagram creation | `diagrammer` |
| Documentation writing | `writer-editor` |
| Structural consistency | `curator` |
| Data aggregation | `synthesizer` |
| Terminology validation | `lexical` |
| Repository mapping | `bootstrap-bill` |

## 5. Task Creation

To create a new task (not as delegation):

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

## 6. Error Handling

When a task cannot be completed:

1. Update `status` to `"error"`
2. Add `error` block with:
   - `message`: Clear description of the problem
   - `details`: Technical specifics, stack traces, or context
   - `failed_at`: ISO 8601 timestamp
3. Leave task in `work/collaboration/assigned/<your-agent-name>/`
4. Log detailed error information in `work/reports/logs/<your-agent-name>/`

Human intervention will be required to resolve error-state tasks.

## 7. Coordination Artifacts

Monitor these files for system-wide coordination:

- `work/collaboration/AGENT_STATUS.md`: Real-time agent activity dashboard
- `work/collaboration/HANDOFFS.md`: Agent-to-agent transition log
- `work/collaboration/WORKFLOW_LOG.md`: System orchestration events

## 8. Best Practices

1. **Check assigned work first** before asking humans for direction
2. **Process one task at a time** to maintain focus and quality
3. **Delegate early** when encountering out-of-scope work
4. **Be specific** in delegation instructions to minimize back-and-forth
5. **Update status promptly** to maintain system visibility
6. **Log comprehensively** for audit trails and debugging
7. **Respect priorities** to align with project goals
8. **Trust the system** - handoffs work asynchronously, no immediate confirmation needed

## 9. Integration with Other Directives

This directive complements:

- **012 Common Operating Procedures**: General behavioral norms
- **014 Work Log Creation**: Logging standards
- **009 Role Capabilities**: Understanding your specialization boundaries

## 10. Usage

Load this directive when:

- Operating in a multi-agent environment
- Processing asynchronous tasks
- Coordinating with other specialist agents
- Participating in file-based workflows

```
/require-directive 019
```

## 11. Related Documentation

- `work/README.md`: Comprehensive work directory documentation
- `work/collaboration/README.md`: Collaboration-specific guidance
- `docs/templates/task-descriptor.yaml`: Task YAML schema
- `docs/architecture/adrs/ADR-002-file-based-async-coordination.md`: Design rationale

---

**Remember:** The file-based orchestration system enables seamless, transparent, asynchronous collaboration. Trust the process, focus on your specialization, and delegate effectively.
