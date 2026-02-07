<!-- The following information is to be interpreted literally -->

# 010 Mode Protocol Directive

**Purpose:** Standardize mode transitions across agents for consistent reasoning traceability.

**Core Concepts:
** See [Mode](../GLOSSARY.md#mode), [Mode Transition](../GLOSSARY.md#mode-transition), and [Primer](../GLOSSARY.md#primer) in the glossary.

Modes:

- `/analysis-mode`: Diagnostic, decomposition, validation.
- `/creative-mode`: Option generation, exploratory reframing, pattern ideation.
- `/meta-mode`: Reflection, process alignment, governance calibration.
- `/planning`: Strategic planning, task decomposition, dependency mapping.
- `/programming`: Code implementation, test-driven development, refactoring.
- `/error-handling`: Debugging, error analysis, remediation strategies.
- `/gathering`: Information collection, research, reference accumulation.
- `/assessing`: Critical evaluation, quality assessment, trade-off analysis.

Transition Notation:

- Always annotate transition explicitly: `[mode: analysis → creative]`.
- Do not switch modes more than once per 10 paragraphs or major artifact section unless explicitly requested.

Mode Misuse Indicators:

- Creative drift while unresolved factual gaps remain → flag ⚠️ and revert to analysis.
- Meta-mode used to justify speculative output → flag ❗️ and re-align.
- See [Integrity Symbol](../GLOSSARY.md#integrity-symbol) for marker definitions.

Minimum Artifacts:

- Long multi-step tasks: include a Mode Summary block at completion listing transitions.

Alignment Checks:

- After any meta-mode reflection leading to changes in approach, re-run `/validate-alignment`.
- See [Alignment](../GLOSSARY.md#alignment) and [Validation](../GLOSSARY.md#validation) for protocols.

---

## Primer Binding (ADR-011)

| Primer                         | Required Mode Sequence                                        | Notes                                                                                      |
|--------------------------------|---------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Context Check                  | `/analysis-mode` → `/validate-alignment`                      | Run before and after major context loads; log ✅/⚠️ outcome in work log header.             |
| Progressive Refinement         | `/analysis-mode`\* → `/fast-draft` → `/precision-pass`        | Mark FIRST PASS outputs; refactor in `/analysis-mode` or `/creative-mode` as needed.       |
| Trade-Off Navigation           | `/analysis-mode` throughout                                   | Explicitly structure reasoning as Problem → Forces → Trade-offs → Patterns → Implications. |
| Transparency & Error Signaling | `/analysis-mode` (or active mode) + `/meta-mode` if escalated | Emit ❗️/⚠️ markers inline; switch to `/meta-mode` when pausing for remediation.            |
| Reflection Loop                | `/analysis-mode` → `[mode: analysis → meta]` → `/meta-mode`   | Produce a heuristic or TODO; re-run `/validate-alignment` before resuming work.            |

\* Use `/creative-mode` during ideation stages of Progressive Refinement only after `/fast-draft` scaffolding exists.

### Exception Handling

- **Trivial edits (<2 min, no draft):** Document “Primer exception” in work log; run quick `/analysis-mode` scan regardless.
- **Automation/CI tasks:** If no prose/code authored, record which primers were not applicable.
