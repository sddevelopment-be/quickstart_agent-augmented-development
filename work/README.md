# Work Directory - Multi-Agent Orchestration

_Version: 1.1.0_  
_Last updated: 2025-11-27_

This directory contains directories, documents, and artifacts that have a short to medium-term lifespan within the repository. They are primarily used for:

- Having a 'workbench' area for agents to experiment and iterate
- Allowing human stakeholders or external systems to exchange ideas without interfering with main codebase
- Versioning work-in-progress by specialized agents
- Facilitating asynchronous multi-agent collaboration
- Enabling task-based orchestration of agent workflows
- Providing ephemeral shared memory for agents
- Storing agent outputs, logs, and reports

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
  collaboration/          # Orchestration and task coordination
    inbox/                # New tasks awaiting assignment
    assigned/             # Tasks assigned to specific agents
      <agent-slug>/       # Tasks for agent <slug>
    done/                 # Completed tasks (organized by agent)
    archive/              # Long-term task retention (by month)
    *.md                  # Cross-agent coordination artifacts
  notes/                  # Persistent project notes
    external_memory/        # Inter-agent context sharing
  planning/               # Planning artifacts, roadmaps, and strategies that are yet uncommitted
  reports/                # Agent outputs, logs, and metrics
    logs/                 # Agent execution logs
    synthesizer/          # Synthesizer aggregation reports
    benchmarks/           # Performance benchmarks
    metrics/              # Token usage and iteration metrics
```

## Detailed Workflow

The complete workflow, lifecycle diagrams, task schema guidance, and troubleshooting procedures now live in [`agents/approaches/work-directory-orchestration.md`](../agents/approaches/work-directory-orchestration.md). Treat that approach document as the canonical reference for:

- Task lifecycle definitions and diagrams
- Agent orchestrator responsibilities
- Task creation / processing / handoffs
- Validation, monitoring, and archival scripts
- Troubleshooting checklists

## Related Documentation

- `work/collaboration/README.md` — Directory-level conventions and quick reminders
- `docs/HOW_TO_USE/multi-agent-orchestration.md` — Tutorial view of the workflow
- `agents/approaches/work-directory-orchestration.md` — Detailed design + operating procedure
- ADR-002/003/004/005 — Architectural rationale for the orchestration model

---

_Maintained by: Architect Alphonso_  
_For architecture questions, see: `.github/agents/architect.agent.md`_
