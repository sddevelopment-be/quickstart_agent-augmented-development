# Doctrine Framework: Repository Map

_Version: 1.0.0_  
_Last Updated: 2026-02-13_  
_Agent: Bootstrap Bill_  
_Purpose: Navigate the portable agentic framework_

---

## Overview

The **Doctrine Framework** is a **standalone, zero-dependency agentic governance system** designed for AI-augmented development workflows. It implements a **five-layer instruction hierarchy** that separates concerns, establishes clear precedence, and enables predictable agent behavior.

**Key Characteristics:**
- **Portable:** Distributable via git subtree, works in any repository
- **Zero Dependencies:** Pure markdown and YAML, no external libraries
- **LLM-Agnostic:** Compatible with any LLM supporting markdown context
- **Modular:** Load only relevant instructions (token-efficient)
- **Versioned:** Semantic versioning with comprehensive changelog

### Quick Stats

| Metric | Value |
|--------|-------|
| **Version** | 1.0.0 |
| **Files** | 201 |
| **Agents** | 21 specialized profiles |
| **Directives** | 34 operational instructions |
| **Tactics** | 50 procedural guides |
| **Approaches** | 4+ mental models |
| **Templates** | 20+ structure contracts |
| **Glossary Terms** | 350+ standardized definitions |

---

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [Five-Layer Architecture](#five-layer-architecture)
3. [Navigation by Purpose](#navigation-by-purpose)
4. [Key Files](#key-files)
5. [Usage Patterns](#usage-patterns)
6. [Integration Guide](#integration-guide)
7. [Versioning & Distribution](#versioning--distribution)

---

## Directory Structure

```
doctrine/
├── DOCTRINE_STACK.md        # Framework conceptual reference (5-layer model)
├── GLOSSARY.md              # Standardized terminology (350+ terms)
├── CHANGELOG.md             # Version history and migration guide
├── README.md                # Quick start and overview
│
├── agents/                  # 21 specialized agent profiles
│   ├── analyst-annie.agent.md
│   ├── architect.agent.md
│   ├── backend-dev.agent.md
│   ├── bootstrap-bill.agent.md      # Repository mapping & scaffolding
│   ├── build-automation.agent.md
│   ├── code-reviewer-cindy.agent.md
│   ├── curator.agent.md
│   ├── diagrammer.agent.md
│   ├── framework-guardian.agent.md
│   ├── frontend.agent.md
│   ├── java-jenny.agent.md
│   ├── lexical.agent.md
│   ├── manager.agent.md
│   ├── project-planner.agent.md
│   ├── python-pedro.agent.md
│   ├── researcher.agent.md
│   ├── reviewer.agent.md
│   ├── scribe.agent.md
│   ├── synthesizer.agent.md
│   ├── translator.agent.md
│   └── writer-editor.agent.md
│
├── directives/              # 34 operational instructions (load on-demand)
│   ├── 001_cli_shell_tooling.md
│   ├── 002_context_notes.md
│   ├── 003_repository_quick_reference.md
│   ├── 004_documentation_context_files.md
│   ├── 005_agent_profiles.md
│   ├── 006_version_governance.md
│   ├── 007_agent_declaration.md
│   ├── 008_artifact_templates.md
│   ├── 009_role_capabilities.md
│   ├── 010_mode_protocol.md
│   ├── 011_risk_escalation.md
│   ├── 012_operating_procedures.md
│   ├── 013_tooling_setup.md
│   ├── 014_worklog_creation.md
│   ├── 015_store_prompts.md
│   ├── 016_atdd.md          # Acceptance Test-Driven Development
│   ├── 017_tdd.md           # Test-Driven Development
│   ├── 018_traceable_decisions.md  # ADR protocol
│   ├── 019_file_based_collaboration.md
│   ├── 020_locality_of_change.md
│   ├── 024_self_observation_protocol.md
│   ├── 028_bugfixing_techniques.md
│   ├── 034_specification_driven.md
│   ├── 036_boy_scout_rule.md  # Mandatory pre-task cleanup
│   ├── ... (34 total)
│   └── manifest.json        # Directive registry
│
├── tactics/                 # 50 procedural execution guides
│   ├── README.md            # Tactics catalog & applicability matrix
│   ├── stopping-conditions.tactic.md
│   ├── premortem-risk-identification.tactic.md
│   ├── adversarial-testing.tactic.md
│   ├── AMMERSE-quality-assessment.tactic.md
│   ├── safe-to-fail-experiment-design.tactic.md
│   ├── ATDD_adversarial-acceptance.tactic.md
│   ├── ATDD_boundary-validation.tactic.md
│   ├── ATDD_critical-user-path.tactic.md
│   ├── test-boundary-analysis.tactic.md
│   ├── input-validation-checklist.tactic.md
│   ├── code-review-checklist.tactic.md
│   ├── ... (50 total)
│   └── template.tactic.md   # Tactic document template
│
├── approaches/              # Mental models and philosophies
│   ├── trunk-based-development.md
│   ├── decision-first-development.md
│   ├── locality-of-change.md
│   ├── file-based-orchestration.md
│   └── specification-driven-development.md
│
├── guidelines/              # Core behavioral guidelines (HIGHEST precedence)
│   ├── general_guidelines.md      # Broad operational principles
│   ├── operational_guidelines.md  # Tone, honesty, reasoning discipline
│   ├── bootstrap.md               # Initialization protocol
│   └── rehydrate.md               # State recovery protocol
│
├── templates/               # Output structure contracts
│   ├── architecture/        # ADRs, design docs
│   │   ├── adr.md
│   │   └── design-doc.md
│   ├── automation/          # Scripts, workflows
│   │   ├── github-action.yml
│   │   └── shell-script.sh
│   ├── project/             # Project management
│   │   ├── milestone.md
│   │   └── task.yaml
│   ├── tactic.md            # Tactic document template
│   ├── agent-profile.md     # Agent profile template
│   ├── directive.md         # Directive template
│   └── worklog.md           # Work log template (Directive 014)
│
├── shorthands/              # Command aliases and shortcuts
│   └── README.md
│
├── examples/                # Example usage and patterns
│   ├── agent-initialization/
│   ├── directive-loading/
│   ├── tactic-execution/
│   └── multi-agent-coordination/
│
└── docs/                    # Framework documentation (design docs, diagrams)
    ├── architecture/
    ├── diagrams/
    └── guides/
```

---

## Five-Layer Architecture

### Layer Hierarchy (Precedence Order)

```
┌─────────────────────────────────────────────┐
│ 1. Guidelines (values, preferences)         │ ← Highest precedence
├─────────────────────────────────────────────┤
│ 2. Approaches (mental models, philosophies) │
├─────────────────────────────────────────────┤
│ 3. Directives (instructions, constraints)   │ ← Select tactics
├─────────────────────────────────────────────┤
│ 4. Tactics (procedural execution guides)    │ ← Execute work
├─────────────────────────────────────────────┤
│ 5. Templates (output structure contracts)   │ ← Lowest precedence
└─────────────────────────────────────────────┘
```

### 1. Guidelines Layer

**Location:** `doctrine/guidelines/`  
**Precedence:** Highest (cannot be overridden)  
**Purpose:** Enduring values, preferences, and guardrails

**Files:**

| File | Purpose | Load Priority |
|------|---------|---------------|
| `general_guidelines.md` | Broad operational principles, collaboration ethos | MANDATORY |
| `operational_guidelines.md` | Tone, honesty, reasoning discipline | MANDATORY |
| `bootstrap.md` | Initialization protocol, path selection | ROOT |
| `rehydrate.md` | State recovery protocol | As needed |

**Characteristics:**
- Rarely change (1-2 per year maximum)
- Shape all downstream decisions
- Provide "north star" for agent behavior
- Define tone, integrity, and collaboration boundaries

**Example Guidelines:**
- "Never override general or operational guidelines"
- "Stay within defined specialization"
- "Ask clarifying questions when uncertainty >30%"
- "Escalate issues before they become problems"

### 2. Approaches Layer

**Location:** `doctrine/approaches/`  
**Precedence:** Medium (guide interpretation, don't mandate)  
**Purpose:** Conceptual models and philosophies for reasoning

**Files:**

| File | Purpose |
|------|---------|
| `trunk-based-development.md` | Branching strategy philosophy |
| `decision-first-development.md` | Decision capture workflow |
| `locality-of-change.md` | Premature optimization avoidance |
| `file-based-orchestration.md` | Multi-agent coordination philosophy |
| `specification-driven-development.md` | Requirements-first workflow |

**Characteristics:**
- Justify *why* certain tactics or directives exist
- Provide mental models for systemic reasoning
- Guide problem framing, not execution
- Support strategic alignment

**When to Add:** Introducing a conceptual model that shapes multiple tactics

### 3. Directives Layer

**Location:** `doctrine/directives/`  
**Precedence:** Medium (select tactics, constrain approaches)  
**Purpose:** Explicit instructions or constraints

**Directory:** 34 numbered directives (001-036+)

**Key Directives:**

| Code | Title | Purpose | Invokes Tactics |
|------|-------|---------|-----------------|
| 001 | CLI & Shell Tooling | Fast file/text enumeration | None |
| 007 | Agent Declaration | Mandatory authority affirmation | None |
| 014 | Work Log Creation | Documentation standards | `stopping-conditions` |
| 016 | Acceptance Test-Driven Development | ATDD workflow | `ATDD_adversarial-acceptance`, `ATDD_boundary-validation` |
| 017 | Test-Driven Development | TDD workflow | `test-boundary-analysis` |
| 018 | Traceable Decisions | ADR protocol | None |
| 028 | Bug Fixing Techniques | Test-first bug workflow | None |
| 034 | Specification-Driven Development | Requirements capture | None |
| 036 | Boy Scout Rule | Pre-task cleanup (mandatory) | None |

**Load Pattern:**
```markdown
/require-directive 014  # Work Log Creation
/require-directive 016  # ATDD
```

**Characteristics:**
- Numbered for load-on-demand efficiency
- Prescriptive, not descriptive
- Select tactics, constrain approaches
- Enforce compliance boundaries

**Manifest:** `doctrine/directives/manifest.json` (complete registry)

**When to Add:** Encoding a rule that selects specific actions or establishes compliance requirements

### 4. Tactics Layer

**Location:** `doctrine/tactics/`  
**Precedence:** Medium-Low (execute work procedurally)  
**Purpose:** Step-by-step execution guides

**Directory:** 50 tactics with `.tactic.md` extension

**Catalog:** `doctrine/tactics/README.md` (applicability matrix)

**Key Tactics:**

| Tactic | Purpose | Invoked By |
|--------|---------|------------|
| `stopping-conditions.tactic.md` | Define exit criteria | Directive 014 |
| `premortem-risk-identification.tactic.md` | Failure mode analysis | Directive 011 |
| `adversarial-testing.tactic.md` | Stress-test proposals | Directive 024 |
| `AMMERSE-quality-assessment.tactic.md` | Quality framework | Multiple |
| `safe-to-fail-experiment-design.tactic.md` | Exploration under uncertainty | Directive 024 |
| `ATDD_adversarial-acceptance.tactic.md` | Create adversarial tests | Directive 016 |
| `ATDD_boundary-validation.tactic.md` | Validate edge cases | Directive 016 |
| `test-boundary-analysis.tactic.md` | Identify test boundaries | Directive 017 |
| `input-validation-checklist.tactic.md` | Validate inputs | Multiple |
| `code-review-checklist.tactic.md` | Review code systematically | Directive 017 |

**Characteristics:**
- Procedural (sequence of actions, not advice)
- Context-bounded (state preconditions, exclusions)
- Linear by default (minimal branching)
- Non-creative (minimize interpretation)
- Verifiable (concrete outputs, exit criteria)
- Failure-aware (explicit failure modes documented)

**Discovery Mechanism:**
- **Primary:** Directives explicitly invoke tactics at workflow steps
- **Secondary:** Agents discover via `README.md` and propose to human

**When to Add:** Codifying a repeated task with known pitfalls to eliminate inconsistency

### 5. Templates Layer

**Location:** `doctrine/templates/`  
**Precedence:** Lowest (structure only, no content rules)  
**Purpose:** Structural output contracts

**Categories:**

| Category | Templates | Purpose |
|----------|-----------|---------|
| `architecture/` | ADRs, design docs | Architecture decision capture |
| `automation/` | GitHub Actions, shell scripts | Automation script structure |
| `project/` | Milestones, tasks | Project management artifacts |
| Root | Tactics, agents, directives, work logs | Framework artifact structure |

**Characteristics:**
- Cross-cutting (serve humans and agents)
- Define required sections, not content
- Enable consistent artifact structure
- Reduce cognitive load during creation

**When to Add:** Standardizing artifact structure across agents to ensure required sections

---

## Navigation by Purpose

### For Agent Initialization

**Read in Order:**

1. **`AGENTS.md`** (repository root) - Agent Specification Document
2. **`guidelines/bootstrap.md`** - Initialization protocol
3. **`guidelines/general_guidelines.md`** - Broad operational principles
4. **`guidelines/operational_guidelines.md`** - Tone and reasoning discipline
5. **`agents/<agent-name>.agent.md`** - Your specialist profile
6. **`directives/007_agent_declaration.md`** - Authority affirmation
7. **Load required directives** via `/require-directive NNN`

**Validation:** Run `/validate-alignment` and announce readiness with ✅

### For Understanding the Framework

**Read in Order:**

1. **`DOCTRINE_STACK.md`** - Five-layer conceptual model
2. **`GLOSSARY.md`** - Standardized terminology (350+ terms)
3. **`tactics/README.md`** - Tactics catalog and applicability matrix
4. **`directives/manifest.json`** - Complete directive registry
5. **`agents/`** - Browse agent profiles to see specialization patterns

### For Writing New Directives

**Templates and Examples:**

1. **`templates/directive.md`** - Directive template
2. **`directives/014_worklog_creation.md`** - Example: work log standards
3. **`directives/016_atdd.md`** - Example: workflow directive with tactic invocation
4. **`directives/036_boy_scout_rule.md`** - Example: simple mandatory directive

**Process:**
1. Copy template
2. Assign next available code (037+)
3. Define purpose, applicability, and constraints
4. Identify which tactics to invoke (if any)
5. Update `directives/manifest.json`
6. Link from related approaches (if applicable)

### For Writing New Tactics

**Templates and Examples:**

1. **`templates/tactic.md`** - Tactic template
2. **`tactics/stopping-conditions.tactic.md`** - Example: simple tactic
3. **`tactics/ATDD_adversarial-acceptance.tactic.md`** - Example: testing tactic
4. **`tactics/premortem-risk-identification.tactic.md`** - Example: risk analysis tactic

**Process:**
1. Copy template
2. Define preconditions and exclusions
3. Write step-by-step procedure
4. Document failure modes
5. Define success criteria
6. Add to `tactics/README.md` applicability matrix

### For Creating New Agents

**Templates and Examples:**

1. **`templates/agent-profile.md`** - Agent profile template
2. **`agents/bootstrap-bill.agent.md`** - Example: structural agent
3. **`agents/curator.agent.md`** - Example: content agent
4. **`agents/python-pedro.agent.md`** - Example: language-specific agent

**Process:**
1. Copy template
2. Define clear specialization boundaries
3. List primary focus, secondary awareness, avoid list
4. Specify required directives
5. Define collaboration contract
6. Set mode defaults
7. Write initialization declaration

---

## Key Files

### Core Documentation

| File | Purpose | Audience |
|------|---------|----------|
| **DOCTRINE_STACK.md** | Five-layer governance framework | All users (start here) |
| **GLOSSARY.md** | 350+ standardized terms | All users (reference) |
| **CHANGELOG.md** | Version history and migration guide | Framework maintainers |
| **README.md** | Quick start and overview | New users |

### Catalogs & Indexes

| File | Purpose | Contents |
|------|---------|----------|
| **tactics/README.md** | Tactics catalog | 50 tactics with applicability matrix |
| **directives/manifest.json** | Directive registry | Complete list of 34 directives |
| **agents/** (directory listing) | Agent inventory | 21 specialist profiles |

### Templates

| File | Purpose | Use Case |
|------|---------|----------|
| **templates/tactic.md** | Tactic structure | Creating new tactics |
| **templates/directive.md** | Directive structure | Creating new directives |
| **templates/agent-profile.md** | Agent profile structure | Creating new agents |
| **templates/architecture/adr.md** | ADR structure | Documenting decisions (Directive 018) |
| **templates/worklog.md** | Work log structure | Documenting work (Directive 014) |

---

## Usage Patterns

### Pattern 1: Agent Initialization

```markdown
# Step 1: Read core documents
- AGENTS.md (repository root)
- doctrine/guidelines/bootstrap.md
- doctrine/guidelines/general_guidelines.md
- doctrine/guidelines/operational_guidelines.md

# Step 2: Load agent profile
- doctrine/agents/<agent-name>.agent.md

# Step 3: Load required directives
/require-directive 007  # Agent Declaration
/require-directive 014  # Work Log Creation
/require-directive 016  # ATDD (if writing tests)
/require-directive 018  # Traceable Decisions (if making architectural changes)

# Step 4: Validate alignment
/validate-alignment

# Step 5: Announce readiness
✅ SDD Agent "<Agent Name>" initialized.
**Context layers:** Operational ✓, Strategic ✓, Command ✓, Bootstrap ✓, AGENTS ✓.
**Purpose acknowledged:** <Purpose statement>
```

### Pattern 2: Executing a Task with Tactics

```markdown
# Agent receives task in work/assigned/<agent>/

# Step 1: Load relevant directive
/require-directive 016  # ATDD

# Step 2: Directive invokes tactic
# Read: doctrine/tactics/ATDD_adversarial-acceptance.tactic.md

# Step 3: Follow tactic steps
1. Identify acceptance criteria from specification
2. Write adversarial test cases
3. Run tests (should fail)
4. Implement feature
5. Run tests (should pass)
6. Document decision (ADR if architectural)

# Step 4: Create work log (Directive 014)
# Location: work/reports/logs/<agent>/
# Template: doctrine/templates/worklog.md

# Step 5: Update task status to "done"
```

### Pattern 3: Multi-Agent Coordination

```markdown
# Agent 1 (Architect) completes task
result:
  summary: "Architecture design completed"
  artefacts:
    - "docs/architecture/design/api.md"
  next_agent: "backend-dev"
  next_task_title: "Implement API endpoints"
  next_artefacts:
    - "src/api/endpoints.py"
  next_task_notes:
    - "Follow design in docs/architecture/design/api.md"
    - "Use Directive 016 (ATDD) for tests"
    - "Create ADR if deviating from design (Directive 018)"

# Orchestrator creates new task in work/inbox/
# Agent 2 (Backend-dev) picks up task
# Loads directives: 016 (ATDD), 018 (ADR)
# Executes tactics: ATDD_adversarial-acceptance, test-boundary-analysis
# Creates work log (Directive 014)
```

---

## Integration Guide

### Integrating Doctrine into Your Repository

**Step 1: Add Doctrine as Git Subtree**

```bash
# Add doctrine as subtree
git subtree add --prefix=doctrine \
  https://github.com/sddevelopment-be/quickstart_agent-augmented-development.git \
  main --squash

# Update doctrine later
git subtree pull --prefix=doctrine \
  https://github.com/sddevelopment-be/quickstart_agent-augmented-development.git \
  main --squash
```

**Step 2: Create Configuration**

```bash
# Create local configuration directory
mkdir -p .doctrine-config

# Create config.yaml
cat > .doctrine-config/config.yaml <<EOF
repository:
  name: "your-repo-name"
  description: "Your repository description"
  version: "1.0.0"

paths:
  workspace_root: "work"
  doc_root: "docs"
  spec_root: "specifications"
  output_root: "output"

agents:
  enabled: true
  profiles_path: "doctrine/agents"
  directives_path: "doctrine/directives"
  tactics_path: "doctrine/tactics"
EOF

# Create local guidelines
cat > .doctrine-config/specific_guidelines.md <<EOF
# Project-Specific Guidelines

## Repository-Specific Constraints
- Add your constraints here

## Project Conventions
- Add your conventions here
EOF
```

**Step 3: Initialize Work Directory**

```bash
# Use provided script
bash work/scripts/init-work-structure.sh
```

**Step 4: Customize Agent Profiles**

```bash
# Optional: Copy agent profiles to .doctrine-config/agents/
mkdir -p .doctrine-config/agents
cp doctrine/agents/architect.agent.md .doctrine-config/agents/

# Customize for your needs
# Note: These override doctrine defaults but cannot override guidelines
```

### Using Doctrine with GitHub Copilot

**Export agent profiles:**

```bash
python tools/exporters/copilot/export_to_copilot.py
```

**Profiles exported to:** `.github/copilot/agents/`

### Using Doctrine with Claude Desktop

**Export custom skills:**

```bash
python tools/exporters/claude/export_to_claude.py
```

**Skills exported to:** `.claude/agents/`

### Using Doctrine with OpenCode

**Export cross-platform format:**

```bash
python tools/exporters/opencode/export_to_opencode.py
```

**Config generated:** `opencode-config.json`

---

## Versioning & Distribution

### Semantic Versioning

Doctrine follows [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR:** Breaking changes to directive/tactic APIs or precedence model
- **MINOR:** New directives, tactics, agents, or backward-compatible features
- **PATCH:** Bug fixes, documentation updates, clarifications

**Current Version:** 1.0.0

**See:** `CHANGELOG.md` for complete version history

### Distribution Model

Doctrine is designed for **git subtree distribution**:

**Advantages:**
- Zero external dependencies
- No package manager required
- Version pinning via Git
- Easy updates (git subtree pull)
- Fork-friendly for customization

**Recommended:**
- Add as subtree to `doctrine/` directory
- Keep local customizations in `.doctrine-config/`
- Update periodically to get new tactics/directives
- Contribute improvements back to upstream

### Migration Guide

**Updating from previous versions:**

1. Check `CHANGELOG.md` for breaking changes
2. Review `MIGRATION_GUIDE.md` (if exists for major versions)
3. Update subtree: `git subtree pull --prefix=doctrine ...`
4. Test agent initialization with updated directives
5. Update `.doctrine-config/` customizations if needed

---

## Contributing to Doctrine

### Adding New Directives

1. Copy `templates/directive.md`
2. Assign next code (037+)
3. Follow naming: `NNN_kebab-case-title.md`
4. Update `directives/manifest.json`
5. Link from relevant approaches (if applicable)
6. Submit PR with rationale

### Adding New Tactics

1. Copy `templates/tactic.md`
2. Follow naming: `kebab-case-title.tactic.md`
3. Add to `tactics/README.md` applicability matrix
4. Link from invoking directives
5. Submit PR with usage examples

### Adding New Agents

1. Copy `templates/agent-profile.md`
2. Follow naming: `kebab-case-name.agent.md`
3. Define clear specialization boundaries
4. Avoid overlap with existing agents
5. Submit PR with use case examples

### Improving Documentation

1. Keep DOCTRINE_STACK.md conceptual, not procedural
2. Add terms to GLOSSARY.md (alphabetical order)
3. Update CHANGELOG.md for all changes
4. Cross-reference related directives/tactics/agents

---

## Quick Reference

### File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Directive | `NNN_kebab-case-title.md` | `014_worklog_creation.md` |
| Tactic | `kebab-case-title.tactic.md` | `stopping-conditions.tactic.md` |
| Agent | `kebab-case-name.agent.md` | `bootstrap-bill.agent.md` |
| Approach | `kebab-case-title.md` | `trunk-based-development.md` |
| Template | `kebab-case-title.md` | `adr.md` |

### Load Commands

```markdown
# Load directive
/require-directive 014

# Load multiple
/require-directive 014
/require-directive 016
/require-directive 018

# Validate alignment
/validate-alignment

# Declare agent authority
✅ SDD Agent "<Name>" initialized.
```

### Essential Directives

| Code | Must-Load For |
|------|---------------|
| 007 | All agents (authority declaration) |
| 014 | All agents (work log creation) |
| 016 | Writing tests (ATDD workflow) |
| 017 | Writing code (TDD workflow) |
| 018 | Making architectural changes (ADR protocol) |
| 028 | Fixing bugs (test-first bug workflow) |
| 036 | All agents (Boy Scout Rule - mandatory) |

---

## Related Artifacts

- **[../REPO_MAP.md](../REPO_MAP.md)** - Complete repository structure (parent repo)
- **[../SURFACES.md](../SURFACES.md)** - API surfaces and integration points (parent repo)
- **[../VISION.md](../VISION.md)** - Project vision and strategic goals (parent repo)
- **[DOCTRINE_STACK.md](DOCTRINE_STACK.md)** - Five-layer governance framework
- **[GLOSSARY.md](GLOSSARY.md)** - Standardized terminology (350+ terms)
- **[tactics/README.md](tactics/README.md)** - Tactics catalog and applicability matrix

---

_Generated by Bootstrap Bill_  
_For doctrine updates: Submit issue or PR to upstream repository_  
_For local customizations: Use `.doctrine-config/` directory_  
_Last Updated: 2026-02-13_
