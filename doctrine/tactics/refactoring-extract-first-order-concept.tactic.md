# Tactic: Refactoring.ExtractFirstOrderConcept

**Related tactics:**
- `refactoring-strangler-fig.tactic.md` — used when extraction requires incremental approach
- `test-boundaries-by-responsibility.tactic.md` — defines boundaries for extracted concepts

**Complements:**
- [Directive 017 (Test Driven Development)](../directives/017_test_driven_development.md) — ensures behavior preservation during extraction
- Approach: Locality of Change — extraction should be minimal and surgical

---

## Intent
Improve code structure by extracting implicit or duplicated logic into an explicit first-order concept.

Use this tactic to reduce duplication, clarify responsibilities, and make implicit patterns explicit.

---

## Preconditions

**Required inputs:**
- Code contains duplicated, complex, or implicitly shared logic
- Tests exist or can be added to protect behavior
- The extracted concept has a clear responsibility

**Assumed context:**
- Refactoring is permitted and valued
- Tests are available or can be written
- The system allows introduction of new abstractions

**Exclusions (when NOT to use):**
- When duplication is coincidental, not conceptual
- When tests cannot be written or are impractical
- When extraction would introduce more complexity than it removes

---

## Execution Steps

1. Identify the logic to be extracted.
2. Verify current behavior with tests (or add tests if missing).
3. Define the **responsibility** of the new concept in one sentence.
4. Create the new abstraction (class, module, function, delegate).
5. Move the identified logic into the new abstraction.
6. Update callers to use the extracted concept.
7. Re-run tests to verify behavior is preserved.
8. Stop.

---

## Checks / Exit Criteria
- Behavior remains unchanged (tests pass).
- The new concept has a single, clear responsibility.
- Duplication or complexity is measurably reduced.
- Callers are updated consistently.

---

## Failure Modes
- Extracting without a clear responsibility (creating a "utils" dumping ground).
- Creating overly generic abstractions that obscure intent.
- Changing behavior during extraction.
- Extracting too aggressively (premature abstraction).

---

## Outputs
- New first-order concept (class, module, function)
- Updated call sites
- Passing test suite

---

## Notes on Use

**First-order concept** means:
- The abstraction has a clear name and purpose
- It represents a domain or technical concept
- It can be reasoned about independently

**Good extraction candidates:**
- Logic duplicated in 3+ places
- Complex conditionals that represent a policy or rule
- Cross-cutting concerns (logging, validation, formatting)

**Poor extraction candidates:**
- One-time use patterns
- Logic that is inherently context-dependent
- Abstractions that require extensive configuration

**Rule of Three:** Consider extraction when duplication appears in three locations, not two (avoid premature abstraction).

---
