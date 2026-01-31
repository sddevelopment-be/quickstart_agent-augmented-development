# Agent Task Assignments

**Last Updated**: 2026-01-31 (Iteration 2 Planning)  
**Updated By**: Planning Petra  
**Purpose**: Clear mapping of which agent should work on which tasks and artefacts

---

## Iteration 2: Next Batch Assignments (5 TASKS SELECTED)

### Critical Priority: curator ⚡

**Task ID**: `2026-01-31T0900-curator-fix-yaml-format-errors`  
**Priority**: HIGH (CRITICAL - UNBLOCKS ADR-023)  
**Status**: Ready in inbox → assign immediately  
**Estimated Effort**: 2-3 hours  
**Mode**: `/analysis-mode`

**Why This Task**:
- ❗ BLOCKS $140-300k ROI initiative (ADR-023)
- Affects 6 high-value tasks across 3 agents
- Restores orchestrator health monitoring
- Mechanical task, low risk, highest strategic unblocking value

**Artefacts to Fix**:
1. `assigned/backend-dev/2026-01-30T1642-adr023-phase2-prompt-validator.yaml`
2. `assigned/backend-dev/2026-01-30T1643-adr023-phase3-context-loader.yaml`
3. `assigned/build-automation/2026-01-30T1644-adr023-phase2-ci-workflow.yaml`
4. `assigned/build-automation/2026-01-29T0935-mfd-task-0.1-workflow-review.yaml`
5. `assigned/architect/2026-01-30T1120-design-prompt-optimization-framework.yaml`
6. `assigned/architect/2026-01-29T0730-mfd-task-1.3-schema-conventions.yaml`
7. UPDATE: `work/reports/2026-01-31-yaml-format-fixes.md`

**Success Criteria**:
- All 6 files pass `python validation/validate-task-schema.py <file>`
- No information loss from original format
- Orchestrator can parse all files without errors
- System health: 🟡 → 🟢

**Dependencies**: None ✅ (immediate execution)

---

### High Priority: writer-editor ⭐

**Task ID**: `2026-01-31T0714-writer-editor-distribution-user-guide`  
**Priority**: HIGH  
**Status**: Ready in inbox → assign immediately  
**Estimated Effort**: 8-10 hours  
**Mode**: `/creative-mode`

**Why This Task**:
- Direct continuation of Iteration 1 success
- All prerequisites completed (102/102 tests passing)
- High user impact: 60% adoption friction reduction
- Completes distribution capability end-to-end

**Artefacts to Create**:
- `docs/USER_GUIDE_distribution.md` - Distribution profiles, building releases
- `docs/USER_GUIDE_installation.md` - First-time installation walkthrough
- `docs/USER_GUIDE_upgrade.md` - Upgrade workflow, conflict handling
- `docs/quickstart/GETTING_STARTED.md` - 5-minute quick start

**Context Files to Load**:
- `docs/HOW_TO_USE/framework_install.md` (technical reference, 570 lines)
- `ops/release/README.md` (build system, 300+ lines)
- `ops/release/distribution-config.yaml` (configuration)
- `work/collaboration/ITERATION_2026-01-31_SUMMARY.md` (Iteration 1 context)

**Success Criteria**:
- Conversational, user-friendly tone
- All command examples tested and working
- Non-technical team member can follow guides
- Consistent with technical documentation
- Troubleshooting sections included

**Dependencies**: ✅ All met (install/upgrade scripts completed Iteration 1)

**Validation**:
- Test every command example
- Non-technical person review for clarity
- Validate all links and cross-references

---

### High Priority: architect ⭐

**Task ID**: `2026-01-31T0930-architect-docsite-foundation-setup`  
**Priority**: HIGH (STRATEGIC INITIATIVE START)  
**Status**: Ready in inbox → assign immediately  
**Estimated Effort**: 6-8 hours  
**Mode**: `/analysis-mode`

**Why This Task**:
- Starts critical documentation website initiative (10-14 weeks total)
- No blockers or dependencies
- Creates foundation for professional framework presentation
- Generates handoff tasks for 3 agents (completes Batch 1)

**Artefacts to Create**:
- `work/analysis/docsite-technology-selection.md` - Hugo rationale
- `docs-site/ARCHITECTURE.md` - Site structure, audience mapping
- `docs-site/README.md` - Setup instructions
- `docs-site/config.toml` - Hugo configuration
- `docs-site/content/_index.md` - Homepage skeleton
- `work/planning/docsite-batch-1-implementation-plan.md` - Plan update

**Handoff Tasks to Create**:
1. `2026-01-31T1000-build-automation-docsite-deployment-workflow` (4-6h)
2. `2026-01-31T1030-writer-editor-docsite-homepage-content` (6-8h)
3. `2026-01-31T1100-diagrammer-docsite-structure-diagram` (2-3h)

**Context Files to Load**:
- `work/planning/documentation-website-roadmap.md` (full roadmap)
- `docs/architecture/adrs/ADR-022-docsite-separated-metadata.md` (metadata strategy)
- Existing HOW_TO_USE guides (content to eventually migrate)

**Success Criteria**:
- Hugo site builds without errors (`hugo` succeeds)
- Development server runs (`hugo server -D` works)
- Architecture documented with clear rationale
- Handoff tasks created with clear prerequisites
- Supports all 5 planned batches

**Dependencies**: None ✅ (immediate execution)

**Strategic Impact**:
- Enables Batch 2: Content migration (3 weeks, 50-70 hours)
- Enables Batch 3: User onboarding (2-3 weeks, 40-60 hours)
- Enables Batch 4: Developer/architect content (2-3 weeks, 45-65 hours)
- Enables Batch 5: Polish & launch (1-2 weeks, 25-40 hours)

---

### Medium Priority: architect (FOLLOW-UP)

**Task ID**: `2025-12-05T1014-architect-framework-guardian-agent-definition`  
**Priority**: MEDIUM  
**Status**: Assigned (ready for execution after Task 3 or in parallel)  
**Estimated Effort**: 4-6 hours  
**Mode**: `/analysis-mode`

**Why This Task**:
- Prerequisites completed in Iteration 1
- Natural companion to distribution work
- Enables automated health monitoring
- Can execute after primary architect task (Task 3) or in parallel if capacity

**Artefacts to Create**:
- `agents/framework-guardian.agent.md` - Agent profile
- `agents/directives/025_framework_audit_guidelines.md` - Audit directive
- Templates for framework audits (in `docs/templates/`)
- Integration points documentation

**Context Files to Load**:
- `ops/release/build_release_artifact.py` (packaging system)
- `ops/release/framework_install.sh` (install script)
- `ops/release/framework_upgrade.sh` (upgrade script)
- Existing agent profiles for pattern reference

**Success Criteria**:
- Agent profile follows established patterns
- Directive 025 provides clear, actionable guidelines
- Templates usable by non-technical users
- Integration with install/upgrade system defined

**Dependencies**: ✅ All met (packaging system complete from Iteration 1)

**Execution Strategy**: Execute after Task 3 completes (sequential) OR in parallel if architect capacity available

---

### Medium Priority: writer-editor (FOLLOW-UP)

**Task ID**: `2025-12-05T1016-writer-editor-release-documentation-checklist`  
**Priority**: MEDIUM  
**Status**: Assigned (ready for execution after Task 2 or in parallel)  
**Estimated Effort**: 3-4 hours  
**Mode**: `/creative-mode`

**Why This Task**:
- Same agent as Task 2 (natural follow-up)
- Completes release process documentation
- Low complexity, well-defined scope
- Supports release manager workflow

**Artefacts to Create**:
- Release documentation checklist (Markdown template in `ops/release/`)
- Release process documentation (integrate with existing `ops/release/`)
- Quality gates for release documentation

**Context Files to Load**:
- `ops/release/README.md` (build system docs)
- `ops/release/build_release_artifact.py` (packaging script)
- USER_GUIDE_* from Task 2 (for consistency)

**Success Criteria**:
- Checklist covers all release documentation aspects
- Integrated into existing release workflow
- Clear, actionable items
- Usable by any team member

**Dependencies**: ✅ All met (install/upgrade scripts complete from Iteration 1)

**Execution Strategy**: Execute after Task 2 completes (sequential) OR in parallel if capacity available

---

## Current Agent Queue Breakdown (Updated for Iteration 2)

### Iteration 2 Selected Agents

**curator** - Task 1 (NEW, critical)
**writer-editor** - Tasks 2, 5 (NEW + existing)
**architect** - Tasks 3, 4 (NEW + existing)

All other agents remain unchanged from previous status.

---
- Usable by any team member

**Dependencies**: ✅ All met (install/upgrade scripts complete from Iteration 1)

**Execution Strategy**: Execute after Task 2 completes (sequential) OR in parallel if capacity available

---

## Execution Summary

| Agent | Tasks | Total Hours | Priority | Timeline |
|-------|-------|-------------|----------|----------|
| **curator** | 1 | 2-3h | HIGH (critical) | Day 1 morning |
| **writer-editor** | 2 | 11-14h | HIGH + MEDIUM | Days 1-2 |
| **architect** | 2 | 10-14h | HIGH + MEDIUM | Days 1-2 |
| **Total** | **5 tasks** | **26-35h** | **Mixed** | **1-2 days** |

### Parallel Execution Strategy

**Phase 1** (Independent, parallel):
```
curator (Task 1)         → YAML Format Fixes         [2-3h]
writer-editor (Task 2)   → Distribution User Guide   [8-10h]
architect (Task 3)       → Doc Website Foundation    [6-8h]
```

**Phase 2** (Sequential or parallel):
```
architect (Task 4)       → Framework Guardian        [4-6h]  (after Task 3)
writer-editor (Task 5)   → Release Checklist         [3-4h]  (after Task 2)
```

---

## Current Agent Queue Breakdown

### build-automation (11 tasks, ~40-60 hours estimated)

**High Priority / Recently Active**:
- ✅ 2025-12-05T1010: Release packaging pipeline (COMPLETED 2026-01-31)
- ✅ 2025-12-05T1012: Install/upgrade scripts (COMPLETED 2026-01-31)

**Pending Tasks**:
1. `2025-11-24T0953-parallel-installation` - Optimize setup.sh (3-4h)
2. `2025-11-24T0954-telemetry-collection` - Add telemetry (2-3h)
3. `2025-11-25T1839-test-workflows` - Automated testing workflows (4-6h)
4. `2025-11-28T0426-manifest-maintenance-script` - Manifest automation (2-3h)
5. `2025-11-28T0427-work-items-cleanup-script` - Cleanup tooling (2-3h)
6. `2025-11-30T1201-model-router-config` - Model router configuration (3-4h)
7. `2025-11-30T1204-ollama-worker-pipeline` - Ollama integration (4-6h)
8. `2025-11-30T1206-ci-router-schema-validation` - Schema validation (2-3h)
9. `2025-12-01T0512-router-metrics-dashboard` - Metrics dashboard (4-6h)
10. `2025-12-04T0529-validation-tooling-prototype` - Validation prototype (4-6h)
11. ❗️ `2026-01-29T0935-mfd-task-0.1-workflow-review` - **YAML FORMAT ERROR** (needs fix)
12. ❗️ `2026-01-30T1644-adr023-phase2-ci-workflow` - **YAML FORMAT ERROR** (needs fix)

**Recommendation**: Hold new assignments until queue reduces or old tasks archived

---

### architect (6 tasks, ~36-48 hours estimated)

**Ready for Execution**:
1. `2025-12-05T1014-framework-guardian-agent-definition` - **RECOMMENDED** (4-6h)
2. 📬 `2026-01-31T0930-docsite-foundation-setup` - **NEW IN INBOX, HIGH PRIORITY** (6-8h)
   - Documentation website Batch 1 foundation
   - No blockers, ready to execute
   - Enables multi-batch docsite initiative

**Pending Tasks**:
3. `2025-11-24T0950-version-policy-documentation` - Version policy ADR (4-6h)
4. `2025-11-24T1736-framework-efficiency-assessment` - Efficiency analysis (6-8h)
5. `2025-11-30T1202-model-client-interface` - Model client design (4-6h)
6. ❗️ `2026-01-29T0730-mfd-task-1.3-schema-conventions` - **YAML FORMAT ERROR** (needs fix)
7. ❗️ `2026-01-30T1120-design-prompt-optimization-framework` - **YAML FORMAT ERROR** (needs fix before execution)

**Note**: Task #7 is part of high-value ADR-023 initiative but blocked by YAML issue

**Recommendation**: Execute docsite foundation task (high strategic value) or Framework Guardian (also ready)

---

### backend-dev (4 tasks, ~30-35 hours estimated)

**High-Value Tasks (Blocked)**:
1. ❗️ `2026-01-30T1642-adr023-phase2-prompt-validator` - **YAML FORMAT ERROR** (needs fix)
   - Part of ADR-023 initiative
   - Prompt validation system
   - High strategic value (30% efficiency gain)
   
2. ❗️ `2026-01-30T1643-adr023-phase3-context-loader` - **YAML FORMAT ERROR** (needs fix)
   - Part of ADR-023 initiative
   - Progressive context loading
   - Depends on task #1

**Other Pending Tasks**:
3. `2025-12-01T0510-framework-config-loader` - Config loader (4-6h)
4. `2025-12-01T0511-agent-profile-parser` - Profile parser (4-6h)

**Recommendation**: Fix YAML errors for tasks #1-2 to unblock ADR-023 initiative

---

### curator (4 tasks, ~15-20 hours estimated)

**Pending Tasks**:
1. `2025-11-24T0805-changelog-clarity` - Changelog improvements (2-3h)
2. `2025-11-24T0952-maintenance-checklist-templates` - Maintenance templates (3-4h)
3. `2025-11-24T0951-tooling-best-practices-guide` - Tooling guide (4-6h)
4. `2025-11-24T1734-locality-of-change-directive` - Directive creation (3-4h)
5. `2025-12-04T0528-integrate-feasibility-study-artifacts` - Artifact integration (3-4h)

**Artefacts**:
- Various directive documents
- Template files
- Best practices guides

**Recommendation**: Manageable queue, can accept new work if prioritized

---

### writer-editor (3 assigned + 1 inbox, ~20-25 hours estimated)

**NEXT BATCH - HIGH PRIORITY**:
1. 📬 `2026-01-31T0714-distribution-user-guide` - **RECOMMENDED** (8-10h)
   - Currently in inbox
   - See "Next Batch Assignments" section above

**Pending Tasks**:
2. `2025-11-25T1838-update-docs` - Documentation updates (3-4h)
3. `2025-11-27T1956-followup-poc3-metrics` - Metrics synthesis polish (2-3h)
4. `2025-12-04T0527-polish-feasibility-documents` - Feasibility doc polish (3-4h)
5. `2025-12-05T1016-release-documentation-checklist` - Release checklist (3-4h)

**Artefacts**:
- User guides (new)
- Documentation updates (various)
- Polish and review work

**Recommendation**: Execute high-priority inbox task first, then assess capacity

---

### diagrammer (2 tasks, ~8-12 hours estimated)

**Pending Tasks**:
1. `2025-11-30T1205-multi-tier-runtime-diagram` - Runtime architecture diagram (4-6h)
2. `2025-12-04T0526-docsite-architecture-diagrams` - Documentation site diagrams (4-6h)

**Artefacts**:
- PlantUML diagrams
- Architecture visualizations

**Recommendation**: Light load, ready for new work if needed

---

### manager (2 tasks, ~5-10 hours estimated)

**Pending Tasks**:
1. `2025-11-24T0955-tooling-enhancements-coordination` - Coordination task (2-4h)
2. `2025-12-04T0530-orchestrate-decision-review` - ADR-022 review coordination (3-6h)

**Artefacts**:
- Coordination summaries
- Decision review documents

**Recommendation**: Coordination role, light load

---

### scribe (1 task, ~2-4 hours estimated)

**Pending Task**:
1. `2025-11-30T1203-model-selection-template` - Template creation (2-4h)

**Artefact**:
- `docs/templates/model-selection-template.md`

**Recommendation**: Very light load, ready for work

---

## Inbox Tasks Awaiting Assignment (8 total)

### High Priority

1. **2026-01-31T0714-writer-editor-distribution-user-guide**
   - Agent: writer-editor
   - Priority: HIGH
   - **Recommendation**: ASSIGN IMMEDIATELY ⭐
   - See "Next Batch Assignments" above

2. **2026-01-31T0930-architect-docsite-foundation-setup** 🆕
   - Agent: architect
   - Priority: HIGH
   - Initiative: Documentation Website (Batch 1)
   - Estimated: 6-8 hours
   - **Recommendation**: ASSIGN AFTER DISTRIBUTION USER GUIDE OR IN PARALLEL
   - Deliverables: Technology selection, site architecture, Hugo setup
   - Enables: Multi-batch documentation website initiative
   - No blockers (ready to execute)
   - Creates handoff tasks for: build-automation, writer-editor, diagrammer

### Recent Handoffs (From Completed Work)

2. **2026-01-31T0638-writer-editor-followup-orchestration-guide**
   - Agent: writer-editor
   - Handoff from: curator
   - Artefact: `docs/HOW_TO_USE/multi-agent-orchestration.md`

3. **2026-01-31T0638-writer-editor-followup-metrics-synthesis**
   - Agent: writer-editor
   - Handoff from: synthesizer
   - Artefact: `docs/architecture/synthesis/poc3-orchestration-metrics-synthesis.md`

4. **2026-01-31T0638-diagrammer-followup-poc3-diagrams**
   - Agent: diagrammer
   - Handoff from: architect
   - Artefacts: PlantUML diagrams + descriptions

5. **2026-01-31T0638-synthesizer-followup-diagram-updates**
   - Agent: synthesizer
   - Handoff from: diagrammer
   - Artefact: Metrics synthesis update

6. **2026-01-31T0638-curator-followup-primer-alignment**
   - Agent: curator
   - Handoff from: curator (self-follow-up)
   - Artefacts: Aliases, directives, agent profiles

7. **2026-01-31T0638-architect-followup-testing-directives**
   - Agent: architect
   - Handoff from: curator
   - Artefacts: Testing directives rollout

### Potentially Obsolete

8. **2025-11-23T2134-curator-add-github-issue-type**
   - Agent: curator
   - Priority: NORMAL
   - ⚠️ OLD (from Nov 2025)
   - **Recommendation**: Review for relevance before assigning

---

## Task Dependencies Map

### Sequential Dependencies

**ADR-023 Prompt Optimization Initiative** (After YAML fixes):
```
1. Design Framework (architect) 
   → 2. Validator Implementation (backend-dev)
   → 3. Context Loader (backend-dev)
   → 4. CI Integration (build-automation)
```

**Framework Guardian Initiative** (Ready Now):
```
1. Agent Definition (architect) ✅ unblocked
   ↓ (parallel or sequential)
2. Documentation Checklist (writer-editor) ✅ unblocked
```

**Distribution Docs Initiative** (Ready Now):
```
Single task: User Guide Creation (writer-editor) ✅ fully unblocked
```

### Parallel Opportunities

Can execute simultaneously (no conflicts):
- writer-editor: Distribution user guide
- architect: Framework Guardian agent definition
- curator: Any maintenance task
- diagrammer: Architecture diagrams

---

## Critical Path Analysis

### To Unblock ADR-023 (High-Value Initiative)

**Blocker**: 4 tasks have invalid YAML format  
**Action Required**: Convert to pure YAML (2-3 hours)  
**Impact**: Unlocks 30-40% efficiency improvement initiative  
**Affected Tasks**:
- 2026-01-30T1120 (architect) - design
- 2026-01-30T1642 (backend-dev) - validator
- 2026-01-30T1643 (backend-dev) - context loader
- 2026-01-30T1644 (build-automation) - CI workflow

### To Execute Distribution Docs (Ready Now)

**Blocker**: None ✅  
**Action Required**: Assign task to writer-editor  
**Impact**: Enables framework adoption  
**Affected Task**: 2026-01-31T0714 (writer-editor)

### To Execute Framework Guardian (Ready Now)

**Blocker**: None ✅  
**Action Required**: Activate architect  
**Impact**: Automated framework health monitoring  
**Affected Tasks**:
- 2025-12-05T1014 (architect)
- 2025-12-05T1016 (writer-editor)

---

## Agent Availability & Execution Model

### Current Model: Manual Invocation

Observations from workflow log and agent activity patterns suggest:
- Agents do not automatically poll their queues
- Work is triggered manually by human operators
- "Last seen" timestamps indicate when orchestrator last scanned
- Actual execution requires explicit invocation

### Implications for Task Assignment

1. **Assignment ≠ Automatic Execution**
   - Moving task to `assigned/` makes it visible
   - Agent must be explicitly invoked to execute
   - Consider this when planning timelines

2. **Capacity Planning Must Include Invocation**
   - Plan who will invoke which agent when
   - Consider human operator availability
   - Batch work for efficiency

3. **Handoffs Require Coordination**
   - Follow-up tasks created automatically
   - But execution still requires manual trigger
   - Ensure handoff timing is coordinated

---

## Recommendations

### Immediate (Next 24-48 hours)

1. **Assign** `2026-01-31T0714-writer-editor-distribution-user-guide` to writer-editor
2. **Invoke** writer-editor to execute (estimated 8-10 hours)
3. **Optional**: Assign and invoke architect for Framework Guardian task (4-6 hours)

### Short-Term (Next 1-2 weeks)

4. **Fix** 6 malformed YAML task files
5. **Review** tasks >60 days old with stakeholders
6. **Archive** confirmed obsolete tasks to `archive/2025-11/`

### Medium-Term (Next 4-6 weeks)

7. **Execute** ADR-023 initiative after YAML fixes (4 tasks, sequential)
8. **Process** inbox handoff tasks (7 tasks from completed work)
9. **Establish** regular task review cadence (weekly or bi-weekly)

---

## Notes

**Agent Invocation Pattern**:
- See `.github/agents/` for agent profiles
- Agents have defined specializations and collaboration contracts
- Follow primer execution matrix per ADR-011 and Directive 010

**Work Log Requirements**:
- All completed tasks must create work log per Directive 014
- Log location: `work/reports/logs/<agent>/`
- Include metrics, challenges, lessons learned

**Quality Standards**:
- ATDD (Directive 016) and TDD (Directive 017) for code tasks
- Work logs for all tasks (Directive 014)
- Traceable decisions (Directive 018) for architecture work

---

**Related Documents**:
- Status Assessment: `work/reports/2026-01-31-planning-petra-status-assessment.md`
- Next Batch Plan: `work/collaboration/NEXT_BATCH.md`
- Agent Status: `work/collaboration/AGENT_STATUS.md`
- Dependencies: `work/collaboration/DEPENDENCIES.md`

