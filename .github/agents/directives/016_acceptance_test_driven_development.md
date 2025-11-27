<!-- The following information is to be interpreted literally -->
# 016 Acceptance Test Driven Development Directive

**Purpose:** Normalize acceptance-test-first behaviour so user-visible intent anchors every change.

**Core Concept:** See [ATDD](../GLOSSARY.md#atdd-acceptance-test-driven-development) in the glossary for foundational definition.

Scope:
- Applies to features, bug fixes, and refactors that alter externally observable behaviour (API responses, CLI output, workflows, documents).
- Exception: trivial throw-away utilities or single-use shell scripts (log exception in [work log](../GLOSSARY.md#work-log) and reference ADR-012).

Workflow:
1. Capture behaviour as an executable acceptance test (BDD spec, contract test, high-level script) before coding.
2. Reference the scenario ID/ticket/task inside the test metadata.
3. Keep acceptance tests close to real workflows—prefer black-box interactions (HTTP endpoints, CLI commands) over internal seams.
4. Use the [Testing Pyramid](../GLOSSARY.md#testing-pyramid) to balance coverage: few but meaningful acceptance tests per capability.
5. Once acceptance tests fail for the right reason, delegate detailed work to [TDD](../GLOSSARY.md#tdd-test-driven-development) cycles.

Documentation:
- Store acceptance specs with accompanying README or annotations describing inputs/outputs.
- Store requirement files in `docs/architecture/requirements/`
- Record links to the acceptance test files inside `work/reports/logs/<agent>/` or ADRs for traceability.

Integrity Rules:
- Failing acceptance test must exist before implementation begins; document the failure state in the task log.
- Acceptance tests must include clear Arrange/Act/Assert narrative, even if implemented via higher-level tooling.

Alignment Checks:
- If an acceptance test cannot be automated (hardware limitations, external vendors), document the manual fallback and review with an architect.

