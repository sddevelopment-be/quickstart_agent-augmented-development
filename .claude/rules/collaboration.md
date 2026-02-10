<!-- Source: 019_file_based_collaboration.md -->
# Collaboration

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

See `approaches/file_based_collaboration/README.md` for:

- Complete task lifecycle overview
- Step-by-step procedures (one file per step)
- Delegation patterns
- Error handling protocols
- Automation script references

## Quick Procedure

1. Check `${WORKSPACE_ROOT}/collaboration/assigned/<your-agent-name>/` for tasks
2. Load approach step for current phase (check work → prioritize → process → delegate → log)
3. **Use task management scripts** (do NOT manually move files):
   - **Start:** `python tools/scripts/start_task.py TASK_ID`
   - **Complete:** `python tools/scripts/complete_task.py TASK_ID`
   - **Freeze (if blocked):** `python tools/scripts/freeze_task.py TASK_ID --reason "Reason"`
   - **List tasks:** `python tools/scripts/list_open_tasks.py [--status STATUS] [--agent AGENT]`
4. Follow approach guidance for that specific step
5. Update task result block and create work logs
6. Scripts automatically handle file movements and validation

## Task Management Scripts

**CRITICAL:** Always use the provided scripts instead of manual file operations.

### Script Usage Examples

```bash
python tools/scripts/start_task.py 2025-11-23T1500-structural-repomap

python tools/scripts/complete_task.py 2025-11-23T1500-structural-repomap

python tools/scripts/freeze_task.py 2025-11-23T1500-structural-repomap --reason "Waiting for dependency"

python tools/scripts/list_open_tasks.py --status assigned --agent structural

python tools/scripts/list_open_tasks.py --priority high
```

### Benefits of Script Usage
- ✅ **Validation:** Enforces proper YAML structure and required fields
- ✅ **State Management:** Prevents invalid status transitions
- ✅ **Consistency:** Standardized timestamps and metadata
- ✅ **Auditability:** Clear lifecycle tracking
- ✅ **Error Prevention:** Validates task completeness before changes

### Deprecated Manual Operations
❗️ **Do NOT:**
- Manually move task files between directories
- Directly edit status fields in YAML
- Skip validation by manual file operations

Use scripts to ensure data integrity and proper orchestration.
