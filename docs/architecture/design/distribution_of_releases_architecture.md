# Distribution of Releases – Architectural Vision

Prepared by: Architect Alphonso  
Date: 2025-11-24

## Business Goal Statement

Enable any downstream repository to adopt and continuously upgrade the agent-augmented development framework through a predictable distribution package that preserves local intent. Each release must be consumable without assuming Git remotes or specific tooling so that partners can install, audit, and upgrade from a single zip artifact plus helper scripts.

## Desired Quality Attributes

- **Portability:** Releases must run on GitHub, GitLab, local NAS, or air‑gapped environments using only POSIX shell + unzip.
- **Upgradeability:** Installing a new version must never overwrite local modifications silently; conflicts are surfaced as explicit `.framework-new` files.
- **Auditability:** Every upgrade produces manifest, meta, and agent reports so teams can prove what changed.
- **Safety:** Scripts and agents favor minimal diffs, backups, and human review instead of destructive mutations.
- **Operability:** Framework Guardian automation keeps humans in the loop with actionable reports rather than raw file dumps.

## Organizational Context

- **Framework Maintainers** (core team): cut versioned zips, curate META/MANIFEST.yml, publish release notes, maintain install/upgrade scripts.
- **Derivative Teams**: embed the framework inside product repos, maintain `local/` overrides, and rely on scripted upgrades rather than manual merges.
- **Framework Guardian Agent**: new specialist role responsible for running audits and upgrade plans after scripts execute, ensuring compliance with AGENTS/Directive governance.
- **Distribution Channels**: zipped artifacts delivered via Github Releases or internal storage; no assumption of Git submodules.

Dependencies include existing governance (AGENTS.md, directives 001–017), task orchestration, and the file-based coordination model in `work/`.

## Solution Overview

1. **Release Package Format**
   - `quickstart-framework-<version>.zip` containing:
     - `framework_core/` (curated `.github/agents`, directives, guidelines, templates, validation assets, work scaffolds).
     - `scripts/framework_install.sh` and `scripts/framework_upgrade.sh`.
     - `META/` with `MANIFEST.yml`, `RELEASE_NOTES.md`, `UPGRADE_NOTES_<prev>_to_<current>.md`.
   - Package intentionally excludes local overrides to keep updates deterministic.

2. **Core vs Local Boundary**
   - Projects treat files under `framework_core/` (or the mapped directories) as managed.
   - Local customizations live under `local/**` (agents, guidelines, directives) or other project folders.
   - `.framework_meta.yml` records installed version, date, and checksum of the release.

3. **Installation / Upgrade Scripts**
   - `framework_install.sh` copies missing framework files into a target repo, records metadata, and reports NEW/SKIPPED files.
   - `framework_upgrade.sh` compares each file; identical → `UNCHANGED`, missing → `NEW`, diverged → writes `<name>.framework-new` and logs a `CONFLICT`. Supports `--dry-run`.
   - Scripts never touch `local/**` or delete files; they generate summaries suitable for automation.

4. **Framework Guardian Agent**
   - Consumes script output along with `META/MANIFEST.yml`, `.framework_meta.yml`, and any `.framework-new` conflicts.
   - Runs in two modes:
     - **Audit**: compares local state against the canonical manifest, flagging missing, outdated, or misplaced files; outputs `validation/FRAMEWORK_AUDIT_REPORT.md`.
     - **Upgrade**: classifies conflicts, proposes minimal patches, recommends relocating local customizations, and writes `validation/FRAMEWORK_UPGRADE_PLAN.md`.
   - Acts as the bridge between low-level scripts and human reviewers.

5. **Governance + Documentation**
   - ADR-013 (Zip Distribution) and ADR-014 (Framework Guardian Agent) capture the reasoning for the above structure.
   - Technical design (see `docs/architecture/design/distribution_of_releases_technical_design.md`) specifies script behavior, manifest schema, and Guardian workflows.
   - Templates in `tmp/ideas/distribution_of_releases/TEMPLATE_*.md` become canonical outputs (audit report, upgrade plan, manifest).

By combining a deterministic release artifact, conservative scripts, and the Framework Guardian agent, derivative repositories can safely consume framework updates without sacrificing local autonomy.
