# Task Cold Storage ("Fridge")

**Purpose:** Archive for tasks that are no longer active but may have historical value.

## Directory Structure

```
fridge/
├── README.md       # This file
├── complete/       # Tasks that were successfully completed
└── outdated/       # Tasks that became obsolete or irrelevant
```

## When to Use Cold Storage

### Move to `complete/`
- ✅ Task was successfully completed and delivered
- ✅ Output artifacts are in version control
- ✅ No further work needed
- ✅ Keeping for historical reference only

### Move to `outdated/`
- ⏸️ Task became irrelevant due to architecture changes
- ⏸️ Requirements changed and task is no longer needed
- ⏸️ Superseded by other work
- ⏸️ POC/research tasks that concluded
- ⏸️ Blocked indefinitely with no clear path forward

## How to Archive Tasks

1. **Move the task file** from `assigned/<agent>/` to appropriate fridge subdirectory
2. **Update AGENT_TASKS.md** to remove task from active assignments
3. **Update DEPENDENCIES.md** to remove any dependency references
4. **Document reason** in commit message or task update log

## How to Revive Tasks

If a task needs to be reactivated:

1. **Review and update** the task context and requirements
2. **Update paths** to current repository structure
3. **Move back to** `assigned/<agent>/` or `inbox/`
4. **Update planning docs** (AGENT_TASKS.md, DEPENDENCIES.md, NEXT_BATCH.md)
5. **Assign priority** and add to current batch if urgent

## Organization Guidelines

- **Maintain directory structure**: Keep agent subdirectories (e.g., `complete/backend-dev/`)
- **File naming**: Preserve original task file names for traceability
- **No modifications**: Don't edit task content when archiving (keep as-is for history)
- **Batch operations**: Use scripts for bulk archiving (see tools/scripts/)

## Cold Storage vs Done Directory

| Location | Purpose | Criteria |
|----------|---------|----------|
| `work/collaboration/done/` | Active completion tracking | Recently completed, part of current milestone |
| `work/collaboration/fridge/complete/` | Historical archive | Completed >1 month ago, no active reference |
| `work/collaboration/fridge/outdated/` | Obsolete tasks | Never completed, became irrelevant |

## Maintenance

- **Review quarterly**: Check fridge/ for tasks that can be permanently deleted
- **Retention policy**: Keep for 6-12 months, then consider deletion
- **Git history**: Remember that deleted tasks remain in git history if needed

---

**Last Updated:** 2026-02-08  
**Maintainer:** Planning Petra  
**Related:** AGENT_TASKS.md, POST_REFACTOR_TASK_REVIEW.md
