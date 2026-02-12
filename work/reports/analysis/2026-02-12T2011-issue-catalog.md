# Issue Catalog - Concrete Examples

**Project:** sddevelopment-be/quickstart_agent-augmented-development  
**Analysis Date:** 2026-02-12  
**Purpose:** Detailed examples of each issue type for developer reference

---

## 1. Security Issues (Bandit)

### HIGH Severity: None detected ✅

### MEDIUM Severity (2 issues)

#### B108: Insecure Temporary File/Directory Usage

**Location:** `src/framework/orchestration/benchmark_orchestrator.py:44`

**Issue:**
```python
TEST_WORK_DIR = Path("/tmp/benchmark_work")
```

**Problem:**
- Hardcoded `/tmp/` path vulnerable to:
  - Race conditions (TOCTOU attacks)
  - Predictable naming (security risk)
  - Permission issues on shared systems
  - Cross-platform incompatibility

**Fix:**
```python
import tempfile
from pathlib import Path

def create_benchmark_workdir() -> Path:
    """Create secure temporary directory for benchmarks."""
    return Path(tempfile.mkdtemp(prefix="benchmark_work_", suffix="_test"))

# Usage
TEST_WORK_DIR = create_benchmark_workdir()

# Cleanup
import atexit
import shutil

def cleanup_workdir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)

atexit.register(cleanup_workdir, TEST_WORK_DIR)
```

**Impact:** MEDIUM - Potential security vulnerability in multi-user environments  
**Effort:** 2 hours

---

### LOW Severity (22 issues)

#### B110: Try-Except-Pass (Silent Error Suppression)

**Location 1:** `src/domain/collaboration/types.py:74`

**Issue:**
```python
try:
    return agent_name in valid_agents
except Exception:
    # Fallback to Literal type if dynamic loading fails
    pass
```

**Problem:**
- Errors are silently ignored
- No logging for debugging
- Implicit fallback behavior (returns None)
- Makes troubleshooting difficult

**Fix:**
```python
import logging

logger = logging.getLogger(__name__)

try:
    return agent_name in valid_agents
except Exception as e:
    logger.warning(
        f"Failed to validate agent '{agent_name}': {e}. "
        "Falling back to static validation.",
        exc_info=True  # Include stack trace in debug logs
    )
    return False  # Explicit fallback
```

**Impact:** LOW - Debugging difficulty  
**Effort:** 30 minutes per occurrence (4 occurrences = 2 hours)

---

#### B603: Subprocess Call Without Input Validation

**Location:** `src/framework/context/assemble-agent-context.py:104`

**Issue:**
```python
result = subprocess.run(
    [sys.executable, str(self.directive_loader)] + directive_codes,
    capture_output=True,
    text=True,
    check=True,
)
```

**Problem:**
- `directive_codes` could contain shell metacharacters
- No validation of input parameters
- Potential command injection if input is user-controlled

**Fix:**
```python
import subprocess
import shlex
from pathlib import Path

def validate_directive_code(code: str) -> str:
    """Validate directive code is alphanumeric with hyphens/underscores.
    
    Args:
        code: Directive code to validate
        
    Returns:
        Validated code
        
    Raises:
        ValueError: If code contains invalid characters
    """
    if not code.replace("-", "").replace("_", "").isalnum():
        raise ValueError(f"Invalid directive code: {code}")
    return code

def load_directives_safe(loader_path: Path, codes: list[str]) -> str:
    """Safely load directives with validated inputs."""
    # Validate all codes
    validated = [validate_directive_code(c) for c in codes]
    
    # Build command safely
    cmd = [sys.executable, str(loader_path.resolve())] + validated
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
        timeout=30,  # Prevent hanging
    )
    return result.stdout
```

**Impact:** LOW - Risk only if user-controlled input  
**Effort:** 2 hours

---

## 2. Code Style Issues (Ruff)

### W293: Blank Line Contains Whitespace (617 occurrences)

**Example:** Various files

**Issue:**
```python
def function_one():
    pass
    
def function_two():  # Line has spaces/tabs
    pass
```

**Fix:** Auto-fixable with `ruff check --fix`

**Impact:** TRIVIAL - Visual noise in diffs  
**Effort:** Automated (1 minute)

---

### UP006: Use Built-in Types (104 occurrences)

**Example:** `framework/core.py:45`

**Issue:**
```python
from typing import List, Dict

def get_items() -> List[str]:
    return ["item1", "item2"]
```

**Fix:** Auto-fixable
```python
def get_items() -> list[str]:
    return ["item1", "item2"]
```

**Rationale:** Python 3.9+ supports built-in generic types (PEP 585)

**Impact:** LOW - Modernization  
**Effort:** Automated

---

### UP045: Use Union Syntax (68 occurrences)

**Example:** `framework/core.py:77`

**Issue:**
```python
from typing import Optional

def process(value: Optional[str]) -> str:
    return value or "default"
```

**Fix:** Auto-fixable
```python
def process(value: str | None) -> str:
    return value or "default"
```

**Rationale:** Python 3.10+ supports `X | Y` syntax (PEP 604)

**Impact:** LOW - Modernization  
**Effort:** Automated

---

### F401: Unused Import (15 occurrences)

**Example:** `framework/core.py:17`

**Issue:**
```python
from typing import Dict, List, Optional, Any

# Any is never used in the file
```

**Fix:** Auto-fixable
```python
from typing import Dict, List, Optional
```

**Impact:** LOW - Code cleanliness  
**Effort:** Automated

---

### B904: Raise Without 'from' (14 occurrences)

**Example:** Various files

**Issue:**
```python
try:
    data = parse_file(path)
except ValueError:
    raise ParsingError("Failed to parse file")
```

**Fix:** Manual
```python
try:
    data = parse_file(path)
except ValueError as e:
    raise ParsingError("Failed to parse file") from e
```

**Rationale:** Preserves original exception context (PEP 3134)

**Impact:** MEDIUM - Debugging experience  
**Effort:** 10 minutes per occurrence (14 × 10min = 2.3 hours)

---

## 3. Type Annotation Issues (MyPy)

### Missing Return Type Annotation (37 occurrences)

**Example:** `src/llm_service/telemetry/logger.py:105`

**Issue:**
```python
def log_event(self, event_type: str, data: dict):
    """Log an event."""
    self.events.append({"type": event_type, "data": data})
```

**MyPy Error:**
```
logger.py:105: error: Function is missing a return type annotation  [no-untyped-def]
logger.py:105: note: Use "-> None" if function does not return a value
```

**Fix:**
```python
from typing import Any

def log_event(self, event_type: str, data: dict[str, Any]) -> None:
    """Log an event to the event store.
    
    Args:
        event_type: Type of event (e.g., 'task_created', 'agent_assigned')
        data: Event data with arbitrary structure
    """
    self.events.append({"type": event_type, "data": data})
```

**Impact:** MEDIUM - Type safety  
**Effort:** 5 minutes per function (37 × 5min = 3 hours)

---

### Missing Generic Type Parameters (31 occurrences)

**Example:** `src/llm_service/dashboard/progress_calculator.py:65`

**Issue:**
```python
def calculate_progress(tasks: list) -> dict:
    """Calculate progress statistics."""
    return {"total": len(tasks), "completed": 0}
```

**MyPy Error:**
```
progress_calculator.py:65: error: Missing type parameters for generic type "dict"  [type-arg]
```

**Fix:**
```python
from typing import Any

def calculate_progress(tasks: list[dict[str, Any]]) -> dict[str, int]:
    """Calculate progress statistics.
    
    Args:
        tasks: List of task dictionaries
        
    Returns:
        Dictionary with 'total' and 'completed' counts
    """
    return {"total": len(tasks), "completed": 0}
```

**Impact:** MEDIUM - Type safety  
**Effort:** 5-10 minutes per occurrence (31 × 7.5min = 4 hours)

---

### Library Stubs Not Installed (10 occurrences)

**Example:** `src/domain/collaboration/task_schema.py:13`

**Issue:**
```python
import yaml  # Untyped import
```

**MyPy Error:**
```
task_schema.py:13: error: Library stubs not installed for "yaml"  [import-untyped]
task_schema.py:13: note: Hint: "python3 -m pip install types-PyYAML"
```

**Fix:**
```bash
pip install types-PyYAML types-Flask-SocketIO types-Flask-Cors types-psutil
```

**Impact:** MEDIUM - Type checking coverage  
**Effort:** 10 minutes (one-time installation)

---

### Function Missing Type Annotation (22 occurrences)

**Example:** `src/llm_service/cli.py:38`

**Issue:**
```python
def setup_logging(verbose):
    """Configure logging based on verbosity."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
```

**MyPy Error:**
```
cli.py:38: error: Function is missing a type annotation  [no-untyped-def]
```

**Fix:**
```python
def setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity level.
    
    Args:
        verbose: If True, enable DEBUG level; otherwise INFO level
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
```

**Impact:** HIGH - Type safety for parameters  
**Effort:** 5-10 minutes per function (22 × 7.5min = 2.75 hours)

---

### Untyped Decorator (2 occurrences)

**Example:** `src/framework/orchestration/example_agent.py:90`

**Issue:**
```python
@timing_decorator
def execute_task(self, task):
    """Execute a task."""
    pass
```

**MyPy Error:**
```
example_agent.py:90: error: Untyped decorator makes function "execute_task" untyped  [untyped-decorator]
```

**Fix 1: Type the Decorator**
```python
from typing import Callable, TypeVar, Any
from functools import wraps

F = TypeVar('F', bound=Callable[..., Any])

def timing_decorator(func: F) -> F:
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper  # type: ignore[return-value]
```

**Fix 2: Type Ignore with Comment**
```python
@timing_decorator  # type: ignore[misc]
def execute_task(self, task: Task) -> None:
    """Execute a task."""
    pass
```

**Impact:** MEDIUM - Type propagation  
**Effort:** 15-30 minutes per decorator (2 × 22.5min = 45 minutes)

---

### Value Not Indexable (4 occurrences)

**Example:** `src/llm_service/dashboard/file_watcher.py:206`

**Issue:**
```python
from typing import Collection

class FileWatcher:
    def __init__(self):
        self.files: Collection[str] = []
    
    def add_file(self, filename: str):
        self.files.append(filename)  # Error: Collection doesn't have append
```

**MyPy Error:**
```
file_watcher.py:206: error: "Collection[str]" has no attribute "append"  [attr-defined]
```

**Fix:**
```python
from typing import List  # or list in Python 3.9+

class FileWatcher:
    def __init__(self):
        self.files: list[str] = []
    
    def add_file(self, filename: str) -> None:
        self.files.append(filename)
```

**Explanation:** `Collection` is abstract and doesn't guarantee mutation methods. Use `list` for mutable sequences.

**Impact:** HIGH - Incorrect type annotation  
**Effort:** 5 minutes per occurrence (4 × 5min = 20 minutes)

---

## 4. Architecture Issues

### Import Not Found (5+ occurrences)

**Example:** `src/framework/orchestration/example_agent.py:23`

**Issue:**
```python
from agent_base import AgentBase  # Can't find module
```

**MyPy Error:**
```
example_agent.py:23: error: Cannot find implementation or library stub for module named "agent_base"  [import-not-found]
```

**Root Cause:** Module not in PYTHONPATH or missing `__init__.py`

**Fix:**
```python
# Correct relative import
from framework.orchestration.agent_base import AgentBase

# Or absolute import from src
from src.framework.orchestration.agent_base import AgentBase
```

**Verification:**
```bash
# Check PYTHONPATH
python -c "import sys; print('\n'.join(sys.path))"

# Verify module structure
tree src/framework/orchestration/
```

**Impact:** HIGH - Build/import failure  
**Effort:** 15 minutes per occurrence

---

## 5. Bug Example

### Unreachable Code

**Location:** `src/domain/collaboration/task_validator.py:44`

**Issue:** (Hypothetical based on MyPy warning)
```python
def validate_task_status(status: str) -> bool:
    """Validate task status value."""
    valid_statuses = ["pending", "in_progress", "completed"]
    
    if status not in valid_statuses:
        return False
        print(f"Invalid status: {status}")  # UNREACHABLE
    
    return True
```

**MyPy Error:**
```
task_validator.py:44: error: Statement is unreachable  [unreachable]
```

**Fix:**
```python
import logging

logger = logging.getLogger(__name__)

def validate_task_status(status: str) -> bool:
    """Validate task status value.
    
    Args:
        status: Status string to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_statuses = {"pending", "in_progress", "completed"}
    
    if status not in valid_statuses:
        logger.warning(f"Invalid task status: {status}")
        return False
    
    return True
```

**Impact:** MEDIUM - Dead code indicates logic error  
**Effort:** 15 minutes

---

## 6. Summary Statistics

### By Category

| Category | Count | Auto-fix | Manual | Effort |
|----------|-------|----------|--------|--------|
| Security (HIGH/MED) | 3 | 0 | 3 | 6h |
| Security (LOW) | 22 | 0 | 22 | 6h |
| Code Style | 850+ | 850 | 14 | 3h |
| Type Annotations | 178 | 0 | 178 | 50h |
| Architecture | 5 | 0 | 5 | 2h |
| Bugs | 1 | 0 | 1 | 0.25h |
| **TOTAL** | **1059** | **850** | **223** | **67.25h** |

### By Priority

| Priority | Count | Effort | Timeline |
|----------|-------|--------|----------|
| CRITICAL | 3 | 6h | Week 1 |
| HIGH | 40 | 12h | Week 1-2 |
| MEDIUM | 836 | 25h | Week 2-6 |
| LOW | 180 | 24h | Week 6-12 |

---

## 7. Quick Reference: Fix Patterns

### Security

```python
# Pattern: Replace hardcoded temp paths
- Path("/tmp/mydir")
+ Path(tempfile.mkdtemp(prefix="mydir_"))

# Pattern: Replace silent exceptions
- except Exception: pass
+ except Exception as e: logger.warning(f"...: {e}"); return fallback

# Pattern: Validate subprocess input
+ if not input.isalnum(): raise ValueError(...)
subprocess.run([cmd, validated_input])
```

### Style

```python
# Pattern: Modern type hints
- from typing import List, Dict, Optional
- def func() -> Optional[Dict[str, List[int]]]:
+ def func() -> dict[str, list[int]] | None:

# Pattern: Exception chaining
- except ValueError: raise CustomError("msg")
+ except ValueError as e: raise CustomError("msg") from e
```

### Type Annotations

```python
# Pattern: Add return types
- def func(x: int):
+ def func(x: int) -> None:

# Pattern: Add generic parameters
- def func(items: list) -> dict:
+ def func(items: list[str]) -> dict[str, int]:

# Pattern: Import Any for unknown structures
+ from typing import Any
+ data: dict[str, Any] = load_json()
```

---

**End of Issue Catalog**

Use this document as a reference when fixing issues in your IDE or during code reviews.
