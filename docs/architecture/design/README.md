# Architecture Design Documents

This directory contains detailed design documents for major architectural components and systems.

## Overview

Design documents elaborate on architectural decisions (ADRs) with implementation details, technical specifications, and system diagrams. They bridge high-level vision with concrete implementation.

## Available Designs

### Multi-Agent Orchestration

- **[async_multiagent_orchestration.md](async_multiagent_orchestration.md)** - File-based asynchronous agent coordination architecture
  - System overview and coordination patterns
  - State management through Git-tracked YAML
  - Agent communication protocols
  - Related ADRs: [ADR-003](../adrs/ADR-003-task-lifecycle-state-management.md), [ADR-004](../adrs/ADR-004-work-directory-structure.md), [ADR-008](../adrs/ADR-008-file-based-async-coordination.md)

- **[async_orchestration_technical_design.md](async_orchestration_technical_design.md)** - Technical implementation details for orchestration system
  - Component specifications
  - Data flow and state transitions
  - Integration patterns
  - Related: [multi-agent-orchestration.md](../../HOW_TO_USE/multi-agent-orchestration.md)

### Agent Directive System

- **[directive_system_architecture.md](directive_system_architecture.md)** - Modular directive system design
  - Directive loading and precedence
  - Context layer composition
  - Version governance
  - Related ADRs: [ADR-001](../adrs/ADR-001-modular-agent-directive-system.md), [ADR-006](../adrs/ADR-006-adopt-three-layer-governance-model.md)

### Distribution & Portability

- **[distribution_of_releases_architecture.md](distribution_of_releases_architecture.md)** - Release distribution architecture
  - Packaging strategy
  - Distribution channels
  - Version management
  - Related ADR: [ADR-013](../adrs/ADR-013-zip-distribution.md)

- **[distribution_of_releases_technical_design.md](distribution_of_releases_technical_design.md)** - Technical implementation of release distribution
  - Build pipeline
  - Artifact generation
  - Automation workflows

## Relationship to ADRs

Design documents expand on architectural decisions:

| Design Document | Primary ADRs |
|----------------|-------------|
| async_multiagent_orchestration.md | ADR-003, ADR-004, ADR-005, ADR-008 |
| directive_system_architecture.md | ADR-001, ADR-006, ADR-007 |
| distribution_of_releases_architecture.md | ADR-002, ADR-013 |

## Document Structure

Design documents typically include:

1. **Context & Goals** - Problem space and objectives
2. **System Overview** - High-level architecture
3. **Component Design** - Detailed component specifications
4. **Data Flow** - Information flow and state management
5. **Integration Points** - Interfaces and protocols
6. **Implementation Notes** - Technical considerations
7. **References** - Related ADRs and documentation

## Related Documentation

- **ADRs:** [../adrs/README.md](../adrs/README.md)
- **Patterns:** [../patterns/agent_specialization_patterns.md](../patterns/agent_specialization_patterns.md)
- **Synthesis:** [../synthesis/](../synthesis/)
- **Vision:** [../../VISION.md](../../VISION.md)

## Contributing

When adding design documents:

1. Link to relevant ADRs explicitly
2. Include diagrams (PlantUML preferred)
3. Specify integration points clearly
4. Update this README index
5. Cross-reference from related ADRs

---

_Design documents provide implementation-ready specifications for architectural decisions_
