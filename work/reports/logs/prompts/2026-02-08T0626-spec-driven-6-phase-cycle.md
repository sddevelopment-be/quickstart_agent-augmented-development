# Prompt Template: 6-Phase Specification-Driven Development Cycle

**Prompt Type:** Workflow / Process Protocol  
**Version:** 1.0.0  
**Created:** 2026-02-08  
**Author:** Analyst Annie  
**Status:** Active

**Related Directives:**
- Directive 034: Specification-Driven Development
- Directive 016: Acceptance Test-Driven Development  
- Directive 018: Traceable Decisions
- Directive 014: Work Log Creation
- Directive 015: Store Prompts

---

## Purpose

Defines the complete 6-phase specification-driven development cycle per Directive 034 and user-specified workflow, ensuring proper hand-offs between specialized agents and preventing phase-skipping violations.

---

## The 6-Phase Cycle

```
1. ANALYSIS (Analyst Annie)
   └─→ Output: Specification STUB
   └─→ Hand-off: Architect Alphonso

2. ARCHITECTURE / TECH DESIGN (Architect Alphonso)
   └─→ Output: Detailed design + approval
   └─→ Hand-off: Planning Petra

3. PLANNING (Planning Petra)
   └─→ Output: Task breakdown + YAML files
   └─→ Hand-off: Test Agent

4. ACCEPTANCE TEST IMPLEMENTATION (Assigned Agent)
   └─→ Output: Failing tests (red phase)
   └─→ Hand-off: Implementation Agent

5. CODE IMPLEMENTATION (Assigned Agent)
   └─→ Output: Passing tests (green phase)  
   └─→ Hand-off: Review Agents

6. REVIEW (Multiple Agents)
   └─→ Output: Approval OR change requests
   └─→ Hand-off: Merge (approved) OR Phase 5 (changes)
```

---

## Phase Checkpoint Protocol

**Execute at end of EVERY phase:**

```
□ Which phase am I in? [1-6]
□ Is this phase complete? [YES/NO]
□ Who owns next phase? [Agent name]
□ Do I have authority for next phase? [YES/NO]
   → If NO: Hand off immediately
□ Directives 014/015 satisfied? [YES/NO]
   → Create work log (014) + prompt doc (015) if applicable
□ Ready to hand off? [YES/NO]
   → Document outputs, notify next agent
```

---

## Role Boundaries

| Agent | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|-------|---------|---------|---------|---------|---------|---------|
| Analyst Annie | ✅ PRIMARY | ❌ Support | ❌ Support | ❌ No | ❌ No | ⚠️ AC only |
| Architect Alphonso | ⚠️ Consult | ✅ PRIMARY | ❌ No | ❌ No | ❌ No | ✅ Arch review |
| Planning Petra | ❌ No | ❌ No | ✅ PRIMARY | ❌ No | ❌ No | ❌ No |
| Implementers | ❌ No | ⚠️ Consult | ❌ No | ✅ If assigned | ✅ If assigned | ⚠️ Peer review |

✅ PRIMARY = Owns phase  
⚠️ Limited role (consult/review)  
❌ No authority

---

## SWOT Analysis (Directive 015)

**Strengths:**
- ✅ Clear phase separation prevents phase-skipping
- ✅ Explicit hand-offs leverage specialization
- ✅ Quality gates (architecture review before implementation)
- ✅ Test-first discipline (acceptance criteria defined early)
- ✅ Traceability (spec → tests → code)

**Weaknesses:**
- ⚠️ Overhead (6 phases vs. direct implementation)
- ⚠️ Latency (hand-offs add time)
- ⚠️ Requires discipline (easy to skip phases)
- ⚠️ Documentation burden (work logs per phase)

**Opportunities:**
- ✅ Process automation (phase transition validation)
- ✅ Phase tracking (add `current_phase` to YAML tasks)
- ✅ Checkpoint tooling (`/phase-check` command)
- ✅ Parallel execution (multiple features in different phases)

**Threats:**
- ⚠️ Momentum bias (agents skip phases in flow state)
- ⚠️ Role confusion (analyst vs. architect boundaries)
- ⚠️ Process fatigue (perceived overhead, shortcuts taken)
- ⚠️ Context loss (hand-offs may lose nuance)

---

## When to Use

**✅ USE for:**
- Complex features spanning multiple components
- Architectural changes requiring design review
- Cross-agent coordination needed
- High-risk areas (security, performance, data integrity)
- Features with ambiguous requirements

**❌ DO NOT USE for:**
- Simple bug fixes
- Typo corrections
- Internal utility functions
- Emergency hotfixes
- Documentation-only changes

---

## Corrective Example: SPEC-DIST-001

**What Happened (WRONG):**
1. ✅ Annie created specification → CORRECT (Phase 1)
2. ❌ Annie added detailed design → WRONG (Alphonso's job, Phase 2)
3. ❌ Annie suggested implementation → WRONG (skipped Phases 3-5)

**What Should Happen (CORRECT):**
1. ✅ Phase 1: Annie creates stub → hands to Alphonso
2. ✅ Phase 2: Alphonso evaluates, approves design
3. ✅ Phase 3: Petra breaks down tasks, creates YAML files
4. ✅ Phase 4: DevOps Danny creates validation tests (red)
5. ✅ Phase 5: DevOps Danny updates exporters (green)
6. ✅ Phase 6: Alphonso + Gail review, approve merge

---

## Related Documentation

- **Full Prompt Template:** `work/reports/logs/meta-analysis/2026-02-08T0626-spec-driven-cycle-violation.md` (complete phase descriptions)
- **Directive 034:** `doctrine/directives/034_spec_driven_development.md`
- **SDD PRIMER:** `doctrine/approaches/spec-driven-development.md`

---

**Metadata:**

**Complexity:** High (6 phases, multiple agents)  
**Estimated Time:** Days to weeks (depending on feature)  
**Token Cost:** Distributed across agents  
**Success Rate:** High (if adhered to strictly)  
**Common Failures:** Phase skipping, role confusion, momentum bias

**Tags:** `#spec-driven`, `#multi-agent`, `#quality-gates`, `#test-first`

**Version History:**
- 1.0.0 (2026-02-08): Initial prompt created after process violation

**Maintainer:** Analyst Annie  
**Review Cycle:** After 5 uses
