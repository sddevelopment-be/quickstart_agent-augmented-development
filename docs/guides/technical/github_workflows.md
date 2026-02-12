# GitHub Workflows Guide

**Version:** 2.0.0  
**Last Updated:** 2026-02-12  
**Purpose:** Automated CI/CD pipelines for quality assurance  
**Audience:** Maintainers reviewing or modifying GitHub Actions workflows (see `docs/audience/process_architect.md`).

---

## Overview

This repository uses GitHub Actions workflows to automatically test and validate code changes. The workflows ensure code quality, test coverage, and compliance with project standards.

**Major Update (2026-02-12):** Workflows have been consolidated into a single canonical build validation pipeline. See [CONSOLIDATION.md](../../../.github/workflows/CONSOLIDATION.md) for migration details.

---

## Primary Build Workflow

### Build Validation (Consolidated) (`validation-enhanced.yml`)

**Trigger:** Runs on all pull requests and pushes to `main` branch

**Purpose:** Comprehensive quality validation and testing pipeline

**What it does:**

#### Stage 1: Code Quality (5 min timeout)
- **Black formatting check:** Ensures Python code formatting standards
- **Ruff linting check:** Detects code quality issues and style violations
- **Outcome:** Blocks build if quality checks fail

#### Stage 2: Unit & Integration Tests (10 min timeout)
- Runs comprehensive test suite across all test directories
- Generates multiple coverage formats (XML, JSON, HTML)
- Parallel test execution with `pytest-xdist`
- Uploads JUnit XML test results
- Uploads coverage reports as artifacts (30-day retention)
- **Outcome:** Blocks build if any tests fail

#### Stage 3: Work Directory Validation (5 min timeout)
- **Structure validation:** Validates work directory organization
- **Schema validation:** Validates task YAML files against schemas
- **Naming validation:** Ensures task naming conventions
- **E2E tests:** Runs orchestration end-to-end tests (if available)
- **Error reporting:** Generates structured error reports (JSON/markdown)
- **PR comments:** Posts validation summary as PR comment
- **Outcome:** Blocks build if validations fail

#### Stage 4: SonarQube (independent)
- Code quality scanning with SonarQube
- Runs independently without blocking other jobs

**Typical workflow:**
```
Push to branch or create PR
  ↓
Code Quality ✅ (Black + Ruff)
  ↓
Unit & Integration Tests ✅ (All tests with coverage)
  ↓
Work Directory Validation ✅ (Structure + Schema + Naming + E2E)
  ↓
SonarQube Analysis ✅ (Independent)
  ↓
✅ Build passes - PR ready to merge
OR
❌ Build fails - fix issues and retry
```

**How to view:**
1. Open your pull request or go to **Actions** tab
2. Click on "Build Validation (Consolidated)" workflow
3. View job-by-job execution logs
4. Download artifacts (coverage reports, error reports) from workflow run

**Job Dependencies:**
```
code-quality
  └── unit-tests
       └── validate
            └── (PR comment with results)

sonarqube (independent, no dependencies)
```

---

## Specialized Workflows

### Workflow Validation (`workflow-validation.yml`)
**Trigger:** Changes to `.github/workflows/` or `.github/actions/`  
**Purpose:** YAML syntax and GitHub Actions best practices validation  
**What it does:** yamllint + actionlint checks

### Copilot Setup (`copilot-setup.yml`)
**Trigger:** Manual (workflow_dispatch)  
**Purpose:** Install CLI tooling (rg, fd, ast-grep, jq, yq, fzf)

### Diagram Rendering (`diagram-rendering.yml`)
**Trigger:** Push with `.puml` file changes  
**Purpose:** Generate PNG diagrams from PlantUML sources

### Orchestration (`orchestration.yml`)
**Trigger:** Cron schedule or manual  
**Purpose:** Automated agent orchestration workflows

### Update README (`update_readme.yml`)
**Trigger:** Push to main  
**Purpose:** Automated README updates

### Doctrine-specific Workflows
- `doctrine-dependency-validation.yml`: Validate doctrine dependencies
- `doctrine-glossary-maintenance.yml`: Maintain glossary consistency
- `glossary-update-pr.yml`: Automated glossary PR creation

### Release (`release-packaging.yml`)
**Trigger:** Manual or tag push  
**Purpose:** Package and publish releases

### Validate Prompts (`validate-prompts.yml`)
**Trigger:** Changes to prompt files  
**Purpose:** Validate prompt template schemas

---

## Artifacts

### validation-enhanced.yml Artifacts
- **coverage-reports:** Coverage data in XML, JSON, and HTML formats (30-day retention)
- **test-results:** JUnit XML test results (30-day retention)
- **error-reports:** Structured validation error reports (via error-summary action)

**How to download artifacts:**
1. Go to workflow run in Actions tab
2. Scroll to "Artifacts" section at bottom
3. Click artifact name to download ZIP

---

## Timeouts

| Workflow | Job | Timeout |
|----------|-----|---------|
| validation-enhanced | code-quality | 5 minutes |
| validation-enhanced | unit-tests | 10 minutes |
| validation-enhanced | validate | 5 minutes |
| validation-enhanced | sonarqube | N/A |

---

## Failure Scenarios & Remediation

### Code Quality Failure

**Symptom:** Black or Ruff checks fail

**Fix:**
```bash
# Format code with Black
black src/ tests/ framework/

# Fix linting issues with Ruff
ruff check src/ tests/ framework/ --fix

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

### Mutation Test Issues```

### Test Failures

**Symptom:** Unit or integration tests fail

**Fix:**
```bash
# Run tests locally to reproduce
python -m pytest tests/ -v --tb=short

# Run specific failing test
python -m pytest tests/path/to/test_file.py::test_function -vv

# Check test output for assertion details
# Fix the code or update the test
```

### Validation Failures

**Symptom:** Work directory structure, schema, or naming validation fails

**Fix:**
```bash
# Structure validation
bash tools/validators/validate-work-structure.sh

# Schema validation
python tools/validators/validate-task-schema.py work/path/to/file.yaml

# Naming validation  
bash tools/validators/validate-task-naming.sh

# Fix issues identified in validation output
```

---

## Local Testing

Before pushing, run the same checks locally:

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Code quality checks
black src/ tests/ framework/
ruff check src/ tests/ framework/ --fix

# Run comprehensive test suite
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ \
  --cov=src \
  --cov=framework \
  --cov-report=term-missing:skip-covered \
  --cov-report=html

# View coverage report
open htmlcov/index.html  # or xdg-open on Linux

# Validation checks
bash tools/validators/validate-work-structure.sh
bash tools/validators/validate-task-naming.sh
```

---

## Workflow Customization

### Changing Python Version

Edit `validation-enhanced.yml`:
```yaml
- name: Setup Python environment
  uses: ./.github/actions/setup-python-env
  with:
    python-version: '3.11'  # Change here
```

### Adding More Tests

Workflows automatically discover and run all test files matching `test_*.py` in the `tests/` directory tree.

Just add your test file:
```bash
tests/
  ├── test_task_utils.py
  ├── orchestration/
  │   └── test_agent_orchestrator.py
  ├── framework/
  │   └── test_your_module.py  # Automatically discovered
  └── integration/
      └── test_integration.py    # Automatically discovered
```

### Adjusting Timeouts

If workflows timeout, increase limits in `validation-enhanced.yml`:
```yaml
jobs:
  unit-tests:
    timeout-minutes: 15  # Increase from 10 if needed
```

---

## SonarQube Setup

SonarQube analysis is configured in the `validation-enhanced.yml` workflow but requires a SonarQube server and authentication token.

### Configuration

The workflow includes a `sonarqube` job that runs independently. To enable:

1. Set up SonarQube server (or use SonarCloud)
2. Add `SONAR_TOKEN` secret to GitHub repository settings
3. Update `sonarqube` job in `validation-enhanced.yml` with your configuration

---

## Best Practices

### ✅ Do

- Run tests locally before pushing
- Keep workflows fast (target: <15 min total)
- Review workflow failures before re-pushing
- Monitor test coverage trends
- Fix validation errors promptly

### ❌ Don't

- Push without running local tests
- Ignore linting/formatting violations
- Disable required checks to merge faster
- Merge PRs with failing quality gates
- Skip work directory validation fixes

---

## Monitoring

### Success Metrics

- **Test pass rate:** Should be 100%
- **Workflow duration:** Should be <15 minutes total
- **Coverage:** Target 85%+
- **Build success rate:** Target 95%+

### Health Indicators

✅ **Healthy:**
- All tests passing
- Workflows complete in <15 minutes
- No timeout issues
- Coverage stable or increasing

⚠️ **Needs Attention:**
- Occasional test failures
- Workflows taking 15-20 minutes
- Coverage declining slightly

❌ **Critical:**
- Frequent test failures
- Workflows timing out
- Coverage dropping significantly
- Validation errors accumulating

---

## Troubleshooting

### Workflow Won't Start

**Cause:** Workflow file syntax error or disabled workflow  
**Solution:** Check workflow YAML syntax, ensure workflow is not disabled

### Tests Pass Locally, Fail in CI

**Cause:** Environment differences  
**Solution:** 
- Check Python version match (should be 3.10)
- Verify all dependencies in requirements.txt
- Look for filesystem path assumptions
- Check for timing-dependent tests

### Workflow Stuck/Slow

**Cause:** Tests taking longer than expected  
**Solution:**
- Check test execution logs for slow tests
- Consider increasing timeout limits
- Optimize slow tests
- Use `pytest-xdist` for parallel execution (already enabled)

### Can't Download Artifacts

**Cause:** Artifact retention expired (30 days)  
**Solution:** Re-run workflow if needed, artifacts regenerate

### Validation Errors in PR Comment

**Cause:** Work directory structure/schema/naming issues  
**Solution:**
- Read error report in PR comment
- Download error-reports artifact for details
- Fix issues identified
- Re-run validation

---

## Maintenance

### Regular Tasks

**Weekly:**
- Review failed workflow runs
- Monitor test execution time trends
- Check coverage reports

**Monthly:**
- Update Python dependencies (requirements.txt)
- Update GitHub Actions versions
- Review and optimize slow tests

**Quarterly:**
- Evaluate new testing tools
- Review workflow efficiency
- Update documentation

---

## Additional Resources

- **Workflow Consolidation:** `.github/workflows/CONSOLIDATION.md`
- **Testing Guide:** `work/reports/metrics/TEST_COVERAGE.md`
- **Python Conventions:** `docs/styleguides/python_conventions.md`
- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **pytest Documentation:** https://docs.pytest.org/

---

## Version History

| Version | Date       | Changes                                              |
|---------|------------|------------------------------------------------------|
| 1.0.0   | 2025-11-29 | Initial workflow documentation                       |
| 2.0.0   | 2026-02-12 | Consolidated workflows into validation-enhanced.yml  |

---

**Maintained by:** Build Automation Team  
**Review Cycle:** After significant workflow changes
