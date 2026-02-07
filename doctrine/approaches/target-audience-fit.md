# Target-Audience Fit Approach

**Approach Type:** Communication Pattern  
**Version:** 1.0.0  
**Last Updated:** 2025-11-28  
**Status:** Active

## Purpose

Translate the “Target Audience Personas” practice (see
`work/notes/ideation/opinionated_platform/target_audience_personas.md`) into a repeatable workflow so every artifact intentionally addresses the right reader. Writers and editors use this approach to keep tone, depth, and structure aligned with actual personas rather than a generic “user.”

## Core Steps

1. **Identify Reader Segment** – Determine which persona(s) in `docs/audience/` the artifact must serve. When none fit, capture a draft persona in
   `work/notes/` and flag for curator follow-up.
2. **Load Persona Context
   ** – Ingest the persona file (goals, frustrations, engagement style) plus any supporting notes or external-memory snippets that mention that audience.
3. **Plan Differentiation
   ** – Decide whether a single artifact with signposted sections suffices or whether multiple variants are required (split content if depth/needs diverge sharply).
4. **Write/Revise with Filters
   ** – While drafting, periodically check: “Does this sentence help Persona X solve their stated pain point?” Adjust tone, vocabulary, and examples accordingly.
5. **Validate & Log
   ** – Record in the summary/work log which personas were targeted and how the artifact addresses their needs. Note deviations or new insights for persona maintenance.

## Tips & Heuristics

- **Use Persona Tables:
  ** The “Desiderata” and “Behavioral Cues” tables are quick checklists—ensure your draft speaks to each row relevant to the persona.
- **Signpost Sections:** Label portions of the document (“For Jordan – getting started”) if serving multiple audiences to reduce cognitive load.
- **Split When Necessary:
  ** If attempting to address conflicting needs (e.g., senior architect vs. motivated beginner) forces excessive caveats, produce separate docs or appendices.
- **Refresh Context Frequently:** Personas are living artifacts; skim
  `work/notes/external_memory/` or recent work logs for updates before large writing efforts.

## Inputs & Outputs

| Input                            | Source                                                                 |
|----------------------------------|------------------------------------------------------------------------|
| Persona files                    | `docs/audience/*.md`                                                   |
| Persona practice note            | `work/notes/ideation/opinionated_platform/target_audience_personas.md` |
| Structural templates             | `${DOC_ROOT}/templates/`                                                      |
| External-memory notes (optional) | `work/notes/external_memory/`                                          |

| Output                       | Expectation                                 |
|------------------------------|---------------------------------------------|
| Aligned artifact             | Tone/structure mapped to a specific persona |
| Summary note/log             | References personas used + rationale        |
| Persona feedback (as needed) | Insights filed for curator updates          |

## Integration

- **Directive 021 (Audience Oriented Writing)** enforces use of this approach for writing-focused agents.
- Pair with **Directive 004** to locate structural references and **Directive 002** for token discipline when loading persona context.

---

_Maintainers: Curator Claire & Writer-Editor team_
