<!-- Source: 016_acceptance_test_driven_development.md, 017_test_driven_development.md -->
# Testing

**Purpose:** Normalize acceptance-test-first behaviour so user-visible intent anchors every change.

**Core Concept:** See [ATDD](../GLOSSARY.md#atdd-acceptance-test-driven-development) in the glossary for foundational definition.

Scope:

- Applies to features, bug fixes, and refactors that alter externally observable behaviour (API responses, CLI output, workflows, documents).
- Exception: trivial throw-away utilities or single-use shell scripts (log exception in [work log](../GLOSSARY.md#work-log) and reference ADR-012).

Workflow:

1. Capture behaviour as an executable acceptance test (BDD spec, contract test, high-level script) before coding.
2. Reference the scenario ID/ticket/task inside the test metadata.
3. **When defining acceptance boundaries:**
   - **For adversarial edge cases:** Invoke `tactics/ATDD_adversarial-acceptance.tactic.md`
   - **For test scope clarity:** Invoke `tactics/test-boundaries-by-responsibility.tactic.md`
4. Keep acceptance tests close to real workflows—prefer black-box interactions (HTTP endpoints, CLI commands) over internal seams.
5. Use the [Testing Pyramid](../GLOSSARY.md#testing-pyramid) to balance coverage: few but meaningful acceptance tests per capability.
6. Once acceptance tests fail for the right reason, delegate detailed work to [Directive 017 (TDD)](./017_test_driven_development.md) cycles.

Documentation:

- Store acceptance specs with accompanying README or annotations describing inputs/outputs.
- Store requirement files in `${DOC_ROOT}/architecture/requirements/`
- Record links to the acceptance test files inside `${WORKSPACE_ROOT}/reports/logs/<agent>/` or ADRs for traceability.

Integrity Rules:

- Failing acceptance test must exist before implementation begins; document the failure state in the task log.
- Acceptance tests must include clear Arrange/Act/Assert narrative, even if implemented via higher-level tooling.

Alignment Checks:

- If an acceptance test cannot be automated (hardware limitations, external vendors), document the manual fallback and review with an architect.




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
