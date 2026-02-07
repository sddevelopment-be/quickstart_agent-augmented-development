# Dependency Scan Results
**Date:** 2026-02-07T14:33:00Z
**Purpose:** Identify which files have external references

## Summary

### Files with External Dependencies
- **work/ references:** 30 files
- **docs/ references:** 31 files  
- **specifications/ references:** 5 files
- **Total unique files with deps:** ~50-60 (some overlap)

### Self-Contained Files (Category A - Ready to Move)
Approximately **50-55 files** have NO external references:

#### Agents (Likely Clean)
- backend-dev.agent.md
- bootstrap-bill.agent.md
- build-automation.agent.md
- diagrammer.agent.md
- frontend.agent.md
- java-jenny.agent.md
- lexical.agent.md
- manager.agent.md
- project-planner.agent.md
- python-pedro.agent.md
- researcher.agent.md
- scribe.agent.md
- synthesizer.agent.md
- translator.agent.md
- writer-editor.agent.md

#### Approaches (Likely Clean)
- agent-profile-handoff-patterns.md
- bug-fixing-checklist.md
- design_diagramming-incremental_detail.md
- file-based-orchestration.md
- locality-of-change.md
- file_based_collaboration/* (8 files)
- operating_procedures/* (2 files)
- prompt_documentation/* (5 files)
- traceable-decisions-detailed-guide.md (references docs/ - WAIT)

#### Directives (Likely Clean)
- 005_agent_profiles.md
- 007_agent_declaration.md
- 009_role_capabilities.md
- 010_mode_protocol.md
- 011_risk_escalation.md
- 012_operating_procedures.md
- 013_tooling_setup.md
- 017_test_driven_development.md
- 020_lenient_adherence.md
- 024_self_observation_protocol.md
- 026_commit_protocol.md

#### Tactics (All Likely Clean - 19 files)
All tactics appear self-contained.

#### Guidelines (All Clean - 5 files)
- bootstrap.md
- general_guidelines.md
- operational_guidelines.md
- rehydrate.md
- runtime_sheet.md

#### Core Files
- GLOSSARY.md (has work/ and docs/ refs - WAIT)
- DOCTRINE_STACK.md (has work/ and docs/ refs - WAIT)

## Action Plan

### Phase 1A: Move Self-Contained Files (Quick Wins)
1. **Guidelines/** - All 5 files (verified clean)
2. **Tactics/** - All 19 files (assumed clean, verify)
3. **Clean Agent Profiles** - ~15 agents
4. **Clean Directives** - ~11 directives
5. **Clean Approaches** - ~10 approaches

### Phase 1B: Abstract and Move High-Value Files
1. **DOCTRINE_STACK.md** - Core framework, needs abstraction
2. **GLOSSARY.md** - Core framework, needs abstraction
3. **directive 014** (worklogs) - Critical, needs parameterization
4. **directive 019** (file-based collab) - Critical, needs parameterization
5. **directive 008** (templates) - References docs/templates/

### Phase 1C: Special Decisions Needed
- **aliases.md** - Repository-specific?
- **prompts/** - Framework or examples?
- **directives 003, 004** - Repository-specific context?
- **directives 034, 035** - Specification directives (repository-specific?)

## Rudimentary Decision: Start with Guidelines

Move all 5 guidelines/ files first - definitely framework content, appear clean.
