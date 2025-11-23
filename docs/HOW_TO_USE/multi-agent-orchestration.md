# Using the Multi-Agent Orchestration System

This guide explains how to leverage the multi-agent orchestration system to get work done in this repository. The system allows you to create tasks that are automatically assigned to specialized agents, which then complete the work asynchronously.

## What is Multi-Agent Orchestration?

The orchestration system coordinates multiple specialized agents working together on different tasks. Each agent has a specific area of expertise (documentation, architecture, code structure, etc.), and tasks flow between agents automatically based on handoffs.

**Key benefits:**

- **Transparent:** All task states are visible in Git
- **Asynchronous:** Agents work independently without blocking each other
- **Traceable:** Complete audit trail from task creation to completion
- **Simple:** Just create a YAML file describing the work needed

## Quick Start: Creating Your First Task

### 1. Choose the Right Agent

First, identify which agent should handle your task:

| Agent              | Specialization          | Use When You Need                   |
|--------------------|-------------------------|-------------------------------------|
| `structural`       | Code organization       | Repository maps, structure analysis |
| `lexical`          | Voice & style           | Tone consistency, terminology       |
| `curator`          | Documentation alignment | Structural consistency across docs  |
| `architect`        | System design           | ADRs, architecture decisions        |
| `diagrammer`       | Visual diagrams         | Architecture diagrams, flowcharts   |
| `writer-editor`    | Content polish          | Review, clarity, accessibility      |
| `planning`         | Project planning        | Roadmaps, feature planning          |
| `researcher`       | Investigation           | Research, analysis, exploration     |
| `translator`       | Multi-language          | Translation, internationalization   |
| `build-automation` | CI/CD                   | Build scripts, automation           |
| `backend-dev`      | Backend code            | API, database, server logic         |
| `frontend`         | Frontend code           | UI, UX, client-side code            |
| `synthesizer`      | Integration             | Combining multiple sources          |
| `bootstrap-bill`   | Repository setup        | Initial configuration               |
| `manager`          | Coordination            | Agent creation, oversight           |

### 2. Create a Task File

Create a new YAML file in the `work/inbox/` directory following this naming pattern:

```
YYYY-MM-DDTHHMM-<agent>-<short-description>.yaml
```

**Example:** `2025-11-23T1430-structural-repomap.yaml`

### 3. Use the Task Template

Here's a minimal task example:

```yaml
id: 2025-11-23T1430-structural-repomap
agent: structural
status: new

title: "Generate repository map for current state"

artefacts:
  - docs/REPO_MAP.md

context:
  repo: "sddevelopment-be/quickstart_agent-augmented-development"
  branch: "main"
  notes:
    - "Focus on recently updated files"
    - "Include directory structure overview"

created_at: "2025-11-23T14:30:00Z"
created_by: "stijn"
```

**Required fields:**

- `id`: Unique identifier (matches filename without `.yaml`)
- `agent`: Target agent name
- `status`: Always `"new"` for new tasks
- `artefacts`: List of files the agent should create or modify

**Optional but helpful:**

- `title`: Human-readable description
- `context.notes`: Additional guidance for the agent
- `priority`: `critical`, `high`, `normal`, or `low` (default: `normal`)
- `mode`: `/analysis-mode`, `/creative-mode`, or `/meta-mode` (default: `/analysis-mode`)

### 4. Commit and Push

Once you've created the task file:

```bash
git add work/inbox/2025-11-23T1430-structural-repomap.yaml
git commit -m "Add task: Generate repository map"
git push
```

### 5. Monitor Progress

The Agent Orchestrator will:

1. Move your task from `work/inbox/` to `work/assigned/<agent>/`
2. The agent updates status to `in_progress` when it starts
3. The agent completes work and moves the task to `work/done/`

Check task progress by viewing the YAML file:

```bash
# See where your task is
find work/ -name "2025-11-23T1430-structural-repomap.yaml"

# View task details
cat work/assigned/structural/2025-11-23T1430-structural-repomap.yaml
```

## Understanding Task Lifecycle

Tasks move through these stages:

```
┌─────┐     ┌──────────┐     ┌─────────────┐     ┌──────┐
│ new │ ──> │ assigned │ ──> │ in_progress │ ──> │ done │
└─────┘     └──────────┘     └─────────────┘     └──────┘
   ↓                                ↓
   └───────────────> error <────────┘
```

- **new:** Task created in `work/inbox/`, waiting for orchestrator
- **assigned:** Moved to `work/assigned/<agent>/`, ready for agent pickup
- **in_progress:** Agent is actively working on it
- **done:** Completed successfully, moved to `work/done/`
- **error:** Failed and needs human intervention

## Common Use Cases

### Scenario 1: Generate Documentation

Create a task for the curator agent to review documentation consistency:

```yaml
id: 2025-11-23T1500-curator-doc-audit
agent: curator
status: new
title: "Audit documentation for structural consistency"
artefacts:
  - docs/audit-report.md
context:
  notes:
    - "Check all HOW_TO_USE guides for consistent structure"
    - "Verify metadata completeness"
created_at: "2025-11-23T15:00:00Z"
created_by: "stijn"
```

### Scenario 2: Create Architecture Decision

Request an ADR from the architect:

```yaml
id: 2025-11-23T1600-architect-adr-database
agent: architect
status: new
mode: /analysis-mode
priority: high
title: "Create ADR for database selection"
artefacts:
  - docs/architecture/adrs/ADR-006-database-selection.md
context:
  notes:
    - "Evaluate PostgreSQL vs MongoDB"
    - "Consider scalability and query patterns"
    - "Reference existing ADRs for format"
created_at: "2025-11-23T16:00:00Z"
created_by: "stijn"
```

### Scenario 3: Multi-Agent Workflow

Chain multiple agents together using handoffs. The first agent completes its work and automatically creates a task for the next agent.

**Initial task (architect creates ADR):**

```yaml
id: 2025-11-23T1700-architect-adr-api
agent: architect
status: new
title: "Create ADR for API design"
artefacts:
  - docs/architecture/adrs/ADR-007-api-design.md
created_at: "2025-11-23T17:00:00Z"
created_by: "stijn"
```

When the architect completes the task, it adds a handoff in the `result` section:

```yaml
result:
  summary: "Created ADR-007 with API design recommendations"
  artefacts:
    - docs/architecture/adrs/ADR-007-api-design.md
  next_agent: "writer-editor"
  next_task_title: "Review and polish ADR-007"
  next_artefacts:
    - docs/architecture/adrs/ADR-007-api-design.md
  next_task_notes:
    - "Check technical terminology clarity"
    - "Ensure examples are easy to follow"
  completed_at: "2025-11-23T17:45:00Z"
```

The orchestrator automatically creates a new task for the writer-editor.

## Monitoring the System

### Check Agent Status

View the agent status dashboard:

```bash
cat work/collaboration/AGENT_STATUS.md
```

### View Recent Handoffs

See task transitions between agents:

```bash
tail -n 50 work/collaboration/HANDOFFS.md
```

### Check Orchestration Events

Monitor system-wide activity:

```bash
tail -n 100 work/collaboration/WORKFLOW_LOG.md
```

### Find Tasks by Status

```bash
# All new tasks waiting for assignment
ls work/inbox/*.yaml

# All tasks in progress
find work/assigned -name "*.yaml"

# Recently completed tasks
ls -lt work/done/*.yaml | head -n 10
```

## Troubleshooting

### Task Stuck in "assigned"

**Symptoms:** Task hasn't moved to `in_progress` after expected time.

**Possible causes:**

- Agent orchestrator isn't running
- Agent has crashed or isn't watching the directory

**Solutions:**

1. Check if the orchestrator is running (manual execution or cron/GitHub Actions)
2. Review agent logs in `work/logs/`
3. Manually trigger the agent if needed

### Task Stuck in "in_progress"

**Symptoms:** Task status shows `in_progress` but no completion.

**Possible causes:**

- Agent timed out (default: 2 hours)
- Agent encountered an unexpected error

**Solutions:**

1. Check `WORKFLOW_LOG.md` for timeout warnings
2. Review the task YAML for any `error` block
3. May need to manually reset task to `assigned` status

### Task Failed with Error

**Symptoms:** Task status is `error` with error details.

**Solutions:**

1. Read the error message in the task YAML
2. Address the underlying issue (missing context, unclear requirements, etc.)
3. Create a new task with corrected information

### No Follow-up Task Created

**Symptoms:** Agent completed with `next_agent` but no new task appeared.

**Solutions:**

1. Verify the orchestrator ran after task completion
2. Check `WORKFLOW_LOG.md` for orchestrator errors
3. Manually create the follow-up task if needed

## Advanced Features

### Task Dependencies

Specify tasks that must complete before yours starts:

```yaml
context:
  dependencies:
    - 2025-11-23T1400-structural-repomap
    - 2025-11-23T1500-lexical-analysis
```

The orchestrator won't assign your task until dependencies are done.

### Priority Levels

Control task urgency:

```yaml
priority: critical  # Highest priority
priority: high      # Important
priority: normal    # Default
priority: low       # Background work
```

### Reasoning Modes

Guide how agents approach the task:

```yaml
mode: /analysis-mode  # Default: analytical, structured
mode: /creative-mode  # Narrative, exploratory
mode: /meta-mode      # Self-reflective, process-focused
```

## Best Practices

### 1. Be Specific with Artifacts

List exact files you want created or modified:

```yaml
artefacts:
  - docs/REPO_MAP.md          # Good: specific path
  - "update documentation"     # Bad: vague
```

### 2. Provide Context Notes

Help agents understand intent:

```yaml
context:
  notes:
    - "Focus on user-facing features"
    - "Skip internal implementation details"
    - "Include code examples"
```

### 3. Use Clear Task IDs

Follow the naming convention for easy identification:

```
YYYY-MM-DDTHHMM-<agent>-<description>
  ↑       ↑        ↑         ↑
  Date    Time    Agent    Short slug
```

### 4. One Task, One Focus

Keep tasks focused on a single deliverable:

```yaml
# Good: Single focused task
title: "Generate repository structure map"
artefacts:
  - docs/REPO_MAP.md

# Bad: Multiple unrelated items
title: "Generate map and write guide and create diagram"
artefacts:
  - docs/REPO_MAP.md
  - docs/GUIDE.md
  - docs/DIAGRAM.png
```

Instead, create separate tasks or use handoffs.

### 5. Check Existing Work First

Before creating a task:

1. Check if similar work exists in `work/done/`
2. Review agent output directories
3. Search Git history for related changes

## Getting Help

### Reference Documentation

- **Task Template:** `docs/templates/task-descriptor.yaml`
- **Work Directory Overview:** `work/README.md`
- **Architecture:** `docs/architecture/design/async_multiagent_orchestration.md`
- **Technical Design:** `docs/architecture/design/async_orchestration_technical_design.md`

### Architecture Decision Records

- **ADR-002:** File-Based Asynchronous Agent Coordination
- **ADR-003:** Task Lifecycle and State Management
- **ADR-004:** Work Directory Structure
- **ADR-005:** Coordinator Agent Pattern

### Agent Profiles

See `.github/agents/*.agent.md` for detailed agent capabilities and specializations.

---

_Last updated: 2025-11-23_  
_Maintained by: Curator Claire_  
_For questions about this guide, see: `.github/agents/curator.agent.md`_
