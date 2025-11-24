# Technical Design: Framework Distribution & Guardian Workflow

## Context

Architecture vision (`docs/architecture/design/distribution_of_releases_architecture.md`) and ADRs 013–014 define a release model where every framework version ships as a zip plus install/upgrade scripts, with a Framework Guardian agent orchestrating audits. We must translate that vision into precise scripts, metadata formats, and automation artifacts so that downstream teams can adopt upgrades safely without manual guesswork.

Key forces:
- Consumers operate in heterogeneous environments (GitHub, GitLab, air‑gapped VMs) with only POSIX shell support.
- Local customizations must never be overwritten; core vs local boundaries require enforcement.
- Audits/upgrade plans need canonical templates for automation and compliance.

## Acceptance Criteria

1. **Zip artefact structure** matches ADR-013: `framework_core/`, `scripts/`, `META/`.
2. **framework_install.sh** copies new files only, sets `.framework_meta.yml`, and prints NEW/SKIPPED summary.
3. **framework_upgrade.sh** supports `--dry-run`, writes `<file>.framework-new` for conflicts, and never modifies `local/**`.
4. **META/MANIFEST.yml** lists every managed file with checksum + version; Guardian reads it to detect drift.
5. **Framework Guardian outputs** include `validation/FRAMEWORK_AUDIT_REPORT.md` and `validation/FRAMEWORK_UPGRADE_PLAN.md` using the templates supplied in `tmp/ideas/distribution_of_releases/`.
6. Documentation (CHANGELOG, README pointers) explains workflow end-to-end.

## Design

### Overview

1. **Packaging Pipeline**
   - CI job collects curated directories into `framework_core/`, copies scripts and META files, compresses to `quickstart-framework-<version>.zip`.
   - `META/MANIFEST.yml` enumerates each core file with `path`, `sha256`, `mode`, and `scope` (core vs template).
   - Release notes summarise major ADRs and script changes.

2. **Installation Script (`framework_install.sh`)**
   - Detects first-time installs by checking for `.framework_meta.yml`.
   - Iterates over `framework_core/` using `find`.
   - Copies files only when absent in the target repo; never overwrites existing files.
   - After copying, writes `.framework_meta.yml`:
     ```yaml
     framework_version: 1.2.0
     installed_at: 2025-11-24T20:00:00Z
     source_release: quickstart-framework-1.2.0.zip
     ```

3. **Upgrade Script (`framework_upgrade.sh`)**
   - Accepts `PROJECT_ROOT` and optional `--dry-run`.
   - For each file:
     - Missing → copy (or echo in dry-run) and record `NEW`.
     - Identical (checksum match) → log `UNCHANGED`.
     - Divergent → write new version to `<path>.framework-new`, optionally back up existing file, log `CONFLICT`.
   - Generates `upgrade-report.txt` summarizing counts per status.
   - Updates `.framework_meta.yml` only when not in dry-run.

4. **Framework Guardian Agent Flow**
   - Invocation sequence:
     1. Run `framework_install.sh` or `framework_upgrade.sh`.
     2. Launch Guardian in Audit mode → produce `validation/FRAMEWORK_AUDIT_REPORT.md` (use `TEMPLATE_AUDIT_REPORT.md`).
     3. Launch Guardian in Upgrade mode if conflicts exist → produce `validation/FRAMEWORK_UPGRADE_PLAN.md` (use `TEMPLATE_FRAMEWORK_UPDATE_PLAN.md`).
   - Reads `META/MANIFEST.yml`, `.framework_meta.yml`, `upgrade-report.txt`, and any `.framework-new`.
   - Classifies each conflict:
     - Auto-merge candidate (line-for-line match except comments) → propose patch.
     - Manual decision required → highlight sections and recommend moving custom snippets into `local/`.
   - Outputs include summary tables, per-file recommendations, and TODO items for humans.

5. **Supporting Templates**
   - `TEMPLATE_MANIFEST.yml` defines schema for `META/MANIFEST.yml`.
   - `TMP/reference` templates become authoritative by copying them into `docs/templates/framework/`.

### Implementation Considerations

- **Checksum Calculation:** Use `sha256sum` so the Guardian can detect drift reliably; store values in the manifest.
- **Path Normalization:** Scripts must respect spaces and handle relative vs absolute paths; use `find . -type f -print0 | while IFS= read -r -d '' ...`.
- **Backup Policy:** When writing `.framework-new`, also create `file.bak.<timestamp>` when the user disables backups, noting the behavior in logs.
- **Cross-platform Support:** Keep scripts POSIX compliant; avoid Bash-only features. Document Windows usage via WSL.
- **Guardian Agent Inputs:** Provide CLI or task YAML to specify mode (audit/upgrade), target repo, release version, and output paths.
- **Error Handling:** Scripts exit non-zero on fatal errors; Guardian uses ❗️ markers when missing manifest/meta data.

### Cross-cutting Concerns

#### Security
- Scripts run locally and never download remote code beyond the zip the user already obtained.
- Guardian must never exfiltrate data; reports stay within repo.

#### Performance
- Iterating over `framework_core/` is linear in file count; use checksums only when files differ in size/timestamp to avoid unnecessary hashing.

#### Deployment
- Zip published through release pipeline; include instructions in release notes.
- Guardian agent profile stored under `.github/agents/framework-guardian.agent.md`.

#### Auditing and Logging
- Scripts log their actions (NEW/UNCHANGED/CONFLICT) to stdout and `upgrade-report.txt`.
- Guardian logs mode transitions, primer usage, and outputs structured Markdown tables for compliance.

## Planning
- **Estimated development time:** 5–7 workdays (packaging automation, script updates, templates).
- **Estimated rollout time:** 2 days (prepare release artifact, pilot upgrade).
- **Urgency:** high — required before next public release.
- **Estimated added value:** high — unlocks reproducible distribution for all downstream projects.
- **Depends on:** Completion of ADR-013/014, availability of Framework Guardian agent profile, CI pipeline access to build artifacts.
