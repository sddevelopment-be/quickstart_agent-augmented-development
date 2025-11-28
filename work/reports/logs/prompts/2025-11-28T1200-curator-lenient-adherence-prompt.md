# Original Prompt Documentation: Lenient Adherence Directive + Persona Alignment

**Task ID:** N/A  
**Agent:** curator-claire  
**Date Executed:** 2025-11-28T12:00:00Z  
**Documentation Date:** 2025-11-28T12:00:00Z

---

## Original Problem Statement

```
Remember this, by storing it in `notes/external_memory`. Next: Write a new directive titled "Lenient adherence", which details 5 different leniency levels rated from 0 (do whatever, minimal adherance) to 4 (extremely strict adherence). My previous prompt describes leniency level 3 (strict-ish). Then, apply the changes suggested earlier to align the `docs/audience` files to the PERSONA template.  Then, Apply directives 014 and 015.
```

---

## SWOT Analysis

### Strengths

- Specifies exact storage location for the “remember this” step.
- Defines directive title, scale (0–4), and example of level 3.
- References prior findings (“changes suggested earlier”) to scope persona updates.
- Explicitly calls out directives 014 and 015, clarifying compliance expectations.

### Weaknesses

- Does not state whether other personas need verification again (implicit assumption from earlier result).
- “Apply directives 014 and 015” lacks detail on expected deliverables (e.g., naming conventions, templates).
- No explicit success criteria for leniency directive format beyond listing the five levels.
- Doesn’t mention whether manifest updates or other metadata changes are required.

### Opportunities

- Clarify that leniency directive should include guidance on default behavior, escalation, and conflicts.
- Spell out which files require updates (e.g., manifest.json, README references) to avoid assumptions.
- Provide acceptance criteria for persona alignment (e.g., “automation_agent only” vs. “all entries”).
- Include whether prompt/work-log artifacts need to reference each other.

### Threats

- Agent might over- or under-apply Directive 015 if “Apply directives 014 and 015” isn’t interpreted correctly.
- Without manifest mention, directive could become orphaned from discovery tools.
- Lack of explicit list of affected audience files could lead to redundant edits or missed personas.
- Vague leniency description might yield inconsistent future usage if not formalized properly.

---

## Suggested Improvements

### Version 2.0: Enhanced Prompt

```
1. Capture the earlier leniency observation inside `work/notes/external_memory/` (create a dated markdown note summarizing the finding).
2. Create a new directive `.github/agents/directives/020_lenient_adherence.md` that defines leniency levels 0–4, explains requester/agent responsibilities, and notes that level 3 equals “strict-ish.” Update `manifest.json` accordingly.
3. Re-evaluate every file in `docs/audience/` against `docs/templates/architecture/PERSONA.md`; fix any non-compliant personas (current known issue: `automation_agent.md` diverges) while keeping extra sections that complement the template.
4. Produce artifacts required by Directives 014 and 015:
   - Work log in `work/reports/logs/curator/` covering the tasks above.
   - Prompt documentation in `work/logs/prompts/` referencing this request and linking back to the work log.
5. Report back with a summary of changes and any residual risks.
```

### Improvements Explained

**1. Explicit file targets:**  
- What changed: Item 3 now states to review “every file in `docs/audience/`” and names `automation_agent.md`.  
- Why: Removes ambiguity about scope.  
- Impact: Prevents redundant edits or missed personas.

**2. Directive deliverable clarity:**  
- What changed: Item 2 references filename, numbering, dependencies, and manifest updates.  
- Why: Ensures discoverability.  
- Impact: Avoids orphan directives.

**3. Directive 014/015 specifics:**  
- What changed: Item 4 specifies exact file paths for logs and prompt docs.  
- Why: Eliminates guesswork.  
- Impact: Faster compliance, easier verification.

**4. Reporting requirement:**  
- What changed: Added Item 5 requesting a summary/residual risks.  
- Why: Provides closure and review context.  
- Impact: Helps stakeholders validate work quickly.

---

## Pattern Recognition

### Effective Prompt Elements

1. Sequenced instructions (“Remember this… Next… Then…”) keep tasks ordered.
2. References to previous findings ensure continuity.
3. Mandating directives 014/015 encourages logging discipline.

### Anti-Patterns to Avoid

1. ❌ Vague instructions like “apply directives” without specifying deliverables or locations.  
2. ❌ Implicit assumptions (“changes suggested earlier”) that depend on agent memory.  
3. ❌ Missing metadata updates when adding new governance artifacts.

---

## Recommendations for Similar Prompts

For template-alignment tasks:
1. List every target file explicitly or specify “all files in <directory>”.
2. Provide acceptance criteria (e.g., “matches all template headings”).
3. State follow-up artifacts (work logs, prompt docs) with exact paths.
4. Include reporting expectations (summary, risks, verification steps).

---

**Documented by:** curator-claire  
**Date:** 2025-11-28T12:00:00Z  
**Purpose:** Improve future leniency-alignment prompts  
**Related:** Work log `work/reports/logs/curator/2025-11-28T1200-lenient-adherence.md`
