# Approach: Decision Reference Types

**Purpose:** Guide for correctly referencing decisions in framework versus repository contexts  
**Status:** Active  
**Version:** 1.0.0  
**Last Updated:** 2026-02-11

---

## Intent

Clarify when to use DDRs (Doctrine Decision Records), Directives, generic ADR placeholders, or repository-specific ADRs to maintain framework portability while preserving decision traceability.

Use this approach when documenting decisions, creating examples, or referencing architectural rationale in doctrine framework files.

---

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
**Location:** `${DOC_ROOT}/architecture/adrs/` (in local repo, NOT in doctrine/)  
**Use when:** Making repository-specific implementation decisions

**Important:** These should NEVER be referenced from `doctrine/` framework files!

**Examples of repository ADRs (stay in local repo):**
- ADR-001: Modular Agent Directive System (this repo's choice)
- ADR-013: Zip-Based Distribution (this repo's tooling)
- ADR-028: Flask-SocketIO for WebSockets (this repo's tech choice)

**In local repo code (outside doctrine/):**
```markdown
✅ ALLOWED in ${DOC_ROOT}/architecture/adrs/ADR-028.md:
   Implements coordination pattern from doctrine/

✅ ALLOWED in src/main.py:
   # Per ADR-028: Using Flask-SocketIO
   
❌ NEVER in doctrine/approaches/example.md:
   Use Flask-SocketIO per ADR-028
```

**Exception for Generic References:**
This approach document may reference the *expected ADR location* generically using `${DOC_ROOT}` variable, which consuming repositories will customize. This is not a violation of dependency direction rules.

---

## Summary Table

| Reference Type | Location | Use Case | Example |
|---------------|----------|----------|---------|
| **DDR-NNN** | `doctrine/decisions/` | Framework-level patterns | DDR-001 (Primer Execution) |
| **Directive NNN** | `doctrine/directives/` | Process requirements | Directive 017 (TDD) |
| **ADR-NNN** | Generic placeholder | Examples/templates | ADR-NNN (tech choice) |
| **Repository ADR** | `${DOC_ROOT}/architecture/adrs/` | Local decisions | Never in doctrine/ |

---

## Related Resources

- **Directive 018:** Traceable Decisions - When to document decisions
- **Directive 020:** Lenient Adherence - Balancing strictness with pragmatism
- **DDR-001:** Primer Execution Matrix - Example framework-level decision
- **DDR-002:** Framework Guardian Role - Example framework-level decision
- **Validation Script:** `work/curator/validate-dependencies.sh` - Automated checking

---

**Version History:**
- 1.0.0 (2026-02-11): Initial creation following Boy Scout Rule ADR violation remediation
