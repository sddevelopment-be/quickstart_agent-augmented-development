# Architecture Documentation

This directory contains architectural decisions, patterns, and technical designs for the agent-augmented development repository.

## Overview

The architecture documentation captures:

- **Strategic decisions** with full rationale and trade-offs (ADRs)
- **System vision** and guiding principles
- **Technical patterns** for common agent workflows
- **System architecture** for key subsystems

## Document Index

### Core Architecture

| Document                                                                       | Purpose                                           | Audience                                   |
|--------------------------------------------------------------------------------|---------------------------------------------------|--------------------------------------------|
| [`architectural_vision.md`](architectural_vision.md)                           | High-level principles, layers, quality attributes | Architects, stakeholders, new contributors |
| [`directive_system_architecture.md`](design/directive_system_architecture.md) | Technical details of modular directive system     | Developers, curators, automation agents    |
| [`agent_specialization_patterns.md`](patterns/agent_specialization_patterns.md)         | Patterns for agent roles and collaboration        | Agent developers, architects               |
| [`async_multiagent_orchestration.md`](design/async_multiagent_orchestration.md) | File-driven asynchronous multi-agent coordination | Architects, developers, automation agents |

### Technical Designs

| Document | Purpose | Audience |
|----------|---------|----------|
| [`async_orchestration_technical_design.md`](design/async_orchestration_technical_design.md) | Implementation details for async orchestration | Developers, build automation agents |

### Architecture Decision Records (ADRs)

Architecture Decision Records capture significant architectural decisions made in this project. Each ADR includes context, decision, rationale, consequences, and alternatives. They are stored in the [`adrs/`](./adrs/README.md) directory.


| ADR                                                                  | Title                                        | Status    | Date       |
|----------------------------------------------------------------------|----------------------------------------------|-----------|------------|
| [ADR-001](adrs/ADR-001-modular-agent-directive-system.md)            | Modular Agent Directive System             | Accepted  | 2025-11-17 |
| [ADR-002](adrs/ADR-008-file-based-async-coordination.md)             | File-Based Asynchronous Agent Coordination | Proposed  | 2025-11-20 |
| [ADR-003](adrs/ADR-003-task-lifecycle-state-management.md)           | Task Lifecycle and State Management        | Accepted  | 2025-11-20 |
| [ADR-004](adrs/ADR-004-work-directory-structure.md)                  | Work Directory Structure and Conventions   | Accepted  | 2025-11-20 |
| [ADR-005](adrs/ADR-005-coordinator-agent-pattern.md)                 | Coordinator Agent Pattern                  | Accepted  | 2025-11-20 |
| [ADR-006](adrs/ADR-006-adopt-three-layer-governance-model.md)        | Adopt Three-Layer Governance Model       | Accepted  | 2025-11-22 |
| [ADR-007](adrs/ADR-007-repository-restructuring-layer-separation.md) | Repository Restructuring for Layer Separation | Rejected / Adapted | 2025-11-22 |

## Key Architectural Principles

### 1. Token Efficiency

**Minimize LLM context window consumption** while maintaining quality.

- Modular directives with lazy loading
- Selective context assembly
- Deduplication of shared content
- Lean core specification

**Target:** 40-60% reduction in context vs. monolithic approaches.

### 2. Maintainability

**Enable sensible human-readable execution** with minimal overhead.

- Separation of concerns (core, directives, profiles, templates)
- Clear ownership and safety flags
- Predictable structure with automated validation
- Explicit versioning and change tracking

**Target:** Update single directive without touching unrelated files.

### 3. Portability

**Enable reuse across different LLM toolchains** and projects.

- Markdown-first format (no vendor lock-in)
- Standardized manifest for metadata
- Toolchain-agnostic patterns
- Clear intent/process/artifact separation

**Target:** Directives adoptable by other projects with minimal changes.

## Architectural Layers

```
┌──────────────────────────────────────────────┐
│  Core Governance (AGENTS.md)                 │
│  - Initialization protocol                   │
│  - Runtime behavior defaults                 │
│  - Safety & escalation                       │
└────────────────┬─────────────────────────────┘
                 │ references
                 ▼
┌──────────────────────────────────────────────┐
│  Modular Directives (.github/agents/directives/)│
│  - 001-012: Specialized operational guidance │
│  - Manifest: Metadata & dependencies         │
└────────────────┬─────────────────────────────┘
                 │ consumed by
                 ▼
┌──────────────────────────────────────────────┐
│  Agent Profiles (.github/agents/*.agent.md)  │
│  - Role specializations                      │
│  - Directive dependencies                    │
│  - Collaboration contracts                   │
└────────────────┬─────────────────────────────┘
                 │ use
                 ▼
┌──────────────────────────────────────────────┐
│  Templates (docs/templates/)                 │
│  - ADRs, designs, reports                    │
│  - Standard output formats                   │
└──────────────────────────────────────────────┘
```

## System Boundaries

### What This Architecture Supports

- ✅ Multiple specialized agents working concurrently
- ✅ Token-efficient context loading
- ✅ Human review and approval workflows
- ✅ Cross-project portability
- ✅ Iterative directive refinement
- ✅ Automated integrity validation

### What This Architecture Does Not Support

- ❌ Fully autonomous execution without human oversight
- ❌ Real-time agent-to-agent communication
- ❌ Database-backed directive storage
- ❌ Vendor-specific LLM features
- ❌ Dynamic directive self-modification

## Quality Attributes

| Attribute               | Target                          | Measurement                    |
|-------------------------|---------------------------------|--------------------------------|
| **Token Efficiency**    | 40-60% reduction vs. monolithic | Context window size on init    |
| **Initialization Time** | <2 seconds                      | Profile + directives load time |
| **Validation Time**     | <1 second                       | Full suite structural checks   |
| **Maintainability**     | Single-file updates             | Change isolation score         |
| **Portability**         | Cross-toolchain                 | Markdown compatibility         |

## Future Enhancements

### Phase 1: Integrity (Critical)

- Per-directive versioning and checksums
- Dependency resolution automation
- Tooling setup directive (013)

### Phase 2: Validation (High)

- Semantic validation (purpose checks, orphan detection)
- CI integration with JSON reports

### Phase 3: Governance (Medium)

- Recovery and integrity protocols (directive 014)
- Meta-versioning (composite version tracking)

### Phase 4: Developer Experience (Low)

- Automated manifest regeneration
- Prose linting and normalization

## Contributing to Architecture

### Adding a New ADR

1. Review [`docs/templates/architecture/adr.md`](../templates/architecture/adr.md)
2. Create `ADR-XXX-<slug>.md` in this directory (next sequential number)
3. Fill in: Context, Decision, Rationale, Consequences, Alternatives
4. Update this README's ADR index table
5. Cross-reference from relevant architecture documents

### Updating Architecture Vision

1. Propose changes in `work/architecture/` (draft)
2. Request Architect agent review
3. Get human approval
4. Update `architectural_vision.md`
5. Update version and timestamp

### Proposing System Changes

1. Identify architectural impact (layers, boundaries, quality attributes)
2. Draft ADR or design document
3. Solicit feedback via `work/collaboration/`
4. Iterate based on review
5. Final approval and integration

## Related Documentation

- Core Specification: [`AGENTS.md`](/AGENTS.md)
- Repository Vision: [`docs/VISION.md`](/docs/VISION.md)
- Agent Audience Documentation: [`docs/audience/automation_agent.md`](/docs/audience/automation_agent.md)
- Curator Assessment: [`work/curator/agentic_setup_reassessment.md`](/work/curator/agentic_setup_reassessment.md)
- Directive Suite: [`.github/agents/directives/`](/.github/agents/directives/)
- Templates: [`docs/templates/architecture/`](../templates/architecture/)
- Orchestration Implementation Plan: [`work/collaboration/orchestration-implementation-plan.md`](/work/collaboration/orchestration-implementation-plan.md)

## Questions?

- **How do I understand the directive system?** → Read [`directive_system_architecture.md`](design/directive_system_architecture.md)
- **How should agents collaborate?** → Read [`agent_specialization_patterns.md`](patterns/agent_specialization_patterns.md)
- **What are the guiding principles?** → Read [`architectural_vision.md`](architectural_vision.md)
- **Why was a decision made?** → Check ADRs in this directory
- **How do I propose a change?** → See "Contributing to Architecture" above
- **How does multi-agent orchestration work?** → Read [`async_multiagent_orchestration.md`](design/async_multiagent_orchestration.md)
- **How do I implement the orchestration system?** → Read [`async_orchestration_technical_design.md`](design/async_orchestration_technical_design.md)

---

_Maintained by: Architect agents_  
_Last updated: 2025-11-17_  
_Version: 1.0.0_
