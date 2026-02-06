# Tool Versioning Policy

**Version:** 1.0.0  
**Last Updated:** 2026-02-06  
**Audience:** Maintainers and platform owners responsible for Copilot toolchain stability.

## Purpose

Define when and how preinstalled tooling versions are selected, updated, and rolled back to balance reliability with access to new capabilities.

## Scope

Applies to tools installed by `.github/copilot/setup.sh` and referenced in `docs/HOW_TO_USE/copilot-tooling-setup.md`.

## Update Cadence

- **Quarterly review** (default): Review versions, changelogs, and security advisories.
- **On-demand update**: Triggered by critical security fixes, broken installs, or major compatibility issues.

## Version Selection Criteria

- **Stability first**: Prefer versions with stable releases and known compatibility.
- **Security**: Prioritize versions that address CVEs or supply-chain concerns.
- **Operational fit**: Avoid versions that break scripts, workflows, or CI validation.
- **Reproducibility**: Pin versions when upstream churn is high or package managers differ.

## Update Procedure

1. Review tool changelogs and relevant CVEs.
2. Update version pins (or documented version references) in `.github/copilot/setup.sh`.
3. Run local setup validation and CI validation workflow.
4. Update `docs/HOW_TO_USE/copilot-tooling-setup.md` with new versions.
5. Record changes in `docs/CHANGELOG.md` when impacts are user-visible.

## Testing Requirements

- Setup script runs idempotently on Linux and macOS paths.
- CLI tools respond to `--version` checks.
- CI workflow for Copilot setup passes.
- If tools are used in validation scripts, run targeted smoke tests.

## Breaking Changes & Rollback

- **Breaking change detection:** If CLI flags or output formats change, document the change and adjust dependent scripts.
- **Rollback trigger:** Revert to last known good version if validation fails or tooling regresses.
- **Rollback method:** Restore previous version pin and re-run validation.

## Communication

- Notify maintainers via the changelog and relevant planning notes.
- Track pending upgrades in planning artifacts when work is deferred.

## Related References

- `docs/HOW_TO_USE/copilot-tooling-setup.md`
- `.github/copilot/setup.sh`
- `docs/architecture/assessments/copilot-tooling-value-assessment.md`
