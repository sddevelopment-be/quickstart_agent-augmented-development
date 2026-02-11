# Execution Authorization

**Authorized by:** Architect Alphonso  
**Date:** 2026-02-11  
**Authorization ID:** AUTH-M5.1-20260211  
**Review Reference:** `work/reports/architecture/2026-02-11-execution-approval-review.md`

---

## Authorization Scope

**APPROVED FOR IMMEDIATE EXECUTION:**
- **M5 Batch 5.1** - Conceptual Alignment Foundation (ADR-046/045 implementation)
- **M4 Batch 4.3** - Dashboard Initiative Tracking (continuation, already in progress)
- **SPEC-TERM-001 Phase 1** - Directive Updates only (4h, Code Reviewer)

**TOTAL AUTHORIZED EFFORT:** 29-40 hours across 3 parallel streams

---

## Approved Work Items

### IMMEDIATE (CRITICAL - Start Now)

#### 1. Backend Dev: ADR-046 Task 1 - Domain Structure (1-2h)

**Task ID:** `2026-02-11T0900-adr046-task1-domain-structure`  
**Priority:** ⭐⭐⭐⭐⭐ CRITICAL  
**Status:** READY TO START IMMEDIATELY  
**Agent:** Backend Dev (backend-dev)

**Authorization:**
✅ APPROVED - Execute immediately upon task file creation

**Deliverables:**
- `src/domain/` directory structure with bounded contexts
- `src/domain/README.md` explaining bounded contexts
- `__init__.py` files with docstrings

**Acceptance Criteria:**
- 7 MUST items (structure creation, preserve src/common/)
- 3 SHOULD items (docstrings, README, bounded context docs)
- 3 MUST NOT items (no file moves, no import updates, no deletions)

**Estimated Completion:** 1-2 hours  
**Blocks:** Task 2 (move files)

---

#### 2. Python Pedro: M4.3 Initiative Tracking Backend (6-8h)

**Task ID:** `2026-02-06T1150-dashboard-initiative-tracking`  
**Priority:** ⭐⭐⭐⭐ HIGH  
**Status:** READY TO START (already assigned)  
**Agent:** Python Pedro (python-pedro)

**Authorization:**
✅ APPROVED - Continue execution (already in progress)

**Deliverables:**
- Specification frontmatter parser (YAML + markdown)
- Task linker (specification: field matching)
- Progress rollup calculator
- GET /api/portfolio endpoint
- WebSocket portfolio updates

**Acceptance Criteria:**
- Initiative hierarchy displays correctly
- Progress bars reflect task completion
- Portfolio loads <500ms uncached
- Real-time updates via WebSocket

**Estimated Completion:** 6-8 hours  
**Blocks:** Frontend initiative tracking UI

**Parallel Safety:** ✅ LOW CONFLICT with M5.1 (different codebase areas)

---

### SHORT-TERM (Week 1-2)

#### 3. Backend Dev: ADR-046 Tasks 2-4 - File Moves & Import Updates (7-10h)

**Task IDs:**
- `2026-02-11T[TBD]-adr046-task2-move-files` (2-3h)
- `2026-02-11T[TBD]-adr046-task3-update-imports` (3-4h) ⚠️ HIGH RISK
- `2026-02-11T[TBD]-adr046-task4-test-docs` (2-3h)

**Priority:** ⭐⭐⭐⭐⭐ CRITICAL  
**Status:** WAITING ON TASK 1 COMPLETION  
**Agent:** Backend Dev

**Authorization:**
✅ APPROVED - Execute sequentially after Task 1

**Special Conditions for Task 3 (Import Updates):**
⚠️ **MANDATORY COORDINATION WINDOW**
1. Execute during low-activity period (coordinate with team)
2. Notify team via Slack/Discord before starting
3. Use automated refactoring tools (PyCharm "Refactor → Move" or `rope`)
4. Run test suite incrementally (catch import errors early)
5. Commit after validation (rollback point if conflicts)

**Deliverables (All Tasks):**
- Files moved to bounded contexts (Task 2)
- All imports updated (~50 files) (Task 3)
- Full test suite passing (Task 4)
- Architecture diagrams updated (Task 4)
- Migration guide created (Task 4)
- Old `src/common/` removed (Task 4)

**Estimated Completion:** 7-10 hours total  
**Blocks:** ADR-045 implementation (Tasks 5-9)

---

#### 4. Code Reviewer: SPEC-TERM-001 Directive Updates (4h)

**Task ID:** `2026-02-11T[TBD]-term001-feat01-directives`  
**Priority:** ⭐⭐⭐⭐ HIGH  
**Status:** READY TO START IMMEDIATELY  
**Agent:** Code Reviewer Cindy

**Authorization:**
✅ APPROVED - Execute in parallel with M5.1

**Deliverables:**
- Update `.github/agents/directives/` for workflow enforcement
- Document "Use collaboration scripts ONLY" requirement
- Document "Avoid generic naming in domain code" guideline
- Create PR comment templates for violations

**Acceptance Criteria:**
- Directives clearly document naming enforcement
- Workflow compliance requirements explicit
- PR templates ready for use

**Estimated Completion:** 4 hours  
**Parallel Safety:** ✅ INDEPENDENT (no code changes, directives only)

---

### MEDIUM-TERM (Week 2-3)

#### 5. Backend Dev: ADR-045 Tasks 1-5 - Domain Model Implementation (10-15h)

**Task IDs:**
- `2026-02-11T[TBD]-adr045-task1-models` (4h) - Create dataclasses
- `2026-02-11T[TBD]-adr045-task2-parsers` (4h) - Directive/Approach/Tactic parsers
- `2026-02-11T[TBD]-adr045-task3-agent-parser` (2h) - Agent profile parser
- `2026-02-11T[TBD]-adr045-task4-validators` (2-3h) - Validation + tests
- `2026-02-11T[TBD]-adr045-task5-integration` (2-4h) - Dashboard/exporter integration

**Priority:** ⭐⭐⭐⭐ HIGH  
**Status:** BLOCKED until ADR-046 complete  
**Agent:** Backend Dev

**Authorization:**
✅ APPROVED - Execute after ADR-046 Task 4 complete

**Special Conditions for Task 5 (Integration):**
⚠️ **SCOPE CONTROL REQUIRED**
- Limit integration to portfolio view ONLY
- Defer other dashboard UI updates to follow-on work
- If scope exceeds 4h, create follow-up task (do not expand in-flight)

**Deliverables:**
- `src/domain/doctrine/models.py` - 6 dataclasses, 4 enums
- `src/domain/doctrine/parsers.py` - Markdown + YAML parsing
- `src/domain/doctrine/agent_parser.py` - Agent profile parser
- `src/domain/doctrine/validators.py` - Cross-reference validation
- Dashboard API integration
- Exporter integration (OpenCode, Claude-Code)

**Acceptance Criteria:**
- All doctrine artifacts parseable to domain objects
- Dashboard displays doctrine configuration
- Exporters use domain model
- 90%+ test coverage on parsers
- Type-safe access to doctrine metadata

**Estimated Completion:** 10-15 hours total  
**Enables:** Dashboard doctrine display, vendor distribution, SPEC-TERM-001 Phase 2

---

#### 6. Frontend: M4.3 Initiative Tracking UI (5-7h)

**Task ID:** `2026-02-06T1150-dashboard-initiative-tracking` (frontend portion)  
**Priority:** ⭐⭐⭐ MEDIUM  
**Status:** WAITING ON BACKEND API  
**Agent:** Frontend Freddy

**Authorization:**
✅ APPROVED - Execute after Python Pedro backend complete

**Deliverables:**
- Portfolio hierarchical view (accordion or tree)
- Progress bars per initiative/feature
- Drill-down navigation
- Real-time WebSocket updates
- Orphan tasks section

**Acceptance Criteria:**
- Initiative hierarchy displays correctly
- Progress bars accurate
- Drill-down smooth
- Real-time updates work
- Responsive design

**Estimated Completion:** 5-7 hours  
**Completes:** M4 Batch 4.3 (Dashboard Initiative Tracking)

---

## Conditions

### 1. Sequential Execution (MANDATORY)

**M5.1 Dependency Chain:**
```
ADR-046 Task 1 (structure)
  ↓ BLOCKS
ADR-046 Task 2 (move files)
  ↓ BLOCKS
ADR-046 Task 3 (update imports)
  ↓ BLOCKS
ADR-046 Task 4 (test & docs)
  ↓ BLOCKS
ADR-045 Task 1-5 (domain model implementation)
```

**Enforcement:**
- Backend Dev MUST NOT start ADR-045 tasks until ADR-046 Task 4 complete
- Manager Mike to verify completion before authorizing next phase
- Task dependencies encoded in YAML frontmatter (`blocks:` field)

**Rationale:** Architectural dependency (domain model needs bounded context structure)

---

### 2. Coordination Window (REQUIRED)

**ADR-046 Task 3 - Import Updates:**

**Before Starting:**
1. Verify low team activity (check Git commits, Slack activity)
2. Post notification: "Starting M5.1 Task 3 (import updates) - ~50 files affected, expect branch activity"
3. Confirm automated tools available (PyCharm refactoring or `rope` installed)

**During Execution:**
1. Use automated refactoring (NOT manual find/replace)
2. Run `mypy` and `pylint` after each batch of updates
3. Run subset of tests incrementally (catch errors early)
4. Commit after validation (rollback point)

**After Completion:**
1. Run full test suite (`pytest tests/`)
2. Post completion notice: "M5.1 Task 3 complete, import updates merged"
3. Document any issues encountered (for retrospective)

**Fallback:** If conflicts arise, pause and resolve manually before continuing

---

### 3. Backend Dev Workload Decision (HUMAN CHOICE)

**Current Allocation:**
- M5.1 (approved): 18-27 hours
- SPEC-TERM-001 Phase 1 (approved directives): 4 hours (Code Reviewer)
- SPEC-TERM-001 Phase 1 (pending refactors): 31 hours (Backend Dev)

**Option A: Sequential (Lower Risk)**
```
1. Execute M5.1 (18-27h)
2. Then execute SPEC-TERM-001 refactors (31h)
Total: 49-58h serial
```

**Option B: Phased Parallel (Higher Velocity)**
```
Stream 1: M5.1 (Backend Dev, 18-27h)
Stream 2: SPEC-TERM-001 directives (Code Reviewer, 4h) - parallel OK
After M5.1: SPEC-TERM-001 refactors (Backend Dev, 31h)
Total: 49-58h with parallelism
```

**Architect Recommendation:** Option B (phased parallel)
- M5.1 and SPEC-TERM-001 directives can run independently
- Backend Dev focuses on M5.1 first (CRITICAL priority)
- SPEC-TERM-001 refactors start after M5.1 complete
- Reduces wall-clock time, maintains quality

**Human Decision Needed:**
- Approve Option A (sequential, safer) OR
- Approve Option B (phased parallel, faster) OR
- Defer SPEC-TERM-001 refactors entirely (focus M5.1 only)

**Default if no decision:** Option B (phased parallel per planning recommendation)

---

### 4. Scope Control (MONITORING REQUIRED)

**ADR-045 Task 5 (Dashboard Integration):**
- **Approved Scope:** Portfolio view integration ONLY
- **Out of Scope:** Other dashboard UI updates, additional exporters, caching optimization
- **If scope grows:** Create follow-up task, do not expand in-flight
- **Monitoring:** Architect Alphonso reviews scope at task completion

**SPEC-TERM-001 Phase 1:**
- **Approved Scope:** Directive updates (4h) + Top 5 generic class refactors (31h)
- **Out of Scope:** Phase 2 (Standardization, 46h), Phase 3 (Completion, 60h)
- **Enforcement:** Manager Mike blocks Phase 2 execution until Phase 1 reviewed
- **Rationale:** Prevent scope creep, validate Phase 1 outcomes before continuing

---

## Architectural Oversight

### Architect Alphonso Monitoring Points

**1. Post-ADR-046 Task 4 Review (Week 1)**
- **What:** Verify architecture diagrams updated correctly
- **Check:** `REPO_MAP.md`, `docs/architecture/` reflect new `src/domain/` structure
- **Action:** Approve ADR-045 execution OR request diagram corrections

**2. Post-ADR-045 Task 8 Review (Week 2)**
- **What:** Verify test coverage meets 90% target
- **Check:** `pytest --cov=src/domain/doctrine` output, coverage report
- **Action:** Approve Task 9 (integration) OR request additional tests

**3. Post-ADR-045 Task 9 Review (Week 3)**
- **What:** Verify integration scope limited to portfolio view
- **Check:** Dashboard API changes, exporter changes
- **Action:** Approve M5.1 completion OR escalate scope creep

**4. Post-M5.1 Completion Review (Week 3)**
- **What:** Validate domain model implementation quality
- **Check:** Code review, ADR accuracy, test coverage, documentation
- **Deliverable:** Post-implementation review report
- **Action:** Approve SPEC-TERM-001 Phase 2 OR defer pending fixes

---

## Parallel Work Streams

**AUTHORIZED PARALLEL EXECUTION:**

**Stream 1: M4.3 (Python Pedro + Frontend)**
- Backend: Initiative tracking (6-8h)
- Frontend: Initiative tracking UI (5-7h, after backend)
- **Total:** 11-15h
- **Conflict Risk:** LOW (different codebase areas)

**Stream 2: M5.1 (Backend Dev)**
- ADR-046 Tasks 1-4 (8-12h)
- ADR-045 Tasks 1-5 (10-15h)
- **Total:** 18-27h
- **Conflict Risk:** MEDIUM (import updates touch 50 files)

**Stream 3: SPEC-TERM-001 Directives (Code Reviewer)**
- Directive updates (4h)
- **Total:** 4h
- **Conflict Risk:** NONE (directives only, no code changes)

**Coordination:**
- Manager Mike monitors progress across streams
- Daily standup: Report blockers, conflicts, completion status
- Slack notifications: Before/after high-risk tasks (import updates)

**Conflict Resolution:**
- If merge conflicts arise: Pause, resolve manually, continue
- If blockers surface: Escalate to Human In Charge immediately
- If scope grows: Create follow-up tasks, do not expand in-flight

---

## Success Criteria

### M5.1 Batch Success Criteria

**Technical:**
- ✅ `src/domain/` structure established with bounded contexts
- ✅ All imports updated (`src.common` → `src.domain.{context}`)
- ✅ Doctrine domain model complete (6 dataclasses, 3 parsers)
- ✅ Dashboard integrated with domain model
- ✅ All tests passing (unit + integration)
- ✅ 90%+ test coverage on parsers

**Strategic:**
- ✅ Foundation for SPEC-TERM-001 Phase 2 (task context boundary)
- ✅ Enables dashboard doctrine display (SPEC-DASH-008)
- ✅ Enables vendor distribution (SPEC-DIST-001)
- ✅ Establishes bounded context pattern for future work

**Team:**
- ✅ Migration guide created for contributors
- ✅ Architecture diagrams updated (REPO_MAP, docs/architecture/)
- ✅ Import conventions documented
- ✅ No regressions (all existing features work)

### M4.3 Completion Criteria

**Backend:**
- ✅ GET /api/portfolio endpoint implemented
- ✅ Specification parsing works (frontmatter + markdown)
- ✅ Task linking accurate (specification: field matching)
- ✅ Progress rollup correct (task status → feature → initiative)
- ✅ WebSocket portfolio updates working

**Frontend:**
- ✅ Portfolio hierarchical view displays correctly
- ✅ Progress bars reflect actual completion
- ✅ Drill-down navigation smooth
- ✅ Real-time updates work via WebSocket
- ✅ Orphan tasks section functional

### SPEC-TERM-001 Phase 1 Criteria (Directives Only)

**Deliverables:**
- ✅ Directives updated for naming enforcement
- ✅ Workflow compliance documented
- ✅ PR comment templates created
- ✅ Team briefed on new guidelines

**Validation:**
- ✅ Directives clear and actionable
- ✅ Examples provided for common violations
- ✅ Templates ready for immediate use

---

## Risk Management

### Monitored Risks

**RISK-001: Import Update Conflicts**
- **Monitoring:** Backend Dev reports conflicts immediately
- **Escalation:** If conflicts >5 files, pause and coordinate resolution
- **Mitigation Active:** Low-activity window, automated tools, test validation

**RISK-002: Backend Dev Overload**
- **Monitoring:** Manager Mike tracks hours (18-27h M5.1 + 31h SPEC-TERM-001)
- **Escalation:** If overload signals appear (missed deadlines, quality issues), defer SPEC-TERM-001
- **Mitigation Active:** Phasing plan (M5.1 first, SPEC-TERM-001 second)

**RISK-003: Dashboard Integration Scope Creep**
- **Monitoring:** Architect Alphonso reviews Task 9 scope at completion
- **Escalation:** If scope exceeds portfolio view, create follow-up task
- **Mitigation Active:** Explicit scope limits, follow-up task process

**RISK-004: Test Coverage Gaps**
- **Monitoring:** Architect Alphonso reviews coverage report (Task 8)
- **Escalation:** If coverage <90%, request additional tests before Task 9
- **Mitigation Active:** 90% coverage target, comprehensive test plan

---

## Rollback Plan

### If Critical Issues Arise

**Scenario 1: Import Updates Break Production**
- **Action:** `git revert <commit>` for Task 3
- **Validation:** Re-run test suite, verify working state
- **Next Steps:** Fix imports manually, re-execute Task 3

**Scenario 2: Domain Model Design Flaw Discovered**
- **Action:** Pause ADR-045 execution
- **Escalation:** Architect Alphonso reviews design flaw
- **Next Steps:** Update ADR-045, adjust implementation, resume

**Scenario 3: Backend Dev Unavailable**
- **Action:** Pause M5.1 execution
- **Contingency:** Assign Backend Benny (if available) or defer
- **Next Steps:** Resume when Backend Dev returns

**Scenario 4: Unresolvable Merge Conflicts**
- **Action:** Pause conflicting stream (M4.3 or M5.1)
- **Resolution:** Coordinate manual resolution with affected agents
- **Next Steps:** Resume after conflicts resolved

---

## Reporting & Communication

### Daily Updates (While Work Active)

**Manager Mike Responsibilities:**
1. Collect status from active agents (Backend Dev, Python Pedro, Code Reviewer)
2. Update AGENT_STATUS.md with current task progress
3. Flag blockers immediately (Slack notification to Human In Charge)
4. Coordinate merge windows (especially for import updates)

**Agent Responsibilities:**
1. Report progress at end-of-day (hours spent, deliverables complete, blockers)
2. Update task YAML status field (`assigned` → `in-progress` → `done`)
3. Commit code incrementally (not one large commit at end)
4. Escalate issues within 2 hours of discovery (not end-of-day)

### Completion Reports

**Required Reports:**
1. **M5.1 Completion Report** (Backend Dev)
   - Deliverables summary
   - Test coverage report
   - Architecture diagram changes
   - Lessons learned
   - Recommendations for future work

2. **M4.3 Completion Report** (Python Pedro + Frontend)
   - Feature demonstration (portfolio view)
   - Performance metrics (load times, WebSocket latency)
   - Known issues / technical debt
   - Follow-up tasks

3. **SPEC-TERM-001 Phase 1 Report** (Code Reviewer)
   - Directives updated (list)
   - PR template usage (initial feedback)
   - Team adoption (any resistance?)
   - Phase 2 readiness assessment

---

## Sign-off

**Architect Alphonso**  
Authorization ID: AUTH-M5.1-20260211  
Date: 2026-02-11  
Scope: M5.1 Batch (9 tasks, 18-27h), M4.3 continuation, SPEC-TERM-001 directives (4h)

**Approval:**
✅ APPROVED FOR IMMEDIATE EXECUTION

**Conditions:**
1. ✅ Sequential execution (ADR-046 → ADR-045)
2. ✅ Coordination window (import updates)
3. ⏳ Human decision (Backend Dev workload, default Option B)
4. ✅ Scope control (dashboard integration, SPEC-TERM-001 Phase 1 only)

**Architectural Oversight:**
- Review after Task 4, Task 8, Task 9
- Post-M5.1 implementation review
- Pre-SPEC-TERM-001 Phase 2 approval

**Monitoring:**
- Manager Mike: Daily status, blocker escalation
- Architect Alphonso: Scope control, design validation
- Human In Charge: Strategic decisions, risk acceptance

---

**@manager-mike:** You are authorized to begin orchestration and task delegation immediately. Execute per approved work items above.

**@backend-dev:** You may start ADR-046 Task 1 immediately upon task file creation.

**@python-pedro:** You may continue M4.3 initiative tracking backend (already in progress).

**@code-reviewer-cindy:** You may start SPEC-TERM-001 directive updates immediately upon task file creation.

**@frontend-freddy:** Wait for Python Pedro backend API completion, then proceed with initiative tracking UI.

---

**Execution Status:** ✅ AUTHORIZED - Work may commence immediately per approved scope and conditions.
