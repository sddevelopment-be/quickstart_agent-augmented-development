# Ideation Directory

_Version: 1.0.0_  
_Last updated: 2025-11-25_

This directory contains ideation artifacts—early-stage exploration, brainstorming outputs, concept sketches, and preliminary analysis that inform architectural decisions and feature development. It now lives under `work/notes/` to emphasize that everything here is provisional until promoted into the long-term `docs/` tree.

## Overview

The ideation directory serves as a structured workspace for:

1. **Early-stage concepts** that may evolve into formal proposals or ADRs
2. **Exploratory analysis** of potential solutions and approaches
3. **Brainstorming artifacts** from planning sessions or collaborative exploration
4. **Problem space mapping** to understand requirements and constraints before design
5. **Traceability roots** linking architectural decisions back to initial thinking

## Purpose

### What Belongs Here

- ✅ Concept sketches and preliminary designs
- ✅ Problem exploration and constraint analysis
- ✅ Brainstorming outputs and creative exploration
- ✅ Early-stage research findings
- ✅ Rough architectural options before ADR formalization
- ✅ Feature ideation and possibility mapping

### What Does Not Belong Here

- ❌ Formal Architecture Decision Records (use `docs/architecture/adrs/`)
- ❌ Approved architectural designs (use `docs/architecture/design/`)
- ❌ Production documentation (use appropriate `docs/` subdirectories)
- ❌ Active project tasks (use `work/` orchestration system)
- ❌ Meeting notes or logs (keep them in other `work/notes/` subdirectories or `work/collaboration/`)

## Workflow

### Ideation → Formalization

Typical artifact evolution:

```
work/notes/ideation/   →  docs/architecture/adrs/     →  docs/architecture/design/
(exploration)             (decision capture)             (detailed implementation)
```

### Best Practices

1. **Date-prefix files**: Use `YYYY-MM-DD-<topic>.md` for chronological clarity
2. **Link forward**: When an ideation doc leads to an ADR, add cross-references
3. **Preserve history**: Keep ideation artifacts even after formalization—they provide context
4. **Mark status**: Use front-matter or headers to indicate if an idea is explored, adopted, rejected, or superseded
5. **Agent collaboration**: Researcher, Architect, and Planner agents commonly work here

## File Naming Convention

Recommended format for ideation documents:

```
YYYY-MM-DD-<topic-slug>.md
```

Examples:
- `2025-11-25-async-task-routing.md`
- `2025-11-26-documentation-pipeline-concepts.md`
- `2025-11-27-agent-specialization-exploration.md`

## Subdirectories

As the repository grows, consider organizing by theme:

```
work/notes/ideation/
  features/           # Feature-level ideation
  architecture/       # System-level exploration
  workflows/          # Process and workflow concepts
  tooling/            # Tool selection and integration ideas
```

## Relationship to Other Directories

| Directory | Relationship |
|-----------|--------------|
| `docs/architecture/adrs/` | Ideation informs ADRs; ADRs reference ideation artifacts for rationale |
| `docs/architecture/design/` | Design documents elaborate on ideas vetted through ideation |
| `docs/planning/` | Planning may spawn ideation tasks; ideation feeds planning refinement |
| Other `work/notes/` subdirectories | Informal notes may start there before getting structured here |

## Agent Involvement

Agents expected to work in this directory:

- **Researcher**: Gathers data, explores problem spaces
- **Architect**: Sketches system-level concepts
- **Planning/Project-Planner**: Maps features and dependencies
- **Curator**: Ensures ideation artifacts link properly to downstream docs
- **Synthesizer**: Distills multiple ideation threads into coherent proposals

## Example Artifacts

### Concept Sketch

```markdown
# Feature: Multi-Stage Documentation Pipeline

## Problem
Current documentation generation is single-pass; complex docs need staged refinement.

## Initial Ideas
1. Template → Draft → Review → Publish stages
2. Agent handoffs at each boundary
3. Quality gates before promotion

## Open Questions
- How to handle rollback?
- Who owns review approval?
- Where does final output live?

## Next Steps
- Draft ADR if concept is validated
- Prototype in work/scripts/
```

### Exploration Document

```markdown
# Exploration: Agent Coordination Patterns

## Patterns Evaluated
1. Queue-based (simple, sequential)
2. Event-driven (complex, reactive)
3. File-based (transparent, Git-native) ← Selected

## Trade-offs
...

## Decision
Captured in ADR-008: File-Based Asynchronous Agent Coordination
```

## Contributing

When adding ideation artifacts:

1. Use the file naming convention
2. Include front-matter (version, date, status)
3. Mark exploratory status clearly
4. Cross-reference related documents
5. Update this README if introducing new subdirectories

## Related Documentation

- Architecture Overview: [`docs/architecture/README.md`](../../docs/architecture/README.md)
- Project Vision: [`docs/VISION.md`](../../docs/VISION.md)
- Work Directory: [`work/README.md`](../../README.md)
- Templates: [`docs/templates/`](../../docs/templates/)

## Current Ideation Status (2025-11-25)

### Active Ideation

#### `tracability/`
**Status:** ✅ Captured in ADR-017 (Traceable Decision Integration)

- `structured_knowledge_sharing.md` - Organizational knowledge sharing patterns
- `personal_productivity_flow.md` - Individual contributor workflow patterns

**Related Artifacts:**
- ADR-017: Traceable Decision Integration
- Synthesis: `docs/architecture/synthesis/traceable-decision-patterns-synthesis.md`
- Directive 018: Traceable Decisions
- Approach: `agents/approaches/decision-first-development.md`

#### `portability_testing/`
**Status:** 🔄 Not yet formalized into ADR

- `portability_testing.md` - Main protocol description
- `test_protocol.md` - Step-by-step testing procedure
- `meta_agents.md` - Multi-agent portability testing
- `issue_template.md` - GitHub issue template

**Next Steps:** Consider moving to `docs/HOW_TO_USE/` or `validation/` as operational documentation

#### `opinionated_platform/`
**Status:** 📚 Reference material (intentionally kept as source principles)

Contains foundational principles that guide framework design. These remain as reference materials rather than being "captured" since they represent ongoing design philosophy.

**Related to:**
- ADR-011: Command Alias Primer Alignment (solutioning_primer)
- ADR-012: Default to ATDD + TDD (testing_pyramid, quad_A_test_structure)
- Various directives incorporate these principles

#### `2025-11-25-video-transcription-documentation-pipeline.md`
**Status:** 🆕 New exploration, not yet synthesized

### Recently Captured (2025-11-25)

**distribution_of_releases/** - Fully captured and removed

- ✅ Captured in ADR-013 (Zip Distribution) and ADR-014 (Framework Guardian)
- ✅ Templates moved to `docs/templates/automation/`
- ✅ Ideation files removed after formalization

---

_Maintained by: Curator, Researcher, Architect agents_  
_For questions, consult the agent coordination system via `work/collaboration/`_
