# Before & After: ADR Violation Fixes

## Critical Fixes

### Fix 1: Directive 017 - Test-Driven Development

**Before:**
```markdown
- Exception: trivial shell utilities or disposable scripts noted per ADR-012.

## Related Resources
- **ADR-012:** Test-Driven Development Mandate
```

**After:**
```markdown
- Exception: trivial shell utilities or disposable scripts (document exception rationale in work log per Directive 014).

## Related Resources
- **Directive 014:** Work Log Creation (for documenting test exceptions)
```

**Rationale:** ADR-012 was a repository-specific decision. The framework should reference the directive that defines the process.

---

### Fix 2: Agent Profiles - Test-First Requirement

**Before:**
```markdown
**Test-First Requirement:** Follow Directives 016 (ATDD) and 017 (TDD) whenever 
authoring or modifying executable code; document any ADR-012 exception in the work log.
```

**After:**
```markdown
**Test-First Requirement:** Follow Directives 016 (ATDD) and 017 (TDD) whenever 
authoring or modifying executable code; document any test-first exception in the 
work log per Directive 014.
```

**Rationale:** Removes dependency on local ADR-012, explains the concept ("test-first exception") and references the correct directive for logging.

---

### Fix 3: DDR-001 - Primer Execution Matrix

**Before:**
```markdown
**status**: Accepted  
**date**: 2026-02-11  
**supersedes**: ADR-011 (content extracted and elevated to doctrine)
```

**After:**
```markdown
**status**: Accepted  
**date**: 2026-02-11  
**supersedes**: Repository-level primer decisions (elevated to framework level)
```

**Rationale:** DDR doesn't reference specific local ADR numbers. Describes what was superseded generically.

---

### Fix 4: Ralph Wiggum Loop Approach

**Before:**
```markdown
**Related:** Directive 010 (Mode Protocol), ADR-011 (Primer Alignment), 
            Directive 024 (Self-Observation Protocol)

### Relation to Reflection Loop Primer (ADR-011)

## References
- **ADR-011:** Command Alias Primer Alignment (reflection loop)
```

**After:**
```markdown
**Related:** Directive 010 (Mode Protocol), DDR-001 (Primer Execution Matrix), 
            Directive 024 (Self-Observation Protocol)

### Relation to Reflection Loop Primer (DDR-001)

## References
- **DDR-001:** Primer Execution Matrix (reflection loop primer definition)
```

**Rationale:** ADR-011 is now DDR-001 (framework decision), so approach references the DDR.

---

## Example Genericization Fixes

### Fix 5: Traceable Decisions Detailed Guide

**Before:**
```markdown
Step 2: Identify relevant: ADR-002, ADR-003, ADR-008
Step 3: Load full text of ADR-008 (File-Based Async Coordination)
Step 5: Reference in proposal: "Per ADR-008, will use file-based handoff..."

## Work Log Entry
Architecture: ADR-008 (File-Based Async Coordination)
Related: ADR-003 (Task Lifecycle State Management)
```

**After:**
```markdown
Step 2: Identify relevant: ADR-YYY, ADR-MMM, ADR-NNN
Step 3: Load full text of ADR-NNN (coordination pattern)
Step 5: Reference in proposal: "Per ADR-NNN (coordination pattern), will use file-based handoff..."

## Work Log Entry
Architecture: ADR-NNN (coordination pattern)
Related: ADR-MMM (lifecycle management)
```

**Rationale:** These are instructional examples showing the pattern. Using generic placeholders makes them portable.

---

### Fix 6: Traceability Chain Pattern

**Before:**
```markdown
# Implementation note: Uses Flask-SocketIO per ADR-028

## ADR-028: WebSocket Technology Choice

from flask_socketio import SocketIO  # ADR-028: Chosen technology

**ADR Referenced:** ADR-028 (WebSocket Technology Choice)
```

**After:**
```markdown
# Implementation note: Uses WebSocket library per ADR-NNN (technology choice)

## ADR-NNN (technology choice): WebSocket Technology Choice

from flask_socketio import SocketIO  # ADR-NNN (technology choice): Chosen technology

**ADR Referenced:** ADR-NNN (WebSocket Technology Choice)
```

**Rationale:** Example showing how to reference technology decisions. Generic placeholder shows the pattern.

---

### Fix 7: Trunk-Based Development

**Before:**
```markdown
git commit -m "docs(adr): add ADR-019 trunk-based development"

### 2. Path Conventions (ADR-004)
```

**After:**
```markdown
git commit -m "docs(adr): add ADR-NNN (trunk-based development)"

### 2. Path Conventions (ADR-NNN (path conventions))
```

**Rationale:** Example commit messages and section headers use generic placeholders.

---

## Template Fixes

### Fix 8: Task Descriptor Template

**Before:**
```yaml
# outcomes:
#   summary: "Created ADR-006 with versioning recommendations"
#   next_task_title: "Review and polish ADR-006 for clarity"

# References:
# - ADR-002: File-Based Asynchronous Agent Coordination
# - ADR-003: Task Lifecycle and State Management
```

**After:**
```yaml
# outcomes:
#   summary: "Created ADR-NNN (versioning decision) with recommendations"
#   next_task_title: "Review and polish ADR-NNN for clarity"

# References:
# - ADR-YYY (coordination pattern): File-Based Asynchronous Agent Coordination
# - ADR-MMM (lifecycle pattern): Task Lifecycle and State Management
```

**Rationale:** Template shows the pattern with generic placeholders instead of specific numbers.

---

### Fix 9: Prompt Templates (All 5 Canonical Templates)

**Before:**
```yaml
# Addresses: Patterns 1-9, 11 from ADR-023

**Related:** ADR-023 Prompt Optimization Framework
```

**After:**
```yaml
# Addresses: Patterns 1-9, 11 from Directive 023 (Clarification Before Execution)

**Related:** Directive 023 (Clarification Before Execution) - Prompt Optimization Framework
```

**Rationale:** ADR-023 was actually defining Directive 023. Reference the directive, not the local ADR.

---

## Guardian & Distribution Fixes

### Fix 10: GUARDIAN_UPGRADE_PLAN Template

**Before:**
```markdown
+When mode transitions occur, agents must invoke appropriate primers per ADR-011.

## References
- **ADR-013:** Zip-Based Framework Distribution
- **ADR-014:** Framework Guardian Agent

3. **Check ADR-014:** Framework Guardian decision rationale
```

**After:**
```markdown
+When mode transitions occur, agents must invoke appropriate primers per DDR-001 (Primer Execution Matrix).

## References
- **DDR-002:** Framework Guardian Role (distribution pattern)

3. **Check DDR-002:** Framework Guardian decision rationale
```

**Rationale:** Guardian and distribution are framework-level patterns (DDRs), not local decisions.

---

### Fix 11: RELEASE_NOTES Template

**Before:**
```markdown
> 🛡️ This release has been validated by Framework Guardian per ADR-014.

- **Framework Guardian Metadata**: NEW in v2.0.0 - ADR-014 compliance

The Guardian Metadata section is a key addition per ADR-014.

- **v2.0.0**: Added Guardian Metadata and Distribution Metadata sections per ADR-013/014
```

**After:**
```markdown
> 🛡️ This release has been validated by Framework Guardian per DDR-002 (Framework Guardian).

- **Framework Guardian Metadata**: NEW in v2.0.0 - DDR-002 (Distribution Pattern) compliance

The Guardian Metadata section is a key addition per DDR-002 (Distribution Pattern).

- **v2.0.0**: Added Guardian Metadata and Distribution Metadata sections per DDR-002 (Distribution Pattern)
```

**Rationale:** Guardian pattern is a framework decision (DDR-002), not local implementation.

---

## Self-Reference Removal

### Fix 12: Directive 018 - Traceable Decisions

**Before:**
```markdown
## Related Resources
- **Approach:** [`traceable-decisions-detailed-guide.md`](../approaches/traceable-decisions-detailed-guide.md)
- **Tactic:** [`adr-drafting-workflow.tactic.md`](../tactics/adr-drafting-workflow.tactic.md)
- **ADR-017:** Self-referential; defines traceable decision patterns
```

**After:**
```markdown
## Related Resources
- **Approach:** [`traceable-decisions-detailed-guide.md`](../approaches/traceable-decisions-detailed-guide.md)
- **Tactic:** [`adr-drafting-workflow.tactic.md`](../tactics/adr-drafting-workflow.tactic.md)
```

**Rationale:** Directive doesn't need to reference the ADR that created it. The directive stands on its own.

---

## Pattern Summary

| Pattern | Count | Before Example | After Example |
|---------|-------|----------------|---------------|
| ADR → DDR | 12 | ADR-011 | DDR-001 (Primer Matrix) |
| ADR → Directive | 15 | ADR-012 | Directive 017 (TDD) |
| Specific → Generic | 48 | ADR-028 | ADR-NNN (tech choice) |
| Remove Reference | 3 | ADR-017 (self) | (removed) |

---

## Key Principles Applied

1. **Framework Independence:** Framework artifacts don't depend on local repository decisions
2. **Generic Examples:** Templates use ADR-NNN to show patterns without hardcoding
3. **Correct Abstraction:** DDRs for framework, Directives for process, ADRs for local
4. **Preserve Intent:** All original meanings maintained, just decoupled from local implementation

---

_Before/After Examples compiled by Curator Claire_  
_2026-02-11_
