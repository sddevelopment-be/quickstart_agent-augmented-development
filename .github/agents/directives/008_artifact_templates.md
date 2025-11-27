<!-- The following information is to be interpreted literally -->
# 008 Artifact Templates Directive

**Purpose:** Central reference to template locations to prevent duplication and drift.

**Core Concepts:** See [Template](../GLOSSARY.md#template) and [Artifact](../GLOSSARY.md#artifact) in the glossary.

Template Locations:
- Architecture: `docs/templates/architecture/`
- Lexical: `docs/templates/LEX/`
- Structure: `docs/templates/structure/`
- Planning: `docs/planning/` (PLAN_OVERVIEW, NEXT_BATCH, DEPENDENCIES, AGENT_TASKS)
- Task Descriptor: `docs/templates/task-descriptor.yaml`
- Agent Reports: `work/reports/` for logs, metrics, benchmarks
- Synthesis: `work/reports/synthesizer/` for aggregation artifacts
- Curator Reports: `work/reports/logs/curator/` discrepancy & validation outputs
- External Memory: `work/external_memory/` for temporary inter-agent context

Usage Guidance:
- Always check for an existing template before proposing a new one.
- Extend templates minimally; avoid wholesale rewrites.
- When adding a new template, create a short README in the template directory describing:
    - Intent
    - Required fields / sections
    - Example usage

Versioning:
- Major structural changes require updating [Version Governance](../GLOSSARY.md#version-governance) directive (006) if they alter process assumptions.

**Related Terms:** [Work Log](../GLOSSARY.md#work-log)

