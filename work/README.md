# Work Directory - Multi-Agent Orchestration

_Version: 1.0.0_  
_Last updated: 2025-11-23_

This directory contains the file-based orchestration system for coordinating multiple specialized agents in an asynchronous, transparent, and Git-native manner.

## Overview

The work directory implements a task-based workflow where:

1. Tasks are created as YAML files describing work to be done
2. An Agent Orchestrator routes tasks to appropriate specialized agents
3. Agents process tasks and update their status
4. Completed tasks can trigger follow-up tasks via handoffs
5. All state changes are visible in Git history

## Directory Structure

```
work/
  inbox/              # New tasks awaiting assignment
  assigned/           # Tasks assigned to specific agents
    architect/        # Tasks for Architect agent
    backend-dev/      # Tasks for Backend Developer agent
    bootstrap-bill/   # Tasks for Bootstrap agent
    build-automation/ # Tasks for Build/CI agents
    coordinator/      # Meta-orchestration tasks
    curator/          # Tasks for Curator agent
    diagrammer/       # Tasks for Diagrammer agent
    frontend/         # Tasks for Frontend agent
    lexical/          # Tasks for Lexical agent
    manager/          # Tasks for Manager agent
    planning/         # Tasks for Planning agent
    researcher/       # Tasks for Researcher agent
    structural/       # Tasks for Structural agent
    synthesizer/      # Tasks for Synthesizer agent
    translator/       # Tasks for Translator agent
    writer-editor/    # Tasks for Writer-Editor agent
  done/               # Completed tasks with results
  archive/            # Long-term task retention (by month)
  logs/               # Agent execution logs (optional)
  collaboration/      # Cross-agent coordination artifacts
  schemas/            # Task YAML schema definitions
  scripts/            # Utility scripts for orchestration
```

## Task Lifecycle

Tasks progress through the following states:

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

**See also:** [Task Lifecycle State Machine Diagram](../docs/architecture/diagrams/task-lifecycle-state-machine.puml)

### State Descriptions

- **new**: Task created in `work/inbox/`, awaiting assignment
- **assigned**: Task moved to `work/assigned/<agent>/`, awaiting agent pickup
- **in_progress**: Agent has started work on the task
- **done**: Task completed successfully, moved to `work/done/`
- **error**: Task failed, requires human intervention
- **archive**: Old completed tasks, organized by month in `work/archive/`

## Quick Start

### Creating a Task

1. Create a YAML file in `work/inbox/` using the template at `docs/templates/task-descriptor.yaml`
2. Name the file: `YYYY-MM-DDTHHMM-<agent>-<slug>.yaml`
3. Specify the target agent, artifacts, and context

Example:
```bash
# Create a task for the structural agent
cat > work/inbox/2025-11-23T1500-structural-repomap.yaml <<EOF
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
EOF
```

### Running the Agent Orchestrator

The Agent Orchestrator assigns tasks, creates follow-ups, and monitors system health.

**Manual execution:**
```bash
python work/scripts/agent_orchestrator.py
```

**Automated execution:**
- Via cron: `*/5 * * * * cd /path/to/repo && python work/scripts/agent_orchestrator.py`
- Via GitHub Actions: See `.github/workflows/agent-orchestrator.yml`

### Processing Tasks as an Agent

Agents poll their assigned directory and process tasks:

1. Read task from `work/assigned/<agent-name>/*.yaml`
2. Update status to `in_progress`
3. Perform specialized work
4. Update artifacts
5. Add `result` block to task YAML
6. Update status to `done`
7. Move task to `work/done/`

## Collaboration Artifacts

The `work/collaboration/` directory contains system-wide coordination files:

- **AGENT_STATUS.md**: Real-time dashboard of agent activity
- **HANDOFFS.md**: Log of agent-to-agent transitions
- **WORKFLOW_LOG.md**: System-wide orchestration events
- **orchestration-implementation-plan.md**: Implementation roadmap
- **orchestration-architecture-summary.md**: Architecture overview

## Task YAML Schema

See `docs/templates/task-descriptor.yaml` for complete schema documentation.

**Required fields:**
- `id`: Unique task identifier
- `agent`: Target agent name
- `status`: Current state
- `artefacts`: List of files to create/modify

**Optional fields:**
- `title`: Human-readable description
- `mode`: Reasoning mode (/analysis-mode, /creative-mode, /meta-mode)
- `priority`: critical | high | normal | low
- `context`: Additional information for the agent

**Auto-populated fields:**
- `created_at`, `created_by`: Task creation metadata
- `assigned_at`, `started_at`, `completed_at`: Lifecycle timestamps
- `result`: Completion details (added by agent)
- `error`: Failure details (added by agent)

## Agent Handoffs

Tasks can chain to create multi-step workflows:

```yaml
result:
  summary: "Completed structural analysis"
  artefacts:
    - docs/REPO_MAP.md
  next_agent: "lexical"
  next_task_title: "Perform voice/style analysis on REPO_MAP"
  next_artefacts:
    - docs/REPO_MAP.md
  next_task_notes:
    - "Check for consistency with LEX guidelines"
  completed_at: "2025-11-23T15:30:00Z"
```

The Agent Orchestrator automatically creates the follow-up task in `work/inbox/`.

## Validation

Validate task files and directory structure:

```bash
# Validate task YAML schema
python work/scripts/validate-task-schema.py work/inbox/task.yaml

# Validate directory structure
bash work/scripts/validate-work-structure.sh

# Validate all (when implemented)
bash work/scripts/validate-all.sh
```

## Monitoring

Check system status:

```bash
# View agent status dashboard
cat work/collaboration/AGENT_STATUS.md

# View recent handoffs
tail -n 50 work/collaboration/HANDOFFS.md

# View orchestration events
tail -n 100 work/collaboration/WORKFLOW_LOG.md
```

## Archival

Old completed tasks are automatically moved to `work/archive/<YYYY-MM>/` after 30 days (configurable).

Manual archival:
```bash
# Archive tasks older than specified date
python work/scripts/archive-tasks.py --before 2025-10-01
```

## Design Principles

1. **Simplicity**: All workflows derive from file movements
2. **Transparency**: Every state transition visible in Git
3. **Determinism**: Predictable, repeatable task execution
4. **Composability**: Complex workflows emerge from simple handoffs
5. **Traceability**: Complete audit trail from creation to archive

## Related Documentation

- [Async Multi-Agent Orchestration Architecture](../docs/architecture/design/async_multiagent_orchestration.md)
- [Technical Design](../docs/architecture/design/async_orchestration_technical_design.md)
- [ADR-002: File-Based Asynchronous Agent Coordination](../docs/architecture/adrs/ADR-002-file-based-async-coordination.md)
- [ADR-003: Task Lifecycle and State Management](../docs/architecture/adrs/ADR-003-task-lifecycle-state-management.md)
- [ADR-004: Work Directory Structure](../docs/architecture/adrs/ADR-004-work-directory-structure.md)
- [ADR-005: Coordinator Agent Pattern](../docs/architecture/adrs/ADR-005-coordinator-agent-pattern.md)
- [Task Descriptor Template](../docs/templates/task-descriptor.yaml)

## Troubleshooting

### Task stuck in "assigned" state
- Check if agent is running
- Verify agent is watching correct directory
- Check agent logs for errors

### Task stuck in "in_progress" state
- Agent may have crashed or timed out
- Check timeout settings (default: 2 hours)
- Review Agent Orchestrator warnings in WORKFLOW_LOG.md

### Merge conflicts in work directory
- Tasks are independent files - resolve conflicts by choosing appropriate version
- Use `git log work/` to see task history
- Manual resolution may be needed for collaboration artifacts

### Agent Orchestrator not running
- Check cron or GitHub Actions configuration
- Verify Python dependencies installed
- Run manually to diagnose: `python work/scripts/agent_orchestrator.py`

## Support

For questions or issues:
1. Review architecture documentation in `docs/architecture/`
2. Check WORKFLOW_LOG.md for recent system events
3. Consult with human stakeholders
4. Open issue in repository issue tracker

---

_Maintained by: Architect Alphonso_  
_For architecture questions, see: `.github/agents/architect.agent.md`_
