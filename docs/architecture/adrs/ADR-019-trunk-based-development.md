# ADR-019: Adopt Trunk-Based Development

**status**: `Accepted`  
**date**: 2025-11-30

### Context

Multi-agent orchestration systems face unique version control challenges:

- **Async coordination**: Multiple agents work simultaneously on different tasks
- **File-based state**: Task files move through directories as state changes
- **Rapid iteration**: Agents produce artifacts in minutes to hours, not days
- **Conflict potential**: Multiple agents may edit overlapping documentation or shared files
- **Stale work risk**: Long-lived branches accumulate context drift (Issue #107, task_age_checker.py)

Traditional feature-branch workflows create friction:

- **Branch divergence**: Long-lived branches accumulate merge conflicts
- **Integration delays**: Changes sit in branches waiting for review/merge
- **Context staleness**: By merge time, base branch has evolved significantly
- **Complex coordination**: Agents must track which branch contains which context
- **Review bottlenecks**: PRs pile up waiting for human approval

The repository already has mechanisms that reduce risk:

- **ATDD/TDD discipline** (ADR-012, Directives 016/017): Test-first approach catches regressions
- **Task age detection** (task_age_checker.py): Flags tasks >24h old as potentially stale
- **Path conventions** (ADR-004): Standardized directory structure reduces accidental conflicts
- **State-based ownership** (ADR-003): Task files have clear ownership through directory location
- **Automated validation** (validation/ scripts): Schema and structure checks run continuously

We need a branching strategy that:

- Minimizes integration delays and merge conflicts
- Works with async agent execution patterns
- Leverages existing safety mechanisms
- Supports both local development and CI/CD workflows
- Remains VCS-agnostic but optimizes for GitHub
- Enables rapid feedback through automated pipelines

### Decision

**We will adopt trunk-based development as the default branching strategy.**

Specifically:

1. **Single shared trunk**: `main` branch is the source of truth
2. **Small, frequent commits**: Changes committed to trunk multiple times per day
3. **Short-lived feature branches** (optional): Maximum lifetime 24 hours, preferred <4 hours
4. **Feature flags for incomplete work**: Hide partially implemented features behind toggles
5. **Continuous validation**: Every commit runs full test suite and validation checks
6. **Release from trunk**: Deployments and releases cut directly from trunk
7. **Hotfix protocol**: Critical fixes committed directly to trunk, then backported if needed

**Branch lifetime policy:**

- **Preferred**: Direct commits to trunk for small changes (<100 lines, single concern)
- **Acceptable**: Short-lived branch (4-8 hours) for coordinated multi-file changes
- **Warning zone**: Branches >8 hours old trigger review
- **Maximum**: 24 hours before mandatory merge or abandon (enforced by task age checker)

**Integration requirements:**

- All commits must pass:
  - Automated test suite (unit + acceptance tests)
  - Validation scripts (task schema, directory structure, naming conventions)
  - Linting and formatting checks
  - Documentation consistency checks
- Pre-commit hooks run validation locally
- CI pipeline validates on every push
- Failed validations block merge to trunk

### Rationale

**Why trunk-based development?**

- **Reduces merge conflicts**: Small, frequent integrations prevent large divergences
- **Accelerates feedback**: Changes validated immediately, not days later
- **Aligns with agent patterns**: Agents complete tasks in hours, not weeks—branch lifetime matches task lifetime
- **Simplifies coordination**: Single branch = single source of truth, no "which branch has X?" questions
- **Enables rapid fixes**: Critical issues addressed immediately without branch management overhead
- **Improves observability**: Linear history easier to audit and understand

**Why 24-hour branch maximum?**

- **Context drift prevention**: Matches task age checker threshold (task_age_checker.py)
- **Forces decomposition**: Changes too large for 24h should be split into smaller tasks
- **Agent compatibility**: Most agent tasks complete in <4 hours; 24h provides buffer for complex work
- **Reduces stale work**: Long-lived branches accumulate conflicts; short lifetime minimizes this
- **Human intervention window**: 24h gives humans time to review without blocking progress

**Why leverage existing safety mechanisms?**

- **ATDD/TDD as safety net** (ADR-012): Test-first approach catches regressions before they reach trunk
- **Validation pipeline**: Schema checks, naming conventions, and structure validation run automatically
- **Task lifecycle enforcement**: State-based ownership (ADR-003) prevents concurrent edits to same task
- **Path conventions** (ADR-004): Predictable file locations reduce accidental conflicts
- **Monitoring**: Task age checker, metrics collection, and dashboard provide observability

**Trade-offs accepted:**

- **Discipline required**: Team must maintain test coverage and validation checks
- **Incomplete features in trunk**: Feature flags add complexity but enable continuous integration
- **Less isolation**: Bugs can reach trunk faster (mitigated by automated validation)
- **Revert frequency**: Broken commits must be reverted quickly (automation makes this fast)
- **Initial friction**: Transition from feature-branch model requires habit change

**Alternatives considered:**

1. **Git Flow (develop + release branches)**
   - Rejected: Too heavyweight for rapid agent iteration; integration delays accumulate
   
2. **GitHub Flow (long-lived feature branches + PRs)**
   - Rejected: PR review becomes bottleneck; branch divergence increases conflict risk
   
3. **Ship/Show/Ask pattern** (selective PR review)
   - Partially adopted: Small changes can skip review (Ship), complex changes get async review (Show)
   
4. **Continuous deployment from feature branches**
   - Rejected: Multiple deployment targets complicate rollback and create environment drift

5. **Agent-trunk/main split (dual-trunk model)**
   - **Considered for low-trust environments**: Separate `agent-trunk` for autonomous agent commits with frequent reviewed PRs to `main`
   - **Trade-off**: Balances trust requirements with TBD benefits
   - **Use case**: Organizations requiring human oversight on all production changes
   - **Decision**: Adopt as optional trust model variant (see "Trust Model Variants" section below)

### Trust Model Variants

Trunk-based development assumes sufficient trust for direct trunk commits. However, different organizational contexts have different trust requirements:

#### High-Trust Model (Default)

**Context**: Established teams, robust automation, high confidence in validation pipeline.

**Configuration:**
- Single trunk (`main`)
- Agents commit directly for small changes
- Humans commit directly or use 4h branches
- Post-merge review acceptable (Ship/Show pattern)

**Advantages:**
- Maximum velocity
- Minimal coordination overhead
- Fastest feedback loops

**Requirements:**
- Comprehensive test coverage (ATDD/TDD)
- Robust validation pipeline
- Team discipline and training
- Revert-first culture

#### Low-Trust Model (Agent-Trunk Variant)

**Context**: New teams, regulatory requirements, external contributors, or environments where human oversight is mandatory.

**Configuration:**
- **Agent trunk**: `agent-trunk` branch for autonomous agent commits
- **Human trunk**: `main` branch requiring human review
- **Integration**: Frequent (2-4x daily) reviewed PRs from `agent-trunk` → `main`
- **CI/CD**: Both branches run full validation; `agent-trunk` enables continuous testing

**Advantages:**
- Maintains TBD benefits for agent velocity
- Provides human oversight gate for production
- Separates "autonomous work" from "reviewed work"
- Enables learning period for trust building

**Workflow:**
```
Agents → commit directly to agent-trunk
       ↓
   CI validates on agent-trunk
       ↓
   Batched PR (2-4x daily) → main
       ↓
   Human reviews and approves
       ↓
   Merge to main → production deployment
```

**Branch protection:**
- `agent-trunk`: Agents have write access, humans can review
- `main`: Requires PR + human approval, agents cannot commit directly

**Migration path:**
- Start with low-trust (agent-trunk/main split)
- Build confidence through metrics (test coverage, revert rate, issue frequency)
- Transition to high-trust (single trunk) after 3-6 months of stable operation

#### Hybrid Model (Task-Based Trust)

**Context**: Mixed team composition, some agents more mature than others.

**Configuration:**
- Trusted agents: Direct commit to `main`
- New/experimental agents: Commit to `agent-trunk`, require review
- Trust level tracked per agent profile

**Implementation:**
- Branch protection rules grant write access based on agent identity
- Task metadata includes trust level: `trust: high | medium | low`
- Medium/low trust tasks route through `agent-trunk`

**Decision criteria:**
- Agent maturity (number of successful tasks)
- Domain sensitivity (infrastructure changes vs. documentation)
- Task complexity (risk assessment)

### Recommended Trust Model Selection

**Choose High-Trust (single trunk) if:**
- ✅ Team has >3 months experience with agent orchestration
- ✅ Test coverage >80% with ATDD/TDD discipline
- ✅ Revert rate <5% over last 30 days
- ✅ Validation pipeline catches >95% of issues pre-merge
- ✅ Team comfortable with post-merge review

**Choose Low-Trust (agent-trunk/main) if:**
- ⚠️ New to agent orchestration (<3 months)
- ⚠️ Regulatory requirements mandate human review
- ⚠️ External contributors (untrusted agents)
- ⚠️ High-risk domain (security, compliance, legal)
- ⚠️ Building confidence in validation pipeline

**Choose Hybrid (task-based) if:**
- 🔀 Mixed team maturity levels
- 🔀 Different risk levels across domains
- 🔀 Transitioning from low-trust to high-trust
- 🔀 Want granular control over review requirements

**Implementation Note:** The dual-trunk model adds one merge point (agent-trunk → main) but preserves TBD benefits:
- Agents maintain rapid iteration on agent-trunk
- Small, frequent commits (no long-lived branches)
- Continuous validation on agent-trunk
- Human review batched 2-4x daily (reduces bottleneck)
- Clear separation between "tested" (agent-trunk) and "approved" (main)

This approach addresses the trust concern while maintaining most TBD advantages. The key insight: **trust is built over time**. Start with agent-trunk/main split, measure quality metrics, and migrate to single trunk when confidence justifies it.

### Envisioned Consequences

**Positive:**

- ✅ **Reduced conflicts**: Small, frequent integrations minimize merge complexity
- ✅ **Faster feedback**: Validation runs on every commit, catches issues immediately
- ✅ **Agent compatibility**: Branch lifetime aligns with task completion time
- ✅ **Simplified coordination**: Single source of truth reduces "which branch?" confusion
- ✅ **Improved traceability**: Linear history easier to audit and understand
- ✅ **Leverages existing safety**: ATDD/TDD, validation, and monitoring provide safety net
- ✅ **Reduces stale work**: 24h maximum prevents long-lived branches from accumulating drift
- ✅ **Enables rapid hotfixes**: Critical issues addressed without branch management overhead

**Negative:**

- ⚠️ **Requires discipline**: Test coverage and validation must be maintained consistently
- ⚠️ **Feature flag complexity**: Incomplete features need toggles, adding code overhead
- ⚠️ **Revert friction**: Broken commits must be detected and reverted quickly
- ⚠️ **Less isolation**: Experimental work may affect trunk (mitigated by feature flags)
- ⚠️ **Cultural shift**: Teams familiar with Git Flow need habit adjustment
- ⚠️ **Review pressure**: Async review (Show pattern) requires trust and post-merge accountability

**Risks:**

- **Test suite degradation**: Without maintained test coverage, trunk becomes unstable
  - Mitigation: ADR-012 mandates ATDD/TDD; validation pipeline enforces test presence
  
- **Merge conflicts on shared files**: Multiple agents editing same file simultaneously
  - Mitigation: Path conventions (ADR-004), state-based ownership (ADR-003), task age checker
  
- **Incomplete features visible**: Partially implemented features leak into production
  - Mitigation: Feature flags hide incomplete work; validation checks for missing flags
  
- **Revert fatigue**: Frequent reverts create frustration
  - Mitigation: Pre-commit hooks catch issues locally; CI validation prevents bad commits reaching trunk
  
- **Branch policy violations**: Developers create long-lived branches out of habit
  - Mitigation: GitHub branch protection rules, task age checker warnings, automated cleanup

**Dependencies:**

- Requires robust test suite (ATDD/TDD directives 016/017)
- Requires automated validation pipeline (validation/ scripts)
- Requires task age checker to flag long-lived branches (task_age_checker.py)
- Requires GitHub branch protection rules (or equivalent in other VCS)
- Requires feature flag infrastructure for incomplete work
- Requires team training on trunk-based workflow

### Implementation Guidance

**For Agents:**

1. Check out trunk (`main`) before starting work
2. Make small, focused changes (prefer <100 lines per commit)
3. Run validation locally before committing: `./validation/validate-all.sh`
4. Commit directly to trunk for small changes
5. Use short-lived branch (prefix: `task/<id>`) for coordinated multi-file changes
6. Merge within 4 hours (target) or 24 hours (maximum)
7. If task age checker flags your work as stale (>24h), reconcile immediately

**For Humans:**

1. Pull trunk frequently (`git pull --rebase origin main`)
2. Small changes: commit directly to trunk
3. Large changes: create short-lived branch, merge within 24h
4. Use feature flags for incomplete features
5. If CI fails, revert or fix immediately (target: <15 minutes)
6. Review "Show" changes asynchronously (post-merge review acceptable)

**Branch naming conventions:**

- Direct to trunk: no branch needed
- Task-related: `task/<task-id>-<slug>` (e.g., `task/2025-11-30T0830-architect-adr019`)
- Hotfix: `hotfix/<issue>-<slug>` (e.g., `hotfix/107-stale-task-detection`)
- Experiment: `experiment/<slug>` (deleted after 24h regardless of outcome)

**Validation checkpoints:**

- **Pre-commit**: Local hooks run linting, formatting, basic validation
- **Pre-push**: Local hooks run unit tests, task schema validation
- **CI pipeline**: Full test suite, acceptance tests, documentation checks
- **Post-merge**: Monitoring dashboard tracks trunk health, task age checker flags stale work

**Recovery procedures:**

- **Broken commit**: Revert immediately (`git revert <sha>`), fix in new commit
- **Stale branch**: Merge or abandon within 24h; task age checker flags for review
- **Merge conflict**: Rebase on trunk, resolve conflicts, re-validate, merge
- **Failed CI**: Fix within 15 minutes or revert; do not accumulate failures

---

**Related ADRs:**

- [ADR-003: Task Lifecycle and State Management](ADR-003-task-lifecycle-state-management.md) - State-based ownership prevents conflicts
- [ADR-004: Work Directory Structure](ADR-004-work-directory-structure.md) - Path conventions reduce conflicts
- [ADR-008: File-Based Asynchronous Agent Coordination](ADR-008-file-based-async-coordination.md) - Async model compatible with trunk-based flow
- [ADR-012: Default to ATDD + TDD for Code Changes](ADR-012-test-driven-defaults.md) - Safety net for continuous integration

**References:**

- [Trunk-Based Development](https://trunkbaseddevelopment.com/) - Community best practices
- [Continuous Integration (Fowler)](https://martinfowler.com/articles/continuousIntegration.html) - Foundational principles
- Issue #107: Stale task detection and conflict avoidance
- `ops/orchestration/task_age_checker.py` - Implementation of 24h threshold enforcement
