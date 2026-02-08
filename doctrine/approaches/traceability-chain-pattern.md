# Approach: Traceability Chain Pattern

**Status:** Active  
**Created:** 2026-02-08  
**Source:** Extracted from [SDD Learnings Reflection](../../work/reports/reflections/2026-02-06-specification-driven-development-learnings.md)  
**Related Directives:** 018 (Traceable Decisions), 034 (Specification-Driven Development), 016 (ATDD)

---

## Purpose

Maintain bidirectional links between artifacts throughout the development lifecycle, ensuring every implementation can be traced back to requirements and every requirement forward to implementation.

**Key Insight:** Traceability is not just documentation—it's a quality assurance mechanism that enables impact analysis, onboarding, and compliance auditing.

---

## The Traceability Chain

```
Strategic Goal (WHY this initiative exists)
    ↓ (WHAT to build)
Specification (functional requirements, scenarios)
    ↓ (HOW to verify)
Acceptance Tests (executable criteria)
    ↓ (WHY technical choices)
ADRs (architectural decisions, trade-offs)
    ↓ (HOW implemented)
Implementation (code, tests, documentation)
    ↓ (WHAT happened)
Work Logs (execution trace, decisions made)
```

**Bidirectional Property:**
- Forward links: Requirements → Tests → Code
- Backward links: Code → Tests → Requirements
- Change impact: Modify requirement → identify affected tests/code
- Rationale discovery: Read code → understand requirements

---

## Chain Links Explained

### 1. Strategic Goal → Specification

**Link Type:** "Derives from"

**Example:**
```markdown
## Strategic Goal
Milestone 4: Real-Time Agent Monitoring
- Objective: Enable operators to observe multi-agent workflows

## Specification
specifications/features/dashboard-integration.md
- Derived from: Milestone 4 (Real-Time Agent Monitoring)
- User Story: As a Software Engineer, I want to see task progress...
```

**Bidirectional:**
- Spec frontmatter references milestone
- Milestone document lists all derived specs

### 2. Specification → Acceptance Tests

**Link Type:** "Verifies"

**Example:**
```markdown
## Specification (specifications/features/dashboard-integration.md)
FR-M1: System MUST accept WebSocket connections from localhost
- Success Criteria: Connection succeeds without 400 error
- Test Reference: tests/acceptance/dashboard/test_websocket_connection.py

## Acceptance Test (tests/acceptance/dashboard/test_websocket_connection.py)
"""
Verifies: FR-M1 from specifications/features/dashboard-integration.md
"""
def test_websocket_connection_from_localhost():
    # Given: Dashboard server running
    # When: Client connects from localhost
    # Then: Connection succeeds
```

**Bidirectional:**
- Spec lists test file paths
- Test file docstring references spec requirement ID

### 3. Acceptance Tests → ADRs

**Link Type:** "Implements decision from"

**Example:**
```markdown
## Acceptance Test
# Implementation note: Uses Flask-SocketIO per ADR-028

## ADR-028: WebSocket Technology Choice
**Decision:** Use Flask-SocketIO for real-time communication
**Rationale:** Minimal setup, built-in CORS support
**Consequences:** Tests must use socketio client library
**Affected Tests:**
- tests/acceptance/dashboard/test_websocket_connection.py
- tests/acceptance/dashboard/test_real_time_updates.py
```

**Bidirectional:**
- Test comments reference ADR number
- ADR lists affected tests

### 4. ADRs → Implementation

**Link Type:** "Guides"

**Example:**
```python
# src/llm_service/dashboard/app.py
"""
Dashboard WebSocket server implementation.

Architecture: Flask-SocketIO for real-time communication (ADR-028)
Specification: specifications/features/dashboard-integration.md
Tests: tests/acceptance/dashboard/
"""

from flask_socketio import SocketIO  # ADR-028: Chosen technology

# Configuration per ADR-028: Enable CORS for local development
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')
```

**Bidirectional:**
- Code comments reference ADRs
- ADRs reference affected code modules

### 5. Implementation → Work Logs

**Link Type:** "Documents"

**Example:**
```markdown
## Work Log (work/reports/logs/2026-02-06-dashboard-cors-fix.md)

**Task:** Fix dashboard WebSocket CORS errors
**Specification:** specifications/features/dashboard-integration.md (FR-M1)
**ADR Referenced:** ADR-028 (WebSocket Technology Choice)

**Changes Made:**
- Modified: src/llm_service/dashboard/app.py
  - Added: cors_allowed_origins='*' per ADR-028
  - Rationale: Enables localhost connections (FR-M1 requirement)

**Tests Passing:**
- tests/acceptance/dashboard/test_websocket_connection.py ✅
```

**Bidirectional:**
- Work log references spec, ADR, code, tests
- Git commit messages link to work log

---

## Implementation Guidelines

### Required Links

**Every Specification MUST have:**
- [ ] Reference to strategic goal or milestone
- [ ] List of acceptance test files
- [ ] Related ADRs (if architectural decisions made)

**Every Acceptance Test MUST have:**
- [ ] Docstring referencing spec requirement ID
- [ ] Comments explaining ADR-driven choices

**Every ADR MUST have:**
- [ ] List of affected code modules
- [ ] List of affected tests
- [ ] Link to related specifications

**Every Implementation MUST have:**
- [ ] File docstring referencing spec
- [ ] Comments on ADR-driven design choices
- [ ] Test file references

**Every Work Log MUST have:**
- [ ] Task context (spec, ADR, issue)
- [ ] Changes made (files, rationale)
- [ ] Test status (passing/failing)

### Link Syntax

**Markdown Documents:**
```markdown
**Specification:** [Dashboard Integration](../specifications/features/dashboard-integration.md) (FR-M1)
**ADR:** [ADR-028: WebSocket Technology](../docs/architecture/adrs/028-websocket-technology.md)
**Tests:** `tests/acceptance/dashboard/test_websocket_connection.py`
```

**Code Comments:**
```python
"""
Specification: specifications/features/dashboard-integration.md
Architecture: ADR-028 (WebSocket Technology Choice)
Tests: tests/acceptance/dashboard/
"""
```

**YAML Tasks:**
```yaml
context:
  specification: specifications/features/dashboard-integration.md
  requirement: FR-M1
  adr: ADR-028
  tests: tests/acceptance/dashboard/
```

---

## Benefits

### 1. Impact Analysis

**Scenario:** Spec requirement changes

**Traceability enables:**
```
1. Identify affected tests (spec → tests link)
2. Identify affected code (tests → code link)
3. Identify related decisions (spec → ADR link)
4. Estimate change scope (count artifacts in chain)
```

### 2. Onboarding

**Scenario:** New contributor asks "Why does this code exist?"

**Traceability enables:**
```
1. Read code docstring → find spec reference
2. Read spec → understand user need
3. Read ADR → understand technical choice
4. Read tests → see expected behavior
```

### 3. Compliance Auditing

**Scenario:** "Prove this requirement was implemented"

**Traceability enables:**
```
1. Find spec requirement → FR-M1
2. Find test verifying FR-M1 → test_websocket_connection.py
3. Show test passing → CI logs
4. Find implementation → src/llm_service/dashboard/app.py
5. Show work log → 2026-02-06-dashboard-cors-fix.md
```

### 4. Requirement Coverage

**Scenario:** "Are all spec requirements tested?"

**Traceability enables:**
```bash
# Extract spec requirements
grep "^FR-" specifications/features/*.md > requirements.txt

# Extract test coverage
grep "Verifies: FR-" tests/acceptance/**/*.py > coverage.txt

# Diff to find gaps
diff requirements.txt coverage.txt
```

---

## Anti-Patterns

### ❌ Orphaned Artifacts

**Symptom:** Code exists with no spec, test, or ADR reference

**Problem:** Cannot determine purpose or validity

**Fix:**
```python
# BEFORE (orphaned)
def process_task(task):
    return task.execute()

# AFTER (traceable)
def process_task(task):
    """
    Execute task per Directive 019 (File-Based Collaboration).
    
    Specification: specifications/workflows/multi-agent-orchestration.md
    Tests: tests/integration/test_task_execution.py
    """
    return task.execute()
```

### ❌ Stale Links

**Symptom:** Spec references non-existent test file

**Problem:** Cannot verify requirement implementation

**Fix:** Validate links in CI
```bash
# Link validation script
for spec in specifications/**/*.md; do
    # Extract test references
    grep -o "tests/[^)]*" "$spec" | while read test; do
        [ -f "$test" ] || echo "ERROR: $spec references missing $test"
    done
done
```

### ❌ Forward-Only Links

**Symptom:** Spec references tests, but tests don't reference spec

**Problem:** Cannot navigate backward from code to requirements

**Fix:** Bidirectional linking
```python
# Test file
"""
Verifies FR-M1 from specifications/features/dashboard-integration.md

This enables backward navigation from test to requirement.
"""
```

### ❌ External References Without Context

**Symptom:** "See spec-kitty docs" without specific citation

**Problem:** Link rot, ambiguous references

**Fix:** Archive external references
```markdown
## External Reference
Source: [spec-kitty Documentation](https://github.com/Priivacy-ai/spec-kitty)
Retrieved: 2026-02-05
Archived: docs/references/external/spec-kitty-2026-02-05.md
Key Concept: Specification-first workflow (Section 2.3)
```

---

## Validation Checklist

**Before merging feature branch:**

- [ ] **Spec → Tests:** Every FR-* requirement has test reference
- [ ] **Tests → Spec:** Every test file has spec reference in docstring
- [ ] **Spec → ADR:** Every architectural choice referenced
- [ ] **ADR → Code:** Every ADR lists affected modules
- [ ] **Code → Spec:** Every module docstring references spec
- [ ] **Links Valid:** No broken file references
- [ ] **Work Log:** Task completion references all artifacts

**CI Validation:**
```bash
# Run traceability validation
npm run validate:traceability

# Checks:
# - All spec requirements have tests
# - All tests reference specs
# - All ADR references resolve
# - No orphaned code modules
```

---

## Tools and Automation

### Link Extraction Script

```bash
#!/bin/bash
# tools/scripts/extract-traceability-links.sh

# Extract all specification requirements
echo "=== Specification Requirements ==="
grep -r "^FR-[A-Z][0-9]:" specifications/ | sort

# Extract test coverage
echo "=== Test Coverage ==="
grep -r "Verifies: FR-" tests/ | sort

# Extract ADR references
echo "=== ADR References ==="
grep -r "ADR-[0-9]" specifications/ docs/ src/ | sort -u
```

### Traceability Matrix Generator

```python
# tools/scripts/generate-traceability-matrix.py
"""
Generate HTML traceability matrix: Requirements → Tests → Code
"""

import re
from pathlib import Path

def extract_requirements(spec_path):
    """Extract FR-* requirements from specification."""
    with open(spec_path) as f:
        return re.findall(r'^(FR-[A-Z]\d+):', f.read(), re.MULTILINE)

def find_tests_for_requirement(req_id):
    """Find tests verifying this requirement."""
    tests = []
    for test_file in Path('tests/acceptance').rglob('*.py'):
        if f'Verifies: {req_id}' in test_file.read_text():
            tests.append(test_file)
    return tests

# Generate matrix...
```

---

## Related Patterns

**Complements:**
- [Specification-Driven Development](spec-driven-development.md) - Creates specs with traceability built-in
- [Directive 018: Traceable Decisions](../directives/018_traceable_decisions.md) - ADR linking requirements
- [Directive 016: ATDD](../directives/016_acceptance_test_driven_dev.md) - Test-first approach

**Extends:**
- Git commit messages linking to issues/tasks
- YAML task files referencing specs
- Work logs documenting artifact relationships

---

## Further Reading

- [SDD Learnings Reflection](../../work/reports/reflections/2026-02-06-specification-driven-development-learnings.md) - Real-world traceability lessons (Section: "Meta-Learnings: Process Improvement")
- [Directive 034: Specification-Driven Development](../directives/034_spec_driven_development.md) - Spec structure requirements
- [Directive 018: Traceable Decisions](../directives/018_traceable_decisions.md) - ADR traceability

---

**Maintained by:** Architect Alphonso, Planning Petra, Curator Claire  
**Version:** 1.0.0  
**Last Updated:** 2026-02-08  
**Status:** ✅ Active
