# Agent Task Assignments

**Last Updated:** 2026-02-08  
**Planning Cycle:** Post-PR #135 Refactor Review  
**Active Batch:** M4 Batch 4.3b - Dashboard Initiative Tracking

---

## Current Focus: Dashboard Initiative (M4 Batch 4.3)

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

## Agent Workload Distribution

| Agent | Active Tasks | Total Effort (Active) | Priority Level |
|-------|--------------|----------------------|----------------|
| python-pedro | 6 | 11-15h (immediate), 90-120h (backlog) | CRITICAL |
| backend-dev | 10 | 16h (critical), 12-16h (high) | HIGH |
| frontend | 3 | 5-7h (after backend), 9-12h (backlog) | HIGH |
| architect | 5 | 9-11h (high), 4-6h (medium) | HIGH |
| build-automation | 10 | 4-6h (immediate), 8-12h (high) | HIGH |
| writer-editor | 4 | 3-5h | MEDIUM |
| curator | 2 | 4-6h | MEDIUM |
| scribe | 2 | 4-6h (after unblocked) | MEDIUM |
| manager | 2 | 3-5h | MEDIUM |
| diagrammer | 3 | 4-8h | LOW |
| synthesizer | 1 | 1-2h | LOW |

---

## Recommendations for Human

### This Week
1. **Approve:** Continue M4 Batch 4.3b (Initiative Tracking) - python-pedro + frontend
2. **Review:** Prompt Optimization Framework scope (architect-alphonso)
3. **Decision:** LLM Service architecture post-refactor (architect review needed)

### Path Migration
- **Planning Petra:** Create path migration script for 18 tasks with `ops/` references
- **All Agents:** Review assigned tasks for artifact path accuracy

### Unblocking Actions
- **Analyst Annie:** Spec for Model Selection Template (blocks scribe)
- **Analyst Annie:** Define benchmarks for Parallel Installation (blocks build-automation)

---

_Document maintained by: Planning Petra_  
_Last reviewed: 2026-02-08T1250_  
_Next review: After M4 Batch 4.3b completion_
