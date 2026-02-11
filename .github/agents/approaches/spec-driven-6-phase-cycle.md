# Approach: Specification-Driven Development (6-Phase Cycle)

**Type:** Mental model and workflow philosophy  
**Version:** 1.0.0  
**Created:** 2026-02-08  
**Author:** Curator Claire (validated by SPEC-DIST-001)  
**Status:** Active

**Related Directive:** [034 - Specification-Driven Development](../directives/034_spec_driven_development.md)  
**Related Tactic:** [6-Phase Implementation Flow](../tactics/6-phase-spec-driven-implementation-flow.md)  
**Related Tactic:** [Phase Checkpoint Protocol](../tactics/phase-checkpoint-protocol.md)

---

## Purpose

Explain the philosophy, rationale, and mental model behind the 6-phase specification-driven development cycle. This approach helps teams understand **why** each phase exists, **when** to use the full cycle, and **what** outcomes to expect.

**Validated:** SPEC-DIST-001 implementation (2026-02-08) - 100% specification conformance, 0 violations

**For execution checklists,** see the [6-Phase Implementation Flow Tactic](../tactics/6-phase-spec-driven-implementation-flow.md).

---

## Philosophy & Rationale

### Why Six Phases?

The 6-phase cycle emerged from observing failure modes in agent-augmented development:

1. **Phase skipping** - Agents jumping from analysis to implementation without architecture or planning
2. **Role confusion** - Analysts doing architects' work, blurring responsibilities
3. **Missing validation** - Code implemented without acceptance tests proving requirements
4. **Quality gaps** - Features merged without proper review by specialists

**Core principle:** Each phase has a **primary agent owner** with explicit hand-off protocols to prevent momentum bias and role confusion.

### The Six Phases

```
Phase 1: ANALYSIS        → Analyst Annie      → Spec stub (DRAFT)
Phase 2: ARCHITECTURE    → Architect Alphonso → Review + decision (APPROVED)
Phase 3: PLANNING        → Planning Petra     → Task breakdown
Phase 4: ACCEPTANCE TEST → Assigned agent     → Tests (RED phase)
Phase 5: IMPLEMENTATION  → Assigned agent     → Code (GREEN phase)  
Phase 6: REVIEW          → Multiple agents    → Dual approval (merge ready)
```

### Key Design Decisions

1. **Separate architecture from analysis** - Prevents analysts from making technical decisions outside their authority
2. **Planning before testing** - Task breakdown identifies all work upfront, prevents scope creep
3. **RED before GREEN** - Acceptance tests must fail first (proves they work)
4. **Dual review gates** - Architecture compliance + standards compliance both required
5. **Mandatory hand-offs** - Each phase ends with explicit hand-off to next phase owner

---

## When to Use This Approach
- Complex features requiring cross-team alignment
- Multi-component changes affecting multiple agents
- Work requiring formal architectural review
- Features with ambiguous requirements needing clarification
- High-risk or security-sensitive functionality

**Do NOT use for:**
- Simple bug fixes (use standard fix flow)
- Refactoring existing code (use refactor flow)
- One-off scripts or utilities (inline documentation sufficient)
- Chores and maintenance tasks


**Use the full 6-phase cycle for:**

---
**Decision Rule:** If [Directive 034](../directives/034_spec_driven_development.md) requires specification creation, use this approach.

**For lightweight work,** use standard fix/refactor flows instead.

---

## Detailed Phase Descriptions

**For execution checklists and step-by-step instructions,** see [6-Phase Implementation Flow Tactic](../tactics/6-phase-spec-driven-implementation-flow.md).

The following sections explain **what happens** in each phase and **why** it matters.

### Phase 1: ANALYSIS (Analyst Annie)

**Input:** User request, problem statement, or strategic goal

**Outputs:**
- Specification stub in `specifications/<category>/SPEC-<ID>-<name>.md`
- YAML frontmatter with metadata (per Directive 035)
- Problem statement and background
- Stakeholder requirements (functional + non-functional)
- Open questions for architectural review
- Edge cases and constraints identified

**Duration:** ~20-40 minutes (varies by complexity)

**Execution Steps:**
1. Bootstrap as Analyst Annie
2. Create specification stub using template
3. Document requirements with evidence
4. Identify ambiguities and edge cases
5. List open questions for Architect
6. Run [Phase Checkpoint Protocol](phase-checkpoint-protocol.md):
   - Current phase: 1 (Analysis)
   - Phase complete: YES
   - Next owner: Architect Alphonso
   - My authority for Phase 2: ⚠️ CONSULT (hand off required)
   - Directives 014/015: Check if needed
   - Hand-off: Commit with phase declaration

**Commit Template:**
```
docs(spec): Phase 1 - create SPEC-<ID> stub

Analyst Annie (Phase 1 of 6 - Analysis):

Specification stub created with:
- Problem statement and background
- Stakeholder requirements (FR-1 through FR-N)
- Non-functional requirements (NFR-1 through NFR-N)
- Open questions for architectural review

Phase: 1 of 6 (Analysis)
Specification: SPEC-<ID> v1.0.0
Agent: Analyst Annie
Status: DRAFT
Hand-off: Architect Alphonso (Phase 2)
```

**Hand-off Note:** "Specification ready for architectural review. Key questions: [list 2-3 critical questions]"

---

### Phase 2: ARCHITECTURE / TECH DESIGN (Architect Alphonso)

**Input:** SPEC-<ID> v1.0.0 (DRAFT) from Analyst Annie

**Outputs:**
- Architectural review document in `work/reports/architecture/<timestamp>-<spec-id>-review.md`
- Updated specification with status `approved` and version bump to 1.1.0
- Technical feasibility assessment (HIGH/MEDIUM/LOW)
- Risk assessment with mitigation strategies
- Architectural decision documented (or reference to ADR-XXX)
- Trade-off analysis (pros/cons of chosen approach)

**Duration:** ~10-20 minutes

**Execution Steps:**
1. Bootstrap as Architect Alphonso
2. Review specification for technical feasibility
3. Evaluate alternative approaches (trade-off analysis)
4. Assess risks and identify mitigations
5. Make architectural decision (document rationale)
6. Create architectural review document
7. Update specification status to `approved` (or `rejected` with rationale)
8. Run [Phase Checkpoint Protocol](phase-checkpoint-protocol.md):
   - Current phase: 2 (Architecture)
   - Phase complete: YES (decision made, documented)
   - Next owner: Planning Petra
   - My authority for Phase 3: ❌ NO (hand off required)
   - Directives 014/015: Check if needed
   - Hand-off: Commit with phase declaration

**Commit Template:**
```
arch(review): Phase 2 - architectural review approved

Architect Alphonso (Phase 2 of 6 - Architecture):

Architectural review completed:
✅ Technical feasibility: <HIGH/MEDIUM/LOW>
✅ Risk assessment: <LOW/MEDIUM/HIGH> (all risks mitigated)
✅ Decision: <approach chosen>

Specification updated: status DRAFT → approved, v1.0.0 → v1.1.0

Phase: 2 of 6 (Architecture/Tech Design)
Specification: SPEC-<ID> v1.1.0
Agent: Architect Alphonso
Status: APPROVED
Hand-off: Planning Petra (Phase 3)
```

**Hand-off Note:** "Architecture approved. Recommended implementation approach: [brief description]. See review document for details."

---

### Phase 3: PLANNING (Planning Petra)

**Input:** SPEC-<ID> v1.1.0 (APPROVED) from Architect Alphonso

**Outputs:**
- Task breakdown document in `work/reports/planning/<timestamp>-<spec-id>-plan.md`
- YAML task files in `work/collaboration/inbox/<timestamp>-<agent>-<task>.yaml` (one per phase)
- Dependency analysis (critical path identified)
- Agent assignments (Phase 4 and Phase 5)
- Time estimates (optional, not commitments)

**Duration:** ~10-15 minutes

**Execution Steps:**
1. Bootstrap as Planning Petra
2. Break down specification into concrete tasks (typically 5-10 tasks)
3. Identify dependencies and critical path
4. Assign agents for Phase 4 (tests) and Phase 5 (implementation)
5. Create YAML task files with clear acceptance criteria
6. Document task breakdown in planning document
7. Run [Phase Checkpoint Protocol](phase-checkpoint-protocol.md):
   - Current phase: 3 (Planning)
   - Phase complete: YES (tasks defined, agents assigned)
   - Next owner: Assigned agent (e.g., DevOps Danny)
   - My authority for Phase 4: ❌ NO (hand off required)
   - Directives 014/015: Check if needed
   - Hand-off: Commit with phase declaration

**Commit Template:**
```
plan: Phase 3 - task breakdown and YAML files

Planning Petra (Phase 3 of 6 - Planning):

Task breakdown complete:
- <N> tasks identified (<X>min estimated)
- YAML files created for Phases 4-5
- Critical path: <task-1> → <task-2> → <task-3>
- Agent assignment: <Agent Name>

Phase: 3 of 6 (Planning)
Specification: SPEC-<ID> v1.1.0
Agent: Planning Petra
Status: APPROVED
Hand-off: <Assigned Agent> (Phase 4 - Acceptance Tests)
```

**Hand-off Note:** "Task breakdown ready. YAML files in `work/collaboration/inbox/`. Critical path: [describe]."

---

### Phase 4: ACCEPTANCE TEST IMPLEMENTATION (Assigned Agent)

**Input:** 
- SPEC-<ID> v1.1.0 (APPROVED)
- Task breakdown from Planning Petra
- YAML task file: `<timestamp>-<agent>-acceptance-tests.yaml`

**Outputs:**
- Test files in `tests/` directory (unit/integration/e2e as appropriate)
- Tests MUST FAIL initially (red phase per ATDD)
- Test coverage for all functional requirements (FR-1, FR-2, etc.)
- Test documentation (comments explaining what each test validates)

**Duration:** ~20-40 minutes (varies by test complexity)

**Execution Steps:**
1. Bootstrap as assigned agent (e.g., DevOps Danny)
2. Read specification and task breakdown
3. Create test files following project conventions
4. Write tests for ALL functional requirements
5. Run tests and verify they FAIL (red phase)
6. Document why tests fail (expected behavior not yet implemented)
7. Run [Phase Checkpoint Protocol](phase-checkpoint-protocol.md):
   - Current phase: 4 (Acceptance Tests)
   - Phase complete: YES (tests failing as expected)
   - Next owner: Same agent (or different if assigned)
   - My authority for Phase 5: ✅ PRIMARY (if same agent assigned)
   - Directives 014/015: Check if needed
   - Hand-off: Commit with phase declaration

**Commit Template:**
```
test: Phase 4 - validation tests created (RED phase)

<Agent Name> (Phase 4 of 6 - Acceptance Tests):

Created validation tests:
- <test-file-1>: <N> tests for <functionality>
- <test-file-2>: <M> tests for <functionality>
- Total: <X> tests, <Y> failing (RED phase as expected)

Tests verify:
- FR-1: <requirement>
- FR-2: <requirement>
- NFR-1: <requirement>

Phase: 4 of 6 (Acceptance Test Implementation)
Specification: SPEC-<ID> v1.1.0
Agent: <Agent Name>
ATDD: Red phase confirmed ✅
Hand-off: <Agent Name> continues (Phase 5 - Implementation)
```

**Hand-off Note:** "Tests created and failing as expected (red phase). Ready for implementation."

---

### Phase 5: CODE IMPLEMENTATION (Assigned Agent)

**Input:**
- SPEC-<ID> v1.1.0 (APPROVED)
- Failing tests from Phase 4
- Task breakdown from Planning Petra
- YAML task file: `<timestamp>-<agent>-implementation.yaml`

**Outputs:**
- Implementation code in appropriate directories
- All tests passing (green phase per ATDD)
- Code following project conventions
- Inline documentation (comments where needed)
- No unrelated changes (locality of change per Directive 020)

**Duration:** ~30-60 minutes (varies by complexity)

**Execution Steps:**
1. Continue as assigned agent (or bootstrap if different)
2. Read specification, tests, and architectural review
3. Implement features to make tests pass
4. Run tests frequently (aim for green phase)
5. Verify ALL tests pass (no red tests remaining)
6. Check for unrelated changes (git diff review)
7. Run [Phase Checkpoint Protocol](phase-checkpoint-protocol.md):
   - Current phase: 5 (Implementation)
   - Phase complete: YES (all tests passing)
   - Next owner: Review agents (Alphonso, Gail, etc.)
   - My authority for Phase 6: ⚠️ PEER REVIEW (limited role)
   - Directives 014/015: Check if needed
   - Hand-off: Commit with phase declaration

**Commit Template:**
```
feat: Phase 5 - implementation complete (GREEN phase)

<Agent Name> (Phase 5 of 6 - Implementation):

Implementation complete:
- <file-1>: <changes>
- <file-2>: <changes>
- Total: <N> files modified, <M> lines changed

Test results:
✅ <X> tests passing (was <Y> failing in Phase 4)
✅ ATDD green phase achieved
✅ All functional requirements met (FR-1 through FR-N)
✅ All non-functional requirements met (NFR-1 through NFR-N)

Phase: 5 of 6 (Code Implementation)
Specification: SPEC-<ID> v1.1.0
Agent: <Agent Name>
ATDD: Green phase confirmed ✅
Hand-off: Architect Alphonso + Framework Guardian Gail (Phase 6 - Review)
```

**Hand-off Note:** "Implementation complete. All tests passing. Ready for review."

---

### Phase 6: REVIEW (Multiple Agents)

**Input:**
- SPEC-<ID> v1.1.0 (APPROVED)
- Implementation code from Phase 5
- All tests passing (green phase)

**Outputs:**
- Architecture compliance review: `work/reports/architecture/<timestamp>-<spec-id>-phase6-review.md`
- Standards compliance review: `work/reports/review/<timestamp>-<spec-id>-phase6-standards.md`
- Final verdict: APPROVED FOR MERGE or CHANGES REQUESTED
- If approved: Update specification status to `IMPLEMENTED`

**Duration:** ~10-20 minutes per reviewer

**Execution Steps:**

**6a. Architecture Compliance (Architect Alphonso):**
1. Bootstrap as Architect Alphonso
2. Verify implementation matches architectural decision
3. Check specification conformance (all requirements met)
4. Assess code quality and maintainability
5. Review risk mitigations implemented
6. Create architecture compliance review document
7. Verdict: APPROVED or CHANGES REQUESTED

**6b. Standards Compliance (Framework Guardian Gail):**
1. Bootstrap as Framework Guardian Gail
2. Verify directive compliance (016, 020, 034, etc.)
3. Check repository standards (commit messages, file structure)
4. Review code quality (error handling, documentation)
5. Verify test coverage adequate
6. Create standards compliance review document
7. Verdict: APPROVED or CHANGES REQUESTED

**6c. Final Verdict:**
- If BOTH approve: APPROVED FOR MERGE ✅
- If EITHER requests changes: Return to Phase 5 (implementation) with feedback
- Update specification status to `IMPLEMENTED` if approved

**Commit Template:**
```
review: Phase 6 - all reviews approved

Phase 6 of 6 (Review):

Architecture Review (Architect Alphonso):
✅ Architecture compliance: PASS
✅ Specification conformance: <X>/<X> requirements met
✅ Risk mitigation: All addressed

Standards Review (Framework Guardian Gail):
✅ Directive compliance: PASS (<list directives>)
✅ Code quality: <HIGH/MEDIUM/LOW>
✅ Test coverage: <X>% (<target>% required)

Final Verdict: APPROVED FOR MERGE ✅

Phase: 6 of 6 (Review)
Specification: SPEC-<ID> v1.1.0 → IMPLEMENTED
Agents: Architect Alphonso + Framework Guardian Gail
Status: READY FOR MERGE
```

**Hand-off Note:** "All reviews approved. Specification status updated to IMPLEMENTED. Ready for merge to main."

---

## Post-Iteration Activities

After Phase 6 completes (approved), perform these activities per directives:

### Directive 014: Work Log Creation

Create iteration log in `work/reports/logs/iteration/<timestamp>-<spec-id>-full-cycle.md`

**Contents:**
- Executive summary (duration, commits, test coverage, conformance)
- Phase breakdown with durations and agents
- Metrics (time, tokens, code changes, quality)
- Key decisions made
- Lessons learned
- Follow-up tasks (if any)

**Estimated time:** ~15 minutes

### Directive 015: Store Prompts (if applicable)

If reusable patterns emerged, document in `work/reports/logs/prompts/<timestamp>-<pattern-name>.md`

**Contents:**
- SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
- When to use / not use
- Template or example
- Related directives

**Estimated time:** ~10 minutes (only if reusable pattern identified)

---

## Complete Timeline Example (SPEC-DIST-001)

| Phase | Agent | Duration | Deliverable | Commit |
|-------|-------|----------|-------------|--------|
| 1 | Analyst Annie | ~20min | Spec stub (DRAFT) | `49ad1d1` |
| 2 | Architect Alphonso | ~4min | Arch review (APPROVED) | `71b6b47` |
| 3 | Planning Petra | ~3min | Task breakdown + YAML | `6fc2154` |
| 4 | DevOps Danny | ~5min | Tests created (RED) | `78b255c` |
| 5 | DevOps Danny | ~4min | Implementation (GREEN) | `0e801a0` |
| 6 | Alphonso + Gail | ~2min | Reviews (APPROVED) | `0e5b097`, `3143ae3` |
| **Total** | **6 agents** | **~38min** | **Spec IMPLEMENTED** | **5 commits** |

**Post-Iteration:**
- Work log created: `598e884`
- Curation review: `7abf13e`

**Result:** 100% specification conformance, 0 violations, APPROVED FOR MERGE ✅

---

## Tips for Success

1. **Use Phase Checkpoint Protocol:** Execute at END of every phase (prevents 80% of violations)
2. **Small, frequent commits:** One commit per phase (clear history, easy rollback)
3. **Document hand-offs explicitly:** Next agent should know exactly what to do
4. **ATDD is non-negotiable:** Red phase (Phase 4) BEFORE green phase (Phase 5)
5. **Don't skip reviews:** Phase 6 catches issues that slip through earlier phases
6. **Update specification status:** DRAFT → approved → IMPLEMENTED (traceability)
7. **Work logs are valuable:** Capture lessons learned for future iterations

---

## Troubleshooting

**Q: Can I combine phases?**  
A: No. Each phase has a distinct purpose and owner. Combining phases increases violation risk.

**Q: What if specification changes mid-cycle?**  
A: Return to the phase where change impacts. Example: Architecture change in Phase 5 → return to Phase 2 for Alphonso review.

**Q: Can I skip Phase 6 for "simple" changes?**  
A: No. Phase 6 is where spec conformance is verified. Without it, no guarantee requirements met.

**Q: What if tests can't be written before implementation?**  
A: This indicates specification ambiguity. Return to Phase 1 (analysis) or Phase 2 (architecture) to clarify requirements.

**Q: Can multiple agents work in parallel?**  
A: Yes, but only WITHIN a phase, not ACROSS phases. Example: Multiple agents can implement Phase 5 tasks concurrently if properly coordinated.

---

## Related

- **Directive 034:** [Specification-Driven Development](../directives/034_spec_driven_development.md) - Defines when to use this tactic
- **Tactic:** [Phase Checkpoint Protocol](phase-checkpoint-protocol.md) - Execute at end of every phase
- **Directive 016:** [ATDD](../directives/016_acceptance_test_driven_development.md) - Phase 4-5 relationship
- **Directive 020:** [Locality of Change](../directives/020_locality_of_change.md) - Minimize changes in Phase 5
- **Guideline:** [Commit Message Phase Declarations](../guidelines/commit-message-phase-declarations.md) - How to write phase commits

---

**Version:** 1.0.0  
**Status:** ✅ Active (validated by SPEC-DIST-001)  
**Next Review:** After 5 full iterations using this tactic  
**Changelog:**
- 2026-02-08: Initial tactic created (Curator Claire), validated by SPEC-DIST-001 iteration
