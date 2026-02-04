# Next Batch: Implementation Plan

**Batch ID**: 2026-02-04-llm-service-m2-prep (Pre-Milestone 2)  
**Created**: 2026-02-04  
**Updated**: 2026-02-04 (Post-M1 Completion)  
**Prepared By**: Planning Petra  
**Status**: 🟡 Ready for Assignment  
**Estimated Duration**: 1 day (4-6 hours + buffer)

---

## Batch Objective

Complete **pre-Milestone 2 documentation requirements** for LLM Service Layer to unblock Tool Integration work:

1. **Document tactical ADRs** (3 decisions made during M1 implementation)
2. **Review adapter interface design** (prepare for M2 Tool Integration)
3. **Plan command template security** (injection prevention strategy)

**Success Criteria**:
- 3 tactical ADRs documented (ADR-026, ADR-027, ADR-028)
- Adapter interface design reviewed and decision captured
- Security posture documented
- Milestone 2 kickoff unblocked
- 1-day buffer before M2 start

---

## Context: LLM Service Layer Milestone 1 Complete

**Achievement:** ✅ Milestone 1 (Foundation) COMPLETE
- 93% test coverage (target: 80%) ✅ EXCEEDED
- 65/65 tests passing ✅ PERFECT
- Architect Alphonso APPROVED for M2 ✅
- Production-ready foundation ✅

**Gap Identified:** 3 tactical ADRs needed to document implementation decisions made during M1:
1. ADR-026: Pydantic V2 for Schema Validation
2. ADR-027: Click for CLI Framework
3. ADR-028: Tool-Model Compatibility Validation

**Why Critical:**
- Preserves decision context for future maintainers
- Satisfies Directive 018 (Traceable Decisions)
- Unblocks Milestone 2 progression
- Required by Architect Alphonso's review recommendations
## Selected Tasks (5 Total - Priority Order)

### Task 1: ADR-026 - Pydantic V2 for Schema Validation

- **ID**: `2026-02-04T2000-architect-adr026-pydantic-v2-validation`
- **Agent**: architect (Alphonso)
- **Priority**: HIGH
- **Status**: Ready to assign
- **Estimated Effort**: 1 hour
- **Mode**: `/analysis-mode`
- **Strategic Value**: ⭐⭐⭐⭐ Preserves decision context

**Why This ADR:**
- Decision made during M1: Chose Pydantic v2 over JSON Schema, Marshmallow, attrs
- Trade-offs: Strong type integration + validation vs. learning curve + v1→v2 migration risk
- Impact: Affects validation performance, developer experience, type safety
- Required per Directive 018 (Traceable Decisions)

**Deliverables**:
1. `docs/architecture/adrs/ADR-026-pydantic-v2-validation.md`
   - Context: Configuration validation framework choice
   - Decision: Use Pydantic v2 for schema validation
   - Trade-offs: Pros (type integration, field validators) vs. Cons (learning curve, v2 breaking changes)
   - Consequences: Strong validation, Python-native, excellent DX

**Dependencies**: None (immediate execution)

**Success Criteria**:
- ADR follows standard template (Context, Decision, Status, Consequences)
- Trade-offs clearly articulated
- References LLM Service Layer prestudy
- Decision rationale preserved for future maintainers

---

### Task 2: ADR-027 - Click for CLI Framework

- **ID**: `2026-02-04T2001-architect-adr027-click-cli-framework`
- **Agent**: architect (Alphonso)
- **Priority**: HIGH
- **Status**: Ready to assign
- **Estimated Effort**: 45 minutes
- **Mode**: `/analysis-mode`
- **Strategic Value**: ⭐⭐⭐⭐ Documents CLI framework choice

**Why This ADR:**
- Decision made during M1: Chose Click over argparse, Typer, raw sys.argv
- Trade-offs: Mature ecosystem + testing vs. not type-safe by default
- Impact: Affects CLI extensibility, testing, user experience

**Deliverables**:
1. `docs/architecture/adrs/ADR-027-click-cli-framework.md`
   - Context: CLI interface framework selection
   - Decision: Use Click for CLI implementation
   - Trade-offs: Pros (mature, testable, composable) vs. Cons (not type-safe like Typer)
   - Consequences: Excellent testing support (CliRunner), subcommand composition

**Dependencies**: None (immediate execution)

**Success Criteria**:
- ADR documents Click selection rationale
- Trade-off analysis includes Typer comparison
- References cli.py implementation
- Connects to user experience goals

---

### Task 3: ADR-028 - Tool-Model Compatibility Validation

- **ID**: `2026-02-04T2002-architect-adr028-tool-model-compatibility`
- **Agent**: architect (Alphonso)
- **Priority**: MEDIUM
- **Status**: Ready to assign
- **Estimated Effort**: 1 hour
- **Mode**: `/analysis-mode`
- **Strategic Value**: ⭐⭐⭐⭐ Documents enhancement decision

**Why This ADR:**
- Decision made during M1 code review: Added by Backend-dev Benny
- Enhancement not in original prestudy
- Trade-offs: Configuration quality vs. validation complexity
- Impact: Prevents runtime errors, improves config validation

**Deliverables**:
1. `docs/architecture/adrs/ADR-028-tool-model-compatibility-validation.md`
   - Context: Configuration validation enhancement
   - Decision: Validate agent's preferred_model is supported by preferred_tool
   - Rationale: Catches misconfigurations at validation time vs. runtime
   - Consequences: Higher config quality, better error messages

**Dependencies**: None (immediate execution)

**Success Criteria**:
- ADR documents validation enhancement
- Credits Backend-dev Benny as proposer
- Explains why added (not in prestudy)
- Shows example of caught error

---

### Task 4: Adapter Interface Design Review

- **ID**: `2026-02-04T2003-architect-adapter-interface-review`
- **Agent**: architect (Alphonso)
- **Priority**: HIGH
- **Status**: Ready to assign
- **Estimated Effort**: 1 hour
- **Mode**: `/analysis-mode`
- **Strategic Value**: ⭐⭐⭐⭐⭐ Unblocks Milestone 2

**Why Critical:**
- Milestone 2 (Tool Integration) starts with adapter base interface
- Decision point: Abstract base class vs. Protocol vs. duck typing
- Impacts extensibility, testing, community contributions
- Must be decided before M2 implementation begins

**Deliverables**:
1. Design review document: `work/analysis/llm-service-adapter-interface-review.md`
   - Options: ABC vs. Protocol vs. duck typing
   - Trade-offs: Type safety, testability, extensibility
   - Recommendation: Preferred approach with rationale
2. ADR-029 draft: `docs/architecture/adrs/ADR-029-adapter-interface-design.md`
   - Decision: Adapter base interface approach
   - Context: Tool adapter extensibility strategy
   - Consequences: Affects M2 implementation, community tool additions

**Dependencies**: None (M1 complete, foundation in place)

**Success Criteria**:
- 3 options evaluated with pros/cons
- Clear recommendation with rationale
- ADR-029 ready for finalization during M2 Batch 2.1
- Unblocks M2 kickoff

---

### Task 5: Command Template Security Review

- **ID**: `2026-02-04T2004-architect-command-template-security`
- **Agent**: architect (Alphonso)
- **Priority**: MEDIUM
- **Status**: Ready to assign
- **Estimated Effort**: 30 minutes
- **Mode**: `/analysis-mode`
- **Strategic Value**: ⭐⭐⭐ Documents security posture

**Why Important:**
- Command template substitution could be injection vector
- Current mitigation: YAML is trusted configuration (not user input)
- Future risk: If YAML becomes user-editable, need safeguards

**Deliverables**:
1. Security posture document: `work/analysis/llm-service-command-template-security.md`
   - Current approach: Trusted YAML configuration
   - Risk assessment: Injection scenarios
   - Mitigation options: Whitelist placeholders, escape args, subprocess with shell=False
   - Recommendation: Security strategy for M2

**Dependencies**: None (immediate execution)

**Success Criteria**:
- Security risks identified and assessed
- Current posture documented (trusted YAML)
- Mitigation options outlined for M2
- Clear recommendation for tool adapter implementation

---

## Execution Plan

### Phase 1: ADR Documentation (Hours 0-3)

**Sequential Execution (Architect Alphonso):**
```
Task 1: ADR-026 (Pydantic V2)         [1h]   HIGH
Task 2: ADR-027 (Click CLI)           [45m]  HIGH
Task 3: ADR-028 (Tool-Model Compat)   [1h]   MEDIUM
```

**Time Estimate:** 2.75 hours (round to 3 hours)

**Immediate Actions:**
1. Assign all 3 ADR tasks to architect
2. Execute sequentially (dependencies on shared ADR template)
3. Validate ADRs follow Directive 018 format

---

### Phase 2: M2 Preparation (Hours 3-5)

**Parallel Execution (Can Start After ADRs or In Parallel):**
```
Task 4: Adapter Interface Review      [1h]   HIGH
Task 5: Security Review               [30m]  MEDIUM
```

**Time Estimate:** 1.5 hours

**Characteristics:**
- Can execute in parallel with ADRs (different artifacts)
- Task 4 is blocking for M2 kickoff (adapter design decision)
- Task 5 informs M2 implementation but not blocking

---

### Timeline Estimates

**Realistic** (Sequential Execution): 1 day
- Morning: Tasks 1-3 complete (ADRs)
- Afternoon: Tasks 4-5 complete (M2 prep)
- Buffer: 2-3 hours for review/refinement

**Optimistic** (Some Parallelization): 4-6 hours
- ADRs + Reviews can overlap if architect switches contexts
- All tasks complete same day
- No buffer needed

**Recommended:** Plan for 1 day with buffer before M2 kickoff

---

## Checkpoints & Milestones

### Checkpoint 1: ADR Completion (Hour 3)
**Check**: Tasks 1-3 (ADRs) complete  
**Expected**: 3 ADRs documented, validated, committed  
**Decision**: Proceed to M2 prep OR refine ADRs  
**Trigger**: Architect completes Task 3

### Checkpoint 2: M2 Readiness (Hour 5)
**Check**: Tasks 4-5 (M2 prep) complete  
**Expected**: 
- Adapter interface decision documented ✅
- Security posture reviewed ✅
- ADRs complete ✅
**Decision**: Approve M2 kickoff OR extend prep  
**Trigger**: All 5 tasks complete

### Checkpoint 3: M2 Kickoff Gate (Day 2)
**Check**: All deliverables reviewed, buffer day complete  
**Expected**: M2 Batch 2.1 (Adapter Base Interface) ready to assign  
**Decision**: Start Milestone 2 OR address gaps  
**Trigger**: 1-day buffer complete, human approval

---

## Resource Allocation

| Agent | Tasks | Total Hours | Complexity | Timeline |
|-------|-------|-------------|------------|----------|
| **architect** | 5 | 4.25h | LOW-MEDIUM | 1 day |
| **Total** | **5 tasks** | **4.25h** | **Low** | **1 day** |

### Agent Workload: Architect Alphonso

**Workload:** Light (4.25 hours concentrated work)
- Task 1: 1 hour (ADR-026)
- Task 2: 45 min (ADR-027)
- Task 3: 1 hour (ADR-028)
- Task 4: 1 hour (Adapter interface review)
- Task 5: 30 min (Security review)

**Characteristics:**
- All tasks same agent (sequential or contextual parallelization)
- Low complexity (documentation, not implementation)
- High strategic value (unblocks M2)
- Fits in 1 working day with buffer

---

## Risk Assessment & Mitigation

### Risk 1: ADR Documentation Scope Creep
**Description**: ADRs expand beyond tactical decision documentation  
**Probability**: LOW  
**Impact**: MEDIUM (delays M2 kickoff)  
**Mitigation**: 
- Time-box each ADR to 1 hour max
- Use standard ADR template
- Focus on decision + trade-offs, not exhaustive analysis
- Defer deep dives to design docs if needed

### Risk 2: Adapter Interface Analysis Paralysis
**Description**: Too many options, difficult to choose  
**Probability**: MEDIUM  
**Impact**: MEDIUM (delays M2)  
**Mitigation**:
- Limit to 3 options (ABC, Protocol, duck typing)
- Use lightweight spike if needed (30 min code exploration)
- Make recommendation, finalize during M2 Batch 2.1
- Don't block on perfect decision

### Risk 3: Security Review Rabbit Hole
**Description**: Security analysis becomes exhaustive threat modeling  
**Probability**: LOW  
**Impact**: LOW (not blocking M2)  
**Mitigation**:
- Time-box to 30 minutes
- Focus on current posture + M2 guidance
- Defer comprehensive security audit to post-MVP
- Document assumptions, not solutions

---

## Success Metrics

### Task-Level Metrics
- ✅ 5/5 tasks completed within 1 day
- ✅ All ADRs follow Directive 018 template
- ✅ Adapter interface decision documented
- ✅ Security posture reviewed
- ✅ M2 kickoff unblocked

### Strategic Metrics
- ✅ Decision context preserved (3 tactical ADRs)
- ✅ Milestone 2 preparation complete
- ✅ No blocking issues for M2 Tool Integration
- ✅ 1-day buffer achieved before M2 start

### Value Realization
- **Immediate**: M2 unblocked, decision context preserved
- **Short-term** (M2-M4): Clear architectural guidance for implementation
- **Long-term**: Future maintainers understand decision rationale

---

## Dependency Management

### Prerequisites (All Met ✅)

| Dependency | Status | Location | Notes |
|------------|--------|----------|-------|
| Milestone 1 Complete | ✅ | M1 foundation | 93% coverage, approved |
| Architectural Review | ✅ | Alphonso review | APPROVED, 5 recommendations |
| Prestudy Documentation | ✅ | ADR-025, prestudy | 4,400+ lines |
| Implementation Code | ✅ | src/llm_service/ | Production-ready |
| Test Suite | ✅ | tests/unit/ | 65 tests, all passing |

### Internal Dependencies (This Batch)

**No Blocking Dependencies:**
- All 5 tasks can execute in parallel (different artifacts)
- ADRs benefit from sequential execution (shared template)
- Recommended: Tasks 1-3 sequential, Tasks 4-5 parallel

---

## Handoff to Milestone 2

### Expected Outputs After This Batch

**Documentation:**
1. ✅ `docs/architecture/adrs/ADR-026-pydantic-v2-validation.md`
2. ✅ `docs/architecture/adrs/ADR-027-click-cli-framework.md`
3. ✅ `docs/architecture/adrs/ADR-028-tool-model-compatibility-validation.md`
4. ✅ `work/analysis/llm-service-adapter-interface-review.md`
5. ✅ `work/analysis/llm-service-command-template-security.md`
6. 🟡 `docs/architecture/adrs/ADR-029-adapter-interface-design.md` (DRAFT)

**M2 Readiness Checklist:**
- ✅ Tactical decisions documented
- ✅ Adapter interface approach decided
- ✅ Security posture defined
- ✅ ADR backlog cleared
- ✅ 1-day buffer complete

**Next Batch (M2 Batch 2.1):**
- Task: Implement adapter base interface (ADR-029 decision)
- Agent: Backend-dev Benny
- Estimated Effort: 2 days
- Deliverable: Base adapter architecture with command template parsing

---

## Alternative Batches

### Alternative 1: ADRs Only (Minimal Scope)

**If**: Architect has limited availability  
**Execute**: Tasks 1-3 (ADRs only)  
**Duration**: 2.75 hours  
**Value**: Decision context preserved, partial M2 unblocking

**Rationale**: ADRs are highest priority per Directive 018. M2 prep can be done during M2 Batch 2.1 if needed.

---

### Alternative 2: M2 Prep Only (Defer ADRs)

**If**: M2 kickoff is urgent  
**Execute**: Tasks 4-5 (Adapter interface + Security)  
**Duration**: 1.5 hours  
**Value**: M2 immediately unblocked

**Rationale**: ADRs can be created in parallel with M2 work. Not blocking for implementation.

**Risk**: Decision context may be lost if not documented soon.

---

## Comparison to Previous Batch

| Metric | Previous Batch | This Batch | Change |
|--------|----------------|------------|--------|
| **Tasks** | 5 (multi-initiative) | 5 (focused prep) | Same count |
| **Agents** | 3-4 (parallel) | 1 (sequential) | Simplified |
| **Total Effort** | 26-35h | 4.25h | -85% |
| **Duration** | 1-2 days | 1 day | Same |
| **Strategic** | 3 initiatives | 1 initiative (M2 prep) | Focused |
| **Complexity** | Mixed | LOW | Reduced |

**Key Insights**:
- Lighter batch (documentation vs. implementation)
- Single agent focus (no coordination overhead)
- High strategic value (unblocks M2)
- Low risk (no code changes)

---

## Sign-off

**Prepared By**: Planning Petra  
**Date**: 2026-02-04  
**Status**: 🟡 Ready for Assignment  
**Batch ID**: 2026-02-04-llm-service-m2-prep  
**Recommended Start**: Immediate (M1 complete, dependencies met)  
**Expected Completion**: 1 day (with buffer before M2)

**Next Steps**:
1. Assign Tasks 1-5 to Architect Alphonso
2. Monitor progress per checkpoint schedule
3. Review ADRs for Directive 018 compliance
4. Approve M2 kickoff after 1-day buffer
5. Prepare M2 Batch 2.1 (Adapter Base Interface)

---

**Related Documents**:
- **M1 Completion Summary:** `work/collaboration/ITERATION_2026-02-04_LLM_SERVICE_M1_SUMMARY.md`
- **Architectural Review:** `work/reports/2026-02-04-architect-alphonso-milestone1-review.md`
- **Implementation Plan:** `docs/planning/llm-service-layer-implementation-plan.md`
- **Agent Status:** `work/collaboration/AGENT_STATUS.md`
- **Prestudy:** `docs/architecture/design/llm-service-layer-prestudy.md`
