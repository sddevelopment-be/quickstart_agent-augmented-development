# Tactic: Testing.SelectAppropriateLevel

**Related tactics:**
- `test-boundaries-by-responsibility.tactic.md` — uses boundaries to determine test level
- `ATDD_adversarial-acceptance.tactic.md` — system-level testing for acceptance criteria

**Complements:**
- [Directive 016 (Acceptance Test Driven Development)](../directives/016_acceptance_test_driven_development.md)
- [Directive 017 (Test Driven Development)](../directives/017_test_driven_development.md)
- Approach: Test Readability and Clarity Check — validates test quality at each level

---

## Intent
Determine the appropriate level of testing (unit, integration, system) for a change based on risk, scope, and feedback needs.

Use this tactic to balance test coverage, cost, and value by selecting the minimal set of tests that provides sufficient confidence.

---

## Preconditions

**Required inputs:**
- A change or feature has been defined
- The system architecture and test landscape are known
- Testing effort must be balanced against cost and value

**Assumed context:**
- Multiple test levels are available (unit, integration, system)
- Test execution time and maintenance cost matter
- Over-testing and under-testing both carry risk

**Exclusions (when NOT to use):**
- When only one test level is available (just use it)
- When test strategy is already determined by standards
- For trivial changes with obvious test requirements

---

## Execution Steps

1. Identify the change being introduced.
2. Assess the **scope of impact**:
   - **Local** — single function or class
   - **Cross-module** — multiple components or services
   - **System-wide** — affects user-visible behavior or data flow
3. Evaluate the **risk of failure**:
   - **High** — data loss, security, correctness of critical logic
   - **Medium** — degraded UX, maintainability, performance
   - **Low** — cosmetic, easily reversible
4. Map the change to testing levels:
   - **Unit tests** for isolated logic and algorithms
   - **Integration tests** for interactions between components
   - **System tests** for end-to-end behavior and user scenarios
5. Select the **minimal set of tests** that provides sufficient confidence given scope and risk.
6. Explicitly document **what is not tested and why**.
7. Stop.

---

## Checks / Exit Criteria
- Chosen test levels align with impact and risk.
- Overlapping or redundant tests are avoided.
- Untested areas are explicitly acknowledged.
- Test strategy is documented (even if brief).

---

## Failure Modes
- Defaulting to one test level for all changes (e.g., "always write unit tests").
- Over-testing low-risk changes (wastes effort and slows feedback).
- Relying solely on end-to-end tests (slow, brittle, hard to debug).
- Under-testing high-risk changes due to time pressure.

---

## Outputs
- Test strategy decision (which levels, why)
- Selected test cases or test plan
- Explicit statement of untested areas

---

## Notes on Use

**Test pyramid guidance:**
- **Many** unit tests — fast, cheap, focused
- **Some** integration tests — validate interactions
- **Few** system tests — validate user-facing behavior

**When to prefer each level:**

**Unit tests when:**
- Change is isolated to a single component
- Logic is algorithmic or conditional
- Fast feedback is critical

**Integration tests when:**
- Change crosses component boundaries
- Side effects or state management are involved
- Interactions are complex or error-prone

**System tests when:**
- Change affects user-visible behavior
- End-to-end workflow must be validated
- Acceptance criteria require observable outcomes

**Cost considerations:**
- Unit tests: low execution time, low maintenance
- Integration tests: moderate execution time, moderate maintenance
- System tests: high execution time, high maintenance

**Risk-based exceptions:**
- High-risk changes may warrant **all three levels**
- Low-risk changes may warrant **unit tests only**
- Refactorings with no behavior change may rely on **existing tests**

---
