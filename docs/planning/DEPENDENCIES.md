# Task Dependencies Map

**Last Updated:** 2026-02-11  
**Context:** Post-conceptual alignment stabilization  
**Purpose:** Track what needs to happen before what

**Recent Additions (2026-02-11):**
- ✅ Added ADR-046 → ADR-045 dependency (domain refactoring before domain model)
- ✅ Added SPEC-TERM-001 phasing dependencies
- ✅ Added DDR-001/002 as prerequisites for agent profile updates
- ✅ Added M5.1 batch dependencies

---

## 🆕 Critical Path Analysis - M5.1 (Conceptual Alignment Foundation)

### Path 1: Domain Model Implementation - CRITICAL

```
M5 Milestone 1: Domain Foundation
├─ ADR-046: Domain Module Refactoring ⭐⭐⭐⭐⭐ CRITICAL (must go first)
│   ├─ Task 5.1.1: Create domain directory structure (1-2h)
│   ├─ Task 5.1.2: Move files to bounded contexts (2-3h)
│   ├─ Task 5.1.3: Update import statements (3-4h) ⚠️ HIGH TOUCH COUNT
│   └─ Task 5.1.4: Test & documentation (2-3h)
│   └─ **Total:** 8-12 hours
│
├─ ADR-045: Doctrine Concept Domain Model ⭐⭐⭐⭐ HIGH (after ADR-046)
│   ├─ Task 5.1.5: Create doctrine domain models (4h)
│   ├─ Task 5.1.6: Implement parsers (4h)
│   ├─ Task 5.1.7: Agent profile parser (2h)
│   ├─ Task 5.1.8: Validators & tests (2-3h)
│   └─ Task 5.1.9: Dashboard & exporter integration (2-4h)
│   └─ **Total:** 10-15 hours
│   └─ **BLOCKS:** Dashboard doctrine display, vendor distribution
│
└─ **M5.1 Total:** 18-27 hours (sequential, cannot parallelize)

**Status:** Tasks not yet created (Planning Petra action item)  
**Next:** Planning Petra creates task files, backend-dev executes
```

### Dependency Relationship

```
ADR-046 (Domain Refactoring)
    ↓ BLOCKS
ADR-045 (Domain Model)
    ↓ ENABLES
├─ Dashboard doctrine display (SPEC-DASH-008)
├─ Vendor distribution (SPEC-DIST-001)
├─ SPEC-TERM-001 implementation (needs bounded contexts)
└─ Future domain work
```

---

## Critical Path Analysis

### Path 1: Dashboard Initiative (M4 Batch 4.3) - ACTIVE

```
├─ Phase 1: Markdown Rendering ✅ COMPLETE (2026-02-06)
├─ Phase 2: Priority Editing ✅ COMPLETE (2026-02-06)
├─ Phase 3: Initiative Tracking (IN PROGRESS)
│   ├─ Backend API (python-pedro, 6-8h) → Frontend UI (frontend, 5-7h)
│   └─ Specification parsing + Task linking + Progress rollup
├─ Phase 4: Docsite Integration (BACKLOG)
│   └─ Depends on: Initiative tracking ✅
├─ Phase 5: Repository Initialization (BACKLOG)
│   └─ Depends on: Initiative tracking ✅
└─ Phase 6: Configuration Management (BACKLOG)
    └─ Depends on: Repository initialization

**Status:** 2/6 complete (47% of Batch 4.3)  
**Next:** Python-pedro starts backend, frontend waits for API contract
```

---

### Path 2: SPEC-TERM-001 Terminology Alignment - HIGH PRIORITY

```
Phase 1: Foundation (Can Parallel with M5.1)
├─ FEAT-TERM-001-01: Directive Updates (4h) ⭐⭐⭐⭐ HIGH
│   └─ Update directives for naming enforcement and workflow compliance
│   └─ **Prerequisites:** None (can start immediately)
│   └─ **Enables:** Future PR enforcement
│
├─ FEAT-TERM-001-02: Top 5 Generic Class Refactors (31h) ⭐⭐⭐⭐ HIGH
│   ├─ ModelConfigurationManager → ModelRouter (8h)
│   ├─ TemplateManager → TemplateRenderer (6h)
│   ├─ TaskAssignmentHandler → TaskAssignmentService (8h)
│   ├─ OrchestrationConfigLoader → Domain name (5h)
│   └─ AgentSpecRegistry → Domain name (4h)
│   └─ **Prerequisites:** ADR-046 helpful but not required
│   └─ **Impact:** 65% → 75% linguistic health score
│
└─ **Phase 1 Total:** 35 hours (can parallel with M5.1)

Phase 2: Standardization (After Phase 1)
├─ FEAT-TERM-001-03: Terminology Standardization (6h)
│   └─ Resolve State/Status, Load/read, Persist/write conflicts
│   └─ **Prerequisites:** Phase 1 complete, glossary established
│
└─ FEAT-TERM-001-04: Task Context Boundary (40h)
    └─ Implement ADR for bounded context separation
    └─ **Prerequisites:** ADR-045/046 complete (needs domain structure)
    └─ **BLOCKED BY:** M5.1 completion

Phase 3: Completion (Opportunistic)
├─ FEAT-TERM-001-05: CQRS Research (8h)
├─ FEAT-TERM-001-06: Remaining 14 Refactors (52h) - Boy Scout Rule
└─ FEAT-TERM-001-07: Glossary Automation (ongoing, 30min/week)

**Total Effort:** ~120 hours across 3 phases  
**Critical Path:** Phase 1 (35h) can start immediately  
**Recommended:** Execute Phase 1 during M5.1 (parallel work streams)
```

### DDR-001/002 Prerequisites

```
DDR-001: Primer Execution Matrix
└─ Prerequisites for:
    ├─ Agent profile updates (primer modes documented)
    ├─ Orchestration workflow refinements
    └─ Test-first execution patterns

DDR-002: Framework Guardian Role  
└─ Prerequisites for:
    ├─ Guardian agent profile updates
    ├─ Distribution / release enablement features
    └─ Framework integrity automation
```

---

### Path 3: Dashboard Initiative (M4 Batch 4.3) - IN PROGRESS

```
Milestone 1: Schema Complete
├─ Task 1.1: Design IR Structure ✅ ASSUMED COMPLETE
├─ Task 1.2: Implement Parser (backend-dev, 6h) ⚠️ PATH UPDATE NEEDED
│   └─ Artifact: tools/exporters/parser.js (was ops/exporters/parser.js)
├─ Task 1.3: Schema Conventions (architect-alphonso, 3h) ⏳ WAITING ON 1.2
│   └─ Blocks: 1.4, 2.4 (all schema creation tasks)
├─ Task 1.4: Create 5 Schemas (backend-dev, 4h) ⏳ WAITING ON 1.3
└─ Task 1.5: Base Validator ✅ COMPLETE

Milestone 2: Generators Complete
├─ Task 2.1: OpenCode Generator (backend-dev, 6h) ⏳ WAITING ON 1.2
├─ Task 2.2: Copilot Generator ❓ NOT ASSIGNED
├─ Task 2.3: Claude-Code Generator ❓ NOT ASSIGNED
└─ Task 2.4: Complete 12 Schemas (backend-dev) ⏳ WAITING ON 1.4

**Status:** 1/5 complete in Milestone 1, 0/4 in Milestone 2  
**Critical Blocker:** Parser implementation (1.2) with path updates  
**Next:** Backend-dev updates task artifact paths, then implements parser
```

---

### Path 3: ADR-023 Prompt Optimization - READY

```
Phase 1: Design
└─ 2026-01-30T1120: Design Prompt Optimization Framework (architect, 6-8h) ✅ READY
    └─ Depends on: Analysis complete ✅ (work-log-analysis-suboptimal-patterns.md)

Phase 2: Validation
├─ 2026-01-30T1642: Prompt Validator (backend-dev) ⏳ WAITING ON DESIGN
└─ 2026-01-30T1644: CI Workflow (build-automation) ⏳ WAITING ON VALIDATOR

Phase 3: Context Loading
└─ 2026-01-30T1643: Progressive Context Loader (backend-dev) ⏳ WAITING ON DESIGN

**Status:** Design ready to start, implementation waiting  
**Next:** Architect Alphonso designs framework, backend-dev implements
```

---

### Path 4: LLM Service Layer - ON HOLD

```
Foundation
├─ Architecture Review ❗ NEEDS VALIDATION post-refactor
│   └─ Verify alignment with src/ structure
└─ Config/Tools YAML Schema ⚠️ IN PROGRESS

Adapters
├─ 2026-02-04T1705: Claude-Code Adapter (backend-dev) ⏳ WAITING ON ARCH REVIEW
├─ Generic YAML Adapter (python-pedro) ⏳ WAITING ON ARCH REVIEW
└─ Policy Engine (backend-dev) ⏳ WAITING ON ARCH REVIEW

Integration
└─ 2026-02-05T1002: Routing Integration ⏳ WAITING ON ADAPTERS

**Status:** All blocked pending architecture validation  
**Critical Action:** Architect Alphonso reviews LLM service design doc  
**Risk:** May need significant rework after refactor
```

---

## Dependency Relationships

### Dependency Graph

```mermaid
graph TD
    A[Parser 1.2] --> B[Schema Conventions 1.3]
    B --> C[5 Schemas 1.4]
    C --> D[12 Schemas 2.4]
    A --> E[OpenCode Generator 2.1]
    
    F[Initiative Tracking Backend] --> G[Initiative Tracking Frontend]
    G --> H[Docsite Integration]
    H --> I[Repository Init]
    I --> J[Config Management]
    
    K[Prompt Framework Design] --> L[Prompt Validator]
    K --> M[Context Loader]
    L --> N[CI Workflow]
    
    O[Arch Review: LLM Service] --> P[Claude Adapter]
    O --> Q[YAML Adapter]
    O --> R[Policy Engine]
    P --> S[Routing Integration]
    Q --> S
    R --> S
```

---

## Task Dependency Details

### Dashboard Initiative Dependencies

#### 2026-02-06T1150: Initiative Tracking Backend (python-pedro)
- **Prerequisites:**
  - ✅ Markdown rendering complete (2026-02-06T1148)
  - ✅ Priority editing complete (2026-02-06T1149)
  - ✅ Specification SPEC-DASH-003 complete
  - ✅ ADR-037 accepted
- **Provides:** GET /api/portfolio endpoint, WebSocket portfolio updates
- **Blocks:** Initiative tracking frontend

#### 2026-02-06T1150: Initiative Tracking Frontend (frontend)
- **Prerequisites:**
  - ⏳ Initiative tracking backend API complete
  - ⏳ API contract agreed (portfol io structure, WebSocket events)
- **Provides:** Portfolio UI, progress visualization
- **Blocks:** None (user-facing feature)

#### 2026-02-06T1220: Docsite Integration (frontend)
- **Prerequisites:**
  - ✅ Initiative tracking complete (context: user navigates from portfolio to docs)
- **Provides:** Embedded docs-site in dashboard
- **Blocks:** None

#### 2026-02-06T1221: Repository Initialization (python-pedro)
- **Prerequisites:**
  - ✅ Initiative tracking complete (shows initiative setup progress)
- **Provides:** Web-based repo setup wizard
- **Blocks:** Configuration management

#### 2026-02-06T1222: Configuration Management (python-pedro)
- **Prerequisites:**
  - ⏳ Repository initialization complete (config editor uses repo metadata)
- **Provides:** Web-based config editor
- **Blocks:** None

---

### Multi-Format Distribution Dependencies

#### 2026-01-29T0730-mfd-task-1.2: Parser (backend-dev)
- **Prerequisites:**
  - ✅ IR structure defined (task 1.1)
  - ⚠️ Path update: `tools/exporters/parser.js`
- **Provides:** Agent markdown → IR conversion
- **Blocks:** Schema conventions (1.3), OpenCode generator (2.1), all downstream tasks

#### 2026-01-29T0730-mfd-task-1.3: Schema Conventions (architect)
- **Prerequisites:**
  - ⏳ Parser available for testing extraction heuristics
- **Provides:** JSON Schema standards, migration checklist
- **Blocks:** All schema creation tasks (1.4, 2.4)

#### 2026-01-29T0730-mfd-task-1.4: 5 Schemas (backend-dev)
- **Prerequisites:**
  - ⏳ Schema conventions documented
- **Provides:** Input/output schemas for 5 representative agents
- **Blocks:** Remaining 12 schemas (2.4)

#### 2026-01-29T0730-mfd-task-2.1: OpenCode Generator (backend-dev)
- **Prerequisites:**
  - ⏳ Parser complete (consumes IR output)
- **Provides:** OpenCode agent definition generation
- **Blocks:** None (standalone generator)

---

### ADR-023 Prompt Optimization Dependencies

#### 2026-01-30T1120: Design Framework (architect)
- **Prerequisites:**
  - ✅ Work log analysis complete
  - ✅ 12 suboptimal patterns identified
- **Provides:** ADR with architecture, migration plan, schemas
- **Blocks:** Prompt validator, context loader

#### 2026-01-30T1642: Prompt Validator (backend-dev)
- **Prerequisites:**
  - ⏳ Framework design complete (defines validation schema)
- **Provides:** Prompt structure validation tool
- **Blocks:** CI workflow

#### 2026-01-30T1643: Context Loader (backend-dev)
- **Prerequisites:**
  - ⏳ Framework design complete (defines progressive loading strategy)
- **Provides:** Token-aware context loading
- **Blocks:** None (standalone utility)

#### 2026-01-30T1644: CI Workflow (build-automation)
- **Prerequisites:**
  - ⏳ Prompt validator implemented
- **Provides:** Automated prompt validation in CI/CD
- **Blocks:** None

---

### LLM Service Dependencies (ON HOLD)

#### Architecture Review (architect) - NOT YET SCHEDULED
- **Prerequisites:**
  - ⚠️ Post-refactor structure validation
  - ⚠️ LLM service design doc review
- **Provides:** Validation of src/ compatibility, adaptation recommendations
- **Blocks:** ALL LLM service tasks

#### 2026-02-04T1705: Claude-Code Adapter (backend-dev)
- **Prerequisites:**
  - ⏳ Architecture review complete
  - ⚠️ Config schema defined (tools.yaml structure)
- **Provides:** Claude CLI adapter with template execution
- **Blocks:** Routing integration

#### 2026-02-05T1000: Generic YAML Adapter (python-pedro)
- **Prerequisites:**
  - ⏳ Architecture review complete
  - ⚠️ Adapter base interface defined
- **Provides:** YAML-driven LLM adapter
- **Blocks:** Routing integration

#### 2026-02-04T1709: Policy Engine (backend-dev)
- **Prerequisites:**
  - ⏳ Architecture review complete
- **Provides:** Budget enforcement, cost optimization
- **Blocks:** Routing integration

#### 2026-02-05T1002: Routing Integration (backend-dev)
- **Prerequisites:**
  - ⏳ Claude adapter complete
  - ⏳ YAML adapter complete
  - ⏳ Policy engine complete
- **Provides:** Unified routing with all adapters + policies
- **Blocks:** None (capstone integration)

---

### Framework Core Dependencies

#### 2025-12-01T0510: Framework Config Loader (python-pedro)
- **Prerequisites:**
  - ⚠️ Path update: `src/framework/config/loader.py`
  - ⚠️ Config schema defined (router config, model routing)
- **Provides:** Runtime config loading for orchestration
- **Blocks:** Router-aware orchestration tasks

#### 2025-12-01T0511: Agent Profile Parser (python-pedro)
- **Prerequisites:**
  - ⚠️ Path update: Reference `doctrine/agents/` paths
- **Provides:** Runtime agent profile parsing
- **Blocks:** Dynamic agent loading features

#### 2025-11-30T1202: Model Client Interface (architect)
- **Prerequisites:**
  - ✅ None (standalone design task)
- **Provides:** Router-agnostic orchestration interface
- **Blocks:** None (interface definition, implementations follow)

---

### CI/CD & Validation Dependencies

#### 2025-11-30T1206: CI Router Schema Validation (build-automation)
- **Prerequisites:**
  - ⚠️ Path update: `tools/validators/router_validator.py`
  - ✅ Router config schema defined
- **Provides:** CI validation of router configurations
- **Blocks:** None

#### 2025-12-01T0513: Framework CI Tests (build-automation)
- **Prerequisites:**
  - ⚠️ Path updates: `tests/framework/`, `tools/validators/`
  - ✅ Test suites exist (post-refactor)
- **Provides:** Full framework test suite in CI
- **Blocks:** None

#### 2025-11-28T0427: Work Items Cleanup Script (build-automation)
- **Prerequisites:**
  - ✅ None (utility script)
- **Provides:** Automated archival of completed tasks
- **Blocks:** None

---

### Documentation & Content Dependencies

#### 2025-12-04T0528: Integrate Feasibility Artifacts (curator)
- **Prerequisites:**
  - ✅ Feasibility study complete
- **Provides:** Docsite metadata separation artifacts integrated
- **Blocks:** Feasibility document polish

#### 2025-12-04T0527: Polish Feasibility Documents (writer-editor)
- **Prerequisites:**
  - ⏳ Curator integration complete
- **Provides:** Polished feasibility documentation
- **Blocks:** None

#### 2026-02-04T1714: Persona Workflows (scribe)
- **Prerequisites:**
  - ✅ Persona definitions (docs/audience/)
- **Provides:** Example workflows for 3 personas
- **Blocks:** None

#### 2025-11-30T1203: Model Selection Template (scribe)
- **Prerequisites:**
  - ❗ Analyst Annie specification (BLOCKED)
- **Provides:** Extended task descriptor template
- **Blocks:** None

---

## Blocked Tasks Summary

### Hard Blockers (Cannot Proceed)

1. **MFD Schema Conventions (1.3)** ← Waiting on Parser (1.2)
2. **MFD 5 Schemas (1.4)** ← Waiting on Schema Conventions (1.3)
3. **MFD OpenCode Generator (2.1)** ← Waiting on Parser (1.2)
4. **Initiative Tracking Frontend** ← Waiting on Backend API
5. **ADR-023 Validator** ← Waiting on Framework Design
6. **ADR-023 Context Loader** ← Waiting on Framework Design
7. **ADR-023 CI Workflow** ← Waiting on Validator
8. **All LLM Service Tasks** ← Waiting on Architecture Review

### Soft Blockers (Needs Specification)

1. **Model Selection Template** ← Analyst Annie spec needed
2. **Parallel Installation** ← Analyst Annie benchmarks needed

### Path Update Needed (Can Proceed After Update)

1. **Parser (1.2)** - `ops/` → `tools/`
2. **Framework Config Loader** - `ops/` → `src/`
3. **Agent Profile Parser** - Reference `doctrine/`
4. **CI Router Validation** - `ops/` → `tools/`
5. **Framework CI Tests** - Multiple path updates

---

## Unblocking Actions

### Immediate (This Week)

1. **Planning Petra:** Create path migration script for 18 tasks
2. **Backend-dev:** Update parser task paths, implement parser (6h)
3. **Python-pedro:** Start initiative tracking backend (6-8h)
4. **Architect:** Begin prompt optimization framework design (6-8h)

### High Priority (Next Week)

1. **Architect:** Complete schema conventions after parser (3h)
2. **Architect:** Review LLM service architecture (2h)
3. **Backend-dev:** Create 5 schemas after conventions (4h)
4. **Frontend:** Implement initiative tracking UI after backend (5-7h)

### Medium Priority (Next 2 Weeks)

1. **Analyst Annie:** Spec for model selection template (2h)
2. **Analyst Annie:** Define parallel installation benchmarks (1h)
3. **Backend-dev:** Implement ADR-023 validator and context loader (12h total)
4. **Build-automation:** Create CI workflows for prompt validation (4h)

---

## Dependency Metrics

**Total Dependencies Tracked:** 35 tasks with explicit dependencies  
**Blocked Tasks:** 8 hard blockers, 2 soft blockers  
**Ready Tasks:** 14 tasks with all prerequisites met  
**Path Updates Needed:** 18 tasks

**Longest Dependency Chain:** 6 levels (Parser → Conventions → 5 Schemas → 12 Schemas → Complete Generators → Distribution)

**Critical Path Duration:** 25-35 hours (Parser → OpenCode generator)  
**Parallel Work Capacity:** 3-4 independent streams (Dashboard, ADR-023, LLM Service, CI/CD)

---

## Risk Assessment

### High Risk Dependencies

1. **LLM Service Architecture Review** (MISSING) ← Blocks 6 tasks, no ETA
   - **Mitigation:** Schedule architect review ASAP, 2h effort

2. **Parser Implementation** ← Blocks entire MFD critical path
   - **Mitigation:** Prioritize path updates, assign backend-dev immediately

3. **Schema Conventions** ← Blocks 12+ schema creation tasks
   - **Mitigation:** Architect Alphonso to start after parser available

### Medium Risk Dependencies

1. **Analyst Annie Specifications** ← Blocks 2 tasks, no ETA
   - **Mitigation:** Define scope for model selection template, assign Annie

2. **Initiative Tracking Backend** ← Blocks frontend UI
   - **Mitigation:** Already prioritized in M4 Batch 4.3b

---

_Dependency map maintained by: Planning Petra_  
_Last updated: 2026-02-11_  
_Next update: After M5.1 completion or M4.3 completion_

---

## 🆕 Updated Dependency Graph (2026-02-11)

### Strategic Dependencies

```mermaid
graph TD
    %% M5.1 Conceptual Alignment Foundation
    ADR046[ADR-046: Domain Refactoring] -->|BLOCKS| ADR045[ADR-045: Domain Model]
    ADR045 -->|ENABLES| DASH_DOCTRINE[Dashboard Doctrine Display]
    ADR045 -->|ENABLES| VENDOR_DIST[Vendor Distribution]
    ADR045 -->|ENABLES| TERM_BOUNDARY[SPEC-TERM-001 Phase 2]
    
    %% SPEC-TERM-001 Phases
    TERM_P1[SPEC-TERM-001 Phase 1] -.->|PARALLEL OK| ADR046
    TERM_P1 -->|ENABLES| TERM_P2[SPEC-TERM-001 Phase 2]
    ADR045 -->|REQUIRED FOR| TERM_P2
    
    %% Dashboard Continuation
    M4_3[M4.3 Initiative Tracking] -->|ENABLES| M5_3_DOCSITE[M5.3 Docsite Integration]
    M4_3 -->|ENABLES| M5_3_REPO[M5.3 Repo Initialization]
    ADR045 -->|ENHANCES| M5_3_REPO
    M5_3_REPO -->|ENABLES| M5_3_CONFIG[M5.3 Configuration Management]
    
    %% DDR Prerequisites
    DDR001[DDR-001: Primer Matrix] -.->|PREREQUISITE| AGENT_UPDATES[Agent Profile Updates]
    DDR002[DDR-002: Guardian Role] -.->|PREREQUISITE| GUARDIAN_FEATURES[Guardian Automation]
    
    %% MFD Path (existing)
    MFD_PARSER[MFD Parser 1.2] --> MFD_SCHEMA_CONV[MFD Schema Conventions 1.3]
    MFD_SCHEMA_CONV --> MFD_5SCHEMAS[MFD 5 Schemas 1.4]
    MFD_PARSER --> MFD_GENERATOR[MFD OpenCode Generator 2.1]
```

### Critical Observations

1. **ADR-046 is the critical blocker** - Must complete before ADR-045 (domain model needs bounded contexts)
2. **SPEC-TERM-001 Phase 1 can parallel** - Directive updates and top 5 refactors independent of domain work
3. **M5.1 blocks SPEC-TERM-001 Phase 2** - Task context boundary needs domain structure (ADR-045)
4. **Dashboard continuation deferred** - M4.3 continues, M5.3 (docsite/repo/config) waits for M5.1
5. **DDR-001/002 are informational** - Prerequisites for understanding, not hard blockers

---

## 📊 Updated Blocked Tasks Summary (2026-02-11)

### Hard Blockers (Cannot Proceed)

#### M5.1 - Conceptual Alignment Foundation
1. **ADR-045 Implementation** ← Waiting on ADR-046 (domain refactoring must complete first)
   - 5 tasks, 10-15 hours
   - Backend Dev owner
   - Tasks not yet created

#### SPEC-TERM-001 - Terminology Alignment
2. **FEAT-TERM-001-04 (Task Context Boundary)** ← Waiting on ADR-045 (needs domain model)
   - 40 hours
   - Requires ADR for bounded context separation
   - Phase 2 work, not immediate priority

#### Dashboard (Existing)
3. **Initiative Tracking Frontend** ← Waiting on Backend API (python-pedro, 6-8h remaining)
   - Frontend Freddy, 5-7h
   - API contract needed

#### MFD (Existing - from previous update)
4. **MFD Schema Conventions (1.3)** ← Waiting on Parser (1.2)
5. **MFD 5 Schemas (1.4)** ← Waiting on Schema Conventions (1.3)
6. **MFD OpenCode Generator (2.1)** ← Waiting on Parser (1.2)

#### ADR-023 (Existing)
7. **ADR-023 Validator** ← Waiting on Framework Design
8. **ADR-023 Context Loader** ← Waiting on Framework Design
9. **ADR-023 CI Workflow** ← Waiting on Validator

#### LLM Service (Existing)
10. **All LLM Service Tasks** ← Waiting on Architecture Review

### Soft Blockers (Needs Specification or Approval)

1. **M5.1 Task Execution** ← Human In Charge approval needed (Planning Petra creates tasks)
2. **SPEC-TERM-001 Implementation** ← Spec review approval (Architect, Backend Dev, Code Reviewer)
3. **Model Selection Template** ← Analyst Annie spec needed (existing)

### Tasks Ready to Execute (No Blockers)

#### M5.1 (After Task Creation)
1. **ADR-046 Implementation** (8-12h) - Can start immediately after tasks created
2. **SPEC-TERM-001 Phase 1** (35h) - Can parallel with ADR-046

#### M4.3 (In Progress)
3. **Initiative Tracking Backend** (6-8h) - Python Pedro, in progress

---

## 🎯 Unblocking Actions (Updated 2026-02-11)

### Immediate (This Session - Planning Petra)

1. ✅ **Update FEATURES_OVERVIEW.md** - Add ADR-045/046, SPEC-TERM-001
2. ✅ **Update NEXT_BATCH.md** - Define M5.1 batch
3. ✅ **Update DEPENDENCIES.md** - Add M5.1 and SPEC-TERM-001 dependencies
4. 🔄 **Update AGENT_TASKS.md** - Assign M5.1 and SPEC-TERM-001 tasks (next)
5. 🔄 **Create M5.1 task files** - ADR-046 (4 tasks) and ADR-045 (5 tasks)

### High Priority (Next 1-2 Days)

1. **Human In Charge:** Approve M5.1 batch execution (18-27h, CRITICAL)
2. **Backend-dev:** Execute ADR-046 refactoring (8-12h) after task creation
3. **Python-pedro:** Complete M4.3 initiative tracking backend (6-8h)
4. **Architect:** Review M5.1 task breakdown (1-2h)

### Medium Priority (Next Week)

1. **Backend-dev:** Execute ADR-045 domain model (10-15h) after ADR-046
2. **Analyst Annie:** Create conceptual alignment plan (2-3h)
3. **Curator:** Resolve src-consolidation conflict (30min)
4. **Stakeholders:** Review SPEC-TERM-001 spec (Architect, Backend Dev, Code Reviewer)

---

## 📈 Dependency Metrics (Updated)

**Total Dependencies Tracked:** 45+ tasks with explicit dependencies (+10 from last update)  
**Blocked Tasks:** 10 hard blockers, 3 soft blockers (+2 from M5.1 addition)  
**Ready Tasks:** 18 tasks with all prerequisites met (+3 from M5.1)  
**Path Updates Needed:** 18 tasks (unchanged)

**Longest Dependency Chain:** 7 levels (ADR-046 → ADR-045 → SPEC-TERM-001 Phase 2 → ...)  
**Critical Path Duration:** 18-27 hours (M5.1), then 40h (SPEC-TERM-001 Phase 2)  
**Parallel Work Capacity:** 4-5 independent streams (M4.3, M5.1, SPEC-TERM-001 Phase 1, MFD, CI/CD)

---

## ⚠️ Updated Risk Assessment

### NEW: High Risk Dependencies

1. **M5.1 ADR-046 Import Updates** (NEW) ← Touches ~50 files, high merge conflict risk
   - **Mitigation:** Execute during low-activity window, coordinate with team, automated script
   
2. **M5.1 Sequential Dependency** (NEW) ← ADR-046 must complete before ADR-045 (18-27h serial)
   - **Mitigation:** Cannot parallelize, schedule accordingly
   
3. **SPEC-TERM-001 Scope Creep** (NEW) ← 120 hours total, risk of expansion
   - **Mitigation:** Enforce Phase 1 scope (35h), defer Phase 2/3

### Existing High Risk Dependencies

4. **LLM Service Architecture Review** (MISSING) ← Blocks 6 tasks, no ETA
   - **Mitigation:** Schedule architect review ASAP, 2h effort

5. **Parser Implementation** ← Blocks entire MFD critical path
   - **Mitigation:** Prioritize path updates, assign backend-dev immediately

---
