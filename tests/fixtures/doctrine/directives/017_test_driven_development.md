---
category: testing
scope: all-agents
enforcement: mandatory
version: "1.0"
status: active
tags:
  - testing
  - tdd
---

# Directive 017: Test Driven Development

## Description

Apply Test Driven Development (TDD) for all code changes. Write failing tests first,
implement code to pass tests, then refactor while keeping tests green.

## Rationale

TDD ensures code is testable, reduces bugs, and provides living documentation through tests.
The RED-GREEN-REFACTOR cycle enforces discipline and prevents untested code from entering the codebase.

## Examples

**Example 1: RED-GREEN-REFACTOR Cycle**

```python
# RED: Write failing test
def test_user_validation():
    assert validate_email("invalid") == False

# GREEN: Make it pass
def validate_email(email):
    return "@" in email

# REFACTOR: Improve implementation
import re
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))
```

**Example 2: Test First Bug Fix**

```python
# Reproduce bug with failing test
def test_division_by_zero_handled():
    result = safe_divide(10, 0)
    assert result is None  # Should not raise exception
```
