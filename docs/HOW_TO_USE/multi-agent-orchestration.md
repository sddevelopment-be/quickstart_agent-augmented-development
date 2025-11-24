# Using the Multi-Agent Orchestration System

This guide explains how to use the multi-agent orchestration system to delegate work within this repository. The system enables you to create tasks that are automatically assigned to specialized agents, which complete the work asynchronously—no coordination overhead required.

## What is Multi-Agent Orchestration?

The orchestration system coordinates multiple specialized agents working together on different tasks. Each agent focuses on a specific area of expertise—documentation, architecture, code structure, and more. Tasks flow between agents automatically through **handoffs** (explicit transfers from one agent to the next), creating seamless collaborative workflows.

**Key benefits:**

- **Transparent:** All task states are visible in Git—no hidden queues
- **Asynchronous:** Agents work independently without blocking each other
- **Traceable:** Complete audit trail from task creation to completion
- **Simple:** Just create a YAML file describing what you need

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

Create a new YAML file in the `work/inbox/` directory. Use this naming pattern:

```
YYYY-MM-DDTHHMM-<agent>-<short-description>.yaml
```

**Example:** `2025-11-23T1430-structural-repomap.yaml`

The timestamp helps keep tasks chronologically ordered, while the agent name ensures clear routing.

### 3. Write the Task Descriptor

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

- `id`: Unique identifier (must match filename without `.yaml`)
- `agent`: Target agent name (see table in step 1)
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

The orchestration system automatically:

1. Moves your task from `work/inbox/` to `work/assigned/<agent>/`
2. Updates status to `in_progress` when the agent starts
3. Moves completed tasks to `work/done/`

Track task progress by viewing the YAML file:

```bash
# See where your task is
find work/ -name "2025-11-23T1430-structural-repomap.yaml"

# View task details
cat work/assigned/structural/2025-11-23T1430-structural-repomap.yaml
```

## Understanding the Task Lifecycle

Every task moves through a well-defined sequence of stages:

```
┌─────┐     ┌──────────┐     ┌─────────────┐     ┌──────┐
│ new │ ──> │ assigned │ ──> │ in_progress │ ──> │ done │
└─────┘     └──────────┘     └─────────────┘     └──────┘
   ↓                                ↓
   └───────────────> error <────────┘
```

- **new:** Task created in `work/inbox/`, awaiting orchestrator pickup
- **assigned:** Moved to `work/assigned/<agent>/`, ready for the agent
- **in_progress:** Agent is actively working on the task
- **done:** Completed successfully and moved to `work/done/`
- **error:** Failed—requires human review and intervention

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

### Scenario 3: Multi-Agent Workflow (Handoffs)

Chain multiple agents together using **handoffs**—when the first agent completes its work, it signals the orchestrator to create a follow-up task for the next agent.

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

When the architect completes the task, it adds handoff metadata to the `result` section to signal the next step:

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

The orchestrator detects the `next_agent` field and automatically creates a new task for the writer-editor agent.

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

**Symptom:** Task hasn't moved to `in_progress` after the expected time.

**Common causes:**

- Agent orchestrator isn't running (check manual execution, cron, or GitHub Actions)
- Agent has stopped or isn't monitoring its directory
- Agent startup error (check `work/logs/<agent>/`)

**Solutions:**

1. Verify the orchestrator process is active
2. Review agent logs in `work/logs/<agent>/` for error messages
3. Manually trigger the agent if necessary
4. Check the agent's assigned directory permissions

### Task Stuck in "in_progress"

**Symptom:** Task status shows `in_progress` but hasn't completed.

**Common causes:**

- Agent timed out (default: 2 hours)
- Agent encountered an unexpected error
- Agent is still working on a large task

**Solutions:**

1. Check `WORKFLOW_LOG.md` for timeout warnings
2. Review the task YAML for any `error` block added by the agent
3. Check agent logs in `work/logs/<agent>/` for the latest activity
4. If needed, manually reset task status to `assigned` and restart

### Task Failed with Error

**Symptom:** Task status is `error` with error details in the YAML.

**Solutions:**

1. Read the `error.message` field in the task YAML for specifics
2. Address the root cause (missing context, unclear requirements, invalid artifacts)
3. Create a new task with corrected information
4. Consider adding more context notes to prevent similar failures

### No Follow-up Task Created

**Symptom:** Agent completed with `next_agent` specified, but no new task appeared in the inbox.

**Solutions:**

1. Verify the orchestrator ran after task completion (check recent commits or logs)
2. Inspect `WORKFLOW_LOG.md` for orchestrator errors or warnings
3. Verify handoff was logged in `HANDOFFS.md`
4. Manually create the follow-up task if the orchestrator failed

## Advanced Features

### Task Dependencies

Specify prerequisite tasks that must complete before your task begins:

```yaml
context:
  dependencies:
    - 2025-11-23T1400-structural-repomap
    - 2025-11-23T1500-lexical-analysis
```

The orchestrator won't assign your task until all dependencies are marked `done`.

### Priority Levels

Control task urgency:

```yaml
priority: critical  # Highest priority
priority: high      # Important
priority: normal    # Default
priority: low       # Background work
```

### Reasoning Modes

Guide how agents approach the task (based on the SDD Agent Framework):

```yaml
mode: /analysis-mode  # Default: analytical, structured
mode: /creative-mode  # Narrative, exploratory
mode: /meta-mode      # Self-reflective, process-focused
```

## Best Practices

### 1. Be Specific About Artifacts

Always list exact file paths the agent should create or modify:

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

### 3. Use Consistent Task IDs

Follow the naming convention for easy identification and sorting:

```
YYYY-MM-DDTHHMM-<agent>-<description>
  ↑       ↑        ↑         ↑
  Date    Time    Agent    Short slug
```

### 4. One Task, One Focus

Keep each task focused on a single deliverable:

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

For multiple deliverables, create separate tasks or use handoffs to chain them together.

### 5. Check for Existing Work

Before creating a new task, verify it's not duplicating existing work:

1. Search `work/done/` for similar completed tasks
2. Review agent output directories for recent artifacts
3. Search Git history for related changes (`git log --all --grep="keyword"`)

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
