# Architecture Document Templates

This directory contains standardized templates for creating architecture documentation that maintains consistency across the project.

## Available Templates

### Core Architecture Documents

- **[adr.md](adr.md)** - Architecture Decision Record (ADR) template
  - Captures significant architectural decisions
  - Documents context, decision, consequences
  - Based on MADR (Markdown Architecture Decision Record) format
  - **Usage:** Copy template when documenting new architectural decisions
  - **Target:** `docs/architecture/adrs/ADR-XXX-decision-name.md`

- **[design_vision.md](design_vision.md)** - Architecture vision document template
  - High-level architectural vision and principles
  - System goals and constraints
  - Quality attributes
  - **Usage:** For establishing architectural direction
  - **Target:** `docs/architecture/architectural_vision.md`

- **[technical_design.md](technical_design.md)** - Technical design document template
  - Detailed component specifications
  - Implementation guidelines
  - Integration patterns
  - **Usage:** When elaborating on ADR implementation
  - **Target:** `docs/architecture/design/[component]-technical-design.md`

### Planning & Requirements

- **[functional_requirements.md](functional_requirements.md)** - Functional requirements template
  - User stories and use cases
  - Acceptance criteria
  - Functional specifications
  - **Usage:** For requirements gathering and specification
  - **Target:** `docs/architecture/requirements/[feature]-requirements.md`

- **[roadmap.md](roadmap.md)** - Architecture roadmap template
  - Phased architectural evolution
  - Milestone planning
  - Dependency mapping
  - **Usage:** For planning multi-phase architectural changes
  - **Target:** `docs/architecture/roadmaps/[initiative]-roadmap.md`

## Template Usage Guidelines

### When to Use Each Template

| Template | Use When | Output Location |
|----------|----------|----------------|
| adr.md | Making significant architectural decisions | `docs/architecture/adrs/` |
| design_vision.md | Establishing architectural direction | `docs/architecture/` |
| technical_design.md | Detailing implementation approach | `docs/architecture/design/` |
| functional_requirements.md | Specifying feature requirements | `docs/architecture/requirements/` |
| roadmap.md | Planning architectural evolution | `docs/architecture/roadmaps/` |

### Customization Guidelines

Templates are starting points:

1. **Preserve structure** - Keep main sections for consistency
2. **Adapt content** - Modify examples to fit your context
3. **Remove unnecessary sections** - If a section doesn't apply, remove it
4. **Add domain-specific sections** - Extend as needed
5. **Maintain metadata** - Always include date, status, authors

### Cross-Referencing

Architecture documents should reference each other:

- ADRs reference design documents for implementation details
- Design documents cite ADRs for decision rationale
- Requirements link to ADRs and designs that fulfill them
- Roadmaps coordinate multiple ADRs chronologically

## Related Documentation

- **Architecture Overview:** [../../architecture/README.md](../../architecture/README.md)
- **Existing ADRs:** [../../architecture/adrs/README.md](../../architecture/adrs/README.md)
- **Design Documents:** [../../architecture/design/README.md](../../architecture/design/README.md)
- **Template Index:** [../README.md](../README.md)

## Template Maintenance

Templates evolve based on usage:

- Document template limitations or gaps
- Propose improvements via issues or PRs
- Update this README when adding new templates
- Maintain backward compatibility when possible

## Examples

See existing architecture documentation for template usage examples:

- ADR examples: `docs/architecture/adrs/ADR-001-*.md` through `ADR-017-*.md`
- Design examples: `docs/architecture/design/async_multiagent_orchestration.md`
- Vision example: `docs/architecture/architectural_vision.md`

---

_Templates ensure consistency in architecture documentation across the project_
