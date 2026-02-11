# Task Templates

This directory contains modular task templates for the asynchronous multi-agent orchestration system.

## Template Structure

The task templates have been split into separate files for clarity and ease of use:

### Core Templates

| File                     | Purpose                     | When to Use                               |
|--------------------------|-----------------------------|-------------------------------------------|
| **task-base.yaml**       | Required fields only        | Starting point for all tasks              |
| **task-context.yaml**    | Optional context fields     | Add details to guide agent execution      |
| **task-timestamps.yaml** | System-populated timestamps | Reference only - shows what system adds   |
| **task-result.yaml**     | Result object structure     | Reference only - agents add on completion |
| **task-error.yaml**      | Error object structure      | Reference only - agents add on failure    |
| **task-examples.yaml**   | Complete working examples   | Copy and adapt for your use case          |

### Legacy Template

| File                     | Purpose                      | Status                   |
|--------------------------|------------------------------|--------------------------|
| **task-descriptor.yaml** | Original monolithic template | Maintained for reference |

## Quick Start

### Creating a New Task

1. **Start with task-base.yaml**
   ```bash
   cp templates/task-base.yaml work/inbox/2025-11-23T1430-structural-repomap.yaml
   ```

2. **Update required fields**
    - Set `id` to match filename (without .yaml)
    - Set `agent` to target agent name
    - List `artefacts` to be created/modified

3. **Add optional context** (from task-context.yaml)
    - Add `title` for human readability
    - Set `mode` if needed (/analysis-mode, /creative-mode, /meta-mode)
    - Set `priority` if urgent (critical, high, normal, low)
    - Add `context` with repo, branch, notes

4. **Add timestamps**
    - Set `created_at` to current UTC time (YYYY-MM-DDTHH:MM:SSZ)
    - Set `created_by` to your username or agent name

5. **Commit and push**
   ```bash
   git add work/inbox/2025-11-23T1430-structural-repomap.yaml
   git commit -m "Create task: structural repo mapping"
   git push
   ```

## Template Details

### task-base.yaml - Required Fields

Minimal template with only required fields:

- `id`: Unique identifier matching filename
- `agent`: Target agent name
- `status`: Always "new" for new tasks
- `artefacts`: List of files to create/modify

**Use when:** Creating a simple, straightforward task.

### task-context.yaml - Optional Fields

Additional context to guide agent execution:

- `title`: Human-readable task description
- `mode`: Reasoning mode for agent
- `priority`: Task urgency level
- `context`: Repo info, branch, notes, dependencies

**Use when:** Task needs specific guidance or has special requirements.

### task-timestamps.yaml - System Timestamps

Timestamps automatically populated by the system:

- `created_at`, `created_by`: Set by task creator
- `assigned_at`: Set by Agent Orchestrator
- `started_at`: Set by agent when starting
- `completed_at`: Set by agent when done

**Use when:** Understanding task lifecycle timing.

### task-result.yaml - Completion Result

Result object added by agent on successful completion:

- `summary`: What was accomplished
- `artefacts`: What was actually created/modified
- `next_agent`: Optional handoff to another agent
- `next_task_*`: Details for follow-up task
- `completed_at`: Completion timestamp

**Do NOT include when creating tasks.** Agents add this when completing work.

### task-error.yaml - Error Information

Error object added by agent on failure:

- `message`: What went wrong
- `timestamp`: When error occurred
- `agent`: Which agent encountered error
- `retry_count`: Number of retry attempts
- `stacktrace`: Optional detailed trace

**Do NOT include when creating tasks.** Agents add this when encountering failures.

### task-examples.yaml - Working Examples

Five complete examples demonstrating:

1. Simple documentation task
2. Architecture task with handoff
3. Visual design task (creative mode)
4. Task with dependencies
5. Multi-step workflow (chained tasks)

**Use when:** Learning the system or adapting an existing pattern.

## Common Patterns

### Pattern 1: Simple Task

```yaml
id: "2025-11-23T1430-structural-repomap"
agent: "structural"
status: "new"
artefacts:
  - "docs/REPO_MAP.md"
created_at: "2025-11-23T14:30:00Z"
created_by: "stijn"
```

### Pattern 2: Task with Context

```yaml
id: "2025-11-23T1500-architect-adr"
agent: "architect"
status: "new"
title: "Create ADR for API versioning"
mode: "/analysis-mode"
priority: "high"
artefacts:
  - "${DOC_ROOT}/architecture/adrs/ADR-006.md"
context:
  repo: "sddevelopment-be/app"
  branch: "feature/api"
  notes:
    - "Consider REST and GraphQL approaches"
created_at: "2025-11-23T15:00:00Z"
created_by: "planning-agent"
```

### Pattern 3: Task with Dependencies

```yaml
id: "2025-11-23T1700-curator-consistency"
agent: "curator"
status: "new"
artefacts:
  - "work/curator/report.md"
context:
  dependencies:
    - "2025-11-23T1430-structural-repomap"
    - "2025-11-23T1500-architect-adr"
created_at: "2025-11-23T17:00:00Z"
created_by: "human"
```

## Workflow Integration

### Task Creation → Execution → Completion

1. **Human/Planning Agent**: Creates task in `work/inbox/` using task-base.yaml
2. **Agent Orchestrator**: Moves to `work/assigned/<agent>/`, adds `assigned_at`
3. **Assigned Agent**: Updates status to `in_progress`, adds `started_at`
4. **Assigned Agent**: Performs work, creates artifacts
5. **Assigned Agent**: Adds result block (from task-result.yaml structure)
6. **Assigned Agent**: Updates status to `done`, moves to `work/done/`
7. **Agent Orchestrator**: If `next_agent` specified, creates follow-up task

### Error Handling

1. **Agent encounters error** during execution
2. **Agent adds error block** (from task-error.yaml structure)
3. **Agent updates status** to `error`
4. **Agent leaves task** in `work/assigned/<agent>/` for human review
5. **Human reviews and decides**: retry (reset to assigned) or archive

## Validation

All task files should follow these rules:

1. **ID Format**: YYYY-MM-DDTHHMM-agent-slug
2. **Agent Name**: Must exist as directory under work/assigned/
3. **Status Values**: new | assigned | in_progress | done | error
4. **Artefacts**: Non-empty list of relative paths
5. **Timestamps**: ISO 8601 format with UTC timezone (Z suffix)
6. **Result**: Only present when status is "done"
7. **Error**: Only present when status is "error"

Validate using: `work/scripts/validate-task-schema.py` (when implemented)

## Related Documentation

- **User Guide**: `docs/HOW_TO_USE/multi-agent-orchestration.md`
- **Architecture**: `${DOC_ROOT}/architecture/design/async_multiagent_orchestration.md`
- **Technical Design**: `${DOC_ROOT}/architecture/design/async_orchestration_technical_design.md`
- **Work Directory**: `work/README.md`
- **ADRs**:
    - ADR-YYY (coordination pattern): File-Based Asynchronous Agent Coordination
    - ADR-MMM (lifecycle pattern): Task Lifecycle and State Management
    - ADR-ZZZ (structure pattern): Work Directory Structure
    - ADR-QQQ (coordinator pattern): Coordinator Agent Pattern

## Questions?

- **Which template do I use?** Start with task-base.yaml, add from task-context.yaml as needed
- **Do I include result block?** No, agents add it on completion
- **Do I include error block?** No, agents add it on failure
- **What about timestamps?** Set created_at and created_by, system adds rest
- **Can I see examples?** Yes, check task-examples.yaml for complete examples

---

_Last updated: 2025-11-23_  
_Version: 1.0.0_
