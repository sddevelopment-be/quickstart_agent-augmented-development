# Repository Dependencies

_Version: 1.0.0_  
_Generated: 2025-11-23T22:36:42Z_  
_Agent: Bootstrap Bill_  
_Task: 2025-11-23T2157-bootstrap-bill-repomap-update_

## Overview

This document catalogs all external dependencies, tools, and requirements for the quickstart_agent-augmented-development repository. It serves as a reference for environment setup, CI/CD configuration, and agent tooling.

## Table of Contents

1. [Python Dependencies](#python-dependencies)
2. [CLI Tools](#cli-tools)
3. [GitHub Actions Dependencies](#github-actions-dependencies)
4. [Agent Tooling Requirements](#agent-tooling-requirements)
5. [Runtime Requirements](#runtime-requirements)
6. [Development Dependencies](#development-dependencies)
7. [Optional Dependencies](#optional-dependencies)

---

## Python Dependencies

### Core Requirements

**Source:** `requirements.txt`

| Package | Version | Purpose | Used By |
|---------|---------|---------|---------|
| PyYAML | >=6.0 | YAML parsing | Orchestration, validation scripts |
| pytest | >=7.0 | Testing framework | E2E test suite |
| jsonschema | >=4.0 | JSON schema validation | OpenCode validator (optional) |

### Installation

```bash
# Install all dependencies
pip install -r requirements.txt

# Install specific version
pip install PyYAML==6.0.1 pytest==7.4.0 jsonschema==4.19.0
```

### Dependency Details

#### PyYAML (Required)

**Version:** >=6.0  
**License:** MIT  
**Documentation:** https://pyyaml.org/

**Usage:**
- Task YAML parsing (`ops/scripts/orchestration/agent_orchestrator.py`)
- Task validation (`validation/validate-task-schema.py`)
- Configuration loading

**Example:**
```python
import yaml

with open("work/inbox/task.yaml") as f:
    task = yaml.safe_load(f)
```

#### pytest (Required)

**Version:** >=7.0  
**License:** MIT  
**Documentation:** https://pytest.org/

**Usage:**
- E2E orchestration tests (`validation/test_orchestration_e2e.py`)
- Unit tests (future)

**Example:**
```bash
pytest validation/test_orchestration_e2e.py -v
```

#### jsonschema (Optional)

**Version:** >=4.0  
**License:** MIT  
**Documentation:** https://python-jsonschema.readthedocs.io/

**Usage:**
- OpenCode spec validation (`ops/scripts/opencode-spec-validator.py`)
- Task schema validation (alternative validator)

**Example:**
```python
from jsonschema import validate

schema = {...}
validate(instance=task_data, schema=schema)
```

---

## CLI Tools

### GitHub Copilot Tooling

**Installation:** `.github/copilot/setup.sh`

**Automated Setup:**
```bash
# Via GitHub Actions
gh workflow run copilot-setup.yml

# Manual execution
bash .github/copilot/setup.sh
```

### Tool Inventory

#### ripgrep (rg)

**Purpose:** Fast recursive text search  
**Version:** Latest stable  
**Installation:**
```bash
curl -LO https://github.com/BurntSushi/ripgrep/releases/download/13.0.0/ripgrep_13.0.0_amd64.deb
sudo dpkg -i ripgrep_13.0.0_amd64.deb
```

**Usage:**
```bash
# Search for pattern in repository
rg "orchestration" --type md

# Search with context
rg "agent" -A 3 -B 3

# Search specific files
rg "status.*done" work/done/*.yaml
```

**Agent Context:** Directive 001 (CLI & Shell Tooling)

#### fd

**Purpose:** Fast file finder (modern `find`)  
**Version:** Latest stable  
**Installation:**
```bash
curl -LO https://github.com/sharkdp/fd/releases/download/v8.7.0/fd_8.7.0_amd64.deb
sudo dpkg -i fd_8.7.0_amd64.deb
```

**Usage:**
```bash
# Find Python files
fd -e py

# Find by name pattern
fd "task.*yaml" work/

# Find directories
fd --type d "assigned"
```

**Agent Context:** Directive 001

#### ast-grep

**Purpose:** AST-based code search  
**Version:** Latest stable  
**Installation:**
```bash
curl -L https://github.com/ast-grep/ast-grep/releases/download/0.12.0/ast-grep-x86_64-unknown-linux-gnu.zip -o ast-grep.zip
unzip ast-grep.zip
sudo mv ast-grep /usr/local/bin/
```

**Usage:**
```bash
# Find function definitions
ast-grep --pattern 'def $NAME($$$)' --lang python

# Find class instantiations
ast-grep --pattern 'AgentBase()' ops/scripts/
```

**Agent Context:** Directive 001

#### jq

**Purpose:** JSON processing and querying  
**Version:** Latest stable (system package)  
**Installation:**
```bash
sudo apt-get install -y jq
```

**Usage:**
```bash
# Extract agent names from OpenCode config
jq '.agents[].name' opencode-config.json

# Filter by field
jq '.agents[] | select(.name == "architect")' opencode-config.json
```

**Agent Context:** Directive 001

#### yq

**Purpose:** YAML processing (like jq for YAML)  
**Version:** Latest v4.x  
**Installation:**
```bash
curl -L https://github.com/mikefarah/yq/releases/download/v4.35.1/yq_linux_amd64 -o /tmp/yq
sudo mv /tmp/yq /usr/local/bin/yq
sudo chmod +x /usr/local/bin/yq
```

**Usage:**
```bash
# Extract task status
yq '.status' work/inbox/task.yaml

# Update field
yq eval '.status = "in_progress"' -i work/assigned/architect/task.yaml

# Filter arrays
yq '.artefacts[]' work/done/task.yaml
```

**Agent Context:** Directive 001

#### fzf

**Purpose:** Fuzzy finder for interactive selection  
**Version:** Latest stable  
**Installation:**
```bash
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install --all
```

**Usage:**
```bash
# Fuzzy find files
fd | fzf

# Select task interactively
fd . work/inbox/ | fzf

# Preview file content
fzf --preview 'cat {}'
```

**Agent Context:** Directive 001

### Tool Summary Table

| Tool | Purpose | Install Method | Config File | Version Check |
|------|---------|----------------|-------------|---------------|
| rg | Text search | .deb package | ~/.ripgreprc | `rg --version` |
| fd | File finding | .deb package | ~/.config/fd/ignore | `fd --version` |
| ast-grep | AST search | Binary download | ~/.ast-grep/config.yml | `ast-grep --version` |
| jq | JSON processing | apt-get | ~/.jq | `jq --version` |
| yq | YAML processing | Binary download | - | `yq --version` |
| fzf | Fuzzy finder | Git + install | ~/.fzf.bash | `fzf --version` |

---

## GitHub Actions Dependencies

### Workflow Dependencies

#### Actions Marketplace

| Action | Version | Purpose | Used In |
|--------|---------|---------|---------|
| actions/checkout | v3 | Repository checkout | All workflows |
| actions/setup-python | v4 | Python environment | orchestration.yml, validation.yml |
| actions/upload-artifact | v3 | Artifact storage | diagram-rendering.yml |

#### Custom Scripts

| Script | Language | Purpose | Workflow |
|--------|----------|---------|----------|
| ops/scripts/orchestration/agent_orchestrator.py | Python | Task routing | orchestration.yml |
| validation/validate-task-schema.py | Python | Schema validation | validation.yml |
| validation/validate-work-structure.sh | Bash | Structure validation | validation.yml |
| .github/copilot/setup.sh | Bash | Tool installation | copilot-setup.yml |

### Workflow Matrix

| Workflow | Runs On | Python | Node | Other |
|----------|---------|--------|------|-------|
| orchestration.yml | ubuntu-latest | 3.x | - | - |
| validation.yml | ubuntu-latest | 3.x | - | - |
| copilot-setup.yml | ubuntu-latest | - | - | CLI tools |
| diagram-rendering.yml | ubuntu-latest | - | - | PlantUML |

---

## Agent Tooling Requirements

### Base Requirements

**For All Agents:**
1. Read access to repository
2. Write access to `work/` directory
3. Git credentials (for commit/push)
4. Python >=3.8
5. PyYAML library

### Specialized Requirements

#### Bootstrap Bill (Repository Mapping)

**Additional Tools:**
- fd (file enumeration)
- rg (content search)
- tree (directory visualization, optional)

**Directives:**
- 001: CLI & Shell Tooling
- 003: Repository Quick Reference
- 004: Documentation & Context Files

#### Architect (Design Documentation)

**Additional Tools:**
- PlantUML (diagram generation)
- Mermaid (alternative diagrams)

**Templates:**
- docs/templates/architecture/adr-template.md
- docs/templates/architecture/design-doc-template.md

#### Lexical (Terminology Management)

**Additional Tools:**
- rg (term searching)
- yq (glossary parsing)

**Data Files:**
- data/glossary.toml (if exists)

#### Diagrammer (Diagram Generation)

**Additional Tools:**
- PlantUML Java runtime
- Graphviz (for PlantUML rendering)

**Workflows:**
- .github/workflows/diagram-rendering.yml

### Directive Dependencies

| Agent | Required Directives | Optional Directives |
|-------|---------------------|---------------------|
| bootstrap-bill | 001, 003, 004, 006, 007 | 014 |
| architect | 004, 007, 008 | 001, 014 |
| lexical | 001, 004, 007 | 014 |
| diagrammer | 004, 007, 008 | 001, 014 |
| backend-dev | 001, 007, 009 | 014 |
| test-agent | 001, 007, 009 | 014 |

---

## Runtime Requirements

### System Requirements

**Operating System:**
- Linux (Ubuntu 20.04+)
- macOS 11+
- Windows with WSL2

**Python:**
- Version: 3.8+
- Recommended: 3.10+

**Disk Space:**
- Minimum: 50 MB (repository only)
- Recommended: 500 MB (with CLI tools + cache)

**Memory:**
- Minimum: 512 MB (orchestrator)
- Recommended: 2 GB (multiple agents)

### Git Configuration

**Required:**
```bash
git config --global user.name "Agent Name"
git config --global user.email "agent@example.com"
```

**Recommended:**
```bash
git config --global core.autocrlf input
git config --global pull.rebase false
```

### Environment Variables

**Optional:**
```bash
# Orchestrator polling interval (seconds)
export ORCHESTRATOR_POLL_INTERVAL=30

# Task timeout (hours)
export TASK_TIMEOUT_HOURS=2

# Log level (DEBUG, INFO, WARNING, ERROR)
export LOG_LEVEL=INFO
```

---

## Development Dependencies

### Pre-commit Hooks (Optional)

**Installation:**
```bash
pip install pre-commit
pre-commit install
```

**Configuration:** `.pre-commit-config.yaml` (not yet implemented)

### Linting Tools (Optional)

**Python:**
```bash
pip install black flake8 mypy
```

**Markdown:**
```bash
npm install -g markdownlint-cli
```

### Testing Tools

**E2E Testing:**
- pytest (already in requirements.txt)
- pytest-xdist (parallel execution, optional)

**Installation:**
```bash
pip install pytest-xdist
pytest -n auto validation/test_orchestration_e2e.py
```

---

## Optional Dependencies

### PlantUML (Diagram Rendering)

**Purpose:** Generate diagrams from .puml files

**Installation:**
```bash
# Java runtime (required)
sudo apt-get install -y default-jre

# Graphviz (required for some diagrams)
sudo apt-get install -y graphviz

# PlantUML JAR
wget https://github.com/plantuml/plantuml/releases/download/v1.2023.10/plantuml-1.2023.10.jar
sudo mv plantuml-1.2023.10.jar /usr/local/bin/plantuml.jar

# Wrapper script
echo '#!/bin/bash' | sudo tee /usr/local/bin/plantuml
echo 'java -jar /usr/local/bin/plantuml.jar "$@"' | sudo tee -a /usr/local/bin/plantuml
sudo chmod +x /usr/local/bin/plantuml
```

**Usage:**
```bash
plantuml docs/architecture/diagrams/diagram.puml
# Generates diagram.png
```

### OpenCode Tools (Portability)

**Purpose:** Cross-platform agent definition validation

**Installation:**
```bash
# No installation needed, uses Python standard library + jsonschema
pip install jsonschema
```

**Usage:**
```bash
python ops/scripts/opencode-spec-validator.py opencode-config.json
python ops/scripts/convert-agents-to-opencode.py
```

### GitHub CLI (gh)

**Purpose:** Workflow triggering, issue management

**Installation:**
```bash
# Debian/Ubuntu
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

**Usage:**
```bash
# Trigger orchestration workflow
gh workflow run orchestration.yml

# View workflow runs
gh run list --workflow=orchestration.yml

# Create issue
gh issue create --title "Task: Design API" --body "..."
```

---

## Dependency Verification

### Check All Dependencies

**Script:** `validation/validate_repo.sh` (partial)

**Manual Check:**

```bash
#!/bin/bash

echo "=== Python Dependencies ==="
pip list | grep -E "PyYAML|pytest|jsonschema"

echo ""
echo "=== CLI Tools ==="
for tool in rg fd ast-grep jq yq fzf; do
  if command -v $tool &> /dev/null; then
    echo "✓ $tool: $(command -v $tool)"
  else
    echo "✗ $tool: NOT FOUND"
  fi
done

echo ""
echo "=== Python Version ==="
python --version

echo ""
echo "=== Git Configuration ==="
git config user.name
git config user.email
```

### Dependency Health Check

**Task-based:**

```yaml
id: "2025-11-23T1600-coordinator-check-deps"
agent: "coordinator"
status: "new"
title: "Verify all dependencies installed"
artefacts:
  - work/logs/coordinator/dependency-check.md
context:
  check_items:
    - Python packages
    - CLI tools
    - Git config
    - GitHub Actions status
```

---

## Upgrade Strategy

### Python Packages

**Check for updates:**
```bash
pip list --outdated
```

**Upgrade:**
```bash
pip install --upgrade PyYAML pytest jsonschema
pip freeze > requirements.txt
```

### CLI Tools

**Check versions:**
```bash
rg --version
fd --version
yq --version
```

**Upgrade:**
```bash
# Re-run Copilot setup script
bash .github/copilot/setup.sh
```

### GitHub Actions

**Check for newer versions:**
- Visit https://github.com/actions
- Review changelogs
- Update workflow files

---

## Security Considerations

### Pinning Versions

**Not Currently Implemented:**

Current `requirements.txt` uses minimum versions (`>=`).

**Recommendation:**

```
PyYAML==6.0.1
pytest==7.4.0
jsonschema==4.19.0
```

### Vulnerability Scanning

**GitHub Dependabot:**
- Enabled by default for Python dependencies
- Monitors security advisories
- Creates PRs for updates

**Manual Scan:**
```bash
pip install safety
safety check -r requirements.txt
```

### Supply Chain Security

**Considerations:**
- CLI tools installed from official releases
- GitHub Actions pinned to major versions
- No third-party package registries

---

## Troubleshooting

### Common Issues

#### PyYAML Import Error

**Symptom:**
```
ImportError: No module named 'yaml'
```

**Solution:**
```bash
pip install PyYAML
```

#### fd/rg Not Found

**Symptom:**
```
bash: fd: command not found
```

**Solution:**
```bash
bash .github/copilot/setup.sh
```

#### yq Version Mismatch

**Symptom:**
```
yq: command not found or wrong syntax
```

**Solution:**
```bash
# Ensure using yq v4 (mikefarah/yq)
yq --version  # Should show "yq (https://github.com/mikefarah/yq/) version 4.x"

# Remove wrong version
sudo rm $(which yq)

# Reinstall correct version
curl -L https://github.com/mikefarah/yq/releases/download/v4.35.1/yq_linux_amd64 -o /tmp/yq
sudo mv /tmp/yq /usr/local/bin/yq
sudo chmod +x /usr/local/bin/yq
```

---

## Related Documentation

- **REPO_MAP.md**: Repository structure
- **SURFACES.md**: Public interfaces
- **WORKFLOWS.md**: Workflow patterns
- **docs/HOW_TO_USE/copilot-tooling-setup.md**: Detailed tool setup guide
- **.github/copilot/setup.sh**: Automated tool installer
- **.github/agents/directives/013_tooling_setup.md**: Tooling directive

---

_Generated by Bootstrap Bill (Task: 2025-11-23T2157-bootstrap-bill-repomap-update)_  
_For updates, assign new task to `bootstrap-bill` agent_  
_Dependency changes: Update this file + requirements.txt + Copilot setup script_
