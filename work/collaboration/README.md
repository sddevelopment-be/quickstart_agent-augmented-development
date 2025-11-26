# Collaboration Directory

This directory contains the file-based orchestration system for multi-agent coordination.

## Purpose

Enable transparent, asynchronous, Git-native collaboration between specialized agents through task files that move through a defined lifecycle.

## Structure

```
collaboration/
  inbox/              # New tasks awaiting assignment
  assigned/           # Tasks assigned to specific agents
    <agent-name>/     # Agent-specific task queues
  done/               # Completed tasks (organized by agent)
    <agent-name>/     # Agent-specific completion records
  archive/            # Long-term retention (by month)
    YYYY-MM/          # Monthly archive folders
  *.md                # System-wide coordination files
```

## Key Files

- **AGENT_STATUS.md**: Real-time dashboard of agent activity
- **HANDOFFS.md**: Log of agent-to-agent task transitions
- **WORKFLOW_LOG.md**: System-wide orchestration events
- **orchestration-*.md**: Implementation plans and architecture

## Task Lifecycle

```
┌─────┐     ┌──────────┐     ┌─────────────┐     ┌──────┐     ┌─────────┐
│ new │ ──> │ assigned │ ──> │ in_progress │ ──> │ done │ ──> │ archive │
└─────┘     └──────────┘     └─────────────┘     └──────┘     └─────────┘
  inbox/      assigned/            ↓              done/        archive/
                                   │
                                   v
                               ┌───────┐
                               │ error │
                               └───────┘
```

## For Agents

If you are an agent operating in this framework:

1. **Check assigned work**: Look in `assigned/<your-name>/` for tasks
2. **Prioritize**: Process critical/high priority tasks first
3. **Process**: Update status, perform work, add results, move to `done/<your-name>/`
4. **Delegate**: Use `next_agent` in result block to hand off work
5. **Log**: Document your work in `work/reports/logs/<your-name>/`

**See:** Directive 019 (File-Based Collaboration) for complete guidance:
```
/require-directive 019
```

## For Humans

- **Create tasks**: Add YAML files to `inbox/` using `docs/templates/task-descriptor.yaml`
- **Monitor**: Check `AGENT_STATUS.md` and `WORKFLOW_LOG.md` for system activity
- **Review**: Inspect `done/<agent>/` for completed work
- **Troubleshoot**: Check agent logs in `work/reports/logs/` for issues

## Orchestration

The Agent Orchestrator (`ops/scripts/orchestration/agent_orchestrator.py`) automatically:
- Assigns tasks from inbox to agents
- Creates follow-up tasks from handoffs
- Monitors for timeouts
- Archives old completed tasks

## Related Documentation

- `work/README.md`: Complete work directory documentation
- `docs/architecture/adrs/ADR-002-file-based-async-coordination.md`: Design rationale
- `docs/architecture/adrs/ADR-003-task-lifecycle-state-management.md`: State management
- `docs/architecture/adrs/ADR-004-work-directory-structure.md`: Directory structure
- `.github/agents/directives/019_file_based_collaboration.md`: Agent directive
