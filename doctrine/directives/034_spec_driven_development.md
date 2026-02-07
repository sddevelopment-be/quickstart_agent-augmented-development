# Directive 034: Specification-Driven Development

**Status:** Active  
**Introduced:** 2026-02-05  
**Applies to:** All agents (especially Architect Alphonso, Planning Petra)  
**Related Directives:** 016 (ATDD), 018 (Traceable Decisions), 022 (Audience-Oriented Writing)

---

## Purpose

Define when and how to create **specifications** as a bridge between strategic intent and implementation, complementing our existing ATDD (Directive 016) and ADR (Directive 018) practices.

Specifications serve as **detailed design documents** that translate requirements into concrete implementation guidance while remaining independent of specific acceptance tests or architectural decisions.

---

## Core Principles

### 1. Specifications vs. Acceptance Tests vs. ADRs

**Specifications (this directive):**
- **What:** Detailed functional and technical requirements
- **When:** Complex features requiring cross-team alignment
- **Format:** Structured markdown with scenarios, constraints, examples
- **Audience:** Developers, agents, QA engineers
- **Lifecycle:** Living documents, updated as understanding evolves

**Acceptance Tests (Directive 016):**
- **What:** Executable behavioral contracts (Given/When/Then)
- **When:** All user-facing functionality
- **Format:** Gherkin scenarios or test code
- **Audience:** Automated test runners, stakeholders
- **Lifecycle:** Frozen once passing (part of test suite)

**ADRs (Directive 018):**
- **What:** Architectural decisions with trade-off analysis
- **When:** Significant technical choices affecting structure
- **Format:** Standardized ADR template with context/decision/consequences
- **Audience:** Architects, future maintainers, auditors
- **Lifecycle:** Immutable once accepted (historical record)

### 2. When to Create Specifications

Create specifications for:

✅ **Complex Features**
- Multi-step workflows requiring coordination
- Features spanning multiple components/agents
- Interactions with external systems

✅ **Ambiguous Requirements**
- Stakeholder needs requiring clarification
- Edge cases and error scenarios needing definition
- Business logic requiring validation

✅ **Cross-Team Dependencies**
- APIs requiring contract agreement
- Shared data models
- Integration points between subsystems

✅ **High-Risk Areas**
- Security-sensitive functionality
- Performance-critical paths
- Data integrity operations

❌ **Do NOT create specifications for:**
- Simple CRUD operations (use acceptance tests directly)
- Internal utility functions (document in code)
- One-off scripts or tools (inline comments sufficient)
- Architectural decisions (use ADRs instead)

### 3. Specification Structure

**Recommended Template:**

```markdown
# Specification: [Feature Name]

**Status:** Draft | Review | Approved | Implemented  
**Created:** YYYY-MM-DD  
**Author:** [Agent/Person]  
**Stakeholders:** [Who needs to review/approve]

## Overview

Brief description of the feature and its purpose.

## Requirements

### Functional Requirements
1. FR1: The system SHALL...
2. FR2: The system SHALL...

### Non-Functional Requirements
1. NFR1: Performance...
2. NFR2: Security...

## User Scenarios

### Scenario 1: [Happy Path]
**Given:** [Initial state]
**When:** [User action]
**Then:** [Expected outcome]

### Scenario 2: [Error Case]
**Given:** [Initial state]
**When:** [Invalid action]
**Then:** [Error handling]

## Constraints

- Technical constraints
- Business rules
- Compliance requirements

## Open Questions

- [ ] Question 1 → Assigned to [Person/Agent]
- [ ] Question 2 → Assigned to [Person/Agent]

## References

- Related ADRs: [Links]
- Related Tests: [Links]
- External Docs: [Links]
```

---

## Integration with Our Workflow

### Phase 1: Strategic Planning (Planning Petra)

1. **Identify Complex Features**
   - Review strategic goals and milestone plans
   - Flag features requiring specifications
   - Create specification stubs

2. **Specification Assignment**
   - Assign to Architect Alphonso (architectural specs)
   - Assign to domain specialists (functional specs)
   - Set review cycles and approval gates

### Phase 2: Specification Development (Architect/Specialists)

1. **Draft Specification**
   - Use template above
   - Include scenarios, constraints, examples
   - Document open questions

2. **Stakeholder Review**
   - Share with Human-in-Charge (if strategic)
   - Share with implementing agents
   - Iterate based on feedback

3. **Approval**
   - Mark as "Approved" when ready
   - Link from planning documents (NEXT_BATCH.md, AGENT_TASKS.md)
   - Create YAML task files referencing the spec

### Phase 3: Implementation (Backend-Dev, Frontend-Dev, etc.)

1. **Spec-Driven Development**
   - Read specification before starting work
   - Clarify ambiguities before coding
   - Update spec if understanding changes

2. **Acceptance Tests from Spec**
   - Convert scenarios to Gherkin tests (Directive 016)
   - Ensure all requirements have test coverage
   - Link tests back to spec requirements

3. **Spec Maintenance**
   - Update spec if implementation reveals new constraints
   - Mark as "Implemented" when feature complete
   - Archive or move to historical docs

---

## Specification Formats

### 1. Feature Specifications
- Location: `docs/specifications/features/`
- Focus: User-facing functionality
- Example: `dashboard-real-time-updates.md`

### 2. API Specifications
- Location: `docs/specifications/apis/`
- Focus: Interface contracts
- Example: `llm-service-rest-api.md`

### 3. Architecture Specifications
- Location: `docs/architecture/design/`
- Focus: Component interactions, patterns
- Example: `file-based-orchestration-spec.md`

### 4. Integration Specifications
- Location: `docs/specifications/integrations/`
- Focus: External system interactions
- Example: `anthropic-api-integration.md`

---

## Agent-Specific Guidance

### For Architect Alphonso
- Create architectural specifications for complex system designs
- Ensure specs complement ADRs (ADR = decision, spec = design detail)
- Review specs for technical feasibility before approval

### For Planning Petra
- Identify features requiring specifications during planning
- Create specification stubs with structure and assignment
- Track specification status in DEPENDENCIES.md

### For Backend-Dev Benny / Frontend-Dev
- Request specifications before starting complex features
- Clarify ambiguities with spec author before implementation
- Update specs if implementation reveals constraints

### For Writer-Editor Sam
- Review specifications for clarity and audience-appropriateness (Directive 022)
- Ensure specifications follow template structure
- Proofread scenarios and requirements

### For Framework Guardian Gail
- Validate that specifications follow templates
- Check that specs are linked from planning documents
- Ensure acceptance tests trace back to specs

---

## Examples

### Example 1: When to Use Spec vs. ADR

**Scenario:** Dashboard needs real-time updates

**ADR (ADR-032):**
- **Decision:** Use Flask-SocketIO for WebSocket support
- **Why:** Evaluated alternatives (polling, SSE, WebSockets)
- **Trade-offs:** Complexity vs. real-time capability
- **Result:** Decision recorded and immutable

**Specification (separate document):**
- **Requirements:** Update frequency, message format, error handling
- **Scenarios:** Connection loss, reconnection, message ordering
- **Constraints:** Max message size, authentication
- **Open Questions:** How to handle slow clients?

**Outcome:** ADR documents the "what" (WebSockets), spec documents the "how" (detailed behavior).

### Example 2: Spec → Acceptance Test Flow

**Specification Scenario:**
```markdown
### Scenario: User adds new tool via CLI

**Given:** User has valid configuration file
**When:** User runs `llm-service tool add gemini --binary gemini-cli --models gemini-1.5-pro`
**Then:** 
- Tool is added to configuration
- Configuration file is updated atomically
- Success message displayed
- Tool appears in `llm-service tool list`
```

**Acceptance Test (Gherkin):**
```gherkin
Feature: Tool Management CLI

  Scenario: Add new tool successfully
    Given a valid llm-service configuration exists
    When I run "llm-service tool add gemini --binary gemini-cli --models gemini-1.5-pro"
    Then the exit code should be 0
    And the configuration should contain tool "gemini"
    And the output should contain "✅ Tool 'gemini' added"
    And "llm-service tool list" should show "gemini"
```

**Outcome:** Specification drives acceptance test creation.

---

## Common Pitfalls

### ❌ Pitfall 1: Specification Becomes Implementation
**Problem:** Spec dictates code structure, class names, file organization  
**Solution:** Focus on *what* not *how*; leave implementation details to developers

### ❌ Pitfall 2: Specification Duplicates ADR
**Problem:** Spec repeats architectural decision trade-offs  
**Solution:** Reference ADR from spec; don't duplicate rationale

### ❌ Pitfall 3: Specification Never Updated
**Problem:** Spec becomes stale as implementation evolves  
**Solution:** Treat spec as living document during implementation; freeze when feature complete

### ❌ Pitfall 4: No Clear Approval Gate
**Problem:** Unclear when spec is "ready" for implementation  
**Solution:** Explicit approval workflow (Draft → Review → Approved)

### ❌ Pitfall 5: Specification Without Tests
**Problem:** Spec written but no acceptance tests created  
**Solution:** Specification scenarios should become Gherkin tests (Directive 016)

---

## Relationship to spec-kitty

This directive is inspired by [spec-kitty's specification-driven approach](https://github.com/Priivacy-ai/spec-kitty), adapted to our context:

**Similarities:**
- Specifications as design artifacts
- Scenarios drive implementation
- Living documents during development

**Differences:**
- **Our ADRs ≠ Their specs:** We separate architectural decisions (ADRs) from design details (specs)
- **YAML orchestration:** We use YAML task files for agent coordination; specs are referenced from tasks
- **ATDD integration:** Our acceptance tests (Directive 016) are more tightly coupled to specs
- **File-based workflow:** Specs are part of our version-controlled, Git-auditable workflow

**Reference:** See [spec-kitty comparative analysis](../docs/references/comparative_studies/2026-02-05-spec-kitty-comparative-analysis.md) for detailed comparison.

---

## Success Criteria

A specification is successful when:

✅ **Clarity:** Anyone reading the spec understands what to build  
✅ **Completeness:** All scenarios, constraints, and edge cases documented  
✅ **Traceability:** Acceptance tests can be traced back to spec requirements  
✅ **Approval:** Stakeholders have reviewed and approved the spec  
✅ **Actionability:** Developers can start implementation without waiting for clarifications  
✅ **Maintainability:** Spec is updated as understanding evolves, frozen when feature complete

---

## References

**Related Directives:**
- [Directive 016: Acceptance Test-Driven Development](016_acceptance_test_driven_dev.md) - Test creation from specs
- [Directive 018: Traceable Decisions](018_traceable_decisions.md) - ADR vs. spec distinction
- [Directive 022: Audience-Oriented Writing](022_audience_oriented_writing.md) - Spec writing style

**Related Approaches:**
- [Spec-Driven Development PRIMER](../approaches/spec-driven-development.md) - Detailed guidance (to be created)

**Related Documents:**
- [spec-kitty Comparative Analysis](../docs/references/comparative_studies/2026-02-05-spec-kitty-comparative-analysis.md)
- [spec-kitty Source Reference](../docs/references/comparative_studies/references/spec-kitty-spec-driven.md)

**External References:**
- [spec-kitty Repository](https://github.com/Priivacy-ai/spec-kitty) - Original inspiration
- [Behavior-Driven Development](https://cucumber.io/docs/bdd/) - Related methodology

---

**Status:** ✅ Active  
**Next Review:** After first 3 specifications created (validate template effectiveness)  
**Changelog:**
- 2026-02-05: Initial directive created (Planning Petra)
