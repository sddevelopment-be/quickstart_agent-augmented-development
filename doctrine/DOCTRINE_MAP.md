# DOCTRINE_MAP — Framework Structure

_Last updated: 2026-02-07_  
_Version: 1.0.0_

## Summary

- **Purpose:** Provide a navigable map of the SDD Agentic Framework for quick discovery, onboarding, and agent routing.
- **Scope:** Core framework files, doctrine layers, templates, and reference documents.
- **Portability:** This directory is self-contained with zero external dependencies.

## Tree (condensed)

```
doctrine/
├── DOCTRINE_STACK.md              # Layer architecture definition
├── GLOSSARY.md                    # Framework terminology reference
├── agents/                        # 20 agent profiles
├── approaches/                    # 34 mental models & patterns
│   ├── file_based_collaboration/  # 8 orchestration workflows
│   ├── operating_procedures/      # 2 procedural norms
│   └── prompt_documentation/      # 5 prompt guidelines
├── directives/                    # 29 instructions & constraints
├── tactics/                       # 22 procedural execution guides
├── guidelines/                    # 5 behavioral norms
├── shorthands/                    # 3 command aliases & quick prompts
├── templates/                     # 80 output structure templates
└── docs/
    ├── references/                # Comparative studies & primers
    └── styleguides/               # 4 language-specific style guides
```

**Total:** 201 framework files

---

## Core Files

### DOCTRINE_STACK.md
**Purpose:** Defines the five-layer doctrine architecture (guidelines → approaches → directives → tactics → templates)  
**Key sections:** Layer definitions, precedence rules, initialization protocol  
**When to read:** Agent initialization, understanding framework hierarchy

### GLOSSARY.md
**Purpose:** Centralized definitions of framework terminology  
**Key sections:** Agent concepts, orchestration terms, workflow states, testing vocabulary  
**When to read:** Encountering unfamiliar framework terms, onboarding new contributors

---

## Directories

### `/agents/` — Agent Profiles (20 files)
**Purpose:** Specialized agent configurations extending the base AGENTS.md specification  
**Contents:**
- Role-specific competencies and responsibilities
- Collaboration contracts and handoff patterns
- Mode defaults and directive usage
- Success criteria and avoidance zones

**Example files:**
- `analyst-annie.agent.md` — Data analysis & synthesis
- `architect.agent.md` — Architectural decision making
- `backend-dev.agent.md` — Backend implementation
- `curator.agent.md` — Documentation curation & normalization
- `researcher.agent.md` — Research & comparative analysis

**When to use:** Selecting the right agent for a task, understanding agent capabilities

---

### `/approaches/` — Mental Models & Patterns (34 files)
**Purpose:** High-level conceptual frameworks and operational philosophies  
**Contents:**
- Workflow patterns (file-based orchestration, trunk-based development)
- Quality practices (test-readability checks, locality of change)
- Decision frameworks (decision-first development, traceable decisions)
- Meta-cognitive patterns (Ralph Wiggum loop, meta-analysis)

**Subdirectories:**
- `file_based_collaboration/` (8 files) — Task lifecycle workflows
- `operating_procedures/` (2 files) — Procedural redundancy rationale
- `prompt_documentation/` (5 files) — Prompt storage & SWOT analysis

**Example files:**
- `decision-first-development.md` — Capture architectural decisions systematically
- `trunk-based-development.md` — Branch strategy for agent-first workflows
- `work-directory-orchestration.md` — File-based async orchestration model
- `ralph-wiggum-loop.md` — Self-observation pattern for agents

**When to use:** Designing workflows, establishing team conventions, solving cross-cutting concerns

---

### `/directives/` — Instructions & Constraints (29 files)
**Purpose:** Explicit instructions and constraints for agent behavior  
**Contents:**
- Operational procedures (014 worklogs, 019 file-based collaboration)
- Quality standards (016 ATDD, 017 TDD, 026 commit protocol)
- Metadata requirements (035 specification frontmatter standards)
- Tool usage patterns (001 CLI tooling, 013 tooling setup)

**Example files:**
- `014_worklog_creation.md` — Standards for documenting agent execution
- `019_file_based_collaboration.md` — Task orchestration via YAML files
- `034_spec_driven_development.md` — Specification-first methodology
- `024_self_observation_protocol.md` — Mid-execution self-checks

**When to use:** Implementing specific procedures, ensuring compliance, understanding requirements

---

### `/tactics/` — Procedural Execution Guides (22 files)
**Purpose:** Step-by-step procedures invoked by directives  
**Contents:**
- Testing strategies (ATDD, adversarial testing, boundary testing)
- Refactoring patterns (strangler fig, extract concept)
- Analysis methods (AMMERSE, premortem risk identification)
- Development workflows (BDD, fresh context iteration)

**Example files:**
- `task-completion-validation.tactic.md` — 5-step validation before marking tasks done
- `ATDD_adversarial-acceptance.tactic.md` — Adversarial acceptance testing procedure
- `stopping-conditions.tactic.md` — When to stop work and escalate

**When to use:** Executing specific procedures, referenced by directives

---

### `/guidelines/` — Behavioral Norms (5 files)
**Purpose:** General operational principles and collaboration ethos  
**Contents:**
- Bootstrap procedures for agent initialization
- Operational principles (transparency, collaboration, integrity)
- Context rehydration after state loss
- Runtime behavioral sheet

**Files:**
- `bootstrap.md` — Agent initialization sequence
- `general_guidelines.md` — Broad operational principles
- `operational_guidelines.md` — Tone, honesty, reasoning discipline
- `rehydrate.md` — Context restoration protocol
- `runtime_sheet.md` — Quick reference for execution

**When to use:** Agent initialization, establishing baseline behavior

---

### `/shorthands/` — Command Aliases & Quick Prompts (3 files)
**Purpose:** Reusable command shortcuts and prompt templates for quick workflow invocation  
**Contents:**
- Complex multi-step workflows encapsulated as simple commands
- Skill creation patterns
- Iteration orchestration workflows

**Files:**
- `README.md` — Shorthand concept and usage patterns (originally aliases.md)
- `iteration-orchestration.md` — Multi-agent batch coordination workflow
- `SKILLS_CREATED.md` — Catalog of available skills and patterns

**When to use:** Quick invocation of complex workflows, discovering available commands

---

### `/docs/references/` — Comparative Studies & Primers
**Purpose:** Long-form reference material, methodology comparisons, external framework analyses  
**Contents:**
- Comparative studies of methodologies
- Source references from external frameworks
- Primers for complex concepts

**Current contents:**
- `comparative_studies/2026-02-05-spec-kitty-comparative-analysis.md` — Spec-driven development comparison
- `comparative_studies/references/` — spec-kitty source files (README, AGENTS, spec-driven methodology)

**When to use:** Understanding design rationale, comparing approaches, learning from external frameworks

---

### `/docs/styleguides/` — Language-Specific Style Guides (4 files)
**Purpose:** Writing style rules and language-specific conventions  
**Contents:**
- Java guidelines
- Python conventions
- Version control hygiene
- General styleguide principles

**When to use:** Code review, establishing coding standards, onboarding to language conventions

---

### `/templates/` — Output Structure Templates (80 files)
**Purpose:** Pre-defined structures for consistent artifact creation  
**Contents:**
- Agent task templates (descriptors, worklogs, assessments)
- Architecture templates (ADRs, design visions, technical designs)
- Automation templates (agent profiles, framework audits)
- Checklists (tool review, repo setup)
- Diagramming examples (PlantUML themes)
- Project templates (vision, changelog, guidelines)
- Specification templates

**Subdirectories:**
- `agent-tasks/` — Task YAML descriptors, worklogs
- `architecture/` — ADRs, design docs, roadmaps
- `automation/` — Framework audit reports, agent templates
- `checklists/` — Derivative repo setup, quarterly tool reviews
- `diagramming/` — PlantUML examples and themes
- `LEX/` — Lexical analysis outputs
- `project/` — Vision, changelog, guidelines
- `prompts/` — Prompt templates for common tasks
- `schemas/` — Agent migration schemas
- `specifications/` — Feature specification templates
- `structure/` — Repo maps, surfaces, workflows

**When to use:** Creating standardized artifacts, ensuring required sections included

---

## Path Parameterization

All files use configurable path variables (defaults shown):

| Variable | Default | Description |
|----------|---------|-------------|
| `${WORKSPACE_ROOT}` | `work` | Orchestration workspace for tasks, reports, coordination |
| `${DOC_ROOT}` | `docs` | Repository documentation root |
| `${SPEC_ROOT}` | `specifications` | Specification files location |
| `${OUTPUT_ROOT}` | `output` | Output directory for generated artifacts |

**Configuration:** Create `.doctrine/config.yaml` in consuming repository to override defaults.

---

## Quick Navigation

### I want to...

**Understand the framework:**
- Read `DOCTRINE_STACK.md` for architecture
- Read `GLOSSARY.md` for terminology
- Explore `guidelines/` for operational principles

**Create a new agent:**
- Review `agents/` for existing profiles
- Use `templates/automation/NEW_SPECIALIST.agent.md` template
- Follow `directives/005_agent_profiles.md` standards

**Set up task orchestration:**
- Read `approaches/work-directory-orchestration.md`
- Follow `directives/019_file_based_collaboration.md`
- Use templates in `templates/agent-tasks/`

**Document a decision:**
- Read `approaches/decision-first-development.md`
- Follow `directives/018_traceable_decisions.md`
- Use `templates/architecture/adr.md` template

**Implement TDD/ATDD:**
- Read `directives/017_test_driven_development.md`
- Read `directives/016_acceptance_test_driven_development.md`
- Apply `tactics/ATDD_adversarial-acceptance.tactic.md`

**Style/format code:**
- Check `docs/styleguides/` for language-specific rules
- Follow version control hygiene guidelines

---

## Framework Metadata

- **Version:** 1.0.0
- **Last Updated:** 2026-02-07
- **Total Files:** 201
- **External Dependencies:** Zero (self-contained)
- **Distribution:** Git subtree recommended
- **License:** See repository root LICENSE file

---

## Notes

- **Zero Dependencies:** This directory is fully self-contained and portable
- **Path Variables:** All references use `${VARIABLE}` syntax for configurability
- **Tool Agnostic:** Content is tool-neutral; exporters generate tool-specific formats
- **Versioned:** Framework follows semantic versioning (MAJOR.MINOR.PATCH)
- **Exportable:** Can be extracted and used in other repositories via Git subtree

---

## See Also

- **AGENTS.md** (repository root) — Agent initialization protocol
- **specific_guidelines.md** (repository root) — Repository-specific rules
- `.doctrine/config.yaml` — Path configuration overrides (create in consuming repo)
- `.github/instructions/` — Generated Copilot skills (exported from doctrine/)
- `.claude/skills/` — Generated Claude skills (exported from doctrine/)
