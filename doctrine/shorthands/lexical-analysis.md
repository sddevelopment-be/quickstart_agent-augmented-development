# Shorthand: lexical-analysis

**Alias:** `/lexical-analysis`  
**Category:** Documentation  
**Agent:** Lexical Larry  
**Complexity:** Low  
**Version:** 1.0.0  
**Created:** 2026-02-08

---

## Purpose

Quick command to bootstrap Lexical Larry and perform lexical style diagnostic + minimal diff proposal.

---

## Usage

```
/lexical-analysis
```

Or with parameters:
```
/lexical-analysis FILES="docs/guides/guide1.md,docs/guides/guide2.md"
```

---

## Process

1. Clear context
2. Bootstrap as Lexical Larry
3. Perform analysis:
   - Sentence structure analysis
   - Tone consistency check
   - Readability scoring
   - Style issue identification

---

## Required Inputs

- **Target Files:** Comma-separated paths to analyze

---

## Output

- Lexical analysis report
- Style issues with recommendations
- Minimal diff proposals
- Readability metrics

---

## Related

- **Template:** `doctrine/templates/prompts/LEXICAL_ANALYSIS.prompt.md`
- **Agent Profile:** `doctrine/agents/lexical.agent.md`
- **Follow-up:** `/editor-revision`

---

**Status:** ✅ Active  
**Maintained by:** Lexical Larry  
**Last Updated:** 2026-02-08
