# ADR-045 Task 4: Verification Commands

Run these commands to verify the implementation:

## Test Execution

### Unit Tests (20 tests)
```bash
pytest tests/unit/domain/doctrine/test_validators.py -v
```

### Integration Tests (9 tests)
```bash
pytest tests/integration/doctrine/test_doctrine_loading.py -v -s
```

### Performance Tests (5 tests)
```bash
pytest tests/performance/doctrine/test_load_performance.py -v -s
```

### All Validator Tests (34 tests)
```bash
pytest tests/unit/domain/doctrine/test_validators.py \
       tests/integration/doctrine/test_doctrine_loading.py \
       tests/performance/doctrine/test_load_performance.py -v
```

## Coverage Analysis

### Validators Coverage (Should be 100%)
```bash
pytest tests/unit/domain/doctrine/test_validators.py \
       --cov=src.domain.doctrine.validators \
       --cov-report=term-missing
```

### Core Doctrine Coverage (Should be ≥90%)
```bash
pytest tests/unit/domain/doctrine/ \
       --cov=src.domain.doctrine.validators \
       --cov=src.domain.doctrine.models \
       --cov-report=term-missing
```

### Full Doctrine Module Coverage
```bash
pytest tests/unit/domain/doctrine/ \
       --cov=src.domain.doctrine \
       --cov-report=term-missing \
       --cov-report=html
```

## Code Quality

### Type Checking (mypy strict mode)
```bash
mypy src/domain/doctrine/validators.py --strict
```

### Linting (ruff)
```bash
ruff check src/domain/doctrine/validators.py \
           tests/unit/domain/doctrine/test_validators.py
```

### Format Check (black)
```bash
black --check src/domain/doctrine/validators.py \
              tests/unit/domain/doctrine/test_validators.py
```

## Performance Benchmarking

### Load Performance Only
```bash
pytest tests/performance/doctrine/test_load_performance.py::TestLoadPerformance -v -s
```

### Memory Usage Test
```bash
pytest tests/performance/doctrine/test_load_performance.py::TestMemoryUsage -v -s
```

## Real-World Validation

### Load All Agents
```bash
pytest tests/integration/doctrine/test_doctrine_loading.py::TestDoctrineLoading::test_load_all_agents -v -s
```

### Complete Doctrine Validation
```bash
pytest tests/integration/doctrine/test_doctrine_loading.py::TestDoctrineLoading::test_complete_doctrine_validation -v -s
```

### Cross-Reference Validation
```bash
pytest tests/integration/doctrine/test_doctrine_loading.py::TestDoctrineLoading::test_cross_reference_validation -v -s
```

## Quick Verification

### All Tests (Expected: 34 passed)
```bash
pytest tests/unit/domain/doctrine/test_validators.py \
       tests/integration/doctrine/test_doctrine_loading.py \
       tests/performance/doctrine/test_load_performance.py \
       --tb=line -q
```

### Quality Gates
```bash
mypy src/domain/doctrine/validators.py --strict && \
ruff check src/domain/doctrine/validators.py && \
pytest tests/unit/domain/doctrine/test_validators.py -q && \
echo "✅ All quality gates passed"
```

## Expected Results

- **Unit Tests:** 20/20 passing
- **Integration Tests:** 9/9 passing
- **Performance Tests:** 5/5 passing
- **Total Tests:** 34/34 passing (100%)
- **Validators Coverage:** 100%
- **Core Coverage:** 99%
- **mypy:** No errors
- **ruff:** No errors
- **Load Time (20 agents):** <10ms (target: <500ms)
- **Validation Time:** <1ms (target: <200ms)

## Documentation

- **Validation Report:** `work/validation/adr045-validation-report.md`
- **Work Log:** `work/reports/logs/python-pedro/2026-02-12T0606-adr045-task4-validators.md`
- **Source Code:** `src/domain/doctrine/validators.py`
