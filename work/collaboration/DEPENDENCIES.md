# Task Dependencies Map

**Last Updated**: 2026-01-31 (Iteration 2 Planning)  
**Updated By**: Planning Petra  
**Purpose**: Explicit mapping of task dependencies, blocking relationships, and execution sequences

---

## Iteration 2: Selected Tasks Dependency Analysis

### Overview: 5 Tasks, Minimal Dependencies

**Key Finding**: All 5 selected tasks have **NO BLOCKING DEPENDENCIES** for immediate execution.

**Parallel Execution Capability**: 
- Phase 1: 3 tasks fully independent (curator, writer-editor, architect)
- Phase 2: 2 tasks depend only on same-agent completion (architect Task 4, writer-editor Task 5)

---

## Critical Path: High-Priority Initiatives

### Initiative 1: YAML Format Fixes (NEW - CRITICAL UNBLOCKING) ✅

**Task**: `2026-01-31T0900-curator-fix-yaml-format-errors`  
**Status**: ⭐ SELECTED - CRITICAL - IMMEDIATE EXECUTION  
**Agent**: curator  
**Effort**: 2-3 hours

```
Prerequisites (ALL MET):
✅ No prerequisites - mechanical conversion task
✅ Schema validator available (validate-task-schema.py)
✅ All 6 target files exist in assigned/ directories

Task:
→ 2026-01-31T0900-curator-fix-yaml-format-errors (2-3h)
  Fix 6 YAML files (convert to pure YAML format)
  Agent: curator
  Blocker: None ✅
  
Unblocks (Next Iteration):
→ ADR-023 Initiative ($140-300k ROI)
  - 2026-01-30T1120-architect-design-prompt-optimization-framework
  - 2026-01-30T1642-backend-dev-adr023-phase2-prompt-validator
  - 2026-01-30T1643-backend-dev-adr023-phase3-context-loader
  - 2026-01-30T1644-build-automation-adr023-phase2-ci-workflow
→ Multi-Format Distribution (MFD) Work
  - 2026-01-29T0730-architect-mfd-task-1.3-schema-conventions
  - 2026-01-29T0935-build-automation-mfd-task-0.1-workflow-review

Enables:
→ Orchestrator health monitoring restored
→ System health: 🟡 → 🟢
→ 6 high-value tasks ready for next iteration
```

**Recommendation**: Execute FIRST (highest unblocking value)

---

### Initiative 2: Distribution User Documentation (CONTINUATION) ✅

**Task**: `2026-01-31T0714-writer-editor-distribution-user-guide`  
**Status**: ⭐ SELECTED - HIGH PRIORITY  
**Agent**: writer-editor  
**Effort**: 8-10 hours

```
Prerequisites (ALL COMPLETE):
✅ Install/Upgrade Scripts (2025-12-05T1012) - COMPLETED Iteration 1
✅ Release Packaging (2025-12-05T1010) - COMPLETED Iteration 1
✅ Technical Documentation (docs/HOW_TO_USE/framework_install.md) - EXISTS
✅ Build System Docs (ops/release/README.md) - EXISTS
✅ Distribution Config (ops/release/distribution-config.yaml) - EXISTS

Task:
→ 2026-01-31T0714-writer-editor-distribution-user-guide (8-10h)
  Artefacts: 4 user guides (distribution, installation, upgrade, getting started)
  Agent: writer-editor
  Blocker: None ✅
  
Enables:
→ Framework adoption by downstream teams (60% friction reduction)
→ Reduced onboarding time (<30 minutes target)
→ Support burden reduction (40% in 12 months target)
→ Documentation coverage: 70% → 85%+
```

**Recommendation**: Execute in Phase 1 (parallel with Tasks 1, 3)

---

### Initiative 3: Documentation Website (NEW - STRATEGIC FOUNDATION) ✅

**Task**: `2026-01-31T0930-architect-docsite-foundation-setup`  
**Status**: ⭐ SELECTED - HIGH PRIORITY  
**Agent**: architect  
**Effort**: 6-8 hours

```
Prerequisites (ALL MET):
✅ Hugo available (installable, documented in roadmap)
✅ GitHub Pages available for repository
✅ Corporate Hugo theme outline available (for future reference)
✅ Existing HOW_TO_USE guides (content to migrate in future batches)
✅ ADR-022 documented (metadata strategy)

Task:
→ 2026-01-31T0930-architect-docsite-foundation-setup (6-8h)
  Artefacts: Technology selection, architecture, Hugo setup
  Agent: architect
  Blocker: None ✅
  
Creates Handoff Tasks (Batch 1 Completion):
→ 2026-01-31T1000-build-automation-docsite-deployment-workflow (4-6h)
→ 2026-01-31T1030-writer-editor-docsite-homepage-content (6-8h)
→ 2026-01-31T1100-diagrammer-docsite-structure-diagram (2-3h)

Enables (Multi-Batch Initiative):
→ Batch 2: Core content migration (3 weeks, 50-70 hours)
→ Batch 3: User onboarding content (2-3 weeks, 40-60 hours)
→ Batch 4: Developer/architect content (2-3 weeks, 45-65 hours)
→ Batch 5: Polish & launch (1-2 weeks, 25-40 hours)

Strategic Value:
→ Professional documentation website
→ SEO and community growth
→ Adoption enablement
```

**Recommendation**: Execute in Phase 1 (parallel with Tasks 1, 2)

---

### Initiative 4: Framework Guardian (COMPLETION) ✅

**Task**: `2025-12-05T1014-architect-framework-guardian-agent-definition`  
**Status**: ⭐ SELECTED - MEDIUM PRIORITY  
**Agent**: architect  
**Effort**: 4-6 hours

```
Prerequisites (ALL COMPLETE):
✅ Release Packaging System (2025-12-05T1010) - COMPLETED Iteration 1
✅ Install/Upgrade Scripts (2025-12-05T1012) - COMPLETED Iteration 1

Internal Dependency:
⏳ Task 3 (architect doc website foundation) - SELECTED THIS ITERATION
   Same agent, sequential execution recommended

Task:
→ 2025-12-05T1014-architect-framework-guardian-agent-definition (4-6h)
  Artefacts: Agent profile, Directive 025, audit templates
  Agent: architect
  Blocker: Task 3 completion (same agent) OR parallel if capacity
  
Enables:
→ Automated framework health monitoring
→ Post-install/upgrade validation
→ Upgrade guidance system
```

**Recommendation**: Execute in Phase 2 (after Task 3 completes) OR in parallel if architect capacity available

---

### Initiative 5: Release Process Documentation (COMPLETION) ✅

**Task**: `2025-12-05T1016-writer-editor-release-documentation-checklist`  
**Status**: ⭐ SELECTED - MEDIUM PRIORITY  
**Agent**: writer-editor  
**Effort**: 3-4 hours

```
Prerequisites (ALL COMPLETE):
✅ Install/Upgrade Scripts (2025-12-05T1012) - COMPLETED Iteration 1
✅ Release process scripts and documentation exist

Internal Dependency:
⏳ Task 2 (writer-editor distribution user guide) - SELECTED THIS ITERATION
   Same agent, sequential execution recommended

Task:
→ 2025-12-05T1016-writer-editor-release-documentation-checklist (3-4h)
  Artefacts: Release checklist, process documentation
  Agent: writer-editor
  Blocker: Task 2 completion (same agent) OR parallel if capacity
  
Enables:
→ Release process fully documented
→ Documentation quality maintained across releases
→ Zero documentation regressions
```

**Recommendation**: Execute in Phase 2 (after Task 2 completes) OR in parallel if capacity available

---

## Iteration 2 Dependency Summary

### No Blocking Dependencies for Phase 1

All 3 Phase 1 tasks are **fully independent**:
- Task 1 (curator): No dependencies
- Task 2 (writer-editor): No dependencies
- Task 3 (architect): No dependencies

✅ **Can execute in parallel**  
✅ **No file conflicts**  
✅ **Different agents, different artifacts**

### Same-Agent Dependencies in Phase 2

Task 4 and Task 5 depend only on **same-agent** completion:
- Task 4 (architect): Depends on Task 3 (same agent)
- Task 5 (writer-editor): Depends on Task 2 (same agent)

✅ **Sequential execution per agent**  
✅ **OR parallel if multiple agent sessions available**  
✅ **No cross-agent dependencies**

---

## Execution Sequence Recommendation

### Phase 1: Parallel Start (Hour 0)

```
curator (Task 1)         [2-3h]  → YAML Format Fixes
writer-editor (Task 2)   [8-10h] → Distribution User Guide  
architect (Task 3)       [6-8h]  → Doc Website Foundation
```

**All independent, execute simultaneously**

### Phase 2: Sequential Continuation (Hour 6-10)

```
architect (Task 4)       [4-6h]  → Framework Guardian (after Task 3)
writer-editor (Task 5)   [3-4h]  → Release Checklist (after Task 2)
```

**Same-agent follow-ups, OR parallel if capacity**

---

## Cross-Initiative Dependencies (Future Iterations)

### After Task 1 (YAML Fixes) Completes

**Unblocked for Next Iteration**:
```
ADR-023 Prompt Optimization Initiative (HIGH VALUE):
  Phase 1: architect - Design framework (6-8h)
    ↓
  Phase 2a: backend-dev - Validator (6-8h)
    ↓
  Phase 2b: build-automation - CI workflow (3-4h)
    ↓  
  Phase 3: backend-dev - Context loader (6-8h)

Total: 21-28 hours, $140-300k annual ROI
```

### After Task 3 (Doc Website Foundation) Completes

**Handoff Tasks Created**:
```
Documentation Website Batch 1 Completion:
  Task A: build-automation - Deployment workflow (4-6h)
    ↓
  Task B: writer-editor - Homepage content (6-8h)
    ↓
  Task C: diagrammer - Structure diagram (2-3h)

Then: Batch 2 (Content Migration) can start
```

---
  Artefacts: Agent profile, Directive 025, templates
  Agent: architect
  Blocker: None ✅

→ 2025-12-05T1016-writer-editor-release-documentation-checklist (3-4h)
  Artefacts: Release checklists
  Agent: writer-editor
  Blocker: None ✅
  Note: Can execute after 2026-01-31T0714 or in parallel with different agent

Enables:
→ Automated framework health monitoring
→ Post-install/upgrade validation
→ Upgrade guidance system
```

**Recommendation**: Execute after or in parallel with Initiative 1

---

### Initiative 3: Documentation Website Implementation (READY ✅)

**Status**: Fully unblocked, multi-batch initiative (10-14 weeks)  
**Critical Path**: Sequential batches with decision gates

```
Prerequisites (ALL COMPLETE):
✅ GitHub Pages available for repository
✅ Hugo installable (documented)
✅ Existing documentation content (HOW_TO_USE guides, ADRs)
✅ Corporate Hugo theme available for future use
✅ ADR-022 metadata strategy documented

Batch 1: Foundation & Setup (2 weeks)
→ 2026-01-31T0930-architect-docsite-foundation-setup (6-8h)
  Artefacts: Technology selection, site architecture, Hugo setup
  Agent: architect
  Blocker: None ✅
  ↓ Enables:
→ 2026-01-31T1000-build-automation-docsite-deployment-workflow (4-6h)
  Artefacts: GitHub Actions deployment
  Agent: build-automation
  Prerequisite: Batch 1 architect task complete
  ↓ Parallel with:
→ 2026-01-31T1030-writer-editor-docsite-homepage-content (6-8h)
  Artefacts: Homepage, section overviews
  Agent: writer-editor
  Prerequisite: Batch 1 architect task complete
  ↓ Parallel with:
→ 2026-01-31T1100-diagrammer-docsite-structure-diagram (2-3h)
  Artefacts: Site structure diagram
  Agent: diagrammer
  Prerequisite: Batch 1 architect task complete

→ Decision Gate 1: Proceed to Batch 2 or adjust?

Batch 2: Core Content Migration (3 weeks)
→ Migration of 19 HOW_TO_USE guides
→ Comprehensive Getting Started guide
→ Navigation and search setup
→ Contribution guide
  Prerequisite: Batch 1 complete
  Estimated: 50-70 hours across writer-editor, curator, architect

→ Decision Gate 2: Proceed to Batch 3 (user content)?

Batch 3: User Onboarding Content (2-3 weeks)
→ Tutorial series (6-8 tutorials)
→ Use cases (5-7 scenarios)
→ Troubleshooting guide
→ FAQ section
  Prerequisite: Batch 2 complete
  Estimated: 40-60 hours across writer-editor, curator

→ Decision Gate 3: Proceed to Batch 4 (advanced) or launch early?

Batch 4: Developer/Architect Content (2-3 weeks)
→ Architecture documentation
→ ADRs migration (24+ ADRs)
→ API/framework reference
→ Extension guides
→ Best practices
  Prerequisite: Batch 3 complete
  Estimated: 45-65 hours across architect, curator, writer-editor, diagrammer

→ Decision Gate 4: Ready for launch preparation?

Batch 5: Polish & Launch (1-2 weeks)
→ Corporate theme integration
→ SEO optimization
→ Analytics setup
→ Performance optimization
→ Accessibility audit
→ Launch preparation
  Prerequisite: Batch 4 complete
  Estimated: 25-40 hours across build-automation, curator, manager

Enables:
→ Professional documentation website for framework adoption
→ Improved onboarding (target: <30 min to first task)
→ Reduced support burden (target: 40% reduction in 12 months)
→ Increased community adoption and contributions
```

**Recommendation**: Execute Batch 1 immediately (architect task in inbox), monitor progress through decision gates

**Related Documentation**:
- Comprehensive Roadmap: `work/planning/documentation-website-roadmap.md`
- ADR-022: Docsite metadata strategy
- Current batch: Distribution user guides (complementary content)

---

### Initiative 4: ADR-023 Prompt Optimization (BLOCKED ❗️)

**Status**: High-value but blocked by YAML format issues  
**Critical Path**: Sequential 4-phase execution (14-22 hours total)

```
Blocker (MUST FIX FIRST):
❗️ 4 tasks have invalid YAML format (multiple document separators)
❗️ Estimated fix time: 2-3 hours
❗️ Tasks affected:
   - 2026-01-30T1120 (architect)
   - 2026-01-30T1642 (backend-dev)
   - 2026-01-30T1643 (backend-dev)
   - 2026-01-30T1644 (build-automation)

After YAML Fix:

Phase 1: Design (architect, 6-8h)
→ 2026-01-30T1120-design-prompt-optimization-framework
  Artefacts: ADR-XXX-prompt-optimization-framework.md
  Blocker: ❗️ YAML format error
  Prerequisite: Work log analysis (COMPLETED)
    ↓
    Blocks Phase 2 & 3 until ADR approved
    ↓
Phase 2a: Validator (backend-dev, 6-8h)
→ 2026-01-30T1642-adr023-phase2-prompt-validator
  Artefacts: JSON schema, validator module, tests, docs
  Blocker: ❗️ YAML format error
  Prerequisite: Phase 1 ADR design
    ↓
    Enables Phase 3 (context loader)
    ↓
Phase 2b: CI Integration (build-automation, estimated 3-4h)
→ 2026-01-30T1644-adr023-phase2-ci-workflow
  Artefacts: GitHub Actions workflow
  Blocker: ❗️ YAML format error
  Prerequisite: Phase 2a validator complete
    ↓
    Parallel with Phase 3
    ↓
Phase 3: Context Loader (backend-dev, estimated 6-8h)
→ 2026-01-30T1643-adr023-phase3-context-loader
  Artefacts: Progressive context loading, token counter
  Blocker: ❗️ YAML format error
  Prerequisite: Phase 2a validator complete

Enables:
→ 30-40% efficiency improvement
→ 30% token savings
→ 140-300 hours saved annually
```

**Recommendation**: Fix YAML issues first, then execute in 2-3 week timeframe

---

## Dependency Chains by Agent

### build-automation

**Independent Tasks** (no blocking dependencies):
- ✅ 2025-12-05T1010-release-packaging-pipeline (COMPLETED)
- ✅ 2025-12-05T1012-install-upgrade-scripts (COMPLETED)
- 2025-11-24T0954-telemetry-collection
- 2025-11-28T0426-manifest-maintenance-script
- 2025-11-28T0427-work-items-cleanup-script

**Dependent Tasks**:
```
2025-11-24T0949-security-checksum-verification
  ↓ (must complete before)
2025-11-24T0953-parallel-installation
  (optimization task depends on security being in place)

Model Router Chain:
2025-11-30T1201-model-router-config
  ↓
2025-11-30T1204-ollama-worker-pipeline
  ↓
2025-11-30T1206-ci-router-schema-validation
  ↓
2025-12-01T0512-router-metrics-dashboard

ADR-023 Chain (after YAML fix):
Phase 2a validator (backend-dev)
  ↓
❗️ 2026-01-30T1644-adr023-phase2-ci-workflow (YAML ERROR)
  (CI workflow depends on validator being complete)
```

---

### architect

**Independent Tasks**:
- 2025-11-24T0950-version-policy-documentation
- 2025-11-24T1736-framework-efficiency-assessment
- 2025-11-30T1202-model-client-interface

**Fully Unblocked**:
```
✅ Release packaging complete
  ↓
2025-12-05T1014-framework-guardian-agent-definition
  (ready for immediate execution)
```

**Blocked by YAML Format**:
```
❗️ 2026-01-30T1120-design-prompt-optimization-framework (YAML ERROR)
  ↓ (blocks entire ADR-023 initiative)
  backend-dev Phase 2a, 3
  build-automation Phase 2b

❗️ 2026-01-29T0730-mfd-task-1.3-schema-conventions (YAML ERROR)
  (part of multi-format distribution work)
```

**Dependency Note**: Framework Guardian task has no blockers but would benefit from being executed before widespread adoption (complements distribution docs).

---

### backend-dev

**Independent Tasks**:
- 2025-12-01T0510-framework-config-loader
- 2025-12-01T0511-agent-profile-parser

**Sequential ADR-023 Chain** (all blocked by YAML format):
```
❗️ Phase 1 Design (architect) - YAML ERROR
  ↓
❗️ 2026-01-30T1642-adr023-phase2-prompt-validator (YAML ERROR)
  ↓
❗️ 2026-01-30T1643-adr023-phase3-context-loader (YAML ERROR)
```

**Dependency Note**: Cannot start any ADR-023 work until:
1. YAML format fixed for all 3 tasks
2. Phase 1 (architect design) completed and ADR approved

---

### writer-editor

**Fully Unblocked** (ready now):
```
✅ Install/Upgrade scripts complete
  ↓
📬 2026-01-31T0714-distribution-user-guide (INBOX)
  (ready for immediate assignment and execution)

✅ Release packaging complete
  ↓
2025-12-05T1016-release-documentation-checklist
  (ready for execution)
```

**Low-Dependency Tasks**:
- 2025-11-25T1838-update-docs (general documentation updates)

**Follow-up Tasks** (from completed work):
- 2025-11-27T1956-followup-poc3-metrics (polish synthesis doc)
- 2025-12-04T0527-polish-feasibility-documents (polish existing docs)

**Dependency Note**: High-priority inbox task is fully unblocked. Other tasks are polish/review work with minimal dependencies.

---

### curator

**Independent Tasks** (no blocking dependencies):
- 2025-11-24T0805-changelog-clarity
- 2025-11-24T0952-maintenance-checklist-templates
- 2025-11-24T0951-tooling-best-practices-guide
- 2025-11-24T1734-locality-of-change-directive
- 2025-12-04T0528-integrate-feasibility-study-artifacts

**Dependency Note**: All curator tasks are independent. Can execute in any order based on priority.

---

### diagrammer

**Dependent on Context**:
```
Architecture/design work must be complete before diagramming
  ↓
2025-11-30T1205-multi-tier-runtime-diagram
  (depends on runtime architecture being defined)

Documentation structure must exist
  ↓
2025-12-04T0526-docsite-architecture-diagrams
  (depends on documentation site structure)
```

**Dependency Note**: Diagrammer tasks typically follow design/architecture work. Check if prerequisites exist before assigning.

---

### manager

**Coordination Tasks** (depend on work completion):
```
Tasks must be complete before review
  ↓
2025-12-04T0530-orchestrate-decision-review
  (depends on ADR-022 feasibility study artifacts being ready)
  Prerequisite: 2025-12-04T0528 (curator integration task)

Coordination across multiple tasks
  ↓
2025-11-24T0955-tooling-enhancements-coordination
  (depends on related tooling tasks progressing)
```

---

### scribe

**Independent Task**:
- 2025-11-30T1203-model-selection-template (no dependencies)

---

## Blocking Issues Analysis

### Issue 1: YAML Format Errors ❗️ (Critical Blocker)

**Impact**: Blocks entire ADR-023 initiative (high-value, 30-40% efficiency gain)

**Affected Tasks** (6 total):
1. 2026-01-30T1120-design-prompt-optimization-framework (architect)
2. 2026-01-30T1642-adr023-phase2-prompt-validator (backend-dev)
3. 2026-01-30T1643-adr023-phase3-context-loader (backend-dev)
4. 2026-01-30T1644-adr023-phase2-ci-workflow (build-automation)
5. 2026-01-29T0730-mfd-task-1.3-schema-conventions (architect)
6. 2026-01-29T0935-mfd-task-0.1-workflow-review (build-automation)

**Root Cause**: Tasks contain YAML frontmatter (---) followed by Markdown content with additional separators, creating multiple YAML documents in single file.

**Resolution Required**:
- Convert to pure YAML format with description fields containing Markdown
- OR: Extract Markdown to separate context files and reference them
- Estimated effort: 2-3 hours for all 6 files
- Test with: `python validation/validate-task-schema.py <file>`

**Priority**: HIGH - Blocks $140-300k annual ROI initiative

---

### Issue 2: Task Age / Staleness ⚠️ (Process Blocker)

**Impact**: Unclear which tasks are active vs obsolete, blocks effective prioritization

**Affected Tasks**:
- 10 tasks >60 days old (from Nov 2025)
- 12 tasks 30-60 days old (from Dec 2025)
- Total: 22 tasks needing review

**Resolution Required**:
- Stakeholder review of all tasks >60 days
- Confirm active vs obsolete status
- Archive obsolete tasks to `work/collaboration/archive/2025-11/`
- Update priorities for active tasks
- Estimated effort: 1-2 hours review meeting + 1 hour archival

**Priority**: MEDIUM - Affects queue clarity but doesn't block execution

---

### Issue 3: Unstated Dependencies ⚠️ (Risk)

**Impact**: Tasks may have implicit dependencies not captured in YAML

**Example**:
```
2025-11-24T0953-parallel-installation
  task_dependencies:
    - "Requires checksum verification task to be completed first"
    - "Should not proceed until security hardening is in place"
  
  But dependency task ID not explicitly listed!
```

**Resolution Required**:
- Review all tasks for implicit dependencies
- Add explicit `dependencies: [task-id-1, task-id-2]` fields
- Validate dependency chains are complete
- Estimated effort: 2-3 hours

**Priority**: LOW-MEDIUM - Prevents surprises but mitigable with careful review

---

## Prerequisite Artifacts

### Completed Prerequisites (Available for Use)

**Distribution System** ✅:
- `ops/release/build_release_artifact.py` (packaging)
- `ops/release/framework_install.sh` (installation)
- `ops/release/framework_upgrade.sh` (upgrade with conflict handling)
- `ops/release/distribution-config.yaml` (configuration)
- `ops/release/README.md` (documentation)
- `docs/HOW_TO_USE/framework_install.md` (technical guide)

**Testing Infrastructure** ✅:
- `validation/tests/framework_install_upgrade_tests.py` (48 tests)
- Release packaging tests (54 tests)
- All passing: 102/102 tests ✅

**Agent Framework** ✅:
- 20+ agent profiles defined
- Directives 014, 016, 017, 018, 022, 025 (in progress)
- Work orchestration system operational

**Analysis/Research** ✅:
- Work log analysis (129 logs analyzed)
- 12 suboptimal patterns identified
- ROI calculation complete (140-300 hours/year)
- Executive summary created

---

### Missing Prerequisites (Gaps)

**For ADR-023**:
- ❗️ YAML format fixes required (4 tasks)
- ⏳ Phase 1 ADR design (must complete before Phases 2-3)

**For Model Router Work**:
- ⏳ Model client interface design (2025-11-30T1202)
- ⏳ Router configuration (2025-11-30T1201)
- Status: Tasks exist but not executed

**For Multi-Format Distribution**:
- ❗️ Schema conventions task has YAML format error
- ⏳ Workflow review task has YAML format error
- Status: Blocked by data integrity issues

---

## Execution Sequence Recommendations

### Immediate (Week 1: Feb 1-7, 2026)

**Priority 1**: Execute ready, high-value work
```
Day 1:
→ Assign 2026-01-31T0714 to writer-editor (distribution user guide)

Days 2-5:
→ Execute distribution user guide (8-10h)

Optional Parallel:
→ Execute 2025-12-05T1014 (architect, Framework Guardian) (4-6h)

Days 6-7:
→ Review and validate deliverables
```

**Priority 2**: Fix blocking issues
```
Parallel with Priority 1:
→ Fix 6 YAML format errors (2-3h)
→ Review and archive obsolete tasks (1-2h)
```

**Expected Output**:
- ✅ 4 user guides delivered
- ✅ 6 YAML errors fixed
- ✅ Queue cleaned up
- ✅ Optional: Framework Guardian agent ready

---

### Short-Term (Weeks 2-3: Feb 8-21, 2026)

**Priority 3**: Execute ADR-023 Phase 1
```
Week 2:
→ Execute 2026-01-30T1120 (architect, design ADR) (6-8h)
→ Review and approve ADR

Week 3:
→ Begin Phase 2a (backend-dev, validator) (6-8h)
```

**Expected Output**:
- ✅ ADR-023 design complete and approved
- 🔄 Validator implementation in progress

---

### Medium-Term (Weeks 4-6: Feb 22 - Mar 14, 2026)

**Priority 4**: Complete ADR-023 implementation
```
Week 4:
→ Complete Phase 2a (backend-dev, validator)
→ Begin Phase 2b (build-automation, CI workflow)

Week 5:
→ Complete Phase 2b
→ Execute Phase 3 (backend-dev, context loader)

Week 6:
→ Integration testing
→ Documentation and rollout
```

**Expected Output**:
- ✅ Full prompt optimization system operational
- ✅ 30-40% efficiency improvement realized
- ✅ CI/CD integration complete

---

## Dependency Tracking Guidelines

### For Task Creators

When creating new tasks, explicitly include:

```yaml
dependencies:
  - task-id-1  # specific task that must complete first
  - task-id-2

prerequisites:
  artifacts:
    - path/to/required/file.md  # artifacts that must exist
    - path/to/another/file.js
  
  tasks_complete:
    - task-id-x  # tasks that should be done (soft dependency)
    - task-id-y

blocks:
  - task-id-future  # tasks that cannot start until this completes
```

### For Task Executors

Before starting a task:
1. Check `dependencies` field - all listed tasks must be in `done/`
2. Verify `prerequisites.artifacts` exist and are current
3. Check `prerequisites.tasks_complete` for context
4. If blocked, update task status with blocker details

### For Orchestrator

When assigning tasks:
1. Validate all dependencies are met
2. Mark tasks with unmet dependencies
3. Suggest dependency resolution order
4. Flag circular dependencies

---

## Circular Dependency Check

**Status**: ✅ No circular dependencies detected

Validation performed on:
- All 32 assigned tasks
- 7 inbox tasks
- Known dependency chains

**Method**:
- Manual inspection of task files
- Cross-reference of dependency fields
- Sequence analysis of related work

---

## Change Log

**2026-01-31**: Initial dependency map created by Planning Petra
- Mapped 3 major initiatives
- Identified 6 blocking YAML format issues
- Documented 39 task dependencies
- Created execution sequence recommendations

---

**Related Documents**:
- Status Assessment: `work/reports/2026-01-31-planning-petra-status-assessment.md`
- Next Batch Plan: `work/collaboration/NEXT_BATCH.md`
- Agent Tasks: `work/collaboration/AGENT_TASKS.md`
- Agent Status: `work/collaboration/AGENT_STATUS.md`

