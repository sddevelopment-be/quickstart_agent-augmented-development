# Approach: Trunk-Based Development for Agent-First Workflows

**Purpose:** Practical guide for implementing trunk-based development in agent-augmented orchestration systems.

**Audience:** Agents, humans, automation engineers

**Status:** Active

**Last updated:** 2025-11-30

---

## Overview

Trunk-based development (TBD) is a branching strategy where all developers (agents and humans) commit frequently to a single shared branch (`main`), with short-lived feature branches (<24 hours) used only for coordinated changes. This approach minimizes merge conflicts, accelerates feedback, and aligns naturally with agent task completion patterns.

**Key principles:**

1. **Single source of truth:** `main` branch is always deployable
2. **Small, frequent commits:** Multiple commits per day
3. **Short-lived branches:** Maximum 24 hours, prefer <4 hours
4. **Continuous validation:** Every commit runs tests and checks
5. **Feature flags:** Hide incomplete work, don't hold it in branches
6. **Rapid revert:** Fix or rollback within 15 minutes of failure

**When to use trunk-based development:**

- ✅ Async multi-agent orchestration (this repository)
- ✅ Rapid iteration with frequent small changes
- ✅ Strong test coverage and automated validation
- ✅ Team comfortable with continuous integration discipline

**When to avoid:**

- ❌ Large, risky changes without adequate test coverage
- ❌ Teams without automated validation infrastructure
- ❌ Work requiring extended isolation (>24h)

---

## Trust Model Selection

Trunk-based development can be configured for different trust levels. Check your repository configuration in `ops/trunk-config.yaml`:

### Single-Trunk (High-Trust) - Default

**All contributors commit directly to `main`.**

```bash
# Check current model
grep "trust_model" ops/trunk-config.yaml
# Output: trust_model: single-trunk

# Trunk branch
TRUNK="main"
```

**Use when:**
- ✅ Team has >3 months experience with agents
- ✅ Test coverage >80%, revert rate <5%
- ✅ Validation pipeline catches >95% of issues

### Dual-Trunk (Low-Trust)

**Agents commit to `agent-trunk`, humans review PRs to `main`.**

```bash
# Check current model
grep "trust_model" ops/trunk-config.yaml
# Output: trust_model: dual-trunk

# Agent trunk (validated, awaiting review)
AGENT_TRUNK="agent-trunk"
# Production trunk (reviewed and approved)
MAIN="main"
```

**Use when:**
- ⚠️ New to agent orchestration (<3 months)
- ⚠️ Regulatory requirements mandate human review
- ⚠️ High-risk domain (security, compliance, legal)
- ⚠️ Building confidence in validation pipeline

**Workflow:**
```
Agent commits → agent-trunk → CI validates
                      ↓
        Automated PR (2-4x daily) → main
                      ↓
            Human reviews and approves
                      ↓
                 Production
```

**For the rest of this guide:**
- If using **dual-trunk**: Replace `main` with `agent-trunk` in agent workflows
- Production deployment always happens from `main` in both models
- See [Technical Design](../../${DOC_ROOT}/architecture/design/trunk_based_development_technical_design.md#trust-model-variants-dual-trunk-implementation) for full implementation details

---

## For Agents: Quick Start

### 1. Before Starting Work

```bash
# Always start from latest trunk
git checkout main
git pull --rebase origin main

# Check for conflicts with other in-progress work
python ops/orchestration/task_age_checker.py --warn-only
```

### 2. Small Changes (Preferred)

**When:** Single-file edits, small refactors, documentation updates (<100 lines)

```bash
# Make change
vim ${DOC_ROOT}/architecture/adrs/ADR-019-trunk-based-development.md

# Validate locally
./validation/validate-all.sh

# Commit directly to trunk
git add ${DOC_ROOT}/architecture/adrs/ADR-019-trunk-based-development.md
git commit -m "docs(adr): clarify branch lifetime policy in ADR-019"
git push origin main
```

**Advantages:**
- ✅ Fastest path to integration
- ✅ No branch management overhead
- ✅ Immediate feedback from CI

### 3. Coordinated Changes (When Necessary)

**When:** Multi-file changes, coordinated refactors, complex features (>100 lines)

```bash
# Create short-lived branch
git checkout -b task/2025-11-30T0830-architect-adr019

# Make changes
vim ${DOC_ROOT}/architecture/adrs/ADR-019-trunk-based-development.md
vim ${DOC_ROOT}/architecture/design/trunk_based_development_technical_design.md
vim .github/agents/approaches/trunk-based-development.md

# Validate locally
./validation/validate-all.sh

# Commit and push
git add docs/ .github/agents/
git commit -m "docs: complete trunk-based development documentation suite"
git push origin task/2025-11-30T0830-architect-adr019

# Merge to trunk (rebase preferred)
git checkout main
git pull --rebase origin main
git rebase main task/2025-11-30T0830-architect-adr019
git checkout main
git merge --ff-only task/2025-11-30T0830-architect-adr019
git push origin main

# Clean up branch
git branch -d task/2025-11-30T0830-architect-adr019
git push origin --delete task/2025-11-30T0830-architect-adr019
```

**Target timeline:**
- Create branch: 0h
- Work complete: 2-4h
- Merged to trunk: 4-8h
- Maximum lifetime: 24h

### 4. Task Lifecycle Integration

Trunk-based development integrates naturally with file-based task orchestration:

**Task states and commits:**

```
new → assigned → in_progress → done
 ↓       ↓            ↓          ↓
 │       │         [commits]     │
 │       │            │          │
 └───────┴────────────┴──────────┘
         All on trunk
```

**Example task workflow:**

```bash
# 1. Assign task (commit to trunk)
mv work/inbox/task.yaml work/assigned/architect/
git add work/
git commit -m "task(architect): assign trunk-based development documentation"
git push origin main

# 2. Start task (commit to trunk)
sed -i 's/status: assigned/status: in_progress/' work/assigned/architect/task.yaml
git add work/assigned/architect/task.yaml
git commit -m "task(architect): start trunk-based development documentation"
git push origin main

# 3. Create artifacts incrementally (multiple commits to trunk)
git add ${DOC_ROOT}/architecture/adrs/ADR-019-trunk-based-development.md
git commit -m "docs(adr): add ADR-019 trunk-based development"
git push origin main

git add ${DOC_ROOT}/architecture/design/trunk_based_development_technical_design.md
git commit -m "docs(design): add technical design for trunk-based development"
git push origin main

git add .github/agents/approaches/trunk-based-development.md
git commit -m "docs(approach): add trunk-based development approach guide"
git push origin main

# 4. Complete task (commit to trunk)
sed -i 's/status: in_progress/status: done/' work/assigned/architect/task.yaml
# Add result block to task.yaml
mv work/assigned/architect/task.yaml work/done/architect/
git add work/
git commit -m "task(architect): complete trunk-based development documentation"
git push origin main
```

### 5. Validation Checklist

Before every commit, ensure:

- [ ] Pre-commit hooks pass (formatting, linting, basic validation)
- [ ] Unit tests pass (`pytest tests/unit/`)
- [ ] Acceptance tests pass (if applicable)
- [ ] Task schemas valid (`python validation/validate-task-schema.py`)
- [ ] No conflicts with other in-progress work
- [ ] Commit message follows conventions

### 6. Conflict Avoidance

**Check for conflicts before starting:**

```bash
# List all in-progress tasks and their artifacts
python ops/orchestration/list-in-flight-artifacts.py

# Example output:
# In-flight artifacts:
#   docs/REPO_MAP.md (structural, 2h ago)
#   ${DOC_ROOT}/architecture/adrs/ADR-020-*.md (architect, 1h ago)
#   .github/workflows/validation.yml (build-automation, 30m ago)
```

**If conflict detected:**

1. **Wait:** Let other agent finish (preferred if <1h remaining)
2. **Coordinate:** Contact other agent to split work
3. **Serialize:** Update task to indicate dependency, work on something else
4. **Override:** Only if urgent and you're confident in merge

### 7. Branch Age Warnings

Task age checker monitors branch age:

```bash
# Check your branch age
python ops/orchestration/branch_age_checker.py $(git branch --show-current)

# Example output:
# Branch 'task/2025-11-30T0830-architect-adr019' age: 3.2 hours
# Status: ✅ OK (threshold: 8h warning, 24h maximum)
```

**If age >8h:**
- ⚠️ Warning: Merge soon
- Review changes, rebase on trunk, merge

**If age >24h:**
- ❗ Maximum exceeded
- Merge immediately or abandon
- If blocked, ask for help

---

## For Humans: Developer Guide

### Daily Workflow

**Morning:**

```bash
# Start day with fresh trunk
git checkout main
git pull --rebase origin main

# Check system status
python ops/orchestration/task_age_checker.py
python ops/dashboards/generate-dashboard.py --view
```

**During work:**

```bash
# Pull frequently (every 30-60 minutes)
git pull --rebase origin main

# Commit frequently (every 30-60 minutes)
git add <files>
git commit -m "<message>"
git push origin main
```

**Before leaving:**

```bash
# Ensure no uncommitted work
git status

# If work incomplete, use feature flag or finish tomorrow
# DO NOT leave long-lived branch overnight
```

### Handling Incomplete Work

**Option 1: Feature flag (preferred)**

```python
# Hide incomplete feature behind flag
from ops.common.feature_flags import FeatureFlags

@FeatureFlags.require("new_feature")
def incomplete_feature():
    # Work in progress
    pass

# Enable in development only
# FEATURE_NEW_FEATURE=true python script.py
```

**Option 2: Finish tomorrow**

```bash
# Commit work-in-progress with clear marker
git add <files>
git commit -m "WIP: partial implementation of X (will complete tomorrow)"
git push origin main

# Next day: continue on trunk
git checkout main
git pull --rebase origin main
# Continue work...
```

**Option 3: Short-lived branch (last resort)**

```bash
# Create branch for overnight work
git checkout -b task/my-work
git add <files>
git commit -m "WIP: partial implementation"
git push origin task/my-work

# Next day: rebase and merge quickly
git checkout main
git pull --rebase origin main
git checkout task/my-work
git rebase main
git checkout main
git merge --ff-only task/my-work
git push origin main
git branch -d task/my-work
git push origin --delete task/my-work
```

### Revert Procedures

**When to revert:**

- CI fails and fix not obvious
- Bug discovered in production
- Change breaks integration tests
- Merge conflict resolution incorrect

**How to revert:**

```bash
# Simple revert (single commit)
git revert <bad-commit-sha>
git push origin main

# Revert range (multiple commits)
git revert <first-bad>^..<last-bad>
git push origin main

# Emergency revert (bypass CI)
git revert <bad-commit-sha>
git push origin main --no-verify
# Then fix CI afterward
```

**Post-revert:**

1. Investigate root cause
2. Fix issue in new commit
3. Re-apply change
4. Document in revert commit message

### Merge Conflict Resolution

**Minimize conflicts:**

- Pull frequently (`git pull --rebase origin main`)
- Keep changes small and focused
- Coordinate on shared files (check task artifacts)

**Resolve conflicts:**

```bash
# Pull with rebase
git pull --rebase origin main

# If conflicts occur
# 1. Fix conflicts in editor
vim <conflicted-file>

# 2. Mark resolved
git add <conflicted-file>

# 3. Continue rebase
git rebase --continue

# 4. Validate after rebase
./validation/validate-all.sh
pytest tests/

# 5. Push
git push origin main
```

### Ship/Show/Ask Pattern

Trunk-based development uses flexible review patterns:

**Ship:** Commit directly to trunk
- Small changes (<50 lines)
- Documentation updates
- Obvious bug fixes
- Test additions
- Configuration tweaks

**Show:** Commit to trunk, notify for async review
- Medium changes (50-200 lines)
- Refactorings
- New features with tests
- Design changes

**Ask:** Short-lived branch with review before merge
- Large changes (>200 lines)
- Breaking changes
- Security-sensitive changes
- Architectural decisions

```bash
# Ship (no review)
git add <file>
git commit -m "fix: correct typo in ADR-019"
git push origin main

# Show (async review)
git add <files>
git commit -m "refactor: simplify task age checker logic"
git push origin main
# Post in chat: "Refactored task age checker, please review when convenient"

# Ask (pre-merge review)
git checkout -b task/breaking-change
git add <files>
git commit -m "feat: redesign task lifecycle state machine"
git push origin task/breaking-change
# Create PR, request review, wait for approval
# Then merge with fast-forward
```

---

## GitHub-Specific Integration

### Branch Protection Setup

**Configure main branch protection:**

1. Go to repository **Settings** > **Branches**
2. Add rule for `main` branch:
   - ✅ Require status checks to pass before merging
     - Required checks: `validation`, `unit-tests`, `acceptance-tests`
   - ✅ Require branches to be up to date before merging
   - ✅ Include administrators (enforce for everyone)
   - ✅ Require linear history (no merge commits)
   - ❌ Require pull request reviews (optional, use Ship/Show/Ask instead)
   - ✅ Do not allow bypassing the above settings
   - ✅ Do not allow force pushes
   - ✅ Do not allow deletions

### GitHub Actions Integration

**Required workflows:**

- `.github/workflows/trunk-validation.yml` - Runs on every push to main
- `.github/workflows/branch-cleanup.yml` - Cleans up stale branches
- `.github/workflows/trunk-health.yml` - Calculates trunk health metrics

**Status checks:**

All commits to `main` must pass:
- `validation` - Task schema, directory structure, naming conventions
- `unit-tests` - Unit test suite with coverage
- `acceptance-tests` - Acceptance test suite
- `linting` - Code style and formatting
- `documentation` - Template and consistency checks

### Auto-Cleanup

GitHub Actions automatically:
- Warns on branches >8h old
- Comments on PRs for branches >24h old
- Deletes experiment branches after 24h
- Updates trunk health dashboard

---

## Generic VCS Implementation

Trunk-based development works on any Git-based VCS:

### GitLab

```yaml
# .gitlab-ci.yml
trunk_validation:
  stage: validate
  script:
    - ./validation/validate-all.sh
    - pytest tests/unit/
    - pytest tests/acceptance/
  only:
    - main
    - merge_requests

branch_age_check:
  stage: validate
  script:
    - python ops/orchestration/branch_age_checker.py $CI_COMMIT_REF_NAME
  only:
    - merge_requests
```

**Branch protection:**
- Settings > Repository > Protected Branches
- Protect `main` branch
- Require pipeline success

### Bitbucket

```yaml
# bitbucket-pipelines.yml
pipelines:
  branches:
    main:
      - step:
          name: Trunk Validation
          script:
            - ./validation/validate-all.sh
            - pytest tests/
  pull-requests:
    '**':
      - step:
          name: Branch Age Check
          script:
            - python ops/orchestration/branch_age_checker.py $BITBUCKET_BRANCH
```

**Branch protection:**
- Repository settings > Branch permissions
- Protect `main` branch
- Require builds to pass

### Gitea

```yaml
# .gitea/workflows/trunk-validation.yml
name: Trunk Validation
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: ./validation/validate-all.sh
      - run: pytest tests/
```

**Branch protection:**
- Settings > Branches > Protected Branches
- Add `main` branch
- Require status checks

---

## Monitoring and Metrics

### Trunk Health Dashboard

Monitor trunk stability:

```bash
# Generate dashboard
python ops/dashboards/generate-dashboard.py --include-trunk-health

# View in terminal
cat work/reports/trunk-health-dashboard.md

# Or open in browser
python -m http.server 8000 &
open http://localhost:8000/work/reports/trunk-health-dashboard.html
```

**Key metrics:**

- **Commit frequency:** >10 commits/day (good), <5 commits/day (warning)
- **Revert rate:** <5% (good), >10% (concerning)
- **Test pass rate:** >95% (good), <90% (action needed)
- **Time to fix:** <15 minutes (good), >1 hour (process issue)
- **Trunk stability:** >95% (good), <90% (rollback consideration)

### Alerts

**Automated alerts trigger on:**

- Branch age >8h (warning)
- Branch age >24h (error)
- Trunk stability <90% for >1 day
- Revert rate >10% for >1 week
- CI failure rate >20%

**Alert destinations:**

- GitHub PR comments (branch age)
- Slack/Discord notifications (trunk health)
- Dashboard warnings (metrics)
- Email digest (daily summary)

---

## Conflict Avoidance Strategies

### 1. Task Artifact Declarations

Declare artifacts in task YAML:

```yaml
id: 2025-11-30T0830-architect-adr019
agent: architect
status: in_progress
artefacts:
  - ${DOC_ROOT}/architecture/adrs/ADR-019-trunk-based-development.md
  - ${DOC_ROOT}/architecture/design/trunk_based_development_technical_design.md
  - .github/agents/approaches/trunk-based-development.md
```

**Pre-commit check:**

```bash
# Before committing, check for conflicts
python ops/orchestration/check-artifact-conflicts.py

# Example output:
# ⚠️  Conflict detected!
# The following artifacts are already being modified:
#   - ${DOC_ROOT}/architecture/adrs/ADR-019-trunk-based-development.md
#     by: architect (task 2025-11-30T0830-architect-adr019, 1.5h ago)
#
# Recommendation:
#   Wait for task to complete or coordinate with agent
```

### 2. Path Conventions (ADR-004)

Use predictable paths:

- Agent-specific directories: `work/assigned/<agent>/`
- Timestamped task files: `YYYY-MM-DDTHHMM-<agent>-<slug>.yaml`
- Agent work logs: `work/reports/logs/<agent>/`

**Benefit:** Reduces accidental same-file edits

### 3. Task Age Monitoring

Detect stale work:

```bash
# Check for stale tasks (>24h old)
python ops/orchestration/task_age_checker.py --threshold 24

# Example output:
# Task Age Warning Report
# ======================================================================
# Threshold: 24 hours
#
# ⚠️  Found 2 stale task(s):
#
# State: in_progress (2 task(s))
# ----------------------------------------------------------------------
#   [⚠️  26.3h]        architect | 2025-11-29T0600-architect-adr018
#                Multi-Repository Orchestration Strategy
#                File: work/assigned/architect/2025-11-29T0600-architect-adr018.yaml
#
# Recommendation:
#   - Review stale tasks for outdated context
#   - Update task specifications if repository has changed
#   - Consider moving very old tasks (>48h) to archive
```

### 4. Communication Channels

**In-task coordination:**

```yaml
# Add coordination notes to task file
id: 2025-11-30T0830-architect-adr019
agent: architect
status: in_progress
coordination:
  blocked_by: []
  blocks: [2025-11-30T0845-writer-proofread-adr019]
  notes: "Will complete by 10:00 UTC, then handoff to writer for proofreading"
```

**Cross-agent handoffs:**

```markdown
# ${WORKSPACE_ROOT}/collaboration/HANDOFFS.md

## Active Handoffs

| From       | To     | Artifact                               | Status      | ETA        |
|------------|--------|----------------------------------------|-------------|------------|
| architect  | writer | ADR-019 trunk-based development        | in_progress | 10:00 UTC  |
| structural | lexical| REPO_MAP.md                            | pending     | 14:00 UTC  |
```

### 5. Small Batch Sizes

**Prefer small, focused changes:**

- ✅ Single ADR per commit
- ✅ Single bug fix per commit
- ✅ Single refactor per commit

**Avoid large batches:**

- ❌ Multiple ADRs in one commit
- ❌ Feature + refactor + docs in one commit
- ❌ Unrelated changes bundled together

**Benefit:** Smaller changes = fewer conflicts, easier reverts

---

## Troubleshooting

### "My branch is >24h old, what do I do?"

**Option 1: Merge immediately**

```bash
# Rebase on trunk
git checkout main
git pull --rebase origin main
git checkout <your-branch>
git rebase main

# Resolve any conflicts
# Fix conflicts, then:
git add <files>
git rebase --continue

# Validate
./validation/validate-all.sh
pytest tests/

# Merge
git checkout main
git merge --ff-only <your-branch>
git push origin main

# Cleanup
git branch -d <your-branch>
git push origin --delete <your-branch>
```

**Option 2: Abandon and restart**

```bash
# If work is outdated or no longer needed
git checkout main
git branch -D <your-branch>
git push origin --delete <your-branch>

# Create new task with updated context
# Start fresh on trunk
```

### "CI failed on my commit, what do I do?"

**Step 1: Assess severity**

- Minor issue (formatting, linting): Fix immediately
- Test failure: Fix within 15 minutes or revert
- Critical failure (security, data loss): Revert immediately

**Step 2: Fix or revert**

```bash
# Quick fix (if obvious)
git add <files>
git commit -m "fix: correct linting issue from previous commit"
git push origin main

# Revert (if fix not obvious)
git revert HEAD
git push origin main
# Then fix in new commit later
```

**Step 3: Learn and improve**

- Update pre-commit hooks to catch issue locally
- Add test to prevent regression
- Document in commit message

### "Multiple agents editing same file"

**Prevention:**

- Check in-flight artifacts before starting
- Declare artifacts in task YAML
- Use path conventions (separate directories)

**Resolution:**

```bash
# Pull latest trunk
git pull --rebase origin main

# Resolve conflicts manually
vim <conflicted-file>

# Mark resolved
git add <conflicted-file>
git rebase --continue

# Validate and push
./validation/validate-all.sh
git push origin main
```

### "Trunk is unstable (tests failing)"

**Immediate action:**

```bash
# Identify breaking commit
git bisect start
git bisect bad HEAD
git bisect good <last-known-good>
# Test at each step until bad commit found

# Revert breaking commit
git revert <bad-commit>
git push origin main
```

**Follow-up:**

- Investigate root cause
- Add test to prevent recurrence
- Fix issue in new commit
- Consider improving CI checks

---

## Best Practices Summary

### Do's ✅

- ✅ Commit frequently (multiple times per day)
- ✅ Pull frequently (every 30-60 minutes)
- ✅ Keep changes small (<100 lines preferred)
- ✅ Run validation locally before pushing
- ✅ Use feature flags for incomplete work
- ✅ Revert quickly if CI fails
- ✅ Communicate when editing shared files
- ✅ Monitor trunk health metrics
- ✅ Merge branches within 24h

### Don'ts ❌

- ❌ Leave branches alive overnight (unless necessary)
- ❌ Push untested changes to trunk
- ❌ Bundle unrelated changes in one commit
- ❌ Force-push to trunk (protected by rules)
- ❌ Ignore CI failures
- ❌ Create long-lived feature branches
- ❌ Work on trunk without pulling first
- ❌ Skip pre-commit hooks

### Guidelines ⚖️

- **Branch lifetime:** Target 4h, maximum 24h
- **Commit size:** Prefer <100 lines, maximum ~300 lines
- **Commit frequency:** Multiple times per day
- **Pull frequency:** Every 30-60 minutes
- **CI feedback:** Fix or revert within 15 minutes
- **Test coverage:** Maintain >80% (target: >90%)
- **Revert rate:** Keep <5%

---

## Related Documentation

- [ADR-019: Adopt Trunk-Based Development](../../${DOC_ROOT}/architecture/adrs/ADR-019-trunk-based-development.md)
- [Technical Design: Trunk-Based Development](../../${DOC_ROOT}/architecture/design/trunk_based_development_technical_design.md)
- [ADR-003: Task Lifecycle and State Management](../../${DOC_ROOT}/architecture/adrs/ADR-003-task-lifecycle-state-management.md)
- [ADR-004: Work Directory Structure](../../${DOC_ROOT}/architecture/adrs/ADR-004-work-directory-structure.md)
- [ADR-012: Default to ATDD + TDD for Code Changes](../../${DOC_ROOT}/architecture/adrs/ADR-012-test-driven-defaults.md)

---

**Version:** 1.0.0  
**Status:** Active  
**Last updated:** 2025-11-30  
**Maintained by:** Architect Alphonso
