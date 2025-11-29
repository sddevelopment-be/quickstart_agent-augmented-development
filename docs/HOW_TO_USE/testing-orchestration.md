# Testing the Agent Orchestration System

_Version: 1.0.0_  
_Last updated: 2025-11-23_  
**Audience:** QA engineers and developers validating orchestration workflows.

## Overview

This document explains how to test the asynchronous multi-agent orchestration system using the E2E test harness.

The test suite validates:

- Task lifecycle (creation → assignment → processing → completion → archival)
- Sequential, parallel, and convergent workflow patterns
- Error handling and recovery scenarios
- Dashboard updates and logging
- Performance characteristics

## Quick Start

### Prerequisites

```bash
# Install pytest framework
pip install pytest pytest-timeout
```

### Running Tests

```bash
# Run all tests
cd work/scripts
python3 test_orchestration_e2e.py

# Or use pytest directly
pytest test_orchestration_e2e.py -v

# Run specific test
pytest test_orchestration_e2e.py::test_simple_task_flow -v

# Run with coverage report (if pytest-cov installed)
pytest test_orchestration_e2e.py --cov=agent_orchestrator --cov-report=html
```

## Test Scenarios

The test harness includes 8 comprehensive scenarios:

### 1. Simple Single-Agent Task

**Purpose:** Validate basic inbox → assigned → done flow

**Test:** `test_simple_task_flow`

**Validates:**
- Task assignment from inbox to agent directory
- Status transitions (new → assigned → in_progress → done)
- Timestamp population (assigned_at, started_at, completed_at)
- Result object creation

**Fixture:** `work/scripts/fixtures/test_task_simple.yaml`

### 2. Sequential Workflow (Agent Handoff)

**Purpose:** Test Agent A → Agent B via next_agent handoff

**Test:** `test_sequential_workflow`

**Validates:**
- Follow-up task creation based on `next_agent` field
- Context preservation from previous task
- Handoff logging to `HANDOFFS.md`
- Multi-stage workflow coordination

**Fixture:** `work/scripts/fixtures/test_task_sequential.yaml`

### 3. Parallel Workflow

**Purpose:** Test multiple agents working simultaneously

**Test:** `test_parallel_workflow`

**Validates:**
- Concurrent task assignment to different agents
- Agent status dashboard updates
- Independent task processing
- No interference between parallel workflows

**Fixture:** `work/scripts/fixtures/test_task_parallel.yaml`

### 4. Convergent Workflow (Conflict Detection)

**Purpose:** Test detection of multiple agents targeting same artifact

**Test:** `test_conflict_detection`

**Validates:**
- Conflict detection when multiple in_progress tasks target same file
- Warning logged to `WORKFLOW_LOG.md`
- System continues operating despite conflicts

**Fixture:** `work/scripts/fixtures/test_task_convergent.yaml`

### 5. Timeout Detection

**Purpose:** Test detection of tasks stuck in in_progress

**Test:** `test_timeout_detection`

**Validates:**
- Tasks in_progress for >2 hours are flagged
- Timeout warnings logged to `WORKFLOW_LOG.md`
- Stalled task identification

**Configuration:** `TIMEOUT_HOURS = 2` in `agent_orchestrator.py`

### 6. Archive Execution

**Purpose:** Test archival of old completed tasks

**Test:** `test_archive_old_tasks`

**Validates:**
- Tasks older than 30 days moved from `done/` to `archive/`
- Year-month directory structure created (YYYY-MM)
- Task files moved correctly
- Original files removed from `done/`

**Configuration:** `ARCHIVE_RETENTION_DAYS = 30` in `agent_orchestrator.py`

### 7. Error Handling - Invalid Schema

**Purpose:** Test handling of invalid task files

**Test:** `test_error_handling_invalid_schema`

**Validates:**
- Tasks with missing required fields are not assigned
- Error logged to `WORKFLOW_LOG.md`
- System does not crash
- Invalid tasks remain in inbox for manual intervention

### 8. Error Handling - Missing Agent

**Purpose:** Test handling of tasks for non-existent agents

**Test:** `test_error_handling_missing_agent`

**Validates:**
- Tasks for unknown agents are not assigned
- Error logged to `WORKFLOW_LOG.md`
- System does not crash
- Tasks remain in inbox for correction

## Integration Tests

### Full Orchestrator Cycle

**Test:** `test_full_orchestrator_cycle`

**Purpose:** Validate complete orchestrator execution including all functions

**Validates:**
- All orchestrator functions execute without errors
- Collaboration artifacts created (AGENT_STATUS.md, WORKFLOW_LOG.md)
- Cycle completes within reasonable time
- End-to-end workflow integrity

### Performance Test

**Test:** `test_orchestrator_performance`

**Purpose:** Ensure orchestrator meets performance requirements

**Validates:**
- Cycle completes in <60 seconds (acceptance criteria)
- Handles multiple tasks efficiently
- No performance degradation under load

**Timeout:** 60 seconds (pytest-timeout)

### Function Coverage Test

**Test:** `test_orchestrator_function_coverage`

**Purpose:** Exercise all major orchestrator functions

**Validates:**
- `log_event()` - Event logging
- `read_task()` / `write_task()` - Task file I/O
- `assign_tasks()` - Task assignment
- `process_completed_tasks()` - Follow-up creation
- `check_timeouts()` - Timeout detection
- `detect_conflicts()` - Conflict detection
- `update_agent_status()` - Dashboard updates
- `archive_old_tasks()` - Archival
- `log_handoff()` - Handoff logging

## Test Environment

### Isolated Testing

Tests use `pytest` fixtures to create isolated temporary environments:

```python
@pytest.fixture
def temp_work_env(tmp_path: Path) -> Path:
    """Create isolated test environment with work directory structure."""
```

Each test gets:
- Temporary `work/` directory
- Full directory structure (inbox, assigned, done, archive, collaboration)
- Test agent directories (test-agent, test-agent-2, test-agent-3)
- Monkey-patched orchestrator paths

### Cleanup

All test artifacts are automatically cleaned up after test execution. No manual cleanup required.

## CI Integration

### GitHub Actions

Add to `.github/workflows/test.yml`:

```yaml
name: Test Orchestration System

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install pytest pytest-timeout pyyaml
      
      - name: Run orchestration tests
        run: |
          cd work/scripts
          pytest test_orchestration_e2e.py -v --tb=short
      
      - name: Check test coverage
        run: |
          pip install pytest-cov
          cd work/scripts
          pytest test_orchestration_e2e.py --cov=agent_orchestrator --cov-report=term
```

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
cd work/scripts
pytest test_orchestration_e2e.py --tb=short -q
if [ $? -ne 0 ]; then
    echo "Orchestration tests failed. Commit aborted."
    exit 1
fi
```

## Troubleshooting

### Test Failures

**Issue:** `ModuleNotFoundError: No module named 'pytest'`

**Solution:** Install pytest: `pip install pytest pytest-timeout`

---

**Issue:** `ModuleNotFoundError: No module named 'yaml'`

**Solution:** Install PyYAML: `pip install pyyaml`

---

**Issue:** Tests timeout after 60 seconds

**Solution:** Check for infinite loops or deadlocks. Increase timeout: `@pytest.mark.timeout(120)`

---

**Issue:** Fixture path errors

**Solution:** Run tests from `work/scripts/` directory or use absolute paths

### Debugging

Enable verbose output:

```bash
pytest test_orchestration_e2e.py -v -s
```

Run specific test with debugging:

```bash
pytest test_orchestration_e2e.py::test_simple_task_flow -v -s --pdb
```

Print orchestrator internal state:

```python
# Add to test
import agent_orchestrator
print(f"WORK_DIR: {agent_orchestrator.WORK_DIR}")
print(f"INBOX_DIR: {agent_orchestrator.INBOX_DIR}")
```

## Test Fixtures

Test fixtures are located in `work/scripts/fixtures/`:

- `test_task_simple.yaml` - Basic single-agent task
- `test_task_sequential.yaml` - Multi-stage workflow with handoff
- `test_task_parallel.yaml` - Concurrent execution scenario
- `test_task_convergent.yaml` - Conflict detection scenario

Fixtures follow the task schema defined in `docs/templates/agent-tasks/task-descriptor.yaml`.

## Performance Benchmarks

Expected performance on standard hardware:

- Single task assignment: <0.1 seconds
- Orchestrator cycle (10 tasks): <5 seconds
- Full test suite execution: <60 seconds
- Archive operation (100 tasks): <2 seconds

## Coverage Goals

Target coverage metrics:

- **Function coverage:** 100% (all orchestrator functions)
- **Branch coverage:** >90% (critical paths)
- **Integration coverage:** 100% (all workflow patterns)

## Related Documentation

- [Orchestration Architecture](../architecture/design/async_multiagent_orchestration.md)
- [Technical Design](../architecture/design/async_orchestration_technical_design.md)
- [Task Schema](../templates/agent-tasks/task-descriptor.yaml)
- [ADR-008: File-Based Async Coordination](../architecture/adrs/ADR-008-file-based-async-coordination.md)
- [ADR-003: Task Lifecycle Management](../architecture/adrs/ADR-003-task-lifecycle-state-management.md)

## Contributing

When adding new orchestrator features:

1. Add corresponding test scenario
2. Update this documentation
3. Ensure all tests pass: `pytest test_orchestration_e2e.py -v`
4. Maintain <60 second test suite execution time
5. Keep test coverage at 100% for critical functions

## Support

For issues or questions:

1. Check [Troubleshooting](#troubleshooting) section
2. Review test output: `pytest test_orchestration_e2e.py -v -s`
3. Consult architecture documentation
4. Open issue with test failure details
