---
description: 'Prompt for Curator Claire to audit and normalize a target directory'
agent: curator-claire
category: documentation
complexity: medium
inputs_required: PATH, SCOPE, STYLE_DOCS
outputs: curation report, proposed deltas, metrics summary
tags: [curation, consistency, structure, metadata, audit]
version: 2025-11-22
---

Clear context. Bootstrap as Curator Claire. When ready: 

Perform a structural + tonal + metadata curation pass.

## Inputs:

- Target Directory: \<PATH>
- Scope (structure|tone|metadata|links|all): \<SCOPE>
- Style Anchor Docs (comma paths): \<STYLE_DOCS>
- Exclusions (glob patterns): \<EXCLUDE>
- Critical Rules (bullets): \<RULES>
- Expected Audience (path or label): \<AUDIENCE>
- Related ADRs (list): \<ADRS>
- Output Depth (summary|detailed): \<DEPTH>
- Auto-Fix Allowed? (yes/no): \<AUTO_FIX>

## Task:

1. Inventory files (respect \<EXCLUDE>).
2. Derive style + structure norms from \<STYLE_DOCS> (fallback to `docs/specific_guidelines.md`).
3. Produce discrepancy report (sections: Overview, Findings by Category, Recommended Minimal Corrections, Risk Flags, Next Actions).
4. If \<AUTO_FIX> = yes: generate patch block proposals (no direct edits) in `work/curator/PROPOSED_DELTAS.md`.
5. Summarize alignment metrics (consistency %, missing metadata count, broken links found).
6. Append a curation log entry to `work/curator/CURATION_LOG.md`.

## Output:

- `work/curator/\<slug>-CURATION_REPORT.md`
- Optional `work/curator/PROPOSED_DELTAS.md`
- Metrics summary block

## Constraints:

- No silent changes; only propose.
- Keep recommendations minimal & reversible.
- Flag any file lacking required metadata header if strategic/operational/execution layering applies.

Ask clarifying questions if \<PATH> missing or invalid.

