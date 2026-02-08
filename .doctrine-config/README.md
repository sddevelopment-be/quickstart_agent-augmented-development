# Doctrine Configuration Directory

**Purpose:** Repository-specific doctrine overrides, custom agent rules, local settings, and configuration that applies ONLY to this repository.

**Version:** 1.0.0  
**Created:** 2026-02-08

---

## Directory Purpose

This directory contains **local doctrine configuration** that supplements or overrides the framework defaults from `doctrine/`. Use this for:

- **Repository-specific guidelines** that don't belong in the framework
- **Custom agent behavior rules** for this project
- **Local path overrides** for directory structures
- **Tool-specific integrations** unique to this repository
- **Commit hooks and automation** tailored to this workflow

---

## File Structure

```
.doctrine-config/
├── README.md                    # This file
├── repository-guidelines.md     # Project-specific conventions (moved from specific_guidelines.md)
├── config.yaml                  # Local path overrides and settings
├── custom-agents/               # Repository-specific agent extensions
│   └── README.md
└── hooks/                       # Git hooks and automation scripts
    └── README.md
```

---

## Principles

### 1. Framework vs. Local Separation

**Framework (`doctrine/`):**
- Universal patterns, approaches, directives
- Portable across repositories
- Maintained as core framework

**Local (`.doctrine-config/`):**
- Repository-specific conventions
- Project-unique requirements
- Not intended for reuse

### 2. Configuration Override Precedence

When conflicts exist between layers:

```
1. .doctrine-config/ (highest precedence - local overrides)
2. doctrine/ (framework defaults)
3. Tool-specific distributions (.github/, .claude/, etc.)
```

### 3. Version Control

- ✅ **DO commit:** Configuration files, guidelines, custom agent definitions
- ❌ **DON'T commit:** Secrets, API keys, personal preferences
- 🔒 **Sensitive data:** Use `.gitignore` for secrets (`.doctrine-config/.secrets/`)

---

## Usage by Agents

### Loading Local Configuration

Agents should check for `.doctrine-config/` during initialization:

1. Load framework defaults from `doctrine/`
2. Check for `.doctrine-config/config.yaml`
3. Apply local overrides
4. Check for `repository-guidelines.md`
5. Apply project-specific conventions

### Example: Bootstrap Bill

```bash
# During repository bootstrap
1. Read doctrine/templates/automation/doctrine-config-template.yaml
2. Generate .doctrine-config/config.yaml with local paths
3. Copy specific_guidelines.md → .doctrine-config/repository-guidelines.md
4. Configure tool integrations based on detected tooling
```

---

## Configuration Schema

### config.yaml Structure

```yaml
repository:
  name: "quickstart_agent-augmented-development"
  description: "Agent-augmented development framework quickstart"
  version: "1.0.0"

paths:
  workspace_root: "work"              # Task orchestration workspace
  doc_root: "docs"                    # Documentation root
  spec_root: "specifications"         # Specification files
  output_root: "output"               # Generated artifacts
  doctrine_source: "doctrine"         # Framework source (if moved)

tools:
  enabled:
    - github-copilot
    - claude-desktop
    - opencode
  distributions:
    github_copilot: ".github/instructions"
    claude_desktop: ".claude"
    opencode: ".opencode"

overrides:
  commit_signing: false               # Disable GPG for agent commits
  phase_checkpoint_required: true     # Enforce checkpoint protocol
```

---

## Migration from Root Files

**Moved from repository root:**

- `specific_guidelines.md` → `.doctrine-config/repository-guidelines.md`

**Reasoning:**
- Clarifies local vs. framework scope
- Reduces root directory clutter
- Makes configuration discoverable
- Follows tool-specific patterns (.github/, .claude/, .opencode/)

---

## Custom Agents

Repository-specific agent extensions live in `.doctrine-config/custom-agents/`:

```yaml
# Example: .doctrine-config/custom-agents/data-analyst-dana.agent.yaml
name: "Data Analyst Dana"
slug: "data-analyst-dana"
role: "domain-specific"
specialization: "CSV validation and data quality checks"
extends: "analyst-annie"
capabilities:
  - data-validation
  - csv-schema-inference
  - quality-reporting
```

**When to create custom agents:**
- Domain-specific expertise (e.g., financial data validation)
- Project-unique workflows (e.g., legacy system integration)
- NOT for general-purpose patterns (those belong in `doctrine/agents/`)

---

## Related Documentation

- **Framework Source:** `doctrine/` - Universal patterns and approaches
- **Distribution Mapping:** `doctrine/DOCTRINE_DISTRIBUTION.md` - How framework exports to tools
- **Bootstrap Template:** `doctrine/templates/automation/doctrine-config-template.yaml`
- **Agent Profiles:** `doctrine/agents/*.agent.md` - Framework agent definitions

---

**Maintained by:** Repository maintainers  
**Scope:** This repository only  
**Review Cycle:** As needed
