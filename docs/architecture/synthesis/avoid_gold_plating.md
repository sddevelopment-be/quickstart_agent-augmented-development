# Avoid Gold Plating – Agentic Fit Analysis
*Prepared by Architect Alphonso — 2025-11-24*

## Source Snapshot
- Reference: `tmp/reference_docs/avoid_gold_plating.md`
- Core thesis: deliver only the design fidelity needed **now**, note richer ideas for future iterations, and work in small increments to keep throughput high.

## Key Forces & Trade-offs
- **Throughput vs. Optionality:** throttling scope accelerates delivery but reduces optionality unless teams maintain explicit logs of deferred ideas.
- **Readability vs. Future-proofing:** intentionally lean designs keep code approachable yet risk churn if requirements evolve faster than expected.
- **Risk posture:** works best where failure cost is modest and change cadence is high; safety-critical contexts may demand more upfront structure.

## Fit to the Agentic Framework
- **Bootstrap & Operational guidance:** aligns with the directive to keep work increments reviewable; agents should log “better ideas later” inside `work/notes` rather than embedding scaffolding prematurely.
- **Strategic resonance:** supports the framework’s bias toward progressive refinement and structured delegation—agents can spike or scaffold in `work/` artifacts, then promote hardened designs only when value is proven.
- **Command alias mapping:** pair `/fast-draft` with `/summarize-notes` to capture deferred abstractions; follow with `/validate-alignment` before promoting simplifications that might erode architecture.

## Application Patterns
1. **Synthesis staging:** when designing components, agents produce a minimal interface spec plus a backlog entry referencing richer abstractions; future ADRs can elevate those notes as requirements firm up.
2. **Review hooks:** embed “gold plating check” prompts inside design reviews (e.g., ADR templates asking whether scope exceeds validated demand).
3. **Runway management:** map technical debt intentionally—lightweight modules carry “expiry dates” that trigger reassessment by architecture agents before reuse.

## Risks & Open Questions
- How do we ensure that deferred improvements are actually revisited? Suggest tracking them via `docs/architecture/patterns` backlog or `work/planning`.
- What metrics indicate harmful under-design (e.g., repeated rework in the same module)? Need instrumentation guidance before codifying into directives.
- Agents must avoid equating “no gold plating” with “skip documentation”; synthesis outputs like this file remain mandatory even for lean implementations.
