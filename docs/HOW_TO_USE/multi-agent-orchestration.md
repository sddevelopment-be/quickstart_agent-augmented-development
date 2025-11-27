# Using the Multi-Agent Orchestration System

This guide explains how to use the multi-agent orchestration system to delegate work within this repository. The system enables you to create tasks that are automatically assigned to specialized agents, which complete the work asynchronously—no coordination overhead required.

## What is Multi-Agent Orchestration?

The orchestration system coordinates multiple specialized agents working together on different tasks. Each agent focuses on a specific area of expertise—documentation, architecture, code structure, and more. Tasks flow between agents automatically through **handoffs** (explicit transfers from one agent to the next), creating seamless collaborative workflows.

Think of it as a file-based workflow where:
- You create a task by writing a YAML file
- The orchestrator assigns it to the right agent
- The agent completes the work and updates the file
- If needed, the agent hands off to another agent
- All activity is tracked in Git with full transparency

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

Create a new YAML file in the `work/collaboration/inbox/` directory. Use this naming pattern:

```
YYYY-MM-DDTHHMM-<agent>-<short-description>.yaml
```

**Example:** `2025-11-23T1430-structural-repomap.yaml`

The timestamp helps keep tasks chronologically ordered, while the agent name ensures clear routing.

### 3. Write the Task Descriptor

A task descriptor is a YAML file that tells the orchestration system what work needs to be done. Here's a minimal example:

```yaml
id: 2025-11-23T1430-structural-repomap
agent: structural
status: new

title: "Generate repository map for current state"

artifacts:
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
- `artifacts`: List of files the agent should create or modify

**Optional but helpful:**

- `title`: Human-readable description
- `context.notes`: Additional guidance for the agent
- `priority`: `critical`, `high`, `normal`, or `low` (default: `normal`)
- `mode`: `/analysis-mode`, `/creative-mode`, or `/meta-mode` (default: `/analysis-mode`)

### 4. Commit and Push

Once you've created the task file:

```bash
git add work/collaboration/inbox/2025-11-23T1430-structural-repomap.yaml
git commit -m "Add task: Generate repository map"
git push
```

### 5. Monitor Progress

The orchestration system automatically:

1. Moves your task from `work/collaboration/inbox/` to `work/collaboration/assigned/<agent>/`
2. Updates status to `in_progress` when the agent starts
3. Moves completed tasks to `work/collaboration/done/<agent>/`
4. Creates a work log in `work/reports/logs/<agent>/` documenting the execution

Track task progress by viewing the YAML file:

```bash
# See where your task is
find work/collaboration/ -name "2025-11-23T1430-structural-repomap.yaml"

# View task details
cat work/collaboration/assigned/structural/2025-11-23T1430-structural-repomap.yaml

# View work log after completion
cat work/reports/logs/structural/2025-11-23T1430-structural-repomap.md
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

- **new:** Task created in `work/collaboration/inbox/`, awaiting orchestrator pickup
- **assigned:** Moved to `work/collaboration/assigned/<agent>/`, ready for the agent
- **in_progress:** Agent is actively working on the task
- **done:** Completed successfully and moved to `work/collaboration/done/<agent>/` with work log in `work/reports/logs/<agent>/`
- **error:** Failed—requires human review and intervention

## Common Use Cases

### Scenario 1: Generate Documentation

Create a task for the curator agent to review documentation consistency:

```yaml
id: 2025-11-23T1500-curator-doc-audit
agent: curator
status: new
title: "Audit documentation for structural consistency"
artifacts:
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
artifacts:
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

Chain multiple agents together using **handoffs**. A handoff occurs when one agent completes its work and signals the orchestrator to create a follow-up task for another agent. This enables complex workflows without manual coordination.

**How it works:**
1. First agent completes its task
2. Agent adds `next_agent` field to the result block
3. Orchestrator detects the handoff signal
4. Orchestrator creates a new task for the next agent
5. Second agent picks up and continues the workflow

**Initial task (architect creates ADR):**

```yaml
id: 2025-11-23T1700-architect-adr-api
agent: architect
status: new
title: "Create ADR for API design"
artifacts:
  - docs/architecture/adrs/ADR-007-api-design.md
created_at: "2025-11-23T17:00:00Z"
created_by: "stijn"
```

When the architect completes the task, it adds handoff metadata to the `result` section to signal the next step:

```yaml
result:
  summary: "Created ADR-007 with API design recommendations"
  artifacts:
    - docs/architecture/adrs/ADR-007-api-design.md
  metrics:
    duration_minutes: 15
    token_count:
      input: 8500
      output: 4200
      total: 12700
    context_files_loaded: 5
    artifacts_created: 1
    artifacts_modified: 0
  next_agent: "writer-editor"
  next_task_title: "Review and polish ADR-007"
  next_artifacts:
    - docs/architecture/adrs/ADR-007-api-design.md
  next_task_notes:
    - "Check technical terminology clarity"
    - "Ensure examples are easy to follow"
  completed_at: "2025-11-23T17:45:00Z"
```

The orchestrator detects the `next_agent` field and automatically creates a new task for the writer-editor agent. The handoff is logged in `work/collaboration/HANDOFFS.md` for tracking and transparency.

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
ls work/collaboration/inbox/*.yaml

# All tasks in progress
find work/collaboration/assigned -name "*.yaml"

# Recently completed tasks
find work/collaboration/done -name "*.yaml" -type f | xargs ls -lt | head -n 10

# View work logs for completed tasks
ls -lt work/reports/logs/*/*.md | head -n 10
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
2. Review agent logs in `work/reports/logs/<agent>/` for error messages
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
3. Check agent logs in `work/reports/logs/<agent>/` for the latest activity
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

## Understanding Metrics and Work Logs

The orchestration system captures comprehensive metrics and creates detailed work logs for every task. This helps track performance, improve efficiency, and maintain transparency.

### Metrics Captured

When agents complete tasks, they automatically capture the following metrics in the result block (per **ADR-009: Orchestration Metrics and Quality Standards**):

**Required Metrics:**
- `duration_minutes`: Total execution time from task start to completion
- `token_count`: Input, output, and total tokens processed
- `context_files_loaded`: Number of files loaded for context
- `artifacts_created`: Count of new files created
- `artifacts_modified`: Count of existing files modified

**Optional Metrics:**
- `per_artifact_timing`: Detailed breakdown per artifact
- `handoff_latency_seconds`: Time between task completion and next task creation

**Example metrics block in task result:**

```yaml
result:
  summary: "Documentation audit completed"
  artifacts:
    - docs/audit-report.md
  metrics:
    duration_minutes: 12
    token_count:
      input: 15000
      output: 3500
      total: 18500
    context_files_loaded: 8
    artifacts_created: 1
    artifacts_modified: 0
  completed_at: "2025-11-24T10:30:00Z"
```

### Work Logs

Every completed task generates a detailed work log in `work/reports/logs/<agent>/` (per **Directive 014: Work Log Creation**). Work logs are markdown files that provide narrative documentation of the agent's execution process.

**What work logs contain:**

- **Context**: What prompted the work and initial conditions
- **Approach**: Decision-making rationale and alternatives considered
- **Execution Steps**: Chronological log of actions taken
- **Artifacts Created**: Files produced with validation markers (✅ validated, ⚠️ partial, ❗️ issue)
- **Outcomes**: Results achieved and deliverables completed
- **Lessons Learned**: Actionable insights for framework improvement
- **Metadata**: Execution duration, token counts, context size, handoffs initiated

**Why work logs matter:**

Work logs provide transparency into agent reasoning, enable continuous improvement of the orchestration framework, and serve as training examples for future agent development. They complement the brief task result blocks with detailed narratives of how work was accomplished.

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
artifacts:
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
artifacts:
  - docs/REPO_MAP.md

# Bad: Multiple unrelated items
title: "Generate map and write guide and create diagram"
artifacts:
  - docs/REPO_MAP.md
  - docs/GUIDE.md
  - docs/DIAGRAM.png
```

For multiple deliverables, create separate tasks or use handoffs to chain them together.

### 5. Check for Existing Work

Before creating a new task, verify it's not duplicating existing work:

1. Search `work/collaboration/done/` for similar completed tasks
2. Review agent output directories for recent artifacts
3. Review work logs in `work/reports/logs/` for related work
4. Search Git history for related changes (`git log --all --grep="keyword"`)

## Getting Help

### Reference Documentation

- **Task Templates:** `docs/templates/agent-tasks/` (task-descriptor.yaml, task-examples.yaml, task-result.yaml)
- **Work Directory Overview:** `work/README.md`
- **Architecture:** `docs/architecture/design/async_multiagent_orchestration.md`
- **Technical Design:** `docs/architecture/design/async_orchestration_technical_design.md`
- **Metrics Standard:** `docs/architecture/adrs/ADR-009-orchestration-metrics-standard.md`
- **Work Log Directive:** `.github/agents/directives/014_worklog_creation.md`

### Architecture Decision Records

- **ADR-002:** File-Based Asynchronous Agent Coordination
- **ADR-003:** Task Lifecycle and State Management
- **ADR-004:** Work Directory Structure
- **ADR-005:** Coordinator Agent Pattern
- **ADR-009:** Orchestration Metrics and Quality Standards

### Agent Profiles

See `.github/agents/*.agent.md` for detailed agent capabilities and specializations.

---

_Last updated: 2025-11-27_  
_Maintained by: Curator Claire & Editor Eddy_  
_For questions about this guide, see: `.github/agents/curator.agent.md` and `.github/agents/writer-editor.agent.md`_
