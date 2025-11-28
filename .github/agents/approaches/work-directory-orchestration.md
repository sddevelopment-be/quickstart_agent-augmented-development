# Work Directory Orchestration Approach

**Approach Type:** Coordination Pattern  
**Version:** 1.1.0  
**Last Updated:** 2025-11-27  
**Status:** Active

## Purpose

Provide a single, precise reference for the file-based asynchronous orchestration model that powers the `work/` directory. The approach keeps exploratory and operational work visible inside Git by representing every task as a YAML file that flows through clearly defined directories and lifecycle states. Humans, agents, and automation can collaborate without bespoke services while preserving a full audit trail.

## Core Principles

1. **Simplicity** – Workflows are just file moves; no queues or servers.  
2. **Transparency** – Every transition is committed to Git, so history is reviewable.  
3. **Determinism** – State is explicit in filenames, directories, and YAML fields.  
4. **Composability** – Specialized agents chain work via handoffs encoded in task files.  
5. **Traceability** – Artefacts, decisions, and logs stay linked across the lifecycle.

## Directory Model

```
work/
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

See `work/collaboration/README.md` for directory-specific conventions.

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

- **new** – YAML file created in `work/collaboration/inbox/`, `status: new`.  
- **assigned** – Orchestrator validates task, stamps `assigned_at`, and moves it into `work/collaboration/assigned/<agent>/`.  
- **in_progress** – Agent claims the task, updates status, adds `started_at`.  
- **done** – Agent adds a `result` block, moves file to `work/collaboration/done/<agent>/`, and logs work.  
- **error** – Agent cannot complete; status set to `error` for human review.  
- **archive** – Automation moves older completed tasks to `work/collaboration/archive/<YYYY-MM>/`.

## Task Files

### Naming

`YYYY-MM-DDTHHMM-<agent>-<slug>.yaml` (ID mirrors filename without extension).

### Required & Optional Fields

Use the templates under `docs/templates/agent-tasks/`:
- `task-descriptor.yaml` – Required fields (`id`, `agent`, `status`, `artefacts`).
- `task-context.yaml`, `task-examples.yaml`, etc. – Optional helpers.
- `task-timestamps.yaml`, `task-result.yaml` – Lifecycle metadata populated by agents.

### Quick Creation Example

```bash
cat > work/collaboration/inbox/2025-11-23T1500-structural-repomap.yaml <<'YAML'
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

## Operating Roles

### Human Operators

1. Create new tasks in `work/collaboration/inbox/` using the template.  
2. Monitor status via `work/collaboration/AGENT_STATUS.md` and `WORKFLOW_LOG.md`.  
3. Review `work/collaboration/done/<agent>/` to audit completed work.  
4. Inspect `work/reports/` for agent logs, benchmarks, and synthesizer summaries.  
5. Use `validation/` scripts to enforce schema and structure integrity.

### Agent Orchestrator (`ops/scripts/orchestration/agent_orchestrator.py`)

- **Assignment** – Scans `inbox/`, validates YAML, updates status to `assigned`, records timestamps, and moves files into the appropriate agent queue.  
- **Handoffs** – Watches `done/<agent>/` for tasks with `result.next_agent`, creates follow-up YAML in `inbox/`, and copies context/artefacts.  
- **Health Monitoring** – Detects tasks stuck `in_progress` beyond timeout, logs warnings, and escalates via `WORKFLOW_LOG.md`.  
- **Archival** – Periodically moves aged `done/` tasks into `archive/<YYYY-MM>/`.

### Specialized Agents

1. Poll `work/collaboration/assigned/<agent>/` for `status: assigned`.  
2. Update to `in_progress`, stamp `started_at`, and commit change.  
3. Produce the requested artefacts, referencing directives/approaches as needed.  
4. Update the task YAML with `result` (summary, artefacts, optional `next_agent`, completion metadata).  
5. Move file to `work/collaboration/done/<agent>/`, add a work log under `work/reports/logs/<agent>/`, and commit together.  
6. If blocked, add an `error` block, set `status: error`, and notify humans via coordination artefacts.

## Collaboration Artefacts

- **AGENT_STATUS.md** – High-level dashboard of agent queues.  
- **HANDOFFS.md** – Chronological record of delegated work.  
- **WORKFLOW_LOG.md** – Operational timeline (assignments, errors, orchestrator events).  
- **orchestration-*.md** – Architecture plans and implementation diaries.  
- **work/reports/logs/** – Required per Directive 014 for every completed task.

## Reports & Shared Memory

- `work/reports/` consolidates logs, metrics, benchmarks, and synthesizer outputs for audits.  
- `work/external_memory/` provides temporary shared scratch space so agents can park intermediate artefacts or notes without polluting long-term docs.  
- `work/notes/` (including `work/notes/ideation/`) stores structured but provisional thinking before it graduates into `docs/`.

## Handoffs

Source agents encode follow-up work via the `result.next_agent` block:

```yaml
result:
  summary: "Created ADR-006 with recommendations"
  artefacts:
    - docs/architecture/adrs/ADR-006.md
  next_agent: writer-editor
  next_task_title: "Review and polish ADR-006"
  next_artefacts:
    - docs/architecture/adrs/ADR-006.md
  next_task_notes:
    - "Check for clarity"
  completed_at: "2025-11-23T15:45:00Z"
```

The orchestrator converts this into a fresh YAML task inside `inbox/`, copying dependencies and context so the next agent can continue seamlessly.

## Validation & Monitoring

```bash
# Validate a task against the schema
python validation/validate-task-schema.py work/collaboration/inbox/task.yaml

# Ensure structure + directory health
bash validation/validate-work-structure.sh

# View dashboards / logs
cat work/collaboration/AGENT_STATUS.md
tail -n 100 work/collaboration/WORKFLOW_LOG.md
tail -n 50 work/collaboration/HANDOFFS.md
```

## Archival & Automation

- Automatic archival moves tasks older than 30 days into `archive/<YYYY-MM>/`.  
- Manual archival: `python ops/scripts/planning/archive-tasks.py --before YYYY-MM-DD`.  
- Cron or GitHub Actions can run the orchestrator continuously (see `.github/workflows/agent-orchestrator.yml`).

## Troubleshooting

| Symptom | Likely Cause | Action |
|---------|--------------|--------|
| Task stuck in `assigned` | Agent/orchestrator not running | Check automation logs, restart agent, ensure polling directory matches agent name |
| Task stuck in `in_progress` | Agent crash, timeout, or forgot to update | Review `WORKFLOW_LOG.md`, inspect agent logs, reset status if needed |
| Handoff missing | Orchestrator didn’t run after completion or invalid `next_agent` | Rerun orchestrator, verify agent directory exists, or create task manually |
| Merge conflicts in `work/` | Concurrent edits | Resolve per-file, keeping latest task status; use `git log work/` for history |
| Unknown directory clutter | Tasks in wrong folders | Run `validation/validate-work-structure.sh` and relocate files |

## References

- ADR-002 — File-Based Asynchronous Agent Coordination  
- ADR-003 — Task Lifecycle & State Management  
- ADR-004 — Work Directory Structure  
- ADR-005 — Coordinator Agent Pattern  
- Directive 014 — Work Log Creation  
- Directive 019 — File-Based Collaboration  
- `docs/HOW_TO_USE/multi-agent-orchestration.md`  
- `work/README.md` (high-level overview)  
- `work/collaboration/README.md` (directory-specific guide)

---

_Maintained by: Curator Claire & Architect Alphonso_
