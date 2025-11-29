# GitHub Workflows Guide

**Version:** 1.0.0  
**Last Updated:** 2025-11-29  
**Purpose:** Automated CI/CD pipelines for quality assurance
**Audience:** Maintainers reviewing or modifying GitHub Actions workflows (see `docs/audience/process_architect.md`).

---

## Overview

This repository uses GitHub Actions workflows to automatically test and validate code changes. The workflows ensure code quality, test coverage, and compliance with project standards.

---

## Workflows

### 1. Test Ops Changes (`test-ops-changes.yml`)

**Trigger:** Runs on all branches when files in `ops/` directory change

**Purpose:** Quick feedback loop for automation script changes

**What it does:**
- Runs unit tests for `task_utils.py` (24 tests)
- Runs unit tests for `agent_orchestrator.py` (31 tests)
- Runs E2E orchestration tests (11 tests)
- Provides fast feedback (typically <5 minutes)

**Triggers:**
- Push to any branch with changes in:
  - `ops/**`
  - `validation/**`
  - `requirements.txt`
  - `requirements-dev.txt`
- Pull requests with changes in the same paths

**Typical workflow:**
```
Push changes to ops/ directory
  ↓
Workflow automatically runs
  ↓
Unit tests execute (55 tests)
  ↓
E2E tests execute (11 tests)
  ↓
Results reported in GitHub UI
```

**How to view:**
1. Go to **Actions** tab in GitHub
2. Click on "Test Ops Changes" workflow
3. View latest run for your branch

---

### 2. PR Quality Gate (`pr-quality-gate.yml`)

**Trigger:** Runs on pull requests to `main` branch

**Purpose:** Comprehensive quality validation before merging to mainline

**What it does:**

#### Stage 1: Code Quality
- Black formatting check
- Ruff linting check
- Ensures code style compliance

#### Stage 2: Unit Tests with Coverage
- Runs all 55 unit tests
- Generates coverage reports (XML, HTML)
- Uploads coverage artifacts

#### Stage 3: E2E Tests
- Runs all 11 E2E orchestration tests
- Validates complete workflow scenarios
- Tests integration between components

#### Stage 4: Mutation Testing
- Runs `mutmut` on orchestration code
- Introduces controlled bugs
- Validates test effectiveness
- Generates mutation score

#### Stage 5: SonarCloud (Placeholder)
- Currently displays setup instructions
- Ready for SonarCloud integration
- Downloads coverage reports for analysis

#### Stage 6: Quality Gate Summary
- Aggregates all check results
- Provides pass/fail decision
- Blocks merge if critical checks fail

**Typical workflow:**
```
Create PR to main
  ↓
Workflow automatically runs (parallel jobs)
  ↓
Code Quality ✅
Unit Tests ✅
E2E Tests ✅
Mutation Testing ✅
SonarCloud ⚠️ (not configured)
  ↓
Quality Gate Summary
  ↓
✅ PR ready to merge
OR
❌ PR blocked - fix issues
```

**How to view:**
1. Open your pull request
2. Scroll to "Checks" section
3. Click "Details" for any failing check
4. View step-by-step execution logs

---

## Job Dependencies

### test-ops-changes.yml

```
unit-tests (parallel)
  └── acceptance-tests (E2E)
```

### pr-quality-gate.yml

```
code-quality
  ├── unit-tests ──┬──> mutation-testing
  │               └──> sonarcloud
  └── e2e-tests ───┴──> mutation-testing
                       sonarcloud
                       
All → quality-gate-summary
```

---

## Required Secrets

### Current Setup
No secrets required - workflows use default GitHub tokens

### Future (SonarCloud)
- `SONAR_TOKEN`: SonarCloud authentication token

---

## Artifacts

### test-ops-changes.yml
No artifacts (fast feedback only)

### pr-quality-gate.yml
- **Coverage reports:** `coverage-reports` (XML + HTML, 30 days)
- **Mutation results:** `mutation-test-results` (logs + cache, 30 days)

**How to download artifacts:**
1. Go to workflow run
2. Scroll to "Artifacts" section
3. Click artifact name to download

---

## Timeouts

| Workflow | Job | Timeout |
|----------|-----|---------|
| test-ops-changes | unit-tests | 5 minutes |
| test-ops-changes | acceptance-tests | 5 minutes |
| pr-quality-gate | code-quality | 5 minutes |
| pr-quality-gate | unit-tests | 5 minutes |
| pr-quality-gate | e2e-tests | 5 minutes |
| pr-quality-gate | mutation-testing | 30 minutes |
| pr-quality-gate | sonarcloud | 10 minutes |

---

## Failure Scenarios

### Code Quality Failure

**Symptom:** Black or Ruff checks fail

**Fix:**
```bash
# Format code
black validation/ ops/scripts/

# Fix linting issues
ruff check validation/ ops/scripts/ --fix

# Commit and push
git add .
git commit -m "Fix code formatting and linting"
git push
```

### Unit Test Failure

**Symptom:** Unit tests fail

**Fix:**
```bash
# Run tests locally
python -m pytest validation/test_task_utils.py -v
python -m pytest validation/test_agent_orchestrator.py -v

# Fix failing tests
# Commit and push
```

### E2E Test Failure

**Symptom:** E2E orchestration tests fail

**Fix:**
```bash
# Run E2E tests locally
python -m pytest validation/test_orchestration_e2e.py -v

# Fix workflow issues
# Commit and push
```

### Mutation Test Issues

**Symptom:** Many mutations survive

**Action:** Not a blocker, but investigate
```bash
# Run locally
mutmut run
mutmut results

# See what mutations survived
mutmut show <id>

# Write tests to catch them
```

---

## Local Testing

Before pushing, run the same checks locally:

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Code quality
black validation/ ops/scripts/
ruff check validation/ ops/scripts/ --fix

# Unit tests
python -m pytest validation/test_task_utils.py validation/test_agent_orchestrator.py -v

# E2E tests
python -m pytest validation/test_orchestration_e2e.py -v

# Coverage (optional)
python -m pytest validation/ --cov=ops/scripts/orchestration --cov-report=term-missing

# Mutation testing (optional, takes time)
mutmut run
mutmut results
```

---

## Workflow Customization

### Changing Python Version

Edit workflow files:
```yaml
- name: Setup Python environment
  uses: ./.github/actions/setup-python-env
  with:
    python-version: '3.11'  # Change here
```

### Adding More Tests

Workflows automatically detect test files matching `test_*.py` in `validation/`.

Just add your test file:
```bash
validation/
  ├── test_task_utils.py
  ├── test_agent_orchestrator.py
  ├── test_orchestration_e2e.py
  └── test_your_new_module.py  # Automatically runs
```

### Adjusting Timeouts

If workflows timeout, increase limits:
```yaml
jobs:
  your-job:
    timeout-minutes: 10  # Increase this
```

---

## SonarCloud Setup

To enable SonarCloud analysis:

### 1. Sign Up
- Go to https://sonarcloud.io/
- Sign in with GitHub account
- Select organization

### 2. Import Repository
- Click "+" → "Analyze new project"
- Select this repository
- Complete setup wizard

### 3. Add Secret
- Go to GitHub repository → Settings → Secrets
- Add new secret: `SONAR_TOKEN`
- Copy token from SonarCloud

### 4. Create Configuration
Create `sonar-project.properties`:
```properties
sonar.projectKey=sddevelopment-be_quickstart_agent-augmented-development
sonar.organization=sddevelopment-be

sonar.sources=ops/scripts/
sonar.tests=validation/

sonar.python.version=3.10
sonar.python.coverage.reportPaths=coverage.xml

sonar.exclusions=**/*_test.py,**/test_*.py
sonar.test.inclusions=**/test_*.py
```

### 5. Uncomment Workflow Step
In `pr-quality-gate.yml`, uncomment:
```yaml
- name: SonarCloud Scan
  uses: SonarSource/sonarcloud-github-action@master
  # ... (see workflow file)
```

### 6. Test
Create a PR and verify SonarCloud runs successfully.

---

## Best Practices

### ✅ Do

- Run tests locally before pushing
- Keep workflows fast (current: <5 min for quick tests)
- Review workflow failures before re-pushing
- Update timeout limits if legitimate slowdown
- Monitor mutation testing results

### ❌ Don't

- Push without running local tests
- Ignore mutation testing results
- Disable required checks to merge faster
- Commit formatting violations
- Merge PRs with failing quality gates

---

## Monitoring

### Success Metrics

- **Test pass rate:** Should be 100%
- **Workflow duration:** Should be <10 minutes
- **Mutation score:** Target 95%+
- **Coverage:** Target 95%+

### Health Indicators

✅ **Healthy:**
- All tests passing
- Workflows complete in <10 minutes
- No timeout issues
- Mutation score >90%

⚠️ **Needs Attention:**
- Occasional test failures
- Workflows taking 10-15 minutes
- Mutation score 80-90%

❌ **Critical:**
- Frequent test failures
- Workflows timing out
- Mutation score <80%
- Coverage dropping

---

## Troubleshooting

### Workflow Won't Start

**Cause:** Path filter doesn't match  
**Solution:** Check that changed files match path patterns in workflow

### Tests Pass Locally, Fail in CI

**Cause:** Environment differences  
**Solution:** 
- Check Python version match
- Verify all dependencies installed
- Look for filesystem path assumptions

### Workflow Stuck/Slow

**Cause:** Usually mutation testing  
**Solution:**
- Check mutation test step logs
- Consider increasing timeout
- Run mutation tests weekly instead of every PR

### Can't Download Artifacts

**Cause:** Artifact retention expired  
**Solution:** Artifacts kept for 30 days; re-run workflow if needed

---

## Maintenance

### Regular Tasks

**Weekly:**
- Review mutation test results
- Check for workflow timeouts
- Monitor test execution time

**Monthly:**
- Review and update Python dependencies
- Update GitHub Actions versions
- Clean old workflow runs

**Quarterly:**
- Review and optimize slow tests
- Update documentation
- Evaluate new testing tools

---

## Additional Resources

- **Testing Guide:** `validation/TEST_COVERAGE.md`
- **Mutation Testing:** `docs/HOW_TO_USE/mutation_testing.md`
- **Python Conventions:** `docs/styleguides/python_conventions.md`
- **GitHub Actions Docs:** https://docs.github.com/en/actions

---

## Version History

| Version | Date       | Changes                          |
|---------|------------|----------------------------------|
| 1.0.0   | 2025-11-29 | Initial workflow documentation   |

---

**Maintained by:** Build Automation Team  
**Review Cycle:** After significant workflow changes
