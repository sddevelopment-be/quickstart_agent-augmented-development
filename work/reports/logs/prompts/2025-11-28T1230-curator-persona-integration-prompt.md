# Original Prompt Documentation: Persona Approach & Directive

**Task ID:** N/A  
**Agent:** curator-claire  
**Date Executed:** 2025-11-28T12:30:00Z  
**Documentation Date:** 2025-11-28T12:30:00Z

---

## Original Problem Statement

```
Describe the "target-audience fit" approach in a new file under  `agents/approaches`. Then create a new directive titled "Audience Oriented Writing". Add it to the relevant agents.
```

---

## SWOT Analysis

### Strengths

- Clear deliverables: approach file, directive, agent updates.  
- Explicit directory locations (agents/approaches, new directive).  
- “Relevant agents” hint encourages thoughtful scope.

### Weaknesses

- No acceptance criteria for the approach structure (length, sections).  
- “Relevant agents” ambiguous—requires interpretation.  
- Missing instruction about manifest updates or logging requirements.

### Opportunities

- Specify approach contents (steps, inputs/outputs, heuristics).  
- Clarify directive dependencies and logging expectations (Directives 014/015).  
- Provide list of agents expected to load the directive.

### Threats

- Risk of missing manifest entry, causing orphan directive.  
- Over- or under-scoping agent updates without explicit guidance.  
- Without logging instruction, Directive 014 compliance could be overlooked.

---

## Suggested Improvements

### Version 2.0 Prompt

```
1. Read work/notes/ideation/opinionated_platform/target_audience_personas.md and summarize the “Target Audience Personas” practice in a new approach file (agents/approaches/target-audience-fit.md) covering purpose, steps, inputs/outputs, and integration notes.
2. Create Directive 021 “Audience Oriented Writing” (depends on 002 & 004) describing persona identification, context loading, application of the new approach, and logging requirements. Update directives/manifest.json.
3. Update the following agent profiles to load Directive 021 when drafting audience-facing documents: writer-editor, scribe, translator, curator, synthesizer, architect, manager.
4. Produce a work log (Directive 014) and prompt documentation (Directive 015) summarizing the changes, including token usage and rationale metrics.
```

### Improvement Highlights

1. **Explicit File Targets:** Avoids guessing which note inspired the approach.  
2. **Directive Detail:** Captures dependencies, key content, and manifest updates.  
3. **Agent List:** Removes ambiguity around “relevant agents.”  
4. **Compliance Reminder:** Ensures logging requirements are satisfied.

---

## Pattern Recognition

**Effective Elements**
- Sequenced commands with clear outputs.  
- Emphasis on “relevant agents” encourages thoughtful scoping.

**Anti-Patterns**
- ❌ Lacks details on documentation expectations.  
- ❌ Omits logging requirements, risking Directive 014/015 gaps.

---

## Recommendations

1. Always cite source files for new approaches.  
2. When introducing new governance, list dependent updates (manifest, agent references).  
3. Include validation/logging instructions to ensure compliance.

---

**Documented by:** curator-claire  
**Related Work Log:** `work/reports/logs/curator/2025-11-28T1230-persona-integration.md`
