# Three-Layer Model Assessment

Date: 2025-11-22  
Author: Architect Alphonso  
Related Artifacts: ADR-001, ADR-002, `architectural_vision.md`, `directive_system_architecture.md`, `work/architect/three-layer-idea.md`

## Initialization Declaration

✅ SDD Agent “Architect Alphonso” initialized.  
Context layers: Operational ✓, Strategic ✓, Command ✓, Bootstrap ✓, AGENTS ✓.  
Purpose acknowledged: Clarify complex systems with contextual trade-offs; produce ADRs, decomposition maps, and governance patterns.  
Operating Mode: `/analysis-mode` (architecture exploration & ADR drafting).  
Authority confirmation per Directive 007 (Agent Declaration) complete.

## 1. Executive Summary

The proposed Three-Layer Governance Model introduces a stratified approach for agentic system evolution:

- Strategic Layer: Vision, long-horizon direction, cross-repository principles, version governance.
- Operational Layer: Procedures, guidelines, patterns, reusable templates governing agent behaviors and interactions.
- Execution (Command) Layer: Concrete directives, runtime configurations, validation rules, per-agent capability manifests.

This model responds to growing coupling between agent profiles, directive files, and emerging portability goals (ADR-002). It aims to reduce drift, enable selective portability, and establish clearer authority boundaries for change control.

## 2. Alignment with ADR-001 & ADR-002

| Aspect              | ADR-001 (Modular Directive System)                                             | ADR-002 (Portability Enhancement)                                                | Three-Layer Model Contribution                                                             |
|---------------------|--------------------------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Modularity          | Reinforces modular directive grouping by scoping directives to Execution layer | Enables layer-aware exports for external systems                                 | Adds governance rules for modular extension                                                |
| Portability         | N/A baseline; modularity precondition                                          | Introduces portability surfaces; requires separation of stable vs mutable assets | Distinguishes strategic (stable), operational (moderately variant), execution (high churn) |
| Versioning          | Initial directive versioning implicit                                          | Requires consistent semantic alignment across repos                              | Introduces explicit version domains per layer                                              |
| Change Control      | Currently flat; ad hoc updates                                                 | Needs predictable compatibility envelope                                         | Defines escalation paths and approval gates                                                |
| Semantic Drift Risk | Rising complexity                                                              | Risk of misaligned external embedding                                            | Layer segmentation reduces drift vectors                                                   |

## 3. Gap Analysis

| Current State                                                   | Gap                                     | Impact                                     | Recommended Closure                 |
|-----------------------------------------------------------------|-----------------------------------------|--------------------------------------------|-------------------------------------|
| Mixed artifacts in `agents/` (profiles, directives, guidelines) | No enforced layer boundary              | Inconsistent updates; review fatigue       | Restructure directories (ADR-004)   |
| Single validation script (`validate_directives.sh`)             | Lacks layer-specific rules              | False positives / missed governance errors | Extend validation with layer schema |
| No explicit version blocks per artifact                         | Hard to audit compatibility             | Untracked breaking changes                 | Introduce header metadata per layer |
| Portable spec (OpenCode) loosely referenced                     | Missing binding to ADR-002 upgrade path | Portability friction                       | Add compatibility matrices          |
| Limited escalation protocol clarity                             | Unclear authority for strategic shifts  | Risk of unauthorized directional changes   | Formalize strategic change workflow |
| Agent specialization patterns partially documented              | Incomplete cross-links                  | Knowledge silos                            | Auto-generate layer indexes         |

## 4. Migration & Repository Adjustment Plan (Phased)

### Phase 0 – Preparation (1–2 days)

- Catalog all files under `agents/` by type: profile, directive, guideline, template.
- Define layer classification matrix (artifact type → layer).
- Draft metadata header spec (Status, Layer, Version, Owner, Review Cycle).

### Phase 1 – Structural Refactor (2–3 days)

- Create new top-level directories (proposed):
    - `layers/strategic/`
    - `layers/operational/`
    - `layers/execution/`
- Move or symlink (initially prefer copy + diff) artifacts into layer dirs.
- Add README per layer describing scope, change frequency, governance gates.

### Phase 2 – Metadata & Validation (2–3 days)

- Inject metadata headers into moved files.
- Extend validation script: enforce presence + correctness of layer metadata.
- Add a version ledger file: `layers/version-governance.md`.

### Phase 3 – Index & Cross-Link (1–2 days)

- Generate machine-readable index: `layers/index.json` (artifact → layer → version).
- Cross-link ADRs to layer READMEs.
- Update `AGENTS.md` to reference layer separation.

### Phase 4 – Portability Integration (2 days)

- Tag strategic artifacts with portability stability level (e.g., STABLE, GUARDED).
- Map operational patterns to portability guidelines per ADR-002.
- Provide export spec: which execution directives are externally consumable.

### Phase 5 – Optimization & Hardening (ongoing)

- Introduce automated review gate: strategic changes require ADR + version bump.
- Publish a change calendar; define review cadence (monthly strategic audit).
- Monitor churn metrics per layer (files changed / interval).

## 5. Risks & Mitigations

| Risk                      | Description                            | Layer(s) Affected      | Mitigation                                                           |
|---------------------------|----------------------------------------|------------------------|----------------------------------------------------------------------|
| Over-segmentation         | Tooling overhead, slower iteration     | Operational, Execution | Keep initial move lightweight (copy first); defer strict enforcement |
| Incomplete classification | Misplaced artifacts cause confusion    | All                    | Run classification workshop; maintain provisional tag list           |
| Metadata fatigue          | Manual maintenance friction            | Execution              | Provide generator script to apply headers                            |
| Portability mis-scope     | Exposing unstable execution directives | Execution              | Add stability labels + explicit export whitelist                     |
| Governance rigidity       | Blocked innovation                     | Strategic              | Include exception fast-track with curator approval                   |
| Validation complexity     | Increased false failures               | All                    | Incrementally phase rules; maintain compatibility mode               |
| Knowledge drift           | Contributors ignore new structure      | Operational            | Layer orientation guide + onboarding update                          |

## 6. Open Questions

1. Should strategic documents adopt semantic versioning independent of repository version?
2. How are deprecated execution directives tracked—tombstone file or index flag?
3. Is portability stability determined by usage metrics or manual designation?
4. Should curator role own cross-layer reconciliation or only strategic sign-off?
5. Are external consumers permitted to propose changes directly to operational layer?
6. Will CI enforce layer integrity (e.g., blocking strategic edits without ADR reference)?
7. What is the minimum metadata set for agent profile files post-migration?

## 7. Recommendation (Original)
Proceed with ADR-003 (adopt model) and ADR-004 (repository restructuring) in tandem, with a controlled Phase 1 pilot restricted to directives and guidelines before expanding to all profiles.

## 8. Decision Summary (Updated 2025-11-22)

### Outcomes
- **ADR-003**: ✅ **Accepted** on 2025-11-22
- **ADR-004**: ❌ **Rejected** on 2025-11-22

### Rejection Rationale (ADR-004)
Physical directory restructuring was rejected due to:
1. High structural impact on existing tooling and documentation
2. Limited pragmatic benefits compared to metadata-driven approach
3. Significant tooling integration costs defeating "quickstart" repository positioning
4. Complexity overhead from migration phases, symlinks, and compatibility shims

### Implementation Approach (Approved)
Three-Layer Governance Model will be implemented **in-place** using existing repository structure:

**Strategic Layer**: `docs/architecture/`
- Vision documents, ADRs, architectural patterns
- Semantic versioning (MAJOR.MINOR.PATCH)

**Operational Layer**: `agents/guidelines/` and `agents/approaches/` (**NEW**)
- Guidelines, bootstrap/rehydration procedures
- Operational processes and algorithms (new `approaches/` directory)
- Date-based versioning (YYYY-MM-DD)

**Execution Layer**: `agents/directives/` and `agents/*.agent.md`
- Directives and agent profiles
- Patch versioning (0.0.X)

**Classification mechanism**: Metadata headers added to artifacts in-place; logical layer index generated without physical file moves.

## 9. Next Steps
1. ✅ ADR-003 approved; ADR-004 rejected and documented
2. Create `agents/approaches/` directory with README
3. Define and ratify metadata header schema
4. Add metadata headers to existing artifacts (strategic → operational → execution)
5. Generate logical layer index: `docs/architecture/layer-index.json`
6. Create Three-Layer Model overview: `docs/architecture/THREE_LAYER_MODEL.md`
7. Extend validation scripts with layer-aware rules
8. Update `AGENTS.md` with layer references
9. See detailed implementation plan: `work/collaboration/curator/curator_claire_three-layer-implementation-note.md`
