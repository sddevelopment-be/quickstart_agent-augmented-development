# Tactic: RED-GREEN-REFACTOR Cycle

**Invoked by:**
- [Directive 017 (TDD)](../directives/017_test_driven_development.md)

**Related tactics:**
- Test-First Development

---

## Intent

Apply the core TDD workflow: write failing test (RED), make it pass (GREEN), improve code (REFACTOR).

## Preconditions

**Required inputs:**
- Feature or bug to implement
- Testing framework available
- Understanding of expected behavior

## Execution Steps

1. **RED Phase: Write Failing Test**
   - Write test for desired behavior
   - Run test - it MUST fail
   - Verify failure reason is correct

2. **GREEN Phase: Make Test Pass**
   - Write minimal code to pass test
   - Run test - it MUST pass
   - No premature optimization

3. **REFACTOR Phase: Improve Code**
   - Improve code structure
   - Keep tests passing
   - Remove duplication

## Expected Outcomes

- Working, tested code
- High test coverage
- Clean, refactored implementation

## Common Pitfalls

- Skipping RED phase (writing passing tests)
- Over-engineering in GREEN phase
- Skipping REFACTOR phase
