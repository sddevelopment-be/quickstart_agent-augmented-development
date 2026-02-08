# Tactic: 6-Phase Spec-Driven Implementation Flow

**Type:** Execution checklist  
**Version:** 2.0.0  
**Created:** 2026-02-08  
**Updated:** 2026-02-08 (refactored from v1.0.0)  
**Author:** Curator Claire  
**Status:** Active

**Related Directive:** [034 - Specification-Driven Development](../directives/034_spec_driven_development.md)  
**Related Approach:** [Spec-Driven 6-Phase Cycle](../approaches/spec-driven-6-phase-cycle.md) ← Read for philosophy/rationale  
**Related Tactic:** [Phase Checkpoint Protocol](phase-checkpoint-protocol.md)

---

## Purpose

Provide a lean execution checklist for the 6-phase specification-driven development cycle. Use this for step-by-step guidance during implementation.

**For philosophy, rationale, and examples,** see [Spec-Driven 6-Phase Cycle Approach](../approaches/spec-driven-6-phase-cycle.md).

---

## Quick Reference

```
Phase 1: ANALYSIS        → Analyst Annie      → Spec stub (DRAFT)
Phase 2: ARCHITECTURE    → Architect Alphonso → Review (APPROVED/REJECTED)
Phase 3: PLANNING        → Planning Petra     → Task breakdown + YAML files
Phase 4: ACCEPTANCE TEST → Assigned agent     → Tests (RED phase)
Phase 5: IMPLEMENTATION  → Assigned agent     → Code (GREEN phase)  
Phase 6: REVIEW          → Multiple agents    → Dual approval (MERGE READY)
```

---

## Phase 1: ANALYSIS (Analyst Annie)

**Input:** User request, problem statement, strategic goal

**Outputs:**
- Specification stub: `specifications/<category>/SPEC-<ID>-<name>.md`
- YAML frontmatter (per Directive 035)
- Requirements (functional + non-functional)
- Open questions for Architect

**Execution:**
1. Bootstrap as Analyst Annie
2. Create spec stub with template
3. Document requirements + constraints
4. List open questions for Phase 2
5. Run [Phase Checkpoint Protocol](phase-checkpoint-protocol.md)
6. Commit with phase declaration (see [commit guidelines](../guidelines/commit-message-phase-declarations.md))

**Hand-off:** "Spec ready for architectural review. Key questions: [list 2-3]"

**Duration:** ~20-40 minutes

---

## Phase 2: ARCHITECTURE (Architect Alphonso)

**Input:** SPEC-<ID> v1.0.0 (DRAFT)

**Outputs:**
- Architectural review: `work/reports/architecture/<timestamp>-<spec-id>-review.md`
- Updated spec: status `approved` (or `rejected`), version bump to 1.1.0
- Feasibility assessment (HIGH/MEDIUM/LOW)
- Risk assessment + mitigations
- Trade-off analysis

**Execution:**
1. Bootstrap as Architect Alphonso
2. Review spec for feasibility
3. Evaluate alternatives (trade-offs)
4. Make architectural decision
5. Create review document
6. Update spec status/version
7. Run [Phase Checkpoint Protocol](phase-checkpoint-protocol.md)
8. Commit with phase declaration

**Hand-off:** "Architecture approved. Approach: [brief description]"

**Duration:** ~10-20 minutes

---

## Phase 3: PLANNING (Planning Petra)

**Input:** SPEC-<ID> v1.1.0 (APPROVED)

**Outputs:**
- Planning document: `work/reports/planning/<timestamp>-<spec-id>-plan.md`
- Task breakdown (7-15 tasks typical)
- YAML task files: `work/tasks/backlog/<timestamp>-<task-name>.yaml`
- Agent assignments

**Execution:**
1. Bootstrap as Planning Petra
2. Decompose spec into tasks
3. Create planning document
4. Generate YAML task files (if agents needed)
5. Run [Phase Checkpoint Protocol](phase-checkpoint-protocol.md)
6. Commit with phase declaration

**Hand-off:** "Planning complete. X tasks created. Agent Y assigned Phase 4."

**Duration:** ~5-10 minutes

---

## Phase 4: ACCEPTANCE TESTS (Assigned Agent)

**Input:** SPEC-<ID> + task assignments from Phase 3

**Outputs:**
- Test file(s): `tests/integration/<area>/test_<feature>.test.js` (or equivalent)
- Tests that FAIL (RED phase - proves tests work)
- Test coverage for all acceptance criteria

**Execution:**
1. Bootstrap as assigned agent
2. Read acceptance criteria from spec
3. Create tests for all criteria
4. Run tests → verify RED phase (some/all failing)
5. Run [Phase Checkpoint Protocol](phase-checkpoint-protocol.md)
6. Commit with phase declaration

**Hand-off:** "Acceptance tests created. X/Y failing (RED phase verified)."

**Duration:** ~10-20 minutes

---

## Phase 5: IMPLEMENTATION (Assigned Agent)

**Input:** Failing tests from Phase 4

**Outputs:**
- Implementation code (feature complete)
- Tests passing (GREEN phase)
- Updated exporters/scripts/configs as needed

**Execution:**
1. Continue as assigned agent (or re-bootstrap)
2. Implement features to pass tests
3. Run tests → verify GREEN phase (all passing)
4. Verify specification conformance (100%)
5. Run [Phase Checkpoint Protocol](phase-checkpoint-protocol.md)
6. Commit with phase declaration

**Hand-off:** "Implementation complete. All tests passing (GREEN phase)."

**Duration:** ~15-30 minutes

---

## Phase 6: REVIEW (Multiple Agents)

**Input:** Complete implementation (tests passing)

**Outputs:**
- Architecture review: `work/reports/architecture/<timestamp>-<spec-id>-phase6-review.md`
- Standards review: `work/reports/review/<timestamp>-<spec-id>-phase6-standards.md`
- Both verdicts: APPROVED FOR MERGE (or CHANGES REQUESTED)

**Execution:**

### Step 1: Architecture Review (Architect Alphonso)
1. Bootstrap as Architect Alphonso
2. Review implementation vs. architectural design
3. Check specification conformance
4. Create architecture review document
5. Verdict: APPROVED or CHANGES REQUESTED
6. Commit with phase declaration

### Step 2: Standards Review (Framework Guardian or appropriate agent)
1. Bootstrap as Framework Guardian (or specialist)
2. Review standards compliance (Directive adherence, code quality)
3. Check test coverage
4. Create standards review document
5. Verdict: APPROVED or CHANGES REQUESTED
6. Run [Phase Checkpoint Protocol](phase-checkpoint-protocol.md)
7. Commit with phase declaration

**Hand-off:** "Phase 6 complete. Both reviews approved. Ready for merge."

**Duration:** ~10-15 minutes (both reviews)

---

## Post-Iteration Activities

### Directive 014: Work Log Creation
- Create iteration log: `work/reports/logs/iteration/<timestamp>-<spec-id>-full-cycle.md`
- Include: phases, duration, metrics, lessons learned
- Commit log

### Directive 015: Store Prompts (Optional)
- If new workflow created or significant learning occurred
- Document prompt with SWOT analysis
- Store in `work/reports/logs/prompts/`

---

## Checkpoint Reminders

At the **end of every phase**, run [Phase Checkpoint Protocol](phase-checkpoint-protocol.md):
1. ✅ Phase complete?
2. ✅ All outputs created?
3. ✅ My authority for next phase? (hand-off if CONSULT/NO)
4. ✅ Phase Checkpoint Protocol executed?
5. ✅ Directives 014/015 needed?
6. ✅ Committed with phase declaration?

---

## Tips

- **Read the approach first** if unfamiliar with the philosophy: [Spec-Driven 6-Phase Cycle](../approaches/spec-driven-6-phase-cycle.md)
- **Use commit phase declarations** for traceability (see [guidelines](../guidelines/commit-message-phase-declarations.md))
- **Don't skip phases** - each has a purpose (prevents violations)
- **Hand-off explicitly** - announce next agent/phase in every commit
- **Checkpoint religiously** - prevents role confusion and phase-skipping

---

## Related

- **Approach:** [Spec-Driven 6-Phase Cycle](../approaches/spec-driven-6-phase-cycle.md) - Philosophy & rationale
- **Directive:** [034 - Specification-Driven Development](../directives/034_spec_driven_development.md) - Policy
- **Tactic:** [Phase Checkpoint Protocol](phase-checkpoint-protocol.md) - Phase transition checklist
- **Guideline:** [Commit Message Phase Declarations](../guidelines/commit-message-phase-declarations.md) - Commit standards
