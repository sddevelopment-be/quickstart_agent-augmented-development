# Mutation Testing Guide

**Tool:** mutmut  
**Version:** 3.4.0+  
**Purpose:** Verify test suite quality by introducing controlled bugs
**Audience:** Developers and QA engineers assessing test suite effectiveness (see `docs/audience/software_engineer.md`).

---

## What is Mutation Testing?

Mutation testing validates the effectiveness of your test suite by deliberately introducing bugs ("mutations") into your code and checking if your tests catch them. Use this when you need evidence that coverage numbers correspond to real defect-catching power.

### How It Works

1. **Mutate:** Change a line of code (e.g., `==` becomes `!=`, `True` becomes `False`)
2. **Test:** Run your test suite against the mutated code
3. **Evaluate:** Did the tests catch the bug?
   - ✅ **Killed:** Test failed (good! The mutation was detected)
   - ❌ **Survived:** Test passed (bad! The mutation wasn't caught)
   - ⚠️ **Timeout:** Test took too long
   - ⚠️ **Suspicious:** Test behaved unexpectedly

### Example Mutations

```python
# Original code
if status == "new":
    process_task()

# Mutation 1: Operator change
if status != "new":  # Flipped operator
    process_task()

# Mutation 2: Constant change
if status == "XXnewXX":  # Modified string
    process_task()

# Mutation 3: Return value
def get_status():
    return "new"  # Original
    # Mutated to:
    return "XXnewXX"
```

**Good tests should FAIL on all these mutations.**

---

## Installation

```bash
# Install mutmut
pip install mutmut

# Or add to requirements-dev.txt
echo "mutmut>=3.4.0" >> requirements-dev.txt
pip install -r requirements-dev.txt
```

---

## Quick Start

### Run Mutation Testing

```bash
# Run mutations on orchestration code
mutmut run --paths-to-mutate=ops/scripts/orchestration/

# Check results
mutmut results

# Show summary
mutmut show
```

### Example Output

```
Legend for output:
🎉 Killed mutants.   The goal is for everything to end up in this bucket.
⏰ Timeout.          Test suite took 10 times as long as the baseline so were killed.
🤔 Suspicious.       Tests took a long time, but not long enough to be considered a timeout.
🙁 Survived.         We need to write tests for these mutants.
🔇 Skipped.          Mutants that were skipped for various reasons.

Progress: 45/45
Killed: 42 (93%)
Survived: 3 (7%)
```

---

## Configuration

Configuration is in `pyproject.toml`:

```toml
[tool.mutmut]
# Code to mutate
paths_to_mutate = "ops/scripts/orchestration/"

# Test command
runner = "python -m pytest validation/"

# Tests location
tests_dir = "validation/"

# Timeout (seconds)
timeout = 60
```

---

## Interpreting Results

### Killed Mutations (Good ✅)

```bash
$ mutmut results

To apply a mutant on disk:
    mutmut apply <id>

To show a mutant:
    mutmut show <id>

Killed mutants (42 total):
---- task_utils.py (10) ----
1, 2, 3, 4, 5, 6, 7, 8, 9, 10
```

**Meaning:** Your tests successfully detected these bugs.

### Survived Mutations (Bad ❌)

```bash
Survived mutants (3 total):
---- task_utils.py (3) ----
11, 12, 13
```

**Action Required:** Write tests to cover these cases.

**Inspect survived mutation:**
```bash
# See what the mutation was
mutmut show 11

# Apply it temporarily to understand
mutmut apply 11

# View the diff
git diff ops/scripts/orchestration/task_utils.py

# Write a test, then restore
git checkout ops/scripts/orchestration/task_utils.py
```

---

## Common Workflows

### 1. Full Mutation Test

```bash
# Run all mutations
mutmut run

# View summary
mutmut results

# Generate HTML report
mutmut html
```

### 2. Test Specific File

```bash
# Mutate only task_utils.py
mutmut run --paths-to-mutate=ops/scripts/orchestration/task_utils.py

# Check results
mutmut results
```

### 3. Investigate Survivors

```bash
# List survived mutations
mutmut results

# Show details of mutation 5
mutmut show 5

# Apply mutation 5 to disk (temporarily)
mutmut apply 5

# Run tests to see why they pass
python -m pytest validation/test_task_utils.py -v

# Restore original code
git checkout ops/scripts/orchestration/
```

### 4. Incremental Testing

```bash
# Run just new/surviving mutations
mutmut run --rerun-all

# Or continue from last run
mutmut run --resume
```

---

## Writing Tests to Kill Mutations

### Example: Survived Mutation

**Mutation:**
```python
# Original
def update_status(task, status):
    task["status"] = status
    return task

# Mutated (string changed)
def update_status(task, status):
    task["status"] = "XXstatusXX"  # Hardcoded
    return task
```

**Problem:** No test verifies the actual status value is set.

**Solution:** Add assertion test:
```python
def test_update_status_sets_correct_value():
    # Arrange
    task = {"id": "test", "status": "old"}
    
    # Assumption Check
    assert task["status"] == "old"
    
    # Act
    result = update_status(task, "new")
    
    # Assert
    assert result["status"] == "new"  # This kills the mutation!
```

---

## Mutation Score Goals

### Target Scores

- **Excellent:** 95-100% (most mutations killed)
- **Good:** 85-95% (strong test coverage)
- **Acceptable:** 75-85% (adequate but room for improvement)
- **Poor:** <75% (significant gaps in testing)

### Our Current Score

Run `mutmut results` to see current score:

```bash
# Check score
mutmut results | grep "Killed:"

# Goal: Aim for 95%+ killed
```

---

## Common Mutation Types

### 1. Operator Mutations

```python
# Comparison operators
==  →  !=
>   →  >=
<   →  <=
and →  or

# Arithmetic operators
+  →  -
*  →  /
%  →  //
```

### 2. Constant Mutations

```python
# Numbers
0  →  1
1  →  0
42 →  43

# Strings
"text"  →  "XXtextXX"
""      →  "XX"

# Booleans
True  →  False
False →  True
```

### 3. Return Value Mutations

```python
# Function returns
return value    →  return None
return True     →  return False
return []       →  return [None]
```

### 4. Statement Mutations

```python
# Remove statements
some_function()  →  pass

# Modify conditions
if condition:    →  if not condition:
```

---

## Best Practices

### Do's ✅

1. **Run regularly:** Include in CI/CD pipeline
2. **Investigate survivors:** Each survived mutation is a test gap
3. **Focus on critical code:** Mutate business logic first
4. **Set realistic goals:** Aim for 95%+, accept some survivors
5. **Use with coverage:** Mutation testing complements code coverage

### Don'ts ❌

1. **Don't mutate test code:** Only mutate production code
2. **Don't ignore survivors:** They reveal real gaps
3. **Don't aim for 100%:** Some mutations are legitimately unkillable
4. **Don't run on every commit:** It's slow, use for pre-release validation
5. **Don't mutate trivial code:** Focus on logic, not getters/setters

---

## Integration with CI/CD

### GitHub Actions Workflow

```yaml
name: Mutation Testing

on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday at 2 AM
  workflow_dispatch:      # Manual trigger

jobs:
  mutmut:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install mutmut
      
      - name: Run mutation tests
        run: mutmut run
      
      - name: Check results
        run: |
          mutmut results
          mutmut html
      
      - name: Upload HTML report
        uses: actions/upload-artifact@v4
        with:
          name: mutation-report
          path: html/
```

---

## Troubleshooting

### Timeouts

**Problem:** Many mutations timeout

**Solutions:**
```bash
# Increase timeout
mutmut run --timeout-multiplier=2

# Or in pyproject.toml
[tool.mutmut]
timeout = 120  # Increase from 60
```

### Too Many Mutations

**Problem:** Mutation testing takes too long

**Solutions:**
```bash
# Test specific module
mutmut run --paths-to-mutate=ops/scripts/orchestration/task_utils.py

# Use sampling (test 50% of mutations)
mutmut run --paths-to-mutate=ops/scripts/orchestration/ --use-coverage --rerun-all
```

### False Survivors

**Problem:** Mutation should be killed but survives

**Investigation:**
```bash
# Apply the mutation
mutmut apply <id>

# Run specific test
python -m pytest validation/test_file.py::test_function -v

# Check if test logic is correct
# Restore after investigation
git checkout ops/scripts/orchestration/
```

---

## Metrics and Reporting

### Generate HTML Report

```bash
# Run mutations
mutmut run

# Generate HTML visualization
mutmut html

# Open in browser
open html/index.html
```

### Command Line Summary

```bash
# Quick summary
mutmut results

# Detailed breakdown
mutmut show

# Show specific mutation
mutmut show 5
```

### Export Results

```bash
# Export to JSON
mutmut junitxml > mutation-results.xml

# Or use results file
cat .mutmut-cache
```

---

## Example: Complete Workflow

```bash
# 1. Install mutmut
pip install mutmut

# 2. Run mutations on orchestration code
mutmut run --paths-to-mutate=ops/scripts/orchestration/

# 3. Check results
mutmut results
# Output: Killed: 42/45 (93%)

# 4. Investigate survivors
mutmut show 43
mutmut show 44
mutmut show 45

# 5. Apply first survivor to see it
mutmut apply 43
git diff

# 6. Write test to kill it
# ... edit validation/test_task_utils.py ...

# 7. Restore and test
git checkout ops/scripts/orchestration/
python -m pytest validation/test_task_utils.py -v

# 8. Re-run mutation test
mutmut run --paths-to-mutate=ops/scripts/orchestration/task_utils.py

# 9. Verify mutation is now killed
mutmut results
# Output: Killed: 43/45 (96%)

# 10. Repeat for remaining survivors
```

---

## References

- **mutmut Documentation:** https://mutmut.readthedocs.io/
- **Mutation Testing Theory:** https://en.wikipedia.org/wiki/Mutation_testing
- **Test Coverage vs Mutation:** `validation/TEST_COVERAGE.md`

---

## Version History

| Version | Date       | Changes                     |
|---------|------------|-----------------------------|
| 1.0.0   | 2025-11-29 | Initial mutation test setup |

---

**Maintained by:** Build Automation Team  
**Review Cycle:** After significant code changes or test additions
