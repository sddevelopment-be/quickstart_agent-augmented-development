# Plan Overview: Agent Specialization Hierarchy

**Plan ID:** PLAN-ASH-001
**Initiative:** Agent Specialization Hierarchy
**Specification:** `specifications/initiatives/agent-specialization-hierarchy/agent-specialization-hierarchy.md`
**Architecture Design:** `docs/architecture/design/agent-specialization-hierarchy.md`
**DDR:** DDR-011
**Planner:** Planning Petra
**Date:** 2026-02-12
**Status:** Ready for Approval

---

## Executive Summary

**Effort:** 54-68 hours across 6 phases, 8-10 weeks
**Agents:** 7 specialists (Architect Alphonso, Python Pedro, Backend Benny, Curator Claire, Scribe Sally, Analyst Annie, Manager Mike)
**Critical Path:** Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6

**Strategic Value:**
- Improve task routing accuracy from ~50% to >90% specialist selection
- Enable workload-aware fallback (prevent specialist overload)
- Support repository-specific specialists via `.doctrine-config`
- Reduce manual handoff overhead by 70%+

**Key Innovation:** Context-based agent routing with parent-child specialization hierarchy, automatic fallback chains, and local specialist discovery.

---

## Problem Statement

### Current State

The orchestration system (Manager Mike) assigns tasks using:
1. Explicit `agent` field in task YAML
2. Simple keyword matching on task descriptions

Both mechanisms treat agents as a flat pool with no hierarchy, context matching, or workload awareness.

### Observed Failures

| Failure Mode | Example | Impact |
|--------------|---------|--------|
| **Suboptimal routing** | Python FastAPI task → Backend Benny instead of Python Pedro | Specialist expertise unused, lower output quality |
| **Specialist overload** | All Python tasks → Pedro regardless of workload | Tasks pile up, throughput degrades |
| **No complexity matching** | Complex cross-domain task → narrow specialist | Specialist lacks broader context, rework needed |
| **Missing local specialists** | User guide task not routed to User Guide Ursula (`.doctrine-config`) | Repository-specific expertise unused |
| **Manual handoff burden** | Agents must explicitly name every downstream specialist | New specialists require updating every handoff source |

### Business Value

- **Quality:** Tasks handled by agents with deepest relevant expertise
- **Throughput:** Workload-aware routing prevents bottlenecks
- **Scalability:** Adding specialists doesn't require updating existing agents
- **Customization:** Teams define project-specific specialists without framework changes

---

## Solution Architecture

### Conceptual Model

```
Backend Specialist (Backend Benny) [parent, priority=50]
  ├── Python Specialist (Python Pedro) [child, priority=80]
  ├── Java Specialist (Java Jenny) [child, priority=80]
  └── Node.js Specialist [future child]

Frontend Specialist (Frontend Freddy) [parent, priority=50]
  ├── React Specialist [future child]
  └── Vue Specialist [future child]

Writer-Editor (Editor Eddy) [parent, priority=50]
  ├── User Guide Specialist (Ursula) [local child, priority=85]
  └── API Docs Specialist [future child]
```

### Key Components

1. **Agent Profile Schema Enhancement**
   - `specializes_from`: Declares parent agent
   - `routing_priority`: Numeric specificity score (0-100)
   - `specialization_context`: Conditions for specialist selection
     - `language`: Programming languages (python, java, etc.)
     - `frameworks`: Libraries/frameworks (flask, spring, etc.)
     - `file_patterns`: Glob patterns (`**/*.py`)
     - `domain_keywords`: Task domain terms
     - `writing_style`: For writing-focused agents
     - `complexity_preference`: Preferred task complexity levels

2. **SELECT_APPROPRIATE_AGENT Tactic**
   - Context extraction (language, files, domain, complexity)
   - Candidate discovery (doctrine + `.doctrine-config`)
   - Match scoring (language 40%, framework 20%, files 20%, keywords 10%, exact 10%)
   - Workload adjustment (penalty if overloaded)
   - Complexity adjustment (specialists prefer low/medium, parents prefer high)
   - Tie resolution (language match > score > priority > free choice)

3. **Handoff Protocol Enhancement**
   - Intercept handoffs to parent agents
   - Invoke SELECT_APPROPRIATE_AGENT to check for specialists
   - Override assignment if specialist available and not overloaded

4. **Reassignment Pass**
   - Periodic review of task assignments
   - Upgrade generic assignments to specialists
   - Safety: Don't reassign `in_progress` or `pinned` tasks

5. **Local Specialization Override**
   - Discover agents in `.doctrine-config/custom-agents/`
   - Apply +20 routing priority boost
   - Support repository-specific specialists (User Guide Ursula, etc.)

---

## Phase Breakdown

### Phase 1: Core Decision & Glossary (6-8 hours) - PARTIALLY COMPLETE

**Status:** DDR-011 completed ✅, GLOSSARY.md updates pending

**Deliverables:**
- ✅ DDR-011 (Agent Specialization Hierarchy)
- Update `doctrine/GLOSSARY.md` with terminology:
  - Agent Specialization Hierarchy
  - Parent Agent
  - Child Agent / Specialist Agent
  - Specialization Context
  - Routing Priority
  - Reassignment Pass
  - SELECT_APPROPRIATE_AGENT
- Document domain model in architecture design ✅

**Assigned:**
- Curator Claire: GLOSSARY.md updates (3 hours)
- Architect Alphonso: Architecture design review (1 hour)

**Dependencies:** None

**Acceptance Criteria:**
- All 7 terms added to GLOSSARY.md
- Cross-references to DDR-011 and architecture design
- Examples for each term
- Architecture design reviewed and approved

**Risk:** Low - foundational documentation phase

---

### Phase 2: SELECT_APPROPRIATE_AGENT Tactic (10-12 hours)

**Status:** Not Started

**Deliverables:**
- Create `doctrine/tactics/SELECT_APPROPRIATE_AGENT.tactic.md`
  - Tactic purpose and invocation conditions
  - Step-by-step procedure (context extraction, scoring, selection)
  - Algorithm pseudocode
  - Examples and scenarios
- Python reference implementation (`tools/orchestration/agent_selector.py`)
  - `extract_task_context()` function
  - `discover_candidates()` function
  - `calculate_match_score()` function
  - `adjust_for_workload()` function
  - `adjust_for_complexity()` function
  - `resolve_ties()` function
  - `select_appropriate_agent()` main entry point
- Logging and telemetry
  - Structured log entry for every routing decision
  - Match score breakdown
  - Textual rationale

**Assigned:**
- Architect Alphonso: Tactic document (4 hours)
- Python Pedro: Reference implementation (6 hours)
- Python Pedro: Unit tests (2 hours)

**Dependencies:** Phase 1 complete (terminology defined)

**Acceptance Criteria:**
- Tactic document follows template, includes decision tree
- Routing algorithm passes unit tests:
  - Language match correctly scores
  - Workload penalty applied correctly
  - Complexity adjustment works
  - Tie resolution deterministic
- Every invocation produces structured log entry

**Risk:** Medium - complex routing logic, requires comprehensive testing

---

### Phase 3: Agent Profile Schema Enhancement (8-10 hours)

**Status:** Not Started

**Deliverables:**
- Update `doctrine/templates/agent-profile-template.md`
  - Add optional `specializes_from` field
  - Add optional `routing_priority` field (default 50)
  - Add optional `max_concurrent_tasks` field
  - Add optional `specialization_context` block
  - Document each field with examples
- Update agent profiles with hierarchy metadata:
  - Python Pedro: `specializes_from: backend-benny`, context for Python
  - Java Jenny: `specializes_from: backend-benny`, context for Java
  - Backend Benny: Parent agent, broad `specialization_context`
- Create `tools/validators/validate-agent-hierarchy.py`
  - Check for circular dependencies
  - Check for missing parent references
  - Check for duplicate agent names
  - Check for priority conflicts
  - Report all issues with non-zero exit code

**Assigned:**
- Curator Claire: Template update (2 hours)
- Backend Benny: Agent profile updates (4 hours) - REASSIGNED from Pedro
- Python Pedro: Validation script (2 hours)

**Dependencies:** Phase 1 complete (glossary terminology)

**Acceptance Criteria:**
- Template updated, all fields documented
- Python Pedro, Java Jenny, Backend Benny profiles updated
- Validation script detects circular dependencies
- Validation script detects missing parents
- All agent profiles pass validation

**Risk:** Low - additive schema changes, backward compatible

---

### Phase 4: Manager Mike Enhancement (10-12 hours)

**Status:** Not Started

**Deliverables:**
- Update `doctrine/agents/manager.agent.md` profile
  - Reference SELECT_APPROPRIATE_AGENT tactic
  - Document handoff enhancement behavior
  - Document reassignment pass procedure
- Implement handoff protocol enhancement
  - Detect handoffs to parent agents
  - Invoke SELECT_APPROPRIATE_AGENT on handoff context
  - Override assignment if specialist selected
  - Log routing override decision
- Implement reassignment pass script (`tools/scripts/reassignment_pass.py`)
  - Scan `work/collaboration/assigned/` for eligible tasks
  - Invoke SELECT_APPROPRIATE_AGENT for each task
  - Move tasks to new agent directory if reassigned
  - Generate reassignment report (Markdown)
  - Safety: Skip `in_progress` and `pinned` tasks

**Assigned:**
- Python Pedro: Handoff protocol enhancement (5 hours)
- Backend Benny: Reassignment pass script (5 hours)
- Architect Alphonso: Manager Mike profile update (2 hours)

**Dependencies:** Phase 2 (routing algorithm), Phase 3 (agent profiles)

**Acceptance Criteria:**
- Handoff to `backend-benny` with Python context routes to `python-pedro`
- Handoff override logged with rationale
- Reassignment pass generates report with all reassignments
- Reassignment pass does NOT touch `in_progress` tasks
- Reassignment pass does NOT touch `pinned` tasks
- Reassignment report includes workload distribution post-reassignment

**Risk:** Medium - handoff override must preserve task context integrity

---

### Phase 5: Validation & Testing (12-16 hours)

**Status:** Not Started

**Deliverables:**
- Unit tests for routing algorithm
  - Test context extraction (language inference, framework detection)
  - Test match scoring (language, framework, file pattern, keywords)
  - Test workload penalty (0-2 tasks, 3-4 tasks, 5+ tasks)
  - Test complexity adjustment (low, medium, high)
  - Test tie resolution (language preference, priority, free choice)
- Integration tests
  - End-to-end routing (task → specialist selection)
  - Handoff override (parent → specialist)
  - Reassignment pass (generic → specialist upgrade)
  - Local specialist discovery (`.doctrine-config` agents)
  - Parent fallback (specialist overloaded)
- Test scenarios
  - Python task routes to Python Pedro
  - Specialist overload falls back to Backend Benny
  - Local specialist (User Guide Ursula) preferred over framework agent
  - High complexity task prefers parent over specialist
  - Circular dependency detected by validation
- Coverage target: >85% for routing algorithm functions

**Assigned:**
- Python Pedro: Unit tests (6 hours)
- Backend Benny: Integration tests (6 hours)
- Analyst Annie: Test scenario validation (4 hours)

**Dependencies:** Phase 2, 3, 4 complete

**Acceptance Criteria:**
- All unit tests pass
- All integration tests pass
- All test scenarios produce expected routing decisions
- Test coverage >85% for `agent_selector.py`
- No failing tests in CI pipeline

**Risk:** High - inadequate testing risks production routing failures

---

### Phase 6: Documentation & Migration (8-10 hours)

**Status:** Not Started

**Deliverables:**
- Migration guide for existing repositories
  - How to add hierarchy metadata to existing agents
  - How to run validation script
  - How to test routing decisions
  - Rollback procedure if issues arise
- Repository adopter guide
  - How to define custom specialists in `.doctrine-config`
  - How to inherit from framework agents
  - How to set routing priority
  - Examples (User Guide Ursula, Payment Processing Paul)
- Decision tree: "When to use which agent"
  - Flowchart for common task types
  - Agent selection rationale for each path
  - When to create new specialists vs use existing

**Assigned:**
- Scribe Sally: Migration guide, adopter guide (5 hours)
- Curator Claire: Decision tree, documentation updates (3 hours)

**Dependencies:** Phase 5 complete (all tests passing)

**Acceptance Criteria:**
- Migration guide includes step-by-step instructions
- Adopter guide includes at least 2 complete examples
- Decision tree covers common scenarios (Python, Java, docs, frontend)
- Documentation reviewed by Architect Alphonso

**Risk:** Low - documentation phase, no code changes

---

## Batch Sequencing

### Batch 1: Phase 1 Complete + Phase 2 Start (2 weeks)

**Theme:** Foundations - terminology and tactic specification

**Tasks:**
- Curator Claire: GLOSSARY.md updates (3h)
- Architect Alphonso: SELECT_APPROPRIATE_AGENT tactic document (4h)
- Architect Alphonso: Architecture design review (1h)

**Total Effort:** ~8 hours

**Acceptance Criteria:**
- GLOSSARY.md updated with all 7 terms
- Tactic document complete and reviewed
- Architecture design approved

**Blocks:** Batch 2 (implementation needs tactic spec)

---

### Batch 2: Phase 2 Complete (2 weeks)

**Theme:** Routing algorithm implementation and testing

**Tasks:**
- Python Pedro: Routing algorithm implementation (6h)
- Python Pedro: Unit tests for routing (2h)
- Architect Alphonso: Code review (1h)

**Total Effort:** ~9 hours

**Acceptance Criteria:**
- Routing algorithm passes all unit tests
- Structured logging for every routing decision
- Code reviewed and approved

**Blocks:** Batch 3 (profiles need working algorithm for testing)

**Depends on:** Batch 1 (tactic spec complete)

---

### Batch 3: Phase 3 Complete (2 weeks)

**Theme:** Agent profile schema and validation

**Tasks:**
- Curator Claire: Template update (2h)
- Backend Benny: Agent profile updates (4h)
- Python Pedro: Validation script (2h)

**Total Effort:** ~8 hours

**Acceptance Criteria:**
- Template updated with all new fields
- Python Pedro, Java Jenny, Backend Benny profiles updated
- Validation script detects all error conditions
- All profiles pass validation

**Blocks:** Batch 4 (Manager Mike needs updated profiles)

**Depends on:** Batch 2 (routing algorithm available for reference)

---

### Batch 4: Phase 4 Complete (2 weeks)

**Theme:** Manager Mike integration

**Tasks:**
- Python Pedro: Handoff protocol enhancement (5h)
- Backend Benny: Reassignment pass script (5h)
- Architect Alphonso: Manager Mike profile update (2h)

**Total Effort:** ~12 hours

**Acceptance Criteria:**
- Handoff override works correctly
- Reassignment pass generates report
- Manager Mike profile updated

**Blocks:** Batch 5 (testing needs full integration)

**Depends on:** Batch 3 (profiles updated)

---

### Batch 5: Phase 5 Complete (2-3 weeks)

**Theme:** Comprehensive testing and validation

**Tasks:**
- Python Pedro: Unit tests (6h)
- Backend Benny: Integration tests (6h)
- Analyst Annie: Test scenario validation (4h)

**Total Effort:** ~16 hours

**Acceptance Criteria:**
- All tests pass
- Test coverage >85%
- All scenarios validated

**Blocks:** Batch 6 (documentation needs working system)

**Depends on:** Batch 4 (Manager Mike integration complete)

---

### Batch 6: Phase 6 Complete (1 week)

**Theme:** Documentation and launch

**Tasks:**
- Scribe Sally: Migration guide, adopter guide (5h)
- Curator Claire: Decision tree, documentation updates (3h)

**Total Effort:** ~8 hours

**Acceptance Criteria:**
- All documentation complete
- Guides reviewed and approved
- Ready for production rollout

**Depends on:** Batch 5 (all tests passing)

---

## Dependency Graph

```
Batch 1 (Foundations)
  │
  ├─► Batch 2 (Routing Algorithm)
  │      │
  │      ├─► Batch 3 (Profiles)
  │      │      │
  │      │      └─► Batch 4 (Manager Mike Integration)
  │      │             │
  │      │             └─► Batch 5 (Testing)
  │      │                    │
  │      │                    └─► Batch 6 (Documentation)
  │      │
  │      └─► [Parallel] Terminology Alignment Phase 1
  │
  └─► [Parallel] Dashboard Enhancements M4 4.3
```

---

## Agent Assignment Rationale

| Agent | Why Selected | Phases | Total Hours |
|-------|-------------|--------|-------------|
| **Architect Alphonso** | Architecture design owner; validates technical decisions | 1, 2, 4 | ~8h |
| **Python Pedro** | Python specialist; owns routing algorithm and handoff logic | 2, 3, 4, 5 | ~21h |
| **Backend Benny** | Backend generalist; agent profile updates and reassignment script | 3, 4, 5 | ~15h |
| **Curator Claire** | Content curator; template and glossary updates | 1, 3, 6 | ~8h |
| **Scribe Sally** | Documentation specialist; migration and adopter guides | 6 | ~5h |
| **Analyst Annie** | Validation specialist; test scenario verification | 5 | ~4h |

**Total:** 61 hours (within 54-68h estimate)

---

## Capacity Planning

### Current Agent Utilization

| Agent | Current Tasks | Capacity | Utilization | Available for ASH |
|-------|--------------|----------|-------------|-------------------|
| Architect Alphonso | 4 | 5 | 80% | Limited (20%) |
| Python Pedro | 6 | 5 | 120% | ⚠️ Overloaded |
| Backend Benny | 6 | 8 | 75% | Moderate (25%) |
| Curator Claire | 1 | 5 | 20% | High (80%) |
| Scribe Sally | 2 | 5 | 40% | High (60%) |
| Analyst Annie | 0 | 5 | 0% | Full (100%) |

### Capacity Adjustments

**CRITICAL: Python Pedro Overloaded**
- Current: 6 tasks active (120% capacity)
- ASH Allocation: 21 hours across Phases 2-5
- **Mitigation:**
  1. Defer Batch 2 start until Dashboard M4 4.3 complete (week 3)
  2. Reassign Phase 3 profile updates from Pedro to Backend Benny (4h saved)
  3. Spread Phase 5 testing across Pedro + Benny + Annie (6h → 6h + 6h + 4h)
- **Result:** Pedro allocation reduced from 21h → 15h, spread over 6 weeks

**OPPORTUNITY: Curator Claire, Scribe Sally, Analyst Annie Underutilized**
- Leverage for Phases 1, 3, 5, 6
- High-quality documentation and validation work

---

## Risk Management

### High Risks

**RISK-001: Python Pedro Overload**
- **Impact:** Delays in Phase 2, 4, 5
- **Probability:** HIGH (already at 120%)
- **Mitigation:** See capacity adjustments above
- **Owner:** Planning Petra

**RISK-002: Routing Algorithm Complexity**
- **Impact:** Phase 2 takes 2x estimated effort (20h instead of 10h)
- **Probability:** MEDIUM
- **Mitigation:**
  - Strong technical design in tactic document
  - Architect review before implementation
  - Incremental implementation (scoring first, then workload, then complexity)
- **Owner:** Architect Alphonso

**RISK-003: Testing Coverage Inadequate**
- **Impact:** Production routing failures
- **Probability:** MEDIUM
- **Mitigation:**
  - Dedicated Phase 5 with 12-16h allocation
  - Comprehensive test scenarios in specification
  - Integration tests covering end-to-end workflows
- **Owner:** Python Pedro, Backend Benny

### Medium Risks

**RISK-004: Manager Mike Integration Breaks Existing Workflows**
- **Impact:** Current task assignment stops working
- **Probability:** LOW-MEDIUM
- **Mitigation:**
  - Extensive integration testing
  - Gradual rollout (opt-in flag initially)
  - Rollback plan documented
- **Owner:** Backend Benny

**RISK-005: Terminology Alignment Conflicts**
- **Impact:** Parallel GLOSSARY updates conflict
- **Probability:** LOW
- **Mitigation:**
  - Coordinate Phase 1 updates with Terminology spec
  - Single source of truth: `doctrine/GLOSSARY.md`
- **Owner:** Curator Claire

---

## Success Metrics

### Initiative-Level Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Routing accuracy** | >= 90% | Routing decision logs for tasks with specialist match |
| **Specialist utilization** | 60-90% | Task count per specialist / max_concurrent_tasks |
| **Handoff override rate** | >= 70% | Handoffs to parent with specialist context / total handoffs |
| **Workload balance** | No agent >100% | Max(active_tasks / capacity) across all agents |
| **Validation passing** | 100% | Hierarchy validation script exit code |
| **Test coverage** | >= 85% | Coverage report for `agent_selector.py` |

### Phase-Level Metrics

| Phase | Deliverable | Success Criteria |
|-------|------------|-----------------|
| **Phase 1** | GLOSSARY.md | All 7 terms added with examples |
| **Phase 2** | Routing algorithm | All unit tests pass, structured logging |
| **Phase 3** | Agent profiles | Validation script passes for all agents |
| **Phase 4** | Manager Mike | Handoff override works, reassignment report generated |
| **Phase 5** | Testing | >85% coverage, all scenarios pass |
| **Phase 6** | Documentation | Migration guide complete, adopter guide with examples |

---

## Timeline

### Recommended Sequencing (Sequential with Gates)

**Total Duration:** 8-10 weeks

**Week 1-2:** Batch 1 (Phase 1 complete, Phase 2 start)
**Week 3-4:** Batch 2 (Phase 2 complete)
**Week 5-6:** Batch 3 (Phase 3 complete) + Batch 4 start
**Week 7-8:** Batch 4 complete (Phase 4) + Batch 5 start
**Week 9-10:** Batch 5 complete (Phase 5) + Batch 6 (Phase 6)

**Key Milestones:**
- M1 (End Week 2): Tactic document approved
- M2 (End Week 4): Routing algorithm functional
- M3 (End Week 6): Agent profiles updated
- M4 (End Week 8): Manager Mike integration complete
- M5 (End Week 10): All tests passing, documentation published

### Aggressive Sequencing (Parallel Execution)

**Total Duration:** 6-7 weeks

**Parallelization:**
- Phase 1 + Phase 2 (overlapping documentation and tactic spec)
- Phase 3 + Phase 4 start (profile updates while handoff enhancement begins)
- Phase 5 unit tests + integration tests (parallel development)

**Risk:** Higher - parallel work may cause integration issues, rework

**Not Recommended:** Higher quality and lower risk with sequential approach

---

## Approval

**Planning Petra:** Plan submitted - 2026-02-12
**Architect Alphonso:** Pending (technical review)
**Manager Mike:** Pending (resource allocation review)
**Human-in-Charge:** Pending (strategic alignment review)

---

**Plan Status:** Ready for Approval
**Next Step:** Manager Mike creates task files after approval
**Version:** 1.0.0
