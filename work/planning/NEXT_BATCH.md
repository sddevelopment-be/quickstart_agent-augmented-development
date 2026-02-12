# Next Batch: Agent Specialization Hierarchy - Phase 1 & Foundations

**Batch ID:** ASH-BATCH-1
**Initiative:** Agent Specialization Hierarchy
**Status:** Ready to Start
**Planned Start:** 2026-02-12 (immediate)
**Target Completion:** 2026-02-26 (2 weeks)
**Planner:** Planning Petra
**Date:** 2026-02-12

---

## Executive Summary

**Theme:** Foundations - Complete Phase 1 (GLOSSARY updates) and prepare Phase 2 (routing algorithm specification)

**Effort:** ~10 hours across 3 agents
**Duration:** 2 weeks (allows parallel work on Dashboard M4 4.3 completion)

**Strategic Context:**
- Completes DDR-011 implementation prerequisites
- Enables Phase 2 (routing algorithm) to start after dashboard work completes
- Leverages underutilized agents (Curator Claire, Architect Alphonso)

**Why This Batch:**
- Phase 1 partially complete (DDR-011 done ✅, GLOSSARY.md updates pending)
- Documentation-focused work doesn't conflict with current dashboard push
- Sets foundation for technical implementation in Phase 2-6

---

## Current State

### Recently Completed

**Dashboard M4 4.3 (In Progress):**
- Initiative tracking panel: In progress (Frontend Freddy, Python Pedro)
- Portfolio view: In progress
- Target completion: Week of 2026-02-17

**Agent Specialization Hierarchy Phase 1 (Partial):**
- ✅ DDR-011 created and approved
- ✅ Architecture design document completed
- ✅ Specification completed (Analyst Annie)
- ❌ GLOSSARY.md updates pending

### Active Work (Current Agent Assignments)

| Agent | Active Tasks | Capacity | Utilization |
|-------|-------------|----------|-------------|
| Architect Alphonso | 4 | 5 | 80% |
| Python Pedro | 6 | 5 | 120% ⚠️ |
| Backend Benny | 6 | 8 | 75% |
| Frontend Freddy | 2 | 5 | 40% |
| Curator Claire | 1 | 5 | 20% |
| Scribe Sally | 2 | 5 | 40% |
| Analyst Annie | 0 | 5 | 0% |

**Key Constraint:** Python Pedro overloaded (120% capacity)
- Mitigation: Defer Pedro-heavy work (Phase 2 implementation) until dashboard complete

---

## Batch Goals

### Primary Objective

Complete Agent Specialization Hierarchy Phase 1 and create comprehensive Phase 2 specification.

### Secondary Objectives

1. Update repository glossary with hierarchy terminology
2. Finalize SELECT_APPROPRIATE_AGENT tactic specification
3. Prepare Phase 2 implementation for post-dashboard execution
4. Validate alignment between DDR-011, architecture design, and specification

---

## Tasks

### Task 1: GLOSSARY.md Hierarchy Terminology Update

**ID:** ASH-P1-T1-GLOSSARY
**Agent:** Curator Claire
**Priority:** HIGH
**Effort:** 3 hours
**Status:** Ready to start

**Scope:**

Add the following terms to `doctrine/GLOSSARY.md`:

1. **Agent Specialization Hierarchy**
   - Definition: Parent-child relationship where specialized agents refine their parent's scope to narrower contexts
   - Example: Python Pedro specializes Backend Benny for Python-specific tasks
   - Cross-reference: DDR-011, architecture design

2. **Parent Agent**
   - Definition: Generalist agent whose collaboration contract and capabilities are inherited by specialist children
   - Example: Backend Benny (parent) → Python Pedro, Java Jenny (children)
   - Cross-reference: `specializes_from` field

3. **Child Agent / Specialist Agent**
   - Definition: Agent that inherits parent's contract but operates in narrower specialization context
   - Example: Python Pedro specializes in Python, Flask, FastAPI
   - Cross-reference: `specialization_context` field

4. **Specialization Context**
   - Definition: Declarative conditions defining when specialist preferred over parent
   - Fields: language, frameworks, file_patterns, domain_keywords, writing_style, complexity_preference
   - Example: Python Pedro's context includes `language: [python]`, `frameworks: [flask, fastapi]`

5. **Routing Priority**
   - Definition: Numeric specificity score (0-100) for specialist agents
   - Default: Parents=50, Specialists=60-90, Local specialists=+20 boost
   - Usage: Tie resolution in SELECT_APPROPRIATE_AGENT

6. **Reassignment Pass**
   - Definition: Manager Mike process that reviews existing task assignments and upgrades to specialists
   - Trigger: Manual invocation, new specialist added, periodic schedule
   - Safety: Skip `in_progress` and `pinned` tasks

7. **SELECT_APPROPRIATE_AGENT**
   - Definition: Orchestration tactic determining most appropriate agent for a task
   - Inputs: Task context (language, files, domain, complexity), agent pool, workload state
   - Output: Selected agent + routing rationale
   - Algorithm: Context match → workload adjustment → complexity adjustment → tie resolution

**Acceptance Criteria:**
- All 7 terms added to GLOSSARY.md
- Each term includes definition, example, cross-references
- Follows existing glossary format and style
- Links to DDR-011 and architecture design
- No conflicts with existing terminology

**Dependencies:** None

**Deliverables:**
- Updated `doctrine/GLOSSARY.md`
- Work log entry documenting changes

---

### Task 2: SELECT_APPROPRIATE_AGENT Tactic Specification

**ID:** ASH-P2-T1-TACTIC-SPEC
**Agent:** Architect Alphonso
**Priority:** HIGH
**Effort:** 4 hours
**Status:** Ready to start

**Scope:**

Create comprehensive tactic document at `doctrine/tactics/SELECT_APPROPRIATE_AGENT.tactic.md`:

**Structure:**
1. **Purpose**
   - What: Determine most appropriate agent for a task
   - When: Initial task assignment, handoff processing, reassignment pass
   - Why: Context-aware routing, workload awareness, automatic fallback

2. **Invocation Conditions**
   - Manager Mike receives new task
   - Manager Mike processes handoff to parent agent
   - Manager Mike runs reassignment pass

3. **Inputs**
   - Task metadata (files, description, priority, complexity)
   - Agent pool (doctrine agents + `.doctrine-config` agents)
   - Current workload state (active tasks per agent)

4. **Procedure (Step-by-Step)**
   - Step 1: Extract task context
     - Infer language from file extensions
     - Extract frameworks from task description
     - Extract domain keywords from title/description
     - Read or infer complexity
   - Step 2: Discover candidates
     - Load agents from `doctrine/agents/`
     - Load local agents from `.doctrine-config/custom-agents/`
     - Filter agents matching task context
     - Include parent agents as fallback
   - Step 3: Calculate match scores
     - Language match: 40% weight
     - Framework match: 20% weight
     - File pattern match: 20% weight
     - Domain keyword match: 10% weight
     - Exact match bonus: 10% weight
   - Step 4: Adjust for workload
     - 0-2 active tasks: No penalty
     - 3-4 active tasks: 15% penalty
     - 5+ active tasks: 30% penalty
   - Step 5: Adjust for complexity
     - Low complexity: Specialist +10% boost
     - Medium complexity: Neutral
     - High complexity: Parent +10%, Specialist -10%
   - Step 6: Resolve ties
     - Highest adjusted score wins
     - If tie: Prefer language match (for programming tasks)
     - If tie: Prefer higher routing priority
     - If tie: Manager Mike free choice (first candidate)
   - Step 7: Return selection
     - Selected agent name
     - Match score breakdown
     - Textual rationale

5. **Outputs**
   - Selected agent name
   - Match score (0.0-1.0)
   - Workload-adjusted score
   - Complexity-adjusted score
   - Rationale string
   - Fallback agent (if applicable)

6. **Examples**
   - Example 1: Python task → Python Pedro
   - Example 2: Specialist overloaded → Backend Benny fallback
   - Example 3: Local specialist → User Guide Ursula selected
   - Example 4: High complexity → Backend Benny preferred over Pedro

7. **Decision Tree**
   - Flowchart showing routing logic
   - Visual representation of scoring factors

8. **Logging Requirements**
   - Every invocation produces structured log entry
   - Log includes: timestamp, task ID, selected agent, score breakdown, rationale

**Acceptance Criteria:**
- Tactic document follows template format
- All 8 sections complete
- At least 4 examples included
- Decision tree flowchart included
- Algorithm pseudocode included
- Cross-references to DDR-011, architecture design, specification
- Reviewed by Planning Petra for completeness

**Dependencies:** Task 1 (GLOSSARY.md) should be complete for terminology consistency

**Deliverables:**
- `doctrine/tactics/SELECT_APPROPRIATE_AGENT.tactic.md`
- Work log entry documenting creation

---

### Task 3: Architecture Design Review and Validation

**ID:** ASH-P1-T2-ARCH-REVIEW
**Agent:** Architect Alphonso
**Priority:** MEDIUM
**Effort:** 1 hour
**Status:** Ready to start

**Scope:**

Review existing architecture design document and validate alignment with:
- DDR-011 (decision record)
- Specification (SPEC-ASH-001)
- Tactic document (Task 2 deliverable)
- GLOSSARY.md updates (Task 1 deliverable)

**Review Checklist:**
1. Domain model consistent across all documents
2. Routing algorithm specification matches architecture design
3. Agent profile schema changes documented consistently
4. Phase breakdown in architecture matches plan
5. Success metrics aligned across documents
6. No contradictions or conflicts

**Actions:**
- Identify any misalignments
- Update architecture design if needed
- Document validation results in work log

**Acceptance Criteria:**
- Architecture design reviewed
- No critical misalignments found (or resolved if found)
- Validation report created
- Architecture design marked as "Reviewed - 2026-02-12"

**Dependencies:** Task 1, Task 2 (for cross-reference validation)

**Deliverables:**
- Validation report (work log entry or separate document)
- Updated `docs/architecture/design/agent-specialization-hierarchy.md` (if needed)

---

### Task 4: Phase 2 Implementation Preparation

**ID:** ASH-BATCH-1-PREP
**Agent:** Planning Petra
**Priority:** LOW
**Effort:** 2 hours
**Status:** Ready to start

**Scope:**

Prepare for Phase 2 (routing algorithm implementation) to start after dashboard completion:

1. **Create detailed task breakdown for Phase 2:**
   - Task: Implement `extract_task_context()` function
   - Task: Implement `calculate_match_score()` function
   - Task: Implement `adjust_for_workload()` function
   - Task: Implement `adjust_for_complexity()` function
   - Task: Implement `resolve_ties()` function
   - Task: Implement `select_appropriate_agent()` entry point
   - Task: Add structured logging
   - Task: Write unit tests

2. **Capacity check for Phase 2 start:**
   - Confirm Dashboard M4 4.3 completion date
   - Check Python Pedro availability post-dashboard
   - Confirm Backend Benny availability for parallel work

3. **Dependency validation:**
   - Ensure Task 2 (tactic spec) complete before Phase 2 implementation
   - Ensure GLOSSARY.md updated for implementation reference

**Acceptance Criteria:**
- Phase 2 tasks created in `work/collaboration/inbox/`
- Phase 2 start date confirmed (contingent on dashboard completion)
- Agent assignments validated
- Dependencies documented

**Dependencies:** Task 2 (tactic spec must be complete for implementation reference)

**Deliverables:**
- 8 task files for Phase 2 in inbox
- Batch 2 planning document (brief)

---

## Schedule

### Week 1 (2026-02-12 to 2026-02-18)

**Monday-Tuesday (Feb 12-13):**
- Task 1: Curator Claire starts GLOSSARY.md updates (3h)
- Task 2: Architect Alphonso starts tactic specification (2h)

**Wednesday-Friday (Feb 14-16):**
- Task 2: Architect Alphonso continues tactic specification (2h)
- Task 3: Architect Alphonso starts architecture review (1h)
- Task 1: Curator Claire completes GLOSSARY.md (if not done)

**Concurrent Work:**
- Dashboard M4 4.3: Frontend Freddy, Python Pedro continue work

---

### Week 2 (2026-02-19 to 2026-02-26)

**Monday-Wednesday (Feb 19-21):**
- Task 2: Architect Alphonso completes tactic specification
- Task 3: Architect Alphonso completes architecture review
- Task 4: Planning Petra prepares Phase 2 tasks (2h)

**Thursday-Friday (Feb 22-23):**
- Task 4: Planning Petra completes Phase 2 preparation
- Review: All batch deliverables reviewed by Planning Petra
- Handoff: Phase 2 tasks ready for assignment after dashboard complete

**Expected Dashboard Completion:** Week of Feb 17-21
**Phase 2 Start:** Week of Feb 24 (if dashboard complete)

---

## Success Criteria

### Batch-Level Success

- ✅ All 7 glossary terms added to `doctrine/GLOSSARY.md`
- ✅ SELECT_APPROPRIATE_AGENT tactic document complete
- ✅ Architecture design reviewed and validated
- ✅ Phase 2 tasks created and ready for assignment
- ✅ No conflicts with concurrent dashboard work
- ✅ Zero capacity overruns (all agents within limits)

### Phase-Level Success (Phase 1 Complete)

- ✅ DDR-011 approved and published ✅ (already done)
- ✅ GLOSSARY.md updated with hierarchy terminology
- ✅ Architecture design validated and current
- ✅ All terminology consistent across documents

---

## Dependencies

### Upstream (Must Complete First)

- ✅ DDR-011 created and approved
- ✅ Architecture design document created
- ✅ Specification (SPEC-ASH-001) created

### Parallel (Can Run Concurrently)

- Dashboard M4 4.3 (different agents, different focus)
- Terminology Alignment spec review (different agents)

### Downstream (Enabled By This Batch)

- Phase 2 implementation (routing algorithm)
- Phase 3 implementation (agent profiles)
- Manager Mike enhancement (Phase 4)

---

## Risk Management

### Batch-Specific Risks

**RISK-B1: Tactic Specification Takes Longer Than Expected**
- Impact: Phase 2 start delayed
- Probability: LOW-MEDIUM (4h estimate may be tight)
- Mitigation: Architect Alphonso can extend to 6h if needed, still completes in Week 2
- Owner: Planning Petra monitors progress

**RISK-B2: GLOSSARY.md Terminology Conflicts with Existing Terms**
- Impact: Rework needed, terminology inconsistency
- Probability: LOW (terms are net-new)
- Mitigation: Curator Claire reviews existing glossary first, coordinates with Terminology spec
- Owner: Curator Claire

**RISK-B3: Dashboard Completion Delayed**
- Impact: Phase 2 start delayed (Python Pedro not available)
- Probability: LOW-MEDIUM (dashboard in final stages)
- Mitigation: Phase 2 can start with Backend Benny if Pedro unavailable
- Owner: Manager Mike tracks dashboard completion

### Ongoing Risks (From PLAN_OVERVIEW.md)

**RISK-001: Python Pedro Overload**
- Status: Mitigated for this batch (no Pedro assignments)
- Next Review: Phase 2 planning (after dashboard complete)

---

## Agent Assignments

| Agent | Task(s) | Effort | Timing |
|-------|---------|--------|--------|
| **Curator Claire** | Task 1 (GLOSSARY.md) | 3h | Week 1 |
| **Architect Alphonso** | Task 2 (Tactic spec), Task 3 (Review) | 5h | Week 1-2 |
| **Planning Petra** | Task 4 (Phase 2 prep) | 2h | Week 2 |

**Total Effort:** ~10 hours
**Total Agents:** 3

**Capacity Validation:**
- Curator Claire: 1 current task, 80% available → ✅ Has capacity
- Architect Alphonso: 4 current tasks, 20% available → ✅ Can accommodate 5h over 2 weeks
- Planning Petra: Planning role → ✅ Has capacity

---

## Deliverables Summary

### Documentation

- ✅ `doctrine/GLOSSARY.md` (updated with 7 new terms)
- ✅ `doctrine/tactics/SELECT_APPROPRIATE_AGENT.tactic.md` (complete tactic spec)
- ✅ Architecture design validation report

### Planning Artifacts

- ✅ Phase 2 task files (8 tasks in inbox)
- ✅ Batch 2 planning document

### Work Logs

- ✅ Curator Claire: GLOSSARY.md update log
- ✅ Architect Alphonso: Tactic specification and review log
- ✅ Planning Petra: Phase 2 preparation log

---

## Validation Checklist

Before marking this batch complete:

- [ ] All 7 terms added to GLOSSARY.md with examples
- [ ] GLOSSARY.md cross-references DDR-011 and architecture design
- [ ] SELECT_APPROPRIATE_AGENT tactic document complete
- [ ] Tactic includes all 8 required sections
- [ ] Tactic includes decision tree and examples
- [ ] Architecture design reviewed and validated
- [ ] No misalignments found (or resolved)
- [ ] Phase 2 tasks created (8 tasks)
- [ ] Phase 2 agent assignments validated
- [ ] Phase 2 start date confirmed
- [ ] All work logs created
- [ ] Planning Petra final review complete

---

## Next Batch Preview

**Batch 2: Phase 2 Implementation (Routing Algorithm)**

**Start Date:** ~2026-02-24 (contingent on dashboard completion)
**Duration:** 2 weeks
**Effort:** ~12 hours

**Focus:**
- Implement routing algorithm in Python
- Unit tests for all scoring functions
- Structured logging for routing decisions
- Code review and validation

**Agents:**
- Python Pedro: Implementation and unit tests (8h)
- Architect Alphonso: Code review (1h)

**Dependencies:**
- Dashboard M4 4.3 complete (Python Pedro available)
- Batch 1 complete (tactic spec ready)

---

## Approval

**Planning Petra:** Batch plan submitted - 2026-02-12
**Manager Mike:** Pending (task assignment approval)
**Architect Alphonso:** Pending (technical review)

---

**Status:** Ready to Start
**Next Action:** Manager Mike creates task assignments from this batch plan
**Version:** 1.0.0
