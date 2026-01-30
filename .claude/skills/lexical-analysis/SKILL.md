---
name: "LEXICAL ANALYSIS"
description: "Prompt for Lexical Larry to perform a lexical style diagnostic and minimal diff pass"
version: "1.0.0"
type: "prompt-template"
agent: "lexical-larry"
category: "documentation"
tags: ["lexical", "style", "tone", "diagnostics", "minimal-diffs"]
---

# LEXICAL ANALYSIS

Prompt for Lexical Larry to perform a lexical style diagnostic and minimal diff pass

## Instructions

Clear context. Bootstrap as Lexical Larry. When ready: 

Perform lexical analysis + minimal diff proposal.

## Inputs:
- Target Files (comma paths): \<FILES>
- Style Anchor (path or none): \<ANCHOR>
- Directives (comma codes, optional): \<DIRECTIVES>
- Tone Objectives (bullets): \<TONE>
- Diff Strictness (minimal|moderate|advisory): \<STRICTNESS>
- Report Depth (summary|full): \<DEPTH>
- Include Before/After Snippets? (yes/no): \<SNIPPETS>

## Task:

1. Load style baseline from \<ANCHOR> or `docs/specific_guidelines.md`.
2. Generate `work/LEX/LEX_REPORT.md` (sections: Tone, Rhythm, Markdown Hygiene, Anti-Fluff, Medium Fit, Clarity Before Complexity).
3. Produce `work/LEX/LEX_DELTAS.md` with diff groups per violated rule; obey \<STRICTNESS>.
4. If \<SNIPPETS> = yes: include before/after blocks for non-trivial changes.
5. Provide confidence markers (✓ / ⚠ / ❗) per rule.
6. Summarize metrics: avg sentence length, para length variance, modality issues.

## Output:

- LEX_REPORT.md content
- LEX_DELTAS.md content
- Metrics summary block

## Constraints:

- Preserve author voice; avoid reflow unless necessary.
- No hype, flattery, or style homogenization.
- Only modify lines with concrete rule justification.

Ask clarifying questions if \<FILES> missing.

## Workflow

1. Summarize metrics: avg sentence length, para length variance, modality issues.

## Inputs

- **FILES** (required) - comma paths
- **ANCHOR** (required) - path or none
- **DIRECTIVES** (required) - comma codes, optional
- **TONE** (required) - bullets
- **STRICTNESS** (required) - minimal|moderate|advisory
- **DEPTH** (required) - summary|full
- **SNIPPETS** (required) - yes/no

## Outputs

- Metrics summary block

