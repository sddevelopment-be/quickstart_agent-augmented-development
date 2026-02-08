# Tactic: Phase Checkpoint Protocol

**Type:** Procedural execution guide  
**Version:** 1.0.0  
**Created:** 2026-02-08  
**Author:** Curator Claire (validated by SPEC-DIST-001 iteration)  
**Status:** Active

**Related Directive:** [034 - Specification-Driven Development](../directives/034_spec_driven_development.md)

---

## Purpose

Prevent phase-skipping violations in specification-driven development by providing a systematic checkpoint at the end of every phase, ensuring proper hand-offs between specialized agents.

**Validated Effectiveness:** 0 violations in SPEC-DIST-001 full 6-phase cycle (2026-02-08)

---

## When to Use

**Execute this tactic:**
- At the end of EVERY phase in a 6-phase specification-driven development cycle
- When switching between specialized agents (e.g., Annie → Alphonso)
- Before committing phase deliverables
- When uncertain whether you have authority to continue

**Do NOT skip this tactic:**
- Even if "just one more small thing" (momentum bias trap)
- Even if you know the next phase well (role confusion trap)
- Even if documentation feels like overhead (directive adherence lapse trap)

---

## The Checkpoint (Execute in Order)

```
□ STEP 1: Identify Current Phase
   Which phase am I in? [1-6]
   
   1. ANALYSIS (create specification stub)
   2. ARCHITECTURE / TECH DESIGN (evaluate and approve)
   3. PLANNING (task breakdown)
   4. ACCEPTANCE TEST IMPLEMENTATION (red phase)
   5. CODE IMPLEMENTATION (green phase)
   6. REVIEW (approve or request changes)

□ STEP 2: Verify Phase Completion
   Is this phase complete? [YES/NO]
   
   → If NO: Continue work until phase deliverable ready
   → If YES: Proceed to Step 3

□ STEP 3: Identify Next Phase Owner
   Who owns the next phase? [Agent name]
   
   → Consult Role Boundaries Table in Directive 034
   → Examples:
     - Phase 1 complete → Architect Alphonso (Phase 2)
     - Phase 2 complete → Planning Petra (Phase 3)
     - Phase 3 complete → Assigned agent (Phase 4)

□ STEP 4: Check Your Authority
   Do I have authority for the next phase? [YES/NO]
   
   → Check Role Boundaries Table for your agent + next phase
   → Authority levels:
     - ✅ PRIMARY: You can proceed
     - ⚠️ CONSULT: You can advise, NOT execute
     - ❌ NO: You MUST hand off
   
   → If NO or CONSULT: Hand off immediately (do NOT continue)
   → If PRIMARY: Proceed to Step 5

□ STEP 5: Verify Directive Compliance
   Are Directives 014/015 satisfied? [YES/NO]
   
   → Directive 014 (Work Log): Required for major phase completions
   → Directive 015 (Store Prompts): Required for reusable patterns
   
   → If NO: Create required documentation before hand-off

□ STEP 6: Execute Hand-off
   Ready to hand off? [YES/NO]
   
   → Document outputs clearly
   → Notify next agent explicitly (in commit or comment)
   → Commit phase deliverables with phase declaration
   → Update specification status if applicable
```

---

## Example: Analyst Annie After Phase 1

```
□ STEP 1: Current Phase?
   ✅ Phase 1 (ANALYSIS)

□ STEP 2: Phase Complete?
   ✅ YES - Specification stub created with:
      - Problem statement
      - Requirements
      - Open questions for Alphonso

□ STEP 3: Next Phase Owner?
   ✅ Architect Alphonso (Phase 2: Architecture/Tech Design)

□ STEP 4: My Authority for Phase 2?
   ⚠️ CONSULT ONLY (per Role Boundaries Table)
   ❌ MUST HAND OFF (I cannot do architectural review)

□ STEP 5: Directives 014/015?
   ✅ Work log not required (analysis was straightforward)
   ✅ No reusable pattern created (standard spec template used)

□ STEP 6: Hand-off Execution
   ✅ Commit specification with message:
      "docs(spec): Phase 1 - create SPEC-XYZ stub
       
       Analyst Annie (Phase 1 of 6):
       Specification created, ready for architectural review.
       
       Hand-off: Architect Alphonso (Phase 2)"
```

---

## Common Violations Prevented

### Violation 1: Phase Skipping
**Symptom:** Analyst jumping Phase 1 → Phase 5 (implementation)

**How Checkpoint Prevents:**
- Step 3 identifies next owner (Alphonso, not self)
- Step 4 checks authority (❌ NO for Phase 2)
- Forces hand-off before skipping phases

---

### Violation 2: Role Overstepping
**Symptom:** Analyst doing Architect's work (trade-off analysis)

**How Checkpoint Prevents:**
- Step 4 checks authority level (⚠️ CONSULT only)
- Clear distinction: CONSULT ≠ PRIMARY
- Cannot proceed without PRIMARY authority

---

### Violation 3: Missing Documentation
**Symptom:** Skipping work logs, no prompt documentation

**How Checkpoint Prevents:**
- Step 5 explicitly checks Directives 014/015
- Forces decision: "satisfied?" [YES/NO]
- Cannot hand off until YES

---

### Violation 4: Premature Implementation
**Symptom:** Starting code before tests exist (violates ATDD)

**How Checkpoint Prevents:**
- Phase sequence enforced: 4 (tests) before 5 (code)
- Step 1 identifies current phase
- Cannot skip from Phase 3 → Phase 5

---

## Integration with Other Tools

**Ralph Wiggum Loop (Mid-Execution Self-Observation):**
- Use during long phases for continuous monitoring
- Phase Checkpoint Protocol used at phase boundaries
- Complementary, not redundant

**Commit Message Phase Declarations:**
- Step 6 (Hand-off) includes phase declaration in commit
- Makes phase progression visible in git history
- See: `doctrine/guidelines/commit-message-phase-declarations.md`

**Role Boundaries Table:**
- Referenced in Step 4 (Check Authority)
- Canonical source: Directive 034
- Each agent profile includes their specific row

---

## Validation Evidence

**Test Case:** SPEC-DIST-001 Full 6-Phase Cycle (2026-02-08)

**Before (with violation):**
- Analyst Annie skipped Phase 1 → Phase 5
- User intervention required to catch error
- Process integrity compromised

**After (with checkpoint):**
- All 6 phases executed in order
- 5 explicit hand-offs documented
- 0 phase-skipping violations
- 0 role-overstepping violations

**Metrics:**
- **Phases Completed:** 6/6
- **Hand-offs Executed:** 5/5
- **Violations Detected:** 0
- **Review Approval:** 2/2 (Alphonso + Gail)

---

## Troubleshooting

**Q: Can I skip the checkpoint for "small" phases?**  
A: No. Small phases are where violations happen (momentum bias). Always execute all 6 steps.

**Q: What if I'm uncertain about Step 4 (authority)?**  
A: Check the Role Boundaries Table in Directive 034. If still unclear, ask for clarification or hand off.

**Q: Can I execute Phase 4 and Phase 5 together?**  
A: Only if you're the same assigned agent. ATDD requires red phase (Phase 4) BEFORE green phase (Phase 5), but same agent can do both sequentially.

**Q: What if the specification changes mid-cycle?**  
A: Return to the phase where the change impacts. Example: Architecture change during Phase 5 → return to Phase 2 (Alphonso review).

---

## Related

- **Directive 034:** [Specification-Driven Development](../directives/034_spec_driven_development.md) - Defines 6-phase cycle
- **Directive 016:** [ATDD](../directives/016_acceptance_test_driven_development.md) - Phase 4-5 relationship
- **Approach:** [Ralph Wiggum Loop](../approaches/ralph-wiggum-loop.md) - Mid-execution self-observation
- **Guideline:** [Commit Message Phase Declarations](../guidelines/commit-message-phase-declarations.md) - Step 6 implementation

---

**Version:** 1.0.0  
**Status:** ✅ Active (validated)  
**Next Review:** After 5 full spec-driven cycles using this tactic  
**Changelog:**
- 2026-02-08: Initial tactic created (Curator Claire), validated by SPEC-DIST-001 iteration
