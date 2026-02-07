---
description: 'Prompt for Architect Alphonso to perform analysis and draft a Proposed ADR'
agent: architect-alphonso
category: architecture
complexity: high
inputs_required: TITLE, CONTEXT, FORCES, OPTIONS, PREFERRED
outputs: ADR markdown, option impact matrix, success metrics
tags: [architecture, adr, decision-record, trade-offs, design]
version: 2025-11-22
---

Clear context. Bootstrap as Architect Alphonso. When ready: 

Execute an architectural analysis and draft a Proposed ADR.

## Inputs:

- Decision Title: \<TITLE>
- Problem Context (paragraph): \<CONTEXT>
- Forces / Constraints (bullets): \<FORCES>
- Options (bullets, short labels): \<OPTIONS>
- Preferred Option: \<PREFERRED>
- Impact Areas (e.g., performance, portability, maintainability): \<IMPACTS>
- Related Artifacts (paths): \<RELATED>
- Existing ADR References (list): \<ADR_REFS>
- Risk Appetite (low|medium|high): \<RISK_APPETITE>
- Time Horizon (short|medium|long): \<HORIZON>
- Non-Functional Requirements (bullets): \<NFRS>

## Task:

1. Validate uniqueness of \<TITLE> vs existing ADRs.
2. Decompose context into problem statement + drivers + constraints.
3. Analyze each \<OPTION> against \<IMPACTS> and \<NFRS> (matrix-style, qualitative scores).
4. Provide rationale for selecting \<PREFERRED> (trade-off narrative).
5. Draft ADR in template format (status: Proposed) with sections: Context, Decision, Rationale, Envisioned Consequences (+ positive/negative), Considered Alternatives.
6. Add risk assessment (tie to \<RISK_APPETITE>) and horizon alignment.
7. Suggest acceptance criteria + success metrics.
8. Output file: `${DOC_ROOT}/architecture/adrs/ADR-XXX-\<slug>.md` (choose next number).
9. Provide diff plan for cross-link updates (README index).

## Output:
- ADR markdown content
- Option Impact Matrix block
- Success Metrics list

## Constraints:
- Keep Decision section ≤ 120 words.
- Each alternative: one sentence reason for rejection.
- Avoid speculative implementation detail; defer to Technical Design doc if needed.

Ask clarifying questions if \<CONTEXT> or \<PREFERRED> ambiguous.

