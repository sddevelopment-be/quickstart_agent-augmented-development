# Test-First Development Approach

**Approach Type:** Problem-Solving Technique
**Status:** Active
**Last Updated:** 2026-02-11

## Purpose

Improve code quality and design by writing tests before implementation code.

## Principles

1. **Tests Define Behavior:** Tests specify what code should do
2. **Design Emerges:** Good design emerges from testable code
3. **Confidence Through Coverage:** Tests provide safety net for refactoring
4. **Documentation:** Tests serve as executable documentation

## When to Use

- New feature development
- Bug fixes with reproduction cases
- Refactoring existing code
- API design and contracts

## When to Avoid

- Quick prototypes or spikes
- Exploratory programming
- Well-established patterns (copy-paste with tests)
- Non-deterministic systems (hard to test)

## Related Directives

- Directive 016: ATDD
- Directive 017: TDD
- Directive 028: Bug Fixing Techniques

## Implementation Guidelines

**Step 1: Write Test**
```python
def test_feature():
    result = new_feature(input_data)
    assert result == expected_output
```

**Step 2: See It Fail**
```bash
$ pytest test_feature.py
FAILED - NameError: new_feature not defined
```

**Step 3: Implement**
```python
def new_feature(data):
    return process(data)
```

**Step 4: Pass and Refactor**
```bash
$ pytest test_feature.py
PASSED
```
