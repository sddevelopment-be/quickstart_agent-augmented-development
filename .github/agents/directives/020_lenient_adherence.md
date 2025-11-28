# 020 Lenient Adherence Directive

**Purpose:
** Define five leniency levels so agents and humans can calibrate how strictly they must follow templates, checklists, or procedures when responding to a task. Leniency governs structural adherence, not overall integrity—Operational and Strategic rules always apply.

**Scope:** Documentation reviews, template alignment, refactoring plans, code cleanups, or any task where the requester specifies a leniency value.

## Leniency Levels

| Level | Label               | Expectation                                                                                                                                                                 |
|-------|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0     | _Freeform_          | Do whatever yields the best outcome. Treat templates as inspiration only. Major structural deviations allowed if intent is satisfied.                                       |
| 1     | _Loose Alignment_   | Follow the general section order and include core metadata, but minor omissions or creative reorganizations are fine. Equivalent substitutions accepted without comment.    |
| 2     | _Balanced Fidelity_ | Use every required heading/table from the template, though short contextual notes or extra sub-sections are allowed. Small deviations must be justified in-line.            |
| 3     | _Strict-ish_        | Fully match the template structure and data fields while permitting clearly labeled extras. Only introduce new sections when they complement—not replace—the standard ones. |
| 4     | _Ultra Rigid_       | Copy the template verbatim before populating content. No additional sections, reordering, or renaming. Any divergence requires explicit approval and documentation.         |

## Usage Guide

1. **Requester Duty:** State the leniency level (0–4) when assigning template-sensitive work. Defaults to 2 if unspecified.
2. **Agent Duty:** Document the requested level in outputs or work logs so reviewers know which tolerance was applied.
3. **Conflicts:** When leniency contradicts safety/ethical rules, safety wins.
4. **Escalation:** If strictness prevents meeting core intent, flag ⚠️ or ❗️ and request clarification.

## Metadata

- **Version:** 1.0.0
- **Last Updated:** 2025-11-28
- **Dependencies:** 004 (Documentation & Context Files), 008 (Artifact Templates)
- **Status:** Active
- **Maintainer:** Curator Claire
