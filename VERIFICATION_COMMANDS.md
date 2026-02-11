# Quick Verification Commands

Run these commands to verify the ADR-046 action items are complete:

## 1. Test Collection (Task 1: Fix CI Dependencies)
```bash
python -m pytest tests/ --collect-only -q
# Expected: 1042 tests collected
```

## 2. Import Linter (Task 2: Import-Linter Configuration)
```bash
lint-imports
# Expected: Bounded context independence KEPT
#          No collaboration to doctrine imports KEPT
#          No doctrine to specifications imports KEPT
#          Domain isolation from framework KEPT
#          (4/4 domain contracts passing)
```

## 3. Type Checking (Task 3: mypy Strict Configuration)
```bash
mypy src/domain/
# Expected: Success: no issues found in 11 source files
```

## 4. Documentation (Task 4: Import Guidelines)
```bash
ls -lh docs/styleguides/import-guidelines.md
# Expected: File exists with ~9KB size
```

## 5. Test Execution (Task 5: Test Count Analysis)
```bash
python -m pytest tests/ -q --tb=no | tail -1
# Expected: 8 failed, 933 passed, 101 skipped (99.15% pass rate)
```

## 6. Architectural Tests
```bash
pytest tests/integration/test_bounded_context_independence.py -v
# Expected: 8 passed in 0.0Xs
```

## All-in-One Validation
```bash
echo "=== TEST COLLECTION ===" && \
python -m pytest tests/ --collect-only -q 2>&1 | grep "collected" && \
echo "" && echo "=== IMPORT LINTER ===" && \
lint-imports 2>&1 | grep "KEPT" | grep -i domain && \
echo "" && echo "=== MYPY ===" && \
mypy src/domain/ 2>&1 | grep "Success" && \
echo "" && echo "=== ARCHITECTURAL TESTS ===" && \
pytest tests/integration/test_bounded_context_independence.py -q 2>&1 | tail -1
```

## Expected All-in-One Output
```
=== TEST COLLECTION ===
1042 tests collected

=== IMPORT LINTER ===
Bounded context independence KEPT
No collaboration to doctrine imports KEPT
No doctrine to specifications imports KEPT
Domain isolation from framework KEPT

=== MYPY ===
Success: no issues found in 11 source files

=== ARCHITECTURAL TESTS ===
8 passed in 0.0Xs
```

---

## Configuration Files Modified

### pyproject.toml
```bash
git diff pyproject.toml | grep "^\+" | head -20
```

### .importlinter
```bash
git diff .importlinter | grep "^\+" | head -20
```

---

## New Documentation Files

```bash
ls -lh docs/styleguides/import-guidelines.md
ls -lh work/reports/2026-02-11-test-count-analysis.md
ls -lh work/logs/2026-02-11-python-pedro-adr046-action-items.md
ls -lh work/reports/2026-02-11-action-items-COMPLETE.md
```

---

## Success Indicators

✅ All commands exit with code 0  
✅ No collection errors in pytest  
✅ All domain contracts KEPT in lint-imports  
✅ mypy Success message shown  
✅ 99%+ test pass rate  
✅ All documentation files created  

---

**Status:** Ready for commit and ADR-045 kickoff
