# Next Batch: M5 Batch 5.1 - Conceptual Alignment Foundation

**Previous Batch:** M4 Batch 4.3 - Dashboard Initiative Tracking (IN PROGRESS)  
**Current Status:** 🔄 **PLANNING** - Post-conceptual alignment stabilization  
**Strategic Context:** ADR-045/046 accepted, SPEC-TERM-001 drafted, domain boundaries defined

---

## 📋 Planning Update (2026-02-11)

**Context:** Major conceptual alignment work completed in current branch:
- ✅ ADR-045 (Doctrine Concept Domain Model) - Accepted
- ✅ ADR-046 (Domain Module Refactoring) - Accepted  
- ✅ DDR-001 (Primer Execution Matrix) - Established
- ✅ DDR-002 (Framework Guardian Role) - Established
- ✅ SPEC-TERM-001 (Terminology Alignment) - Draft, ready for review
- ✅ Dependency violations fixed (DDR-NNN format)
- ✅ Generators implemented (agent/rules/claudemd)

**Next Priority:** Implement architectural decisions before continuing dashboard work.

---

## 🎯 M4 Batch 4.3 Status (Dashboard - IN PROGRESS)

### Features Delivered

**1. ✅ Markdown Rendering (COMPLETE)** - 6 hours actual vs 9-11h estimated
- Client-side markdown parsing (marked.js + DOMPurify)
- GFM support (tables, task lists, strikethrough, autolinks)
- XSS prevention (DOMPurify + CSP headers)
- Selective rendering (description/context/notes → markdown)
- Performance: <50ms typical, <200ms P95 ✅
- Cross-browser tested (Chrome, Firefox, Safari) ✅
- **Files:** dashboard-markdown.js (11.4KB), dashboard.css (+300 lines)
- **Security:** 12/12 OWASP XSS payloads blocked ✅

**2. ✅ Priority Editing (COMPLETE)** - 5.83 hours actual vs 7-9h estimated
- Backend: PATCH /api/tasks/:id/priority endpoint
- YAML comment preservation (ruamel.yaml) ✅
- In-progress task protection (409 Conflict) ✅
- Frontend: Interactive priority dropdown
- In-progress indicator (pulsing dot) ✅
- Real-time WebSocket updates ✅
- Loading/success/error states ✅
- Performance: <200ms API call, <100ms WebSocket ✅
- **Backend Tests:** 55/55 passing (85% coverage) ✅
- **Frontend Tests:** 10/10 manual tests passing ✅
- **Files:** task_priority_updater.py (285 lines), dashboard.js (+130 lines), dashboard.css (+214 lines)

**3. 📋 Initiative Tracking (PENDING)** - 11-15 hours estimated
- Specification frontmatter parser
- Task linking via `specification:` field
- Progress rollup calculator
- Portfolio view UI
- **Status:** Next in queue

### Metrics Summary

**Delivered (2/3 features):**
- **Time:** 14 hours actual vs 18 hours estimated (22% under estimate) ✅
- **Tests:** 55 backend tests + 10 frontend manual tests (100% passing) ✅
- **Coverage:** 85% backend (exceeds 80% target) ✅
- **Performance:** All targets met (<50ms markdown, <200ms priority) ✅
- **Security:** All XSS tests passing ✅
- **Lines:** 629 production code, 38 automated tests

**Remaining (1/3 features):**
- Initiative Tracking: 11-15 hours

### Dashboard UX Improvements (Bonus)

**Additional improvements delivered:**
- ✅ Sidebar layout (metrics on left, content in center)
- ✅ Task sorting by latest change/creation date

---

## 🧹 Debt / Docs / Low-Priority Track (Background)

**Completed this iteration (2026-02-06):**
- `work/collaboration/done/curator/2025-11-25T1837-curator-validate-refactor.yaml` — Validate script reorganization and code quality improvements.
- `work/collaboration/done/writer-editor/2025-11-25T1838-writer-editor-update-docs.yaml` — Update documentation to reflect new script organization.
- `work/collaboration/done/curator/2025-11-24T0951-curator-tooling-best-practices-guide.yaml` — Tooling setup best practices guide confirmed.
- `work/collaboration/done/curator/2025-11-24T0952-curator-maintenance-checklist-templates.yaml` — Maintenance checklist templates confirmed.
- `work/collaboration/done/architect/2025-11-24T0950-architect-version-policy-documentation.yaml` — Tool versioning policy documented.

**Remaining (open):**
- `work/collaboration/assigned/architect/2025-11-24T1736-architect-framework-efficiency-assessment.yaml`

**Blockers:**
- Efficiency assessment blocked: missing `work/metrics/token-metrics-2025-11-24.json` and ADR-012 naming conflict.
- ✅ Recent Activity moved to top
- ✅ Charts moved to bottom
- ✅ Responsive design (desktop/tablet/mobile)
- **Time:** ~1 hour (not part of original estimate)

## 🎯 M4 Batch 4.3 Status (Dashboard - IN PROGRESS)

### Features Delivered (2/3)

**1. ✅ Markdown Rendering (COMPLETE)** - 6 hours actual
**2. ✅ Priority Editing (COMPLETE)** - 5.83 hours actual  
**3. 📋 Initiative Tracking (IN PROGRESS)** - 11-15 hours estimated
- Backend: Python Pedro
- Frontend: Frontend Freddy (waiting on backend API)

### M4 Batch 4.3 Completion Criteria
- ✅ Initiative tracking backend complete
- ✅ Initiative tracking frontend complete
- ✅ Portfolio view functional
- ✅ Progress rollup accurate

**Estimated Completion:** After python-pedro finishes backend (6-8h) + frontend completes UI (5-7h)

---

## 🚀 M5 Batch 5.1 - Conceptual Alignment Foundation (NEXT)

**Priority:** ⭐⭐⭐⭐⭐ CRITICAL  
**Estimated Duration:** 18-27 hours  
**Goal:** Implement domain model architecture before continuing feature work  
**Rationale:** ADR-045/046 accepted, establishes foundation for language-first architecture

**Strategic Value:**
- **CRITICAL PATH** for future domain work
- **BLOCKS** SPEC-TERM-001 implementation (needs domain boundaries)
- **ENABLES** dashboard doctrine display, vendor distribution, terminology automation
- **REDUCES** conceptual drift and maintenance burden

---

### Scope: Domain Refactoring & Foundation

#### Feature 1: Domain Module Refactoring (ADR-046) - CRITICAL

**Estimated Duration:** 8-12 hours  
**Priority:** ⭐⭐⭐⭐⭐ CRITICAL (blocks ADR-045)  
**Owner:** Backend Developer

**Goal:** Refactor `src/common/` → `src/domain/` with bounded context modules.

**Tasks (3-4 tasks):**

1. **Create Domain Directory Structure** (1-2h)
   - Create `src/domain/` with bounded context modules
   - Module structure: collaboration/, doctrine/, specifications/, common/
   - Preserve existing `src/common/` during migration

2. **Move Files to Bounded Contexts** (2-3h)
   - Move agent_loader.py → src/domain/doctrine/agent.py
   - Move task_schema.py → src/domain/collaboration/task.py  
   - Move types.py (split by context) → appropriate modules
   - Update internal imports within moved files

3. **Update Import Statements** (3-4h)
   - Scan entire codebase for `from src.common` imports
   - Update to `from src.domain.{context}` imports
   - Run linters to catch missed imports
   - Coordinate with team (high touch count)

4. **Test & Documentation** (2-3h)
   - Run full test suite, fix import errors
   - Update architecture diagrams (src/ structure)
   - Update import documentation
   - Remove old `src/common/` directory
   - Create migration guide for contributors

**Success Criteria:**
- ✅ All tests passing with new structure
- ✅ Zero `from src.common` imports remaining
- ✅ Bounded contexts clear in directory structure
- ✅ Documentation updated

**Agent Assignment:**
- Backend Dev: Implementation (8-12h)
- Planning Petra: Task creation and coordination

---

#### Feature 2: Doctrine Concept Domain Model (ADR-045) - CRITICAL

**Estimated Duration:** 10-15 hours  
**Priority:** ⭐⭐⭐⭐ HIGH (after ADR-046 complete)  
**Owner:** Backend Developer + Architect

**Goal:** Create Python dataclasses for doctrine artifacts enabling runtime introspection.

**Dependencies:**
- ⚠️ **BLOCKED BY:** ADR-046 must complete first (needs src/domain/ structure)

**Tasks (4-5 tasks):**

1. **Create Doctrine Domain Models** (4h)
   - File: `src/domain/doctrine/models.py`
   - Dataclasses: Directive, Approach, Tactic, AgentProfile, StyleGuide, Template
   - Enums: DirectiveStatus, EnforcementTier, AgentRole, TemplateCategory
   - Frozen dataclasses (immutability)
   - Type hints throughout

2. **Implement Directive/Approach/Tactic Parsers** (4h)
   - File: `src/domain/doctrine/parsers.py`
   - Parse markdown frontmatter (YAML)
   - Parse markdown content sections
   - Handle malformed files gracefully
   - Return domain model instances

3. **Implement Agent Profile Parser** (2h)
   - File: `src/domain/doctrine/agent_parser.py`
   - Parse `.agent.md` files
   - Extract capabilities, specialization, directives
   - Handle Directive table format

4. **Create Validators & Tests** (2-3h)
   - File: `src/domain/doctrine/validators.py`
   - Validate directive number uniqueness
   - Validate cross-references (e.g., approach → directives)
   - Unit tests for parsers (pytest)
   - Integration tests with real doctrine files

5. **Integrate with Dashboard & Exporters** (2-4h)
   - Update dashboard API to use domain model
   - Update exporters (OpenCode, Claude-Code) to use domain model
   - Update UI to display doctrine configuration
   - Smoke test end-to-end

**Success Criteria:**
- ✅ All doctrine artifacts parseable to domain objects
- ✅ Dashboard displays doctrine configuration
- ✅ Exporters use domain model
- ✅ 90%+ test coverage on parsers
- ✅ Type-safe access to doctrine metadata

**Agent Assignment:**
- Backend Dev: Implementation (8-12h)
- Architect: Review & validation (2-3h)
- Planning Petra: Task creation

---

### M5 Batch 5.1 Success Criteria

**Technical:**
- ✅ `src/domain/` structure established with bounded contexts
- ✅ All imports updated (`src.common` → `src.domain.{context}`)
- ✅ Doctrine domain model complete (6 dataclasses, 3 parsers)
- ✅ Dashboard integrated with domain model
- ✅ All tests passing (unit + integration)

**Strategic:**
- ✅ Foundation for SPEC-TERM-001 implementation
- ✅ Enables dashboard doctrine display
- ✅ Enables vendor distribution (structured domain model)
- ✅ Establishes bounded context pattern for future work

**Team:**
- ✅ Migration guide created for contributors
- ✅ Architecture diagrams updated
- ✅ Import conventions documented

---

### M5 Batch 5.1 Risks & Mitigations

**RISK-001: High Touch Count for Import Updates**
- **Impact:** ADR-046 task 3 touches ~50 files
- **Mitigation:** Run during low-activity period, coordinate in Slack/Discord
- **Contingency:** Automate with find/replace script, review carefully

**RISK-002: ADR-045 Blocked by ADR-046**
- **Impact:** Cannot parallelize, sequential dependency
- **Mitigation:** Complete ADR-046 first (8-12h), then start ADR-045
- **Contingency:** None (architectural dependency, must be sequential)

**RISK-003: Dashboard Integration Complexity**
- **Impact:** ADR-045 task 5 could take longer than estimated (2-4h → 6h)
- **Mitigation:** Limit scope to portfolio view integration only, defer other UI updates
- **Contingency:** Create follow-up task if scope grows

---

## 🔮 Future Batches (Post-M5.1)

### M5 Batch 5.2 - Terminology Alignment Phase 1 (Proposed)

**Priority:** ⭐⭐⭐⭐ HIGH  
**Estimated Duration:** 35 hours  
**Features:**
- FEAT-TERM-001-01: Directive Updates (4h)
- FEAT-TERM-001-02: Top 5 Generic Class Refactors (31h)

**Dependencies:**
- ✅ ADR-046 complete (bounded context structure available)
- ✅ Domain boundaries clear (helps guide refactoring decisions)

### M5 Batch 5.3 - Dashboard Continuation (Proposed)

**Priority:** ⭐⭐⭐ MEDIUM  
**Features:**
- Docsite Integration (9-12h)
- Repository Initialization (16-21h)
- Configuration Management (23-30h)

**Dependencies:**
- ✅ M4 Batch 4.3 complete (initiative tracking)
- ✅ M5 Batch 5.1 complete (domain model for repo setup)

---

## 📊 Overall Dashboard Progress

**M4 Initiative Total:** 98 hours estimated  
**Completed:** 14h (markdown, priority editing)  
**In Progress:** 11-15h (initiative tracking)  
**Remaining:** 73h (docsite, repo init, config management)  
**Progress:** 14% complete

**Note:** Dashboard work paused during M5.1 (conceptual alignment foundation) per strategic priority.

---

### Scope

**Backend (6-8 hours):**
- Specification frontmatter parser (YAML + markdown)
- Task linker (specification: field matching)
- Progress calculator (task status → feature → initiative rollup)
- GET /api/portfolio endpoint
- Caching strategy (<50ms cached, <500ms uncached)

**Frontend (5-7 hours):**
- Portfolio hierarchical view (accordion or tree)
- Progress bars per initiative/feature
- Drill-down navigation
- Real-time updates via WebSocket
- Orphan tasks section (tasks without specs)

**Agent Assignment:**
- Backend: python-pedro (6-8h)
- Frontend: frontend (5-7h)
- Can work in parallel after API contract agreed

### Success Criteria

- ✅ Initiative hierarchy displays correctly
- ✅ Progress bars reflect actual task completion
- ✅ Drill-down navigation works smoothly
- ✅ Portfolio loads fast (<500ms uncached)
- ✅ Real-time updates when tasks/specs change
- ✅ Responsive design

---

## 📊 Overall Progress: M4 Dashboard Enhancement Initiative

### Completed Features (3/6)
1. ✅ Markdown Rendering (6h) - Batch 4.3a
2. ✅ Priority Editing (5.83h) - Batch 4.3a
3. 📋 Initiative Tracking (11-15h) - Batch 4.3b (NEXT)

### Pending Features (3/6) - Batch 4.4
4. 📋 Docsite Integration (9-12h)
5. 📋 Repository Initialization (16-21h)
6. 📋 Configuration Management (23-30h)

**Total Progress:** 14h / 98h (14% complete)  
**Batch 1 Progress:** 14h / 30h (47% complete)

---

## Action Items

### For Agents

**Python Pedro:**
- Ready to start Initiative Tracking backend (6-8h)
- Task: work/collaboration/assigned/python-pedro/2026-02-06T1150-dashboard-initiative-tracking.yaml

**Frontend:**
- Ready to start Initiative Tracking frontend (5-7h) after backend API contract
- Task: work/collaboration/assigned/python-pedro/2026-02-06T1150-dashboard-initiative-tracking.yaml

### For Human

**Testing:**
- ✅ Test markdown rendering at http://localhost:8080
- ✅ Test priority editing dropdown
- ✅ Verify in-progress task protection
- ✅ Check XSS test page: http://localhost:8080/static/test-xss-payloads.html

**Decisions:**
- Approve continuing with Initiative Tracking?
- Or pivot to Batch 4.4 features (docsite/repo-init/config)?

---

## References

- **Work Logs:**
  - `work/logs/frontend/2026-02-06T1148-dashboard-markdown-rendering-worklog.md`
  - `work/logs/dashboard/2026-02-06-priority-editing-complete.md`
- **Completed Tasks:**
  - `work/collaboration/done/frontend/2026-02-06T1148-dashboard-markdown-rendering.yaml`
  - `work/collaboration/done/python-pedro/2026-02-06T1149-dashboard-priority-editing.yaml`
- **ADRs:**
  - `docs/architecture/adrs/ADR-035-dashboard-task-priority-editing.md` (Accepted)
  - `docs/architecture/adrs/ADR-036-dashboard-markdown-rendering.md` (Accepted)
  - `docs/architecture/adrs/ADR-037-dashboard-initiative-tracking.md` (Accepted)
- **Specifications:**
  - `specifications/llm-dashboard/task-priority-editing.md` (SPEC-DASH-001)
  - `specifications/llm-dashboard/markdown-rendering.md` (SPEC-DASH-002)
  - `specifications/llm-dashboard/initiative-tracking.md` (SPEC-DASH-003)

## 📋 Action Items

### For Human In Charge

**Decision Points:**
1. **Approve M5.1 Batch?** - Domain refactoring (ADR-046) + Domain model (ADR-045)
2. **Pause dashboard work?** - Complete initiative tracking first, or pivot to M5.1?
3. **Review SPEC-TERM-001?** - Terminology alignment spec ready for stakeholder review

**Recommended Decision:**
- ✅ Complete M4.3 (Initiative Tracking) - Already in progress, 11-15h remaining
- ✅ Execute M5.1 (Conceptual Alignment) - 18-27h, CRITICAL foundation work
- ✅ Execute M5.2 (Terminology Phase 1) - 35h, HIGH priority language-first work
- ⏸️ Defer M5.3 (Dashboard continuation) - Non-critical, can wait

### For Agents

**Backend Developer:**
- ⏳ Complete M4.3 initiative tracking backend (python-pedro, 6-8h)
- 📋 Execute M5.1 ADR-046 refactoring (backend-dev, 8-12h) - Tasks to be created
- 📋 Execute M5.1 ADR-045 domain model (backend-dev, 10-15h) - Tasks to be created

**Frontend:**
- ⏳ Complete M4.3 initiative tracking frontend (frontend-freddy, 5-7h) - After backend

**Architect Alphonso:**
- 📋 Review M5.1 tasks before execution (2-3h)
- 📋 Review SPEC-TERM-001 terminology alignment spec (1-2h)

**Planning Petra:**
- ✅ Create M5.1 task files (this session)
- ✅ Update DEPENDENCIES.md
- ✅ Update AGENT_TASKS.md

**Analyst Annie:**
- 📋 Create conceptual alignment plan (glossary work, 2-3h)
- 📋 Stakeholder review of SPEC-TERM-001

**Curator Claire:**
- 📋 Resolve src-consolidation plan conflict (30min)

---

## 🔗 References

**ADRs:**
- `docs/architecture/adrs/ADR-045-doctrine-concept-domain-model.md` (Accepted)
- `docs/architecture/adrs/ADR-046-domain-module-refactoring.md` (Accepted)
- `docs/architecture/adrs/ADR-037-dashboard-initiative-tracking.md` (Accepted)

**Specifications:**
- `specifications/initiatives/terminology-alignment-refactoring.md` (SPEC-TERM-001)
- `specifications/initiatives/conceptual-alignment/initiative.md`
- `specifications/initiatives/dashboard-enhancements/*.md`

**Doctrine Decisions:**
- `doctrine/decisions/DDR-001-primer-execution-matrix.md`
- `doctrine/decisions/DDR-002-framework-guardian-role.md`

**Planning:**
- `docs/planning/FEATURES_OVERVIEW.md` (Updated 2026-02-11)
- `docs/planning/DEPENDENCIES.md` (To be updated)
- `docs/planning/AGENT_TASKS.md` (To be updated)
- `work/planning/2026-02-11-alignment-assessment.md` (This session)

---

_Document maintained by: Planning Petra_  
_Last updated: 2026-02-11_  
_Next update: After M4.3 completion or M5.1 approval_
