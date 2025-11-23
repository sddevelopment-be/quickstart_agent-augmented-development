# Curator Note: Guidance for Revising `agents` Directory under Three-Layer Model

Date: 2025-11-22  
Role: Curator Claire  
Related: ADR-003 (Proposed), ADR-004 (Proposed), ADR-001, ADR-002

## Purpose

Provide actionable guidance for separating guidelines and directives, establishing index structures, maintaining version governance continuity, and defining validation protocol adjustments. This is instructive only—no implementation performed here.

## 1. Classification Principles

| Artifact Type                  | Current Location                                 | Target Layer                                  | Notes                                                          |
|--------------------------------|--------------------------------------------------|-----------------------------------------------|----------------------------------------------------------------|
| Agent Profiles (`*.agent.md`)  | `agents/`                                        | Execution                                     | Profile definitions are runtime-facing capability descriptors. |
| Directives (`directives/*.md`) | `agents/directives/`                             | Execution                                     | Low-level instructions referenced by agents.                   |
| Guidelines (`guidelines/*.md`) | `agents/guidelines/`                             | Operational                                   | Process / behavioral standards.                                |
| Bootstrap / Rehydration docs   | `agents/guidelines/rehydrate.md`, `bootstrap.md` | Operational                                   | Lifecycle procedural references.                               |
| Role capability manifests      | In profiles & directives                         | Operational (template) + Execution (instance) | Split templates vs active profiles.                            |
| Architecture vision / ADRs     | `docs/architecture/`                             | Strategic                                     | High-level persistent intent.                                  |

## 2. Extraction Plan (Guidelines vs Directives)

1. Enumerate all files under `agents/`.
2. Tag each as directive, guideline, profile, template, or mixed.
3. For mixed files: extract directive-specific sections into new execution-layer files; leave procedural context in operational layer.
4. Insert metadata header into each newly separated file.

## 3. Index Creation

Create machine-readable index: `agents/index.json`.
Schema (draft):

```json
{
  "generated_at": "ISO-8601",
  "artifacts": [
	{
	  "path": "agents/directives/validate_directives.md",
	  "layer": "execution",
	  "type": "directive",
	  "version": "1.0.0",
	  "status": "active",
	  "portability": "internal",
	  "related_adrs": [
		"ADR-001"
	  ]
	}
  ]
}
```

Companion human-readable index: `directives/README.md`, `guidelines/README.md`, `approaches/README.md`  includes layer overview and change workflow summary.

Main `agents/README.md` file informs about Three-Layer Model and points to aforementioned indices and architecture docs. ( This should be a very brief overview, not a full explanation. )

## 4. Version Governance Continuity

- Strategic layer artifacts adopt semantic version (MAJOR.MINOR).
- Operational guidelines date-versioned (YYYY-MM-DD + optional patch).
- Execution directives optionally patch-only (e.g., 0.0.X) unless externally exposed.
- Maintain ledger: `docs/architecture/version-ledger.md` referencing ADR deltas.

## 5. Validation Protocol Adjustments

Extend existing `validate_directives.sh` to:

- Check presence & correctness of metadata headers.
- Enforce allowed transitions (e.g., draft → active requires review label).
- Fail if strategic artifact modified without commit message containing `[ADR-XXX]`.
- Optionally generate diff summary of layer churn metrics.

## 6. Portability Alignment

- Tag execution directives with portability classification (`stable|guarded|internal`).
- Curator maintains mapping file: `architecture/design/portability-map.json`.
- Guarded artifacts require explicit export justification.

## 7. Governance Workflow Summary

| Layer       | Change Trigger  | Required Artifact | Review Gate         |
|-------------|-----------------|-------------------|---------------------|
| Strategic   | Vision shift    | ADR               | Architect + Curator |
| Operational | New pattern     | Guideline PR      | Curator             |
| Execution   | Directive tweak | Standard PR       | Maintainers         |

## 8. Quality Assurance Suggestions

- Weekly automated index regeneration; diff posted to collaboration channel.
- Broken link scan across moved artifacts.
- Lint rule: metadata header must precede first H1.

## 9. Deferred Considerations

- Auto-generation of curator report
- Integration with external portability validator
- Contributor training module update

## 10. Action Checklist (For Implementation Team)
## 10. Action Checklist (For Implementation Team)
- [ ] Create `agents/approaches/` directory with README
- [ ] Inventory classification complete (in-place)
- [ ] Metadata schema ratified
- [ ] Metadata headers added to existing artifacts
- [ ] Logical layer index (`docs/architecture/layer-index.json`) generated
- [ ] Three-Layer Model overview doc (`docs/architecture/THREE_LAYER_MODEL.md`) created
- [ ] Index generator script stub committed
- [ ] Validation enhancements merged in warn-only mode
- [ ] Update `AGENTS.md` with layer references
- [ ] Transition announcement published

## 11. Open Questions for Curator Review

1. Retention policy for deprecated execution directives?
2. Are internal portability items ever auto-promoted?
3. Should we adopt unified versioning for cross-layer bundles?

## 12. Closing

This note establishes boundaries and expectations. Implementation should proceed only after ADR-003 and ADR-004 acceptance.

