# Python Conventions & Style Guide

**Version:** 1.0.0  
**Last Updated:** 2025-11-29  
**Status:** Active

---

## Purpose

This document captures Python coding conventions and best practices learned through implementing and maintaining the orchestration automation framework. These guidelines ensure consistency, readability, and maintainability across the codebase.

---

## Table of Contents

1. [Formatting & Style](#formatting--style)
2. [Test Structure (Quad-A Pattern)](#test-structure-quad-a-pattern)
3. [Validation & Guard Clauses](#validation--guard-clauses)
4. [Type Hints](#type-hints)
5. [String Formatting](#string-formatting)
6. [Testing Pyramid](#testing-pyramid)
7. [Tooling](#tooling)

---

## Formatting & Style

### Use Black for Consistent Formatting

**Tool:** `black` (version 25.11.0+)

**Command:**
```bash
python -m black path/to/file.py
```

**What Black Handles:**
- Line length (88 characters default)
- Consistent spacing around operators
- String quote normalization (prefer double quotes)
- Trailing commas in multi-line structures
- Blank line management

**Example:**
```python
# Before
def function(arg1,arg2,arg3):
    return{
        'key1':arg1,'key2':arg2,
        'key3':arg3
    }

# After (Black formatted)
def function(arg1, arg2, arg3):
    return {
        "key1": arg1,
        "key2": arg2,
        "key3": arg3,
    }
```

### Use Ruff for Linting

**Tool:** `ruff` (version 0.14.7+)

**Command:**
```bash
python -m ruff check path/to/file.py --fix
```

**What Ruff Catches:**
- Unused imports
- Undefined variables
- Code quality issues
- Common anti-patterns
- PEP 8 violations

---

## Test Structure (Quad-A Pattern)

### The Correct Quad-A Structure

Tests MUST follow the **Arrange - Assumption Check - Act - Assert** pattern:

1. **Arrange** — Set up test preconditions (create objects, seed data, configure mocks)
2. **Assumption Check** — Validate that the arranged state matches expected preconditions
3. **Act** — Execute the behavior under test (single operation when possible)
4. **Assert** — Verify the expected outcomes

**Key Principle:** The Assumption Check validates that your test setup created the scenario you intended to test. This catches test setup bugs early.

### Example: Testing File Operations

```python
def test_read_task_valid_file(temp_task_dir: Path, sample_task: dict) -> None:
    """Test reading a valid task YAML file."""
    # Arrange
    task_file = temp_task_dir / "task.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(sample_task, f, default_flow_style=False, sort_keys=False)

    # Assumption Check
    assert task_file.exists(), "Test precondition failed: task file should exist"

    # Act
    result = read_task(task_file)

    # Assert
    assert result == sample_task
    assert result["id"] == "2025-11-28T2000-test-agent-sample-task"
```

### Example: Testing Error Conditions

When testing that a system correctly handles non-existent files:

```python
def test_read_task_missing_file(temp_task_dir: Path) -> None:
    """Test reading a non-existent file raises FileNotFoundError."""
    # Arrange
    task_file = temp_task_dir / "missing.yaml"

    # Assumption Check
    assert not task_file.exists(), "Test precondition failed: file should NOT exist"

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        read_task(task_file)
```

### Example: Testing Directory Creation

```python
def test_write_task_creates_parent_dirs(tmp_path: Path, sample_task: dict) -> None:
    """Test writing task creates parent directories if missing."""
    # Arrange
    task_file = tmp_path / "nested" / "dirs" / "task.yaml"

    # Assumption Check
    assert not task_file.exists(), "Test precondition failed: file should NOT exist"
    assert not task_file.parent.exists(), "Test precondition failed: parent dir should NOT exist"

    # Act
    write_task(task_file, sample_task)

    # Assert
    assert task_file.exists()
    assert task_file.parent.exists()
```

### What NOT to Do

❌ **Don't skip Assumption Checks:**
```python
def test_something():
    # Arrange
    file_path = setup_file()  # What if this fails?
    
    # Act
    result = process(file_path)  # Fails with confusing error
    
    # Assert
    assert result.is_ok()
```

❌ **Don't use "After" for cleanup (use fixtures instead):**
```python
def test_something():
    # Arrange
    file = create_file()
    
    # Act
    result = process(file)
    
    # Assert
    assert result
    
    # After - WRONG! Use pytest fixtures for cleanup
    cleanup_file(file)
```

✅ **Do use pytest fixtures for automatic cleanup:**
```python
@pytest.fixture
def temp_file(tmp_path):
    """Fixture provides temp file with automatic cleanup."""
    file_path = tmp_path / "test.txt"
    yield file_path
    # Cleanup happens automatically via tmp_path fixture
```

---

## Validation & Guard Clauses

### Prefer Guard Clauses Over Nested Conditionals

**Principle:** Validate inputs early and fail fast rather than nesting logic in conditional branches.

**Pattern:** Check for invalid conditions at the start of a function and raise exceptions immediately.

### Example: Input Validation

❌ **Don't use nested if-else:**
```python
def process_task(task: dict) -> dict:
    if task.get("agent"):
        if task.get("status") == "new":
            # Do work
            return {"result": "processed"}
        else:
            return {"error": "Invalid status"}
    else:
        return {"error": "Missing agent"}
```

✅ **Do use guard clauses:**
```python
def process_task(task: dict) -> dict:
    """Process a task with early validation."""
    # Guard clauses: validate and fail early
    if not task.get("agent"):
        raise ValueError("Task missing required 'agent' field")
    
    if task.get("status") != "new":
        raise ValueError(f"Invalid task status: {task.get('status')}")
    
    # Main logic with clean, single-purpose flow
    return {"result": "processed"}
```

### Example: File Operations

❌ **Don't nest file checks:**
```python
def read_config(path: Path) -> dict:
    if path.exists():
        if path.is_file():
            with open(path) as f:
                return yaml.safe_load(f)
        else:
            raise ValueError("Path is not a file")
    else:
        raise FileNotFoundError(f"Config not found: {path}")
```

✅ **Do check conditions sequentially:**
```python
def read_config(path: Path) -> dict:
    """Read configuration file with upfront validation."""
    # Guard clauses
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    
    # Main logic
    with open(path) as f:
        return yaml.safe_load(f)
```

### Benefits of Guard Clauses

1. **Clarity:** Each validation is explicit and independent
2. **Maintainability:** Easy to add/remove validations
3. **Error Messages:** Specific, actionable error information
4. **Reduced Nesting:** Flatter code is easier to read
5. **Performance:** Fail fast on invalid inputs

---

## Type Hints

### Always Type-Hint Public Functions

**Standard:** All public functions MUST have type hints for parameters and return values.

```python
from pathlib import Path
from typing import Any, Dict

def read_task(task_file: Path) -> Dict[str, Any]:
    """Load task YAML file.
    
    Args:
        task_file: Path to task YAML file
        
    Returns:
        Dictionary containing task data
    """
    with open(task_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
```

### Use Modern Type Hints (Python 3.10+)

```python
# Prefer built-in types over typing module when possible
from pathlib import Path

def process(data: dict[str, any]) -> list[str]:
    """Modern type hints using built-in types."""
    return list(data.keys())

# For union types, use | operator
def get_value(key: str) -> str | None:
    """Returns string or None."""
    return data.get(key)
```

### When to Use `from __future__ import annotations`

Add this import at the top of files using forward references:

```python
from __future__ import annotations

from pathlib import Path

def process_task(task_file: Path) -> Task:  # Task not yet defined
    """Forward reference works with future annotations."""
    pass

class Task:
    """Defined after being referenced."""
    pass
```

---

## String Formatting

### Always Use f-strings

**Standard:** Use f-strings for all string formatting (Python 3.6+).

❌ **Don't use:**
```python
# Old-style formatting
message = "Task %s assigned to %s" % (task_id, agent)

# .format() method
message = "Task {} assigned to {}".format(task_id, agent)

# String concatenation
message = "Task " + task_id + " assigned to " + agent
```

✅ **Do use f-strings:**
```python
message = f"Task {task_id} assigned to {agent}"

# With expressions
message = f"Processed {len(tasks)} tasks in {elapsed:.2f}s"

# Multi-line
message = (
    f"Task {task['id']} completed:\n"
    f"  Agent: {task['agent']}\n"
    f"  Status: {task['status']}"
)
```

### Benefits of f-strings

1. **Readability:** Variables inline with text
2. **Performance:** Faster than other methods
3. **Debugging:** Easy to add debug expressions
4. **Type Safety:** Works well with type checkers

---

## Testing Pyramid

### Maintain Proper Test Distribution

Our test suite follows the Testing Pyramid pattern:

```
        /\
       /  \  E2E Tests (17% - 11 tests)
      /----\  Realistic workflows, slower
     /      \ 
    /--------\
   /          \ Unit Tests (83% - 55 tests)
  /____________\ Fast, isolated, focused
```

### Guidelines

1. **83% Unit Tests:** Fast, isolated function/method tests
   - Execution time: <0.3 seconds for all unit tests
   - Each test validates single behavior
   - Use fixtures for test isolation

2. **17% E2E Tests:** Complete workflow validation
   - Execution time: <0.2 seconds for all E2E tests
   - Test component interactions
   - Simulate real-world scenarios

3. **No Integration Tests (Yet):** None needed without external dependencies
   - Add when integrating with databases, APIs, or external services

### Test Speed Target

- Individual test: <10ms average
- Full unit suite: <1 second
- Full test suite: <1 second total
- CI/CD execution: <5 seconds with overhead

---

## Tooling

### Required Development Tools

```bash
# Install formatting and linting tools
pip install black ruff pytest pyyaml

# Or use requirements-dev.txt
pip install -r requirements-dev.txt
```

### Pre-commit Workflow

```bash
# Format all Python files
python -m black .

# Lint and auto-fix issues
python -m ruff check . --fix

# Run tests
python -m pytest validation/ -v

# Type check (if mypy is configured)
python -m mypy src/
```

### VS Code Configuration

Add to `.vscode/settings.json`:

```json
{
    "python.formatting.provider": "black",
    "python.linting.ruffEnabled": true,
    "python.linting.enabled": true,
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true
}
```

---

## Module Structure

### Preferred Layout

```
project/
├── src/                    # Source code (if using src layout)
│   └── package/
│       ├── __init__.py
│       └── module.py
├── ops/                    # Operations/scripts (alternative to src)
│   └── scripts/
│       └── module.py
├── tests/                  # or validation/
│   ├── test_module.py
│   └── fixtures/
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── pyproject.toml         # Optional: poetry/build config
```

### Import Organization

```python
"""Module docstring."""

# Future imports first
from __future__ import annotations

# Standard library imports
import sys
from datetime import datetime, timezone
from pathlib import Path

# Third-party imports
import pytest
import yaml

# Local imports
from module import function
```

---

## Documentation

### Docstring Format

Use Google-style docstrings:

```python
def process_task(task_file: Path, validate: bool = True) -> dict[str, Any]:
    """Process a task file and return result.
    
    Longer description of what this function does,
    including any important details or edge cases.
    
    Args:
        task_file: Path to the task YAML file
        validate: Whether to validate task schema (default: True)
        
    Returns:
        Dictionary containing processed task data with keys:
        - id: Task identifier
        - status: Processing status
        - result: Processing outcome
        
    Raises:
        FileNotFoundError: If task_file doesn't exist
        ValueError: If task schema is invalid and validate=True
        
    Example:
        >>> result = process_task(Path("task.yaml"))
        >>> print(result["status"])
        'completed'
    """
    pass
```

---

## Common Patterns

### Working with Paths

```python
from pathlib import Path

# ✅ Use Path objects, not strings
config_file = Path("config") / "settings.yaml"

# ✅ Check existence before operations
if not config_file.exists():
    raise FileNotFoundError(f"Config not found: {config_file}")

# ✅ Create parent directories
output_file = Path("output") / "result.txt"
output_file.parent.mkdir(parents=True, exist_ok=True)

# ✅ Use context managers for file operations
with open(config_file, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
```

### Working with Timestamps

```python
from datetime import datetime, timezone

# ✅ Always use UTC with timezone info
now = datetime.now(timezone.utc)

# ✅ ISO format with Z suffix
timestamp = now.isoformat().replace("+00:00", "Z")
# Result: "2025-11-29T06:00:00Z"

# ✅ Parse ISO timestamps
dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
```

### Working with YAML

```python
import yaml

# ✅ Write YAML preserving order
with open(file_path, "w", encoding="utf-8") as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)

# ✅ Read YAML safely
with open(file_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f) or {}  # Return {} if empty
```

---

## References

- **Style Guide:** `approaches/style-execution-primers.md`
- **Quad-A Testing:** `${WORKSPACE_ROOT}/notes/ideation/opinionated_platform/opinions/quad_A_test_structure.md`
- **Testing Pyramid:** `${WORKSPACE_ROOT}/notes/ideation/opinionated_platform/opinions/testing_pyramid.md`
- **Test Coverage:** `validation/TEST_COVERAGE.md`
- **Pyramid Analysis:** `validation/TEST_PYRAMID_ANALYSIS.md`

---

## Version History

| Version | Date       | Changes                                      |
|---------|------------|----------------------------------------------|
| 1.0.0   | 2025-11-29 | Initial version from test implementation work|

---

**Maintained by:** Build Automation Team  
**Review Cycle:** Quarterly or when significant patterns emerge
