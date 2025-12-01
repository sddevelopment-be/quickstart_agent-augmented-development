# Python Setup Guide Documentation

**Date:** 2025-12-01  
**Agent:** DevOps Danny  
**Mode:** `/analysis-mode`  
**Status:** Complete

## Objective

Create comprehensive Python development setup documentation for framework developers and software engineers working with the `framework/` and `ops/` modules.

## Deliverable

Created `docs/HOW_TO_USE/python-setup.md` with complete setup instructions including:

### Content Structure

1. **Overview & Prerequisites**
   - Python 3.10+ requirement
   - Installation verification commands
   - Platform-specific installation instructions

2. **Virtual Environment Explanation**
   - What is a virtual environment
   - Why use them (isolation, reproducibility, safety, flexibility)
   - How they work (technical details)

3. **Step-by-Step Setup**
   - Clone repository
   - Create virtual environment (`.venv`)
   - Activate (Linux/macOS/Windows variants)
   - Upgrade pip
   - Install dependencies (requirements.txt + requirements-dev.txt)
   - Optional PYTHONPATH configuration

4. **Validate Your Setup Section**
   - Run full test suite
   - Run tests with coverage
   - Run specific test modules
   - Verify code formatting (Black)
   - Verify linting (Ruff)
   - Optional type checking (mypy)
   - Test framework imports
   - Run sample script

5. **Troubleshooting**
   - Common issues and solutions:
     - Module not found errors
     - pip command not found
     - Import errors
     - Permission issues (Windows PowerShell)
     - Package version conflicts

6. **Next Steps**
   - Links to framework README
   - Links to ops README
   - Python conventions guide
   - ADRs
   - Mutation testing guide

7. **Quick Reference**
   - Common commands
   - Project structure overview
   - Deactivation instructions

8. **References**
   - External documentation links
   - Internal project references

## Integration

Updated `docs/HOW_TO_USE/README.md` to:

- Add python-setup.md to Development Environment section
- Include setup step in all user journey sections:
  - New Users
  - Agent Developers
  - DevOps/Automation Engineers

## Features

✅ **Clear explanations** of virtual environment concepts  
✅ **Platform-specific commands** (Linux/macOS/Windows)  
✅ **Copy-pasteable examples** throughout  
✅ **Comprehensive validation** section with 8 verification steps  
✅ **Troubleshooting guide** with common issues  
✅ **Quick reference** for experienced users  
✅ **Cross-references** to related documentation

## Target Audiences

- **Framework Developers:** Working on `framework/core`, `framework/execution`, `framework/interface`
- **Software Engineers:** Contributing to `ops/orchestration`, `ops/dashboards`, `ops/planning`
- **Quality Engineers:** Running and extending `validation/` tests
- **DevOps Engineers:** Integrating Python scripts in CI/CD pipelines

## Validation Commands Included

```bash
# Full test suite
python -m pytest validation/ -v

# Coverage report
python -m pytest validation/ --cov=ops --cov=framework --cov-report=term-missing

# Specific tests
python -m pytest validation/framework/ -v

# Formatting check
python -m black ops/ framework/ --check

# Linting
python -m ruff check ops/ framework/

# Type checking
python -m mypy ops/ framework/ --ignore-missing-imports

# Import verification
python -c "from framework.core import Task; print('✓')"

# Sample script
python ops/framework-core/template-status-checker.py --help
```

## Files Modified

1. **Created:** `docs/HOW_TO_USE/python-setup.md` (400+ lines)
2. **Updated:** `docs/HOW_TO_USE/README.md` (added python-setup references in 4 locations)

## Compliance

✅ **Markdown formatting** (proper headings, code blocks, lists)  
✅ **Clear structure** with numbered sections  
✅ **Beginner-friendly** explanations  
✅ **Platform coverage** (Linux, macOS, Windows)  
✅ **Executable commands** ready to copy-paste  
✅ **Cross-referenced** with existing documentation

---

**Completion Status:** ✅ Python setup guide complete with comprehensive coverage for all target audiences.
