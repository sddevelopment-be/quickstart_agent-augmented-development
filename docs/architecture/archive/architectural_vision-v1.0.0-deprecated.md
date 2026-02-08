# Architectural Vision: Agent-Augmented Development Repository

**Version:** 1.0.0  
**Last Updated:** 2025-11-17  
**Status:** Active

---

## Purpose

This repository serves as a **quickstart template and reference implementation
** for agent-augmented development workflows. It provides a structured, portable, and maintainable foundation for teams integrating AI agents into their software development processes.

## Core Principles

### 1. Token Efficiency

**Goal:** Minimize LLM context window consumption while maintaining quality and guideline adherence.

**Implementation:**

- Modular directive system with lazy loading
- Selective context assembly based on agent role and task
- Deduplication of shared governance content
- Lean core specification with external references

**Success Metric:** Agents consume 40-60% less context compared to monolithic governance approaches.

### 2. Maintainability

**Goal:** Enable sensible human-readable execution, minimizing review and maintenance overhead.

**Implementation:**

- Separation of concerns (core spec, directives, profiles, templates)
- Clear ownership and safety-critical flags
- Predictable structure with validation tooling
- Explicit versioning and change tracking

**Success Metric:** Developers can update specific directives without touching unrelated governance content.

### 3. Portability

**Goal:** Enable reuse across different LLM toolchains and projects.

**Implementation:**

- Markdown-first format (no vendor-specific syntax)
- Standardized manifest for metadata and dependencies
- Toolchain-agnostic patterns and templates
- Clear separation of intent, process, and artifacts

**Success Metric:** Directives and profiles can be adopted by other projects with minimal modification.

## Architectural Layers

### Overview: Five-Layer Doctrine Stack

The repository implements a **doctrine stack**: a layered governance system that separates concerns deliberately to enable predictable, inspectable, and repeatable agent behavior. Each layer has a distinct role with minimal overlap.

```
┌─────────────────────────────────────────────┐
│ 1. Guidelines (values, preferences)         │ ← Highest precedence
├─────────────────────────────────────────────┤
│ 2. Approaches (mental models, philosophies) │
├─────────────────────────────────────────────┤
│ 3. Directives (instructions, constraints)   │ ← Select tactics
├─────────────────────────────────────────────┤
│ 4. Tactics (procedural execution guides)    │ ← NEW: Execute work
├─────────────────────────────────────────────┤
│ 5. Templates (output structure contracts)   │
└─────────────────────────────────────────────┘
```

**Design Principle:** Directives *select* which tactics to invoke; tactics *execute* the work procedurally. This separation enables:
- Directive authority over what gets executed
- Tactic reuse across multiple directives
- Clear boundaries between policy (directives) and procedure (tactics)

### Layer 1: Core Governance (AGENTS.md)

**Responsibility:** Define universal agent behavior, initialization protocol, and safety guardrails.

**Contents:**

- Context stack priorities
- Runtime behavior defaults
- Integrity markers and escalation protocol
- Command interpretation logic
- Output requirements
- Extended directive index

**Design Decision:** Keep lean (~3KB) to minimize every agent's baseline context cost.

### Layer 2: Modular Directives (.github/agents/directives/)

**Responsibility:** Provide specialized operational guidance on specific topics. These are self-contained modules that agents can load as needed. Users can extend this layer with custom directives if desired, or activate/deactivate existing ones by updating the agent profiles ( [`.github/agents/*.agent.md`](/.github/agents/).

**Example Contents:**

- [001: CLI & Shell Tooling](/agents/directives/001_cli_shell_tooling.md)
- [002: Context Notes](/agents/directives/002_context_notes.md)
- [003: Repository Quick Reference](/agents/directives/003_repository_quick_reference.md)
- [004: Documentation & Context Files](/agents/directives/004_documentation_context_files.md)
- [005: Agent Profiles](/agents/directives/005_agent_profiles.md)
- [016: Acceptance Test-Driven Development](/agents/directives/016_acceptance_test_driven_development.md)
- [022: Audience-Oriented Writing](/agents/directives/022_audience_oriented_writing.md)

**Design Decision:** One directive = one concern. Load on-demand via `/require-directive <code>`.

### Layer 3: Approaches (.github/agents/approaches/)

**Responsibility:** Provide conceptual models and philosophies for reasoning. Explain *how problems are generally framed and explored*.

**Example Contents:**

- [Trunk-Based Development](/.github/agents/approaches/trunk-based-development.md)
- [Decision-First Development](/.github/agents/approaches/decision-first-development.md)
- [Locality of Change](/.github/agents/approaches/locality-of-change.md)
- [Ralph Wiggum Loop (Self-Observation)](/.github/agents/approaches/ralph-wiggum-loop.md)

**Design Decision:** Approaches justify *why* certain tactics or directives exist. They provide mental models for systemic reasoning and guide problem framing, not execution.

### Layer 4: Tactics (.github/agents/tactics/)

**Responsibility:** Define procedural execution guides for specific activities. Provide step-by-step instructions that agents follow to accomplish well-defined objectives.

**Repository Structure:**
```
.github/agents/tactics/
├── README.md                                   # Discovery index
├── stopping-conditions.tactic.md              # Exit criteria
├── premortem-risk-identification.tactic.md    # Risk discovery
├── adversarial-testing.tactic.md              # Stress-testing
├── ammerse-analysis.tactic.md                 # Trade-off analysis
├── safe-to-fail-experiment-design.tactic.md   # Exploration
├── ATDD_adversarial-acceptance.tactic.md      # Acceptance testing
├── test-boundaries-by-responsibility.tactic.md# Test scoping
├── input-validation-fail-fast.tactic.md       # Validation patterns
└── code-review-incremental.tactic.md          # Code review
```

**Characteristics:**
- **Procedural:** Step-by-step actions, not advisory
- **Bounded:** Clear preconditions, exclusions, exit criteria
- **Verifiable:** Concrete outputs, measurable completion signals
- **Failure-aware:** Explicit failure modes documented
- **Invoked:** Either by directive mandate or exploratory discovery (with Human approval)

**Discovery Mechanism:**
1. **Primary:** Directives explicitly invoke tactics at workflow steps
2. **Secondary:** Agents discover via `.github/agents/tactics/README.md` and propose to Human

**Example Invocation (from Directive 024):**
> Task initialization — Define stopping conditions: Invoke `tactics/stopping-conditions.tactic.md` before starting long-running tasks

**Design Decision:** Tactics sit between Directives (which select what to do) and Templates (which define output shape). This enables:
- Reusable procedures across directives
- Systematic execution without creative interpretation
- Clear ownership: directives select, tactics execute

### Layer 2.5: Approaches (agents/approaches/) [DEPRECATED - See Layer 3]

**Responsibility:** Capture reusable strategies for common tasks that can be referenced by multiple agents. Think of these as "playbooks" or "walkthroughs" that provide step-by-step guidance on how to tackle specific challenges.

**Example Contents:**

- [Prompt Documentation and Logging](/.github/agents/approaches/prompt_documentation/)
- [File-based Orchestration](/.github/agents/approaches/file-based-orchestration.md)

**Design Decision:** [DEPRECATED] This layer is now superseded by the formal split between **Approaches** (Layer 3 - mental models) and **Tactics** (Layer 4 - procedural execution). Historical content migrated or archived.

### Layer 5: Agent Profiles (.github/agents/*.agent.md)

**Responsibility:** Define role-specific specializations, capabilities, and directive dependencies.

**Contents:**

- Role purpose and boundaries
- Primary/secondary focus areas
- Success criteria
- Collaboration contract
- Directive reference table
- Mode defaults

**Design Decision:** Each agent loads only directives relevant to its specialization.

### Layer 6: Templates (docs/templates/)

**Responsibility:** Standardize output formats for common artifacts.

**Contents:**

- Architecture templates (ADR, design vision, roadmap, technical design, functional requirements)
- **Tactic template** (`tactic.md`) — Structure for procedural execution guides
- Structure templates (repo map, surfaces, workflows, context links)
- LEX templates (style rules, deltas, reports)
- Automation templates (agent personas, new specialist definitions)

**Design Decision:** Templates are canonical. Agents reference but do not modify them. Templates define *what shape results must take*, while Tactics define *how to execute*.

### Layer 7: Documentation (docs/)

**Responsibility:** Capture strategic intent, vision, audience needs, and evolving decisions.

**Contents:**

- `VISION.md`: Repository purpose and scope
- `CHANGELOG.md`: Notable changes over time
- `specific_guidelines.md`: Project-specific constraints
- `audience/`: Stakeholder-specific documentation
- `architecture/`: ADRs and architectural vision
- `styleguides/`: Writing and formatting standards
- `planning/`: Future roadmaps and considerations

**Design Decision:** Human-authored, agent-consumed. Agents propose changes via `work/`, humans approve and promote.

### Layer 8: Work Coordination (work/)

**Responsibility:** Provide scratch space for agent collaboration, progress logs, and human-agent handoffs.

**Contents:**

- `curator/`: Validation, consistency checks, assessments
- `collaboration/`: Cross-agent coordination messages
- Role-specific directories for task logs

**Design Decision:** Fully tracked in git to maintain context across sessions and agents.

## Multi-Tier Agentic Framework (Refined)

We consolidate runtime responsibilities into four execution tiers informed by recent multi-vendor brainstorming:

- Layer 0: Human Interface & Utilities
	- IDE workflows (GitHub Copilot), command aliases, local utility scripts.
	- Outcome: ergonomic editing, inline completions, developer-led changes.

- Layer 1: Orchestration & Governance
	- `AGENTS.md`, `.github/agents/**`, YAML task descriptors, Python validators, Titan scripts.
	- Outcome: role definitions, planning, validation gates, and handoffs.

- Layer 2: Model Routing
	- OpenRouter and/or OpenCode.ai unifying vendor endpoints with fallbacks and pricing control.
	- Outcome: multi-model selection, graceful degradation, easy migration.

- Layer 3: Model Execution
	- Direct APIs (OpenAI GPT-5/4.1, Anthropic Claude) and local models (Ollama: Llama3, DeepSeek, Codestral).
	- Outcome: long-context analysis, explicit tool-calls, offline worker tasks.

Design intent: keep orchestration portable and auditable while allowing execution strategies to evolve independently with the model landscape.

## System Boundaries

### What This Architecture Supports

- ✅ Multiple specialized agents working concurrently
- ✅ Token-efficient context loading
- ✅ Human review and approval workflows
- ✅ Cross-project portability of governance frameworks
- ✅ Iterative refinement of directives and profiles
- ✅ Automated validation of structural integrity
- ✅ Explicit versioning and change tracking

### What This Architecture Does Not Support

- ❌ Fully autonomous agent execution without human oversight
- ❌ Real-time agent-to-agent communication (async coordination via `work/` only)
- ❌ Database-backed directive storage or querying
- ❌ Vendor-specific LLM features or extensions
- ❌ Dynamic directive generation or self-modification

## Key Architectural Decisions

### ADR-001: Modular Agent Directive System

**Decision:** Adopt externalized, numerically ordered directives with manifest-based metadata.

**Rationale:** Achieve token efficiency, maintainability, and portability without sacrificing quality or safety.

**Status:** Accepted  
**See:** [`docs/architecture/ADR-001-modular-agent-directive-system.md`](adrs/ADR-001-modular-agent-directive-system.md)

## Quality Attributes

### Performance

**Token consumption:** Target 40-60% reduction vs. monolithic approaches  
**Initialization time:** <2 seconds for typical agent profile + directives  
**Validation time:** <1 second for full directive suite structural checks

### Reliability

**Integrity checks:** Automated validation on every directive change  
**Fail-safe defaults:** Agents halt on missing/corrupted directives  
**Escalation protocol:** Explicit ❗️ markers for critical issues

### Maintainability

**Change isolation:** Update single directive without touching others  
**Clear ownership:** Manifest indicates safety-critical vs. advisory content  
**Version discipline:** All architecture artifacts versioned and timestamped

### Portability

**Format independence:** Markdown-first, no vendor lock-in  
**Cross-toolchain:** Compatible with any LLM supporting markdown context  
**Reusability:** Directives usable across projects with minimal adaptation

### Scalability

**Directive count:** System designed for 15-20 directives (currently 12)  
**Agent count:** Supports 10-15 specialized agents concurrently  
**Repository size:** Optimized for small-to-medium codebases (up to 100K SLOC)

## Extension Points

### Adding New Directives

1. Create `XXX_<slug>.md` in `.github/agents/directives/` (next sequential number)
2. Add entry to `manifest.json` with metadata and dependencies
3. Update Extended Directives Index in `AGENTS.md`
4. Run `validation/validate_directives.sh` to verify structural conformity
5. Update relevant agent profiles to reference new directive

### Adding New Agent Profiles

1. Use template: `docs/templates/automation/NEW_SPECIALIST.agent.md`
2. Define specialization, capabilities, and directive dependencies
3. Place in `.github/agents/<role>.agent.md`
4. Update `directives/005_agent_profiles.md` catalog

### Adding New Templates

1. Determine template category (architecture, structure, LEX, automation)
2. Create in appropriate `docs/templates/<category>/` subdirectory
3. Update `directives/008_artifact_templates.md` with location and usage
4. Cross-reference from relevant agent profiles

## Future Architectural Considerations

### Phase 1: Integrity Enhancements (Critical)

- Per-directive version numbers and SHA256 checksums
- Dependency resolution and deduplication in loader script
- Tooling setup directive (013) with install/fallback guidance

### Phase 2: Validation Improvements (High)

- Semantic checks (Purpose section existence, orphan detection)
- Index order verification
- JSON validation output for CI integration

### Phase 3: Governance Maturity (Medium)

- Recovery and integrity directive (014)
- Meta-version tracking (core + directive set composite version)
- Redundancy justification documentation

### Phase 4: Developer Experience (Low)

- Dash/punctuation normalization
- Alias mapping directive (015)
- Prose linting (trailing whitespace, line length)

### Phase 5: Continuous Improvement

- Automated manifest regeneration
- CI-based validation enforcement
- Metrics collection (token usage, task completion time)

## Cross-Cutting Concerns

### Security

- No secrets in directives or profiles
- Human approval required for `docs/` modifications
- Validation tooling prevents corrupted directive execution
- Safety-critical directives flagged in manifest

### Observability

- Progress logs in `work/` directories
- Explicit integrity markers in agent outputs (✅ ⚠️ ❗️)
- Version tags and timestamps on all architectural artifacts
- Changelog tracking of notable changes

### Developer Experience

- Clear onboarding path (bootstrap protocol)
- Templates for common tasks
- Validation feedback on structural issues
- Consistent tone and format across all documentation

## Success Criteria

This architecture is successful when:

- ✅ New agents can initialize and execute tasks within token budget
- ✅ Developers can update governance without touching multiple files
- ✅ Directives can be reused across different projects
- ✅ Validation tooling catches structural issues before runtime
- ✅ Human review cycles are efficient (minimal back-and-forth)
- ✅ Agents produce consistent, high-quality outputs
- ✅ Cross-agent collaboration proceeds smoothly via `work/` coordination

## Related Documentation

- Core Specification: [`AGENTS.md`](/AGENTS.md)
- Modular Directive System ADR: [`ADR-001-modular-agent-directive-system.md`](adrs/ADR-001-modular-agent-directive-system.md)
- Agent Audience Documentation: [`docs/audience/automation_agent.md`](/docs/audience/automation_agent.md)
- Repository Vision: [`docs/VISION.md`](/docs/VISION.md)
- Curator Assessment: [`work/curator/agentic_setup_reassessment.md`](/work/logs/curator/agentic_setup_reassessment.md)

---

_Prepared by: Architect Alphonso_  
_Mode: `/analysis-mode`_  
_Version: 1.0.0_
