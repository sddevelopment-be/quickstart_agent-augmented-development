# Mutation Testing Quick Reference

**One-page guide for running mutation tests**

---

## Setup (One Time)

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Verify mutmut is installed
mutmut --version
```

---

## Quick Commands

```bash
# Run all mutations (uses pyproject.toml config)
mutmut run

# View results summary
mutmut results

# Show specific mutation
mutmut show <id>

# Apply mutation to disk (for investigation)
mutmut apply <id>

# Restore original code
git checkout ops/scripts/orchestration/

# Generate HTML report
mutmut html
open html/index.html
```

---

## Understanding Output

### Legend

- 🎉 **Killed:** Test caught the bug (GOOD!)
- 🙁 **Survived:** Test missed the bug (BAD - needs fix)
- ⏰ **Timeout:** Test took too long (adjust timeout)
- 🤔 **Suspicious:** Test behavior unusual
- 🔇 **Skipped:** Mutation skipped

### Goal

**Aim for 95%+ killed mutations**

### Example Output

```
Progress: 45/45
Killed: 42 (93%)
Survived: 3 (7%)
Timeout: 0 (0%)
```

---

## Investigating Survivors

When mutations survive, it means your tests didn't catch a bug:

```bash
# 1. See what the mutation is
mutmut show 5

# 2. Apply it temporarily
mutmut apply 5

# 3. Look at the change
git diff ops/scripts/orchestration/task_utils.py

# 4. Run the tests (they should pass but shouldn't)
python -m pytest validation/test_task_utils.py -v

# 5. Write a test to catch this bug

# 6. Restore original code
git checkout ops/scripts/orchestration/

# 7. Verify your new test catches it
mutmut run
mutmut results
```

---

## Common Mutation Examples

```python
# Operator changes
==  →  !=      # Equality flipped
>   →  >=      # Comparison weakened
and →  or      # Logic inverted

# Constant changes
"new"  →  "XXnewXX"  # String modified
True   →  False      # Boolean flipped
0      →  1          # Number changed

# Return value changes
return value  →  return None
return True   →  return False
```

---

## Configuration

Edit `pyproject.toml`:

```toml
[tool.mutmut]
paths_to_mutate = "ops/scripts/orchestration/"
runner = "python -m pytest validation/"
tests_dir = "validation/"
timeout = 60
```

---

## Tips

✅ **Do:**
- Run before major releases
- Investigate all survivors
- Focus on business logic
- Use with code coverage tools

❌ **Don't:**
- Run on every commit (it's slow)
- Ignore survivors
- Expect 100% (some are unkillable)
- Mutate test code itself

---

## Full Documentation

See `docs/HOW_TO_USE/mutation_testing.md` for complete guide.

---

**Quick Start:** `mutmut run && mutmut results`
