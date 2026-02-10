# Work Directory Orchestration Approach

**Approach Type:** Coordination Pattern  
**Version:** 1.1.0  
**Last Updated:** 2025-11-27  
**Status:** Active

## Purpose

Provide a single, precise reference for the file-based asynchronous orchestration model that powers the
`work/` directory. The approach keeps exploratory and operational work visible inside Git by representing every task as a YAML file that flows through clearly defined directories and lifecycle states. Humans, agents, and automation can collaborate without bespoke services while preserving a full audit trail.

## Core Principles

1. **Simplicity** – Workflows are just file moves; no queues or servers.
2. **Transparency** – Every transition is committed to Git, so history is reviewable.
3. **Determinism** – State is explicit in filenames, directories, and YAML fields.
4. **Composability** – Specialized agents chain work via handoffs encoded in task files.
5. **Traceability** – Artefacts, decisions, and logs stay linked across the lifecycle.

## Directory Model

```
`${WORKSPACE_ROOT}/
  collaboration/          # Task routing + coordination artifacts
    inbox/                # new tasks
    assigned/<agent>/     # pending agent work
    done/<agent>/         # completed tasks per agent
    archive/YYYY-MM/      # historical retention
    *.md                  # AGENT_STATUS, HANDOFFS, WORKFLOW_LOG, etc.
  reports/                # Work logs, metrics, benchmarks, synth reports
  external_memory/        # Shared scratch space for interim artefacts
  notes/                  # Structured notes (e.g., ideation now lives here)
  planning/               # Planning aids that feed task creation
  schemas/                # YAML schema definitions & validators
  scripts/                # Utility + orchestration helpers
```

See `${WORKSPACE_ROOT}/collaboration/README.md` for directory-specific conventions.

## Task Lifecycle

```
┌─────┐     ┌──────────┐     ┌─────────────┐     ┌──────┐     ┌─────────┐
│ new │ ──> │ assigned │ ──> │ in_progress │ ──> │ done │ ──> │ archive │
└─────┘     └──────────┘     └─────────────┘     └──────┘     └─────────┘
  inbox/      assigned/             │              done/        archive/
                                     │
                                     v
                                 ┌───────┐
                                 │ error │
                                 └───────┘
```

- **new** – YAML file created in `${WORKSPACE_ROOT}/collaboration/inbox/`, `status: new`.
- **assigned** – Orchestrator validates task, stamps `assigned_at`, and moves it into `${WORKSPACE_ROOT}/collaboration/assigned/<agent>/`.
- **in_progress** – Agent claims the task, updates status, adds `started_at`.
- **done** – Agent adds a `result` block, moves file to `${WORKSPACE_ROOT}/collaboration/done/<agent>/`, and logs work.
- **error** – Agent cannot complete; status set to `error` for human review.
- **archive** – Automation moves older completed tasks to `${WORKSPACE_ROOT}/collaboration/archive/<YYYY-MM>/`.

## Task Files

### Naming

`YYYY-MM-DDTHHMM-<agent>-<slug>.yaml` (ID mirrors filename without extension).

### Required & Optional Fields

Use the templates under `templates/agent-tasks/`:

- `task-descriptor.yaml` – Required fields (`id`, `agent`, `status`, `artefacts`).
- `task-context.yaml`, `task-examples.yaml`, etc. – Optional helpers.
- `task-timestamps.yaml`, `task-result.yaml` – Lifecycle metadata populated by agents.

### Quick Creation Example

```bash
cat > ${WORKSPACE_ROOT}/collaboration/inbox/2025-11-23T1500-structural-repomap.yaml <<'YAML'
id: 2025-11-23T1500-structural-repomap
agent: structural
status: new
title: "Generate REPO_MAP for current repository state"
artefacts:
  - docs/REPO_MAP.md
context:
  repo: "sddevelopment-be/quickstart_agent-augmented-development"
  branch: "main"
  notes:
    - "Focus on recently updated files"
created_at: "2025-11-23T15:00:00Z"
created_by: "stijn"
YAML
```

## Task Management Scripts

Agents MUST use the provided scripts to ensure proper validation and state transitions:

### Starting Tasks
```bash
python tools/scripts/start_task.py TASK_ID
```
- Validates current state is 'assigned'
- Updates status to 'in_progress'
- Adds started_at timestamp
- Enforces state transition rules

### Completing Tasks
```bash
python tools/scripts/complete_task.py TASK_ID
```
- Validates result block exists (unless --force used)
- Updates status to 'done'
- Adds completed_at timestamp
- Moves task to done/{agent}/ directory
- Enforces state transition rules

### Freezing Tasks (when blocked)
```bash
python tools/scripts/freeze_task.py TASK_ID --reason "Reason for pause"
```
- Preserves original status and context
- Adds freeze_reason and frozen_at timestamp
- Moves task to fridge/ directory
- Allows later review and unfreezing

### Listing Open Tasks
```bash
python tools/scripts/list_open_tasks.py [--status STATUS] [--agent AGENT] [--priority PRIORITY]
```
- Lists all non-terminal tasks (not done/error)
- Supports filtering by status, agent, priority
- Available output formats: table (default) or json

### Script Benefits
- **Validation:** Enforces proper YAML structure and required fields
- **State Management:** Centralized state machine prevents invalid transitions
- **Consistency:** Standardized timestamps and metadata
- **Auditability:** Clear lifecycle tracking
- **Error Prevention:** Validates task completeness before state changes

### Manual Operations (Deprecated)
❗️ **Do NOT manually move task files or edit status fields directly.** Use the provided scripts to ensure data integrity and proper validation.

## Operating Roles

### Human Operators

1. Create new tasks in `${WORKSPACE_ROOT}/collaboration/inbox/` using the template.
2. Monitor status via `${WORKSPACE_ROOT}/collaboration/AGENT_STATUS.md` and `WORKFLOW_LOG.md`.
3. Review `${WORKSPACE_ROOT}/collaboration/done/<agent>/` to audit completed work.
4. Inspect `work/reports/` for agent logs, benchmarks, and synthesizer summaries.
5. Use `validation/` scripts to enforce schema and structure integrity.

### Agent Orchestrator (`ops/scripts/orchestration/agent_orchestrator.py`)

- **Assignment** – Scans `inbox/`, validates YAML, updates status to
  `assigned`, records timestamps, and moves files into the appropriate agent queue.
- **Handoffs** – Watches `done/<agent>/` for tasks with `result.next_agent`, creates follow-up YAML in `inbox/`, and copies context/artefacts.
- **Health Monitoring** – Detects tasks stuck `in_progress` beyond timeout, logs warnings, and escalates via `WORKFLOW_LOG.md`.
- **Archival** – Periodically moves aged `done/` tasks into `archive/<YYYY-MM>/`.

### Specialized Agents

1. Poll `${WORKSPACE_ROOT}/collaboration/assigned/<agent>/` for `status: assigned`.
2. **Start task** using the provided script:
   ```bash
   python tools/scripts/start_task.py TASK_ID
   ```
   This automatically updates status to `in_progress`, stamps `started_at`, and validates state transitions.
3. Produce the requested artefacts, referencing directives/approaches as needed.
4. Update the task YAML with `result` (summary, artefacts, optional `next_agent`, completion metadata).
5. **Complete task** using the provided script:
   ```bash
   python tools/scripts/complete_task.py TASK_ID
   ```
   This validates the result block exists, moves the file to `${WORKSPACE_ROOT}/collaboration/done/<agent>/`, and enforces proper state transitions.
6. Add a work log under `work/reports/logs/<agent>/`, and commit together.
7. If blocked, **freeze task** using the provided script:
   ```bash
   python tools/scripts/freeze_task.py TASK_ID --reason "Reason for pause/block"
   ```
   This moves the task to fridge/ with metadata while preserving original status for later review.

## Collaboration Artefacts

- **AGENT_STATUS.md** – High-level dashboard of agent queues.
- **HANDOFFS.md** – Chronological record of delegated work.
- **WORKFLOW_LOG.md** – Operational timeline (assignments, errors, orchestrator events).
- **orchestration-*.md** – Architecture plans and implementation diaries.
- **work/reports/logs/** – Required per Directive 014 for every completed task.

## Reports & Shared Memory

- `work/reports/` consolidates logs, metrics, benchmarks, and synthesizer outputs for audits.
-
`work/external_memory/` provides temporary shared scratch space so agents can park intermediate artefacts or notes without polluting long-term docs.
- `work/notes/` (including `work/notes/ideation/`) stores structured but provisional thinking before it graduates into `docs/`.

## Handoffs

Source agents encode follow-up work via the `result.next_agent` block:

```yaml
result:
  summary: "Created ADR-006 with recommendations"
  artefacts:
    - ${DOC_ROOT}/architecture/adrs/ADR-006.md
  next_agent: writer-editor
  next_task_title: "Review and polish ADR-006"
  next_artefacts:
    - ${DOC_ROOT}/architecture/adrs/ADR-006.md
  next_task_notes:
    - "Check for clarity"
  completed_at: "2025-11-23T15:45:00Z"
```

The orchestrator converts this into a fresh YAML task inside `inbox/`, copying dependencies and context so the next agent can continue seamlessly.

## Validation & Monitoring

```bash
# Validate a task against the schema
python validation/validate-task-schema.py ${WORKSPACE_ROOT}/collaboration/inbox/task.yaml

# List all open tasks
python tools/scripts/list_open_tasks.py

# List tasks by status or agent
python tools/scripts/list_open_tasks.py --status assigned --agent python-pedro

# Ensure structure + directory health
bash validation/validate-work-structure.sh

# View dashboards / logs
cat ${WORKSPACE_ROOT}/collaboration/AGENT_STATUS.md
tail -n 100 ${WORKSPACE_ROOT}/collaboration/WORKFLOW_LOG.md
tail -n 50 ${WORKSPACE_ROOT}/collaboration/HANDOFFS.md
```

## Archival & Automation

- Automatic archival moves tasks older than 30 days into `archive/<YYYY-MM>/`.
- Manual archival: `python ops/scripts/planning/archive-tasks.py --before YYYY-MM-DD`.
- Cron or GitHub Actions can run the orchestrator continuously (see `.github/workflows/agent-orchestrator.yml`).

## Troubleshooting

| Symptom                     | Likely Cause                                                     | Action                                                                            |
|-----------------------------|------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Task stuck in `assigned`    | Agent/orchestrator not running                                   | Check automation logs, restart agent, ensure polling directory matches agent name |
| Task stuck in `in_progress` | Agent crash, timeout, or forgot to update                        | Review `WORKFLOW_LOG.md`, inspect agent logs, use `complete_task.py` or `freeze_task.py` |
| Task completion fails       | Missing result block or invalid state transition                 | Add result block to task YAML, or use `--force` flag with `complete_task.py`     |
| Handoff missing             | Orchestrator didn’t run after completion or invalid `next_agent` | Rerun orchestrator, verify agent directory exists, or create task manually        |
| Merge conflicts in `work/`  | Concurrent edits                                                 | Resolve per-file, keeping latest task status; use `git log work/` for history     |
| Unknown directory clutter   | Tasks in wrong folders                                           | Run `validation/validate-work-structure.sh` and relocate files using scripts     |
| Invalid task status         | Manual file editing bypassed validation                         | Use `start_task.py`, `complete_task.py`, or `freeze_task.py` instead of manual edits |

## References

- ADR-002 — File-Based Asynchronous Agent Coordination
- ADR-003 — Task Lifecycle & State Management
- ADR-004 — Work Directory Structure
- ADR-005 — Coordinator Agent Pattern
- Directive 014 — Work Log Creation
- Directive 019 — File-Based Collaboration
- `docs/HOW_TO_USE/multi-agent-orchestration.md`
- `work/README.md` (high-level overview)
- `${WORKSPACE_ROOT}/collaboration/README.md` (directory-specific guide)

---

_Maintained by: Curator Claire & Architect Alphonso_
