---
name: "spec-create"
description: "Create functional specification for complex features: detailed requirements, user scenarios, constraints, acceptance criteria. Bridges strategic intent and implementation with MoSCoW prioritization and Given/When/Then scenarios."
version: "1.0.0"
type: "specification"
category: "documentation"
---

# Spec Create: Specification-Driven Development

Create comprehensive functional specifications for complex features before implementation. Specifications translate requirements into concrete implementation guidance while remaining independent of specific acceptance tests or architectural decisions.

## Instructions

Initialize as **Scribe Sally** or **Analyst Annie** to create a specification.

1. **Identify scope:**
   - Feature name and purpose
   - Target personas (see `docs/audience/`)
   - Related ADRs or design documents

2. **Gather requirements:**
   - Functional requirements (MUST/SHOULD/COULD/WON'T)
   - Non-functional requirements (performance, security, usability)
   - Business rules and constraints
   - Edge cases and error scenarios

3. **Write specification using template:**

```markdown
# Specification: [Feature Name]

**Status:** Draft
**Created:** YYYY-MM-DD
**Author:** [Agent Name]
**Stakeholders:** [Who needs to review/approve]
**Target Personas:** [List from docs/audience/]

---

## User Story

**As a** [persona]
**I want** [capability]
**So that** [benefit]

**Alternative: Acceptance Criterion Format**
**Given** [context]
**When** [action]
**Then** [outcome]
**Unless** [exception]

---

## Overview

Brief description of the feature (2-3 paragraphs):
- What problem does this solve?
- Why is it needed now?
- What constraints exist?

**Related Documentation:**
- Related ADRs: [links]
- Related Specifications: [links]
- Background: [context documents]

---

## Functional Requirements (MoSCoW)

### MUST Have (Critical - Feature unusable without these)

**FR-M1:** System MUST [requirement]
- **Rationale:** [Why this is critical]
- **Personas Affected:** [Primary users]
- **Success Criteria:** [How to verify]

**FR-M2:** System MUST [requirement]
...

### SHOULD Have (Important - Feature degraded without these)

**FR-S1:** System SHOULD [requirement]
- **Rationale:** [Why important]
- **Workaround if omitted:** [Alternative approach]

### COULD Have (Nice to have - Enhances experience)

**FR-C1:** System COULD [requirement]
- **Rationale:** [Why beneficial]
- **If omitted:** [Impact on users]

### WON'T Have (Explicitly out of scope)

**FR-W1:** [Feature/capability]
- **Rationale:** [Why excluded]
- **Future Consideration:** [When to revisit]

---

## Scenarios and Behavior

### Scenario 1: [Happy Path Name]

**Context:** [When this applies]

**Given:** [Initial state]
**And:** [Additional context]
**When:** [User action]
**And:** [Additional actions]
**Then:** [Expected outcome]
**And:** [Additional outcomes]

**Personas:** [Who this applies to]
**Priority:** MUST | SHOULD | COULD

---

### Scenario 2: [Error Case Name]

**Context:** [When this applies]

**Given:** [Initial state with error condition]
**When:** [User action]
**Then:** [Error handling outcome]
**And:** [System state after error]

**Personas:** [Who encounters this]
**Priority:** MUST | SHOULD

---

## Constraints and Business Rules

### Business Rules

**BR1:** [Rule statement]
- **Applies to:** [Which scenarios]
- **Enforcement:** [How validated]

**BR2:** [Rule statement]
...

### Technical Constraints

**TC1:** [Constraint description]
- **Measurement:** [How to verify]
- **Rationale:** [Why this constraint exists]

### Non-Functional Requirements (MoSCoW)

**NFR-M1 (MUST):** [Requirement]
- **Example:** [Concrete example]
- **Measurement:** [Metrics]
- **Verification:** [Testing approach]

---

## Open Questions

### Unresolved Requirements

- [ ] **Q1:** [Question about requirements]
  - **Assigned to:** [Who will answer]
  - **Target Date:** [When needed]
  - **Blocking:** [What can't proceed without answer]

### Design Decisions Needed

- [ ] **D1:** [Decision point]
  - **Options:** (A) ..., (B) ..., (C) ...
  - **Decision Maker:** [Who decides]
  - **Context:** [Why decision needed]

### Clarifications Required

- [ ] **C1:** [What needs clarification]
  - **Who to ask:** [Stakeholder]
  - **Why it matters:** [Impact on implementation]

---

## Out of Scope

**Explicitly NOT included in this specification:**

1. **[Feature/capability]**
   - **Reason:** [Why excluded]
   - **Future:** [When/if to consider]

---

## Acceptance Criteria Summary

**This feature is DONE when:**

- [ ] All MUST requirements (FR-M*) implemented and verified
- [ ] All SHOULD requirements (FR-S*) implemented OR documented workarounds exist
- [ ] All MUST scenarios pass acceptance tests
- [ ] All business rules (BR*) enforced in code
- [ ] All technical constraints (TC*) met and verified
- [ ] Open questions resolved or documented for future iterations
- [ ] Acceptance tests derived from scenarios are passing
- [ ] Documentation updated
- [ ] Target personas have validated feature meets their needs

---

## Traceability

### Derives From (Strategic)
- **Strategic Goal:** [High-level objective]
- **User Need:** [Problem being solved]
- **Related ADRs:** [Architecture decisions]

### Feeds Into (Tactical)
- **Acceptance Tests:** [Test files/scenarios]
- **Implementation Tasks:** [Task IDs or files]
- **API Documentation:** [API specs or contracts]

### Related Specifications
- **Dependencies:** [Specs that must be complete first]
- **Dependents:** [Specs that depend on this one]
- **Cross-References:** [Related features]

---

## Approval

### Reviewers

| Role | Name | Date | Status | Comments |
|------|------|------|--------|----------|
| Implementer | [Agent] | - | ⏳ Pending | - |
| Architect | Alphonso | - | ⏳ Pending | - |
| Target Persona | [Name] | - | ⏳ Pending | - |
| Stakeholder | [Name] | - | ⏳ Pending | - |

### Sign-Off

**Final Approval:**
- **Date:** [When approved]
- **Approved By:** [Authority]
- **Status:** Draft | Approved | Implemented

---

## Metadata

**Tags:** `#feature-spec` `#[domain]` `#[milestone]`

**Related Files:**
- Template: `docs/templates/specifications/feature-spec-template.md`
- Persona: [Links to persona documents]
- ADR: [Links to relevant ADRs]
- Tests: [Links to test files]

**Navigation:**
- Previous Spec: [Link]
- Next Spec: [Link]
- Parent Spec: [Link if hierarchical]
```

4. **Location:**
   - Save in `specifications/[domain]/[feature-name].md`
   - Create domain directory if needed

5. **Review cycle:**
   - Draft: Initial creation
   - Review: Stakeholder feedback
   - Approved: Ready for implementation
   - Implemented: Feature complete, spec frozen

## When to Create Specifications

### Create Spec For ✅

- Complex features spanning multiple components
- Features requiring cross-team coordination
- API contracts needing stakeholder agreement
- Features with security or performance constraints
- Workflows requiring step-by-step definition
- Features with multiple personas

### Skip Spec For ❌

- Simple CRUD operations (use acceptance tests directly)
- Bug fixes (use directive 028: test-first bug fixing)
- Architectural decisions (use ADRs instead)
- Internal utilities (document in code)

## Spec vs. ADR vs. Acceptance Test

| Document Type | Purpose | When | Lifecycle |
|---------------|---------|------|-----------|
| **Specification** | Detailed functional requirements | Complex features | Living (evolves during dev) |
| **ADR** (Directive 018) | Architectural decision rationale | Significant tech choices | Immutable once accepted |
| **Acceptance Test** (Directive 016) | Executable behavioral contract | All user-facing features | Frozen once passing |

**Use all three together:**
1. **Spec** defines WHAT to build (requirements, scenarios)
2. **ADR** explains HOW technical choices were made (architecture)
3. **Acceptance Tests** verify DONE (executable scenarios)

## Example Usage

```
User: We need to implement a real-time execution dashboard for the LLM service

Agent (Scribe Sally): Creating specification...

1. Identified scope:
   - Feature: Real-Time Execution Dashboard
   - Personas: Software Engineer (primary), Cost-Conscious Developer
   - Related ADRs: ADR-032 (dashboard architecture)

2. Gathered requirements:
   - MUST: Real-time task updates via WebSocket (<100ms latency)
   - MUST: Cost tracking (today/month/total)
   - MUST: File-based task tracking (preserve Git audit trail)
   - SHOULD: Metrics visualization (charts)
   - COULD: Task filtering by agent

3. Created specification:
   - Location: specifications/llm-dashboard/real-time-execution-dashboard.md
   - Format: MoSCoW requirements (8 MUST, 5 SHOULD, 4 COULD, 4 WON'T)
   - Scenarios: 6 scenarios (4 happy path, 2 error cases)
   - Constraints: WebSocket latency <100ms, localhost-only
   - Traceability: Links to ADR-032, telemetry API, task files

4. Status: DRAFT → awaiting stakeholder review

Next steps:
- Review with Human-in-Charge (stakeholder)
- Architect review (ADR alignment check)
- Approve and mark ready for implementation
- Derive acceptance tests from scenarios
```

## Integration with Workflow

**Before Implementation:**
```
1. /spec-create    ← Create specification
2. Review with stakeholders
3. Architect review (ADR alignment)
4. Approve specification
5. /iterate        ← Implement using spec as guide
```

**During Implementation:**
```
- Refer to spec for requirements
- Update spec if understanding evolves
- Derive acceptance tests from scenarios
- Link implementation tasks to spec sections
```

**After Implementation:**
```
- Mark spec status: Implemented
- Freeze spec (becomes reference doc)
- Archive in specifications/ directory
```

## Related Skills

- `/iterate` - Implement features defined in specifications
- `/review` - Architect reviews spec for ADR alignment
- `architect-adr` - Create ADR for architectural decisions
- `target-audience-fit` - Validate spec addresses target personas

## References

- **Directive 034:** `.github/agents/directives/034_spec_driven_development.md`
- **Approach:** `.github/agents/approaches/spec-driven-development.md`
- **Template:** `docs/templates/specifications/feature-spec-template.md`
- **Directive 016:** `.github/agents/directives/016_acceptance_test_driven_development.md` (ATDD)
- **Directive 018:** `.github/agents/directives/018_traceable_decisions.md` (ADRs)
- **Directive 022:** `.github/agents/directives/022_audience_oriented_writing.md` (Target personas)
