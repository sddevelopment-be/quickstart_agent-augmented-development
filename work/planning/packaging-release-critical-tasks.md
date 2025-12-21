# Packaging and Release Initiative - Critical Task Identification

**Planning Agent:** Planning Petra  
**Date:** 2025-12-21  
**Context:** Advancement of framework packaging and release functionality

---

## Executive Summary

Based on analysis of the current repository state, architectural decisions (ADR-013, ADR-014), and technical design documents, I have identified **5 critical tasks** to advance the packaging and release initiative from architectural specification to minimal viable implementation.

**Current State:**
- ✅ Architecture foundation complete (ADRs accepted, design docs written)
- ✅ Templates exist for manifest, audit reports, and upgrade plans
- ❗ No implementation artifacts yet (scripts, agent profiles, workflows)

**Strategic Goal:**
Enable downstream repositories to adopt and upgrade the framework through predictable distribution packages that preserve local intent.

---

## Critical Tasks (Prioritized)

### 1. Framework Installation Script ⚠️ CRITICAL + HIGH URGENCY

**Task ID:** `2025-12-21T0720-build-automation-framework-install-script`  
**Agent:** build-automation (DevOps Danny)  
**Priority:** Critical | **Urgency:** High

**Scope:**
Create POSIX-compliant `framework_install.sh` script for first-time framework installations.

**Deliverables:**
- `ops/scripts/framework_install.sh` (POSIX shell script)
- `ops/scripts/tests/test_framework_install.sh` (test suite)
- `docs/HOW_TO_USE/framework-installation.md` (usage guide)

**Key Requirements:**
- POSIX compliance (no Bash-specific features)
- Copy files from `framework_core/` only when absent
- Never overwrite existing files
- Generate `.framework_meta.yml` with version tracking
- Support `--dry-run` mode
- Structured output for Framework Guardian consumption

**Dependencies:** None (foundational)

**Complexity:** Medium-High | **Duration:** 1-2 days | **Risk:** Medium

**Rationale:**
This is the **foundational script** for the entire distribution model. Without it, downstream repositories cannot adopt the framework. All other components (upgrade script, Guardian agent) depend on the metadata and structure this script establishes.

**Blocks:**
- Upgrade script (requires `.framework_meta.yml` format)
- Guardian agent (requires known metadata structure)
- Integration testing of complete workflow

---

### 2. Framework Upgrade Script ⚠️ CRITICAL + HIGH URGENCY

**Task ID:** `2025-12-21T0721-build-automation-framework-upgrade-script`  
**Agent:** build-automation (DevOps Danny)  
**Priority:** Critical | **Urgency:** High

**Scope:**
Create POSIX-compliant `framework_upgrade.sh` script for safe framework upgrades with conflict detection.

**Deliverables:**
- `ops/scripts/framework_upgrade.sh` (POSIX shell script)
- `ops/scripts/tests/test_framework_upgrade.sh` (test suite)
- `docs/HOW_TO_USE/framework-upgrade.md` (usage guide)

**Key Requirements:**
- Compare files: NEW / UNCHANGED / CONFLICT detection
- Create `.framework-new` files for conflicts (never overwrite)
- Never touch `local/` directory
- Generate `upgrade-report.txt` for Guardian parsing
- SHA256 checksum calculation for conflict detection
- Support `--dry-run` mode

**Dependencies:**
- ✅ Must follow `2025-12-21T0720-build-automation-framework-install-script`
- Requires `.framework_meta.yml` format (from install script)

**Complexity:** High | **Duration:** 2-3 days | **Risk:** Medium-High

**Rationale:**
This script enables **safe, repeatable upgrades** without destroying local customizations. It's the core mechanism that makes the distribution model viable for production use. Without it, the promise of "never silently overwrite modifications" cannot be fulfilled.

**Blocks:**
- Framework Guardian implementation (consumes upgrade-report.txt)
- User acceptance testing of upgrade workflow
- Documentation of upgrade conflict resolution patterns

---

### 3. Framework Guardian Agent Profile ⚠️ CRITICAL + HIGH URGENCY

**Task ID:** `2025-12-21T0722-architect-framework-guardian-agent-profile`  
**Agent:** architect (Alphonso)  
**Priority:** Critical | **Urgency:** High

**Scope:**
Create the Framework Guardian agent profile specification as defined in ADR-014.

**Deliverables:**
- `.github/agents/framework-guardian.agent.md` (agent profile)
- `docs/HOW_TO_USE/framework-guardian-usage.md` (usage guide)
- `work/assigned/framework-guardian/.gitkeep` (agent queue)

**Key Requirements:**
- Define two operating modes: Audit and Upgrade
- Specify inputs: MANIFEST.yml, .framework_meta.yml, upgrade-report.txt, .framework-new files
- Specify outputs: FRAMEWORK_AUDIT_REPORT.md, FRAMEWORK_UPGRADE_PLAN.md
- Define conflict classification taxonomy
- Document guardrails: never auto-overwrite, preserve local intent
- Include directive references and collaboration contract

**Dependencies:**
- Conceptually independent (defines interface contracts)
- Requires understanding of install/upgrade script outputs
- Templates already exist (framework-audit-report-template.md, framework-upgrade-plan-template.md)

**Complexity:** Medium | **Duration:** 1 day | **Risk:** Low-Medium

**Rationale:**
The Framework Guardian is the **human-facing layer** that makes the distribution system usable. Without it, users are left with raw `.framework-new` files and no guidance. This profile can be drafted **in parallel** with script development, enabling early validation of the audit/upgrade workflow design.

**Blocks:**
- Human-readable audit and upgrade planning
- Documentation of conflict resolution strategies
- Training/onboarding materials for framework adoption

---

### 4. Populated Framework MANIFEST.yml 📌 HIGH + HIGH URGENCY

**Task ID:** `2025-12-21T0723-build-automation-populate-framework-manifest`  
**Agent:** build-automation (DevOps Danny)  
**Priority:** High | **Urgency:** High

**Scope:**
Generate operational MANIFEST.yml by scanning repository structure and populating the template with actual paths, checksums, and metadata.

**Deliverables:**
- `META/MANIFEST.yml` (populated manifest)
- `ops/scripts/generate_manifest.sh` (generation script)
- `ops/scripts/tests/test_manifest_generation.sh` (test suite)
- `docs/HOW_TO_USE/manifest-maintenance.md` (maintenance guide)

**Key Requirements:**
- Scan framework-managed directories (.github/agents, docs/templates, docs/directives, validation)
- Calculate SHA256 checksums for each file
- Assign appropriate modes (sync-always, copy-once, reference-only)
- Generate complete MANIFEST.yml following template schema
- Create idempotent maintenance script
- Support `--dry-run` and `--output` options

**Dependencies:**
- Template exists: `docs/templates/automation/framework-manifest-template.yml`
- Should align with paths used in install/upgrade scripts

**Complexity:** Medium | **Duration:** 1-2 days | **Risk:** Medium

**Rationale:**
Both install/upgrade scripts and Framework Guardian **require a populated manifest** to function. Without it, there's no source of truth for "what belongs to the framework." This blocks testing of the entire integration workflow.

**Blocks:**
- Testing of install/upgrade scripts with real manifest
- Framework Guardian audit mode implementation
- Release packaging (manifest must be included in zip)

---

### 5. Packaging & Release Workflow 📌 HIGH + NORMAL URGENCY

**Task ID:** `2025-12-21T0724-build-automation-packaging-release-workflow`  
**Agent:** build-automation (DevOps Danny)  
**Priority:** High | **Urgency:** Normal

**Scope:**
Create GitHub Actions workflow that packages the framework as quickstart-framework-<version>.zip and publishes as GitHub Release.

**Deliverables:**
- `.github/workflows/framework-release.yml` (GitHub Actions workflow)
- `ops/scripts/assemble_framework_package.sh` (packaging script)
- `ops/scripts/generate_release_notes.sh` (release notes generator)
- `docs/HOW_TO_USE/creating-framework-releases.md` (maintainer guide)
- `META/.gitkeep` (directory structure)

**Key Requirements:**
- Trigger on version tags (v*.*.*)or manual dispatch
- Assemble framework_core/, scripts/, META/ directories
- Create zip archive with deterministic structure
- Calculate SHA256 checksum
- Publish as GitHub Release with attached artifacts
- Generate release notes from ADRs and CHANGELOG

**Dependencies:**
- ✅ Must follow `2025-12-21T0720-build-automation-framework-install-script` (script to package)
- ✅ Must follow `2025-12-21T0721-build-automation-framework-upgrade-script` (script to package)
- ✅ Must follow `2025-12-21T0723-build-automation-populate-framework-manifest` (manifest to include)

**Complexity:** Medium-High | **Duration:** 2-3 days | **Risk:** Medium

**Rationale:**
This workflow **completes the distribution pipeline**, enabling automated, reproducible releases. Without it, releases must be manually assembled (error-prone). However, it's **lower urgency** than the core scripts because it automates an existing manual process rather than enabling new capabilities. Can be developed after scripts are complete.

**Blocks:**
- Automated release creation
- Public distribution of framework packages
- Downstream adoption at scale

---

## Dependency Graph

```
[Task 1: Install Script] ──┐
                           ├──> [Task 2: Upgrade Script] ──┐
                           │                                ├──> [Task 5: Release Workflow]
[Task 3: Guardian Profile] ┘                                │
                                                            │
[Task 4: Populate Manifest] ────────────────────────────────┘

Legend:
  ──> : Hard dependency (must complete before)
  ─ ─> : Soft dependency (inform design)
```

**Execution Order:**
1. **Parallel Track A:** Task 1 (Install Script) → Task 2 (Upgrade Script)
2. **Parallel Track B:** Task 3 (Guardian Profile) – can start immediately
3. **Parallel Track C:** Task 4 (Populate Manifest) – can start immediately
4. **Sequential:** Task 5 (Release Workflow) – waits for Tasks 1, 2, 4 completion

**Optimal Parallelization:**
- Start Tasks 1, 3, 4 simultaneously (no dependencies)
- Task 2 starts after Task 1 completes
- Task 5 starts after Tasks 1, 2, 4 complete

---

## Priority & Urgency Assessment

### Priority Levels
- **Critical (Tasks 1, 2, 3):** Core functionality that enables the distribution model
- **High (Tasks 4, 5):** Essential supporting infrastructure

### Urgency Levels
- **High (Tasks 1, 2, 3, 4):** Blocks other work or testing
- **Normal (Task 5):** Automates manual process, can wait for scripts

### Risk Levels
- **Medium-High (Task 2):** Upgrade script complexity (checksums, conflicts)
- **Medium (Tasks 1, 4, 5):** Standard implementation risk
- **Low-Medium (Task 3):** Documentation/specification task

---

## Success Criteria (Initiative-Level)

**Minimal Viable Implementation achieved when:**

1. ✅ Downstream repository can install framework from zip using `framework_install.sh`
2. ✅ Downstream repository can upgrade framework safely with conflict detection
3. ✅ Framework Guardian agent can audit installation and generate upgrade plans
4. ✅ MANIFEST.yml accurately represents framework structure
5. ✅ Release pipeline can produce versioned zip artifacts automatically

**Quality Attributes Validated:**
- ✅ Portability: Scripts work on Linux, macOS, WSL (POSIX compliance)
- ✅ Upgradeability: Conflicts surfaced as .framework-new files
- ✅ Auditability: Manifest and reports for every upgrade
- ✅ Safety: Minimal diffs, backups, human review required
- ✅ Operability: Guardian produces actionable reports

---

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| POSIX compliance issues across platforms | High | Medium | Extensive testing on dash, bash, sh; use shellcheck |
| Checksum calculation portability | High | Medium | Test sha256sum vs shasum; document platform differences |
| Conflict detection false positives | Medium | Medium | TDD with diverse test cases; clear logging |
| Manifest drift from repository | Medium | High | Automated generation script; CI validation |
| Release workflow complexity | Medium | Medium | Incremental development; local testing before CI |

---

## Next Steps

1. **Immediate (Day 1):**
   - Assign Task 1 (Install Script) to build-automation agent
   - Assign Task 3 (Guardian Profile) to architect agent
   - Assign Task 4 (Populate Manifest) to build-automation agent

2. **Short-term (Days 2-3):**
   - Assign Task 2 (Upgrade Script) after Task 1 completes
   - Review Guardian profile draft
   - Test manifest generation script

3. **Medium-term (Days 4-7):**
   - Assign Task 5 (Release Workflow) after dependencies complete
   - Integration testing of install → upgrade → Guardian workflow
   - Documentation review and updates

4. **Validation:**
   - Test complete workflow in isolated repository
   - Verify all success criteria
   - Prepare for pilot release

---

## File References

**Architecture:**
- `docs/architecture/adrs/ADR-013-zip-distribution.md`
- `docs/architecture/adrs/ADR-014-framework-guardian-agent.md`
- `docs/architecture/design/distribution_of_releases_architecture.md`
- `docs/architecture/design/distribution_of_releases_technical_design.md`

**Templates (Existing):**
- `docs/templates/automation/framework-manifest-template.yml`
- `docs/templates/automation/framework-audit-report-template.md`
- `docs/templates/automation/framework-upgrade-plan-template.md`

**Tasks Created:**
- `work/collaboration/inbox/2025-12-21T0720-build-automation-framework-install-script.yaml`
- `work/collaboration/inbox/2025-12-21T0721-build-automation-framework-upgrade-script.yaml`
- `work/collaboration/inbox/2025-12-21T0722-architect-framework-guardian-agent-profile.yaml`
- `work/collaboration/inbox/2025-12-21T0723-build-automation-populate-framework-manifest.yaml`
- `work/collaboration/inbox/2025-12-21T0724-build-automation-packaging-release-workflow.yaml`

---

**Planning Notes:**
- All tasks follow file-based orchestration approach (YAML in work/collaboration/inbox/)
- All tasks specify concrete, testable artifacts
- All tasks reference ATDD (directive 016) and TDD (directive 017) requirements
- Prioritization balances urgency (blocks other work) with complexity (development time)
- Dependency graph enables parallel execution where possible

**Estimated Total Effort:** 7-12 days (with parallelization: 5-7 days wall time)

---

_Generated by Planning Petra_  
_Date: 2025-12-21T07:20:00Z_  
_Context: Packaging and Release Initiative Advancement_
