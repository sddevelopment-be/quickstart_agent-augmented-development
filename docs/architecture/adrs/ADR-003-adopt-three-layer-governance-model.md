# ADR-003: Adopt Three-Layer Governance Model

> **Date:** 2025-11-22  
> **Status:** Accepted  
> **Date Accepted:** 2025-11-22  
> **Authors:** Architect Alphonso  
>   
> **Supersedes:** None  
> **Depends On:** [ADR-001](./ADR-001-modular-agent-directive-system.md), [ADR-002](./ADR-002-portability-enhancement-opencode.md)    
> **Tags:** governance, layering, directives, portability

## Context

Growth in agent specialization and directive complexity has introduced coupling between strategic vision documents, operational guidelines, and execution-level directives. ADR-001 established modular directives; ADR-002 emphasized portability. Without a stratified governance model, change control and version integrity are at risk, reducing portability reliability and increasing semantic drift.

## Decision

Adopt a formal Three-Layer Governance Model:

1. Strategic Layer: Vision artifacts, high-stability principles, version governance, cross-cutting direction.
2. Operational Layer: Patterns, guidelines, reusable templates, specialization schemata.
3. Execution (Command) Layer: Concrete directives, agent capability manifests, validation rules.

Each artifact will include a required metadata header:

```
---
layer: strategic|operational|execution
version: <semantic or date-based>
status: active|deprecated|draft
owner: <role/persona>
review_cycle: <interval or event>
related_adrs: [ADR-001, ADR-002, ...]
portability: stable|guarded|internal
---
```

## Rationale

- Clarifies authority boundaries (strategic changes require ADR; operational via review; execution via standard PR).
- Improves portability by isolating unstable content to execution layer.
- Enables differentiated validation rules and metrics (e.g., churn tolerance higher in execution).
- Strengthens traceability linking directives back to architectural intent.

## Options Considered

| Option                     | Description                             | Pros                       | Cons                                       | Reason Rejected         |
|----------------------------|-----------------------------------------|----------------------------|--------------------------------------------|-------------------------|
| Flat model (status quo)    | Keep current mixed directory            | Zero migration cost        | Drift, unclear authority, weak portability | Fails scaling needs     |
| Two-layer model            | Combine operational + execution         | Simpler taxonomy           | Blurs procedure vs directive               | Insufficient separation |
| Tag-only approach          | Add metadata tags without restructuring | Minimal restructure        | Harder discoverability; tag misuse risk    | Lower clarity           |
| Three-layer model (chosen) | Distinct partitions + metadata          | High clarity, traceability | Migration effort                           | Balanced trade-offs     |
| Domain-based segmentation  | Split by agent domains                  | Domain focus               | Fragmented governance                      | Doesn’t solve coupling  |

## Implications

- Requires repository restructuring (see ADR-004).
- Validation scripts must inspect layer metadata.
- Onboarding documentation updated to include layer overview.
- Strategic changes require ADR + version bump.
- Portability mapping performed per layer; strategic artifacts default to stable.

## Trade-Off Analysis

- Time-to-adoption vs governance rigor: Some short-term slowdown offsets long-term clarity.
- Overhead vs scalability: Introduces structured overhead now to reduce ad hoc coordination later.
- Flexibility vs stability: Constrains high-level shifts, while preserving agility in execution layer.
- Tooling complexity vs manual process reliability: Prefer automated validation to reduce manual errors.

## Risks

Key high-risk items: over-segmentation and metadata fatigue. Mitigated by phased rollout and generator tooling.

## Decision Matrix (Abbreviated)

| Criterion           | Weight | Three-Layer | Tag-Only          | Flat |
|---------------------|--------|-------------|-------------------|------|
| Scalability         | High   | Strong      | Medium            | Low  |
| Traceability        | High   | Strong      | Medium            | Low  |
| Migration Cost      | Medium | Higher      | Low               | None |
| Portability Support | High   | Strong      | Weak              | Weak |
| Cognitive Load      | Medium | Moderate    | Higher (implicit) | Low  |

## Implementation Outline
## Implementation Outline
1. ADR-003 approved; ADR-004 (physical restructuring) rejected.
2. Create `agents/approaches/` directory for operational layer processes/algorithms.
3. Add metadata headers to existing artifacts (in-place).
4. Extend validation scripts to enforce layer-specific rules via metadata.
5. Update AGENTS.md and architecture README with layer mapping.
6. Create layer classification index (logical, not physical).
7. Review after initial 2-week pilot.

## Success Metrics

- 100% artifacts tagged with layer metadata.
- Reduced average review time for strategic changes (after initial adoption).
- Portability alignment (execution directives exported via whitelist).
- Churn metrics show >70% of changes confined to execution layer.

## Open Questions

See assessment; to be resolved prior to Phase 2.

## Alternatives for Future Revisit

Potential evolution to include a fourth layer (Experimental) if execution churn becomes disruptive.

## Status Change Protocol

Status: Accepted on 2025-11-22. Implementation proceeds with existing repository structure (ADR-004 rejected due to high impact and limited benefits relative to quickstart goals).

## References

- [ADR-001](./ADR-001-modular-agent-directive-system.md), [ADR-002](./ADR-002-portability-enhancement-opencode.md)
- [ADR-004](./ADR-004-repository-restructuring-layer-separation.md) (Rejected - physical restructuring)
- [`directive_system_architecture.md`](../design/directive_system_architecture.md)
- [`architectural_vision.md`](../architectural_vision.md)

