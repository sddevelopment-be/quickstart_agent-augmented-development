# Agent Task Assignments

**Last Updated:** 2026-02-11  
**Planning Cycle:** Post-Conceptual Alignment Stabilization  
**Active Batch:** M5 Batch 5.1 - Conceptual Alignment Foundation (NEXT) / M4 Batch 4.3 (IN PROGRESS)

**Recent Updates (2026-02-11):**
- ✅ Added M5.1 batch - ADR-046/045 implementation (18-27h, CRITICAL)
- ✅ Added SPEC-TERM-001 Phase 1 tasks (35h, HIGH priority, can parallel)
- ✅ Added Analyst Annie assignments (spec review, conceptual alignment plan)
- ✅ Updated strategic priorities per conceptual alignment branch work

**Strategic Context:**
- **CRITICAL:** M5.1 (Domain Refactoring + Domain Model) establishes foundation for language-first architecture
- **HIGH:** SPEC-TERM-001 Phase 1 (Terminology Alignment) can execute in parallel with M5.1
- **IN PROGRESS:** M4.3 (Dashboard Initiative Tracking) continues

---

## 🆕 SPEC-REFACTOR-001: Refactoring Tactics Foundation (NEW)

**Priority:** HIGH  
**Total Effort:** 18-26 hours  
**Goal:** Create a research-backed doctrine tactic baseline for preferred refactoring techniques and pattern transitions.

### Researcher Ralph

1. **2026-02-12T0910-researcher-refactoring-techniques-matrix** - Build source-backed technique matrix (6h)
   - Capture applicability, failure modes, and selection criteria
   - Store outputs in `work/research/`
   - **Dependencies:** None

### Curator Claire

2. **2026-02-12T0911-curator-refactoring-tactics-authoring** - Author initial tactic set (6h)
   - Create tactic files in `doctrine/tactics/` from selected high-fit techniques
   - Use `doctrine/templates/tactic.md`
   - **Dependencies:** 0910

3. **2026-02-12T0912-curator-refactoring-pattern-references** - Add pattern-oriented references (4h)
   - Add `doctrine/docs/references/` files to support tactic strategy context
   - **Dependencies:** 0910

4. **2026-02-12T0913-curator-refactoring-directive-integration** - Integrate directive/index links (4h)
   - Link refactoring directives to tactics
   - Update `doctrine/tactics/README.md` for discoverability
   - **Dependencies:** 0911, 0912

### Code Reviewer Cindy

5. **2026-02-12T0914-code-reviewer-refactoring-tactics-validation** - Validate consistency and policy fit (2h)
   - Check references, stack precedence compliance, and actionable execution quality
   - **Dependencies:** 0913

---

## 🆕 M5.1 Batch: Conceptual Alignment Foundation (NEXT - CRITICAL)

**Strategic Priority:** ⭐⭐⭐⭐⭐ CRITICAL  
**Total Effort:** 18-27 hours  
**Goal:** Implement ADR-046/045 domain model architecture  
**Status:** Tasks to be created this session (Planning Petra)

### Backend Benny - Domain Refactoring & Implementation
**Priority:** ⭐⭐⭐⭐⭐ CRITICAL PATH (M5.1)

#### M5.1 Tasks (To Be Created)

**ADR-046: Domain Module Refactoring** (8-12 hours, MUST GO FIRST)

1. **2026-02-11T[TBD]-adr046-task1-domain-structure** - Create Domain Directory (1-2h)
   - Create `src/domain/` with bounded context modules
   - Subdirectories: collaboration/, doctrine/, specifications/, common/
   - **Owner:** Backend Dev
   - **Deliverables:** Directory structure, __init__.py files
   - **Status:** TO BE CREATED

2. **2026-02-11T[TBD]-adr046-task2-move-files** - Move Files to Bounded Contexts (2-3h)
   - Move agent_loader.py → src/domain/doctrine/agent.py
   - Move task_schema.py → src/domain/collaboration/task.py
   - Move types.py (split by context)
   - **Owner:** Backend Dev
   - **Dependencies:** Task 1 complete
   - **Status:** TO BE CREATED

3. **2026-02-11T[TBD]-adr046-task3-update-imports** - Update Import Statements (3-4h)
   - Scan codebase for `from src.common` imports (~50 files)
   - Update to `from src.domain.{context}` imports
   - Run linters, coordinate with team
   - **Owner:** Backend Dev
   - **Dependencies:** Task 2 complete
   - **Risk:** HIGH (merge conflicts possible)
   - **Status:** TO BE CREATED

4. **2026-02-11T[TBD]-adr046-task4-test-docs** - Test & Documentation (2-3h)
   - Run full test suite, fix import errors
   - Update architecture diagrams
   - Create migration guide
   - Remove old `src/common/` directory
   - **Owner:** Backend Dev
   - **Dependencies:** Task 3 complete
   - **Status:** TO BE CREATED

**ADR-045: Doctrine Concept Domain Model** (10-15 hours, AFTER ADR-046)

5. **2026-02-11T[TBD]-adr045-task1-models** - Create Doctrine Domain Models (4h)
   - File: `src/domain/doctrine/models.py`
   - Dataclasses: Directive, Approach, Tactic, AgentProfile, StyleGuide, Template
   - Enums: DirectiveStatus, EnforcementTier, AgentRole
   - **Owner:** Backend Dev
   - **Dependencies:** ADR-046 complete (needs src/domain/ structure)
   - **Status:** TO BE CREATED

6. **2026-02-11T[TBD]-adr045-task2-parsers** - Implement Parsers (4h)
   - File: `src/domain/doctrine/parsers.py`
   - Parse directive/approach/tactic markdown + frontmatter
   - Handle malformed files gracefully
   - **Owner:** Backend Dev
   - **Dependencies:** Task 5 complete
   - **Status:** TO BE CREATED

7. **2026-02-11T[TBD]-adr045-task3-agent-parser** - Agent Profile Parser (2h)
   - File: `src/domain/doctrine/agent_parser.py`
   - Parse `.agent.md` files
   - Extract capabilities, directives, specialization
   - **Owner:** Backend Dev
   - **Dependencies:** Task 5 complete
   - **Status:** TO BE CREATED

8. **2026-02-11T[TBD]-adr045-task4-validators** - Validators & Tests (2-3h)
   - File: `src/domain/doctrine/validators.py`
   - Validate cross-references, uniqueness
   - Unit tests for parsers (pytest)
   - Integration tests with real doctrine files
   - **Owner:** Backend Dev
   - **Dependencies:** Tasks 6, 7 complete
   - **Status:** TO BE CREATED

9. **2026-02-11T[TBD]-adr045-task5-integration** - Dashboard & Exporter Integration (2-4h)
   - Update dashboard API to use domain model
   - Update exporters (OpenCode, Claude-Code)
   - Smoke test end-to-end
   - **Owner:** Backend Dev
   - **Dependencies:** Task 8 complete
   - **Status:** TO BE CREATED

**M5.1 Total:** 9 tasks, 18-27 hours, CRITICAL PATH

---

## 🆕 SPEC-TERM-001 Phase 1: Terminology Alignment (HIGH - Can Parallel)

**Priority:** ⭐⭐⭐⭐ HIGH  
**Total Effort:** 35 hours (Phase 1 only)  
**Goal:** Directive updates + Top 5 generic class refactors  
**Status:** Tasks to be created this session (Planning Petra)

### Code Reviewer Cindy - Directive Enforcement
**Priority:** ⭐⭐⭐⭐ HIGH (SPEC-TERM-001 Phase 1)

#### SPEC-TERM-001 Tasks (To Be Created)

1. **2026-02-11T[TBD]-term001-feat01-directives** - Update Directives for Naming Enforcement (4h)
   - Update `.github/agents/directives/` for workflow and naming enforcement
   - Document "Use collaboration scripts ONLY" requirement
   - Document "Avoid generic naming in domain code" guideline
   - Create PR comment templates for violations
   - **Owner:** Code Reviewer Cindy
   - **Dependencies:** None (can start immediately)
   - **Status:** TO BE CREATED

### Backend Benny - Generic Class Refactoring
**Priority:** ⭐⭐⭐⭐ HIGH (SPEC-TERM-001 Phase 1)

#### SPEC-TERM-001 Tasks (To Be Created)

2. **2026-02-11T[TBD]-term001-feat02a-model-router** - Refactor ModelConfigurationManager (8h)
   - Rename `ModelConfigurationManager` → `ModelRouter`
   - Update all references, imports, tests
   - Backward compatibility shim if needed
   - **Owner:** Backend Dev
   - **Dependencies:** ADR-046 helpful but not required
   - **Status:** TO BE CREATED

3. **2026-02-11T[TBD]-term001-feat02b-template-renderer** - Refactor TemplateManager (6h)
   - Rename `TemplateManager` → `TemplateRenderer`
   - Update all references, imports, tests
   - **Owner:** Backend Dev
   - **Dependencies:** Task 2 complete (prevent conflicts)
   - **Status:** TO BE CREATED

4. **2026-02-11T[TBD]-term001-feat02c-task-service** - Refactor TaskAssignmentHandler (8h)
   - Rename `TaskAssignmentHandler` → `TaskAssignmentService`
   - Update all references, imports, tests
   - **Owner:** Backend Dev
   - **Dependencies:** Task 3 complete
   - **Status:** TO BE CREATED

5. **2026-02-11T[TBD]-term001-feat02d-config-loader** - Refactor OrchestrationConfigLoader (5h)
   - Rename to domain-specific name (TBD during implementation)
   - Update all references, imports, tests
   - **Owner:** Backend Dev
   - **Dependencies:** Task 4 complete
   - **Status:** TO BE CREATED

6. **2026-02-11T[TBD]-term001-feat02e-agent-registry** - Refactor AgentSpecRegistry (4h)
   - Rename to domain-specific name (TBD during implementation)
   - Update all references, imports, tests
   - **Owner:** Backend Dev
   - **Dependencies:** Task 5 complete
   - **Status:** TO BE CREATED

**SPEC-TERM-001 Phase 1 Total:** 6 tasks, 35 hours, can parallel with M5.1

---

## 🆕 Analyst Annie - Specification & Planning

**Priority:** ⭐⭐⭐ MEDIUM (Review & Planning)

#### Active Tasks (To Be Created)

1. **2026-02-11T[TBD]-annie-spec-term-review** - Review SPEC-TERM-001 with Stakeholders (2h)
   - Coordinate review with Architect Alphonso, Backend Benny, Code Reviewer Cindy
   - Address feedback, finalize acceptance criteria
   - Mark spec as "Approved" after stakeholder sign-off
   - **Owner:** Analyst Annie
   - **Dependencies:** None (spec draft complete)
   - **Status:** TO BE CREATED

2. **2026-02-11T[TBD]-annie-conceptual-alignment-plan** - Create Conceptual Alignment Plan (2-3h)
   - File: `docs/planning/conceptual-alignment-plan.md`
   - Phase tasks for glossary expansion (40+ DDD terms)
   - Contextive IDE integration plan
   - Concept mapping and visualization plan
   - **Owner:** Analyst Annie
   - **Dependencies:** None (can start immediately)
   - **Status:** TO BE CREATED

**Analyst Annie Total:** 2 tasks, 4-5 hours

---

## Current Focus: Dashboard Initiative (M4 Batch 4.3 - IN PROGRESS)

### Python Pedro - Backend Development
**Priority:** ⭐⭐⭐⭐ CRITICAL (Dashboard Initiative)

#### Active Tasks
1. **2026-02-06T1150** - Initiative Tracking Backend (11-15h) - `READY TO START`
   - Specification parser (frontmatter + markdown)
   - Task linker (specification: field matching)
   - Progress rollup calculator
   - GET /api/portfolio endpoint
   - **Dependencies:** Markdown rendering ✅, Priority editing ✅
   - **Deliverables:** `src/llm_service/portfolio.py`, tests, API endpoint

2. **2026-02-06T1221** - Repository Initialization (16-21h) - `BACKLOG`
   - Dashboard-driven repo setup wizard
   - Bootstrap Bill integration
   - **Dependencies:** Initiative tracking complete

3. **2026-02-06T1222** - Configuration Management (23-30h) - `BACKLOG`
   - Web-based config editor
   - YAML schema validation
   - **Priority:** HIGH but deferred to M4 Batch 4.4

#### On Hold (Needs Path Updates)
4. **2026-02-05T1000** - GenericYAMLAdapter - `HIGH`
   - Blocked pending LLM service architecture review
   
5. **2025-12-01T0510** - Framework Config Loader - `HIGH`
   - Update artifact path: `src/framework/config/loader.py`
   
6. **2025-12-01T0511** - Agent Profile Parser - `MEDIUM`
   - Update to reference `doctrine/agents/` paths

**Total Active Effort:** 11-15h (Initiative Tracking only)  
**Total Backlog Effort:** 90-120h

---

### Frontend Freddy - UI Development
**Priority:** ⭐⭐⭐⭐ HIGH (Dashboard Initiative)

#### Active Tasks
1. **2026-02-06T1200** - Markdown Rendering Test - `IN PROGRESS`
   - Verification of GFM support
   - XSS payload testing
   - Cross-browser validation

2. **2026-02-06T1150** - Initiative Tracking Frontend (5-7h) - `WAITING ON BACKEND`
   - Portfolio hierarchical view (accordion/tree)
   - Progress bars per initiative/feature
   - Real-time WebSocket updates
   - Drill-down navigation
   - **Dependencies:** Python Pedro completes backend API

3. **2026-02-06T1220** - Docsite Integration (9-12h) - `BACKLOG`
   - Embed docs-site content in dashboard
   - Navigation integration
   - **Priority:** MEDIUM, deferred to M4 Batch 4.4

**Total Active Effort:** 5-7h (after backend complete)  
**Total Backlog Effort:** 9-12h

---

### Architect Alphonso - System Design
**Priority:** ⭐⭐⭐ HIGH (Strategic Architecture)

#### High Priority
1. **2026-01-30T1120** - Prompt Optimization Framework (6-8h) - `READY`
   - Design ADR for 12 identified suboptimal patterns
   - Evaluate template standardization vs. metadata-driven approaches
   - Define implementation roadmap
   - **Strategic Value:** 30-40% efficiency gain, 30% token savings
   - **Deliverables:** ADR-XXX (Proposed status)

2. **2026-01-29T0730-mfd-task-1.3** - Schema Conventions (3h) - `CRITICAL PATH`
   - Define JSON Schema standards for agent input/output
   - Document extraction heuristics
   - Create migration checklist
   - **Blocks:** MFD tasks 1.4, 2.1, 2.4
   - **Dependencies:** Parser available (mfd-task-1.2)

#### Medium Priority
3. **2025-11-30T1202** - Model Client Interface - `HIGH`
   - Artifact: `src/framework/orchestration/model_client.py` (path updated)
   - Router-agnostic orchestration interface
   - **Dependencies:** None, can proceed

4. **2026-01-31T0638** - Primer-aligned directive validation - `ASSIGNED`
   - Validate ATDD/TDD directive integration
   - Cross-reference with alias.md

#### Low Priority / On Hold
5. **2025-11-24T1736** - Framework Efficiency Assessment - `BLOCKED`
   - Blocker: Missing metrics artifact
   - Blocker: ADR-012 naming conflict
   - **Recommendation:** Archive or resolve blockers

**Total High-Priority Effort:** 9-11h  
**Total Medium-Priority Effort:** 4-6h

---

### Backend Benny - Implementation
**Priority:** ⭐⭐⭐ HIGH (MFD Critical Path)

#### Critical Path (Needs Path Updates)
1. **2026-01-29T0730-mfd-task-1.2** - Implement Parser (6h) - `TODO`
   - **PATH UPDATE:** `tools/exporters/parser.js` (was `ops/exporters/parser.js`)
   - Parse .agent.md files to IR
   - YAML frontmatter + markdown sections
   - **Dependencies:** IR structure defined (task 1.1)
   - **Blocks:** All MFD tasks

2. **2026-01-29T0730-mfd-task-1.4** - Create 5 Schemas (4h) - `TODO`
   - Apply schema conventions to 5 representative agents
   - **Dependencies:** Schema conventions (task 1.3)
   - **Blocks:** Task 2.4 (remaining 12 schemas)

3. **2026-01-29T0730-mfd-task-2.1** - OpenCode Generator (6h) - `TODO`
   - Generate OpenCode agent definitions from IR
   - **Dependencies:** Parser complete

#### High Priority (ADR-023 Implementation)
4. **2026-01-30T1642** - Prompt Validator (Phase 2) - `HIGH`
   - Schema-based prompt validation
   - **PATH UPDATE:** `tools/validators/prompt_validator.py`

5. **2026-01-30T1643** - Context Loader (Phase 3) - `HIGH`
   - Progressive context loading with token counting
   - **PATH UPDATE:** `src/framework/context/loader.py`

#### LLM Service Tasks (On Hold)
6. **2026-02-04T1705** - Claude-Code Adapter - `HIGH`
   - Path correct: `src/llm_service/adapters/claude_code.py`
   - **On Hold:** Pending architecture review

7. **2026-02-04T1709** - Policy Engine - `HIGH`
   - Budget enforcement and cost optimization
   - **On Hold:** Pending architecture review

8. **2026-02-05T1001** - YAML ENV Variables - `MEDIUM`
9. **2026-02-05T1002** - Routing Integration - `HIGH`

#### Low Priority
10. **2026-02-05T1400** - Rich Terminal UI - `LOW`, `PENDING`
    - Deferred to M5+

**Total Critical Effort:** 16h (MFD)  
**Total High-Priority Effort:** 12-16h (ADR-023)  
**Total LLM Service (On Hold):** 8-12h

---

### Build Automation / DevOps Danny - CI/CD
**Priority:** ⭐⭐⭐ HIGH (Infrastructure)

#### Immediate
1. **2025-11-28T0427** - Work Items Cleanup Script - `MEDIUM`
   - Automate archival of completed tasks
   - Maintain work/ directory hygiene

2. **2026-01-30T1644** - ADR-023 CI Workflow - `HIGH`
   - GitHub Actions for prompt validation
   - **Dependencies:** Prompt validator (backend task 2026-01-30T1642)

#### High Priority (Path Updates Needed)
3. **2025-11-30T1206** - CI Router Schema Validation - `HIGH`
   - **PATH UPDATE:** Use `tools/validators/` scripts
   - Wire into GitHub Actions

4. **2025-12-01T0513** - Framework CI Tests - `HIGH`
   - **PATH UPDATE:** `tests/framework/`, `tools/validators/`
   - Run full test suite in CI

#### Medium Priority
5. **2025-12-01T0512** - Router Metrics Dashboard - `MEDIUM`
   - Integrate with ADR-009 dashboard

6. **2025-11-30T1204** - Ollama Worker Pipeline - `NORMAL`
   - Local worker node operationalization

#### Completed (Needs Archival)
7. **2026-01-29T0935** - GitHub Workflow Review - `COMPLETE` ✅
   - **Action:** Move to done/ directory

#### Low Priority / Deferred
8. **2025-11-24T0953** - Parallel Installation - `NORMAL`
   - **Needs Spec:** Analyst Annie to define benchmarks

9. **2025-11-24T0954** - Telemetry Collection - `LOW`
   - **Recommendation:** Archive to backlog

10. **2025-12-04T0529** - Validation Tooling Prototype - `NORMAL`

**Total Immediate Effort:** 4-6h  
**Total High-Priority Effort:** 8-12h  
**Total Medium-Priority Effort:** 6-10h

---

### Curator Claire - Content Organization
**Priority:** ⭐⭐ MEDIUM (Documentation)

#### Active
1. **2026-01-31T0638** - ATDD/TDD Directive Integration - `ASSIGNED`
   - Integrate testing directives into alias + profile updates
   - Cross-reference with architect validation task

2. **2025-12-04T0528** - Integrate Feasibility Artifacts - `HIGH`
   - Docsite metadata separation artifacts
   - Repository structure integration

**Total Effort:** 4-6h

---

### Writer-Editor Willow - Documentation
**Priority:** ⭐⭐ MEDIUM (Documentation)

#### Active
1. **2025-12-04T0527** - Polish Feasibility Documents - `HIGH`
   - Review docsite metadata separation docs
   - Ensure clarity and completeness

#### Completed (Needs Archival)
2. **2026-02-05T1400** - Spec-Driven Primer - `COMPLETED` ✅
   - **Action:** Move to done/ directory

#### POC3 Follow-ups (Low Priority)
3. **2025-11-27T1956** - POC3 Followup Synthesis - `ASSIGNED`
4. **2026-01-31T0638** - POC3 Aggregate Metrics - `ASSIGNED`

**Recommendation:** Archive POC3 tasks or downgrade priority

**Total Active Effort:** 3-5h

---

### Scribe Sam - Documentation Creation
**Priority:** ⭐⭐ MEDIUM (Specification)

#### Active
1. **2026-02-04T1714** - Persona Workflows (3 examples) - `MEDIUM`
   - Create workflow examples for user personas
   - Reference `docs/audience/` personas

2. **2025-11-30T1203** - Model Selection Template - `HIGH`
   - **Needs Spec:** Analyst Annie to define acceptance criteria
   - Extend task descriptor template with model hints
   - **Blocked:** Waiting on specification

**Total Active Effort:** 4-6h (after unblocked)

---

### Diagrammer Dan - Visual Documentation
**Priority:** ⭐ LOW (Enhancement)

#### Active
1. **2025-11-30T1205** - Multi-tier Runtime Diagram - `NORMAL`
   - PlantUML diagrams-as-code
   - Multi-tier runtime visualization

2. **2025-12-04T0526** - Docsite Architecture Diagrams - `HIGH`
   - Architecture diagrams for docsite metadata separation

#### POC3 Follow-ups
3. **2026-01-31T0638** - POC3 Diagram Updates - `LOW`

**Recommendation:** Prioritize docsite diagrams, defer POC3

**Total Effort:** 4-8h

---

### Synthesizer Sally - Analysis & Reports
**Priority:** ⭐ LOW (Enhancement)

#### POC3 Follow-ups
1. **2026-01-31T0638** - POC3 Metrics Synthesis - `LOW`

**Recommendation:** Archive POC3 work

---

### Manager Mike - Coordination
**Priority:** ⭐⭐ MEDIUM (Governance)

#### Active
1. **2025-11-24T0955** - Tooling Enhancements Coordination - `HIGH`
   - Review and coordinate tooling tasks from assessment

2. **2025-12-04T0530** - Orchestrate Decision Review - `HIGH`
   - Stakeholder review for ADR-022

**Total Effort:** 3-5h

---

## Task Dependencies Summary

**See:** `docs/planning/DEPENDENCIES.md` for detailed dependency graph

**Critical Path:**
1. Parser (backend-dev) → Schema Conventions (architect) → 5 Schemas (backend-dev) → OpenCode Generator
2. Initiative Tracking Backend (python-pedro) → Initiative Tracking Frontend (frontend)

**Parallel Work Streams:**
- Dashboard Initiative (python-pedro + frontend)
- Prompt Optimization (architect)
- ADR-023 Implementation (backend-dev)
- CI/CD Hardening (build-automation)

---

## Agent Workload Distribution (Updated 2026-02-11)

| Agent | M5.1 Tasks | SPEC-TERM-001 | M4.3 (Current) | Backlog | Total (Immediate) | Priority Level |
|-------|------------|---------------|----------------|---------|-------------------|----------------|
| backend-dev | 9 tasks (18-27h) | 5 tasks (31h) | - | 6 tasks (16h+) | 49-58h | ⭐⭐⭐⭐⭐ CRITICAL |
| code-reviewer-cindy | - | 1 task (4h) | - | - | 4h | ⭐⭐⭐⭐ HIGH |
| analyst-annie | - | 1 task (2h) | - | 1 task (2-3h) | 4-5h | ⭐⭐⭐ MEDIUM |
| python-pedro | - | - | 1 task (6-8h) | 6 tasks (90-120h) | 6-8h | ⭐⭐⭐⭐ HIGH |
| frontend | - | - | 1 task (5-7h) | 2 tasks (9-12h) | 5-7h | ⭐⭐⭐ MEDIUM |
| architect | - | - | - | 5 tasks (9-11h) | Review only | ⭐⭐⭐ HIGH |
| curator | - | - | - | 2 tasks (4-6h) | 30min | ⭐⭐ MEDIUM |
| build-automation | - | - | - | 10 tasks (12-18h) | - | ⭐⭐⭐ HIGH |

**Key Observations:**
- **Backend Dev: CRITICAL OVERLOAD** - 49-58h immediate work (M5.1 + SPEC-TERM-001 Phase 1)
- **Python Pedro: M4.3 Focus** - 6-8h immediate (initiative tracking), 90-120h backlog
- **Analyst Annie: NEW ASSIGNMENTS** - 4-5h immediate (spec review + planning)
- **Code Reviewer: NEW ASSIGNMENT** - 4h immediate (directive updates)
- **Architect: REVIEW ROLE** - Light immediate load, review/validation focus

**Recommendation:**
1. **Backend Dev:** Prioritize M5.1 (18-27h) over SPEC-TERM-001 (31h can parallel later)
2. **Python Pedro:** Continue M4.3, M5.1 doesn't block dashboard work
3. **Code Reviewer:** Start SPEC-TERM-001 directive updates immediately (4h, can parallel)

---

## ⭐ Recommendations for Human In Charge (Updated 2026-02-11)

### Immediate Decisions Required

1. **Approve M5.1 Batch Execution?**
   - **What:** ADR-046 (Domain Refactoring, 8-12h) + ADR-045 (Domain Model, 10-15h)
   - **Why:** CRITICAL foundation for language-first architecture, blocks future domain work
   - **Impact:** 18-27 hours backend-dev work, high touch count (~50 files), merge conflict risk
   - **Recommendation:** ✅ APPROVE - Execute after M4.3 completion or parallel if low-conflict

2. **Approve SPEC-TERM-001 Phase 1 Execution?**
   - **What:** Directive updates (4h) + Top 5 generic class refactors (31h)
   - **Why:** HIGH ROI (65% → 75% linguistic health score), can parallel with M5.1
   - **Impact:** 35 hours (code-reviewer-cindy 4h + backend-dev 31h)
   - **Recommendation:** ✅ APPROVE Phase 1 only (defer Phase 2/3 until M5.1 complete)

3. **Review SPEC-TERM-001 Specification?**
   - **Status:** Draft, ready for stakeholder review
   - **Reviewers Needed:** Architect Alphonso, Backend Benny, Code Reviewer Cindy
   - **Effort:** 1-2h per reviewer
   - **Recommendation:** Assign Analyst Annie to coordinate review (task created)

### This Week (Immediate Actions)

1. **Backend Dev:**
   - ✅ **Execute:** ADR-046 refactoring (8-12h) - CRITICAL, must go first
   - ⏳ **Then:** ADR-045 domain model (10-15h) - After ADR-046 complete
   - ⏸️ **Defer:** SPEC-TERM-001 refactors (31h) - Until M5.1 complete or parallel if capacity

2. **Code Reviewer Cindy:**
   - ✅ **Execute:** SPEC-TERM-001 directive updates (4h) - Can start immediately, parallels M5.1

3. **Python Pedro:**
   - ✅ **Continue:** M4.3 initiative tracking backend (6-8h) - In progress, don't block

4. **Analyst Annie:**
   - ✅ **Execute:** SPEC-TERM-001 stakeholder review coordination (2h)
   - ✅ **Execute:** Conceptual alignment plan creation (2-3h)

5. **Planning Petra (This Agent):**
   - ✅ **Create:** M5.1 task files (9 tasks for ADR-046/045)
   - ✅ **Create:** SPEC-TERM-001 Phase 1 task files (6 tasks)
   - ✅ **Create:** Analyst Annie task files (2 tasks)
   - ✅ **Update:** Planning artifacts (FEATURES_OVERVIEW, NEXT_BATCH, DEPENDENCIES) - DONE

### Next Week (After M5.1 or Parallel)

1. **Frontend:**
   - **Execute:** M4.3 initiative tracking frontend (5-7h) - After python-pedro backend complete

2. **Architect Alphonso:**
   - **Review:** M5.1 implementation (ADR-046/045 validation, 1-2h)
   - **Review:** SPEC-TERM-001 specification (stakeholder review, 1-2h)

3. **Curator Claire:**
   - **Execute:** Resolve src-consolidation plan conflict (30min) - Archive or update

### Batch Sequencing Decision

**Option A: Sequential (Lower Risk)**
```
1. Complete M4.3 (Initiative Tracking) - 11-15h
2. Execute M5.1 (Domain Refactoring + Model) - 18-27h
3. Execute SPEC-TERM-001 Phase 1 (Terminology) - 35h
Total: 64-77h sequential
```

**Option B: Parallel (Higher Velocity, Higher Risk)**
```
Stream 1: M4.3 (python-pedro + frontend) - 11-15h
Stream 2: M5.1 ADR-046 (backend-dev) - 8-12h
Stream 3: SPEC-TERM-001 directives (code-reviewer-cindy) - 4h
Then: M5.1 ADR-045 (backend-dev) - 10-15h
Then: SPEC-TERM-001 refactors (backend-dev) - 31h
Total: 64-77h with parallelism (faster wall-clock time)
```

**Recommendation:** **Option B (Parallel)** - M4.3, M5.1, and SPEC-TERM-001 directives can run independently. Backend-dev starts M5.1 ADR-046 after task creation, code-reviewer starts directives immediately.

### Resource Constraint Notes

- **Backend Dev Overload:** 49-58h immediate work (M5.1 + SPEC-TERM-001 Phase 1)
  - **Mitigation:** Parallelize where possible, defer Phase 2/3 of SPEC-TERM-001
  - **Alternative:** Defer SPEC-TERM-001 entirely until M5.1 complete (reduces to 18-27h)

---

## 📋 Task Creation Checklist (Planning Petra)

### M5.1 - ADR-046/045 Implementation

- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-adr046-task1-domain-structure.yaml`
- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-adr046-task2-move-files.yaml`
- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-adr046-task3-update-imports.yaml`
- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-adr046-task4-test-docs.yaml`
- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-adr045-task1-models.yaml`
- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-adr045-task2-parsers.yaml`
- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-adr045-task3-agent-parser.yaml`
- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-adr045-task4-validators.yaml`
- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-adr045-task5-integration.yaml`

### SPEC-TERM-001 Phase 1

- [ ] Create `work/collaboration/assigned/code-reviewer-cindy/2026-02-11T[TIME]-term001-feat01-directives.yaml`
- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-term001-feat02a-model-router.yaml`
- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-term001-feat02b-template-renderer.yaml`
- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-term001-feat02c-task-service.yaml`
- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-term001-feat02d-config-loader.yaml`
- [ ] Create `work/collaboration/assigned/backend-dev/2026-02-11T[TIME]-term001-feat02e-agent-registry.yaml`

### Analyst Annie

- [ ] Create `work/collaboration/assigned/analyst-annie/2026-02-11T[TIME]-spec-term-review.yaml`
- [ ] Create `work/collaboration/assigned/analyst-annie/2026-02-11T[TIME]-conceptual-alignment-plan.yaml`

**Total:** 17 task files to create

---

_Document maintained by: Planning Petra_  
_Last reviewed: 2026-02-11_  
_Next review: After M5.1 task creation or Human In Charge approval_
