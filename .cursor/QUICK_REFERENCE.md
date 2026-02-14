# Cursor Quick Reference Guide

**Purpose:** Fast-access index for Cursor agents working with the doctrine stack

---

## 🚀 Quick Start

1. **Bootstrap:** Read `doctrine/guidelines/bootstrap.md`
2. **Create log:** `work/YYYY-MM-DD-[task].md`
3. **Load as needed:** Directives, agents, tactics from `doctrine/`

---

## 📚 Directive Index

| Code | Name | When to Use |
|------|------|-------------|
| **001** | CLI & Shell Tooling | Using fd/rg/ast-grep/jq/yq/fzf |
| **016** | Acceptance Test-Driven Dev | Writing acceptance tests (Given/When/Then) |
| **017** | Test-Driven Development | Unit testing workflow (RED-GREEN-REFACTOR) |
| **018** | Traceable Decisions | Creating ADRs or design docs |
| **019** | File-Based Collaboration | Multi-agent orchestration via YAML tasks |
| **020** | Locality of Change | Evaluating optimization necessity |
| **024** | Self-Observation Protocol | Mid-execution course correction |
| **028** | Bug Fixing Techniques | Test-first bug fixing (recommended) |
| **034** | Specification-Driven Dev | Writing functional specs before code |
| **036** | Boy Scout Rule | Pre-task code cleanup (mandatory) |

**Full list:** `doctrine/directives/` (36+ directives)

**Load pattern:** Read `doctrine/directives/NNN_name.md`

---

## 🎯 Tactics Catalog

**Location:** `doctrine/tactics/*.tactic.md`

### Workflow Tactics
- `stopping-conditions.tactic.md` - Define clear exit criteria
- `safe-to-fail-experiment-design.tactic.md` - Structured exploration
- `premortem-risk-identification.tactic.md` - Find failure modes early

### Testing Tactics
- `ATDD_adversarial-acceptance.tactic.md` - Red team acceptance tests
- `ATDD_assertion-clarity.tactic.md` - Clear test assertions
- `ATDD_boundary-analysis.tactic.md` - Edge case identification
- `ATDD_given-when-then-structure.tactic.md` - BDD test structure

### Design Tactics
- `incremental-diagramming.tactic.md` - Progressive detail in diagrams
- `design-by-contract.tactic.md` - Interface contracts

**Discovery:** Read `doctrine/tactics/README.md` for full catalog

---

## 👥 Specialist Agents

**Location:** `doctrine/agents/*.agent.md`

### Core Development
| Agent | File | Use For |
|-------|------|---------|
| **Python Pedro** | `python-pedro.agent.md` | Python development, ATDD/TDD |
| **Java Jenny** | `java-jenny.agent.md` | Java development, style enforcement |
| **Backend Benny** | `backend-dev.agent.md` | Service architecture, APIs |
| **Frontend Freddy** | `frontend.agent.md` | UI/UX, component design |
| **DevOps Danny** | `build-automation.agent.md` | CI/CD, deployment pipelines |

### Architecture & Design
| Agent | File | Use For |
|-------|------|---------|
| **Architect Alphonso** | `architect.agent.md` | System design, ADRs, trade-offs |
| **Diagram Daisy** | `diagrammer.agent.md` | PlantUML diagrams, visualizations |

### Quality & Maintenance
| Agent | File | Use For |
|-------|------|---------|
| **Code Reviewer Cindy** | `code-reviewer-cindy.agent.md` | Code reviews, quality checks |
| **Curator Claire** | `curator.agent.md` | Consistency, metadata, integrity |
| **Lexical Larry** | `lexical.agent.md` | Style enforcement, minimal edits |

### Coordination & Documentation
| Agent | File | Use For |
|-------|------|---------|
| **Manager Mike** | `manager.agent.md` | Multi-agent coordination, routing |
| **Planning Petra** | `project-planner.agent.md` | Strategic planning, roadmaps |
| **Scribe Sally** | `scribe.agent.md` | Documentation, traceable records |
| **Synthesizer Sam** | `synthesizer.agent.md` | Integration, insight consolidation |
| **Editor Eddy** | `writer-editor.agent.md` | Content revision, tone alignment |

### Specialized Roles
| Agent | File | Use For |
|-------|------|---------|
| **Analyst Annie** | `analyst-annie.agent.md` | Requirements, specifications, validation |
| **Researcher Ralph** | `researcher.agent.md` | Research, evidence gathering, SWOT |
| **Translator Tanya** | `translator.agent.md` | Cross-language translation |
| **Bootstrap Bill** | `bootstrap-bill.agent.md` | Repository setup, scaffolding |
| **Framework Guardian** | `framework-guardian.agent.md` | Framework audits, safe upgrades |

**Total:** 21 agents

**Loading:** Read `doctrine/agents/[agent-file].agent.md` when specializing

---

## 🧠 Approaches (Mental Models)

**Location:** `doctrine/approaches/*.md`

### Development Philosophy
- `trunk-based-development.md` - Branching strategy
- `decision-first-development.md` - Decision capture workflow
- `locality-of-change.md` - Optimization evaluation

### Testing & Quality
- `test-first-bug-fixing.md` - Bug fixing approach (comprehensive)
- `bug-fixing-checklist.md` - Quick reference for bug fixes

### Design Patterns
- `design-by-contract.md` - Interface design contracts
- `incremental-detail.md` - Progressive elaboration

**Discovery:** Browse `doctrine/approaches/` for full catalog

---

## 📋 Common Workflows

### 1. Architecture Decision Record (ADR)

```bash
# Load context
Read: doctrine/agents/architect.agent.md
Read: doctrine/directives/018_traceable_decisions.md
Read: doctrine/templates/architecture/adr.md

# Create ADR
Location: docs/architecture/adrs/ADR-NNN-title.md
Format: Use template sections (Context, Decision, Consequences)
```

### 2. Test-Driven Development

```bash
# Load context
Read: doctrine/directives/017_test_driven_development.md

# TDD cycle
1. Write failing test (RED)
2. Implement minimal code (GREEN)
3. Refactor for clarity (REFACTOR)
4. Commit test + implementation together
```

### 3. Acceptance Test-Driven Development

```bash
# Load context
Read: doctrine/directives/016_acceptance_test_driven_development.md
Read: doctrine/tactics/ATDD_given-when-then-structure.tactic.md

# ATDD workflow
1. Write acceptance criteria (Given/When/Then)
2. Implement acceptance test (fails)
3. Implement feature (test passes)
4. Verify with stakeholder scenarios
```

### 4. Bug Fixing (Test-First)

```bash
# Load context
Read: doctrine/directives/028_bugfixing_techniques.md

# Bug fix workflow
1. Write test that reproduces bug (RED)
2. Verify test fails for RIGHT reason
3. Fix code (GREEN)
4. Run ALL tests (no regressions)
5. Commit test + fix together
```

### 5. Multi-Agent Task Execution

```bash
# Load context
Read: doctrine/directives/019_file_based_collaboration.md

# Task workflow
1. Read task: work/collaboration/inbox/[task].yaml
2. Update status: work/coordination/AGENT_STATUS.md
3. Execute work
4. Update task status → done/
5. Create handoff if needed: work/coordination/HANDOFFS.md
```

### 6. Boy Scout Rule (Pre-Task Cleanup)

```bash
# Load context
Read: doctrine/directives/036_boy_scout_rule.md

# Cleanup workflow
1. Spot check: Review files you'll touch
2. Fix obvious issues (formatting, typos, dead code)
3. Keep changes small (5-10 line fixes)
4. Commit cleanup separately BEFORE feature work
```

---

## 🗂️ Repository Navigation

### Key Directories

```
doctrine/              # Agentic framework (portable)
├── agents/           # Specialist profiles (21)
├── directives/       # Instructions (001-036+)
├── tactics/          # Procedures (*.tactic.md)
├── approaches/       # Mental models
├── guidelines/       # Core principles
└── templates/        # Output contracts

work/                 # Orchestration workspace
├── collaboration/    # Multi-agent tasks
│   ├── inbox/       # New tasks
│   ├── assigned/    # In-progress tasks
│   └── done/        # Completed tasks
├── coordination/     # Agent status tracking
├── logs/            # Execution logs
└── notes/           # Scratch work

docs/                # Documentation
├── architecture/    # ADRs, design docs
│   └── adrs/       # Architecture decisions
├── templates/       # Output structure guides
└── HOW_TO_USE/     # Setup guides

src/                 # Production code
├── framework/       # Core runtime
└── llm_service/     # Dashboard service

tests/               # Test suites
tools/               # Development utilities
```

### Key Files

- `AGENTS.md` - Full agent specification (load for high-stakes work)
- `CLAUDE.md` - Quick project reference
- `.cursorrules` - This minimal context (auto-loaded)
- `doctrine/DOCTRINE_STACK.md` - Stack architecture
- `doctrine/GLOSSARY.md` - Terminology reference

---

## 🎨 Output Standards

### Markdown Code References

**Existing code:**
```markdown
\`\`\`startLine:endLine:filepath
// code content
\`\`\`
```

**New/proposed code:**
```markdown
\`\`\`python
# new code
\`\`\`
```

**Rules:**
- Never indent triple backticks
- Always add newline before code fence
- Include at least 1 line of code (no empty blocks)

### Integrity Symbols

- ✅ Success, alignment confirmed
- ⚠️ Low confidence, assumptions made
- ❗️ Critical error, misalignment

### Work Logs

**Location:** `work/YYYY-MM-DD-[task-name].md`

**Required sections:**
- Date, task understanding
- Next 2-3 steps
- Aliases/commands used
- Integrity flags (✅/⚠️/❗️)

---

## 🔧 Development Commands

```bash
# Testing
python -m pytest                    # All tests
python -m pytest tests/unit/        # Unit tests only
python -m pytest tests/integration/ # Integration tests
python -m pytest -k "test_name"     # Specific test

# Export distributions
npm run export:all                  # All formats
npm run export:claude               # Claude skills
npm run deploy:claude               # Deploy Claude artifacts

# JavaScript testing
npm test                            # Run JS tests

# Validation
node validate-schemas.js            # Validate JSON schemas
```

---

## 🔍 Search Patterns

### Finding Directives
```bash
# By number
Read: doctrine/directives/NNN_name.md

# By topic
Browse: doctrine/directives/README.md
```

### Finding Tactics
```bash
# By name
Read: doctrine/tactics/[name].tactic.md

# Browse catalog
Read: doctrine/tactics/README.md
```

### Finding Agents
```bash
# By role
Read: doctrine/agents/[agent-name].agent.md

# Browse roster
Read: doctrine/agents/README.md
```

---

## 🎯 Decision Trees

### "Which directive should I load?"

- **Testing?** → 016 (ATDD) or 017 (TDD)
- **Architecture?** → 018 (Traceable Decisions)
- **Bug fix?** → 028 (Bug Fixing Techniques)
- **Optimization?** → 020 (Locality of Change)
- **Multi-agent?** → 019 (File-Based Collaboration)
- **Cleanup?** → 036 (Boy Scout Rule)
- **Spec writing?** → 034 (Specification-Driven Dev)

### "Which agent should I load?"

- **Python code?** → Python Pedro
- **Java code?** → Java Jenny
- **System design?** → Architect Alphonso
- **API design?** → Backend Benny
- **UI work?** → Frontend Freddy
- **CI/CD?** → DevOps Danny
- **Code review?** → Code Reviewer Cindy
- **Consistency check?** → Curator Claire
- **Research?** → Researcher Ralph
- **Planning?** → Planning Petra

### "Which tactic should I use?"

- **Define done?** → `stopping-conditions.tactic.md`
- **Risk analysis?** → `premortem-risk-identification.tactic.md`
- **Acceptance test?** → `ATDD_given-when-then-structure.tactic.md`
- **Experiment?** → `safe-to-fail-experiment-design.tactic.md`
- **Diagram?** → `incremental-diagramming.tactic.md`

---

## 📖 Further Reading

- **Full Specification:** `AGENTS.md` (~3,850 tokens)
- **Doctrine Overview:** `doctrine/DOCTRINE_STACK.md`
- **Bootstrap Guide:** `doctrine/guidelines/bootstrap.md`
- **Runtime Sheet:** `doctrine/guidelines/runtime_sheet.md`
- **Glossary:** `doctrine/GLOSSARY.md`
- **Distribution Design:** `docs/architecture/design/DOCTRINE_DISTRIBUTION.md`

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-10  
**Purpose:** Fast reference for Cursor agents  
**Token Cost:** ~800 tokens (vs 3,850 for full AGENTS.md)

---

**Usage Note:** This file is optimized for quick lookups. For comprehensive guidance, load the full doctrine stack from `doctrine/` and `AGENTS.md`.
