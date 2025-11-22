# ADR-004: Repository Restructuring for Layer Separation

> **Date:** 2025-11-22  
> **Status:** REJECTED / adapted  
> **Authors:** Architect Alphonso  
> **Depends On:** [ADR-003](./ADR-003-adopt-three-layer-governance-model.md)  
> **Tags:** restructuring, governance, validation

## Context

ADR-003 introduces a Three-Layer Governance Model. Current repository layout intermixes agent profiles, directives, guidelines, and architectural documents within
`agents/` and `docs/architecture/`. This impedes automated layer-aware validation and creates ambiguity for change approval boundaries.

## Decision

Restructure repository to physically and semantically separate artifacts by governance layer:

Proposed top-level additions:

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

Transitional approach:

- Maintain legacy paths during migration with deprecation notices.
- Provide an automated script to classify and move artifacts (non-destructive first pass).
- Introduce a compatibility shim: symlinks from old to new paths for external tools (time-boxed).

## Rationale

- Physical separation reduces accidental cross-layer edits.
- Enables layer-differentiated CI rules (e.g., strategic requires ADR reference).
- Facilitates creation of layer-specific onboarding and indexes.
- Minimizes incidental coupling flagged in ADR-001 review notes.

## Options Considered

| Option                      | Description                        | Pros                               | Cons                                   |
|-----------------------------|------------------------------------|------------------------------------|----------------------------------------|
| Soft tagging only           | Metadata without directory changes | Lower migration cost               | Persisting ambiguity                   |
| Partial restructuring       | Only split strategic layer         | Less effort                        | Operational-execution coupling remains |
| Full restructuring (chosen) | Separate all three layers          | Clear semantics, robust automation | Highest initial cost                   |
| Monorepo with submodules    | Externalize strategic artifacts    | Strong isolation                   | Complexity, tool friction              |

## Migration Strategy

Refer to assessment phases; summarized:

1. Inventory classification (build matrix).
2. Create `layers/` directories + READMEs.
3. Copy then diff (avoid destructive move).
4. Add metadata headers.
5. Generate `layer-index.json`.
6. Introduce validation enhancements.
7. Remove deprecated originals after grace period (e.g., 30 days).

## Trade-Offs

- Increased initial overhead vs long-term clarity.
- Potential contributor confusion mitigated by robust READMEs.
- Temporary duplication risk controlled by automated diff checks.

## Validation & Tooling Changes

- Extend `validate_directives.sh` or create `validate_layers.sh`.
- Checks: presence of metadata header, allowed layer → artifact type mapping, ACL for strategic changes (must cite ADR).
- Add CI job: fail if strategic artifact changed without ADR reference in commit message.

## Risks & Mitigations

| Risk                     | Impact                     | Mitigation                                      |
|--------------------------|----------------------------|-------------------------------------------------|
| Broken references        | Docs linking to old paths  | Provide redirect map + search script            |
| Script misclassification | Incorrect layer assignment | Manual review checklist for first run           |
| Contributor pushback     | Slowed contributions       | Publish migration guide & rationale (link ADRs) |
| Tooling failure in CI    | Blocked merges             | Staged rollout; warn-only mode first week       |

## Success Metrics

- \> 95% artifacts correctly layered within 2 weeks.
- Validation false positive rate <5% after week 2.
- Strategic layer churn <10% of total changes (monthly).
- Reduced review cycle time for execution changes (baseline needed).

## Open Questions

1. Time-box for symlink compatibility?
2. Do agent profiles live entirely in execution or partly operational (templates)?
3. Should we maintain a single version ledger or per-layer ledger?

## Implementation Notes

- Classification script spec (future): parse filename, path, header tags; output JSON for index.
- Provide fallback manual override file: `layers/overrides.yaml`.

## Lessons Learned

- Physical restructuring imposes high costs when existing structure is functional and familiar.
- Metadata-driven classification provides sufficient governance without directory churn.
- "Quickstart" positioning requires minimizing structural friction for new contributors.
- Validation and tooling enforcement can operate effectively on logical (metadata) boundaries.

## References

- [ADR-003](./ADR-003-adopt-three-layer-governance-model.md) (layer model) - Approved with in-place implementation
- [ADR-001](./ADR-001-modular-agent-directive-system.md) (directive modularity)
- [ADR-002](./ADR-002-portability-enhancement-opencode.md) (portability)
- [`architectural_vision.md`](../architectural_vision.md)

