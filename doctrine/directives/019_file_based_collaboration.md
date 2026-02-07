<!-- The following information is to be interpreted literally -->

# 019 File-Based Collaboration Framework Directive

**Purpose:** Guide agents in participating in the asynchronous file-based orchestration system for multi-agent collaboration.

**Core Concepts:
** See [Orchestration](../GLOSSARY.md#orchestration), [Task Lifecycle](../GLOSSARY.md#task-lifecycle), [Handoff](../GLOSSARY.md#handoff), and [Work Log](../GLOSSARY.md#work-log) in the glossary.

## Core Principle

All inter-agent coordination happens through YAML task files in `${WORKSPACE_ROOT}/collaboration/` that move through a defined lifecycle: **new → assigned →
in_progress → done → archive**.

## Agent Responsibilities

1. **Check for assigned work** in `${WORKSPACE_ROOT}/collaboration/assigned/<your-agent-name>/`
2. **Process tasks** according to priority (critical > high > normal > low)
3. **Delegate** work outside your specialization to appropriate agents
4. **Log your work** in `${WORKSPACE_ROOT}/collaboration/done/<your-agent-name>/`
5. **Create work logs** in `${WORKSPACE_ROOT}/reports/logs/<your-agent-name>/`

## Approach Reference

**CRITICAL:** Load only the step relevant to your current task phase to maintain token discipline.

See `.github/agents/approaches/file_based_collaboration/README.md` for:

- Complete task lifecycle overview
- Step-by-step procedures (one file per step)
- Delegation patterns
- Error handling protocols
- Automation script references

## Quick Procedure

1. Check `${WORKSPACE_ROOT}/collaboration/assigned/<your-agent-name>/` for tasks
2. Load approach step for current phase (check work → prioritize → process → delegate → log)
3. Follow approach guidance for that specific step
4. Update task status and create work logs
5. Move completed tasks to `${WORKSPACE_ROOT}/collaboration/done/<your-agent-name>/`

## Automation Scripts

- Task assignment: `ops/scripts/orchestration/agent_orchestrator.py`
- Agent base class: `ops/scripts/orchestration/agent_base.py`
- Task validation: `validation/validate-task-schema.py`

## Integration

This directive complements:

- **012 Common Operating Procedures**: General behavioral norms
- **014 Work Log Creation**: Logging standards
- **009 Role Capabilities**: Understanding specialization boundaries

## Usage

```
/require-directive 019
```

When active in the orchestration system, always check for assigned work before requesting human direction.

## Related Documentation

- `${WORKSPACE_ROOT}/collaboration/README.md` - Collaboration directory guide
- `work/README.md` - Complete work directory documentation
- `templates/task-descriptor.yaml` - Task YAML schema
- ADR-002: File-Based Asynchronous Agent Coordination
- ADR-003: Task Lifecycle and State Management

---

**Remember:** Trust the process. Load only task-relevant approach steps. Focus on your specialization. Delegate effectively.
