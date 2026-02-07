# Tactic: Development.BDD

**Related tactics:**
- `ATDD_adversarial-acceptance.tactic.md` — uses BDD scenarios for adversarial validation
- `test-boundaries-by-responsibility.tactic.md` — BDD scenarios define behavioral boundaries

**Complements:**
- [Directive 016 (Acceptance Test Driven Development)](../directives/016_acceptance_test_driven_development.md)
- [Directive 017 (Test Driven Development)](../directives/017_test_driven_development.md)
- Approach: Decision-First Development — BDD scenarios document behavioral decisions

---

## Intent
Define system behavior through concrete examples before implementation, ensuring shared understanding and executable specifications.

Use this tactic to create a shared behavioral contract between stakeholders and implementers using business-relevant language.

---

## Preconditions

**Required inputs:**
- A feature, capability, or rule is being defined
- Stakeholders or domain knowledge are available
- The behavior can be expressed in observable outcomes

**Assumed context:**
- Behavior-driven development is understood or can be explained
- Stakeholders can participate in scenario definition
- Scenarios will be used as acceptance criteria and test definitions

**Exclusions (when NOT to use):**
- Implementation-only tasks with no behavioral ambiguity
- Purely technical refactoring with no user-visible changes
- When stakeholders are unavailable and behavior is already well-defined

---

## Execution Steps

1. Identify the behavior to be defined.
2. Describe the behavior in business-relevant language (avoid technical jargon).
3. For each behavior, define one or more scenarios using:
   - **Given** (context and preconditions)
   - **When** (action or event)
   - **Then** (expected outcome)
4. Ensure scenarios describe **observable behavior**, not implementation details.
5. Validate scenarios with stakeholders or domain experts.
6. Use the scenarios as acceptance criteria and test definitions.
7. Stop.

---

## Checks / Exit Criteria
- Scenarios are written in Given/When/Then form.
- Scenarios are understandable without code knowledge.
- Expected outcomes are explicit and testable.
- Scenarios cover both happy paths and edge cases.

---

## Failure Modes
- Encoding implementation details in scenarios (e.g., "system calls database").
- Writing overly abstract or generic scenarios that lack concrete examples.
- Treating BDD scenarios as documentation only (not as test input).
- Skipping stakeholder validation.

---

## Outputs
- BDD scenarios (Given/When/Then format)
- Acceptance criteria
- Executable test definitions (if using BDD tooling)

---

## Notes on Use

BDD scenarios serve **three purposes**:
1. **Communication** — shared understanding between stakeholders and implementers
2. **Specification** — explicit behavioral contract
3. **Validation** — executable acceptance tests

Good BDD scenarios are:
- **Concrete** — use specific examples, not abstractions
- **Observable** — describe outcomes anyone can verify
- **Business-focused** — written in domain language

Poor example:
```
Given the system is initialized
When data is processed
Then output is correct
```

Good example:
```
Given a customer has an active subscription
When the customer cancels their subscription
Then the customer receives a confirmation email within 5 minutes
And the subscription status is marked "cancelled"
```

---
