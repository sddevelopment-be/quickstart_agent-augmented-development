# SD Development: AI-Augmented Workflow Starter Repo

_Version: 1.1.0_  
_Last updated: 2026-02-08_

[![SonarQube Cloud](https://sonarcloud.io/images/project_badges/sonarcloud-dark.svg)](https://sonarcloud.io/summary/new_code?id=sddevelopment-be_quickstart_agent-augmented-development)

This repository is a **quickstart template** for AI-augmented / agentic workflows built on a **doctrine stack**: a five-layer governance system that separates values, models, instructions, procedures, and structure for predictable, inspectable agent behavior.

## The Doctrine Stack

Five layers with clear precedence ensure consistent, predictable agent behavior:

```
Guidelines (values)       ← Highest precedence
    ↓
Approaches (models)       
    ↓
Directives (instructions) ← Select tactics
    ↓
Tactics (procedures)      ← Execute work
    ↓
Templates (structure)     ← Lowest precedence
```

**How it works:**
- **Guidelines** define values and preferences (what matters most)
- **Approaches** provide mental models and philosophies (how to think)
- **Directives** give explicit instructions and constraints (what to do)
- **Tactics** execute work procedurally (step-by-step how)
- **Templates** provide output structure contracts (format)

**Key Principles:**
- Directives select which tactics to invoke
- Tactics execute the work procedurally
- Human retains approval authority ("Human in Charge")
- Modular loading minimizes token consumption

[📖 Read: Doctrine Stack Documentation](doctrine/DOCTRINE_STACK.md)  
[📖 Browse: Tactics Index](doctrine/tactics/README.md)  
[📖 See: Agent Profiles](doctrine/agents/)  
[📖 Reference: Glossary](doctrine/GLOSSARY.md)

## Repository Structure

```
doctrine/                      # Portable agentic framework (git subtree distributable)
├── DOCTRINE_STACK.md         # Five-layer governance framework
├── GLOSSARY.md               # Standardized terminology
├── guidelines/               # Values and preferences
├── approaches/               # Mental models and philosophies
├── directives/               # Modular operational instructions (20+)
├── tactics/                  # Procedural execution guides (9 tactics)
├── templates/                # Output structure contracts
└── agents/                   # Specialized agent profiles (20 agents)

docs/                         # Project intent and architecture
├── VISION.md                 # Repository purpose
├── architecture/             # Strategic decisions
│   ├── architectural_vision.md
│   ├── adrs/                 # Architecture Decision Records
│   └── diagrams/             # PlantUML C4 diagrams
└── templates/                # Additional output templates

.doctrine-config/             # Project-specific configuration
└── repository-guidelines.md  # Project-specific constraints

work/                         # Multi-agent coordination
├── collaboration/            # Task orchestration and handoffs
├── reports/logs/             # Agent work logs
└── notes/                    # Exploratory work

src/                          # Production code
tools/                        # Development utilities
tests/                        # All test code
```

[📖 Read: Repository Quick Reference](doctrine/directives/003_repository_quick_reference.md)

## Quick Start

1. **Initialize your project**
   ```bash
   # Fork this repository
   # Edit docs/VISION.md and .doctrine-config/repository-guidelines.md
   ```

2. **Review the doctrine stack**
   - Read [doctrine/DOCTRINE_STACK.md](doctrine/DOCTRINE_STACK.md) to understand the five-layer model
   - Browse [doctrine/tactics/README.md](doctrine/tactics/README.md) to see available tactics
   - Review [doctrine/guidelines/general_guidelines.md](doctrine/guidelines/general_guidelines.md) for core principles

3. **Start working with agents**
   - Use the specialist agents in [doctrine/agents/](doctrine/agents/)
   - On GitHub, use the 'agents panel' (top-right icon) or assign issues to agents
   - Follow file-based orchestration via `work/collaboration/`

[📖 See: Architectural Vision](docs/architecture/architectural_vision.md)  
[📊 View: Doctrine Stack Diagram](docs/architecture/diagrams/doctrine-stack-c4.svg)

## What's New

**Version 1.1.0 (2026-02-08):**
- ✨ **Doctrine Stack Integration**: Five-layer governance framework (Guidelines → Approaches → Directives → Tactics → Templates)
- 🛠️ **9 Procedural Tactics**: Stopping conditions, premortem, adversarial testing, AMMERSE, safe-to-fail, ATDD adversarial, test boundaries, input validation, code review
- 🔍 **Hybrid Discovery**: Directive-driven invocation + exploratory README discovery
- 📋 **Updated Directives**: 5 directives now explicitly invoke tactics (016, 017, 018, 021, 024)
- 📊 **Architecture Diagrams**: C4 PlantUML diagram for doctrine stack visualization
- 🎯 **Dashboard Features**: Real-time monitoring, file-based orchestration, WebSocket integration

[📋 See: PR #132 - Doctrine Stack & Tactics Integration](https://github.com/sddevelopment-be/quickstart_agent-augmented-development/pull/132)

---

## Acknowledgements & Inspiration

This project draws inspiration from and acknowledges several pioneering works in AI-augmented development:

### Augmented Coding Patterns
**Source:** [lexler.github.io/augmented-coding-patterns](https://lexler.github.io/augmented-coding-patterns/)  
**Author:** [@lexler](https://github.com/lexler)  

Comprehensive patterns and practices for integrating AI assistants into software development workflows. Essential reading for anyone building AI-augmented development systems.

### Agents.md Specification
**Source:** [agents.md](https://agents.md/)  

Community-driven specification for AI agent behavior and interaction patterns. Provides standardized approaches for agent definition and orchestration.

### spec-kitty

**Source:** [github.com/Priivacy-ai/spec-kitty](https://github.com/Priivacy-ai/spec-kitty)  
**License:** MIT  
**Contributions:**

- **Specification-Driven Development methodology** (adapted) - Code serves specifications, not vice versa
- **Dashboard interface design patterns** - Live kanban board with WebSocket updates for real-time workflow visibility
- **Multi-agent orchestration insights** - Work package lane management and agent coordination patterns
- **Template-based configuration approach** - Quick-start templates with variable substitution and environment scanning
- **Rich CLI feedback** - Extensive use of the `rich` library for structured, colorful terminal output with progress indicators

We're grateful to the spec-kitty team for their innovative work in agent-augmented development. Their `spec-driven.md` guide and comparative architectural patterns have been particularly influential in shaping our workflow patterns and user experience enhancements.

**Comparative Analysis:** See [docs/architecture/design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md](docs/architecture/design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md) for detailed analysis of adopted patterns.

---

**Template Status:** This repository serves as both a working example and a reusable template. Fork and adapt for your project needs.

