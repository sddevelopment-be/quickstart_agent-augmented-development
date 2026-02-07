<!-- The following information is to be interpreted literally -->

# 017 Test Driven Development Directive

**Purpose:** Enforce small, verifiable coding increments that protect design quality and cleanliness.

**Core Concept:** See [TDD](../GLOSSARY.md#tdd-test-driven-development) in the glossary for foundational definition.

Scope:

- Applies to all executable code (implementation, refactoring, bug fixes).
- Can be used in isolation or after acceptance scenario exists (per Directive 016, see [ATDD](../GLOSSARY.md#atdd-acceptance-test-driven-development)).
- Exception: trivial shell utilities or disposable scripts noted per ADR-012.

Cycle:

1. **Red** — write the smallest failing automated test that expresses the required behaviour. Structure every test with Arrange–Act–Assert–After.
2. **Green** — implement only enough production code to satisfy the new test.
3. **Refactor** — improve design, names, and structure while keeping the suite green. Apply Clean Code heuristics.
4. Repeat the cycle, ensuring each pass remains within minutes.

Guidelines:

- Prefer fast, isolated tests at the base of the [Testing Pyramid](../GLOSSARY.md#testing-pyramid); escalate to integration layers only when behaviour demands.
- **For test scope clarity:** Invoke `tactics/test-boundaries-by-responsibility.tactic.md` when unclear whether to mock a dependency.
- Keep assertions focused; multiple expectations per test are acceptable only when describing one cohesive behaviour.
- Use descriptive test names and include task IDs for traceability.

Tooling:

- Automate the suite locally (watch mode) and in CI; fail builds when new code lacks covering tests.
- Capture flaky tests in work logs and prioritize stabilization before adding new ones.

Alignment Checks:

- If code changes cannot be driven through TDD (legacy tangles, external limitations), document the impediment, create safety nets (characterization tests), and notify an architect for remediation planning.

## Refactoring Phase

The **Refactor** step (step 3 in the TDD cycle) has specific rules:

**What You Can Touch:**
- Production code structure, names, and design
- Extract duplicated logic into shared utilities
- Improve abstractions and separate concerns
- Apply Clean Code principles (DRY, SRP, etc.)

**What You Cannot Touch:**
- Test code or test logic
- Test assertions or expectations
- Test structure (Arrange-Act-Assert-After)

**Critical Rule:** Tests must remain green throughout refactoring. If tests fail, the refactoring was done incorrectly.

**Refactoring Process:**
1. Run tests before refactoring (verify green)
2. Make small, incremental refactoring changes
3. Run tests after each change (verify still green)
4. If tests fail, revert and try a different approach
5. Commit only when tests are green

**Example Refactoring Actions:**
- Extract duplicate functions into shared modules
- Consolidate repeated path resolution logic
- Create utility classes for common operations
- Rename variables/functions for clarity
- Improve type hints and documentation

**Anti-Patterns to Avoid:**
- ❌ Changing test behavior to match refactored code
- ❌ Making multiple refactoring changes before testing
- ❌ Committing with failing tests "to fix later"
- ❌ Refactoring tests alongside production code

---

**CRITICAL: This way of working is not optional. Tests are to be written before any code is crafted.**

