# Shorthand: editor-revision

**Alias:** `/editor-revision`  
**Category:** Documentation  
**Agent:** Writer-Editor  
**Complexity:** Medium  
**Version:** 1.0.0  
**Created:** 2026-02-08

---

## Purpose

Quick command to bootstrap Writer-Editor and refine draft based on lexical analysis outputs.

---

## Usage

```
/editor-revision
```

Or with parameters:
```
/editor-revision DRAFT="docs/guides/my-guide.md"
```

---

## Process

1. Clear context
2. Bootstrap as Writer-Editor
3. Refine draft:
   - Apply lexical analysis recommendations
   - Improve clarity and tone
   - Fix structural issues
   - Enhance readability

---

## Required Inputs

- **Draft File:** Path to document for revision

---

## Output

- Revised document
- Change summary
- Style improvements applied

---

## Related

- **Template:** `doctrine/templates/prompts/EDITOR_REVISION.prompt.md`
- **Agent Profile:** `doctrine/agents/writer-editor.agent.md`
- **Shorthand:** `/lexical-analysis` (prerequisite)

---

**Status:** ✅ Active  
**Maintained by:** Writer-Editor  
**Last Updated:** 2026-02-08
