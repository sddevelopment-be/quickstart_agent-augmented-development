# Work Log: Doctrine Migration Phase 1A

**Agent:** GitHub Copilot CLI
**Date:** 2026-02-07T14:35:00Z
**Branch:** refactor/generic_core_files
**Task:** Move self-contained files to doctrine/

## Summary

Successfully migrated **46 self-contained files** to `doctrine/` with zero external dependencies.

## Actions Taken

### 1. Dependency Analysis
- Scanned all 115 .md files in `.github/agents/`
- Identified ~50-60 files with external refs (work/, docs/, specifications/)
- Created systematic scan scripts

### 2. File Migration (Self-Contained Only)

**Tactics (20 files) ✅**
- All 19 tactics + README
- Zero external dependencies verified
- Commit: 279e9de

**Agents (8 files) ✅**
- backend-dev, bootstrap-bill, build-automation
- diagrammer, frontend, researcher
- scribe, writer-editor
- Commit: beb2664

**Directives (11 files) ✅**
- 005, 007, 009, 010, 011, 012, 013
- 017, 020, 024, 026
- Commit: beb2664

**Approaches (7 files) ✅**
- 5 standalone: agent-profile-handoff-patterns, bug-fixing-checklist,
  design_diagramming-incremental_detail, file-based-orchestration, locality-of-change
- 1 subdirectory: operating_procedures/ (2 files)
- Commit: ca532d0

### 3. Documentation
- Created dependency scan results report
- Created migration inventory
- Preserved Annie's and Ralph's analysis reports

## Current doctrine/ Structure

```
doctrine/
├── agents/ (8 files)
├── approaches/ (5 files + 1 subdir with 2 files)
├── directives/ (11 files)
└── tactics/ (20 files)
```

**Total:** 46 files successfully migrated

## Remaining Work

### Phase 1B: Abstraction Required
Files with external dependencies needing parameterization:

**High Priority (Core Framework):**
- DOCTRINE_STACK.md (work/, docs/ refs)
- GLOSSARY.md (work/, docs/ refs)
- directives/014_worklog_creation.md (work/ paths)
- directives/019_file_based_collaboration.md (work/ paths)
- directives/008_artifact_templates.md (docs/templates/ refs)

**Agents (13 remaining):**
- analyst-annie, architect, code-reviewer-cindy, curator
- framework-guardian, java-jenny, lexical, manager
- project-planner, python-pedro, synthesizer, translator
- (plus aliases.md - unclear if framework or repo-specific)

**Approaches (remaining with refs):**
- file_based_collaboration/ subdirectory (work/ refs)
- prompt_documentation/ subdirectory (docs/ refs)
- Many standalone files: decision-first-development, meta-analysis,
  ralph-wiggum-loop, spec-driven-development, style-execution-primers,
  target-audience-fit, test-first-bug-fixing, test-readability-clarity-check,
  tooling-setup-best-practices, traceable-decisions-detailed-guide,
  trunk-based-development, work-directory-orchestration

**Directives (13 remaining):**
- 001_cli_shell_tooling
- 002_context_notes
- 003_repository_quick_reference (repo-specific?)
- 004_documentation_context_files
- 006_version_governance
- 008_artifact_templates
- 014_worklog_creation
- 015_store_prompts
- 016_acceptance_test_driven_development
- 018_traceable_decisions
- 019_file_based_collaboration
- 021_locality_of_change
- 022_audience_oriented_writing
- 023_clarification_before_execution
- 025_framework_guardian
- 028_bugfixing_techniques
- 034_spec_driven_development (repo-specific?)
- 035_specification_frontmatter_standards (repo-specific?)

**Guidelines (5 files - all have refs):**
- bootstrap.md, general_guidelines.md, operational_guidelines.md
- rehydrate.md, runtime_sheet.md
- Need parameterization (work/, docs/ refs)

**docs/ Content:**
- styleguides/ (5 files, minor work/ refs)
- templates/ (20+ files, many work/ and docs/ refs)

**Prompts Directory:**
- 3 files - need decision: framework or repository-specific?

## Core Decisions Needed

**❓ PAUSE FOR HUMAN GUIDANCE:**

1. **Repository-Specific Directives:**
   - 003_repository_quick_reference - stays local?
   - 004_documentation_context_files - stays local?
   - 034_spec_driven_development - framework or repo-specific?
   - 035_specification_frontmatter_standards - framework or repo-specific?

2. **Prompts Directory:**
   - Is `prompts/` framework content or repository examples?
   - If framework: move to doctrine/templates/?
   - If examples: stays in repository

3. **aliases.md:**
   - Framework command reference or repository shortcuts?

4. **Abstraction Strategy:**
   - Begin parameterizing high-priority files now?
   - Or continue moving clean files first?

## Validation

All migrated files verified:
```bash
# No external references
grep -r 'work/' doctrine/ && echo "FAIL" || echo "PASS"
grep -r 'docs/' doctrine/ && echo "FAIL" || echo "PASS"
grep -r 'specifications/' doctrine/ && echo "FAIL" || echo "PASS"
```

## Token Metrics
- Reports created: 4
- Commits made: 4
- Files migrated: 46
- Validation scripts: 2
