<!-- The following information is to be interpreted literally -->
# 012 Common Operating Procedures Directive

Purpose: Centralize repeated behavioral norms WITHOUT removing them from individual agent profiles (redundancy is intentional for safety and predictability).

## 1. Core Behaviors

- Always ask clarifying questions when uncertainty >30% about scope, constraints, or desired artifact format.
- Validate alignment before high-impact operations; run `/validate-alignment` on long tasks.
- Preserve authorial voice and structural intent; prefer minimal diffs.
- Avoid speculative reasoning; state "I don't know" rather than fabricate.
- Annotate assumptions explicitly; mark low-confidence with ⚠️.
- Announce potentially irreversible operations before execution.
- Maintain one active plan item focus; avoid parallel speculative branches.

## 2. Redundancy Rationale

This directive **intentionally duplicates** behavioral norms found in individual agent profiles and other directives. This redundancy serves critical safety and operational purposes.

**Key Points:**
- Repetition reinforces critical norms regardless of context loading order
- Protection against partial context loss or fragmentation
- Ensures consistency across different agent specializations
- Simplifies validation and audit processes
- Supports recovery and session rehydration

**Design Decision:** We accept the ~200-300 token overhead in exchange for increased reliability and safety.

**For detailed rationale:** See `.github/agents/approaches/operating_procedures/01_redundancy_rationale.md`

## 3. Non-Removal Clause

The line "Ask clarifying questions when uncertainty >30%." MUST remain in every agent's Collaboration Contract section.

**Reason:** This specific threshold is safety-critical and must be visible in every agent's primary operating context, not just in external directives that may or may not be loaded.

## 4. Usage

- Agents may reference this directive to justify pausing execution awaiting clarification.
- Manager & Planning agents use this to enforce coordination discipline.
- Curator agents validate agent outputs against these centralized norms.
- Human reviewers reference this directive to assess agent behavior quality.

