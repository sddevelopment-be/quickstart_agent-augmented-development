# Shorthand: curate-directory

**Alias:** `/curate-directory`  
**Category:** Documentation  
**Agent:** Curator Claire  
**Complexity:** Medium  
**Version:** 1.0.0  
**Created:** 2026-02-08

---

## Purpose

Quick command to bootstrap Curator Claire and perform structural + tonal + metadata curation pass.

---

## Usage

```
/curate-directory
```

Or with parameters:
```
/curate-directory TARGET="docs/architecture/"
```

---

## Process

1. Clear context
2. Bootstrap as Curator Claire
3. Perform curation audit:
   - Structural consistency
   - Naming conventions
   - Cross-references
   - Metadata completeness

---

## Required Inputs

- **Target Directory:** Path to directory for curation

---

## Output

- Discrepancy report with findings
- Corrective action recommendations
- Validation summary post-corrections

---

## Related

- **Tactic:** `doctrine/tactics/documentation-curation-audit.tactic.md`
- **Template:** `doctrine/templates/prompts/CURATE_DIRECTORY.prompt.md`
- **Agent Profile:** `doctrine/agents/curator.agent.md`
- **Directive 014:** Work Log Creation

---

**Status:** ✅ Active  
**Maintained by:** Curator Claire  
**Last Updated:** 2026-02-08
