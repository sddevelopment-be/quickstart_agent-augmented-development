# File-Based Asynchronous Agent Orchestration

**Approach Type:** Coordination Pattern  
**Version:** 1.0.0  
**Last Updated:** 2025-11-23  
**Status:** Active  
**Target Location:** `.github/agents/approaches/file-based-orchestration.md`

## Overview

This approach describes how to implement asynchronous multi-agent coordination using a file-based task workflow. Tasks are represented as YAML files that move through directories corresponding to their lifecycle states, providing transparent, Git-native coordination without requiring real-time communication or complex orchestration frameworks.

## Core Principles

### 1. Simplicity
All workflows derive from file movements. No frameworks, no servers, no complex protocols—just files moving through directories.

### 2. Transparency
Every state transition is visible in Git. Every task has a readable YAML representation. Every agent action leaves an audit trail.

### 3. Determinism
No hidden API calls or opaque queues. Task execution is predictable and repeatable.

### 4. Composability
Each agent handles one domain. Complex workflows emerge naturally from simple handoffs via `next_agent` metadata.

### 5. Traceability
Every task leaves a complete audit trail from creation through completion or failure.

## When to Use This Approach

**Use file-based orchestration when:**
- Multiple specialized agents need to collaborate on complex workflows
- Work must be asynchronous (agents may operate at different times)
- Complete audit trails are required for compliance or debugging
- State management must be visible and Git-trackable
- Coordination overhead should be minimal

**Do NOT use this approach when:**
- Real-time coordination is required (use synchronous APIs instead)
- Task volume exceeds filesystem performance limits (thousands per minute)
- State must be kept private or encrypted (files are visible in Git)
- Agents need to negotiate or coordinate dynamically

## Directory Structure

```
work/
  inbox/              # New tasks awaiting assignment
  assigned/           # Tasks assigned to specific agents
    <agent-name>/     # One directory per agent
  done/               # Completed tasks with results
  archive/            # Long-term task retention (by month)
  logs/               # Agent execution logs
  collaboration/      # Cross-agent coordination artifacts
  schemas/            # Task YAML schema definitions
  scripts/            # Utility scripts for orchestration
```

## Task Lifecycle

Tasks progress through well-defined states:

```
┌─────┐     ┌──────────┐     ┌─────────────┐     ┌──────┐     ┌─────────┐
│ new │ ──> │ assigned │ ──> │ in_progress │ ──> │ done │ ──> │ archive │
└─────┘     └──────────┘     └─────────────┘     └──────┘     └─────────┘
                                     │
                                     │
                                     v
                                 ┌───────┐
                                 │ error │
                                 └───────┘
```

### State Descriptions

- **new**: Task created in `work/inbox/`, awaiting assignment
- **assigned**: Task moved to `work/assigned/<agent>/`, awaiting agent pickup
- **in_progress**: Agent has started work on the task
- **done**: Task completed successfully, moved to `work/done/`
- **error**: Task failed, requires human intervention
- **archive**: Old completed tasks, organized by month in `work/archive/`

## Task File Format

Every task is represented by a single YAML file following this naming convention:

```
YYYY-MM-DDTHHMM-<agent>-<slug>.yaml
```

**Example:** `2025-11-23T1430-structural-repomap.yaml`

### Required Fields

see: [task-descriptor.yaml](/docs/templates/agent-tasks/task-descriptor.yaml)

### Optional Fields

see: [task-descriptor.yaml](/docs/templates/agent-tasks/task-descriptor.yaml)

### Timestamps (Auto-populated)

see: [task-timestamps.yaml](/docs/templates/agent-tasks/task-timestamps.yaml)

### Result Block (Added on completion)

see: [task-result.yaml](/docs/templates/agent-tasks/task-result.yaml)

## Implementation Steps

### For Human Operators

**Creating a Task:**

1. Create YAML file in `work/inbox/` using the template in [/docs/templates/agent-tasks/task-base.yaml](/docs/templates/agent-tasks/task-base.yaml)
2. Name it: `YYYY-MM-DDTHHMM-<agent>-<slug>.yaml`
3. Specify target agent, artifacts, and context
4. Commit and push to Git

**Monitoring Progress:**

1. Check task location: `find work/ -name "task-id.yaml"`
2. View task status: `cat work/assigned/<agent>/task-id.yaml`
3. Check collaboration logs: `cat work/collaboration/WORKFLOW_LOG.md`

### For Agents

**Picking Up a Task:**

1. Poll `work/assigned/<my-name>/` directory
2. Find YAML file with `status: assigned`
3. Update `status: in_progress` and add `started_at` timestamp
4. Commit the status update

**Processing the Task:**

1. Read task requirements from YAML
2. Perform specialized work according to agent profile
3. Create or modify artifacts listed in `artefacts` field
4. Document approach in work log (required for orchestrated tasks)

**Completing the Task:**

1. Update task YAML with `result` block:
   - Summary of work completed
   - Actual artifacts created
   - Next agent for handoff (if applicable)
   - Completion timestamp
2. Update `status: done`
3. Move task file from `work/assigned/<my-name>/` to `work/done/`
4. Create work log in `work/logs/` (see Directive 014)
5. Commit all changes together

**Handling Errors:**

1. Update task YAML with `error` block:
   - Error message
   - Timestamp
   - Agent name
   - Retry count
2. Update `status: error`
3. Leave task in `work/assigned/<my-name>/` for human review
4. Commit the error state

### For Agent Orchestrator

**Assignment Logic:**

1. Scan `work/inbox/` for files with `status: new`
2. For each task:
   - Validate task YAML against schema
   - Check dependencies are satisfied
   - Move file to `work/assigned/<agent>/`
   - Update `status: assigned` and add `assigned_at` timestamp
   - Commit assignment

**Handoff Processing:**

1. Scan `work/done/` for tasks with `result.next_agent`
2. For each handoff:
   - Create new task YAML in `work/inbox/`
   - Copy `next_task_title`, `next_artefacts`, `next_task_notes`
   - Set `created_by` to source agent name
   - Add dependency on source task ID
   - Commit new task

**Health Monitoring:**

1. Check for tasks stuck in `in_progress` beyond timeout (default: 2 hours)
2. Log warnings in `work/collaboration/WORKFLOW_LOG.md`
3. Optionally move timed-out tasks to `error` state

## Agent Handoffs

Handoffs enable multi-step workflows by chaining agents:

**Example Flow:**

1. Architect creates ADR → handoff to Writer-Editor
2. Writer-Editor polishes ADR → handoff to Diagrammer
3. Diagrammer creates architecture diagram → done

**Implementation:**

The source agent completes its task with:

```yaml
result:
  summary: "Created ADR-006 with recommendations"
  artefacts:
    - "docs/architecture/adrs/ADR-006.md"
  next_agent: "writer-editor"
  next_task_title: "Review and polish ADR-006"
  next_artefacts:
    - "docs/architecture/adrs/ADR-006.md"
  next_task_notes:
    - "Check for clarity"
    - "Ensure examples are understandable"
  completed_at: "2025-11-23T15:45:00Z"
```

The orchestrator automatically creates:

```yaml
id: 2025-11-23T1545-writer-editor-adr-review
agent: writer-editor
status: new
title: "Review and polish ADR-006"
artefacts:
  - "docs/architecture/adrs/ADR-006.md"
context:
  notes:
    - "Check for clarity"
    - "Ensure examples are understandable"
    - "Created by architect as handoff from task 2025-11-23T1700-architect-adr-api"
  dependencies:
    - 2025-11-23T1700-architect-adr-api
created_at: "2025-11-23T15:45:00Z"
created_by: "architect"
```

## Best Practices

### Task Creation

- **One task, one focus**: Keep tasks atomic and single-purpose
- **Clear artifacts**: List specific files, not vague goals
- **Provide context**: Add notes to guide the agent
- **Use dependencies**: Express task ordering explicitly

### Task Processing

- **Update status promptly**: Keep task states current
- **Commit frequently**: Make state transitions visible
- **Create work logs**: Document approach for framework tuning
- **Handoff thoughtfully**: Only chain when necessary

### Error Handling

- **Don't fail silently**: Update task status with error details
- **Provide diagnostics**: Include enough info for human debugging
- **Retry judiciously**: Increment retry count, don't loop forever
- **Escalate blockers**: Some errors require human intervention

### Coordination

- **Use collaboration artifacts**: Share state in `work/collaboration/`
- **Log significant events**: Update `WORKFLOW_LOG.md`
- **Track handoffs**: Maintain `HANDOFFS.md` for visibility
- **Monitor health**: Check `AGENT_STATUS.md` regularly

## Integration with Agent Profiles

Each agent profile should specify:

- **Work directory**: `work/assigned/<agent-name>/`
- **Output artifacts**: Where agent writes its deliverables
- **Specialization**: What types of tasks the agent handles
- **Handoff patterns**: Common next agents for workflows

Example from Curator profile:

```markdown
### Operating Procedure

- Poll `work/assigned/curator/` for tasks with `status: assigned`
- Update status to `in_progress` when starting work
- Perform structural consistency audits as specified in task
- Write discrepancy reports to `work/curator/`
- Update task with `result` block and move to `work/done/`
- Create work log in `work/logs/` documenting approach
- Common handoffs: writer-editor (for polish), synthesizer (for integration)
```

## Validation

Use these checks to ensure correct implementation:

**Task YAML Validation:**
```bash
python work/scripts/validate-task-schema.py work/inbox/task.yaml
```

**Directory Structure:**
```bash
bash work/scripts/validate-work-structure.sh
```

**Task Lifecycle:**
- New tasks must be in `work/inbox/`
- Assigned tasks must be in `work/assigned/<agent>/`
- Completed tasks must be in `work/done/`
- Task files must not duplicate across directories

**Naming Convention:**
- Format: `YYYY-MM-DDTHHMM-<agent>-<slug>.yaml`
- ID must match filename without extension
- Agent name must match directory under `work/assigned/`

## Troubleshooting

### Task Stuck in "assigned"

**Symptoms:** Task hasn't moved to `in_progress`.

**Causes:**
- Agent orchestrator not running
- Agent not polling its directory
- Agent crashed before updating status

**Solutions:**
1. Check orchestrator logs
2. Verify agent is running and watching correct directory
3. Manually trigger agent if needed

### Task Stuck in "in_progress"

**Symptoms:** Task shows `in_progress` but no completion.

**Causes:**
- Agent timed out or crashed
- Task is genuinely taking a long time
- Agent forgot to update status

**Solutions:**
1. Check `WORKFLOW_LOG.md` for timeout warnings
2. Review agent logs for errors
3. Inspect task YAML for error details
4. May need to reset to `assigned` and retry

### Handoff Not Created

**Symptoms:** Source task completed with `next_agent` but no follow-up task.

**Causes:**
- Orchestrator didn't run after completion
- Orchestrator encountered error creating handoff
- Next agent name is invalid

**Solutions:**
1. Check orchestrator ran after task completion
2. Inspect `WORKFLOW_LOG.md` for handoff errors
3. Verify `next_agent` name matches a directory under `work/assigned/`
4. Manually create follow-up task if needed

## References

- **Technical Design:** `docs/architecture/design/async_orchestration_technical_design.md`
- **Task Template:** `docs/templates/task-descriptor.yaml`
- **Work Directory README:** `work/README.md`
- **User Guide:** `docs/HOW_TO_USE/multi-agent-orchestration.md`
- **Directives:**
  - 004: Documentation & Context Files
  - 008: Artifact Templates
  - 012: Common Operating Procedures
  - 014: Work Log Creation
- **ADRs:**
  - ADR-002: File-Based Asynchronous Agent Coordination
  - ADR-003: Task Lifecycle and State Management
  - ADR-004: Work Directory Structure
  - ADR-005: Coordinator Agent Pattern

## Change Log

| Version | Date       | Changes                                      |
|---------|------------|----------------------------------------------|
| 1.0.0   | 2025-11-23 | Initial approach documentation               |

---

_Maintained by: Development team, Curator Claire & Architect Alphonso_  
_For questions, see: `.github/agents/curator.agent.md` or `.github/agents/architect.agent.md`_

**Note:** This file should be moved to `.github/agents/approaches/file-based-orchestration.md` once the approaches directory is created.
