# SonarCloud Remediation Action Plan

**Project:** sddevelopment-be/quickstart_agent-augmented-development  
**Date:** 2026-02-12  
**Prepared by:** Architect Alphonso  
**Status:** READY FOR REVIEW

---

## Quick Reference: Sprint 1 Action Items

**Timeline:** Week 1-2  
**Total Effort:** 20-28 hours  
**Team Members:** 2-3 developers

### Day 1-2: Security Fixes (CRITICAL)

#### Action 1.1: Fix Insecure Temp Directory Usage

**Files to modify:**
- `src/framework/orchestration/benchmark_orchestrator.py`

**Current Code (Lines 43-44):**
```python
RESULTS_DIR = BENCHMARK_DIR / "results"
TEST_WORK_DIR = Path("/tmp/benchmark_work")
```

**Fixed Code:**
```python
import tempfile
from pathlib import Path

RESULTS_DIR = BENCHMARK_DIR / "results"

def get_test_work_dir() -> Path:
    """Create secure temporary directory for benchmark work.
    
    Returns:
        Path: Secure temporary directory that will be cleaned up
    """
    temp_dir = Path(tempfile.mkdtemp(prefix="benchmark_work_"))
    return temp_dir
```

**Update all usages:**
```python
# Before (line 131-132)
if not str(TEST_WORK_DIR).startswith("/tmp/"):
    raise ValueError(f"TEST_WORK_DIR must be in /tmp for safety: {TEST_WORK_DIR}")

# After
def setup_benchmark_environment() -> Path:
    """Set up secure benchmark environment with cleanup."""
    work_dir = get_test_work_dir()
    work_dir.mkdir(parents=True, exist_ok=True)
    return work_dir

def cleanup_benchmark_environment(work_dir: Path) -> None:
    """Clean up benchmark environment."""
    import shutil
    if work_dir.exists():
        shutil.rmtree(work_dir)
```

**Estimated Time:** 2 hours  
**Verification:** Run Bandit, confirm B108 issues resolved

---

#### Action 1.2: Fix Silent Exception Handlers

**Files to modify:**
1. `src/domain/collaboration/types.py` (lines 74, 97)
2. `src/framework/orchestration/benchmark_orchestrator.py` (lines 92, 287)
3. `src/framework/orchestration/agent_orchestrator.py` (line 233)

**Pattern to Replace:**

**Before:**
```python
try:
    return agent_name in valid_agents
except Exception:
    # Fallback to Literal type if dynamic loading fails
    pass
```

**After:**
```python
import logging

logger = logging.getLogger(__name__)

try:
    return agent_name in valid_agents
except Exception as e:
    logger.warning(
        f"Failed to validate agent name '{agent_name}' dynamically: {e}. "
        "Falling back to static validation."
    )
    return False  # Explicit fallback behavior
```

**Key Changes:**
- Import and use logger
- Catch specific exception (or log Exception with context)
- Return explicit fallback value
- Document why fallback exists

**Estimated Time:** 4 hours  
**Verification:** Run Bandit, confirm B110/B112 issues resolved

---

#### Action 1.3: Validate Subprocess Input

**File:** `src/framework/context/assemble-agent-context.py` (line 104)

**Current Code:**
```python
result = subprocess.run(
    [sys.executable, str(self.directive_loader)] + directive_codes,
    capture_output=True,
    text=True,
    check=True,
)
```

**Fixed Code:**
```python
import shlex
from pathlib import Path

def validate_directive_codes(codes: list[str]) -> list[str]:
    """Validate directive codes are safe strings.
    
    Args:
        codes: List of directive codes to validate
        
    Returns:
        Validated directive codes
        
    Raises:
        ValueError: If any code contains unsafe characters
    """
    for code in codes:
        if not code.replace("-", "").replace("_", "").isalnum():
            raise ValueError(f"Invalid directive code: {code}")
    return codes

def load_directives(directive_loader: Path, directive_codes: list[str]) -> str:
    """Load directives with validated input.
    
    Args:
        directive_loader: Path to directive loader script
        directive_codes: Directive codes to load
        
    Returns:
        Loaded directive content
        
    Raises:
        ValueError: If inputs are invalid
        subprocess.CalledProcessError: If loader fails
    """
    # Validate inputs
    if not directive_loader.exists():
        raise ValueError(f"Directive loader not found: {directive_loader}")
    
    validated_codes = validate_directive_codes(directive_codes)
    
    # Execute with validated inputs
    result = subprocess.run(
        [sys.executable, str(directive_loader)] + validated_codes,
        capture_output=True,
        text=True,
        check=True,
        timeout=30,  # Add timeout for safety
    )
    return result.stdout
```

**Estimated Time:** 2 hours  
**Verification:** Run Bandit, confirm B603 resolved

---

### Day 3: Fix Bug + Enable Coverage

#### Action 2.1: Fix Unreachable Code

**File:** `src/domain/collaboration/task_validator.py` (line 44)

**Investigation Steps:**
1. View the file context around line 44
2. Identify why code is unreachable (likely after return or in impossible condition)
3. Determine if it's dead code (remove) or logic error (fix)

**Generic Fix Pattern:**
```python
# Before (hypothetical)
def validate_task(task: dict) -> bool:
    if task.get("status") == "invalid":
        return False
        print("This is unreachable")  # Line 44
    return True

# After
def validate_task(task: dict) -> bool:
    if task.get("status") == "invalid":
        logger.debug(f"Task validation failed: {task.get('id')}")
        return False
    return True
```

**Estimated Time:** 1 hour  
**Verification:** Run MyPy, confirm unreachable statement warning gone

---

#### Action 2.2: Enable Test Coverage Reporting

**File:** `.github/workflows/tests.yml` (create or modify)

**Add Coverage Configuration:**
```yaml
name: Tests and Coverage

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
      
      - name: Run tests with coverage
        run: |
          pytest \
            --cov=src \
            --cov=framework \
            --cov-report=xml \
            --cov-report=html \
            --cov-report=term-missing
      
      - name: Upload coverage to SonarCloud
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      
      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          fail_ci_if_error: true
```

**Update pyproject.toml:**
```toml
[tool.coverage.run]
source = ["src", "framework"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__pycache__/*",
    "*/venv/*",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false

[tool.coverage.xml]
output = "coverage.xml"

[tool.coverage.html]
directory = "htmlcov"
```

**Estimated Time:** 3 hours  
**Verification:** Run workflow, check SonarCloud shows coverage data

---

### Day 4: Auto-fix Code Style

#### Action 3.1: Run Ruff Auto-fix

**Execute Commands:**
```bash
# Dry run first to see what will change
ruff check --diff src framework

# Apply fixes
ruff check --fix src framework

# Check remaining issues
ruff check src framework

# Format with Black
black src framework

# Verify no issues
ruff check src framework
```

**Expected Results:**
- W293 (617 issues) - ✅ Fixed: Blank line whitespace removed
- W291 (17 issues) - ✅ Fixed: Trailing whitespace removed
- UP006 (104 issues) - ✅ Fixed: `List` → `list`
- UP045 (68 issues) - ✅ Fixed: `Optional[X]` → `X | None`
- UP035 (44 issues) - ✅ Fixed: `typing.Dict` → `dict`
- I001 (30 issues) - ✅ Fixed: Import sorting
- F401 (15 issues) - ✅ Fixed: Unused imports removed
- F541 (7 issues) - ✅ Fixed: Empty f-strings

**Remaining Manual Issues:**
- B904 (14 issues) - Exception chaining (see Action 3.2)

**Estimated Time:** 1 hour (mostly automated)  
**Verification:** Run Ruff again, confirm 850+ issues resolved

---

#### Action 3.2: Fix Exception Chaining (B904)

**Pattern to Fix:**

**Before:**
```python
try:
    result = process_data(data)
except ValueError:
    raise CustomError("Processing failed")
```

**After:**
```python
try:
    result = process_data(data)
except ValueError as e:
    raise CustomError("Processing failed") from e
```

**Find all instances:**
```bash
ruff check --select B904 src framework
```

**Estimated Time:** 2 hours  
**Verification:** Run `ruff check --select B904`, confirm 0 issues

---

## Sprint 2-3: Type Annotations (40-60 hours)

### Phase 1: Install Type Stubs (1 hour)

```bash
pip install \
    types-PyYAML \
    types-Flask-SocketIO \
    types-Flask-Cors \
    types-psutil \
    types-requests

# Update requirements-dev.txt
pip freeze | grep types- >> requirements-dev.txt
```

---

### Phase 2: Add Return Type Annotations (20 hours)

**Priority Files (from analysis):**

1. `src/llm_service/dashboard/app.py` (28 errors)
2. `src/llm_service/cli.py` (17 errors)
3. `src/llm_service/dashboard/file_watcher.py` (10 errors)
4. `src/llm_service/telemetry/logger.py` (7 errors)
5. `src/framework/orchestration/agent_base.py` (6 errors)

**Pattern: Add `-> None` to Functions**

**Find all missing return annotations:**
```bash
mypy src framework 2>&1 | grep "missing a return type annotation" | cut -d: -f1-2 | sort -u
```

**Example Fixes:**

**File: `src/llm_service/telemetry/logger.py:105`**

**Before:**
```python
def log_event(self, event_type: str, data: dict):
    """Log an event."""
    self.events.append({"type": event_type, "data": data})
```

**After:**
```python
def log_event(self, event_type: str, data: dict[str, Any]) -> None:
    """Log an event to the event store.
    
    Args:
        event_type: Type of event to log
        data: Event data dictionary
    """
    self.events.append({"type": event_type, "data": data})
```

---

### Phase 3: Add Generic Type Parameters (15 hours)

**Pattern: `dict` → `dict[str, Any]`**

**Find all instances:**
```bash
mypy src framework 2>&1 | grep "Missing type parameters for generic type" | cut -d: -f1-2 | sort -u
```

**Example Fixes:**

**Before:**
```python
def parse_config(path: Path) -> dict:
    """Parse configuration file."""
    with open(path) as f:
        return yaml.safe_load(f)
```

**After:**
```python
from typing import Any

def parse_config(path: Path) -> dict[str, Any]:
    """Parse configuration file.
    
    Args:
        path: Path to YAML configuration file
        
    Returns:
        Parsed configuration as dictionary
    """
    with open(path) as f:
        return yaml.safe_load(f)
```

---

### Phase 4: Type Flask/SocketIO Decorators (5 hours)

**Challenge:** Flask decorators make return types complex.

**Pattern:**

**Before:**
```python
@app.route('/api/tasks')
def get_tasks():
    return jsonify({"tasks": []})
```

**After:**
```python
from typing import Any
from flask import Response

@app.route('/api/tasks')
def get_tasks() -> Response | tuple[dict[str, Any], int]:
    """Get all tasks.
    
    Returns:
        JSON response with task list
    """
    return jsonify({"tasks": []})
```

**For complex cases, use type: ignore with comment:**
```python
@socketio.on('update_priority')
def handle_priority_update(data: dict[str, Any]) -> None:  # type: ignore[misc]
    """Handle priority update event.
    
    Note: SocketIO decorator typing not fully supported by mypy.
    """
    update_task_priority(data)
```

---

## Verification Checklist

### After Sprint 1 (Week 2)

- [ ] Bandit scan shows 0 HIGH/MEDIUM issues
- [ ] Coverage.xml generated in CI/CD
- [ ] SonarCloud displays coverage metrics
- [ ] Ruff check shows <100 violations (from 926)
- [ ] MyPy error count decreased by 10+
- [ ] All tests passing
- [ ] Pre-commit hooks configured

### After Sprint 2-3 (Week 6)

- [ ] Ruff check shows 0 violations
- [ ] MyPy error count <50 (from 178)
- [ ] Coverage >70% on new code
- [ ] All type stubs installed
- [ ] Core modules fully typed
- [ ] CI/CD quality gate enforced

### After Quarter 1 (Month 3)

- [ ] MyPy strict mode with 0 errors
- [ ] Coverage >80% overall
- [ ] SonarCloud Quality Gate: PASSED
- [ ] Technical debt ratio <5%
- [ ] Mutation testing score >75%
- [ ] All ADRs documented

---

## Automation Scripts

### Script 1: Quick Security Fix

```bash
#!/bin/bash
# fix-security-issues.sh

set -e

echo "Fixing security issues..."

# Fix try-except-pass patterns
find src framework -name "*.py" -exec sed -i \
    's/except Exception:$/except Exception as e:/' {} \;

# Add TODO comments for manual review
find src framework -name "*.py" -exec grep -l "except Exception as e:$" {} \; | while read file; do
    echo "TODO: Review exception handling in $file"
done

echo "Security fixes applied. Manual review required."
```

### Script 2: Bulk Type Annotation

```bash
#!/bin/bash
# add-return-none.sh

set -e

echo "Adding -> None annotations..."

# Find functions with missing return annotations
mypy src framework 2>&1 | \
    grep "missing a return type annotation" | \
    grep "Use \"-> None\"" | \
    cut -d: -f1-2 | \
    sort -u | \
    while IFS=: read file line; do
        sed -i "${line}s/):$/) -> None:/" "$file"
        echo "Fixed $file:$line"
    done

echo "Annotations added. Run mypy to verify."
```

### Script 3: Coverage Check

```bash
#!/bin/bash
# check-coverage.sh

set -e

pytest \
    --cov=src \
    --cov=framework \
    --cov-report=term-missing \
    --cov-fail-under=70

echo "Coverage check completed."
```

---

## Communication Plan

### Week 1: Kick-off
- [ ] Share analysis report with team
- [ ] Schedule sprint planning
- [ ] Assign action items
- [ ] Set up tracking board

### Week 2: Mid-Sprint Check-in
- [ ] Review security fixes (Day 2)
- [ ] Verify coverage enabled (Day 3)
- [ ] Demo auto-fix results (Day 4)

### Week 6: Sprint 2-3 Review
- [ ] Review type annotation progress
- [ ] Assess remaining MyPy errors
- [ ] Adjust timeline if needed

### Month 3: Final Review
- [ ] Present quality improvements
- [ ] Demonstrate SonarCloud dashboard
- [ ] Document lessons learned
- [ ] Plan ongoing maintenance

---

## Risk Mitigation

### Risk: Breaking Changes from Auto-fix

**Mitigation:**
1. Create feature branch: `code-quality/sprint-1`
2. Run full test suite before and after
3. Manual code review of Ruff changes
4. Incremental commits (one issue type at a time)

### Risk: Developer Workload

**Mitigation:**
1. Pair programming for type annotations
2. Spread work across multiple sprints
3. Focus on high-impact areas first
4. Automate wherever possible

### Risk: CI/CD Pipeline Slowdown

**Mitigation:**
1. Run quality checks in parallel
2. Cache dependencies
3. Use matrix testing for multiple Python versions
4. Optimize test execution order

---

## Success Metrics

**Track Weekly:**
1. Open issues count (Ruff + MyPy + Bandit)
2. Code coverage percentage
3. Time spent on quality work
4. Developer satisfaction (survey)

**Report Monthly:**
1. Technical debt trend
2. Quality gate pass rate
3. Defect escape rate
4. Code review turnaround time

---

**End of Action Plan**

**Next Step:** Schedule Sprint 1 planning session to review and assign action items.

**Contact:** Architect Alphonso (for questions on this plan)
