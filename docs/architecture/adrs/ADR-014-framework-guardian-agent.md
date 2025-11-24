# Architecture Decision Records

## ADR-014: Introduce Framework Guardian Agent

**status**: Accepted  
**date**: 2025-11-24

### Context

The new zip distribution (ADR-013) delivers core files plus scripts that stop short of resolving merge conflicts. Ideation in `tmp/ideas/distribution_of_releases/framework-guardian_agent.md` highlighted the risk of leaving users alone with `.framework-new` files, inconsistent agent specs, and misplaced overrides. We need an autonomous-yet-constrained specialist that audits installations and guides upgrades without overwriting local intent.

### Decision

Create a specialist agent profile “Framework Guardian” with two operating modes:

1. **Audit Mode** – compares the project against `META/MANIFEST.yml` and `.framework_meta.yml`, producing `validation/FRAMEWORK_AUDIT_REPORT.md` that lists missing, outdated, or misplaced framework assets.
2. **Upgrade Mode** – runs after `framework_upgrade.sh`, inspects each `.framework-new` conflict, proposes minimal patches, suggests moving customizations to `local/`, and documents the plan in `validation/FRAMEWORK_UPGRADE_PLAN.md`.

Guardrails: never overwrite files automatically, always note whether a change is “Framework-aligned” or “Local customization preserved”, and load canonical context in strict order (general guidelines → AGENTS → docs/VISION → meta → manifest).

### Rationale

- **Human-scale upgrades:** Scripts provide raw diffs; the Guardian interprets them and produces actionable plans.
- **Consistency:** Every repository receives the same audit template (see `tmp/ideas/distribution_of_releases/TEMPLATE_*.md`), making compliance measurable.
- **Safety:** By forbidding silent overwrites, the agent enforces the core/local separation and reduces accidental regressions.

### Envisioned Consequences

**Positive**
- ✅ Clear handoffs: audits and upgrade plans become standard artifacts under `validation/`.
- ✅ Easier adoption for non-core teams; they can rely on the Guardian to interpret upgrades.
- ✅ Provides feedback loops for framework maintainers (recurring drift patterns show up in reports).

**Negative / Watch-outs**
- ⚠️ Requires additional automation or coordination to launch the agent after each upgrade.
- ⚠️ If reports are ignored, conflicts may still linger—process enforcement is needed.
- ⚠️ Agent scope must remain narrow (framework maintenance only) to avoid scope creep.

### Considered Alternatives

1. **Rely solely on scripts.** Rejected: leaves users with raw conflicts and no guidance; fails audit requirements.
2. **Manual review only.** Rejected: scales poorly, inconsistent output, and contradicts automation goals.
3. **Self-upgrading scripts that merge automatically.** Rejected: too risky; undermines the “do not overwrite local intent” principle.
