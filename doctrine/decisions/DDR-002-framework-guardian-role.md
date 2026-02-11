# Doctrine Decision Records

## DDR-002: Framework Guardian Agent Role

**status**: Accepted  
**date**: 2026-02-11  
**supersedes**: Repository-level guardian decisions (elevated to framework level)

### Context

When doctrine is distributed to adopting repositories, there is risk of:
- Leaving users with unresolved merge conflicts (`.framework-new` files)
- Inconsistent agent specifications after upgrades
- Misplaced customizations that override core framework files
- No clear guidance on how to reconcile local intent with framework updates

We need a universal agent role pattern that can audit installations and guide upgrades without overwriting local intent—a pattern that works across any repository adopting the doctrine.

### Decision

Define the **Framework Guardian** as a specialized agent role with two universal operating modes:

#### 1. Audit Mode
Compares the repository against framework manifests and produces a structured audit report that lists:
- Missing framework assets
- Outdated or misplaced framework files
- Customizations that conflict with core patterns
- Recommended corrective actions

**Output artifact**: `validation/FRAMEWORK_AUDIT_REPORT.md`

#### 2. Upgrade Mode
Runs after framework upgrades, inspects conflicts (e.g., `.framework-new` files), and produces an actionable upgrade plan that:
- Proposes minimal patches for each conflict
- Suggests moving customizations to `local/` directories
- Documents whether each change is "Framework-aligned" or "Local customization preserved"

**Output artifact**: `validation/FRAMEWORK_UPGRADE_PLAN.md`

### Universal Guardrails

The Framework Guardian role pattern enforces these constraints across all repositories:

1. **Never overwrite files automatically** – always propose, never execute
2. **Always distinguish framework vs. local intent** – explicit classification of each change
3. **Load context in strict order** – general guidelines → AGENTS → vision → meta → manifest
4. **Produce structured artifacts** – audit reports and upgrade plans follow standard templates
5. **Stay within specialization** – framework maintenance only, no scope creep

### Rationale

- **Human-scale upgrades**: Scripts provide raw diffs; the Guardian interprets them and produces actionable plans.
- **Consistency**: Every repository receives the same audit template, making compliance measurable.
- **Safety**: By forbidding silent overwrites, the pattern enforces core/local separation and reduces accidental regressions.
- **Portability**: The role pattern travels with the doctrine, ensuring upgrade assistance is built-in.

### Consequences

**Positive**
- ✅ Clear handoffs: audits and upgrade plans become standard artifacts under `validation/`.
- ✅ Easier adoption for non-core teams; they can rely on the Guardian to interpret upgrades.
- ✅ Provides feedback loops for framework maintainers (recurring drift patterns show up in reports).
- ✅ Universal pattern: works across any repository adopting the doctrine.

**Watch-outs**
- ⚠️ Requires coordination to launch the agent after each upgrade.
- ⚠️ If reports are ignored, conflicts may still linger—process enforcement is needed.
- ⚠️ Agent scope must remain narrow (framework maintenance only) to avoid scope creep.

### Implementation Pattern

**In Agent Profile:**
```markdown
## Specialization
- **Audit Mode**: Compare repository state against framework manifests
- **Upgrade Mode**: Analyze `.framework-new` conflicts and produce upgrade plans
- **Output**: Structured reports in `validation/` directory
```

**Typical Workflow:**
1. Framework upgrade script creates `.framework-new` files
2. User invokes Framework Guardian in upgrade mode
3. Guardian analyzes conflicts and produces `FRAMEWORK_UPGRADE_PLAN.md`
4. User reviews plan and applies approved changes
5. Guardian can re-audit to confirm resolution

### Considered Alternatives

1. **Rely solely on scripts**: Rejected because it leaves users with raw conflicts and no guidance; fails audit requirements.
2. **Manual review only**: Rejected because it scales poorly, produces inconsistent output, and contradicts automation goals.
3. **Self-upgrading scripts that merge automatically**: Rejected as too risky; undermines "do not overwrite local intent" principle.

### Related

- **Doctrine**: Directive 025 (Framework Guardian Initialization)
- **Implementation**: See your repository's architecture decisions for distribution mechanisms
- **Agent Profile**: `doctrine/agents/framework-guardian.agent.md`
