# Python Development Setup Guide

**Audience:** Framework Developers, Software Engineers  
**Version:** 1.0.0  
**Last Updated:** 2025-12-01

## Overview

This guide walks you through setting up a Python development environment for working with the agentic framework (`framework/`) and operational automation scripts (`ops/`). You'll learn how to create an isolated Python environment, install dependencies, and validate your setup.

## Prerequisites

- **Python 3.10 or later** installed on your system
- **pip** (Python package installer, typically included with Python)
- **git** (for cloning and version control)
- Basic command-line familiarity

### Verify Python Installation

```bash
python --version
# or on some systems:
python3 --version
```

Expected output: `Python 3.10.x` or later.

If Python is not installed, download it from [python.org](https://www.python.org/downloads/) or use your system's package manager:

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# macOS (using Homebrew)
brew install python@3.10

# Windows (using Chocolatey)
choco install python
```

---

## What is a Virtual Environment?

A **virtual environment** is an isolated Python environment that allows you to install packages without affecting your system-wide Python installation or other projects.

### Why Use Virtual Environments?

1. **Isolation:** Each project has its own dependencies, preventing version conflicts
2. **Reproducibility:** Ensures everyone working on the project uses the same package versions
3. **Safety:** Avoids polluting your system Python with project-specific packages
4. **Flexibility:** Easy to delete and recreate if something goes wrong

### How Virtual Environments Work

When activated, a virtual environment:
- Creates a local `bin/` (or `Scripts/` on Windows) directory with Python executables
- Creates a `lib/` directory for installed packages
- Modifies your shell's `PATH` to prioritize the virtual environment's Python
- Keeps a record of installed packages in the environment

---

## Step 1: Clone the Repository

If you haven't already, clone the repository:

```bash
git clone https://github.com/sddevelopment-be/quickstart_agent-augmented-development.git
cd quickstart_agent-augmented-development
```

---

## Step 2: Create a Virtual Environment

Navigate to the project root and create a virtual environment named `.venv`:

```bash
# Create virtual environment
python -m venv .venv
```

**What this does:** Creates a `.venv/` directory inside the project repository containing an isolated Python installation.

**Note:** The `.venv` directory is already listed in `.gitignore` and won't be committed to version control.

**Alternative:** You can share the same virtual environment with other projects by placing it in a shared location. This will help you re-use the same technology stack for other projects. However, you lose some of the modularity and dependency-safety that we are striving towards. Unless you have a good reason to create a shared virtual environment, we recomend creating one for each repository.

---

## Step 3: Activate the Virtual Environment

Activation makes the virtual environment's Python and pip the default for your current shell session.

### Linux / macOS

```bash
source .venv/bin/activate
```

**HINT:** You can create an [alias](https://linuxize.com/post/how-to-create-bash-aliases/) in your `~/.bashrc` or `̉̉~/.bash_aliases` file to quickly activate this. e.g. `alias pyvenv='source .venv/bin/activate`.

### Windows (Command Prompt)

```cmd
.venv\Scripts\activate.bat
```

### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

**Note:** On Windows PowerShell, you may need to enable script execution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Verify Activation

After activation, your shell prompt should be prefixed with `(.venv)`:

```bash
(.venv) user@machine:~/quickstart_agent-augmented-development$
```

Verify you're using the virtual environment's Python:

```bash
which python    # Linux/macOS
# Expected: /path/to/project/.venv/bin/python

where python    # Windows
# Expected: C:\path\to\project\.venv\Scripts\python.exe
```

---

## Step 4: Upgrade pip

Ensure you have the latest version of pip:

```bash
python -m pip install --upgrade pip
```

---

## Step 5: Install Dependencies

The project has two dependency files:

1. **`requirements.txt`** - Core runtime dependencies (YAML parsing, JSON schema validation)
2. **`requirements-dev.txt`** - Development tools (testing, linting, formatting, mutation testing)

### Install Core Dependencies

```bash
pip install -r requirements.txt
```

### Install Development Dependencies and Framework Package

```bash
# Install development tools
pip install -r requirements-dev.txt

# Install framework in editable mode (REQUIRED)
pip install -e .
```

**What gets installed:**

- `pytest` and `pytest-cov` - Testing framework and coverage reporting
- `black` - Code formatter (enforces consistent style)
- `ruff` - Fast Python linter
- `mutmut` - Mutation testing tool
- `PyYAML` - YAML parsing (used by orchestration and validation scripts)
- `jsonschema` - JSON schema validation (used by OpenCode validator)
- `mypy` and `types-PyYAML` - Optional type checking

**Note:** The `pip install -e .` command is **critical** - it installs the project package in "editable" mode, creating symbolic links so the `framework` and `ops` packages become importable. Without this step, tests will fail with `ModuleNotFoundError`.

### Verify Installation

```bash
pip list
```

You should see all installed packages with their versions, including:

- `quickstart-agent-augmented-development` (with editable link to current directory)

---

## Step 6: Add Project to Python Path (Optional)

To import framework and ops modules from anywhere, add the project root to your `PYTHONPATH`:

### Linux / macOS (temporary, current session)

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Windows (temporary, current session)

```cmd
set PYTHONPATH=%PYTHONPATH%;%CD%
```

### Make it Permanent (Optional)

Add the export line to your shell profile:

```bash
# Linux/macOS - add to ~/.bashrc or ~/.zshrc
echo 'export PYTHONPATH="${PYTHONPATH}:/path/to/quickstart_agent-augmented-development"' >> ~/.bashrc

# Windows - use System Properties > Environment Variables
```

**Alternative:** Most IDEs (VS Code, PyCharm) automatically add the project root to `PYTHONPATH` when you open the folder.

---

## Validate Your Setup

Now verify everything is working correctly by running the test suite.

### 1. Run All Tests

```bash
python -m pytest validation/ -v
```

**Expected output:**

```
================= test session starts =================
platform linux -- Python 3.10.x, pytest-7.x.x
collected XX items

validation/test_agent_orchestrator.py::TestAgentOrchestrator::test_... PASSED
validation/test_orchestration_e2e.py::TestOrchestrationE2E::test_... PASSED
validation/framework/test_core.py::TestTaskStatus::test_task_status_values PASSED
validation/framework/test_core.py::TestAgentProfile::test_agent_profile_minimal_valid PASSED
validation/framework/test_execution.py::TestModelProvider::test_model_provider_values PASSED
validation/framework/test_interface.py::TestFrameworkClient::test_init_default_values PASSED
...

================= XX passed in X.Xs =================
```

### 2. Run Tests with Coverage

```bash
python -m pytest validation/ --cov=ops --cov=framework --cov-report=term-missing
```

This shows which lines of code are covered by tests.

### 3. Run Specific Test Modules

```bash
# Test framework only
python -m pytest validation/framework/ -v

# Test orchestration only
python -m pytest validation/test_agent_orchestrator.py -v

# Test a specific test class
python -m pytest validation/framework/test_core.py::TestTask -v
```

### 4. Verify Code Formatting

```bash
# Check if code follows Black style (no changes made)
python -m black ops/ framework/ --check

# Check if code follows Ruff linting rules
python -m ruff check ops/ framework/
```

### 5. Format Code (If Needed)

```bash
# Auto-format with Black
python -m black ops/ framework/

# Auto-fix Ruff issues
python -m ruff check ops/ framework/ --fix
```

### 6. Run Type Checking (Optional)

```bash
python -m mypy ops/ framework/ --ignore-missing-imports
```

### 7. Test Framework Imports

Verify you can import framework modules:

```bash
python -c "from framework.core import Task, Orchestrator; print('✓ Core imports OK')"
python -c "from framework.execution import ModelRouter; print('✓ Execution imports OK')"
python -c "from framework.interface import FrameworkClient; print('✓ Interface imports OK')"
python -c "from ops.orchestration.task_utils import TaskStatus; print('✓ Ops imports OK')"
```

### 8. Run a Sample Script

Execute a simple orchestration helper:

```bash
python ops/framework-core/template-status-checker.py --help
```

Expected output: Help text showing available options.

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'framework'`

**Solution:** Ensure you're in the project root directory and have set `PYTHONPATH`:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

Or run Python with the `-m` flag from the project root.

### Issue: `pip: command not found`

**Solution:** Use `python -m pip` instead of `pip`:

```bash
python -m pip install -r requirements.txt
```

### Issue: Tests fail with import errors

**Solution:** Ensure virtual environment is activated and all dependencies are installed:

```bash
source .venv/bin/activate  # or appropriate activation for your OS
pip install -r requirements.txt -r requirements-dev.txt
```

### Issue: Permission denied on Windows PowerShell

**Solution:** Enable script execution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Old package versions causing conflicts

**Solution:** Recreate the virtual environment:

```bash
# Deactivate current environment
deactivate

# Remove old environment
rm -rf .venv  # Linux/macOS
rmdir /s .venv  # Windows

# Create fresh environment
python -m venv .venv
source .venv/bin/activate  # or appropriate activation
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
```

---

## Next Steps

Once your setup is validated:

1. **Read the Framework README:** [`framework/README.md`](../../framework/README.md) for architecture and usage examples
2. **Explore Ops Scripts:** [`ops/README.md`](../../ops/README.md) for automation tooling
3. **Review Python Conventions:** [`docs/styleguides/python_conventions.md`](../styleguides/python_conventions.md) for coding standards
4. **Check ADRs:** [`docs/architecture/adrs/`](../architecture/adrs/) for architectural decisions
5. **Run Mutation Tests:** See [`validation/MUTATION_TESTING_QUICKSTART.md`](../../validation/MUTATION_TESTING_QUICKSTART.md)

---

## Deactivating the Virtual Environment

When you're done working, deactivate the virtual environment:

```bash
deactivate
```

Your shell prompt will return to normal, and `python` will refer to your system installation again.

---

## Quick Reference

### Common Commands

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Install framework in editable mode (REQUIRED)
pip install -e .

# Run all tests
python -m pytest validation/ -v

# Run tests with coverage
python -m pytest validation/ --cov=ops --cov=framework --cov-report=term-missing

# Format code
python -m black ops/ framework/

# Lint code
python -m ruff check ops/ framework/ --fix

# Deactivate virtual environment
deactivate
```

### Project Structure

```
quickstart_agent-augmented-development/
├── framework/              # Multi-tier agentic framework (Layer 0-3)
│   ├── core/              # Orchestration and governance (Layer 1)
│   ├── execution/         # Model routing and execution (Layers 2-3)
│   └── interface/         # User-facing APIs (Layer 0)
├── ops/                   # Operational automation scripts
│   ├── orchestration/     # Task orchestration and agent coordination
│   ├── framework-core/    # Framework utilities (directives, profiles)
│   ├── dashboards/        # Metrics collection and visualization
│   └── planning/          # Planning and issue management helpers
├── validation/            # Test suite
│   ├── framework/         # Framework-specific tests
│   └── fixtures/          # Test fixtures and data
├── requirements.txt       # Core runtime dependencies
├── requirements-dev.txt   # Development dependencies
└── pyproject.toml        # Python tooling configuration
```

---

## References

- [Python Virtual Environments Documentation](https://docs.python.org/3/library/venv.html)
- [pip User Guide](https://pip.pypa.io/en/stable/user_guide/)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Ruff Linter](https://docs.astral.sh/ruff/)
- [Framework README](../../framework/README.md)
- [Python Conventions Guide](../styleguides/python_conventions.md)

---

**Prepared by:** DevOps Danny  
**Mode:** `/analysis-mode`  
**Date:** 2025-12-01
