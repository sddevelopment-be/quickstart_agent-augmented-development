# 010 Mode Protocol Directive

Purpose: Standardize mode transitions across agents for consistent reasoning traceability.

Modes:
- `/analysis-mode`: Diagnostic, decomposition, validation.
- `/creative-mode`: Option generation, exploratory reframing, pattern ideation.
- `/meta-mode`: Reflection, process alignment, governance calibration.

Transition Notation:
- Always annotate transition explicitly: `[mode: analysis → creative]`.
- Do not switch modes more than once per 10 paragraphs or major artifact section unless explicitly requested.

Mode Misuse Indicators:
- Creative drift while unresolved factual gaps remain → flag ⚠️ and revert to analysis.
- Meta-mode used to justify speculative output → flag ❗️ and re-align.

Minimum Artifacts:
- Long multi-step tasks: include a Mode Summary block at completion listing transitions.

Alignment Checks:
- After any meta-mode reflection leading to changes in approach, re-run `/validate-alignment`.

