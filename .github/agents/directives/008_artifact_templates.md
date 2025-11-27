<!-- The following information is to be interpreted literally -->
# 008 Artifact Templates Directive

**Purpose:** Central reference to template locations to prevent duplication and drift.

**Core Concepts:** See [Template](../GLOSSARY.md#template) and [Artifact](../GLOSSARY.md#artifact) in the glossary.

Template Locations:
- **Template Library:** `docs/templates/README.md` (comprehensive usage guide)
- Architecture: `docs/templates/architecture/` (ADR, design vision, technical design, functional requirements, roadmap)
- Agent Tasks: `docs/templates/agent-tasks/` (task descriptors, work logs, assessments, reports)
- Lexical: `docs/templates/LEX/` (style rules, deltas, reports)
- Structure: `docs/templates/structure/` (repo map, surfaces, workflows, context links)
- Project: `docs/templates/project/` (vision, changelog, guidelines)
- Automation: `docs/templates/automation/` (agent profiles, framework audit/upgrade templates)
- Planning: `docs/planning/` (PLAN_OVERVIEW, NEXT_BATCH, DEPENDENCIES, AGENT_TASKS)
- Agent Reports: `work/reports/` for logs, metrics, benchmarks
- Synthesis: `work/reports/synthesizer/` for aggregation artifacts
- Curator Reports: `work/reports/logs/curator/` discrepancy & validation outputs
- External Memory: `work/external_memory/` for temporary inter-agent context

Core Templates:
- **ADR:** `docs/templates/architecture/adr.md` - Architecture Decision Records
- **Work Log:** `docs/templates/agent-tasks/worklog.md` - Agent execution documentation
- **Assessment:** `docs/templates/agent-tasks/assessment.md` - Evaluation reports
- **Report:** `docs/templates/agent-tasks/report.md` - Analysis and synthesis reports
- **Task Descriptors:** `docs/templates/agent-tasks/task-*.yaml` - Task orchestration

Usage Guidance:
- **Always** consult `docs/templates/README.md` for comprehensive usage patterns
- Check for an existing template before proposing a new one
- Reference template path in directives (saves 80-95% token overhead vs. including full structure)
- Extend templates minimally; avoid wholesale rewrites
- When adding a new template:
    - Document in `docs/templates/README.md`
    - Include purpose, required/optional sections, usage example
    - Provide sample output reference
    - Update this directive

Versioning:
- Major structural changes require updating [Version Governance](../GLOSSARY.md#version-governance) directive (006) if they alter process assumptions.

**Related Terms:** [Work Log](../GLOSSARY.md#work-log)

