# Architecture Decision Records

## ADR-012: Default to ATDD + TDD for Code Changes

**status**: Accepted  
**date**: 2025-11-24

### Context

Reference material in `tmp/reference_docs` (Testing Pyramid, Quadruple-A structure, Clean Code) reinforces that high-quality systems depend on a consistent, test-first practice. Our current guidance encourages testing but does not mandate how agents approach new or modified code. Inconsistent styles complicate collaboration, reduce traceability, and undermine observability of automated pipelines.

### Decision

1. **Acceptance Test Driven Development (ATDD)** becomes the default starting point for any feature or change that has observable behaviour. Capture the customer-facing scenario first (e.g., executable acceptance test, contract, or high-level automation) before implementing internals.
2. **Test Driven Development (TDD)** governs the implementation phase: write the smallest failing automated test, implement to pass, and refactor. Use the quadruple-A (Arrange–Act–Assert–After) structure for readability.
3. **Exceptions:** truly trivial throw-away scripts or one-off shell commands may bypass ATDD/TDD, but they must be flagged as such in work logs, and automation should remain minimal.

### Rationale

- **Traceable quality:** ATDD provides a contract that links stakeholder intent to automated checks, aligning with the Testing Pyramid’s emphasis on behavioural coverage.
- **Design feedback:** TDD enforces small, reviewable steps that keep code clean and evolveable, echoing the Clean Code primer.
- **Suite health:** Using the quadruple-A structure keeps tests maintainable and diagnosable, reducing friction when agents hand work off.
- **Governance simplicity:** A unified approach allows directives and tooling to reason about expected artefacts (e.g., acceptance specs + unit specs) and surface gaps early.

### Envisioned Consequences

**Positive**
- ✅ Improved confidence in refactors because behavioural contracts exist before code changes.
- ✅ Easier onboarding for new agents—everyone follows the same cadence.
- ✅ Clear hooks for automation (pre-commit, CI) to verify required tests exist.

**Negative / Watch-outs**
- ⚠️ Perceived overhead for very small changes; mitigated by explicit exception policy.
- ⚠️ Requires investment in fixtures/builders for ATDD/TDD to stay ergonomic.
- ⚠️ Legacy areas without tests will need bootstrap time; plan spikes accordingly.

### Considered Alternatives

1. **Status quo (encourage but don’t require test-first).** Rejected: leads to drift and uneven quality.
2. **Rely solely on integration or exploratory testing.** Rejected: conflicts with Testing Pyramid best practices and slows feedback.
3. **Mandate TDD only.** Rejected: misses stakeholder-facing acceptance criteria and weakens alignment with socio-technical goals.
