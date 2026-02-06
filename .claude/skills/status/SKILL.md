---
name: "status"
description: "Assess current implementation state: pending tasks, active work, progress metrics, blockers, and next recommended batch. Provides Planning Petra's executive view."
version: "1.0.0"
type: "coordination"
category: "planning"
---

# Status: Planning State Assessment

Initialize as Planning Petra to assess current implementation state and provide an executive summary of progress, tasks, and next steps.

## Instructions

Initialize as Planning Petra. Assess current implementation state:

1. **Check repository state:**
   - Current branch and git status
   - Recent commits (last 5-10)

2. **Review task queues:**
   - List `work/collaboration/inbox/` (pending tasks)
   - List `work/collaboration/assigned/` (in-progress tasks)
   - List `work/collaboration/done/` (recently completed)

3. **Read planning documents (if present):**
   - `docs/architecture/roadmap-*.md` (feature roadmaps)
   - `work/collaboration/NEXT_BATCH.md` (current/next batch)
   - `work/planning/*.md` (planning artifacts)

4. **Review recent activity:**
   - Work logs in `work/reports/logs/` (last 2-3 days)
   - Recent ADRs in `docs/architecture/adrs/`

5. **Provide executive summary:**

   **Current Milestone/Phase:**
   - Name and progress (% complete)
   - Tasks: completed / in-progress / remaining

   **Task Queue Overview:**
   - Inbox: count by priority (critical/high/medium/low)
   - Assigned: agent, task, estimated completion
   - Done (recent): completed this session/day

   **Blockers or Decisions Needed:**
   - Blocking issues preventing progress
   - Decisions requiring human input
   - Dependencies waiting on external factors

   **Next Recommended Batch:**
   - Batch ID/name (e.g., "M3 Batch 3.1")
   - Tasks included (2-4 tasks max)
   - Total estimated time
   - Prerequisites satisfied?

   **Overall Project Health:**
   - Status: `ON TRACK` | `AT RISK` | `BLOCKED`
   - Rationale for status
   - Recommended actions

## Output Format

```markdown
## Current State Assessment

**Date:** YYYY-MM-DD
**Branch:** <current-branch>
**Mode:** `/analysis-mode`

### Milestone Progress

**Current:** M2 Tool Integration - 75% complete
- Completed: 3/4 tasks (Batch 2.1, 2.2)
- In Progress: 1/4 tasks (Batch 2.3)
- Remaining: 0/4 tasks

**Next:** M3 Cost Optimization - 0% complete

### Task Queue

**Inbox (3 tasks):**
- 2 HIGH priority (backend-dev)
- 1 MEDIUM priority (writer-editor)

**Assigned (1 task):**
- backend-dev: GenericYAMLAdapter implementation (3h remaining)

**Done (recent, 5 tasks):**
- M2 Batch 2.1: Adapter base infrastructure (✅)
- M2 Batch 2.2: ClaudeCodeAdapter reference (✅)

### Blockers & Decisions

**None currently** ✅

OR

**Blocker 1:** Human approval needed for budget enforcement policy
- Impact: M3 Batch 3.2 cannot proceed
- Required by: 2026-02-08
- Recommended action: Schedule review meeting

### Next Recommended Batch

**M2 Batch 2.3: Generic YAML Adapter** (2 tasks, ~5h)
- Task 1: GenericYAMLAdapter implementation [HIGH] (3h)
- Task 2: ENV variable support [HIGH] (2h)
- Prerequisites: ✅ All satisfied (adapter base done)
- Ready to start: YES

### Overall Health

**Status:** 🟢 ON TRACK

**Rationale:**
- M1-M2 progressing 40% faster than estimated
- All quality gates passing (90%+ test coverage)
- No blocking issues
- Clear path forward to M3

**Recommended Actions:**
1. Execute M2 Batch 2.3 (via `/iterate`)
2. Schedule M3 planning session
3. Continue current velocity
```

## Use Cases

**Before starting work session:**
```
User: /status
Agent: [Provides current state summary]
User: /iterate
```

**Mid-session progress check:**
```
User: /status
Agent: [Shows updated progress, tasks completed this session]
```

**Decision point check:**
```
User: /status
Agent: [Identifies blocker requiring human decision]
User: [Makes decision]
User: /iterate
```

## Related Skills

- `/iterate` - Execute next batch after reviewing status
- `agents/prompts/iteration-orchestration.md` - Full workflow reference

## References

- **Prompt Template:** `agents/prompts/iteration-orchestration.md`
- **Approach:** `.github/agents/approaches/work-directory-orchestration.md`
- **Directive 019:** `.github/agents/directives/019_file_based_collaboration.md`
