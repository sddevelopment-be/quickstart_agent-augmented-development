# Vision: Agent-Augmented Development Framework

_Version: 2.0.0_  
_Last Updated: 2026-02-14_  
_Agent: Editor Eddy_  
_Purpose: Strategic vision and long-term direction_

---

## Executive Summary

The **quickstart_agent-augmented-development** repository serves as a **production-ready template and reference implementation** for teams adopting AI-augmented development workflows. Built on the **Doctrine Stack**—a five-layer governance framework—it enables **predictable, inspectable, and repeatable agent behavior** through explicit instruction hierarchies, procedural tactics, and file-based orchestration.

### Mission Statement

**Empower development teams to augment their workflows with AI agents through a structured, maintainable, and portable framework that preserves human authority while amplifying productivity and consistency.**

---

## The Problem We Solve

### Current Challenges in AI-Augmented Development

Teams adopting AI-augmented workflows face critical challenges:

| Challenge | Impact | Cost |
|-----------|--------|------|
| **Token Inefficiency** | Monolithic agent instructions consume excessive context window space | Limited task complexity, reduced agent capability |
| **Maintenance Overhead** | Scattered or duplicated governance content | Difficult to update behavioral norms consistently |
| **Portability Barriers** | Vendor-specific or proprietary agent configurations | Lock-in to specific LLM toolchains |
| **Quality Inconsistency** | No standardized patterns | Varying output formats and quality levels |
| **Collaboration Friction** | Unclear handoff protocols | Rework, misalignment, lost context |
| **Behavioral Drift** | Agents over-interpret vague intent | Unpredictable results, wasted iterations |
| **Governance Gaps** | No clear precedence hierarchy | Conflicting instructions, ethical risks |
| **Onboarding Difficulty** | No clear entry points for new agents/humans | Steep learning curve, slow adoption |

### What's Missing

Current AI-augmented development approaches lack structured governance:

- Ad-hoc prompt engineering without systematic instruction hierarchies
- Conversational paradigms that don't scale to complex, multi-step workflows
- Insufficient coordination patterns for multi-agent collaboration
- No standardized artifact formats for cross-tool compatibility
- Weak traceability for decisions and changes
- Inconsistent application of test-first discipline

---

## Our Solution: The Doctrine Stack

### Five-Layer Governance Framework

We introduce a **layered instruction system** that separates concerns and establishes clear precedence:

```
┌─────────────────────────────────────────────┐
│ Guidelines (values, preferences)            │ ← Highest precedence
├─────────────────────────────────────────────┤
│ Approaches (mental models, philosophies)    │
├─────────────────────────────────────────────┤
│ Directives (instructions, constraints)      │ ← Select tactics
├─────────────────────────────────────────────┤
│ Tactics (procedural execution guides)       │ ← Execute work
├─────────────────────────────────────────────┤
│ Templates (output structure contracts)      │ ← Lowest precedence
└─────────────────────────────────────────────┘
```

**Key Insight:** **Directives select tactics; tactics execute work procedurally.** This separation eliminates ambiguity while preserving human approval authority.

### Core Principles

1. **Human in Charge** - Agents are executors under explicit doctrine, not autonomous decision-makers
2. **Predictable Behavior** - Externalized judgment eliminates guesswork
3. **Inspectable Operations** - Every action traceable to governing instruction
4. **Repeatable Workflows** - Stateless agents following consistent protocols
5. **Modular Loading** - Load only relevant instructions (token efficiency)
6. **Cross-Platform Portability** - Markdown-based governance works with any LLM
7. **Test-First Discipline** - ATDD and TDD workflows mandatory (Directives 016, 017)
8. **Traceable Decisions** - Architecture Decision Records for all major choices (Directive 018)

### Core Capabilities

| Capability | Benefit |
|------------|---------|
| **Doctrine Stack** | Layered governance with clear precedence |
| **File-Based Orchestration** | All state visible in Git, no central server |
| **Procedural Tactics** | Step-by-step execution guides |
| **Specialist Agents** | Clear boundaries, explicit collaboration rules |
| **Zero Dependencies** | Doctrine distributable via git subtree |
| **Domain Model API** | Type-safe programmatic access (ADR-045) |
| **Test-First Mandate** | ATDD + TDD enforced via directives |
| **ADR-Driven Architecture** | Complete traceability and rationale |

---

## Vision for Success

### Desired Outcomes

This repository is successful when:

#### For Development Teams

- ✅ **Token efficiency:** Agents consume significantly less context via modular directive loading
- ✅ **Quality maintainability:** Update single directives without touching unrelated content
- ✅ **Cross-toolchain portability:** Directives work with any LLM supporting markdown
- ✅ **Consistent outputs:** Agents produce standardized artifacts following templates
- ✅ **Smooth collaboration:** Well-documented handoffs between agents and humans
- ✅ **Easy adoption:** Other projects reuse framework with minimal modification
- ✅ **High code quality:** Test-first discipline maintained across all code changes
- ✅ **Clear traceability:** Every major decision documented via ADRs

#### For Organizations

- ✅ **Reduced onboarding time:** New team members productive quickly
- ✅ **Lower maintenance costs:** Single-source governance updates propagate automatically
- ✅ **Improved audit compliance:** Complete decision trail via ADRs and work logs
- ✅ **Risk mitigation:** Explicit ethical guardrails and escalation protocols
- ✅ **Vendor independence:** Framework portable across LLM providers and tools

#### For the AI Community

- ✅ **Reusable patterns:** Doctrine framework adopted by other projects
- ✅ **Open standards:** Contribute to agents.md specification and OpenCode
- ✅ **Shared learnings:** Work logs and SWOT analyses improve prompting techniques
- ✅ **Research contributions:** Empirical data on multi-agent coordination effectiveness

---

## Scope Boundaries

### In Scope

✅ **Core Framework**
- Modular directive system for agent governance
- Specialized agent profiles with clear boundaries
- Procedural tactics for step-by-step execution
- Templates for common artifacts (ADRs, documentation, reports)
- Validation tooling for structural integrity
- Human-agent collaboration workflows via file-based orchestration
- Cross-project reusability patterns (git subtree distribution)
- Test-first development discipline (ATDD + TDD)
- Traceable decision capture (ADRs)

✅ **Development Tools**
- Agent profile exporters (Copilot, Claude, OpenCode)
- Task YAML validators and naming convention checkers
- Error reporting system (agent-friendly JSON/Markdown)
- Domain model API for programmatic doctrine access
- Live dashboard for task orchestration monitoring

✅ **Documentation & Training**
- Comprehensive guides for all personas
- Architecture decision records for major choices
- Work logs and prompt documentation (Directives 014, 015)
- Specification templates for feature requirements

### Explicitly Out of Scope

❌ **Not Building:**
- Fully autonomous agent execution without human oversight
- Real-time agent-to-agent communication (async coordination only)
- Database-backed directive storage or querying
- Vendor-specific LLM features or extensions
- Dynamic directive self-modification by agents
- Production code generation without human review
- Proprietary closed-source components
- SaaS hosting or cloud services

❌ **Not Responsible For:**
- LLM model training or fine-tuning
- Prompt optimization algorithms (agents use explicit directives)
- Natural language understanding (agents execute instructions)
- Complex reasoning (tactics provide step-by-step procedures)
- Creative content generation beyond defined templates

---

## Role of Agents

### Agents as Specialized Collaborators

Agents in this repository are **not** general-purpose AI assistants. They are **specialized executors** that:

1. **Load context selectively** - Only directives relevant to their role and current task
2. **Operate within boundaries** - Stay within defined specialization areas, escalate when uncertain
3. **Produce quality artifacts** - Follow templates, maintain consistency, cross-reference existing documentation
4. **Collaborate explicitly** - Use `work/` directory for coordination, respect handoff protocols
5. **Validate alignment** - Run integrity checks, use markers (✅ ⚠️ ❗️) to communicate confidence
6. **Enable human oversight** - Propose changes for approval, never modify `docs/` without permission
7. **Follow test-first discipline** - Write tests before code (Directives 016, 017, 028)
8. **Document decisions** - Create ADRs for architectural changes (Directive 018)
9. **Log work comprehensively** - Create work logs with metrics (Directive 014)
10. **Leave code better** - Apply Boy Scout Rule on every task (Directive 036)

### What Agents Are NOT

- ❌ **Not decision-makers** on strategic direction or architecture
- ❌ **Not autonomous** - Require explicit directives for all actions
- ❌ **Not creative** - Follow procedural tactics, not improvisation
- ❌ **Not flexible** - Bounded by specialization, escalate out-of-scope requests
- ❌ **Not conversational** - Execute instructions, don't negotiate intent
- ❌ **Not self-modifying** - Cannot change their own directives without explicit Human-in-Charge approval
- ❌ **Not responsible** - Human retains approval authority ("Human in Charge")

**See:** [`docs/audience/automation_agent.md`](docs/audience/automation_agent.md) for detailed agent responsibilities.

### Framework Customizability

The framework supports multiple levels of customization:

- **Centralized governance** via doctrine stack with **local overrides** per project
- **Modular directive loading** enables selective context inclusion
- **Extensible agent profiles** allow domain-specific specializations
- **Configurable feedback loops** (Directives 014, 015) capture work patterns and improve prompts over time

### Feedback and Learning

The framework incorporates multiple feedback mechanisms:

- **Work logs** (Directive 014) document metrics, decisions, and blockers
- **Prompt documentation** (Directive 015) captures effective prompt patterns for reuse
- **ADRs** (Directive 018) preserve architectural rationale
- **Boy Scout Rule** (Directive 036) ensures continuous incremental improvement

These feedback loops enable systematic refinement of tactics, directives, and agent profiles based on empirical outcomes.

---

## Target Audiences

### Primary Audiences

1. **Development Teams** - Using agents to augment daily workflows
   - Software engineers, DevOps, QA engineers
   - Need: Productivity boost, consistent quality, reduced cognitive load
   - Value: Test-first discipline, standardized artifacts, clear handoffs

2. **Architects & Technical Leaders** - Designing agent-augmented systems
   - Solution architects, technical leads, engineering managers
   - Need: Governance frameworks, traceability, risk mitigation
   - Value: ADR-driven decisions, explicit precedence, audit trail

3. **Framework Users & Implementers** - Adopting framework in their projects
   - Organizations evaluating AI-augmented development
   - Need: Portable, maintainable, proven patterns
   - Value: Git subtree distribution, zero dependencies, reference implementation

### Secondary Audiences

4. **AI Researchers** - Studying multi-agent coordination
   - Need: Empirical data, benchmarking, reproducible experiments
   - Value: Complete work logs, metrics, decision rationale

5. **Open Source Contributors** - Improving and extending framework
   - Need: Clear contribution guidelines, modular architecture
   - Value: Well-documented codebase, comprehensive tests, ADRs

6. **Educators & Trainers** - Teaching AI-augmented development
   - Need: Pedagogical materials, best practices, case studies
   - Value: Reference implementation, complete documentation

---

## Core Use Cases

For detailed workflow patterns and practical examples, see:

**[doctrine/docs/workflows/core-use-cases.md](doctrine/docs/workflows/core-use-cases.md)**

This document covers:
- Repository bootstrapping
- Multi-agent feature development
- Code quality improvement
- Documentation maintenance
- Specification-driven development

---

## Technology Stack

### Core Technologies

| Technology | Purpose | Version | Rationale |
|------------|---------|---------|-----------|
| **Markdown** | Doctrine content | N/A | Universal, readable, version-controllable |
| **YAML** | Task orchestration | 1.2 | Human-readable, JSON-compatible, well-supported |
| **Python** | Framework runtime | 3.11+ | Rich ecosystem, LLM-friendly, type hints |
| **Git** | State management | 2.x | Distributed, auditable, time-travel |
| **PlantUML** | Diagrams | Latest | Text-based, version-controllable, powerful |
| **JSON Schema** | Validation | Draft 7 | Standard, tool support, clear error messages |

### Testing & Quality

| Tool | Purpose | Coverage |
|------|---------|----------|
| **pytest** | Testing framework | 665 tests (88.7%) |
| **pytest-cov** | Coverage reporting | 92% (domain models) |
| **Black** | Code formatting | 100% |
| **Ruff** | Linting | 562 issues auto-fixed |
| **mypy** | Type checking | Gradual adoption |
| **SonarCloud** | Code quality | Health score 70/100 |

### CLI Tools (Directive 001)

| Tool | Purpose | Use Case |
|------|---------|----------|
| **ripgrep (rg)** | Fast text search | Find references, patterns |
| **fd** | Fast file finding | Locate files by name/pattern |
| **ast-grep** | AST-based search | Structural code queries |
| **jq** | JSON processing | Parse validation results |
| **yq** | YAML processing | Task YAML manipulation |
| **fzf** | Fuzzy finder | Interactive file selection |

### Integrations

| Platform | Integration | Status |
|----------|-------------|--------|
| **GitHub Copilot** | Native profiles | ✅ Supported (exporter available) |
| **Claude Desktop** | Custom skills | ✅ Supported (exporter available) |
| **Cursor** | Inline directives | 🔄 Planned |
| **OpenCode** | Cross-platform | ✅ Supported (exporter available) |
| **VSCode** | Extension | 🔄 Planned |
| **JetBrains** | Plugin | 🔄 Planned |

---

## Guiding Philosophy

### "Boring is Better"

We deliberately choose **predictability over creativity**:

- **Explicit > Implicit** - Instructions are spelled out, not inferred
- **Procedural > Conversational** - Tactics provide steps, not advice
- **Stateless > Stateful** - Agents reload context each time
- **Markdown > Databases** - Text files in Git, not proprietary storage
- **File-Based > API-Based** - Orchestration visible in file system
- **Precedence > Negotiation** - Clear hierarchy, no conflicts

### "Human in Charge"

Agents are **executors under doctrine**, not autonomous decision-makers:

- Agents **propose**, humans **approve**
- Agents **follow** directives, humans **create** directives
- Agents **escalate** uncertainty, humans **resolve** ambiguity
- Agents **execute** tactics, humans **validate** results
- Agents **document** work, humans **review** documentation

### "Test-First or Nothing"

Quality is **non-negotiable**:

- **ATDD** (Directive 016) - Write acceptance tests before features
- **TDD** (Directive 017) - Write unit tests before code
- **Bug Test-First** (Directive 028) - Write failing test, then fix
- **No Exceptions** - Test-first mandate applies to all code changes
- **No Shortcuts** - Tests must pass before merging

### "Decisions are Assets"

Every major choice is **captured and traceable**:

- **ADRs** (Directive 018) - Architecture Decision Records for all major decisions
- **Status Tracking** - Proposed → Accepted → Deprecated → Superseded
- **Consequence Documentation** - Positive, negative, and neutral impacts
- **Context Preservation** - Why the decision was made, not just what
- **Linkage** - ADRs linked to specifications, tests, implementation

---

## Risks & Mitigations

### Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Framework Module Conflict** | 85 skipped tests | High | Rename `/framework/` to `/legacy_framework/` or consolidate |
| **Token Window Limits** | Agents can't load full context | Medium | Modular directive loading, tactic selection |
| **Coordination Complexity** | Handoffs fail or get lost | Low | Explicit handoff logs, orchestrator monitoring |
| **Doctrine Drift** | Agents ignore directives | Low | Validation checks, alignment commands |
| **Test Maintenance Burden** | Tests become brittle | Medium | Focus on behavior tests, not implementation tests |

### Organizational Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Adoption Resistance** | Teams reject framework | Medium | Strong documentation, quick wins (Sprint 1 case study) |
| **Learning Curve** | Slow onboarding | Medium | Comprehensive guides, persona-specific entry points |
| **Governance Overhead** | Too many directives/tactics | Low | Keep guidelines stable, evolve directives gradually |
| **Human Bottleneck** | Agents wait for approvals | High | Clear escalation protocols, batch reviews |
| **Vendor Lock-In (LLM)** | Dependence on single provider | Low | Cross-platform design, OpenCode integration |

### Ethical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Bias Amplification** | Agents perpetuate biases | Medium | Explicit ethical guidelines, human review gates |
| **Over-Reliance** | Humans defer to agents | Medium | "Human in Charge" principle, approval authority |
| **Job Displacement** | Reduced employment | High | Focus on augmentation, not replacement |
| **Intellectual Property** | Unclear code ownership | Low | Clear licenses, human authorship retained |
| **Security Vulnerabilities** | Agents introduce bugs | Medium | Test-first mandate, security review (Directive 036) |

---

## Related Documents

- **[REPO_MAP.md](REPO_MAP.md)** - Complete repository structure and navigation
- **[SURFACES.md](SURFACES.md)** - API surfaces and integration points
- **[docs/WORKFLOWS.md](docs/WORKFLOWS.md)** - Detailed workflow patterns
- **[doctrine/DOCTRINE_STACK.md](doctrine/DOCTRINE_STACK.md)** - Five-layer governance framework
- **[doctrine/docs/workflows/core-use-cases.md](doctrine/docs/workflows/core-use-cases.md)** - Practical workflow examples
- **[work/reports/SPRINT1_EXECUTIVE_SUMMARY.md](work/reports/SPRINT1_EXECUTIVE_SUMMARY.md)** - Sprint 1 case study
- **[docs/architecture/adrs/README.md](docs/architecture/adrs/README.md)** - Architecture decision index

---

_Revised by Editor Eddy on 2026-02-14_  
_Original by Bootstrap Bill on 2026-02-13_  
_For updates: Assign task to appropriate agent via AGENTS.md_

---

**"Boring is better. Human in charge. Test-first or nothing. Decisions are assets."**
