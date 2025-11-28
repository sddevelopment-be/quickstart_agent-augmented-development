# Original Prompt Documentation: Audience Fit Increment 2

**Task ID:** N/A  
**Agent:** researcher-ralph  
**Date Executed:** 2025-11-28T13:00:00Z  
**Documentation Date:** 2025-11-28T13:00:00Z

---

## Original Problem Statement

```
I would like you to go through the main README.md, AGENTS.md, and `docs` directory and subdirectories. For each file, tell me what the envisioned audience is. When a directory contains more than 8 files, try and generalize rather than diving into each of them. Remember to use directive 002 and 011. Expected output: A JSON file in the `notes` directory ... **INCREMENTAL RESEARCH:** Start with 5 files, pauze ...
```

Follow-up clarification:

```
(1) store your increments and output into: work/notes/external_memory. (2) You are only to skip analysis of items in a directory if they TEXT/image/code files, subdirectories do not count as a file. ... Do a 10-file increment, let me review
```

---

## SWOT Analysis

### Strengths
- Clear scope with incremental batching to keep analysis manageable.
- Directive references (002, 011) keep context discipline and risk awareness front-of-mind.
- Storage location specified to maintain durable trail of findings.

### Weaknesses
- Directory skipping rule was clarified mid-task, increasing risk of misinterpretation.
- Persona targeting relies on researcher judgment (no explicit mapping provided).
- JSON schema not fully specified beyond narrative instructions.

### Opportunities
- Restate schema expectations in future prompts to reduce ambiguity.
- Note assumptions (e.g., aggregated ADR directory) to ease reviewer validation.
- Encourage referencing persona files directly to increase traceability.

### Threats
- Miscounting files vs subdirectories could violate the “>8 files” condition.
- Forgetting to pause after increments could misalign with user expectations.
- Missing persona coverage could skew downstream tone guidance.

---

## Suggested Improvements

### Version 2.0 Prompt
```
1. Analyze README.md, AGENTS.md, and the docs tree. For each file or directory (count only text/image/code files; subdirectories do not count), list applicable personas from docs/audience/ plus rationale. When applicable, add potential misses for other personas (i.e. personas for whom the content is likely to be relevant, but the format or depth may not suit their needs).
2. Append incremental results to JSON under work/notes/external_memory/ with fields: path, audiences[{audience, fit, rationale, potential_misses}].
3. Apply Directives 002 and 011 during analysis (token discipline, risk checks) and note assumptions when aggregating directories.
4. To ensure expectation fit, use an incremental approach ( 3 - 5 - 10 items) before processing the entire repository. After each initial increment, pause and provide a short textual summary before proceeding. 
5. After user confirmation, continue processing in batches until all items are processed. Do not pause to confirm after the initial alignment increments. Do make a commit to work/notes/external_memory/ after each increment.

Example JSON entry:
{
  "path": "docs/architecture/adrs/ADR-001-example.md",
  "audiences": [
    {
      "audience": "architect",
      "fit": "high",
      "rationale": "Detailed architectural decision record relevant to architects."
    },
    {
      "audience": "developer",
      "fit": "medium",
      "rationale": "Provides context on design choices impacting development."
    }
  ],
  "potential_misses": [
    {
      "audience": "project_manager",
      "rationale": "May lack high-level summaries preferred by project managers."
    }
  ]
}
```

### Improvement Highlights
1. Clarifies counting rules and schema, reducing guesswork.
2. Repeats incremental/pause expectations to ensure compliance.
3. Reinforces directive usage and assumption logging.

---

## Pattern Recognition
- Incremental instructions + pausing keep scope controlled.
- Lack of schema detail repeats across prompts; improvement recommended.

---

## Recommendations
1. Provide schema snippet or sample entry in future prompts.
2. Clarify directory counting rules up front.
3. Include expectation for textual summaries alongside JSON output.

---

**Documented by:** researcher-ralph  
**Related Work Log:** work/reports/logs/curator/2025-11-28T1230-persona-integration.md
