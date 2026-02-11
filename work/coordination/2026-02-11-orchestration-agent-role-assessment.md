# Orchestration Agent Role Assessment

**Date:** 2026-02-11  
**Agent:** Manager Mike  
**Purpose:** Assess whether spec/review/implementation cycle orchestration fits Manager Mike's role or requires a specialized orchestration agent  
**Context:** Question from @stijn-dejongh regarding need for dedicated collaboration/orchestration agent

---

## Executive Summary

**Recommendation: Option A - Manager Mike handles orchestration (extend existing role)**

**Rationale:**
- Mike's core competencies align well with orchestration requirements
- Doctrine already provides structured support (6-Phase Cycle, Batch Planning, Task Lifecycle)
- Creating a new agent would add unnecessary complexity without clear benefit
- Gap areas (domain knowledge, tactical execution) can be addressed through supporting artifacts and delegation patterns

**Implementation:** Enhance Mike's profile with orchestration-specific guidance; create orchestration playbooks referencing existing doctrine artifacts.

---

## 1. Manager Mike's Current Role Analysis

### Core Specialization

**Primary Focus:**
- Agent selection & sequencing
- Hand-off tracking
- Workflow status mapping

**Secondary Awareness:**
- Dependency ordering
- Version alignment of context layers
- Conflict prevention

**Current Artifacts:**
- `AGENT_STATUS.md` – who did what, when, current state
- `WORKFLOW_LOG.md` – chronological log of multi-agent runs
- `HANDOFFS.md` – ready-for-next-step artefacts

### Strengths

✅ **Already a delegator** – Mike's role is explicitly about routing and coordination, not execution  
✅ **Status tracking infrastructure** – AGENT_STATUS, WORKFLOW_LOG, HANDOFFS provide foundation  
✅ **Conflict prevention focus** – Explicitly responsible for preventing conflicting edits  
✅ **Alignment validation** – "Run alignment validation before triggering downstream agent actions"  
✅ **Meta-awareness** – Has `/meta-mode` for process reflection and coordination improvements

### Current Gaps

⚠️ **Limited orchestration vocabulary** – Profile doesn't reference Batch, Iteration, Cycle concepts explicitly  
⚠️ **No cycle management guidance** – Operating procedures focus on task-by-task routing, not multi-phase workflows  
⚠️ **Tactical execution unclear** – "Trigger or request execution by named agents" is vague  
⚠️ **No reporting structure** – "Avoid verbose status reports" conflicts with orchestration reporting needs  
⚠️ **Planning boundary ambiguous** – Overlap with Planning Petra not clearly defined

---

## 2. Orchestration Requirements

### Core Responsibilities

**Spec/Review/Implementation Cycle Orchestration Needs:**

1. **Phase Sequencing** – Coordinate 6-phase spec-driven cycle (Analysis → Architecture → Planning → Acceptance Test → Implementation → Review)
2. **Agent Coordination** – Route work through multiple specialists (Analyst Annie, Architect Alphonso, Planning Petra, domain specialists, reviewers)
3. **Progress Tracking** – Monitor phase completion, handle blockers, maintain audit trail
4. **Hand-off Management** – Ensure clean transitions with complete context between phases/agents
5. **Status Reporting** – Provide human-readable summaries of cycle progress and blockers

### Domain Knowledge Required

**Orchestration-Specific Concepts (from Doctrine):**

- **Batch Planning** – Breaking work into small, time-boxed batches (1-2 weeks)
- **Six-Phase Cycle** – Structured workflow with distinct phase owners and hand-offs
- **Task Lifecycle** – new → assigned → in_progress → done → archive
- **Iteration** – Complete execution of a batch with fresh context
- **Phase Authority** – Who has PRIMARY, CONSULT, or NO authority in each phase
- **Hand-off Protocol** – Explicit context transfer between agents
- **Phase Checkpoint Protocol** – End-of-phase validation before hand-off

### Tactical Execution Patterns

**Orchestration Mechanics:**

- Create/assign tasks in `work/collaboration/inbox/`
- Move tasks through lifecycle directories (`assigned/<agent>/ → done/<agent>/`)
- Validate task YAML structure and state transitions
- Monitor work logs for completion/blockers
- Update coordination artifacts (AGENT_STATUS, WORKFLOW_LOG, HANDOFFS)
- Trigger reviews at phase gates
- Report cycle metrics to humans

---

## 3. Fit Analysis

### Pros of Mike Handling Orchestration

✅ **Core competency alignment** – Orchestration IS coordination; Mike's already a delegator  
✅ **Infrastructure exists** – AGENT_STATUS/WORKFLOW_LOG/HANDOFFS map directly to orchestration needs  
✅ **Single point of contact** – Humans interact with one agent, not multiple coordinators  
✅ **Reduces agent proliferation** – Avoids creating "yet another meta-agent"  
✅ **Natural authority** – Mike already has "Agent Assignment" responsibility per glossary  
✅ **Doctrine provides structure** – 6-Phase Cycle, Batch Planning, Task Lifecycle are well-documented approaches Mike can reference  
✅ **Delegation pattern** – Mike doesn't do the work, just orchestrates it (matches current role)

### Cons of Mike Handling Orchestration

⚠️ **Conceptual overload** – Mike's profile already spans routing, status tracking, conflict prevention; adding orchestration might dilute focus  
⚠️ **Domain knowledge gap** – Current profile lacks Batch/Iteration/Cycle vocabulary and tactical patterns  
⚠️ **Reporting tension** – "Avoid verbose status reports" conflicts with orchestration's need for cycle summaries  
⚠️ **Tactical execution clarity** – Mike's procedures are strategic (who does what); orchestration needs tactical mechanics (how to move tasks through lifecycle)  
⚠️ **Boundary with Planning Petra** – Risk of stepping on Petra's Phase 3 authority (task breakdown, dependency analysis)

---

## 4. Alternative: Specialized Orchestration Agent

### If Specialized Agent Were Created

**Hypothetical Profile: "Orchestrator Otto"**

**Purpose:** Execute multi-agent spec/review/implementation cycles following doctrine patterns (6-Phase Cycle, Batch Planning, Task Lifecycle).

**Specialization:**
- **Primary focus:** Cycle execution, phase gate management, task lifecycle transitions
- **Secondary awareness:** Phase authority boundaries, hand-off validation, reporting to humans
- **Avoid:** Strategic planning (Petra), agent routing decisions (Mike), domain implementation

**Key Differences from Manager Mike:**
- **Tactical vs. Strategic:** Otto executes cycles; Mike routes work
- **Cycle-centric vs. Task-centric:** Otto manages phases; Mike manages individual hand-offs
- **Reporting focus:** Otto provides cycle summaries; Mike provides status snapshots

### Collaboration Pattern (If Specialized Agent)

```
Human Request
    ↓
Manager Mike (Strategic Routing)
    → "This requires 6-Phase Cycle"
    → Delegate to Orchestrator Otto
        ↓
Orchestrator Otto (Tactical Execution)
    → Phase 1: Route to Analyst Annie
    → Phase 2: Route to Architect Alphonso
    → Phase 3: Route to Planning Petra
    → Phase 4-6: Coordinate specialists
    → Report cycle completion to Mike
        ↓
Manager Mike (Status Consolidation)
    → Update AGENT_STATUS.md
    → Report to Human
```

**Pros of Specialized Agent:**
- Clear separation: Mike does routing, Otto does orchestration
- Otto can develop deep expertise in cycle mechanics
- Reduces cognitive load on Mike's profile

**Cons of Specialized Agent:**
- Added complexity (two coordinators instead of one)
- Unclear handoff boundary (when does Mike delegate to Otto?)
- Risk of "too many cooks" – humans confused about who to ask for status
- Otto's specialization is narrow (only relevant for spec-driven cycles)
- Doctrine already provides orchestration guidance – new agent is just an interpreter

---

## 5. Recommendation: Option A (Manager Mike Handles Orchestration)

### Decision

**Manager Mike should handle orchestration as an extension of his existing coordination role.**

### Rationale

1. **Core competencies align:** Orchestration is coordination at a higher abstraction level; Mike's existing skills transfer directly
2. **Doctrine provides structure:** 6-Phase Cycle, Batch Planning, Task Lifecycle are well-documented; Mike references them rather than re-inventing
3. **Infrastructure exists:** AGENT_STATUS, WORKFLOW_LOG, HANDOFFS are foundation artifacts for orchestration
4. **Single point of contact:** Humans benefit from one coordinator; splitting into Mike + Otto creates confusion
5. **Gap is narrow:** Mike's current gaps (domain vocabulary, tactical patterns) can be filled with profile enhancements and playbooks
6. **Delegation pattern intact:** Mike doesn't execute cycles himself; he delegates to specialists (Petra for planning, Annie for analysis, etc.)
7. **Avoids premature complexity:** Creating Otto before orchestration patterns stabilize is premature optimization

### Trade-offs Acknowledged

**What we gain:**
- Simplicity (one coordinator, not two)
- Clear human interface (ask Mike for status)
- Leverages existing infrastructure
- Mike develops deep orchestration expertise over time

**What we accept:**
- Mike's profile becomes broader (but remains within coordination domain)
- Need to enhance Mike's profile with orchestration-specific guidance
- Tension between "lightweight coordination" and "cycle reporting" must be resolved
- Risk of Mike becoming a bottleneck (mitigated by delegation patterns)

---

## 6. Implementation Guidance

### Phase 1: Profile Enhancement (Immediate)

**Update `manager.agent.md` to include:**

1. **Orchestration Vocabulary:**
   - Add glossary references: Batch Planning, Six-Phase Cycle, Task Lifecycle, Phase Authority
   - Link to approaches: `spec-driven-6-phase-cycle.md`, `work-directory-orchestration.md`
   
2. **Orchestration-Specific Procedures:**
   ```markdown
   ### Operating Procedure: Cycle Orchestration
   
   When coordinating 6-Phase Spec-Driven Cycles:
   1. Validate specification status and phase (per Directive 035)
   2. Route to phase-appropriate agent (use Phase Authority table)
   3. Monitor for phase completion signals (task in done/, work log created)
   4. Execute Phase Checkpoint Protocol before hand-off
   5. Update AGENT_STATUS with phase transitions
   6. Report cycle progress to humans (per cycle, not per task)
   ```

3. **Reporting Clarity:**
   ```markdown
   ### Reporting Standards
   
   - **Task-level:** Minimal (AGENT_STATUS entries only)
   - **Cycle-level:** Executive summary (phases complete, blockers, next phase)
   - **Human-requested:** Full status report (all active work across all cycles)
   ```

4. **Boundary with Planning Petra:**
   ```markdown
   ### Collaboration with Planning Petra
   
   - Mike routes work and tracks status
   - Petra performs Phase 3 (Planning): task breakdown, dependency analysis, YAML creation
   - Mike does NOT create tasks or analyze dependencies; delegates to Petra
   - Handoff: Mike identifies "needs planning" → routes to Petra → Petra hands back planned batch
   ```

### Phase 2: Supporting Artifacts (Short-term)

**Create orchestration playbooks:**

1. **`doctrine/tactics/orchestrate-6-phase-cycle.tactic.md`**
   - Step-by-step tactical guide for executing spec/review/implementation cycles
   - References existing approaches (6-Phase Cycle, Work Directory Orchestration)
   - Provides Mike with concrete procedures for cycle management
   
2. **`doctrine/tactics/orchestration-status-reporting.tactic.md`**
   - Templates for cycle-level summaries
   - Metrics to track (phase durations, blockers, quality gates)
   - Balance between "lightweight" and "informative"

3. **`doctrine/shorthands/orchestration-commands.md`**
   - `/orchestrate-cycle <spec-id>` – Execute full 6-phase cycle
   - `/cycle-status <spec-id>` – Report current phase and blockers
   - `/next-phase <spec-id>` – Execute phase checkpoint and hand-off

### Phase 3: Validation (Medium-term)

**Test orchestration with real cycles:**

1. Run 2-3 complete spec-driven cycles with Mike as orchestrator
2. Document pain points and ambiguities
3. Refine profile and tactics based on learnings
4. Measure:
   - Hand-off clarity (did agents know what to do?)
   - Status visibility (could humans track progress?)
   - Cycle completion rate (how many succeeded vs. blocked?)
   - Mike's cognitive load (is this sustainable?)

**Decision gate:** After 3 cycles, reassess Option B (specialized agent) if:
- Mike becomes a bottleneck (cycles waiting for coordination)
- Orchestration expertise doesn't transfer (Mike struggles with domain knowledge)
- Humans report confusion (unclear who to ask for status)

---

## 7. Example Workflows Under Option A

### Scenario 1: Human Requests New Feature (Full Cycle)

```
Human: "Implement distribution validation for specifications"
    ↓
Manager Mike (Cycle Initiator):
    1. Recognize: This needs 6-Phase Cycle (Directive 034)
    2. Create orchestration tracking in AGENT_STATUS
    3. Phase 1: Route to Analyst Annie
        ↓
Analyst Annie (Phase 1 - Analysis):
    - Create specification stub: SPEC-DIST-001
    - Status: DRAFT
    - Hand-off note: "Ready for architectural review"
        ↓
Manager Mike (Phase Checkpoint):
    - Verify Phase 1 complete (spec exists, status=DRAFT)
    - Update AGENT_STATUS: Phase 1 ✅, Phase 2 next
    - Phase 2: Route to Architect Alphonso
        ↓
Architect Alphonso (Phase 2 - Architecture):
    - Review specification for technical feasibility
    - Update status: DRAFT → approved
    - Hand-off note: "Approved, ready for planning"
        ↓
Manager Mike (Phase Checkpoint):
    - Verify Phase 2 complete (status=approved)
    - Update AGENT_STATUS: Phase 2 ✅, Phase 3 next
    - Phase 3: Route to Planning Petra
        ↓
Planning Petra (Phase 3 - Planning):
    - Create task breakdown
    - Generate YAML task files
    - Assign DevOps Danny for Phases 4-5
    - Hand-off note: "Tasks ready in inbox/"
        ↓
Manager Mike (Phase Checkpoint):
    - Verify Phase 3 complete (YAML tasks exist)
    - Update AGENT_STATUS: Phase 3 ✅, Phase 4 next
    - Phase 4-5: Route to DevOps Danny
        ↓
DevOps Danny (Phases 4-5 - Test + Implementation):
    - Phase 4: Create acceptance tests (RED)
    - Phase 5: Implement features (GREEN)
    - Hand-off note: "Implementation complete, all tests passing"
        ↓
Manager Mike (Phase Checkpoint):
    - Verify Phases 4-5 complete (tests passing, work log exists)
    - Update AGENT_STATUS: Phases 4-5 ✅, Phase 6 next
    - Phase 6: Route to Architect Alphonso + Framework Guardian Gail
        ↓
Review Agents (Phase 6 - Review):
    - Alphonso: Architecture compliance ✅
    - Gail: Standards compliance ✅
    - Final verdict: APPROVED FOR MERGE
    - Hand-off note: "All reviews passed"
        ↓
Manager Mike (Cycle Completion):
    - Update AGENT_STATUS: Phase 6 ✅, Cycle COMPLETE
    - Update specification status: approved → IMPLEMENTED
    - Report to Human: "SPEC-DIST-001 complete, 6/6 phases passed"
```

**Mike's Role:** Route phases, validate checkpoints, report progress. Does NOT analyze, architect, plan, test, implement, or review.

### Scenario 2: Human Asks for Status

```
Human: "What's the status on specification distribution work?"
    ↓
Manager Mike (Status Reporter):
    1. Read AGENT_STATUS.md
    2. Check specification status (SPEC-DIST-001)
    3. Identify current phase (Phase 5 - Implementation)
    4. Check for blockers (none)
    5. Provide executive summary:
    
    "SPEC-DIST-001 - Distribution Validation
    
    Current Phase: 5 of 6 (Implementation)
    Agent: DevOps Danny
    Status: In Progress
    Progress: Phases 1-4 complete ✅
    Next: Phase 6 (Review) after implementation
    Blockers: None
    Estimated completion: Ready for review within 1 session"
```

**Mike's Role:** Consolidate status from AGENT_STATUS, provide human-readable summary. Does NOT dig into implementation details.

### Scenario 3: Cycle Blocked (Needs Human Decision)

```
DevOps Danny (Phase 4 - Acceptance Tests):
    - Discovers specification ambiguity
    - Cannot write tests without clarification
    - Updates task: status=blocked, reason="FR-3 unclear"
    - Notifies Mike via WORKFLOW_LOG
        ↓
Manager Mike (Blocker Handler):
    1. Detect blocker in WORKFLOW_LOG
    2. Read blocker details from task YAML
    3. Assess: Can another agent resolve? (NO - needs human domain knowledge)
    4. Escalate to Human:
    
    "⚠️ SPEC-DIST-001 blocked in Phase 4 (Acceptance Tests)
    
    Agent: DevOps Danny
    Issue: FR-3 (schema validation behavior) is ambiguous
    Question: Should validation fail silently or raise exception?
    
    Action needed: Clarify requirement so Danny can complete tests
    Impact: Phase 4-6 on hold until resolved"
        ↓
Human: "Validation should raise exception with clear error message"
    ↓
Manager Mike (Blocker Resolution):
    1. Route clarification to Analyst Annie
    2. Annie updates specification (FR-3 clarified)
    3. Notify DevOps Danny: "Blocker resolved, proceed"
    4. Update AGENT_STATUS: blocker cleared, Phase 4 resumed
```

**Mike's Role:** Detect blocker, assess resolution options, escalate to human if needed, coordinate resolution. Does NOT make domain decisions.

---

## 8. Success Criteria

**Mike successfully handles orchestration when:**

✅ **Cycles complete without manual intervention** – Mike routes phases correctly based on phase authority  
✅ **Humans can track progress** – AGENT_STATUS and cycle summaries provide clear visibility  
✅ **Blockers surface early** – Phase checkpoint protocol catches issues before hand-off  
✅ **Hand-offs are clean** – Agents receive complete context to start their phase  
✅ **No role confusion** – Mike delegates work, doesn't perform it  
✅ **Mike's cognitive load is sustainable** – Profile and tactics provide clear procedures

**Warning signs (trigger Option B reassessment):**

❗️ **Bottleneck forming** – Cycles waiting days for Mike's coordination  
❗️ **Role bleed** – Mike starts analyzing, planning, or reviewing instead of routing  
❗️ **Status confusion** – Humans can't figure out cycle progress from Mike's reports  
❗️ **Orchestration expertise not developing** – Mike repeats same mistakes across cycles

---

## 9. Metrics to Track

### Cycle-Level Metrics

- **Cycle Duration:** Time from Phase 1 start to Phase 6 completion
- **Phase Transition Time:** How long between phase completion and next phase start
- **Blocker Rate:** Percentage of cycles with at least one blocker
- **Blocker Resolution Time:** How long to clear blockers
- **Review Pass Rate:** Percentage of Phase 6 reviews that pass first time

### Coordination Metrics

- **Hand-off Clarity Score:** Agent-reported (did you have enough context to start?)
- **Mike's Time Per Cycle:** How much effort does orchestration take?
- **Status Report Frequency:** How often do humans ask for status updates?
- **Escalation Rate:** How often does Mike need to escalate to humans?

### Quality Metrics

- **Specification Conformance:** Percentage of cycles that meet all acceptance criteria
- **Cycle Success Rate:** Percentage of initiated cycles that reach IMPLEMENTED status
- **Rework Rate:** How often do cycles return to earlier phases

**Target after 10 cycles:**
- Cycle duration: <5 sessions per cycle
- Phase transition time: <1 session
- Blocker rate: <20%
- Review pass rate: >80%
- Hand-off clarity: >90% "sufficient context"

---

## 10. Related Documentation

**Doctrine References:**
- `doctrine/approaches/spec-driven-6-phase-cycle.md` – Philosophy and mental model
- `doctrine/approaches/work-directory-orchestration.md` – Task lifecycle mechanics
- `doctrine/approaches/batch-planning.md` – Batch planning approach (if exists)
- `doctrine/directives/034_spec_driven_development.md` – When to use spec-driven cycles
- `doctrine/directives/035_specification_frontmatter_standards.md` – Spec status tracking
- `doctrine/shorthands/iteration-orchestration.md` – Command aliases for orchestration

**Agent Profiles:**
- `doctrine/agents/manager.agent.md` – Manager Mike (current profile)
- `doctrine/agents/project-planner.agent.md` – Planning Petra (Phase 3 specialist)
- `doctrine/agents/analyst-annie.agent.md` – Analyst Annie (Phase 1 specialist)
- `doctrine/agents/architect.agent.md` – Architect Alphonso (Phase 2 + Phase 6 specialist)

**Glossary Terms:**
- Batch Planning
- Six-Phase Cycle
- Task Lifecycle
- Phase Authority
- Hand-off Protocol
- Phase Checkpoint Protocol
- Agent Assignment

---

## 11. Conclusion

**Manager Mike should handle orchestration.** The gap between his current role and orchestration needs is narrow and can be bridged with:

1. **Profile enhancements** – Add orchestration vocabulary, procedures, and reporting standards
2. **Supporting tactics** – Create playbooks for cycle execution and status reporting
3. **Clear boundaries** – Define collaboration with Planning Petra to prevent overlap
4. **Iterative validation** – Run real cycles, measure success, refine approach

Creating a specialized orchestration agent (Option B) would add complexity without clear benefit. The 6-Phase Cycle, Batch Planning, and Task Lifecycle patterns already exist in doctrine; Mike just needs to reference and apply them.

**Next steps:**
1. Enhance `manager.agent.md` with orchestration guidance (Phase 1 implementation)
2. Create `orchestrate-6-phase-cycle.tactic.md` playbook (Phase 2 implementation)
3. Run SPEC-DIST-001 with Mike as orchestrator (validation)
4. Collect metrics and refine approach (continuous improvement)

---

**Agent:** Manager Mike  
**Mode:** `/analysis-mode`  
**Directive 014 Compliance:** Token usage and context metrics tracked in work log  
**Status:** ✅ Assessment complete, recommendation provided

