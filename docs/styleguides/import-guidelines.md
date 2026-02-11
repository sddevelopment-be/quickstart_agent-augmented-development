# Import Guidelines for Agent-Augmented Development Framework

**Status:** Active  
**Last Updated:** 2026-02-11  
**Related ADRs:** ADR-046 (Domain Module Refactoring)  

---

## Overview

This document defines import conventions and boundaries for the Agent-Augmented Development Framework. These rules ensure maintainability, modularity, and clear architectural boundaries.

---

## Core Rules

### Rule 1: Always Use `src.` Prefix for Internal Imports

All imports from the framework must use the `src.` prefix to ensure consistency and avoid path resolution issues.

✅ **CORRECT:**
```python
from src.domain.collaboration.task_schema import read_task
from src.domain.doctrine.agent_loader import load_agent
from src.domain.common.version import get_version
from src.framework.orchestration.task_queue import TaskQueue
```

❌ **INCORRECT:**
```python
from domain.collaboration.task_schema import read_task
from common.task_schema import read_task
from framework.orchestration.task_queue import TaskQueue
```

**Rationale:** The `src.` prefix makes imports unambiguous and works consistently across different execution contexts (tests, scripts, installed package).

---

## Domain Module Architecture

The `src.domain` module is organized into **bounded contexts** following Domain-Driven Design principles. Each context is independent and has specific import restrictions.

### Bounded Contexts

1. **`src.domain.common`** - Shared utilities and base types
2. **`src.domain.collaboration`** - Task and workflow management
3. **`src.domain.doctrine`** - Agent definitions and guidelines
4. **`src.domain.specifications`** - Specification parsing and validation

### Rule 2: Bounded Context Independence

Bounded contexts may only import from `src.domain.common`. Cross-context imports are **forbidden**.

✅ **CORRECT:**
```python
# In src/domain/collaboration/task_schema.py
from src.domain.common.version import get_version
from src.domain.common.types import PathLike
```

❌ **INCORRECT:**
```python
# In src/domain/collaboration/task_schema.py
from src.domain.doctrine.agent_loader import load_agent  # ❌ Cross-context
from src.domain.specifications.spec_parser import parse  # ❌ Cross-context
```

**Rationale:** This prevents tight coupling between contexts and allows them to evolve independently.

---

### Rule 3: Domain Layer Must Not Import Framework or Services

The domain layer (`src.domain`) must remain pure and independent of infrastructure concerns.

✅ **CORRECT:**
```python
# In src/domain/collaboration/task_schema.py
from src.domain.common.types import PathLike
from pathlib import Path
import yaml
```

❌ **INCORRECT:**
```python
# In src/domain/collaboration/task_schema.py
from src.framework.orchestration.task_queue import TaskQueue  # ❌ Framework
from src.llm_service.client import LLMClient  # ❌ Service layer
```

**Rationale:** Domain logic should be reusable across different infrastructures and not tied to specific implementations.

---

## Enforcement

### Automated Validation

Import boundaries are enforced using `import-linter`. Configuration is in `.importlinter` and `pyproject.toml`.

**Run validation:**
```bash
lint-imports
```

**Expected output for domain contracts:**
```
Bounded context independence KEPT
No collaboration to doctrine imports KEPT
No doctrine to specifications imports KEPT
Domain isolation from framework KEPT
```

### Architectural Tests

Runtime validation is provided by tests in:
- `tests/integration/test_bounded_context_independence.py`
- `tests/architecture/test_domain_module_architecture.py`

**Run architectural tests:**
```bash
pytest tests/integration/test_bounded_context_independence.py -v
pytest tests/architecture/ -v
```

---

## Common Patterns

### Pattern 1: Cross-Context Communication via Framework

When one context needs functionality from another, use the framework layer as an orchestrator:

```python
# ✅ CORRECT: Framework orchestrates between contexts
# In src/framework/orchestration/task_processor.py

from src.domain.collaboration.task_schema import read_task
from src.domain.doctrine.agent_loader import load_agent

def process_task(task_path: Path) -> None:
    task = read_task(task_path)  # Collaboration context
    agent = load_agent(task.agent_name)  # Doctrine context
    # Orchestration logic here
```

### Pattern 2: Shared Utilities in Common

Place genuinely shared functionality in `src.domain.common`:

```python
# ✅ CORRECT: Shared types in common module
# In src/domain/common/types.py

from typing import Union
from pathlib import Path

PathLike = Union[str, Path]
```

### Pattern 3: Type Hints Without Imports

Use string literals for forward references to avoid circular dependencies:

```python
# ✅ CORRECT: String literal for forward reference
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.doctrine.agent_schema import AgentDefinition

def validate_agent(agent: "AgentDefinition") -> bool:
    pass
```

---

## Migration Guide

### Updating Existing Code

When you encounter incorrect imports:

1. **Identify the violation:**
   ```bash
   lint-imports
   ```

2. **Update the import:**
   ```python
   # Before
   from domain.collaboration.task_schema import read_task
   
   # After
   from src.domain.collaboration.task_schema import read_task
   ```

3. **Verify the fix:**
   ```bash
   lint-imports
   pytest tests/integration/test_bounded_context_independence.py
   ```

### Handling Cross-Context Dependencies

If you need functionality from another context:

1. **Question the dependency:** Is this really needed?
2. **Move to common:** If truly shared, move to `src.domain.common`
3. **Use framework layer:** Orchestrate at the framework level
4. **Refactor:** Consider if the functionality belongs in a different context

---

## Exceptions

### Documented Exceptions

Some legacy code may have violations that are tracked as technical debt:

```python
# TECH DEBT: Remove framework import after refactoring
# See: docs/architecture/decisions/ADR-XXX.md
from src.framework.legacy_util import old_function  # type: ignore[import]
```

**Document all exceptions with:**
- Reason for exception
- Link to ADR or issue tracker
- Plan for resolution

---

## Related Documentation

### Architectural Decisions
- **ADR-046:** Domain Module Refactoring - Core architecture decisions
- **ADR-045:** Doctrine Domain Model - Specific context design

### Code Organization
- **[Python Conventions](python_conventions.md)** - General Python style guide
- **[Architecture Overview](../architecture/README.md)** - High-level architecture

### Testing
- **[Testing Guide](../guides/technical/testing.md)** - Testing strategies
- **Architecture Tests:** Validation of import boundaries

---

## Tools and Configuration

### Import-Linter

**Configuration files:**
- `.importlinter` - Main configuration (legacy format)
- `pyproject.toml` - Additional contracts (modern format)

**Key contracts:**
```toml
[tool.importlinter]
root_package = "src"

[[tool.importlinter.contracts]]
name = "Domain isolation from framework"
type = "forbidden"
source_modules = ["src.domain"]
forbidden_modules = ["src.framework", "src.llm_service"]
```

### Mypy Configuration

Type checking enforces import boundaries at type level:

```toml
[tool.mypy]
python_version = "3.10"
strict = true

[[tool.mypy.overrides]]
module = "src.domain.*"
strict = true
```

---

## FAQ

### Q: Why can't I import from another bounded context?

**A:** Bounded contexts should be independent. If you need shared functionality, either:
- Move it to `src.domain.common` if truly shared
- Orchestrate at the framework layer if it's cross-context business logic

### Q: What if I'm in the framework and need multiple contexts?

**A:** That's fine! The framework layer is the orchestration layer and can import from multiple contexts:

```python
# ✅ Framework can import multiple contexts
from src.domain.collaboration.task_schema import read_task
from src.domain.doctrine.agent_loader import load_agent
```

### Q: How do I handle test imports?

**A:** Test files can import from any module they're testing:

```python
# ✅ Tests can import anything
from src.domain.collaboration.task_schema import read_task
from src.framework.orchestration.task_queue import TaskQueue
```

### Q: What about external library imports?

**A:** External library imports are unrestricted. These rules only apply to internal `src.*` imports:

```python
# ✅ External libraries are fine anywhere
import yaml
from pathlib import Path
from typing import Dict, List
```

---

## Checklist for New Code

Before committing new Python code:

- [ ] All internal imports use `src.` prefix
- [ ] Domain modules don't import from framework/services
- [ ] No cross-context imports in bounded contexts
- [ ] `lint-imports` passes
- [ ] Architecture tests pass
- [ ] Type hints are complete (`mypy` passes)

---

## Version History

| Version | Date       | Changes                                      |
|---------|------------|----------------------------------------------|
| 1.0     | 2026-02-11 | Initial version from ADR-046 implementation  |

---

**Questions?** See [Python Conventions](python_conventions.md) or ask in #architecture channel.
