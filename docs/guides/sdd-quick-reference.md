# Specification-Driven Development: Quick Reference

**Purpose:** 1-page distillation of SDD principles and workflow  
**Target:** 5-minute read for agents and developers  
**Source:** Extracted from [SDD Learnings Reflection](../../work/reports/reflections/2026-02-06-specification-driven-development-learnings.md)

---

## When to Use Specifications

**Decision Tree:**

```
Is this an architectural decision (tech choice)?
  YES → Create ADR in docs/architecture/adrs/
  NO ↓

Is this simple with obvious requirements?
  YES → Write acceptance tests directly (tests/acceptance/)
  NO ↓

Does this feature have:
  • Multiple personas with different needs?
  • Complex scenarios with edge cases?
  • Cross-team coordination required?
  • Security/performance constraints?
  YES → Create SPECIFICATION (specifications/features/)
  
Still uncertain? → Ask Architect Alphonso or Planning Petra
```

**Rule of Thumb:** If you can write acceptance tests without ambiguity, skip the spec.

---

## The Three Pillars of Documentation

| Document Type | Purpose | When | Lifecycle |
|--------------|---------|------|-----------|
| **Specifications** | Define WHAT to build | Complex features, multi-persona alignment | Living → Frozen |
| **Acceptance Tests** | Define HOW to verify | All user-facing functionality | Fail → Pass → Frozen |
| **ADRs** | Record WHY decisions made | Technology choices, architectural patterns | Immutable |

**Key Insight:** Don't conflate them! Each serves a different purpose.

---

## The Proper SDD Workflow

```
1. SPECIFICATION CREATION
   └─ Define functional requirements (WHAT)
   └─ Write scenarios (Given/When/Then)
   └─ Identify personas (WHO needs this)
   └─ Prioritize with MoSCoW (MUST/SHOULD/COULD/WON'T)

2. ACCEPTANCE TEST GENERATION
   └─ Convert spec scenarios to Gherkin tests
   └─ Ensure test coverage for all requirements
   └─ Link tests back to spec (FR-M1, FR-S2, etc.)

3. IMPLEMENTATION TASK CREATION
   └─ Create YAML tasks referencing spec
   └─ Add acceptance criteria from spec
   └─ Ensure traceability

4. IMPLEMENTATION
   └─ Build feature following spec
   └─ Make acceptance tests pass (RED → GREEN)
   └─ Update spec if constraints discovered
```

---

## Anti-Patterns to Avoid

### ❌ 1. Implementation-First Approach

**Symptom:** Creating implementation tasks before defining requirements

**Problem:** No clear acceptance criteria, weak traceability, solving wrong problem

**Fix:** Specification → Tests → Tasks → Implementation

---

### ❌ 2. Confusing Specifications with ADRs

**Symptom:** Including architectural trade-offs in functional specs

**Problem:** Mixing "what" (behavior) with "why" (technical decisions)

**Fix:**
- Specs = Functional behavior (what system does)
- ADRs = Architectural decisions (technology choices)
- Keep them separate, cross-reference when needed

---

### ❌ 3. Mandatory Specs for Everything

**Symptom:** Creating 15-page specifications for trivial features

**Problem:** Documentation debt, slowed velocity, over-engineering

**Fix:** Match rigor to complexity (see decision tree above)

---

## MoSCoW Prioritization

Label requirements by criticality:

**MUST Have** - Critical, feature unusable without
- Example: `FR-M1: System MUST accept WebSocket connections`
- Without this: Feature completely broken

**SHOULD Have** - Important, feature degraded without
- Example: `FR-S1: System SHOULD reconnect automatically on disconnect`
- Without this: Manual refresh required (workaround exists)

**COULD Have** - Nice to have, enhances experience
- Example: `FR-C1: System COULD display connection latency`
- Without this: Minor inconvenience, not critical

**WON'T Have** - Explicitly out of scope
- Example: `FR-W1: Multi-user authentication`
- Reason: Deferred to Phase 2

---

## Specification Template (Minimal)

```markdown
# Specification: [Feature Name]

**Status:** Draft | Review | Approved | Implemented  
**Target Personas:** [From docs/audience/]

## User Story

As a [persona],
I want to [action],
So that [benefit].

## MUST Requirements

FR-M1: System MUST [requirement]
- Rationale: [why this matters]
- Success Criteria: [how to verify]
- Test: [reference to test file]

## SHOULD Requirements

FR-S1: System SHOULD [requirement]
- Rationale: [why this matters]
- Workaround: [if not implemented]

## Scenarios

### Scenario 1: [Happy Path]
Given [context]
When [action]
Then [outcome]

### Scenario 2: [Error Case]
Given [error context]
When [action]
Then [error handling]

## Related Decisions

- ADR-028: [Technology Choice]
- ADR-032: [Architecture Pattern]
```

---

## Traceability Chain

Every artifact should link to requirements:

```
Strategic Goal (WHY)
    ↓
Specification (WHAT)
    ↓
Acceptance Tests (HOW to verify)
    ↓
ADRs (WHY technical choices)
    ↓
Implementation (HOW built)
    ↓
Work Logs (WHAT happened)
```

**Bidirectional:** Requirements → Code AND Code → Requirements

---

## Quick Commands

**Create spec from template:**
```bash
cp docs/templates/specifications/feature-spec-template.md \
   specifications/features/my-feature.md
```

**Link spec to tests:**
```python
"""
Verifies FR-M1 from specifications/features/my-feature.md
"""
def test_requirement():
    # Given: [context]
    # When: [action]
    # Then: [outcome]
    assert result == expected
```

**Reference ADR in spec:**
```markdown
## Technical Constraints
- Architecture: See [ADR-028: WebSocket Technology](../docs/architecture/adrs/028-websocket-technology.md)
```

---

## Key Principles

1. **Specifications describe behavior, not code structure**
2. **Write specs for humans, not just agents**
3. **Living documents: update as you learn, freeze when done**
4. **Traceability: every line of code traces to a requirement**
5. **Persona-driven: always know WHO needs this and WHY**

---

## Common Mistakes

**Mistake:** "This is too simple for a spec"  
**Reality:** If you can't write unambiguous tests without clarification, you need a spec.

**Mistake:** "I'll document it after implementation"  
**Reality:** By then, you've forgotten the rationale and edge cases.

**Mistake:** "The spec is complete, no need to update"  
**Reality:** Specs are living documents; update when constraints discovered.

---

## Related Resources

**Deep Dives:**
- [SDD Learnings Reflection](../../work/reports/reflections/2026-02-06-specification-driven-development-learnings.md) - Real-world lessons (15 min read)
- [Directive 034: Specification-Driven Development](../../doctrine/directives/034_spec_driven_development.md) - Formal directive
- [Traceability Chain Pattern](../../doctrine/approaches/traceability-chain-pattern.md) - Bidirectional linking

**Templates:**
- [Feature Spec Template](../templates/specifications/feature-spec-template.md) - Full template with examples
- [API Spec Template](../templates/specifications/api-spec-template.md) - For API contracts

**Related:**
- [Directive 016: ATDD](../../doctrine/directives/016_acceptance_test_driven_dev.md) - Test-first development
- [Directive 018: Traceable Decisions](../../doctrine/directives/018_traceable_decisions.md) - ADR practices

---

**Target Read Time:** 5 minutes  
**Maintained by:** Architect Alphonso, Curator Claire  
**Version:** 1.0.0  
**Last Updated:** 2026-02-08  
**Status:** ✅ Active
