# Curator Note: Implementing Three-Layer Model (In-Place)

> **Date:** 2025-11-22  
> **Updated:** 2025-11-22  
> **Role:** Curator Claire  
> **Related:
** [ADR-003](/docs/architecture/adrs/ADR-003-adopt-three-layer-governance-model.md) (Accepted), [ADR-004](/docs/architecture/adrs/ADR-004-repository-restructuring-layer-separation.md) (Rejected), [ADR-001](/docs/architecture/adrs/ADR-001-modular-agent-directive-system.md), [ADR-002](/docs/architecture/adrs/ADR-002-portability-enhancement-opencode.md)

## Decision Summary

- [**ADR-003**](/docs/architecture/adrs/ADR-003-adopt-three-layer-governance-model.md): ✅ Approved - Three-Layer Governance Model adopted
- [**ADR-004
  **](/docs/architecture/adrs/ADR-004-repository-restructuring-layer-separation.md): ❌ Rejected - Physical restructuring rejected due to high impact, limited benefits, tooling costs
- **Implementation approach**: In-place using existing directory structure with metadata-driven classification

## Purpose

Provide actionable guidance for implementing the Three-Layer Governance Model within the existing repository structure. Focus on:

- Creating `agents/approaches/` directory for operational processes/algorithms
- Adding metadata headers to existing artifacts (in-place)
- Establishing logical layer indexes
- Maintaining version governance continuity
- Defining validation protocol adjustments

This is instructive only—no implementation performed by architect role.

---

## 1. Repository Structure (Existing - No Changes)

### Strategic Layer

**Location**: `docs/architecture/`

- Vision documents
- ADRs (Architecture Decision Records)
- Architectural patterns
- High-level persistent intent

### Operational Layer

**Location**: `agents/guidelines/` and `agents/approaches/` (NEW)

- Process and behavioral standards (`guidelines/`)
- Operational algorithms and approaches (`approaches/` - **TO BE CREATED**)
- Reusable templates and patterns
- Bootstrap and rehydration procedures

### Execution Layer

**Location**: `agents/directives/` and `agents/*.agent.md`

- Concrete directives (numbered `001_*.md` through `0XX_*.md`)
- Agent profile definitions (`*.agent.md`)
- Runtime-facing capability descriptors
- Validation rules

---

## 2. Classification Principles (In-Place)

| Artifact Type                   | Current Location              | Layer       | Action Required               |
|---------------------------------|-------------------------------|-------------|-------------------------------|
| Agent Profiles (`*.agent.md`)   | `agents/`                     | Execution   | Add metadata header in-place  |
| Directives (`0XX_*.md`)         | `agents/directives/`          | Execution   | Add metadata header in-place  |
| Guidelines                      | `agents/guidelines/`          | Operational | Add metadata header in-place  |
| **Approaches/Algorithms** (NEW) | `agents/approaches/`          | Operational | **Create directory + README** |
| Architecture vision / ADRs      | `docs/architecture/`          | Strategic   | Add metadata header in-place  |
| Patterns                        | `docs/architecture/patterns/` | Strategic   | Add metadata header in-place  |

---

## 3. Implementation Tasks

### Task 1: Create `agents/approaches/` Directory

**Purpose**: House operational-layer processes, algorithms, and approaches that agents reference.

**Action**:

1. Create directory: `agents/approaches/`
2. Create README explaining purpose, examples, and how to reference from agent profiles
3. Example content to migrate/create:
    - `lexical-pass.md` - Operational algorithm for lexical editing
    - `architecture-note.md` - Approach for creating architecture documentation
    - `pattern-entry.md` - Process for creating pattern library entries

### Task 2: Define Metadata Header Schema

**Required fields**:

```yaml
---
layer: strategic|operational|execution
version: <semantic or date-based>
status: active|deprecated|draft
owner: <role/persona>
review_cycle: <interval or event>
related_adrs: [ ADR-001, ADR-002, ... ]
portability: stable|guarded|internal
---
```

**Versioning conventions**:

- Strategic: Semantic versioning (MAJOR.MINOR.PATCH)
- Operational: Date-based (YYYY-MM-DD) + optional patch
- Execution: Patch-only (0.0.X) unless externally exposed

### Task 3: Add Metadata Headers to Existing Artifacts

**In-place additions** - no file moves required.

**Priority order**:

1. Strategic artifacts (`docs/architecture/*.md`)
2. Agent profiles (`agents/*.agent.md`)
3. Directives (`agents/directives/*.md`)
4. Guidelines (`agents/guidelines/*.md`)

### Task 4: Create Logical Layer Index

**File**: `docs/architecture/layer-index.json`

**Schema**:

```json
{
  "generated_at": "2025-11-22T00:00:00Z",
  "repository": "quickstart_agent-augmented-development",
  "artifacts": [
	{
	  "path": "agents/directives/001_cli_shell_tooling.md",
	  "layer": "execution",
	  "type": "directive",
	  "version": "1.0.0",
	  "status": "active",
	  "portability": "internal",
	  "related_adrs": [
		"ADR-001"
	  ]
	},
	{
	  "path": "agents/approaches/lexical-pass.md",
	  "layer": "operational",
	  "type": "approach",
	  "version": "2025-11-22",
	  "status": "active",
	  "portability": "stable",
	  "related_adrs": [
		"ADR-003"
	  ]
	},
	{
	  "path": "docs/architecture/adrs/ADR-003-adopt-three-layer-governance-model.md",
	  "layer": "strategic",
	  "type": "adr",
	  "version": "1.0.0",
	  "status": "accepted",
	  "portability": "stable",
	  "related_adrs": []
	}
  ]
}
```

### Task 5: Create Three-Layer Model Overview

**File**: `docs/architecture/THREE_LAYER_MODEL.md`

**Contents**:

- Layer definitions and boundaries
- Directory mapping (strategic → operational → execution)
- Change workflow per layer
- Metadata schema reference
- Examples of artifact classification
- Governance rules (ADR required for strategic changes, etc.)

### Task 6: Specifications for Validation Scripts

**Goal:
** Create outline and base rules for validation scripts to enforce layer-specific governance, and content structure. The scripts will be written by
`Devops Danny` or `Backend Benny`. Your role is to define the requirements into a clear specification.

**File**: `validation_specifications.md` in the relevant specialist `work` directory.

**Proposed Checks**:

- Presence and correctness of metadata headers
- Layer-appropriate artifact types (e.g., ADRs must be in strategic layer)
- Version format compliance per layer
- Portability classification validity
- Strategic changes require ADR reference in commit message
- Cross-reference validation (related_adrs point to existing ADRs)

### Task 7: Update `AGENTS.md`

Add section referencing Three-Layer Model:

- Link to `docs/architecture/THREE_LAYER_MODEL.md`
- Brief explanation of layer boundaries
- Note on metadata requirements for new artifacts

---

## 4. Version Governance

| Layer       | Location                                   | Version Format               | Example      | Update Trigger                   |
|-------------|--------------------------------------------|------------------------------|--------------|----------------------------------|
| Strategic   | `docs/architecture/`                       | Semantic (MAJOR.MINOR.PATCH) | `1.2.0`      | ADR approval, major vision shift |
| Operational | `agents/guidelines/`, `agents/approaches/` | Date-based (YYYY-MM-DD)      | `2025-11-22` | New pattern, process refinement  |
| Execution   | `agents/directives/`, `agents/*.agent.md`  | Patch (0.0.X)                | `0.0.12`     | Directive tweak, profile update  |

**Version ledger**: `docs/architecture/version-ledger.md` tracking layer versions and ADR linkage.

---

## 5. Portability Alignment

**Mapping file**: `docs/architecture/portability-map.json`

**Classification**:

- `stable`: Externally portable, stable interface (default for strategic/operational)
- `guarded`: Conditionally portable, requires justification
- `internal`: Repository-specific, not portable (default for execution)

**Curator responsibilities**:

- Maintain portability-map.json
- Review export requests for guarded artifacts
- Ensure strategic artifacts default to stable

---

## 6. Governance Workflow

| Layer       | Change Trigger                   | Required Artifact     | Review Gate         | Validation                |
|-------------|----------------------------------|-----------------------|---------------------|---------------------------|
| Strategic   | Vision shift, major direction    | ADR                   | Architect + Curator | Commit must reference ADR |
| Operational | New pattern, approach, guideline | Guideline/Approach PR | Curator             | Standard review           |
| Execution   | Directive tweak, profile update  | Standard PR           | Maintainers         | Automated checks          |

---

## 7. Quality Assurance

### Automated Checks

- Weekly regeneration of `layer-index.json` with diff report
- Broken link scanning across artifacts
- Metadata header linting (must precede first H1)
- Layer-boundary violation detection

### Manual Reviews

- Quarterly strategic layer audit
- Monthly operational layer consistency check
- Portability classification review

---

## 8. Action Checklist

- [ ] **Create `agents/approaches/` directory with README**
- [ ] Inventory all existing artifacts by layer assignment
- [ ] Ratify metadata schema
- [ ] Add metadata headers to strategic artifacts
- [ ] Add metadata headers to operational artifacts
- [ ] Add metadata headers to execution artifacts
- [ ] Generate initial `layer-index.json`
- [ ] Create `THREE_LAYER_MODEL.md` overview
- [ ] Create `version-ledger.md`
- [ ] Create `portability-map.json`
- [ ] Implement/extend validation scripts
- [ ] Update `AGENTS.md` with layer references
- [ ] Run validation in warn-only mode for 1 week
- [ ] Enable enforcement mode
- [ ] Publish transition announcement

---

## 9. Open Questions

1. Should we auto-generate metadata headers via script, or add manually?
> A: manual addition at first, inclusion in templates. Scripting left for future consideration, no immediate need.

2. What is the retention policy for deprecated execution directives?
> A: archive to `agents/deprecated/` after 90 days of deprecation status.

3. Are internal portability items ever auto-promoted to guarded/stable?
> A: only via explicit review and justification by human curator.

4. Should we adopt unified versioning for cross-layer bundles?
> A: no, maintain layer-specific versioning to preserve clarity.

5. How do we handle artifacts that span multiple layers?
> A: classify by primary function; add cross-reference metadata to indicate multi-layer relevance. Exceptions handled case-by-case, or moved to  `docs/architecture` as strategic reference artifacts.

---

## 10. Migration Timeline

**Week 1**: Setup

- Create `agents/approaches/` directory
- Ratify metadata schema
- Create overview documentation

**Week 2**: Metadata Addition

- Add headers to strategic artifacts
- Add headers to operational artifacts
- Generate initial layer-index.json

**Week 3**: Validation

- Add headers to execution artifacts
- Implement validation scripts (warn-only)
- Monitor false positives

**Week 4**: Enforcement

- Enable validation enforcement
- Publish transition guide
- Hold team retrospective

---

## 11. Success Metrics

- [ ] 100% artifacts tagged with layer metadata within 3 weeks
- [ ] `agents/approaches/` populated with initial operational processes
- [ ] Validation false positive rate <5% by week 4
- [ ] Strategic layer churn <10% of total changes (monthly baseline)
- [ ] Layer-index.json successfully generated and validated
- [ ] Zero broken cross-references after migration

---

## 12. Closing

**Status**: ADR-003 approved; ADR-004 rejected.

**Implementation approach**: In-place metadata-driven classification using existing directory structure.

**Key focus areas**:

1. Create `agents/approaches/` for operational layer
2. Add metadata headers to all artifacts
3. Build logical indexes (no physical moves)
4. Extend validation with layer-aware rules

**Authority
**: Curator Claire owns implementation execution and validation protocol. Architect Alphonso provides governance oversight and ADR updates.

**Next step**: Begin Task 1 (create `agents/approaches/` directory).

