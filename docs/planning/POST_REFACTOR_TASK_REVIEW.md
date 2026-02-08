# Post-Refactor Task Relevance Review (PR #135)

**Review Date:** 2026-02-08  
**Reviewer:** Planning Petra  
**Context:** Major structural refactor consolidated `ops/`, `validation/`, `examples/` → `src/`, `tools/`, `tests/`, `fixtures/`

---

## Executive Summary

**Total Tasks Reviewed:** 52 assigned tasks across 10 agent directories  
**Path Conflicts:** 33 tasks reference obsolete `ops/` directory  
**Active & Relevant:** 28 tasks (54%)  
**Needs Path Updates:** 18 tasks (35%)  
**Blocked/Outdated:** 6 tasks (11%)

### Key Findings

1. **✅ Dashboard Initiative (M4 Batch 4.3)** - Active, well-specified, 2/3 features complete
2. **⚠️ Multi-Format Distribution (MFD)** - High-priority but needs path updates (`ops/` → `tools/`)
3. **⚠️ LLM Service Layer** - References old structure, needs architectural review post-refactor
4. **❗️ Build Automation** - Several tasks reference non-existent paths and need validation
5. **✅ ADR-023 Prompt Optimization** - Relevant, aligns with framework health goals

---

## Task Categories

### Category A: Active & Ready to Execute (14 tasks)

These tasks are relevant, unblocked, and correctly reference current structure:

#### Dashboard Enhancement Initiative (M4 Batch 4.3) - HIGHEST PRIORITY
- **2026-02-06T1150** - Initiative Tracking (python-pedro) - `MEDIUM` priority, 11-15h
  - ✅ Spec complete, ADR-037 accepted, dependencies met
- **2026-02-06T1221** - Repository Initialization (python-pedro) - `MEDIUM`, 16-21h  
- **2026-02-06T1222** - Configuration Management (python-pedro) - `HIGH`, 23-30h
- **2026-02-06T1220** - Docsite Integration (frontend) - `MEDIUM`, 9-12h
- **2026-02-06T1200** - Markdown Rendering Test (frontend) - `HIGH`, in_progress

**Recommendation:** Continue M4 Batch 4.3b (Initiative Tracking) as per NEXT_BATCH.md

#### Prompt Optimization (ADR-023 aligned)
- **2026-01-30T1120** - Design Prompt Optimization Framework (architect-alphonso) - `HIGH`
  - Strategic value: 30-40% efficiency gain potential
  - Aligns with framework health goals (target score: 97-98/100)

#### Documentation & Governance
- **2026-02-04T1714** - Persona Workflows (scribe) - `MEDIUM`
- **2026-01-31T0638** - Primer-aligned directive validation (architect) - `ASSIGNED`
- **2026-01-31T0638** - ATDD/TDD directive integration (curator) - `ASSIGNED`

#### Build & CI/CD
- **2025-11-28T0427** - Work items cleanup script (build-automation) - `MEDIUM`
- **2026-01-30T1644** - ADR-023 Phase 2 CI workflow (build-automation) - `HIGH`

#### Content Integration
- **2025-12-04T0528** - Integrate feasibility study artifacts (curator) - `HIGH`
- **2025-12-04T0527** - Polish feasibility documents (writer-editor) - `HIGH`

---

### Category B: Needs Path Updates (18 tasks)

These tasks reference obsolete `ops/` directory and need artifact path corrections:

#### Multi-Format Distribution (MFD) - CRITICAL PATH
All MFD tasks need `ops/` → `tools/` updates:

- **2026-01-29T0730-mfd-task-1.2** - Implement Parser (backend-dev) - `CRITICAL`
  - Artifact: `ops/exporters/parser.js` → `tools/exporters/parser.js` ✅ (already moved)
  - Status: TODO, can proceed with updated paths
  
- **2026-01-29T0730-mfd-task-1.3** - Schema Conventions (architect-alphonso) - `HIGH`
  - Dependencies resolved, ready after parser
  
- **2026-01-29T0730-mfd-task-1.4** - Create 5 Schemas (backend-dev) - `HIGH`
  - Depends on 1.3, blocked
  
- **2026-01-29T0730-mfd-task-2.1** - OpenCode Generator (backend-dev) - `HIGH`
  - Depends on parser, blocked

**Action Required:** Batch update MFD task artifacts to reference `tools/exporters/`

#### LLM Service Layer Tasks
Need architectural validation post-refactor:

- **2026-02-04T1705** - Claude-Code adapter (backend-dev) - `HIGH`
  - Artifact: `src/llm_service/adapters/claude_code.py` ✅ (path correct)
  - Milestone: Tool Integration
  
- **2026-02-04T1709** - Policy engine (backend-dev) - `HIGH`
  - LLM service alignment needed
  
- **2026-02-05T1000** - GenericYAMLAdapter (python-pedro) - `HIGH`
- **2026-02-05T1001** - YAML ENV variables (backend-dev) - `MEDIUM`
- **2026-02-05T1002** - Routing integration (backend-dev) - `HIGH`

**Action Required:** Verify LLM service architecture alignment with `src/` structure

#### Framework Core Tasks
- **2025-12-01T0510** - Framework config loader (python-pedro) - `HIGH`
  - Artifact: Reference `src/framework/config/` (post-refactor location)
  
- **2025-12-01T0511** - Agent profile parser (python-pedro) - `MEDIUM`
  - Update to use `doctrine/agents/` paths

#### Model Client Interface
- **2025-11-30T1202** - model_client interface (architect) - `HIGH`
  - Artifact: `ops/orchestration/model_client.py` → `src/framework/orchestration/model_client.py` ✅

#### ADR-023 Implementation
- **2026-01-30T1642** - Phase 2 Prompt Validator (backend-dev) - `HIGH`
- **2026-01-30T1643** - Phase 3 Context Loader (backend-dev) - `HIGH`

#### CI/CD & Validation
- **2025-11-30T1206** - CI router schema validation (build-automation) - `HIGH`
  - Update to use `tools/validators/`
  
- **2025-12-01T0513** - Framework CI tests (build-automation) - `HIGH`
  - Update paths: `tests/framework/`, `tools/validators/`

---

### Category C: Blocked or Requires Clarification (6 tasks)

#### Blocked Tasks
- **2025-11-24T1736** - Framework efficiency assessment (architect) - `LOW`, `BLOCKED`
  - Blocker: Missing `work/metrics/token-metrics-2025-11-24.json`
  - Blocker: ADR-012 naming conflict (already exists for ATDD/TDD)
  - **Recommendation:** Archive or rename ADR target
  
- **2026-01-29T0935** - GitHub workflow review (build-automation) - `HIGH`, `NEW`
  - **Status:** Already completed on 2026-02-08 (see commit 4937a8e)
  - **Recommendation:** Mark as DONE and archive

#### Needs Specification
- **2025-11-30T1203** - Model selection template (scribe) - `HIGH`
  - Task descriptor template extension
  - **Recommendation:** Analyst Annie should define acceptance criteria

- **2025-11-24T0953** - Parallel tool installation (build-automation) - `NORMAL`
  - Optimization task, no clear success criteria
  - **Recommendation:** Analyst Annie to define performance targets

#### Low Priority / Deferred
- **2025-11-24T0954** - Telemetry collection (build-automation) - `LOW`
  - Infrastructure task, low urgency
  - **Recommendation:** Archive to backlog
  
- **2026-02-05T1400** - Rich Terminal UI (backend-dev) - `LOW`, `PENDING`
  - UX enhancement, not critical path
  - **Recommendation:** Defer to M5 or later

---

### Category D: Outdated / Redundant (4 tasks)

#### Completed but Not Archived
- **2026-01-29T0850-mfd-task-1.5** - Base validator - `COMPLETE`
  - **Action:** Move to `work/collaboration/done/`
  
- **2026-02-05T1400-writer-editor-spec-driven-primer** - `COMPLETED`
  - **Action:** Move to `work/collaboration/done/`

#### POC3 Follow-up Tasks (Low Priority)
- **2025-11-27T1956** - POC3 Followup Synthesis (writer-editor) - `HIGH` (misprioritized)
- **2026-01-31T0638** - POC3 Aggregate metrics (writer-editor) - `ASSIGNED`
- **2026-01-31T0638** - POC3 Diagram updates (synthesizer) - `LOW`
- **2026-01-31T0638** - POC3 Multi-agent chain (diagrammer) - `ASSIGNED`

**Recommendation:** Batch archive POC3 tasks or downgrade to `LOW` priority

---

## Priority Recommendations

### Immediate (This Week)
1. **Complete M4 Batch 4.3b** - Initiative Tracking (python-pedro, 11-15h)
2. **Update MFD task paths** - Batch update artifact references (Planning Petra, 1h)
3. **Archive completed tasks** - Clean up DONE items (Planning Petra, 30min)

### High Priority (Next 2 Weeks)
1. **MFD Critical Path** - Parser → Schema Conventions → 5 Schemas (backend-dev + architect)
2. **Prompt Optimization Framework** - Design ADR (architect-alphonso, 6-8h)
3. **LLM Service Alignment** - Validate architecture post-refactor (architect + backend-dev)

### Medium Priority (Next Month)
1. **Dashboard Remaining Features** - Docsite integration, repo init, config management
2. **ADR-023 Implementation** - Prompt validator + context loader
3. **CI/CD Hardening** - Framework tests, router validation

### Low Priority / Backlog
1. **POC3 Follow-ups** - Archive or defer
2. **Telemetry & Optimization** - Nice-to-have enhancements
3. **UI Polish** - Rich terminal UI, template generation

---

## Delegation Decisions

### Tasks Needing Analyst Annie (Specification Work)
1. **Model Selection Template** (2025-11-30T1203)
   - Define acceptance criteria for template extensions
   - Document integration with existing task descriptors
   
2. **Parallel Installation** (2025-11-24T0953)
   - Define performance benchmarks (baseline vs. optimized)
   - Specify compatibility requirements (OS, shell versions)
   
3. **Framework Efficiency Assessment** (2025-11-24T1736) - BLOCKED
   - Resolve ADR naming conflict
   - Define metrics schema or use alternative artifact location

**Priority Order for Annie:**
1. Model Selection Template (blocks scribe work)
2. Parallel Installation (enables DevOps efficiency gains)
3. Framework Efficiency (blocked, low priority)

---

## Assumptions & Risks

### Assumptions
- ✅ Dashboard initiative remains highest priority (confirmed in NEXT_BATCH.md)
- ⚠️ MFD tasks will proceed with updated paths (needs confirmation)
- ⚠️ LLM service architecture is compatible with new `src/` structure (needs validation)
- ✅ POC3 work is concluded and follow-ups can be archived

### Risks
- **Risk 1:** 33 tasks with obsolete paths may cause confusion if not batch-updated
  - **Mitigation:** Planning Petra to create path migration script
  
- **Risk 2:** MFD critical path blocked by schema conventions (architect dependency)
  - **Mitigation:** Architect Alphonso to prioritize schema conventions task
  
- **Risk 3:** LLM service tasks may need rework after refactor validation
  - **Mitigation:** Architect to review LLM service design document before implementation

---

## Next Actions

### For Planning Petra (This Session)
- ✅ Create task relevance review document
- ✅ Update NEXT_BATCH.md if needed
- ✅ Create AGENT_TASKS.md with updated assignments
- ✅ Create DEPENDENCIES.md mapping
- ⬜ Create path migration guide for task artifact updates

### For Analyst Annie (Next)
- Spec: Model Selection Template (2h)
- Spec: Parallel Installation benchmarks (1h)

### For Architect Alphonso (Next)
- Review: LLM service architecture alignment (2h)
- Task: Schema Conventions (mfd-task-1.3, 3h)
- Task: Prompt Optimization Framework design (6-8h)

### For Backend-Dev/Python-Pedro (Next)
- Task: Initiative Tracking backend (6-8h) - **HIGHEST PRIORITY**
- Task: Parser implementation (6h) - after path updates

---

## Metrics

**Task Health:**
- Active: 28 (54%)
- Needs updates: 18 (35%)
- Blocked: 6 (11%)

**Priority Distribution:**
- CRITICAL: 1
- HIGH: 22
- MEDIUM: 14
- LOW: 7
- UNKNOWN: 8

**Agent Workload (Active Tasks):**
- backend-dev: 10 tasks
- python-pedro: 6 tasks
- build-automation: 9 tasks
- architect: 5 tasks
- frontend: 2 tasks
- writer-editor: 4 tasks
- Others: 16 tasks

**Estimated Effort (Active + Ready):**
- Immediate batch (M4.3b): 11-15 hours
- High priority tasks: 50-70 hours
- Medium priority: 80-120 hours

---

_Review completed: 2026-02-08T1250 by Planning Petra_  
_Next review: After M4 Batch 4.3 completion or if priorities shift_
