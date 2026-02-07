<!-- The following information is to be interpreted literally -->

# 008 Artifact Templates Directive

**Purpose:** Central reference to template locations to prevent duplication and drift.

**Core Concepts:** See [Template](../GLOSSARY.md#template) and [Artifact](../GLOSSARY.md#artifact) in the glossary.

Template Locations:

- **Template Library:** `${DOC_ROOT}/templates/README.md` (comprehensive usage guide)
- Architecture: `${DOC_ROOT}/templates/architecture/` (ADR, design vision, technical design, functional requirements, roadmap)
- Agent Tasks: `${DOC_ROOT}/templates/agent-tasks/` (task descriptors, work logs, assessments, reports)
- Lexical: `${DOC_ROOT}/templates/LEX/` (style rules, deltas, reports)
- Structure: `${DOC_ROOT}/templates/structure/` (repo map, surfaces, workflows, context links)
- Project: `${DOC_ROOT}/templates/project/` (vision, changelog, guidelines)
- Automation: `${DOC_ROOT}/templates/automation/` (agent profiles, framework audit/upgrade templates)
- Planning: `${DOC_ROOT}/planning/` (PLAN_OVERVIEW, NEXT_BATCH, DEPENDENCIES, AGENT_TASKS)
- Agent Reports: `${WORKSPACE_ROOT}/reports/` for logs, metrics, benchmarks
- Synthesis: `${WORKSPACE_ROOT}/reports/synthesizer/` for aggregation artifacts
- Curator Reports: `${WORKSPACE_ROOT}/reports/logs/curator/` discrepancy & validation outputs
- External Memory: `${WORKSPACE_ROOT}/external_memory/` for temporary inter-agent context

Core Templates:

- **ADR:** `${DOC_ROOT}/templates/architecture/adr.md` - Architecture Decision Records
- **Work Log:** `${DOC_ROOT}/templates/agent-tasks/worklog.md` - Agent execution documentation
- **Assessment:** `${DOC_ROOT}/templates/agent-tasks/assessment.md` - Evaluation reports
- **Report:** `${DOC_ROOT}/templates/agent-tasks/report.md` - Analysis and synthesis reports
- **Task Descriptors:** `${DOC_ROOT}/templates/agent-tasks/task-*.yaml` - Task orchestration

Usage Guidance:

- **Always** consult `${DOC_ROOT}/templates/README.md` for comprehensive usage patterns
- Check for an existing template before proposing a new one
- Reference template path in directives (saves 80-95% token overhead vs. including full structure)
- Extend templates minimally; avoid wholesale rewrites
- When adding a new template:
    - Document in `${DOC_ROOT}/templates/README.md`
    - Include purpose, required/optional sections, usage example
    - Provide sample output reference
    - Update this directive

Versioning:

- Major structural changes require updating [Version Governance](../GLOSSARY.md#version-governance) directive (006) if they alter process assumptions.

**Related Terms:** [Work Log](../GLOSSARY.md#work-log)

