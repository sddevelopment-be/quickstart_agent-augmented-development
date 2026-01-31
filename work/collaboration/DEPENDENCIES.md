# Task Dependencies Map

**Last Updated**: 2026-01-31 08:57:00 UTC  
**Updated By**: Planning Petra  
**Purpose**: Explicit mapping of task dependencies, blocking relationships, and execution sequences

---

## Critical Path: High-Priority Initiatives

### Initiative 1: Distribution User Documentation (READY ✅)

**Status**: Fully unblocked, ready for immediate execution  
**Critical Path**: Single task, no dependencies

```
Prerequisites (ALL COMPLETE):
✅ Install/Upgrade Scripts (2025-12-05T1012) - COMPLETED 2026-01-31
✅ Release Packaging (2025-12-05T1010) - COMPLETED 2026-01-31
✅ Technical Documentation (docs/HOW_TO_USE/framework_install.md) - EXISTS
✅ Build System Docs (ops/release/README.md) - EXISTS
✅ Distribution Config (ops/release/distribution-config.yaml) - EXISTS

Task:
→ 2026-01-31T0714-writer-editor-distribution-user-guide (8-10h)
  Artefacts: 4 user guides
  Agent: writer-editor
  Blocker: None ✅
  
Enables:
→ Framework adoption by downstream teams
→ Reduced onboarding friction
```

**Recommendation**: Execute immediately (no blockers)

---

### Initiative 2: Framework Guardian Integration (READY ✅)

**Status**: Fully unblocked, ready for execution  
**Critical Path**: 2 parallel tasks (can execute independently)

```
Prerequisites (ALL COMPLETE):
✅ Release Packaging System (2025-12-05T1010) - COMPLETED 2026-01-31
✅ Install/Upgrade Scripts (2025-12-05T1012) - COMPLETED 2026-01-31

Tasks (Can Execute in Parallel):
→ 2025-12-05T1014-architect-framework-guardian-agent-definition (4-6h)
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

### Initiative 3: ADR-023 Prompt Optimization (BLOCKED ❗️)

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

