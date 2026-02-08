# Templates Directory — Structure and Usage Guide

**Version:** 1.0.0  
**Last Updated:** 2026-02-08  
**Curator:** Claire

---

## Purpose

This directory contains standardized templates for consistent artifact creation across the SDD Agentic Framework. Templates define required structure, sections, and metadata for various document types used in agent-augmented development.

---

## Directory Structure

```
templates/
├── agent-tasks/          Task orchestration YAML descriptors and worklogs
├── architecture/         ADRs, design docs, technical specifications
├── automation/           Framework audits, agent profile templates
├── checklists/           Setup guides, tool reviews, validation checklists
├── diagramming/          PlantUML examples, themes, and diagram templates
├── LEX/                  Lexical analysis output formats
├── project/              Vision, changelog, guideline templates
├── prompts/              Prompt templates for common tasks
├── schemas/              YAML schemas and validation specs
├── specifications/       Feature specification templates
└── structure/            Repository maps, surfaces, workflow catalogs
```

---

## Template Categories

### agent-tasks/
**Purpose:** Task orchestration files for file-based collaboration  
**Key Files:**
- `task-descriptor.yaml` — Task definition schema
- `worklog.md` — Agent work log template
- `assessment.md` — Task completion assessment

**Usage:** See [Directive 019 (File-Based Collaboration)](../directives/019_file_based_collaboration.md)

---

### architecture/
**Purpose:** Architectural documentation templates  
**Key Files:**
- `adr.md` — Architecture Decision Record
- `design-vision.md` — High-level design overview
- `technical-design.md` — Detailed technical specifications
- `roadmap.md` — Feature roadmap template

**Usage:** See [Directive 018 (Traceable Decisions)](../directives/018_traceable_decisions.md)

---

### automation/
**Purpose:** Framework management and agent tooling  
**Key Files:**
- `framework-audit-report-template.md` — Framework version audit
- `NEW_SPECIALIST.agent.md` — Agent profile template
- `GUARDIAN_AUDIT_REPORT.md` — Framework Guardian audit format
- `GUARDIAN_UPGRADE_PLAN.md` — Upgrade planning template

**Usage:** See [Agent Profile: Framework Guardian](../agents/framework-guardian.agent.md)

---

### checklists/
**Purpose:** Validation and setup procedures  
**Key Files:**
- `derivative-repo-setup.md` — Checklist for using framework in new repos
- `quarterly-tool-review.md` — Regular tooling assessment

**Usage:** General procedural validation

---

### diagramming/
**Purpose:** Visual documentation templates  
**Subdirectories:**
- `examples/` — Sample PlantUML diagrams
- `themes/` — PlantUML styling themes

**Usage:** See [Approach: Incremental Detail Design Diagramming](../approaches/design_diagramming-incremental_detail.md)

---

### LEX/
**Purpose:** Lexical analysis output formats  
**Key Files:**
- Lexical diagnostic reports
- Style analysis outputs
- Tone consistency assessments

**Usage:** See [Agent Profile: Lexical Larry](../agents/lexical.agent.md)

---

### project/
**Purpose:** Project-level documentation  
**Key Files:**
- `vision.md` — Project vision statement
- `changelog.md` — Version history
- `guidelines.md` — Project-specific conventions

**Usage:** Repository initialization and documentation

---

### prompts/
**Purpose:** Reusable prompt templates  
**Key Files:**
- Common workflow prompts
- Task-specific prompt patterns

**Usage:** See [Directive 015 (Store Prompts)](../directives/015_store_prompts.md)

---

### schemas/
**Purpose:** YAML and JSON validation schemas  
**Subdirectories:**
- `agent_migration/` — Agent profile migration schemas

**Usage:** Validating task descriptors and structured data

---

### specifications/
**Purpose:** Feature and requirement specifications  
**Key Files:**
- Feature specification templates
- Requirement documentation formats

**Usage:** See [Directive 034 (Spec-Driven Development)](../directives/034_spec_driven_development.md)

---

### structure/
**Purpose:** Repository structure documentation  
**Key Files:**
- Repository map templates
- Surface taxonomy definitions
- Workflow catalog formats

**Usage:** See [Directive 003 (Repository Quick Reference)](../directives/003_repository_quick_reference.md)

---

## Using Templates

### Basic Usage

1. **Copy template** to appropriate location in repository
2. **Fill required sections** (marked as required in template)
3. **Remove placeholder text** and example content
4. **Validate metadata** (frontmatter, version info)
5. **Link to related artifacts** (ADRs, specs, tasks)

### Template Variables

Templates use `${VARIABLE}` syntax for configurable paths:

| Variable | Default | Purpose |
|----------|---------|---------|
| `${WORKSPACE_ROOT}` | `work` | Task orchestration workspace |
| `${DOC_ROOT}` | `docs` | Documentation root |
| `${SPEC_ROOT}` | `specifications` | Specification files |
| `${OUTPUT_ROOT}` | `output` | Generated artifacts |

**Override:** Create `.doctrine/config.yaml` in consuming repository.

---

## Adding New Templates

When creating new templates:

1. **Choose appropriate subdirectory** based on template purpose
2. **Include frontmatter** with metadata (if applicable)
3. **Mark required sections** clearly
4. **Provide inline examples** or comments
5. **Document usage** in this README
6. **Update docs/architecture/design/DOCTRINE_MAP.md** if adding new category

---

## Template Maintenance

**Owner:** Curator Claire  
**Review Cycle:** Annual or when 5+ templates added/changed  
**Change Protocol:** Submit proposals via `${WORKSPACE_ROOT}/collaboration/inbox/`

---

## Related Documentation

- **[DOCTRINE_MAP.md](../../docs/architecture/design/DOCTRINE_MAP.md)** — Framework structure overview
- **[Directive 008 (Artifact Templates)](../directives/008_artifact_templates.md)** — Template usage standards
- **[Agent Profile: Curator Claire](../agents/curator.agent.md)** — Template curation specialist

---

**Last Reviewed:** 2026-02-08  
**Next Review:** 2027-02-08
