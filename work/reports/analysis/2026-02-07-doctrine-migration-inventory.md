# Doctrine Migration File Inventory
**Date:** 2026-02-07T14:30:00Z
**Branch:** refactor/generic_core_files
**Purpose:** Categorize all files for Phase 1 doctrine/ migration

## Summary Statistics

### .github/agents/ Content
- **Total files:** 103 markdown files
- **Agents:** 21 agent profiles
- **Approaches:** 35 files (including subdirectories)
- **Directives:** 24 directives
- **Tactics:** 19 tactics
- **Guidelines:** 5 guidelines
- **Prompts:** 3 prompt files
- **Core:** DOCTRINE_STACK.md, GLOSSARY.md, aliases.md

### docs/ Content to Move
- **styleguides/:** 5 files (java, python, version_control, README)
- **templates/:** 20 files (release notes, agent-tasks, specifications)

## Directory Structure

```
.github/agents/
├── agents/ (21 *.agent.md files)
├── approaches/
│   ├── file_based_collaboration/ (8 files)
│   ├── operating_procedures/ (2 files)
│   ├── prompt_documentation/ (5 files)
│   └── (20 standalone approach files)
├── directives/ (24 files: 001-028, 034-035)
├── guidelines/ (5 files)
├── prompts/ (3 files)
├── tactics/ (19 files)
├── DOCTRINE_STACK.md
├── GLOSSARY.md
└── aliases.md

docs/
├── styleguides/ (5 files)
└── templates/ (20 files)
```

## Next Steps

1. **Categorize each file** by external dependency type
2. **Create migration plan** for each category
3. **Begin with self-contained files** (quick wins)

## Files Requiring Detailed Analysis

### High-Risk (Likely Many External Refs)
- directives/014_worklog_creation.md (references work/)
- directives/019_file_based_collaboration.md (references work/)
- approaches/work-directory-orchestration.md (references work/)
- approaches/decision-first-development.md (references docs/)
- directives/008_artifact_templates.md (references docs/templates/)

### Medium-Risk (Possibly Some Refs)
- All agent profiles (21 files - may have examples)
- directives/003_repository_quick_reference.md (repository-specific?)
- directives/004_documentation_context_files.md (references docs/?)

### Low-Risk (Likely Self-Contained)
- DOCTRINE_STACK.md
- GLOSSARY.md
- guidelines/* (5 files)
- Most tactics/* (19 files)
- Some approaches (e.g., ralph-wiggum-loop.md)

### Special Cases
- **aliases.md:** Move? Repository-specific? Need review
- **prompts/:** Framework content or repository-specific?
- **approaches/file_based_collaboration/:** Subdirectory structure - preserve?
- **docs/templates/agent-tasks/:** Already part of framework templates

## Phase 1 Strategy

1. Start with **Low-Risk** files (move as-is)
2. Analyze **High-Risk** files for abstraction patterns
3. Apply systematic parameterization to **Medium-Risk** files
4. Create validation script for zero-dependency check
5. Commit after each category completion

## Questions for Clarification

1. **aliases.md:** Move to doctrine/ or repository-specific?
2. **prompts/ directory:** Framework content or examples?
3. **Subdirectory structure:** Preserve in doctrine/ (e.g., approaches/file_based_collaboration/)?
4. **agent-tasks templates:** Already in docs/templates/ - consolidate?
