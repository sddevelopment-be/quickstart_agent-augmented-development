# Shorthand: test-readability-check

**Alias:** `/test-readability-check`  
**Category:** Quality Assurance  
**Agent:** Dual-agent (Analyst + Expert Reviewer)  
**Complexity:** High  
**Version:** 1.0.0  
**Created:** 2026-02-08

---

## Purpose

Dual-agent validation approach that assesses whether a test suite effectively documents system behavior by reconstructing system understanding purely from test code.

---

## Usage

```
/test-readability-check
```

Or with parameters:
```
/test-readability-check TEST_DIR="tests/acceptance/"
```

---

## Process

1. **Phase 1: Naive Analysis (Agent A)**
   - Read tests without context
   - Reconstruct system understanding
   - Document inferred behavior

2. **Phase 2: Expert Review (Agent B)**
   - Read tests + full context
   - Compare with Agent A findings
   - Assess accuracy gap

3. **Phase 3: Report Generation**
   - Accuracy metrics
   - Documentation gaps
   - Improvement recommendations

---

## Required Inputs

- **Test Directory:** Path to test suite

---

## Output

- Reconstruction accuracy score
- Behavioral documentation gaps
- Architectural context gaps
- Actionable improvement recommendations

---

## Related

- **Template:** `doctrine/templates/prompts/TEST_READABILITY_CHECK.prompt.md`
- **Approach:** `doctrine/approaches/test-readability-clarity-check.md`
- **Directive 017:** Test-Driven Development

---

**Status:** ✅ Active  
**Maintained by:** Quality Assurance Team  
**Last Updated:** 2026-02-08
