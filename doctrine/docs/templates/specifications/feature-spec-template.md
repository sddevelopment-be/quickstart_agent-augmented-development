# Specification: [Feature Name]

**Status:** Draft | Review | Approved | Implemented | Archived
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Author:** [Agent/Person Name]
**Stakeholders:** [Who needs to review/approve this]

---

## User Story

**As a** [Persona from ${DOC_ROOT}/audience/]
**I want** [capability or feature]
**So that** [business value or benefit]

**Alternative: Acceptance Criterion Format**
**Given** [initial context or state]
**When** [action or trigger occurs]
**Then** [expected outcome or behavior]
**Unless** [exceptional condition - optional]

**Target Personas:**
- [Persona 1] (Primary) - Link: `${DOC_ROOT}/audience/[persona].md`
- [Persona 2] (Secondary) - Link: `${DOC_ROOT}/audience/[persona].md`

---

## Overview

[2-3 paragraphs describing the feature, its purpose, and why it matters to the target personas. Focus on the problem being solved, not the technical solution.]

**Context:**
- What problem does this solve?
- Why is it needed now?
- What constraints exist?

**Related Documentation:**
- Related ADRs: [Link to architectural decisions that provide context]
- Related Specifications: [Link to dependencies or related specs]
- Background: [Any external docs, standards, or references]

---

## Functional Requirements (MoSCoW)

### MUST Have (Critical - Feature unusable without these)

**FR-M1:** [Requirement statement in clear, testable language]
- **Rationale:** Why this is critical
- **Personas Affected:** [List personas who need this]
- **Success Criteria:** How we verify this is met

**FR-M2:** [Next critical requirement]
- **Rationale:** ...
- **Personas Affected:** ...
- **Success Criteria:** ...

### SHOULD Have (Important - Feature degraded without these)

**FR-S1:** [Important but not critical requirement]
- **Rationale:** Why this is important
- **Personas Affected:** [List personas]
- **Success Criteria:** Verification method
- **Workaround if omitted:** [What can users do if this isn't included]

**FR-S2:** [Next important requirement]
- **Rationale:** ...
- **Personas Affected:** ...
- **Success Criteria:** ...
- **Workaround if omitted:** ...

### COULD Have (Nice to have - Enhances experience)

**FR-C1:** [Desirable but not essential requirement]
- **Rationale:** Why this would be nice
- **Personas Affected:** [List personas]
- **Success Criteria:** Verification method
- **If omitted:** [Impact of not including this]

**FR-C2:** [Next nice-to-have requirement]
- **Rationale:** ...
- **Personas Affected:** ...
- **Success Criteria:** ...
- **If omitted:** ...

### WON'T Have (Explicitly out of scope)

**FR-W1:** [Requirement explicitly excluded from this iteration]
- **Rationale:** Why this is out of scope
- **Future Consideration:** Could this be added later?

**FR-W2:** [Next excluded requirement]
- **Rationale:** ...
- **Future Consideration:** ...

---

## Scenarios and Behavior

### Scenario 1: [Happy Path - Primary Success Flow]

**Context:** [Who is doing this and why]

**Given:** [Initial state or preconditions]
**And:** [Additional context if needed]
**When:** [User action or system trigger]
**Then:** [Expected outcome]
**And:** [Additional outcomes]

**Personas:** [Which personas use this scenario]
**Priority:** MUST | SHOULD | COULD

### Scenario 2: [Alternative Path - Different Way to Achieve Goal]

**Context:** [Different situation or approach]

**Given:** [Different initial state]
**When:** [Alternative action]
**Then:** [Expected outcome for this path]

**Personas:** [Which personas use this scenario]
**Priority:** MUST | SHOULD | COULD

### Scenario 3: [Error Case - What Happens When Things Go Wrong]

**Context:** [Error condition explanation]

**Given:** [Setup leading to error]
**When:** [Action that triggers error]
**Then:** [How system handles error]
**And:** [Recovery or fallback behavior]

**Personas:** [Who encounters this scenario]
**Priority:** MUST | SHOULD | COULD

### Scenario 4: [Edge Case - Boundary Conditions]

**Context:** [Unusual but valid situation]

**Given:** [Edge case setup]
**When:** [Edge case action]
**Then:** [Expected edge case behavior]
**Unless:** [Exception within the edge case]

**Personas:** [Who might hit this edge case]
**Priority:** MUST | SHOULD | COULD

---

## Constraints and Business Rules

### Business Rules

**BR1:** [Business logic or policy that must be enforced]
- **Applies to:** [Which scenarios or requirements]
- **Enforcement:** [How this is verified]

**BR2:** [Next business rule]
- **Applies to:** ...
- **Enforcement:** ...

### Technical Constraints

**TC1:** [Performance constraint - e.g., response time, throughput]
- **Measurement:** [How this is measured]
- **Rationale:** [Why this constraint exists]

**TC2:** [Security constraint - e.g., authentication, encryption]
- **Measurement:** ...
- **Rationale:** ...

**TC3:** [Compatibility constraint - e.g., browser support, API versions]
- **Measurement:** ...
- **Rationale:** ...

### Non-Functional Requirements (MoSCoW)

**NFR-M1 (MUST):** [Critical quality attribute]
- **Example:** System MUST respond to user actions within 2 seconds
- **Measurement:** 95th percentile response time
- **Verification:** Performance tests

**NFR-S1 (SHOULD):** [Important quality attribute]
- **Example:** System SHOULD handle 1000 concurrent users
- **Measurement:** Load testing metrics
- **Verification:** Stress tests

**NFR-C1 (COULD):** [Desirable quality attribute]
- **Example:** System COULD cache responses for 5 minutes
- **Measurement:** Cache hit rate
- **Verification:** Monitoring metrics

### Edge Cases and Limits

- **Maximum values:** [E.g., max file size, max concurrent connections]
- **Minimum values:** [E.g., min valid input, min required data]
- **Invalid inputs:** [How system handles bad data]
- **Timeouts:** [When operations abort]
- **Fallbacks:** [Graceful degradation strategies]

---

## Open Questions

### Unresolved Requirements
- [ ] **Q1:** [Question about requirement or behavior]
  - **Assigned to:** [Person/Agent responsible for answering]
  - **Target Date:** YYYY-MM-DD
  - **Blocking:** [What is blocked until this is resolved]

- [ ] **Q2:** [Next unresolved question]
  - **Assigned to:** ...
  - **Target Date:** ...
  - **Blocking:** ...

### Design Decisions Needed
- [ ] **D1:** [Decision about approach or implementation]
  - **Options:** [List alternatives being considered]
  - **Decision Maker:** [Who decides]
  - **Context:** [What depends on this decision]

- [ ] **D2:** [Next design decision]
  - **Options:** ...
  - **Decision Maker:** ...
  - **Context:** ...

### Clarifications Required
- [ ] **C1:** [Clarification needed from stakeholder or persona]
  - **Who to ask:** [Stakeholder or persona]
  - **Why it matters:** [Impact of the answer]

- [ ] **C2:** [Next clarification needed]
  - **Who to ask:** ...
  - **Why it matters:** ...

---

## Out of Scope

**Explicitly NOT included in this specification:**

1. **[Feature/Capability]**
   - **Reason:** [Why this is excluded]
   - **Future:** [Could this be added later? When?]

2. **[Another exclusion]**
   - **Reason:** ...
   - **Future:** ...

3. **[Technical implementation details]**
   - **Reason:** Implementation is left to developers following this spec
   - **Note:** See related ADRs for architectural constraints

---

## Acceptance Criteria Summary

**This feature is DONE when:**

- [ ] All MUST requirements (FR-M* and NFR-M*) are implemented
- [ ] All SHOULD requirements (FR-S* and NFR-S*) are implemented OR documented workarounds exist
- [ ] All MUST scenarios pass acceptance tests
- [ ] All business rules (BR*) are enforced
- [ ] All technical constraints (TC*) are met
- [ ] Open questions are resolved
- [ ] Acceptance tests derived from scenarios are passing
- [ ] Documentation updated to reflect new capability
- [ ] Target personas have validated the feature meets their needs

---

## Traceability

### Derives From (Strategic)
- **Strategic Goal:** [Link to milestone, objective, or strategic plan]
- **User Need:** [Link to user research, persona needs, or problem statement]
- **Related ADRs:** [Architectural decisions that enable this feature]

### Feeds Into (Tactical)
- **Acceptance Tests:** [Link to test files derived from these scenarios]
- **Implementation Tasks:** [Link to YAML task files in ${WORKSPACE_ROOT}/collaboration/]
- **API Documentation:** [Link to API specs or endpoint docs]

### Related Specifications
- **Dependencies:** [Other specs that must be complete first]
- **Dependents:** [Specs that build on this one]
- **Cross-References:** [Related specs for context]

---

## Change Log

Track significant changes to this specification:

| Date | Author | Change | Reason |
|------|--------|--------|--------|
| YYYY-MM-DD | [Name] | Initial draft created | Feature identified in planning |
| YYYY-MM-DD | [Name] | Added NFR-M2 (security constraint) | Discovered during review |
| YYYY-MM-DD | [Name] | Moved FR-S3 to FR-C1 (reprioritized) | Stakeholder feedback |
| YYYY-MM-DD | [Name] | Marked as Approved | All stakeholders signed off |
| YYYY-MM-DD | [Name] | Updated TC1 (performance constraint) | Discovered during implementation |
| YYYY-MM-DD | [Name] | Marked as Implemented | Feature complete, tests passing |

---

## Approval

### Reviewers

| Role | Name | Date | Status | Comments |
|------|------|------|--------|----------|
| Target Persona | [Persona rep] | YYYY-MM-DD | ✅ Approved | Meets needs |
| Architect | Architect Alphonso | YYYY-MM-DD | ✅ Approved | Technically feasible |
| Implementer | Backend-Dev Benny | YYYY-MM-DD | ⏳ Pending | Reviewing scenarios |
| Stakeholder | [Human-in-Charge] | YYYY-MM-DD | ⏳ Pending | - |

### Sign-Off

**Final Approval:**
- **Date:** YYYY-MM-DD
- **Approved By:** [Name/Role]
- **Status:** Ready for implementation

---

## Metadata

**Tags:** `#feature-spec` `#[domain]` `#[component]` `#[persona-id]`

**Related Files:**
- Template: `${DOC_ROOT}/templates/${SPEC_ROOT}/feature-spec-template.md`
- Persona: `${DOC_ROOT}/audience/[persona].md`
- ADR: `${DOC_ROOT}/architecture/adrs/ADR-XXX-[title].md`
- Tests: `tests/acceptance/features/[feature].feature`
- Tasks: `${WORKSPACE_ROOT}/collaboration/inbox/[timestamp]-[agent]-[feature].yaml`

**Navigation:**
- Previous Spec: [Link to prerequisite spec]
- Next Spec: [Link to follow-on spec]
- Parent Spec: [Link to broader spec this is part of]

---

## Notes for Authors

**When filling out this template:**

1. **Start with User Story** - Write from persona perspective first
2. **Use MoSCoW prioritization** - Be honest about MUST vs SHOULD vs COULD
3. **Keep it functional** - Describe WHAT, not HOW
4. **Write testable scenarios** - Every Given/When/Then should be verifiable
5. **Link to personas** - Understand who needs this and why
6. **Reference ADRs** - Don't duplicate architectural decisions
7. **Mark open questions** - Be explicit about unknowns
8. **Update as you learn** - Living document during development
9. **Freeze when implemented** - Mark as Implemented when feature is done
10. **Get approval** - Don't skip stakeholder review

**Common mistakes to avoid:**
- ❌ Dictating implementation (code structure, libraries, file organization)
- ❌ Duplicating ADR content (architectural trade-offs belong in ADRs)
- ❌ Forgetting personas (always identify who needs this)
- ❌ Vague requirements (be specific and testable)
- ❌ Missing edge cases (think about error conditions and limits)

**Good specification example:**
> **FR-M1:** System MUST display task status updates within 500ms of file change
> - **Rationale:** Software Engineers need real-time feedback to monitor agents
> - **Personas Affected:** Software Engineer, Agentic Framework Core Team
> - **Success Criteria:** WebSocket event delivered <500ms (95th percentile)

**Bad specification example:**
> ❌ Create a FileWatcher class using watchdog library with debounce=100ms
> ❌ Store connections in dict keyed by session ID
> ❌ Use Flask-SocketIO for WebSocket handling
