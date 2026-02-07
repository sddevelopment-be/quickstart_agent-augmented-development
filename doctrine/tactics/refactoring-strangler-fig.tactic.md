# Tactic: Refactoring.StranglerFig

**Related tactics:**
- `refactoring-extract-first-order-concept.tactic.md` — atomic extraction pattern for simpler cases
- `safe-to-fail-experiment-design.tactic.md` — provides low-risk validation for each rerouting step

**Complements:**
- [Directive 017 (Test Driven Development)](../directives/017_test_driven_development.md) — ensures safety during incremental replacement
- Approach: Trunk-Based Development — short-lived branches for each rerouting step

---

## Intent
Refactor or replace existing functionality incrementally by introducing a new implementation alongside the old and gradually rerouting behavior.

Use this tactic when large-scale refactoring or replacement cannot be done safely in a single step.

---

## Preconditions

**Required inputs:**
- Existing behavior is covered by tests or can be validated
- The system allows coexistence of old and new paths
- Refactoring cannot be done in a single step (too risky or complex)

**Assumed context:**
- Incremental deployment is possible
- Tests can verify equivalence between old and new behavior
- Temporary duplication is acceptable

**Exclusions (when NOT to use):**
- When a single-step refactoring is safe and sufficient
- When the system architecture prevents coexistence of implementations
- When tests are unavailable and cannot be created

---

## Execution Steps

1. Identify the behavior to be replaced.
2. Add or verify tests for current behavior.
3. Implement the **new behavior alongside** the existing one (do not remove old code yet).
4. Duplicate behavior where necessary to match outcomes exactly.
5. Gradually **reroute calls** from old to new implementation (one call site or module at a time).
6. Run tests after **each reroute** to verify equivalence.
7. Remove unused old implementation once all calls are rerouted.
8. Run final comprehensive tests.
9. Stop.

---

## Checks / Exit Criteria
- Tests pass after each rerouting step.
- No callers depend on the old implementation.
- Old code has been safely removed.
- System behavior is unchanged from external perspective.

---

## Failure Modes
- Rerouting without test coverage (high risk of silent breakage).
- Mixing refactoring with feature changes or behavior modifications.
- Removing old code prematurely (before all reroutes complete).
- Allowing old and new implementations to diverge over time.

---

## Outputs
- Incrementally refactored implementation
- Updated test suite
- Removed legacy code

---

## Notes on Use

**Origin:** The "Strangler Fig" pattern is named after a type of plant that grows around a host tree, eventually replacing it entirely. The metaphor captures the incremental replacement approach.

**Key principle:** Coexistence before removal.

**Rerouting strategies:**
- **By call site** — replace one caller at a time
- **By feature flag** — toggle between old and new at runtime
- **By module** — replace one subsystem boundary at a time
- **By percentage** — gradually shift traffic from old to new

**Safety mechanisms:**
- Run old and new in parallel, compare outputs (shadow mode)
- Use feature flags to quickly roll back if issues arise
- Monitor metrics during rerouting to detect regressions

This tactic is particularly useful for:
- Replacing legacy subsystems
- Migrating to new frameworks or libraries
- Large architectural refactorings

---
