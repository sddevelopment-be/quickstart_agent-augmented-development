# Task Management Script Usage Discrepancy Report

**Date:** 2026-02-09  
**Agent:** Curator Claire  
**Issue:** Inconsistent task lifecycle management documentation  

## Problem Statement

Documentation analysis reveals gaps between available task management scripts and orchestration guidance. Current documentation doesn't clearly instruct agents to use dedicated scripts, leading to manual file operations that bypass validation and introduce inconsistencies.

## Scripts Available (✅ Implemented)

Located in `tools/scripts/`:

1. **complete_task.py** - Moves tasks to done/ with validation
   - Validates result block exists before completion
   - Enforces status transitions via centralized state machine
   - Updates timestamps and moves to appropriate done/{agent}/ directory

2. **start_task.py** - Updates task status to in_progress  
   - Validates state transitions
   - Adds started_at timestamp
   - Preserves task in assigned/{agent}/ directory

3. **freeze_task.py** - Moves tasks to fridge/ with reason
   - Adds freeze metadata and reason
   - Preserves original status
   - Moves to fridge/ directory for later review

4. **list_open_tasks.py** - Lists all open tasks with filters
   - Supports filtering by status, agent, priority
   - Multiple output formats (table, json)

## Documentation Issues (❗️ Gaps Found)

### 1. Work Directory Orchestration Approach

**File:** `doctrine/approaches/work-directory-orchestration.md`

**Current State:** Manual task lifecycle instructions
- Line 117: "Poll `${WORKSPACE_ROOT}/collaboration/assigned/<agent>/` for `status: assigned`"
- Line 118: "Update to `in_progress`, stamp `started_at`, and commit change"
- Line 123: "Move file to `${WORKSPACE_ROOT}/collaboration/done/<agent>/`"

**Missing:** Explicit script usage instructions

### 2. Directive 019 - File-Based Collaboration

**File:** `doctrine/directives/019_file_based_collaboration.md`

**Current State:** High-level process guidance
- Line 17: Generic "Process tasks" instruction
- Line 21: Generic "Log your work" instruction
- Line 43: Generic "Move completed tasks" instruction

**Missing:** Specific script invocation patterns

### 3. Iterate Skill Documentation

**File:** `.claude/skills/iterate/SKILL.md`

**Current State:** Manual orchestration instructions
- Line 37: "Move completed task: `inbox/` → `done/<agent>/`"

**Missing:** Script usage in TDD/ATDD workflow

## Recommended Corrective Actions

### Priority 1 - Update Orchestration Approach

Update `doctrine/approaches/work-directory-orchestration.md` section "Specialized Agents" to include explicit script usage:

**Add after line 116:**

```markdown
## Task Management Scripts

Agents MUST use the provided scripts to ensure proper validation and state transitions:

### Starting Tasks
```bash
python tools/scripts/start_task.py TASK_ID
```

### Completing Tasks
```bash
python tools/scripts/complete_task.py TASK_ID
```

### Freezing Tasks (when blocked)
```bash
python tools/scripts/freeze_task.py TASK_ID --reason "Reason for pause"
```

### Listing Open Tasks
```bash
python tools/scripts/list_open_tasks.py [--status STATUS] [--agent AGENT]
```
```

**Update existing instructions to reference scripts instead of manual operations.**

### Priority 2 - Update Directive 019

Add script usage section to `doctrine/directives/019_file_based_collaboration.md`

### Priority 3 - Update Iterate Skill

Update `.claude/skills/iterate/SKILL.md` to use proper script calls in the TDD cycle

## Validation Criteria

✅ All documentation explicitly mentions script usage  
✅ No remaining references to manual file operations  
✅ Examples show proper script invocation  
✅ Validation requirements are clear  

## Next Steps

1. Apply corrective actions in priority order
2. Validate cross-references remain consistent
3. Create validation summary report
