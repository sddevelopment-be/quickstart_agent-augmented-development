# Quick Reference: Framework vs Repository Decision References

## When to Use What

### ✅ Framework Decisions (DDR-NNN)
**Location:** `doctrine/decisions/`  
**Use when:** Pattern applies universally across all repositories adopting the framework

**Examples:**
- DDR-001: Primer Execution Matrix (universal agent behavior pattern)
- DDR-002: Framework Guardian Role (universal upgrade/audit pattern)

**In code:**
```markdown
See DDR-001 (Primer Execution Matrix) for primer binding requirements.
```

---

### ✅ Directive References
**Location:** `doctrine/directives/`  
**Use when:** Referencing process, workflow, or behavioral requirements

**Examples:**
- Directive 014: Work Log Creation
- Directive 017: Test-Driven Development
- Directive 018: Traceable Decisions
- Directive 023: Clarification Before Execution

**In code:**
```markdown
Document exception rationale per Directive 014 (Work Log Creation).
Follow Directive 017 (TDD) for test-first development.
```

---

### ✅ Generic ADR Placeholders (ADR-NNN)
**Use when:** Providing instructional examples or templates

**Pattern:**
```markdown
ADR-NNN (descriptive suffix)
```

**Examples:**
```markdown
# In template files
See ADR-NNN (technology choice) for implementation details.
Reference ADR-MMM (coordination pattern) for handoff protocol.
Check ADR-PPP (architecture decision) for rationale.
```

---

### ❌ Repository-Specific ADRs
**Location:** `docs/architecture/adrs/` (in local repo, NOT in doctrine/)  
**Use when:** Making repository-specific implementation decisions

**Important:** These should NEVER be referenced from `doctrine/` framework files!

**Examples of repository ADRs (stay in local repo):**
- ADR-001: Modular Agent Directive System (this repo's choice)
- ADR-013: Zip-Based Distribution (this repo's tooling)
- ADR-028: Flask-SocketIO for WebSockets (this repo's tech choice)

**In local repo code (outside doctrine/):**
```markdown
✅ ALLOWED in docs/architecture/adrs/ADR-028.md:
   Implements coordination pattern from doctrine/

✅ ALLOWED in src/main.py:
   # Per ADR-028: Using Flask-SocketIO
   
❌ NEVER in doctrine/approaches/example.md:
   Use Flask-SocketIO per ADR-028
```

---

## Migration Patterns

### Pattern 1: ADR → DDR (Framework Decision)
When an ADR represents a universal framework pattern:

**Before:**
```markdown
Per ADR-011, agents must execute primer checks.
```

**After:**
```markdown
Per DDR-001 (Primer Execution Matrix), agents must execute primer checks.
```

---

### Pattern 2: ADR → Directive (Process Requirement)
When an ADR enforces a process or workflow:

**Before:**
```markdown
Exception must be documented per ADR-012.
```

**After:**
```markdown
Exception must be documented per Directive 017 (TDD) and Directive 014 (Work Log).
```

---

### Pattern 3: Specific ADR → Generic ADR-NNN (Example)
When showing example patterns:

**Before:**
```markdown
# Example commit message
architect: add ADR-028 for WebSocket choice
```

**After:**
```markdown
# Example commit message
architect: add ADR-NNN (technology choice) for WebSocket selection
```

---

### Pattern 4: Remove Reference (Self-Referential)
When a directive references the ADR that created it:

**Before:**
```markdown
## References
- **ADR-017:** Self-referential; defines traceable decision patterns
```

**After:**
```markdown
## References
(Remove - directive stands on its own)
```

---

## Validation

Check for violations:
```bash
bash work/curator/validate-dependencies.sh
```

Expected output:
```
✅ No dependency direction violations found
All framework artifacts properly abstracted from local ADRs.
```

---

## Decision Tree

```
┌─────────────────────────────────────────┐
│ Need to reference a decision pattern?  │
└───────────────┬─────────────────────────┘
                │
                ├─ Is it a universal framework pattern?
                │  (primers, agents, distribution)
                │  → Use DDR-NNN reference
                │
                ├─ Is it a process/workflow requirement?
                │  (testing, logging, documentation)
                │  → Use Directive NNN reference
                │
                ├─ Is it an instructional example?
                │  (showing how to reference ADRs)
                │  → Use ADR-NNN (generic placeholder)
                │
                └─ Is it a repository-specific choice?
                   (technology, tooling, local structure)
                   → Use ADR-NNN ONLY in local repo files
                     NEVER in doctrine/ framework files
```

---

## Common Mistakes

### ❌ Mistake 1: Framework file references local ADR
```markdown
# In doctrine/approaches/example.md
Implements Flask-SocketIO per ADR-028  ← WRONG
```

**Fix:** Genericize the example
```markdown
# In doctrine/approaches/example.md
Implements WebSocket library per ADR-NNN (technology choice)  ← RIGHT
```

---

### ❌ Mistake 2: Using ADR when Directive exists
```markdown
Follow test-first development per ADR-012  ← WRONG
```

**Fix:** Reference the directive
```markdown
Follow Directive 017 (TDD) for test-first development  ← RIGHT
```

---

### ❌ Mistake 3: Hardcoding ADR numbers in templates
```markdown
# Task template
summary: "Created ADR-028 with technology choice"  ← WRONG
```

**Fix:** Use generic placeholder
```markdown
# Task template
summary: "Created ADR-NNN with technology choice"  ← RIGHT
```

---

## Quick Checklist

When writing framework code in `doctrine/`:

- [ ] ✅ Use DDR-NNN for framework-level patterns
- [ ] ✅ Use Directive NNN for process requirements
- [ ] ✅ Use ADR-NNN for generic examples
- [ ] ❌ NEVER reference specific local ADR-001, ADR-028, etc.
- [ ] ✅ Run validation script before committing
- [ ] ✅ Preserve original meaning when refactoring

---

_Quick Reference compiled by Curator Claire_  
_2026-02-11_
