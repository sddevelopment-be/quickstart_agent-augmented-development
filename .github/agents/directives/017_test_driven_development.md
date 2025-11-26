<!-- The following information is to be interpreted literally -->
# 017 Test Driven Development Directive

Purpose: Enforce small, verifiable coding increments that protect design quality and cleanliness.

Scope:
- Applies after an acceptance scenario exists (per Directive 016) and continues through implementation/refinement.
- Exception: trivial shell utilities or disposable scripts noted per ADR-012.

Cycle:
1. **Red** — write the smallest failing automated test that expresses the required behaviour. Structure every test with Arrange–Act–Assert–After.
2. **Green** — implement only enough production code to satisfy the new test.
3. **Refactor** — improve design, names, and structure while keeping the suite green. Apply Clean Code heuristics.
4. Repeat the cycle, ensuring each pass remains within minutes.

Guidelines:
- Prefer fast, isolated tests at the base of the Testing Pyramid; escalate to integration layers only when behaviour demands.
- Keep assertions focused; multiple expectations per test are acceptable only when describing one cohesive behaviour.
- Use descriptive test names and include task IDs for traceability.

Tooling:
- Automate the suite locally (watch mode) and in CI; fail builds when new code lacks covering tests.
- Capture flaky tests in work logs and prioritize stabilization before adding new ones.

Alignment Checks:
- If code changes cannot be driven through TDD (legacy tangles, external limitations), document the impediment, create safety nets (characterization tests), and notify an architect for remediation planning.

