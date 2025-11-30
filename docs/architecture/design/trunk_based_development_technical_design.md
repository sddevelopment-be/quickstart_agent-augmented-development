# Technical Design: Trunk-Based Development Implementation

_Version: 1.0.0_  
_Last updated: 2025-11-30_  
_Status: Proposed_

## Context

This technical design details the implementation of trunk-based development (TBD) for the agent-augmented orchestration repository, as described in [ADR-019: Adopt Trunk-Based Development](../adrs/ADR-019-trunk-based-development.md).

The design addresses:

- Generic VCS implementation patterns
- GitHub-specific integration and automation
- Integration with existing task lifecycle (ADR-003)
- Conflict detection and prevention mechanisms
- Validation pipeline configuration
- Branch protection and enforcement
- Agent and human workflow adaptations

The repository's existing infrastructure provides foundation for trunk-based development:

- **ATDD/TDD discipline** (ADR-012, Directives 016/017): Test-first safety net
- **Task age checker** (task_age_checker.py): Detects stale work >24h
- **Validation scripts** (validation/): Schema, structure, and naming enforcement
- **File-based coordination** (ADR-008): Directory-based state prevents some conflicts
- **Path conventions** (ADR-004): Predictable locations reduce accidental conflicts

References:

- [ADR-003: Task Lifecycle and State Management](../adrs/ADR-003-task-lifecycle-state-management.md)
- [ADR-004: Work Directory Structure](../adrs/ADR-004-work-directory-structure.md)
- [ADR-008: File-Based Asynchronous Agent Coordination](../adrs/ADR-008-file-based-async-coordination.md)
- [ADR-012: Default to ATDD + TDD for Code Changes](../adrs/ADR-012-test-driven-defaults.md)
- [ADR-019: Adopt Trunk-Based Development](../adrs/ADR-019-trunk-based-development.md)

## Acceptance Criteria

### Functional Requirements

- ✅ F1: Developers can commit directly to trunk for small changes (<100 lines)
- ✅ F2: Short-lived branches (4-24h) supported for coordinated changes
- ✅ F3: Branch age checker detects and flags branches >8h old
- ✅ F4: Automated validation runs on every commit (pre-commit, CI)
- ✅ F5: Failed validation blocks merge to trunk
- ✅ F6: Feature flags hide incomplete work in production
- ✅ F7: Revert procedures enable rapid rollback (<5 minutes)
- ✅ F8: Dashboard displays trunk health metrics
- ✅ F9: Task age checker flags stale work >24h
- ✅ F10: Documentation and training materials available

### Non-Functional Requirements

- ✅ NFR1: Pre-commit hooks complete in <10 seconds (developer experience)
- ✅ NFR2: CI validation completes in <5 minutes (feedback speed)
- ✅ NFR3: Branch protection prevents force-push to trunk (safety)
- ✅ NFR4: Trunk remains deployable 95%+ of time (stability)
- ✅ NFR5: Conflict detection alerts within 1 minute (responsiveness)
- ✅ NFR6: Generic VCS patterns work on GitLab, Bitbucket, Gitea (portability)
- ✅ NFR7: GitHub-specific features enhance but don't require trunk-based flow (optional optimization)

### Definition of Done

- [ ] Branch protection rules configured for trunk
- [ ] Pre-commit hooks installed and documented
- [ ] CI pipeline validates all commits
- [ ] Task age checker extended to monitor branch age
- [ ] Feature flag infrastructure documented
- [ ] Revert procedures documented and tested
- [ ] Dashboard updated with trunk health metrics
- [ ] Training guide created for agents and humans
- [ ] Migration plan from feature-branch workflow
- [ ] Rollback strategy documented

## Design

### Overview

The implementation consists of:

1. **VCS Configuration**: Branch protection, merge policies, commit validation
2. **Local Workflow**: Pre-commit hooks, validation scripts, branch naming
3. **CI/CD Pipeline**: Automated testing, validation, deployment from trunk
4. **Monitoring**: Branch age tracking, trunk health dashboard, conflict alerts
5. **Agent Integration**: Task lifecycle compatibility, automation support
6. **Human Workflows**: Development patterns, review processes, revert procedures

### Generic VCS Implementation

These patterns work across Git-based VCS providers (GitHub, GitLab, Bitbucket, Gitea, etc.):

#### Branch Protection Rules

**Trunk branch (`main`) protection:**

```yaml
# Generic branch protection configuration
branch: main
protection:
  # Require validation before merge
  require_status_checks: true
  required_checks:
    - unit-tests
    - acceptance-tests
    - validation-scripts
    - linting
    - documentation-check
  
  # Prevent force-push and deletion
  allow_force_push: false
  allow_deletion: false
  
  # Optional: require reviews for large changes
  require_pull_request_reviews:
    enabled: false  # Ship/Show/Ask pattern allows direct commits
    dismiss_stale_reviews: true
    require_code_owner_reviews: false
  
  # Enforce linear history (optional)
  require_linear_history: true  # Prefer rebase over merge commits
  
  # Allow direct commits from automated agents
  bypass_actors:
    - automation-bot
    - ci-service-account
```

**Short-lived branch policy:**

```yaml
# Branch lifecycle enforcement
branches:
  pattern: "task/*"
  max_lifetime: 24h
  warning_threshold: 8h
  
  pattern: "hotfix/*"
  max_lifetime: 4h
  warning_threshold: 2h
  
  pattern: "experiment/*"
  max_lifetime: 24h
  auto_delete: true
```

#### Pre-Commit Hooks

**File: `.git/hooks/pre-commit`**

```bash
#!/usr/bin/env bash
# Pre-commit validation hook
# Runs fast checks locally before commit

set -e

echo "🔍 Running pre-commit validation..."

# 1. Format check (fast)
echo "  → Checking code formatting..."
if command -v black &> /dev/null; then
    black --check . || {
        echo "❌ Format check failed. Run: black ."
        exit 1
    }
fi

# 2. Lint check (fast)
echo "  → Running linter..."
if command -v ruff &> /dev/null; then
    ruff check . || {
        echo "❌ Linting failed. Run: ruff check --fix ."
        exit 1
    }
fi

# 3. Task schema validation (fast)
echo "  → Validating task schemas..."
if [ -d "work/collaboration" ]; then
    python validation/validate-task-schema.py --fast || {
        echo "❌ Task schema validation failed"
        exit 1
    }
fi

# 4. Basic structure check (fast)
echo "  → Checking directory structure..."
python validation/validate-directory-structure.py --quick || {
    echo "❌ Directory structure validation failed"
    exit 1
}

echo "✅ Pre-commit checks passed"
```

**Installation script:**

```bash
#!/usr/bin/env bash
# install-hooks.sh
# Install Git hooks for trunk-based development

REPO_ROOT=$(git rev-parse --show-toplevel)
HOOKS_DIR="$REPO_ROOT/.git/hooks"

echo "Installing Git hooks..."

# Pre-commit hook
cp "$REPO_ROOT/ops/git-hooks/pre-commit" "$HOOKS_DIR/pre-commit"
chmod +x "$HOOKS_DIR/pre-commit"

# Pre-push hook
cp "$REPO_ROOT/ops/git-hooks/pre-push" "$HOOKS_DIR/pre-push"
chmod +x "$HOOKS_DIR/pre-push"

echo "✅ Hooks installed. Run './ops/git-hooks/uninstall-hooks.sh' to remove."
```

#### Pre-Push Hooks

**File: `.git/hooks/pre-push`**

```bash
#!/usr/bin/env bash
# Pre-push validation hook
# Runs more comprehensive checks before pushing to remote

set -e

echo "🔍 Running pre-push validation..."

# 1. Run unit tests (slower)
echo "  → Running unit tests..."
python -m pytest tests/unit/ -v || {
    echo "❌ Unit tests failed"
    exit 1
}

# 2. Full task validation (slower)
echo "  → Running full task validation..."
python validation/validate-task-schema.py || {
    echo "❌ Task validation failed"
    exit 1
}

# 3. Check for stale tasks
echo "  → Checking for stale tasks..."
python ops/orchestration/task_age_checker.py --threshold 24 --warn-only || {
    echo "⚠️  Warning: Stale tasks detected (>24h old)"
    echo "   Consider updating or archiving before pushing."
}

# 4. Check current branch age
BRANCH=$(git branch --show-current)
if [[ "$BRANCH" != "main" ]]; then
    echo "  → Checking branch age for '$BRANCH'..."
    BRANCH_AGE_HOURS=$(python ops/orchestration/branch_age_checker.py "$BRANCH")
    if (( $(echo "$BRANCH_AGE_HOURS > 8" | bc -l) )); then
        echo "⚠️  Warning: Branch is $BRANCH_AGE_HOURS hours old (threshold: 8h)"
        echo "   Consider merging to trunk soon."
    fi
fi

echo "✅ Pre-push checks passed"
```

#### Commit Message Conventions

```
# Conventional Commits format (optional but recommended)
<type>(<scope>): <subject>

<body>

<footer>

# Types:
feat:     New feature
fix:      Bug fix
docs:     Documentation only
style:    Formatting, missing semicolons, etc
refactor: Code change that neither fixes bug nor adds feature
test:     Adding missing tests
chore:    Updating build tasks, package manager configs, etc
revert:   Reverts a previous commit

# Examples:
feat(task-checker): add branch age monitoring to task_age_checker.py
fix(validation): correct task schema validation for nested artifacts
docs(adr): add ADR-019 for trunk-based development
chore(ci): configure branch protection rules for main branch
```

### GitHub-Specific Implementation

GitHub provides additional features that enhance trunk-based development:

#### Branch Protection Rules (GitHub)

**Configure via GitHub UI or API:**

```bash
# Using GitHub CLI
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["unit-tests","acceptance-tests","validation"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews=null \
  --field restrictions=null \
  --field allow_force_pushes=false \
  --field allow_deletions=false \
  --field required_linear_history=true
```

**Via GitHub Actions workflow:**

```yaml
# .github/workflows/branch-protection.yml
name: Configure Branch Protection
on:
  workflow_dispatch:

jobs:
  configure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure main branch protection
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh api repos/${{ github.repository }}/branches/main/protection \
            --method PUT \
            --field required_status_checks='{"strict":true,"contexts":["unit-tests","acceptance-tests","validation"]}' \
            --field enforce_admins=true \
            --field allow_force_pushes=false \
            --field allow_deletions=false \
            --field required_linear_history=true
```

#### GitHub Actions CI Pipeline

**File: `.github/workflows/trunk-validation.yml`**

```yaml
name: Trunk Validation

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  validation:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for branch age checking
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linting
        run: |
          ruff check .
          black --check .
      
      - name: Validate directory structure
        run: python validation/validate-directory-structure.py
      
      - name: Validate task schemas
        run: python validation/validate-task-schema.py
      
      - name: Check for stale tasks
        run: |
          python ops/orchestration/task_age_checker.py --threshold 24 \
            --format json > task_age_report.json
          cat task_age_report.json
      
      - name: Run unit tests
        run: pytest tests/unit/ -v --cov --cov-report=xml
      
      - name: Run acceptance tests
        run: pytest tests/acceptance/ -v
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
      
      - name: Check documentation
        run: python ops/framework-core/template-status-checker.py

  branch-age-check:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Check branch age
        run: |
          BRANCH_AGE_HOURS=$(python ops/orchestration/branch_age_checker.py ${{ github.head_ref }})
          echo "Branch age: $BRANCH_AGE_HOURS hours"
          
          if (( $(echo "$BRANCH_AGE_HOURS > 24" | bc -l) )); then
            echo "::error::Branch is older than 24 hours. Merge or abandon."
            exit 1
          elif (( $(echo "$BRANCH_AGE_HOURS > 8" | bc -l) )); then
            echo "::warning::Branch is older than 8 hours. Consider merging soon."
          fi
      
      - name: Comment on PR
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '⚠️ This branch is older than 24 hours. Please merge or close this PR to maintain trunk-based development discipline.'
            })

  trunk-health:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Calculate trunk health metrics
        run: |
          # Calculate metrics: commit frequency, test pass rate, revert frequency
          python ops/metrics/calculate-trunk-health.py
      
      - name: Update dashboard
        run: |
          python ops/dashboards/generate-dashboard.py --include-trunk-health
```

#### GitHub Branch Auto-Cleanup

**File: `.github/workflows/branch-cleanup.yml`**

```yaml
name: Branch Cleanup

on:
  schedule:
    - cron: '0 */4 * * *'  # Every 4 hours
  workflow_dispatch:

jobs:
  cleanup-stale-branches:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Find stale branches
        id: find-stale
        run: |
          # Find branches older than 24 hours
          git for-each-ref --format='%(refname:short) %(committerdate:iso8601)' refs/remotes/origin \
            | grep -v 'origin/main' \
            | while read branch date time tz; do
              branch_name=${branch#origin/}
              age_hours=$(python -c "from datetime import datetime; print((datetime.now() - datetime.fromisoformat('$date $time')).total_seconds() / 3600)")
              if (( $(echo "$age_hours > 24" | bc -l) )); then
                echo "::warning::Branch $branch_name is $age_hours hours old"
                echo "$branch_name" >> stale_branches.txt
              fi
            done
      
      - name: Comment on PRs for stale branches
        if: hashFiles('stale_branches.txt') != ''
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          while read branch; do
            pr_number=$(gh pr list --state open --head "$branch" --json number --jq '.[0].number')
            if [ -n "$pr_number" ]; then
              gh pr comment "$pr_number" --body "⚠️ This branch is older than 24 hours. Per [ADR-019](../docs/architecture/adrs/ADR-019-trunk-based-development.md), please merge or close within 24h."
            fi
          done < stale_branches.txt
      
      - name: Auto-close experiment branches
        run: |
          git for-each-ref --format='%(refname:short)' refs/remotes/origin/experiment/* \
            | while read branch; do
              branch_name=${branch#origin/}
              age_hours=$(git log -1 --format=%ct "$branch" | xargs -I {} python -c "import time; print((time.time() - {}) / 3600)")
              if (( $(echo "$age_hours > 24" | bc -l) )); then
                echo "Deleting experiment branch $branch_name (age: $age_hours hours)"
                git push origin --delete "$branch_name"
              fi
            done
```

#### GitHub Actions Status Checks

Required status checks for trunk protection:

- `validation` - Directory structure, task schemas, naming conventions
- `unit-tests` - Unit test suite
- `acceptance-tests` - Acceptance test suite
- `branch-age-check` - Branch lifetime enforcement
- `trunk-health` - Overall trunk stability metrics

### Trust Model Variants: Dual-Trunk Implementation

As described in ADR-019, trunk-based development can be adapted for different trust levels. The **agent-trunk/main dual-trunk model** addresses low-trust environments where human oversight is required.

#### When to Use Dual-Trunk Model

**Use cases:**
- New teams (<3 months with agent orchestration)
- Regulatory requirements mandating human review
- External/untrusted contributors
- High-risk domains (security, compliance, legal)
- Building confidence in validation pipeline

**Migration path:**
- Start with dual-trunk (agent-trunk → main with review)
- Measure quality metrics (test coverage, revert rate, issue frequency)
- Transition to single trunk after 3-6 months of stable operation

#### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Dual-Trunk Workflow                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Agents ──┐                                                │
│           ├──► agent-trunk ──► PR (2-4x daily) ──► main   │
│  Humans ──┘         │                ▲                     │
│                     │                │                     │
│                     └─ CI/CD ────────┘                     │
│                        Validation                          │
│                                                             │
│  Write Access:    agent-trunk        main                  │
│  - Agents         ✅ direct          ❌ PR only            │
│  - Humans         ✅ direct          ✅ direct/PR          │
│                                                             │
│  Deployment:      Testing            Production            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Branch Configuration

**agent-trunk branch:**
```yaml
branch: agent-trunk
protection:
  require_status_checks:
    strict: true
    contexts:
      - validation
      - unit-tests
      - acceptance-tests
  enforce_admins: false
  required_pull_request_reviews: null  # No PR required for agent-trunk
  restrictions:
    users: []
    teams: ["agents"]  # Agents have direct write access
  allow_force_pushes: false
  allow_deletions: false
  required_linear_history: true
```

**main branch:**
```yaml
branch: main
protection:
  require_status_checks:
    strict: true
    contexts:
      - validation
      - unit-tests
      - acceptance-tests
      - agent-trunk-sync  # Ensures PR is from agent-trunk
  enforce_admins: true
  required_pull_request_reviews:
    dismiss_stale_reviews: true
    require_code_owner_reviews: true
    required_approving_review_count: 1
  restrictions:
    users: []
    teams: ["maintainers"]  # Only maintainers can merge to main
  allow_force_pushes: false
  allow_deletions: false
  required_linear_history: true
```

#### GitHub Actions Workflow for Dual-Trunk

**File: `.github/workflows/dual-trunk-sync.yml`**

```yaml
name: Dual-Trunk Sync

on:
  schedule:
    # Auto-create PR from agent-trunk to main 4x daily
    - cron: '0 0,6,12,18 * * *'  # Every 6 hours
  workflow_dispatch:  # Manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Check for changes between agent-trunk and main
        id: check
        run: |
          git fetch origin agent-trunk:agent-trunk
          git fetch origin main:main
          
          CHANGES=$(git rev-list main..agent-trunk --count)
          echo "changes=$CHANGES" >> $GITHUB_OUTPUT
          
          if [ "$CHANGES" -eq 0 ]; then
            echo "✅ No changes to sync"
            exit 0
          fi
          
          echo "📦 Found $CHANGES commits to sync"
      
      - name: Create or update PR
        if: steps.check.outputs.changes > 0
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Check if PR already exists
          EXISTING_PR=$(gh pr list --base main --head agent-trunk --json number --jq '.[0].number')
          
          if [ -z "$EXISTING_PR" ]; then
            # Create new PR
            gh pr create \
              --base main \
              --head agent-trunk \
              --title "Sync: agent-trunk → main ($(date +%Y-%m-%d))" \
              --body "**Automated sync from agent-trunk**

Commits: ${{ steps.check.outputs.changes }}

This PR contains validated agent work ready for production approval.

**Pre-merge checklist:**
- [ ] Review commit messages for clarity
- [ ] Verify all status checks passed
- [ ] Confirm no breaking changes in diff
- [ ] Check deployment readiness

**Merge strategy:** Squash and merge recommended for clean history." \
              --label "automated,sync,agent-trunk"
          else
            # Update existing PR
            echo "♻️  PR #$EXISTING_PR already exists, updated automatically"
          fi
      
      - name: Add reviewers
        if: steps.check.outputs.changes > 0
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          PR_NUMBER=$(gh pr list --base main --head agent-trunk --json number --jq '.[0].number')
          gh pr edit "$PR_NUMBER" --add-reviewer maintainers
```

**File: `.github/workflows/agent-trunk-validation.yml`**

```yaml
name: Agent-Trunk Validation

on:
  push:
    branches:
      - agent-trunk
  pull_request:
    branches:
      - agent-trunk

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run validation
        run: |
          python validation/validate-task-schema.py
          python ops/orchestration/task_age_checker.py --warn-only
      
      - name: Run tests
        run: |
          pytest tests/unit/ -v
          pytest tests/acceptance/ -v
      
      - name: Check agent-trunk health
        run: |
          # Ensure agent-trunk stays close to main
          git fetch origin main
          DIVERGENCE=$(git rev-list origin/main..HEAD --count)
          
          if [ "$DIVERGENCE" -gt 50 ]; then
            echo "⚠️  Warning: agent-trunk has $DIVERGENCE commits ahead of main"
            echo "   Consider syncing to main more frequently (target: 2-4x daily)"
          fi
```

#### Agent Workflow with Dual-Trunk

**For agents (default behavior):**

```python
# ops/orchestration/agent_workflow.py

def commit_to_trunk(task_id: str, changes: list[str], message: str):
    """
    Commit changes following dual-trunk model.
    
    Automatically selects correct trunk based on configuration.
    """
    config = load_trunk_config()
    
    if config.get("trust_model") == "dual-trunk":
        trunk = "agent-trunk"
        # Agents commit to agent-trunk, humans review PR to main
    else:
        trunk = "main"
        # Direct commit to main (high-trust model)
    
    # Commit to appropriate trunk
    subprocess.run(["git", "checkout", trunk])
    subprocess.run(["git", "pull", "--rebase", "origin", trunk])
    
    for file in changes:
        subprocess.run(["git", "add", file])
    
    subprocess.run(["git", "commit", "-m", message])
    subprocess.run(["git", "push", "origin", trunk])
    
    log.info(f"Committed to {trunk}: {message}")
    
    if trunk == "agent-trunk":
        log.info(f"Changes will be reviewed in next PR to main")
```

**Configuration file: `ops/trunk-config.yaml`**

```yaml
# Trunk-based development configuration
trust_model: dual-trunk  # Options: single-trunk, dual-trunk, hybrid

# Dual-trunk settings
dual_trunk:
  agent_branch: agent-trunk
  main_branch: main
  sync_frequency: 4  # PRs per day
  auto_merge: false  # Require human approval
  
# Branch lifetime enforcement
branch_lifetime:
  warning_hours: 8
  maximum_hours: 24
  
# Validation requirements
validation:
  pre_commit: true
  pre_push: true
  ci_pipeline: true
```

#### Migration from Dual-Trunk to Single-Trunk

**Decision criteria (measure over 30 days):**

```yaml
migration_thresholds:
  # Quality metrics
  test_coverage: ">80%"
  revert_rate: "<5%"
  ci_failure_rate: "<10%"
  
  # Velocity metrics
  average_pr_review_time: "<4 hours"
  merge_frequency: ">2x daily"
  
  # Confidence metrics
  human_override_rate: "<2%"
  security_incidents: "0"
  
  # Team maturity
  months_in_operation: ">3"
  team_training_complete: true
```

**Migration process:**

1. **Baseline measurement** (weeks 1-4)
   - Track all quality and velocity metrics
   - Establish baseline revert rate and issue frequency

2. **Quality improvement** (weeks 5-8)
   - Address any recurring issues
   - Increase test coverage to >80%
   - Tune validation pipeline

3. **Confidence building** (weeks 9-12)
   - Reduce human override rate through agent training
   - Improve automation coverage
   - Document lessons learned

4. **Migration preparation** (week 13)
   - Review metrics against thresholds
   - Get team consensus
   - Plan cutover timing

5. **Cutover** (week 14)
   - Update `trust_model: single-trunk` in config
   - Merge agent-trunk to main (final sync)
   - Archive agent-trunk branch
   - Update branch protection rules
   - Notify all stakeholders

6. **Post-migration monitoring** (weeks 15-18)
   - Monitor metrics closely
   - Be prepared to revert if issues arise
   - Gather feedback and adjust

#### Rollback to Dual-Trunk

If single-trunk proves problematic:

```bash
# Restore dual-trunk model
git checkout -b agent-trunk main
git push origin agent-trunk

# Update config
sed -i 's/trust_model: single-trunk/trust_model: dual-trunk/' ops/trunk-config.yaml

# Restore branch protection
./ops/scripts/configure-branch-protection.sh dual-trunk
```

### Integration with Task Lifecycle

Trunk-based development integrates with existing task lifecycle (ADR-003):

#### Task State Transitions and Commits

```
new → assigned → in_progress → done → archived
  ↓       ↓            ↓          ↓        ↓
commit  commit      commits    commit   commit
```

**Commit granularity:**

- **Task assignment**: Single commit moving file to `work/assigned/<agent>/`
- **Task start**: Single commit updating status to `in_progress`
- **Work progress**: Multiple small commits as agent works (incremental artifacts)
- **Task completion**: Single commit with result block, moving to `work/done/`
- **Archive**: Batch commit monthly moving old tasks to `work/archive/`

**Example workflow:**

```bash
# Agent starts task
git checkout main
git pull --rebase origin main

# Move task to assigned
mv work/inbox/2025-11-30T0830-architect-adr019.yaml work/assigned/architect/
git add work/inbox/ work/assigned/architect/
git commit -m "task(architect): assign ADR-019 trunk-based development"
git push origin main

# Update status to in_progress
sed -i 's/status: assigned/status: in_progress/' work/assigned/architect/2025-11-30T0830-architect-adr019.yaml
git add work/assigned/architect/2025-11-30T0830-architect-adr019.yaml
git commit -m "task(architect): start ADR-019 work"
git push origin main

# Create artifacts incrementally
git add docs/architecture/adrs/ADR-019-trunk-based-development.md
git commit -m "docs(adr): add ADR-019 trunk-based development"
git push origin main

git add docs/architecture/design/trunk_based_development_technical_design.md
git commit -m "docs(design): add trunk-based development technical design"
git push origin main

# Complete task
sed -i 's/status: in_progress/status: done/' work/assigned/architect/2025-11-30T0830-architect-adr019.yaml
echo "result:" >> work/assigned/architect/2025-11-30T0830-architect-adr019.yaml
echo "  summary: Created ADR-019, technical design, and approach guide" >> work/assigned/architect/2025-11-30T0830-architect-adr019.yaml
mv work/assigned/architect/2025-11-30T0830-architect-adr019.yaml work/done/architect/
git add work/assigned/architect/ work/done/architect/
git commit -m "task(architect): complete ADR-019 with full documentation suite"
git push origin main
```

#### Conflict Detection and Prevention

**Path-based conflict prevention (ADR-004):**

- Each agent has dedicated directory under `work/assigned/<agent>/`
- Task files named with timestamp prefix ensure uniqueness
- Artifacts listed in task YAML enable pre-commit conflict check

**Pre-commit conflict detection:**

```python
# File: ops/git-hooks/check-conflicts.py
"""
Check for potential conflicts before commit.
Compares artifacts in staged tasks against other in_progress tasks.
"""

import yaml
from pathlib import Path

def get_artifacts_in_flight():
    """Get artifacts from all in_progress tasks."""
    artifacts = set()
    for task_file in Path("work/assigned").rglob("*.yaml"):
        with open(task_file) as f:
            task = yaml.safe_load(f)
        if task.get("status") == "in_progress":
            artifacts.update(task.get("artefacts", []))
    return artifacts

def get_staged_artifacts():
    """Get artifacts from staged task files."""
    # Parse git diff --staged for task files
    # Extract artefacts field from YAML
    pass

def check_conflicts():
    """Check for artifact conflicts."""
    in_flight = get_artifacts_in_flight()
    staged = get_staged_artifacts()
    conflicts = in_flight & staged
    
    if conflicts:
        print("❌ Conflict detected!")
        print("The following artifacts are already being modified:")
        for artifact in conflicts:
            print(f"  - {artifact}")
        return False
    return True

if __name__ == "__main__":
    exit(0 if check_conflicts() else 1)
```

### Feature Flag Infrastructure

For hiding incomplete features in trunk:

**Environment-based flags (simple):**

```python
# File: ops/common/feature_flags.py
"""Simple environment-based feature flags."""

import os

class FeatureFlags:
    @staticmethod
    def is_enabled(feature_name: str) -> bool:
        """Check if feature is enabled via environment variable."""
        return os.getenv(f"FEATURE_{feature_name.upper()}", "false").lower() == "true"
    
    @staticmethod
    def require(feature_name: str):
        """Decorator to guard incomplete features."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not FeatureFlags.is_enabled(feature_name):
                    raise NotImplementedError(
                        f"Feature '{feature_name}' not enabled. "
                        f"Set FEATURE_{feature_name.upper()}=true to enable."
                    )
                return func(*args, **kwargs)
            return wrapper
        return decorator

# Usage:
@FeatureFlags.require("new_orchestrator")
def experimental_orchestrator():
    # Incomplete implementation
    pass
```

**Configuration-based flags (advanced):**

```yaml
# File: ops/config/feature_flags.yaml
# Feature flags for incomplete work in trunk

features:
  new_orchestrator:
    enabled: false
    description: "Experimental async orchestrator with improved conflict detection"
    rollout_percentage: 0
    default_environment: development
  
  enhanced_task_routing:
    enabled: true
    description: "AI-assisted task routing based on agent specialization"
    rollout_percentage: 100
    environments:
      production: false
      development: true
```

### Monitoring and Metrics

**Dashboard integration:**

```python
# File: ops/metrics/trunk_health.py
"""Calculate trunk health metrics for dashboard."""

from datetime import datetime, timedelta
import subprocess

class TrunkHealthMetrics:
    def get_commit_frequency(self, days=7):
        """Commits per day over last N days."""
        result = subprocess.run(
            ["git", "log", "--oneline", f"--since={days} days ago", "main"],
            capture_output=True, text=True
        )
        commits = len(result.stdout.strip().split("\n"))
        return commits / days
    
    def get_revert_rate(self, days=7):
        """Percentage of commits that are reverts."""
        all_commits = subprocess.run(
            ["git", "log", "--oneline", f"--since={days} days ago", "main"],
            capture_output=True, text=True
        ).stdout.strip().split("\n")
        
        reverts = [c for c in all_commits if c.startswith("Revert")]
        return (len(reverts) / len(all_commits)) * 100 if all_commits else 0
    
    def get_test_pass_rate(self):
        """Latest test pass rate from CI."""
        # Parse from CI artifacts or GitHub API
        pass
    
    def get_time_to_fix(self):
        """Average time from failed CI to fix commit."""
        # Parse CI logs
        pass
```

**Trunk health dashboard:**

```markdown
# Trunk Health Dashboard

**Last updated:** 2025-11-30T08:30:00Z

## Key Metrics

| Metric                  | Current | Target | Status |
|-------------------------|---------|--------|--------|
| Commit Frequency        | 12.3/day| >10/day| ✅     |
| Revert Rate             | 2.1%    | <5%    | ✅     |
| Test Pass Rate          | 97.2%   | >95%   | ✅     |
| Avg Time to Fix         | 8 min   | <15min | ✅     |
| Trunk Stability         | 98.1%   | >95%   | ✅     |

## Recent Activity

- Last commit: 4 minutes ago
- Last failure: 2 hours ago (fixed in 6 minutes)
- Active branches: 3 (all <8h old)
- Stale tasks: 0

## Alerts

- ✅ No alerts
```

### Cross-cutting Concerns

#### Security

- Branch protection prevents unauthorized force-push
- Pre-commit hooks block secrets and sensitive data
- Feature flags prevent accidental exposure of incomplete features
- Audit trail in Git log tracks all changes

#### Performance

- Pre-commit hooks complete in <10s (local feedback)
- CI pipeline completes in <5min (rapid validation)
- Dashboard updates in real-time (monitoring)

#### Deployment

- Releases cut directly from trunk (no release branches)
- Feature flags enable gradual rollout
- Revert procedures enable rapid rollback

#### Auditing and Logging

- Git log provides complete commit history
- Task lifecycle tracked in task YAML files
- Dashboard metrics stored for trend analysis
- Branch age checker logs stale branch warnings

## Planning

- **Estimated development time:** 3-5 workdays
- **Estimated rollout time:** 1-2 weeks (phased adoption)
- **Urgency:** Medium (improves workflow but not blocking)
- **Estimated added value:** High (reduces conflicts, accelerates feedback)
- **Depends on:**
  - Existing validation scripts (validation/)
  - Task age checker (task_age_checker.py)
  - ATDD/TDD infrastructure (ADR-012)
  - File-based orchestration (ADR-003, ADR-008)

## Implementation Phases

### Phase 1: Foundation (1-2 days)

1. Configure branch protection for `main`
2. Install pre-commit and pre-push hooks
3. Create branch age checker script
4. Document revert procedures
5. Update validation pipeline

### Phase 2: Automation (1-2 days)

1. Configure GitHub Actions workflows
2. Add branch auto-cleanup automation
3. Integrate trunk health metrics into dashboard
4. Create feature flag infrastructure
5. Add conflict detection to pre-commit hooks

### Phase 3: Training and Rollout (1 week)

1. Create training guide for agents
2. Create training guide for humans
3. Pilot with 2-3 agents
4. Gather feedback and adjust
5. Full rollout to all agents

### Phase 4: Monitoring and Optimization (ongoing)

1. Monitor trunk health metrics
2. Adjust thresholds based on data
3. Refine automation based on feedback
4. Document lessons learned

## Rollback Strategy

If trunk-based development proves incompatible:

1. **Immediate:** Disable branch protection, revert to feature-branch workflow
2. **Short-term:** Document issues, analyze root causes
3. **Long-term:** Consider hybrid approach (trunk for agents, branches for humans)

Rollback triggers:
- Trunk stability <90% for >1 week
- Revert rate >10% for >1 week
- Team consensus that discipline overhead exceeds benefits

---

**Related Documents:**

- [ADR-019: Adopt Trunk-Based Development](../adrs/ADR-019-trunk-based-development.md)
- [Approach: Trunk-Based Development for Agent-First Workflows](../../agents/approaches/trunk-based-development.md)
- [ADR-003: Task Lifecycle and State Management](../adrs/ADR-003-task-lifecycle-state-management.md)
- [ADR-012: Default to ATDD + TDD for Code Changes](../adrs/ADR-012-test-driven-defaults.md)
