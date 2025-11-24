# Agentic Solutioning Primer – Synthesis & Fit
*Prepared by Architect Alphonso — 2025-11-24*

## Source Snapshot
- Reference: `tmp/reference_docs/solutioning_primer.md`
- Thesis: five primers (Context Check, Progressive Refinement, Trade-Off Navigation, Transparency & Error Signaling, Reflection Loop) define durable behavioral habits for autonomous agents.

## Key Forces & Trade-offs
- **Discipline vs. velocity:** strict primer adherence reduces drift but adds ceremony; mitigate by scripting defaults (e.g., context checks embedded in templates).
- **Self-awareness vs. cognitive load:** reflection loops foster learning yet require time-boxing to avoid analysis paralysis.
- **Traceability vs. privacy:** transparency mandates surfacing assumptions, which can expose sensitive reasoning unless logs are properly scoped.

## Fit to the Agentic Framework
- **Context Stack reinforcement:** the primers mirror AGENTS.md ordering—load context, execute iteratively, analyze forces, signal integrity, then reflect. This file can act as the “linker” between high-level directives and on-the-ground agent behaviors.
- **Command alias utilization:** each primer maps to specific aliases (`/validate-alignment`, `/fast-draft`, `/precision-pass`, `/analysis-mode`, `/meta-mode`). Embedding this mapping into future directives will keep agents consistent.
- **Architectural resonance:** trade-off navigation and reflection loops match our ADR expectations: capture forces, explain implications, note learning for future cycles.

## Application Patterns
1. **Primer Checklist Template:** create an appendix for ADRs or architectural briefs prompting authors to confirm primer usage (e.g., “Context loaded?” “Trade-offs enumerated?”).
2. **Delegation Contracts:** when assigning tasks to specialized agents, specify which primer must dominate (e.g., “Use Progressive Refinement for drafts; run Reflection Loop before handoff”).
3. **Runtime Instrumentation:** add logging hooks in orchestrator workflows capturing mode switches (`analysis → creative → analysis`) to ensure reflections aren’t skipped under load.

## Risks & Open Questions
- Need clarity on how to measure compliance—should we enforce via linting (checking for ✅/⚠️ markers) or rely on human review?
- Reflection loops may generate high-volume meta-notes; determine archival strategy (`work/logs/meta/`?) to keep signal usable.
- Some tasks may legitimately skip primers (e.g., trivial edits); consider heuristics or thresholds to avoid burdening quick iterations.
