# 008 Artifact Templates Directive

Purpose: Central reference to template locations to prevent duplication and drift.

Template Locations:
- Architecture: `docs/templates/architecture/`
- Lexical: `docs/templates/lexical/`
- Planning: `docs/planning/` (PLAN_OVERVIEW, NEXT_BATCH, DEPENDENCIES, AGENT_TASKS)
- Synthesis: `work/synthesizer/` for draft integration artifacts
- Curator Reports: `work/curator/` discrepancy & validation outputs

Usage Guidance:
- Always check for an existing template before proposing a new one.
- Extend templates minimally; avoid wholesale rewrites.
- When adding a new template, create a short README in the template directory describing:
    - Intent
    - Required fields / sections
    - Example usage

Versioning:
- Major structural changes require updating Version Governance directive (006) if they alter process assumptions.

