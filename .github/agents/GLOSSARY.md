# Agent Framework Glossary

**Version:** 1.1.0  
**Last Updated:** 2026-02-07  
**Purpose:** Centralized definitions of common terminology used across agent profiles, directives, and documentation.

---

## Overview

This glossary provides standardized definitions for terms used throughout the SDD Agent Framework. These definitions ensure consistent understanding and communication across all agents, directives, and collaborative workflows.

For context on how to use this framework, see:

- [AGENTS.md](../AGENTS.md) - Core agent specification document
- [directives/](./directives/) - Extended directive set
- Agent profiles (e.g., [curator.agent.md](./curator.agent.md), [synthesizer.agent.md](./synthesizer.agent.md))

---

## Terms

### Agent

An autonomous or semi-autonomous system that operates within the SDD contextual environment. Agents perform specialized tasks while adhering to behavioral norms, reasoning discipline, and collaboration protocols defined in AGENTS.md and associated directives.

**Related:** Agent Profile, Specialization

### Agent Declaration

A formal acknowledgment statement that an agent accepts and will operate within the Stijn Dejongh Context Framework. Declaration text includes version confirmations for Operational, Strategic, Command, and Bootstrap layers. Required before an agent can exercise operational authority.

**Reference:** Directive 007  
**Related:** Context Layer, Version Governance

### Agent Profile

A specialized configuration file (
`.agent.md`) that defines an agent's purpose, specialization, collaboration contract, mode defaults, and directive usage. Profiles extend the base AGENTS.md specification with role-specific competencies.

**Location:** `.github/agents/*.agent.md`  
**Reference:** Directive 005  
**Related:** Specialization, Collaboration Contract

### Alignment

The state of conformity between agent behavior and the established guidelines, principles, and contextual requirements. Alignment is validated through the
`/validate-alignment` command and integrity markers (✅, ⚠️, ❗️).

**Related:** Integrity Symbol, Validation

### Artifact

Any generated or modified file produced by an agent during task execution. Artifacts include code, documentation, reports, diagrams, configuration files, and work logs. All artifacts should be traceable to their originating task or decision.

**Related:** Template, Work Log

### ATDD (Acceptance Test Driven Development)

A development approach where executable acceptance tests are written before implementation begins. ATDD anchors changes to user-visible intent and ensures behavioral correctness at the system boundary level.

**Reference:** Directive 016  
**Related:** TDD, Testing Pyramid

### Bootstrap

The initialization sequence an agent follows when first loaded or after context loss. Bootstrap ensures all context layers are loaded in proper order, versions are confirmed, and alignment is validated before operational work begins.

**Reference:** `.github/agents/guidelines/bootstrap.md`  
**Related:** Rehydration, Context Layer

### Collaboration Contract

A section within each agent profile that specifies behavioral commitments, boundaries, escalation protocols, and interaction patterns with other agents and humans. Defines what the agent will and won't do.

**Related:** Agent Profile, Escalation

### Context Layer

A hierarchical component of the agent's operational context. Layers include Bootstrap Protocol, General Guidelines, Operational Guidelines, Project Vision, Project Specific Guidelines, and Command Aliases. Layers are loaded in priority order.

**Reference:** AGENTS.md Section 2  
**Related:** Bootstrap, Version Governance

### Directive

An externalized instruction set (numbered 001-019+) that provides specialized guidance for specific operational domains. Directives are loaded selectively using
`/require-directive <code>` to maintain token efficiency while ensuring agents have access to detailed procedural knowledge when needed.

**Location:** `.github/agents/directives/XXX_name.md`  
**Reference:** AGENTS.md Section 8  
**Related:** Context Layer

### Escalation

The process of flagging issues, uncertainties, or conflicts that require human intervention or inter-agent coordination. Escalation uses integrity markers (❗️, ⚠️) and follows protocols defined in Directive 011.

**Reference:** Directive 011  
**Related:** Integrity Symbol, Risk

### Handoff

The transfer of work artifacts and context from one agent to another. Handoffs include artifact lists, completion status, next steps, and any relevant context needed for the receiving agent to continue work effectively.

**Related:** Orchestration, Work Log

### Human in Charge

A governance principle emphasizing that humans retain ultimate responsibility, authority, and decision-making power in agent-augmented workflows. Distinct from "human in the loop" (which focuses on oversight/approval), "human in charge" explicitly centers human accountability and intervention rights. The human in charge bears responsibility for work outcomes and maintains authority to override, redirect, or halt agentic operations at any point.

**Key distinctions from "human in the loop":**
- **Responsibility:** Human bears accountability for outcomes, not just oversight
- **Authority:** Power to make significant decisions and interventions
- **Control:** Ability to halt, redirect, or override agent operations
- **Ownership:** Ultimate arbiter of quality, direction, and delivery

**Practical implications:**
- Agents request permission for high-impact changes
- Humans retain approval authority over critical decisions
- Agents escalate uncertainty or risk immediately
- Human judgment overrides agent recommendations when conflicting

**Reference:** Directive 026 (Commit Protocol), Directive 011 (Risk & Escalation)  
**Related:** Escalation, Alignment, Collaboration Contract

### Integrity Symbol

Standardized markers used to signal alignment status or confidence levels:

- ✅ Alignment confirmed / validation passed
- ⚠️ Low confidence / assumption-based reasoning / uncertainty
- ❗️ Critical error / misalignment / integrity breach

**Reference:** AGENTS.md Section 3, Directive 011  
**Related:** Alignment, Escalation

### Locality of Change

A design principle emphasizing that changes should be measured against actual problems, not hypothetical concerns. Agents must verify problem existence, quantify severity, and prefer simple solutions over architectural enhancements. Discourages gold plating, premature abstraction, and complexity creep.

**Reference:** Directive 020, `.github/agents/approaches/locality-of-change.md`  
**Related:** Risk, Escalation, Alignment

### Mode

An operational state that governs an agent's reasoning approach and output style. Standard modes include:

- `/analysis-mode` - Diagnostic, decomposition, validation
- `/creative-mode` - Exploratory, ideation, pattern generation
- `/meta-mode` - Self-reflection, process analysis, governance calibration
- `/planning` - Strategic planning, task decomposition
- `/programming` - Code implementation, TDD cycles
- `/gathering` - Research, information collection
- `/assessing` - Critical evaluation, trade-off analysis

**Reference:** Directive 010  
**Related:** Reasoning Mode, Mode Transition

### Mode Transition

The explicit shift from one reasoning mode to another, always annotated as
`[mode: source → target]`. Transitions should be deliberate, infrequent (not more than once per 10 paragraphs), and include validation checks.

**Reference:** Directive 010  
**Related:** Mode, Alignment

### Orchestration

The coordination of multiple agents working on related tasks through structured workflows. The SDD framework uses file-based orchestration with YAML task descriptors that move through a defined lifecycle (new → assigned → in_progress → done → archive).

**Reference:** Directive 019  
**Related:** Task Lifecycle, Handoff

### Primer

A foundational execution pattern defined in ADR-011 that establishes minimum quality thresholds for agent work. Primers include Context Check, Progressive Refinement, Trade-Off Navigation, Transparency & Error Signaling, and Reflection Loop. Primer usage must be documented in work logs.

**Reference:** Directive 010, Directive 014  
**Related:** Work Log, Mode

### Reasoning Mode

See: Mode

### Rehydration

The process of restoring an agent's operational context after state loss, interruption, or restart. Rehydration involves reloading all context layers, confirming versions, running
`/validate-alignment`, and resuming in `/analysis-mode` unless directed otherwise.

**Reference:** AGENTS.md Section 7  
**Related:** Bootstrap, Context Layer

### Specialization

The defined focus area and competency boundaries for an agent. Specialization includes primary focus (core responsibility), secondary awareness (adjacent concerns), avoidance (what not to do), and success criteria (how to measure effective work).

**Related:** Agent Profile, Role Capabilities

### Synthesis

The integration of insights, outputs, or artifacts from multiple sources (agents, documents, data) into coherent, unified narratives or conceptual models. Synthesis preserves source integrity while improving systemic legibility and cross-agent understanding.

**Related:** Synthesizer Agent, Artifact

### Task Lifecycle

The standardized progression of orchestrated tasks through states: **new** (unassigned work), **assigned** (routed to specific agent), **in_progress
** (actively being worked), **done** (completed with results), **archive
** (historical record). Task state transitions are tracked through file-based coordination.

**Reference:** Directive 019, ADR-003  
**Related:** Orchestration, Work Log

### TDD (Test Driven Development)

A development discipline where small, failing automated tests are written before implementation code. The Red-Green-Refactor cycle (write failing test, make it pass, improve design) ensures verifiable increments and protects design quality.

**Reference:** Directive 017  
**Related:** ATDD, Testing Pyramid

### Template

A pre-defined structure or format for creating consistent artifacts. Templates exist for architecture documents, task descriptors, work logs, and other common outputs. Templates reduce cognitive load and ensure required sections are included.

**Location:** `docs/templates/`  
**Reference:** Directive 008  
**Related:** Artifact

### Testing Pyramid

A testing strategy that balances coverage across layers: many fast unit tests at the base, fewer integration tests in the middle, and minimal but meaningful acceptance/system tests at the top. Guides test-first development by encouraging appropriate test granularity.

**Reference:** Directive 016, Directive 017  
**Related:** TDD, ATDD

### Validation

The process of confirming that agent behavior, outputs, or decisions conform to established guidelines, principles, and requirements. Validation includes alignment checks (
`/validate-alignment`), directive compliance verification, and integrity assessments.

**Related:** Alignment, Integrity Symbol

### Version Governance

The system for tracking and managing versions of context layers and governance documents. Ensures agents operate against known, stable versions and prevents silent drift. Version deltas trigger pause, confirmation, and re-alignment sequences.

**Reference:** Directive 006  
**Related:** Context Layer, Alignment

### Work Log

A structured markdown document that records an agent's execution process, decision rationale, steps taken, artifacts created, and lessons learned. Work logs enable framework tuning, pattern recognition, and quality assurance. Required for all orchestrated tasks.

**Location:** `work/reports/logs/<agent-name>/YYYY-MM-DDTHHMM-<description>.md`  
**Reference:** Directive 014  
**Related:** Artifact, Task Lifecycle

---

## Usage Guidelines

### For Agents

- Reference glossary terms when explaining decisions or documenting work
- Use consistent terminology across all artifacts and communications
- When encountering ambiguous terms, consult this glossary first
- Suggest new terms or clarifications via work logs when gaps are identified

### For Humans

- Use glossary terms when providing instructions to agents
- Reference specific terms when clarity is needed
- Propose term additions or refinements through pull requests
- Review glossary during agent framework onboarding

### Cross-Referencing

When directives or agent profiles reference glossary terms, use this format:

```markdown
See [Term Name](./GLOSSARY.md#term-name) for definition.
```

---

## Maintenance

This glossary is a living document. Updates follow Version Governance (Directive 006):

- **Minor updates** (clarifications, examples): Update version patch number
- **New terms** (additions): Update version minor number
- **Structural changes** (reorganization): Update version major number

All changes require review by Curator agent for consistency and alignment with existing framework documentation.

**Maintained by:** Curator Claire  
**Review cycle:** Quarterly or when 5+ new terms are identified  
**Change requests:** Submit via work/collaboration/inbox/ task file

---

## Related Documentation

- [AGENTS.md](../AGENTS.md) - Core agent specification
- [directives/](./directives/) - Extended directive set (001-019)
- [Agent Profiles](.) - Role-specific configurations
- [Version Governance](./directives/006_version_governance.md) - Version tracking system
- [Work Log Creation](./directives/014_worklog_creation.md) - Documentation standards
