# ADR-008: Repository Restructuring for Layer Separation

> **Date:** 2025-11-22  
> **Status:** REJECTED / adapted  
> **Authors:** Architect Alphonso  
> **Depends On:** [ADR-006](./ADR-006-adopt-three-layer-governance-model.md)  
> **Tags:** restructuring, governance, validation

## Context

ADR-006 introduces a Three-Layer Governance Model. Current repository layout intermixes agent profiles, directives, guidelines, and architectural documents within
`agents/` and `docs/architecture/`. This impedes automated layer-aware validation and creates ambiguity for change approval boundaries.

## Decision

Restructure repository to physically and semantically separate artifacts by governance layer (Rejected in favor of logical metadata classification without physical moves):

Proposed top-level additions (not implemented physically):

```
layers/
  strategic/
    README.md
    vision/
    governance/
    version-ledger.md
  operational/
    README.md
    patterns/
    guidelines/
    templates/
  execution/
    README.md
    directives/
    agent-profiles/
    validation/
index/
  layer-index.json
```

Transitional approach (adapted):

- Maintain legacy paths; introduce metadata headers for logical layer tagging.
- Provide non-destructive classification tooling (report-only).
- Avoid symlink-based compatibility to reduce complexity.

## Rationale

- Physical separation would reduce accidental cross-layer edits but imposes migration friction.
- Logical metadata approach achieves governance clarity with lower disruption (see ADR-006 adoption).
- Enables layer-differentiated CI rules (strategic changes require ADR reference) without directory churn.

## Options Considered

| Option                      | Description                        | Pros                               | Cons                                   |
|-----------------------------|------------------------------------|------------------------------------|----------------------------------------|
| Soft tagging only           | Metadata without directory changes | Lower migration cost               | Persisting ambiguity                   |
| Partial restructuring       | Only split strategic layer         | Less effort                        | Operational-execution coupling remains |
| Full restructuring (proposed) | Separate all three layers        | Clear semantics, robust automation | Highest initial cost                   |
| Monorepo with submodules    | Externalize strategic artifacts    | Strong isolation                   | Complexity, tool friction              |

## Adapted Strategy

1. Inventory classification (build matrix).
2. Add metadata headers in-place.
3. Generate logical `layer-index.json` (report artifact) under `docs/architecture/`.
4. Enhance validation scripts for layer rules.
5. Publish migration guide (logical tagging only).

## Trade-Offs

- Reduced restructuring clarity vs minimized contributor friction.
- Avoids temporary duplication and broken references.
- Leverages existing contributor familiarity with paths.

## Validation & Tooling Changes

- Extend `validate_directives.sh` or create `validate_layers.sh` for metadata checks.
- CI job: fail if strategic artifact changed without ADR reference.

## Risks & Mitigations

| Risk                     | Impact                     | Mitigation                                      |
|--------------------------|----------------------------|-------------------------------------------------|
| Broken references        | Docs linking to old paths  | Use relative links; avoid path churn           |
| Script misclassification | Incorrect layer assignment | Manual review checklist for first run           |
| Contributor pushback     | Slowed contributions       | Publish rationale & quickstart updates          |
| Tooling failure in CI    | Blocked merges             | Staged rollout; warn-only mode first week       |

## Success Metrics

- >95% artifacts correctly tagged within 2 weeks.
- Validation false positive rate <5% after week 2.
- Strategic layer churn <10% of total changes (monthly).
- Reduced review cycle time for execution changes (baseline needed).

## Open Questions

1. Formal time-box for tag adoption audit?
2. Do agent profiles live entirely in execution or partly operational (templates)?
3. Single version ledger or per-layer ledger?

## Implementation Notes

- Classification script spec (future): parse filename, path, header tags; output JSON for index.
- Provide fallback manual override file: `layer-overrides.yaml`.

## Lessons Learned

- Physical restructuring imposes high costs when existing structure is functional and familiar.
- Metadata-driven classification provides sufficient governance without directory churn.
- "Quickstart" positioning requires minimizing structural friction for new contributors.
- Validation and tooling enforcement can operate effectively on logical (metadata) boundaries.

## References

- [ADR-006](./ADR-006-adopt-three-layer-governance-model.md) (layer model) - Approved
- [ADR-001](./ADR-001-modular-agent-directive-system.md) (directive modularity)
- [ADR-007](./ADR-007-portability-enhancement-opencode.md) (portability)
- [`architectural_vision.md`](../architectural_vision.md)

