---
Ask clarifying questions if <PATH> missing or invalid.

- Flag any file lacking required metadata header if strategic/operational/execution layering applies.
- Keep recommendations minimal & reversible.
- No silent changes; only propose.
Constraints:

- Metrics summary block
- Optional `work/curator/PROPOSED_DELTAS.md`
- `work/curator/<slug>-CURATION_REPORT.md`
Output:

6. Append a curation log entry to `work/curator/CURATION_LOG.md`.
5. Summarize alignment metrics (consistency %, missing metadata count, broken links found).
4. If <AUTO_FIX> = yes: generate patch block proposals (no direct edits) in `work/curator/PROPOSED_DELTAS.md`.
3. Produce discrepancy report (sections: Overview, Findings by Category, Recommended Minimal Corrections, Risk Flags, Next Actions).
2. Derive style + structure norms from <STYLE_DOCS> (fallback to `docs/specific_guidelines.md`).
1. Inventory files (respect <EXCLUDE>).
Task:

- Auto-Fix Allowed? (yes/no): <AUTO_FIX>
- Output Depth (summary|detailed): <DEPTH>
- Related ADRs (list): <ADRS>
- Expected Audience (path or label): <AUDIENCE>
- Critical Rules (bullets): <RULES>
- Exclusions (glob patterns): <EXCLUDE>
- Style Anchor Docs (comma paths): <STYLE_DOCS>
- Scope (structure|tone|metadata|links|all): <SCOPE>
- Target Directory: <PATH>
Inputs:

Perform a structural + tonal + metadata curation pass.

Clear context. Bootstrap as Curator Claire. When ready: 

---
description: 'Prompt for Curator Claire to audit and normalize a target directory'

