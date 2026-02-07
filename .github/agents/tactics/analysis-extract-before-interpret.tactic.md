# Tactic: Analysis.ExtractBeforeInterpret

**Related tactics:**
- `review-intent-and-risk-first.tactic.md` — uses extraction before interpretation in review context
- `adversarial-testing.tactic.md` — benefits from factual extraction before risk assessment

**Complements:**
- Directive 024 (Self-Observation Protocol) — prevents premature conclusions during Ralph Wiggum checkpoints

---

## Intent
Prevent premature interpretation by first extracting observable facts and patterns before assigning meaning or conclusions.

Use this tactic when analysis or synthesis is required and the risk of bias or premature judgment exists.

---

## Preconditions

**Required inputs:**
- Source material exists (code, text, logs, examples, outputs)
- The task involves analysis or synthesis
- Interpretation is expected as a separate, later step

**Assumed context:**
- Observable elements can be identified and extracted
- Extraction can be performed without requiring interpretation

**Exclusions (when NOT to use):**
- When immediate interpretation is required for time-critical decisions
- When source material is already structured and unambiguous
- When the task is purely generative (no analysis needed)

---

## Execution Steps

1. Identify the source material to be analyzed.
2. Extract observable elements verbatim (tokens, structures, statements, patterns).
3. Organize extracted elements into simple lists or tables.
4. Explicitly label this output as "extraction only" or "facts without interpretation".
5. Stop without drawing conclusions or implications.
6. (If interpretation is needed) Proceed with interpretation as a separate, distinct step after extraction is complete.

---

## Checks / Exit Criteria
- Extracted data contains no interpretation or judgment.
- Source references are preserved.
- Output can be reviewed independently without requiring domain knowledge.
- Extraction is complete enough to support later interpretation.

---

## Failure Modes
- Collapsing extraction and interpretation into one step.
- Renaming or normalizing extracted data prematurely.
- Adding inferred meaning during extraction.
- Omitting observable details because they seem irrelevant.

---

## Outputs
- Structured extraction artifact (lists, tables, JSON, CSV, etc.)
- Clear source references or citations

---

## Notes on Use

This tactic pairs well with:
- **Code review** — extract patterns before interpreting intent or risk
- **Log analysis** — extract events before inferring causation
- **Requirement gathering** — extract stated needs before proposing solutions

Extraction without interpretation creates a **shared factual foundation** before divergent reasoning begins.

---
