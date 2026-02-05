# Specification-Driven Development (SDD) PRIMER

**Approach Type:** Development Methodology  
**Version:** 1.0.0  
**Last Updated:** 2026-02-05  
**Status:** Active

---

## Purpose

This PRIMER provides practical guidance for creating and using **specifications** as the bridge between strategic intent and implementation. Specifications translate requirements into concrete implementation guidance while remaining independent of specific tests or architectural decisions.

**Target Audience:**
- Architect Alphonso (creating architectural and API specifications)
- Planning Petra (identifying when specifications are needed)
- All development agents (Backend-Dev Benny, Frontend-Dev, etc.)
- Writer-Editor Sam (reviewing specification clarity)

**Core Question This PRIMER Answers:**  
*"When do I write a specification vs. an acceptance test vs. an ADR?"*

---

## The Three Pillars of Documentation

Understanding when to use each documentation type is critical to efficient development:

### 1. **Specifications** (SDD - This PRIMER)

**Purpose:** Define *what* to build with detailed functional and technical requirements

**When to Use:**
- Complex multi-step workflows
- Features spanning multiple components or agents
- Ambiguous requirements needing clarification
- API contracts requiring alignment
- High-risk areas (security, performance, data integrity)

**Format:** Structured markdown with scenarios, constraints, examples

**Lifecycle:** Living document during development → frozen when feature complete

**Example:**
```markdown
# Specification: Real-Time Dashboard Updates

## Requirements
FR1: System SHALL push updates to clients within 500ms of data change
FR2: System SHALL handle 1000+ concurrent connections
FR3: System SHALL reconnect clients automatically on disconnect

## Scenario: Connection Loss Recovery
**Given:** Client connected with active session
**When:** Network connection drops
**Then:** Client attempts reconnection every 5s (max 3 attempts)
**And:** Client displays "Reconnecting..." indicator
**And:** Client queues updates received during reconnection
```

### 2. **Acceptance Tests** (ATDD - Directive 016)

**Purpose:** Define *observable behavior* as executable contracts

**When to Use:**
- All user-facing functionality
- API endpoints and CLI commands
- UI workflows and interactions
- Integration points with external systems

**Format:** Gherkin (Given/When/Then) or test code

**Lifecycle:** Fail first → pass on completion → frozen in test suite

**Example:**
```gherkin
Feature: Dashboard Real-Time Updates

  Scenario: Receive live data updates
    Given I am logged into the dashboard
    And I have subscribed to "stock-prices" channel
    When a stock price changes
    Then I should see the updated price within 500ms
    And the UI should not flicker or reload
```

### 3. **ADRs** (Directive 018)

**Purpose:** Record *architectural decisions* with trade-off analysis

**When to Use:**
- Technology selection (frameworks, databases, protocols)
- Architectural patterns (microservices, event-driven, etc.)
- Significant structural changes affecting multiple components
- Trade-offs requiring documented rationale

**Format:** Standardized ADR template (Context/Decision/Consequences)

**Lifecycle:** Immutable once accepted (historical record)

**Example:**
```markdown
# ADR-032: Use Flask-SocketIO for Real-Time Updates

## Context
Dashboard requires real-time updates for stock prices.

## Decision
Use Flask-SocketIO (WebSocket protocol) for bidirectional communication.

## Alternatives Considered
1. HTTP polling - Simple but inefficient (rejected)
2. Server-Sent Events - Unidirectional only (rejected)
3. WebSockets via Flask-SocketIO - Full-duplex, efficient (selected)

## Consequences
✅ Real-time bidirectional communication
✅ Efficient (no polling overhead)
❌ Additional complexity (SocketIO library)
❌ Connection management required
```

---

## Decision Matrix: Which Document Type?

Use this flowchart to determine what to create:

```
START: Do I need to document something?
  │
  ├─► Is this an ARCHITECTURAL DECISION (tech choice, pattern)?
  │   YES → Create ADR (Directive 018)
  │   NO ↓
  │
  ├─► Is this a SIMPLE feature with clear requirements?
  │   YES → Write acceptance tests directly (Directive 016)
  │   NO ↓
  │
  ├─► Does this feature have:
  │   - Multiple scenarios with edge cases?
  │   - Complex business logic needing validation?
  │   - Cross-team dependencies requiring alignment?
  │   - API contracts needing agreement?
  │   YES → Create SPECIFICATION first (this PRIMER)
  │        THEN derive acceptance tests from spec
  │
  └─► Still uncertain? → Ask Planning Petra or Architect Alphonso
```

---

## Specification Structure

### Recommended Template

```markdown
# Specification: [Feature Name]

**Status:** Draft | Review | Approved | Implemented  
**Created:** YYYY-MM-DD  
**Author:** [Agent/Person]  
**Stakeholders:** [Who needs to review/approve]  
**Related ADRs:** [Links to architectural decisions]

## Overview

[2-3 paragraphs describing the feature, its purpose, and context]

## Requirements

### Functional Requirements
1. **FR1:** The system SHALL [specific behavior]
2. **FR2:** The system SHALL [specific behavior]
3. **FR3:** The system SHOULD [optional behavior]

### Non-Functional Requirements
1. **NFR1:** Performance: [specific metric]
2. **NFR2:** Security: [specific constraint]
3. **NFR3:** Scalability: [specific limit]

## User Scenarios

### Scenario 1: [Happy Path Name]
**Given:** [Initial state and preconditions]  
**When:** [User action or trigger]  
**Then:** [Expected outcome]  
**And:** [Additional outcomes]

### Scenario 2: [Edge Case Name]
**Given:** [Initial state]  
**When:** [Error condition or edge case]  
**Then:** [Error handling behavior]  
**And:** [Recovery or fallback]

### Scenario 3: [Alternative Path Name]
**Given:** [Different initial state]  
**When:** [Alternative action]  
**Then:** [Different outcome]

## Technical Constraints

- **Constraint 1:** [Technical limitation or requirement]
- **Constraint 2:** [Integration constraint]
- **Constraint 3:** [Platform or environment constraint]

## Business Rules

1. **Rule 1:** [Business logic or policy]
2. **Rule 2:** [Validation rule]
3. **Rule 3:** [Calculation or derivation rule]

## Open Questions

- [ ] **Q1:** [Unresolved question] → Assigned to: [Name/Agent]
- [ ] **Q2:** [Pending decision] → Assigned to: [Name/Agent]
- [ ] **Q3:** [Clarification needed] → Assigned to: [Name/Agent]

## Acceptance Criteria

*(These will become acceptance tests per Directive 016)*

- [ ] All functional requirements implemented
- [ ] All scenarios tested and passing
- [ ] Performance metrics met
- [ ] Security review completed
- [ ] Documentation updated

## References

- **ADRs:** [Links to related architectural decisions]
- **Tests:** [Links to acceptance test files]
- **External Docs:** [API documentation, standards, etc.]
- **Related Specs:** [Other specifications this depends on]
```

---

## SDD Workflow: From Spec to Implementation

### Phase 1: Specification Creation

**Trigger:** Planning Petra identifies complex feature requiring specification

**Steps:**

1. **Create Specification Stub**
   ```bash
   # Create file at appropriate location
   docs/specifications/features/[feature-name].md
   ```

2. **Draft Specification**
   - Use template above
   - Include all scenarios (happy path, edge cases, error cases)
   - Document constraints and business rules
   - List open questions

3. **Stakeholder Review**
   - Share with Human-in-Charge (if strategic)
   - Share with implementing agents
   - Share with QA/testing agents
   - Iterate based on feedback

4. **Approval**
   - Mark status as "Approved"
   - Link from planning documents (`NEXT_BATCH.md`, `AGENT_TASKS.md`)
   - Create YAML task files referencing the spec

**Agent Prompts:**

```
For Architect Alphonso:
"Create a specification for [feature] covering API contract, 
data models, integration points, and error handling scenarios. 
Reference ADR-XXX for architectural context."

For Planning Petra:
"Review [feature requirements] and determine if specification 
is needed. If yes, create specification stub with structure 
and assign to appropriate specialist."
```

### Phase 2: Acceptance Test Generation

**Trigger:** Specification approved and ready for implementation

**Steps:**

1. **Convert Scenarios to Gherkin**
   - Each specification scenario → Gherkin scenario
   - Map requirements to test assertions
   - Ensure test coverage for all edge cases

2. **Create Test Files**
   ```bash
   # Following Directive 016 (ATDD)
   tests/acceptance/features/[feature-name].feature
   ```

3. **Link Tests to Spec**
   - Add test file links to specification "References" section
   - Add spec link to test file comments
   - Ensure traceability

**Agent Prompts:**

```
For Backend-Dev Benny:
"Convert specification scenarios from docs/specifications/features/[name].md 
into Gherkin acceptance tests. Ensure all requirements (FR1-FRN) have 
corresponding test coverage."

For QA Agent:
"Review specification at [path] and create comprehensive acceptance 
test suite covering all scenarios, edge cases, and error conditions."
```

### Phase 3: Implementation

**Trigger:** Acceptance tests created and failing for right reasons

**Steps:**

1. **Read Specification**
   - Understand all requirements and scenarios
   - Note constraints and business rules
   - Clarify ambiguities before coding

2. **Implement Feature**
   - Follow test-driven development (TDD) cycles
   - Make acceptance tests pass
   - Ensure performance and security requirements met

3. **Update Specification**
   - Document any implementation constraints discovered
   - Update scenarios if understanding evolved
   - Mark as "Implemented" when complete

**Agent Prompts:**

```
For Backend-Dev Benny:
"Implement [feature] according to specification at [path]. 
The acceptance tests at [test-path] should pass. 
Reference ADR-XXX for architectural constraints."

For Frontend-Dev:
"Implement UI for [feature] per specification [path]. 
Ensure all user scenarios work as specified and 
acceptance tests pass."
```

### Phase 4: Maintenance

**Trigger:** Feature complete but specification needs updates

**Steps:**

1. **Living Document During Development**
   - Update spec as understanding evolves
   - Document new constraints discovered
   - Add scenarios found during testing

2. **Freeze on Completion**
   - Mark status as "Implemented"
   - Move to `docs/specifications/archive/` (optional)
   - Spec becomes reference documentation

3. **Future Changes**
   - Create new specification for major changes
   - Reference original spec for context
   - Update acceptance tests first (per Directive 016)

---

## Specification Types and Locations

### 1. Feature Specifications

**Location:** `docs/specifications/features/`  
**Focus:** User-facing functionality, workflows, UI behavior  
**Example:** `dashboard-real-time-updates.md`

**When to Create:**
- Multi-step user workflows
- Complex UI interactions
- Business logic requiring validation

### 2. API Specifications

**Location:** `docs/specifications/apis/`  
**Focus:** Interface contracts, endpoints, data models  
**Example:** `llm-service-rest-api.md`

**When to Create:**
- REST/GraphQL API design
- Inter-service communication contracts
- Integration with external systems

### 3. Architecture Specifications

**Location:** `docs/architecture/design/`  
**Focus:** Component interactions, patterns, system behavior  
**Example:** `file-based-orchestration-spec.md`

**When to Create:**
- Cross-component coordination
- System-wide patterns
- Framework or platform features

### 4. Integration Specifications

**Location:** `docs/specifications/integrations/`  
**Focus:** External system interactions, protocols  
**Example:** `anthropic-api-integration.md`

**When to Create:**
- Third-party API integration
- External service dependencies
- Protocol implementation

---

## Integration with Our File-Based Orchestration

Specifications integrate seamlessly with our YAML task workflow:

### 1. Planning Phase

**File:** `work/planning/NEXT_BATCH.md`

```markdown
## Feature: Real-Time Dashboard Updates

**Requires Specification:** Yes (complex WebSocket implementation)

**Specification:**
- Path: `docs/specifications/features/dashboard-real-time-updates.md`
- Status: Approved
- Author: Architect Alphonso
```

### 2. Task Assignment

**File:** `work/collaboration/inbox/[timestamp]-backend-dev-websocket-impl.yaml`

```yaml
id: 2026-02-05T1500-backend-dev-websocket-impl
agent: backend-dev
status: new
priority: high
title: "Implement WebSocket Real-Time Updates"
artefacts:
  - src/api/websocket/
  - tests/acceptance/features/real-time-updates.feature
context:
  specification: docs/specifications/features/dashboard-real-time-updates.md
  related_adr: docs/architecture/decisions/ADR-032-websocket-framework.md
  acceptance_tests: tests/acceptance/features/real-time-updates.feature
requirements:
  - Implement all scenarios from specification
  - Ensure acceptance tests pass
  - Meet performance requirements (500ms latency)
```

### 3. Implementation Tracking

**File:** `work/reports/logs/backend-dev/[timestamp]-websocket-implementation.md`

```markdown
## Implementation Log: WebSocket Real-Time Updates

**Specification:** docs/specifications/features/dashboard-real-time-updates.md  
**Status:** In Progress

### Progress
- [x] Scenario 1: Basic connection - Implemented
- [x] Scenario 2: Message broadcast - Implemented
- [ ] Scenario 3: Connection loss recovery - In progress
- [ ] Performance testing (NFR1: 500ms latency)

### Implementation Notes
- Discovered additional constraint: max 10KB message size
  → Updated specification with NFR4
- Need clarification on authentication flow
  → Added open question Q4 to specification
```

---

## Relationship to spec-kitty

This approach is inspired by [spec-kitty's specification-driven methodology](https://github.com/Priivacy-ai/spec-kitty), adapted to our context:

### Similarities

✅ **Specifications as Primary Artifacts**
- Both treat specs as first-class development artifacts
- Specifications drive implementation decisions

✅ **Scenario-Driven Design**
- Both use concrete scenarios to clarify requirements
- Given/When/Then format for clarity

✅ **Living Documents**
- Specifications evolve during development
- Update specs as understanding grows

### Key Differences

❌ **Code as Source of Truth** (spec-kitty) vs. **Specifications as Design** (ours)

**spec-kitty Philosophy:**
- Code is always the source of truth
- Specifications are *change requests* (deltas)
- LLMs read code to understand current state
- Specs describe what to *change*, not what exists

**Our Philosophy:**
- Specifications define detailed requirements *before* implementation
- Code implements the specification
- Specifications complement (not replace) ADRs
- Specs are comprehensive design docs, not just deltas

❌ **Our Separation of Concerns:**

| Document Type | spec-kitty                  | Our Approach                        |
|---------------|-----------------------------|------------------------------------|
| Specifications | Change requests            | Detailed design documents          |
| ADRs          | Not emphasized             | Architectural decisions (Directive 018) |
| Tests         | Derived from specs         | Parallel to specs (Directive 016)  |
| Code          | Source of truth            | Implementation of spec + ADR       |

❌ **Integration Approach:**

**spec-kitty:**
- Work packages in Git worktrees
- Kanban lanes tracked in frontmatter
- CLI generates agent commands
- Agents invoked via slash commands

**Our Approach:**
- YAML task files for orchestration
- `work/` directory-based coordination
- File-based state management
- Agents read/write status files

### What We Adopted

✅ **Specification Templates** - Structured format for requirements and scenarios  
✅ **Scenario-Driven Development** - Given/When/Then clarity  
✅ **Approval Workflow** - Draft → Review → Approved → Implemented  
✅ **Traceability** - Link specs to tests to code

### What We Adapted

🔄 **Philosophical Shift** - Specifications as comprehensive design docs, not change deltas  
🔄 **ADR Integration** - Clear separation between decisions (ADR) and design (spec)  
🔄 **ATDD Coupling** - Specifications drive acceptance tests (Directive 016)  
🔄 **File-Based Orchestration** - Specs referenced from YAML tasks, not worktree frontmatter

**Reference:** See [spec-kitty comparative analysis](../../../docs/architecture/design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md) for detailed comparison.

---

## Common Pitfalls and Solutions

### ❌ Pitfall 1: Specification Becomes Implementation

**Problem:** Spec dictates code structure, class names, method signatures

**Example:**
```markdown
❌ BAD:
"Create a `DashboardWebSocketHandler` class that extends 
`SocketIO.Handler` with methods `on_connect()`, `on_message()`, 
and `on_disconnect()`. Store connections in a `dict` keyed by 
session ID."
```

**Solution:** Focus on *what* not *how*; leave implementation details to developers

**Example:**
```markdown
✅ GOOD:
"System SHALL maintain active WebSocket connections and 
route messages to appropriate clients based on subscription 
channels. Connection lifecycle (connect, message, disconnect) 
SHALL be handled gracefully with error recovery."
```

### ❌ Pitfall 2: Specification Duplicates ADR

**Problem:** Spec repeats architectural decision trade-offs and rationale

**Example:**
```markdown
❌ BAD:
"We chose Flask-SocketIO over raw WebSockets because:
- Easier integration with Flask
- Built-in room/namespace support
- Better error handling
[... 3 pages of trade-off analysis ...]"
```

**Solution:** Reference ADR from spec; don't duplicate rationale

**Example:**
```markdown
✅ GOOD:
"Real-time communication uses WebSocket protocol via 
Flask-SocketIO (see ADR-032 for architectural rationale).
This specification defines the connection lifecycle, 
message format, and error handling requirements."
```

### ❌ Pitfall 3: Specification Never Updated

**Problem:** Spec becomes stale as implementation reveals new constraints

**Example:**
- Spec says "handle unlimited connections"
- Implementation discovers 1000 connection limit
- Spec never updated → misleading documentation

**Solution:** Treat spec as living document during implementation

**Best Practice:**
```markdown
## Change Log

2026-02-05: Added NFR4 (max message size 10KB) - discovered during load testing
2026-02-06: Updated Scenario 3 - reconnection uses exponential backoff
2026-02-07: Marked as "Implemented" - feature complete
```

### ❌ Pitfall 4: No Clear Approval Gate

**Problem:** Unclear when spec is "ready" for implementation

**Solution:** Explicit approval workflow with status tracking

```markdown
# Specification Status Workflow

Draft → Review → Approved → Implemented

**Status: Approved**
- Reviewed by: Architect Alphonso, Backend-Dev Benny
- Approved on: 2026-02-05
- Ready for implementation: YES
```

### ❌ Pitfall 5: Specification Without Tests

**Problem:** Spec written but no acceptance tests created

**Solution:** Specification scenarios MUST become Gherkin tests (Directive 016)

**Workflow:**
1. Write specification with scenarios
2. Convert scenarios to Gherkin (`.feature` files)
3. Link spec ↔ tests bidirectionally
4. Implement until tests pass

---

## Success Criteria

A specification is successful when:

✅ **Clarity:** Anyone can understand what to build without asking questions  
✅ **Completeness:** All scenarios, constraints, and edge cases documented  
✅ **Traceability:** Acceptance tests trace back to spec requirements  
✅ **Approval:** Stakeholders reviewed and approved the spec  
✅ **Actionability:** Developers can start coding without waiting for clarifications  
✅ **Maintainability:** Spec updated as understanding evolves, frozen when complete

---

## Agent-Specific Guidance

### For Architect Alphonso

**Responsibilities:**
- Create architectural and API specifications
- Ensure specs complement ADRs (ADR = decision, spec = design)
- Review specs for technical feasibility before approval

**Example Prompts:**
```
"Create an API specification for the LLM Service REST endpoints 
including authentication, request/response formats, error codes, 
and rate limiting. Reference ADR-025 for auth framework choice."

"Review specification at docs/specifications/features/[name].md 
for technical feasibility. Flag any architectural concerns or 
missing constraints."
```

### For Planning Petra

**Responsibilities:**
- Identify features requiring specifications during planning
- Create specification stubs with structure and assignment
- Track specification status in `DEPENDENCIES.md`

**Example Prompts:**
```
"Review milestone M4 features and identify which require 
specifications vs. direct acceptance tests. Create specification 
stubs for complex features."

"Track specification approval status for feature [name]. 
Update DEPENDENCIES.md and create YAML task for implementation 
once approved."
```

### For Backend-Dev Benny / Frontend-Dev

**Responsibilities:**
- Request specifications before starting complex features
- Clarify ambiguities with spec author before implementation
- Update specs if implementation reveals constraints

**Example Prompts:**
```
"Implement feature [name] according to specification at [path]. 
Acceptance tests at [test-path] must pass. Flag any spec 
ambiguities before proceeding."

"During implementation of [feature], discovered constraint: 
[description]. Update specification at [path] with NFR section 
documenting this constraint."
```

### For Writer-Editor Sam

**Responsibilities:**
- Review specifications for clarity and audience-appropriateness
- Ensure specifications follow template structure
- Proofread scenarios and requirements

**Example Prompts:**
```
"Review specification at docs/specifications/features/[name].md 
for clarity. Ensure scenarios are unambiguous and requirements 
use consistent SHALL/SHOULD/MAY language."

"Edit specification [name] to improve readability for developers. 
Simplify complex sentences and ensure technical terms are 
consistently used."
```

### For Framework Guardian Gail

**Responsibilities:**
- Validate specifications follow templates
- Check specs are linked from planning documents
- Ensure acceptance tests trace back to specs

**Example Prompts:**
```
"Validate that specification docs/specifications/features/[name].md 
follows the standard template and includes all required sections 
(Overview, Requirements, Scenarios, Constraints, etc.)."

"Audit traceability: ensure specification [name] is referenced 
from NEXT_BATCH.md and has corresponding acceptance tests linked 
in References section."
```

---

## Quick Reference: Example Prompts

### Creating a Specification

```
Architect Alphonso:
"Create a specification for [feature-name] at 
docs/specifications/features/[filename].md. Include:
- Overview of feature purpose
- Functional requirements (FR1-FRN)
- Non-functional requirements (performance, security)
- User scenarios (happy path, edge cases, errors)
- Technical constraints
- Business rules
Reference ADR-XXX for architectural context."
```

### Converting Spec to Tests

```
Backend-Dev Benny:
"Convert specification scenarios from 
docs/specifications/features/[name].md into Gherkin 
acceptance tests at tests/acceptance/features/[name].feature. 
Ensure all requirements have test coverage."
```

### Implementing from Spec

```
Backend-Dev Benny:
"Implement [feature] per specification at [spec-path]. 
Acceptance tests at [test-path] must pass. Meet all 
performance requirements (NFR sections). Flag any ambiguities 
before coding."
```

### Updating a Specification

```
Backend-Dev Benny:
"Update specification docs/specifications/features/[name].md 
to document constraint discovered during implementation: 
[description]. Add as NFR-X and note in change log."
```

### Reviewing a Specification

```
Architect Alphonso:
"Review specification at docs/specifications/features/[name].md 
for:
- Technical feasibility
- Completeness (all scenarios covered?)
- Consistency with ADRs
- Missing constraints or edge cases
Approve or request changes."
```

---

## Metadata

**Capabilities:**
- Specification creation and management
- Scenario-driven requirement definition
- Traceability from requirements to tests to code
- Integration with YAML task orchestration
- Living document maintenance

**Tags:**
- `#specification-driven-development`
- `#sdd`
- `#requirements-management`
- `#scenario-driven`
- `#atdd-integration`
- `#traceable-decisions`

**Related Directives:**
- [Directive 016: Acceptance Test-Driven Development](../directives/016_acceptance_test_driven_development.md) - Test creation
- [Directive 018: Traceable Decisions](../directives/018_traceable_decisions.md) - ADR vs. spec
- [Directive 022: Audience-Oriented Writing](../directives/022_audience_oriented_writing.md) - Writing style
- [Directive 034: Specification-Driven Development](../directives/034_spec_driven_development.md) - Formal directive

**Related Approaches:**
- [Decision-First Development](decision-first-development.md) - ADR workflow
- [Work Directory Orchestration](work-directory-orchestration.md) - Task file integration
- [Target-Audience Fit](target-audience-fit.md) - Specification writing style

**External References:**
- [spec-kitty Repository](https://github.com/Priivacy-ai/spec-kitty) - Original inspiration
- [spec-kitty Comparative Analysis](../../../docs/architecture/design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md) - Detailed comparison
- [Behavior-Driven Development](https://cucumber.io/docs/bdd/) - Related methodology

---

**Version History:**
- **1.0.0** (2026-02-05): Initial PRIMER created by Writer-Editor Sam
  - Adapted from spec-kitty methodology
  - Integrated with Directive 034 and ATDD (Directive 016)
  - Defined clear distinctions between specs, tests, and ADRs

---

**Maintainer:** Writer-Editor Sam (collaborative with Architect Alphonso)  
**Review Cycle:** After first 5 specifications created (validate template effectiveness)  
**Next Review:** 2026-03-15 or after M4 completion (whichever comes first)
