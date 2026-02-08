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

## Phase Checkpoint Protocol

**Purpose:** Prevent phase-skipping violations and ensure proper hand-offs between agents.

**Implementation:** See [Tactic: Phase Checkpoint Protocol](../tactics/phase-checkpoint-protocol.md)

**Key Requirement:** Execute the 6-step checkpoint at the end of EVERY phase:

1. ✅ Identify current phase [1-6]
2. ✅ Verify phase completion [YES/NO]
3. ✅ Identify next phase owner [Agent name]
4. ✅ Check your authority [YES/NO/CONSULT]
5. ✅ Verify Directives 014/015 satisfied [YES/NO]
6. ✅ Execute hand-off (commit, notify, document)

**Validation:** 0 violations in SPEC-DIST-001 full cycle (2026-02-08)

### Role Boundaries Table

**Authority levels:**
- ✅ **PRIMARY:** Agent has full authority and responsibility for this phase
- ⚠️ **CONSULT:** Agent can advise but should not execute work
- ❌ **NO:** Agent should not participate in this phase

| Agent | Phase 1<br>(Analysis) | Phase 2<br>(Architecture) | Phase 3<br>(Planning) | Phase 4<br>(Tests) | Phase 5<br>(Code) | Phase 6<br>(Review) |
|-------|---------|---------|---------|---------|---------|---------|
| **Analyst Annie** | ✅ PRIMARY | ⚠️ Consult | ⚠️ Consult | ❌ No | ❌ No | ⚠️ AC review only |
| **Architect Alphonso** | ⚠️ Consult | ✅ PRIMARY | ❌ No | ❌ No | ❌ No | ✅ Arch review |
| **Planning Petra** | ❌ No | ❌ No | ✅ PRIMARY | ❌ No | ❌ No | ❌ No |
| **DevOps Danny** | ❌ No | ⚠️ Consult | ❌ No | ✅ If assigned | ✅ If assigned | ⚠️ Peer review |
| **Backend-Dev** | ❌ No | ⚠️ Consult | ❌ No | ✅ If assigned | ✅ If assigned | ⚠️ Peer review |
| **Frontend-Dev** | ❌ No | ⚠️ Consult | ❌ No | ✅ If assigned | ✅ If assigned | ⚠️ Peer review |
| **Framework Guardian Gail** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Standards review |
| **Curator Claire** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Documentation review |

**Notes:**
- **If assigned:** Implementation agents (DevOps Danny, Backend-Dev, Frontend-Dev) are assigned by Planning Petra in Phase 3
- **AC review:** Acceptance Criteria review (verify spec requirements met)
- **Peer review:** Code quality and implementation review
- **Arch review:** Architecture compliance review
- **Standards review:** Directive compliance and code standards

### Common Violations to Avoid

❌ **Phase Skipping:** Analyst jumping from Phase 1 to Phase 5 (implementation)  
→ **Prevention:** Use [Phase Checkpoint Protocol tactic](../tactics/phase-checkpoint-protocol.md)

❌ **Role Overstepping:** Analyst doing Architect's work (trade-off analysis, technical design)  
→ **Prevention:** Check Role Boundaries Table before continuing

❌ **Missing Documentation:** Skipping work logs (Directive 014) or prompt docs (Directive 015)  
→ **Prevention:** Checkpoint Step 5 verifies directive compliance

❌ **Premature Implementation:** Starting code before acceptance tests exist (violates ATDD)  
→ **Prevention:** Phase 4 (tests) MUST complete before Phase 5 (code)

**Related Tactics:**
- [Phase Checkpoint Protocol](../tactics/phase-checkpoint-protocol.md) - 6-step hand-off verification
- [Ralph Wiggum Loop](../approaches/ralph-wiggum-loop.md) - Mid-execution self-observation

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
