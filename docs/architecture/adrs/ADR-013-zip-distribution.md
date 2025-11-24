# Architecture Decision Records

## ADR-013: Adopt Zip-Based Framework Distribution

**status**: Accepted  
**date**: 2025-11-24

### Context

Ideation in `tmp/ideas/distribution_of_releases/zip_based_distribution.md` and related templates identified the need to distribute the agent framework without forcing downstream teams to rely on Git history or submodules. Consumers span GitHub, GitLab, on-prem Git, and file shares, so releases must be self-contained, scriptable, and safe for air‑gapped installs. We also need to respect the “core vs local” boundary to prevent upgrades from overwriting project-specific agents and guidelines.

### Decision

Ship every framework release as `quickstart-framework-<version>.zip` containing:

1. `framework_core/` – curated copies of core directories (`.github/agents/`, `docs/directives/`, `docs/guidelines/`, `docs/templates/`, `validation/`, key `work/` scaffolds).
2. `scripts/framework_install.sh` and `scripts/framework_upgrade.sh` – portable POSIX shell utilities that install/upgrade the core without touching `local/**`.
3. `META/` – `MANIFEST.yml`, release notes, and upgrade notes describing file inventory and migration guidance.

Projects unzip the package anywhere, run the scripts against their repo, and rely on `.framework_meta.yml` to track installed versions. All merge/conflict handling happens outside the zip via `.framework-new` files.

### Rationale

- **Portability:** Zip + shell scripts run everywhere without extra dependencies.
- **Deterministic upgrades:** Managed directories are versioned in the manifest, making audits predictable.
- **Safety:** Scripts never overwrite divergent files; conflicts become explicit artifacts for humans or agents to reconcile.
- **Documentation:** Packaging release notes and manifest data alongside the scripts keeps consumers aligned with the canonical structure.

### Envisioned Consequences

**Positive**
- ✅ Downstream teams can install or upgrade without rewriting history or depending on git remotes.
- ✅ Automated tooling (Framework Guardian) can diff against the manifest to highlight drift.
- ✅ Releases are easy to mirror or archive.

**Negative / Watch-outs**
- ⚠️ Zip must be regenerated for every release, so CI packaging needs to remain reliable.
- ⚠️ Large repositories may inflate artifact size; consider optional compression exclusions later.
- ⚠️ Scripts must be carefully tested to avoid path issues on Windows Subsystem for Linux or macOS.

### Considered Alternatives

1. **Git submodule–based distribution.** Rejected: adds workflow complexity for analysts and non-Git hosts; less portable.
2. **Generator + patch stream.** Rejected: patch application is brittle and requires tooling parity.
3. **Direct forks with manual upstream pulls.** Rejected: high conflict risk and poor upgrade ergonomics.
