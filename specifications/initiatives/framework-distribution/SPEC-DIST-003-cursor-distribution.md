---
id: SPEC-DIST-003
title: Cursor Distribution with Automated Export
status: draft
initiative: framework-distribution
version: 1.0.0
author: Generic Cursor Agent
architect_review: pending
created: 2026-02-10
updated: 2026-02-10
stakeholders: [stijn, architect-alphonso, devops-danny, curator-claire]
approved_by: pending
approved_date: pending
priority: medium
type: feature
tags: [distribution, cursor, exporter, optimization, phase-2]
parent: SPEC-DIST-001
phase_1_implementation: feature/dist-cursor
---

# Cursor Distribution with Automated Export (Phase 2)

## Executive Summary

Phase 1 delivered token-efficient Cursor integration via `.cursorrules` (500 tokens, 87% reduction) and `.cursor/QUICK_REFERENCE.md` (manual creation). Phase 2 automates full `.cursor/` distribution with an exporter pipeline that transforms doctrine stack artifacts into Cursor-native format, achieving ecosystem parity with `.claude/` and `.github/instructions/` distributions while maintaining Cursor's file-based simplicity.

**Parent Specification:** SPEC-DIST-001 (Multi-Tool Distribution Architecture)

**Phase 1 Implementation:** `feature/dist-cursor` (manual `.cursorrules` + Quick Reference)

**Research Foundation:**
- `work/2026-02-10-cursor-doctrine-optimization-analysis.md`
- `work/2026-02-10-cursor-integration-proposal.md`
- `work/2026-02-10-cursor-integration-summary.md`

---

## User Story

**As a** Software Engineer using Cursor IDE
**I want** the doctrine stack automatically exported to `.cursor/` directory
**So that** I can access specialist agents, directives, and tactics without manual file copying

**Target Personas:**
- Software Engineer (Primary) - Uses Cursor for daily development
- Agentic Framework Core Team (Secondary) - Maintains distribution pipeline
- AI/LLM Power User (Secondary) - Seeks consistent agent behavior across tools

---

## Overview

### Problem Statement

**Phase 1 Status (Implemented):**
- ✅ `.cursorrules` provides minimal auto-loaded context (500 tokens)
- ✅ `.cursor/QUICK_REFERENCE.md` provides fast-access index (800 tokens)
- ✅ 87% token reduction for routine tasks
- ⚠️ **Manual maintenance** - Quick Reference must be updated when directives/agents change
- ⚠️ **No full distribution** - Agents and directives not exported to `.cursor/`
- ⚠️ **No automation** - No exporter script like Copilot/Claude/OpenCode

**Phase 2 Goal:**
Automate `.cursor/` distribution with a dedicated exporter that transforms doctrine artifacts into Cursor-native format, enabling:
- Automated agent profile exports (21 files)
- Automated directive mirroring (36+ files)
- Automated rules consolidation (5 themed files)
- Automated Quick Reference regeneration
- One-command deployment: `npm run export:cursor`

### Context

**Why Phase 2 Matters:**
1. **Maintenance Efficiency:** Quick Reference is 180 lines of index data that becomes stale when directives/agents added
2. **Ecosystem Parity:** Claude has `.claude/`, Copilot has `.github/instructions/`, Cursor needs `.cursor/`
3. **Discoverability:** Agents/directives exported to dedicated directories are easier to browse
4. **Consistency:** Exporter ensures transformations applied uniformly (YAML frontmatter removal, etc.)

**Phase 1 → Phase 2 Progression:**

| Aspect | Phase 1 (Manual) | Phase 2 (Automated) |
|--------|------------------|---------------------|
| **Token efficiency** | ✅ 87% reduction | ✅ Same (maintained) |
| **Quick Reference** | ⚠️ Manual updates | ✅ Auto-generated |
| **Agent profiles** | ⚠️ Manual loading | ✅ Exported to `.cursor/agents/` |
| **Directives** | ⚠️ Manual loading | ✅ Exported to `.cursor/directives/` |
| **Rules files** | ❌ Not created | ✅ Auto-generated themed files |
| **Maintenance** | ⚠️ High (manual sync) | ✅ Low (npm script) |
| **Ecosystem parity** | ⚠️ Partial | ✅ Full |

**Related Documentation:**
- Phase 1 Implementation: `.cursorrules`, `.cursor/QUICK_REFERENCE.md` (feature/dist-cursor branch)
- Related Spec: SPEC-DIST-001 (multi-tool distribution architecture)
- Related Spec: SPEC-DIST-002 (Claude Code optimization, similar transformation logic)
- Existing Exporters: `tools/exporters/copilot-generator.js`, `tools/exporters/opencode-generator.js`

---

## Functional Requirements (MoSCoW)

### MUST Have (Critical)

**FR-M1: Cursor Exporter Script**
- **Requirement:** System SHALL provide `tools/exporters/cursor-exporter.js` that transforms doctrine artifacts to Cursor format
- **Rationale:** Automated export is core Phase 2 value proposition
- **Personas Affected:** Agentic Framework Core Team (maintainers), Software Engineer (consumers)
- **Success Criteria:** 
  - Script exists at `tools/exporters/cursor-exporter.js`
  - Executable via `node tools/exporters/cursor-exporter.js`
  - Reads from `doctrine/` directory
  - Writes to `.cursor/` directory
  - Exit code 0 on success, non-zero on error

**FR-M2: Agent Profile Export**
- **Requirement:** System SHALL export all 21 agent profiles from `doctrine/agents/*.agent.md` to `.cursor/agents/*.md`
- **Rationale:** Agents are primary specialization mechanism; must be accessible
- **Personas Affected:** Software Engineer (loads specialist profiles)
- **Success Criteria:**
  - All 21 files exported (1:1 mapping)
  - YAML frontmatter removed (Cursor doesn't parse it)
  - Core content preserved (Purpose, Specialization, Constraints)
  - File size reduced by 30%+ (ceremony removal)
  - Each exported agent under 60 lines

**FR-M3: Directive Mirroring**
- **Requirement:** System SHALL copy all directives from `doctrine/directives/` to `.cursor/directives/` without transformation
- **Rationale:** Directives are already markdown; no transformation needed, just mirror for discoverability
- **Personas Affected:** Software Engineer (loads directives on-demand)
- **Success Criteria:**
  - All `NNN_name.md` files copied
  - Directory structure preserved
  - README.md included
  - File contents identical (no transformation)

**FR-M4: Quick Reference Auto-Generation**
- **Requirement:** System SHALL regenerate `.cursor/QUICK_REFERENCE.md` from doctrine metadata
- **Rationale:** Manual maintenance unsustainable; auto-generate from source of truth
- **Personas Affected:** Software Engineer (uses Quick Reference for discovery)
- **Success Criteria:**
  - Index generated from `doctrine/directives/` file scan
  - Agent roster generated from `doctrine/agents/` metadata
  - Tactics catalog generated from `doctrine/tactics/README.md`
  - Decision trees embedded (static content from template)
  - File under 200 lines

**FR-M5: NPM Script Integration**
- **Requirement:** System SHALL provide `npm run export:cursor` command that executes full export
- **Rationale:** Consistent with existing `export:claude`, `export:copilot`, `export:all` commands
- **Personas Affected:** Agentic Framework Core Team (runs export during release)
- **Success Criteria:**
  - Command added to `package.json` scripts
  - Command runs cursor-exporter.js
  - Command exits 0 on success
  - Command included in `npm run export:all`

**FR-M6: Rules File Generation**
- **Requirement:** System SHALL generate consolidated rule files in `.cursor/rules/` from doctrine content
- **Rationale:** Modular rules improve token efficiency; agents load only what they need
- **Personas Affected:** Software Engineer (benefits from modular context loading)
- **Success Criteria:**
  - Generate `guidelines.md` (general + operational guidelines)
  - Generate `architecture.md` (ADR practices from directive 018)
  - Generate `testing.md` (ATDD + TDD from directives 016, 017)
  - Generate `collaboration.md` (multi-agent from directive 019)
  - Generate `coding-conventions.md` (Python conventions from guidelines)
  - Each file under 100 lines

### SHOULD Have (Important)

**FR-S1: Tactics Export**
- **Requirement:** System SHOULD copy tactics from `doctrine/tactics/` to `.cursor/tactics/`
- **Rationale:** Tactics discoverability improved by dedicated directory
- **Personas Affected:** Software Engineer (discovers tactics)
- **Success Criteria:** All `*.tactic.md` files copied, README.md included
- **Workaround if omitted:** Agents can still load from `doctrine/tactics/` directly

**FR-S2: Export Validation**
- **Requirement:** System SHOULD validate exported files meet formatting requirements
- **Rationale:** Catch export errors early (missing sections, malformed markdown)
- **Personas Affected:** Agentic Framework Core Team (maintains quality)
- **Success Criteria:** 
  - Validate all exported agents have Purpose + Specialization sections
  - Validate Quick Reference has all required index tables
  - Validate rules files parse as valid markdown
  - Warn on validation failure, don't block export
- **Workaround if omitted:** Manual review of exported files

**FR-S3: Incremental Export**
- **Requirement:** System SHOULD support incremental export (only changed files)
- **Rationale:** Performance optimization for large doctrine stacks
- **Personas Affected:** Agentic Framework Core Team (fast iteration)
- **Success Criteria:**
  - Compare file modification times
  - Skip unchanged source files
  - Report skipped files in console
  - `--force` flag to override incremental
- **Workaround if omitted:** Full export every time (acceptable for 21 agents + 36 directives)

**FR-S4: Dry-Run Mode**
- **Requirement:** System SHOULD support `--dry-run` flag that previews changes without writing files
- **Rationale:** Safety mechanism for testing transformations
- **Personas Affected:** Agentic Framework Core Team (tests export logic)
- **Success Criteria:**
  - `--dry-run` flag shows what would be exported
  - No files written in dry-run mode
  - Exit code 0 (success simulation)
- **Workaround if omitted:** Test in separate branch (acceptable)

### COULD Have (Nice to have)

**FR-C1: Custom Templates**
- **Requirement:** System COULD support custom templates for rules file generation
- **Rationale:** Flexibility for repository-specific rules formatting
- **Personas Affected:** Agentic Framework Core Team (customizes distributions)
- **Success Criteria:**
  - Template files in `tools/exporters/templates/cursor/`
  - Template variables: `{{guidelines}}`, `{{directives}}`, etc.
  - Override via `--template-dir` flag
- **If omitted:** Use hardcoded transformation logic (acceptable for standard distributions)

**FR-C2: Export Metrics**
- **Requirement:** System COULD generate export metrics (file counts, token counts, reduction percentages)
- **Rationale:** Transparency into export efficiency
- **Personas Affected:** Agentic Framework Core Team (monitors token efficiency)
- **Success Criteria:**
  - Report: "Exported 21 agents (avg 45 lines, 35% reduction)"
  - Report: "Generated 5 rules files (total 450 lines)"
  - Report: "Quick Reference: 180 lines, 800 tokens"
- **If omitted:** Manual inspection (acceptable)

**FR-C3: Watch Mode**
- **Requirement:** System COULD support `--watch` flag for continuous export during development
- **Rationale:** Convenience for iterative doctrine stack development
- **Personas Affected:** Agentic Framework Core Team (iterates on agents/directives)
- **Success Criteria:**
  - Watches `doctrine/` directory for changes
  - Auto-exports on file save
  - Debounced (500ms delay)
- **If omitted:** Manual `npm run export:cursor` after changes (acceptable)

### WON'T Have (Out of scope)

**FR-W1: Cursor Plugin Development**
- **Requirement:** System WON'T develop native Cursor plugin or extension
- **Rationale:** Cursor extension API research required; deferred to Phase 3
- **Future Consideration:** If Cursor exposes plugin API, consider native integration

**FR-W2: Dynamic Context Assembly**
- **Requirement:** System WON'T implement task-specific `.cursorrules` generation
- **Rationale:** Complexity not justified; Phase 1 minimal context sufficient
- **Future Consideration:** Revisit if users report frequent context switching needs

**FR-W3: Cursor-Specific Syntax Highlighting**
- **Requirement:** System WON'T add custom syntax highlighting for exported files
- **Rationale:** Standard markdown sufficient; Cursor renders natively
- **Future Consideration:** N/A (not a value-add)

---

## Scenarios and Behavior

### Scenario 1: First-Time Export (Happy Path)

**Context:** Maintainer runs Cursor export for first time after Phase 2 implementation

**Given:** Repository with full doctrine stack (`doctrine/agents/`, `doctrine/directives/`, etc.)
**And:** No existing `.cursor/` directory
**When:** Maintainer runs `npm run export:cursor`
**Then:** System creates `.cursor/` directory structure
**And:** System exports 21 agent profiles to `.cursor/agents/`
**And:** System copies 36 directives to `.cursor/directives/`
**And:** System generates 5 rules files in `.cursor/rules/`
**And:** System regenerates `.cursor/QUICK_REFERENCE.md`
**And:** System reports "Export complete: 21 agents, 36 directives, 5 rules, 1 index"
**And:** Command exits with code 0

**Personas:** Agentic Framework Core Team
**Priority:** MUST

### Scenario 2: Incremental Export After Agent Update

**Context:** Maintainer updates one agent profile and re-exports

**Given:** Existing `.cursor/` directory with previous export
**And:** Maintainer edits `doctrine/agents/python-pedro.agent.md`
**When:** Maintainer runs `npm run export:cursor`
**Then:** System detects changed file (modification time comparison)
**And:** System re-exports only `python-pedro.md` to `.cursor/agents/`
**And:** System regenerates Quick Reference (agent metadata changed)
**And:** System skips unchanged agents, directives, rules
**And:** System reports "Export complete: 1 agent updated, 20 skipped"
**And:** Command exits with code 0

**Personas:** Agentic Framework Core Team
**Priority:** SHOULD

### Scenario 3: Dry-Run Preview

**Context:** Maintainer wants to test export logic without writing files

**Given:** Repository with doctrine stack
**And:** Maintainer runs `npm run export:cursor -- --dry-run`
**When:** Cursor exporter executes in dry-run mode
**Then:** System logs intended operations: "Would export python-pedro.agent.md → .cursor/agents/python-pedro.md"
**And:** System logs file size reductions: "python-pedro.md: 120 lines → 45 lines (62% reduction)"
**And:** System does NOT write any files to `.cursor/`
**And:** Command exits with code 0

**Personas:** Agentic Framework Core Team
**Priority:** SHOULD

### Scenario 4: Validation Failure (Non-Blocking)

**Context:** Exporter detects malformed agent file during export

**Given:** `doctrine/agents/new-agent.agent.md` missing "Purpose" section
**When:** Maintainer runs `npm run export:cursor`
**Then:** System warns: "⚠️ new-agent.agent.md missing Purpose section"
**And:** System continues export (other agents unaffected)
**And:** System exports `new-agent.md` with warning comment at top
**And:** System reports: "Export complete with 1 warning (see log)"
**And:** Command exits with code 0 (warnings don't block)

**Personas:** Agentic Framework Core Team
**Priority:** SHOULD

### Scenario 5: Full Export for Release

**Context:** Maintainer preparing multi-platform release

**Given:** Maintainer runs `npm run export:all`
**When:** Export pipeline executes all exporters (Claude, Copilot, OpenCode, Cursor)
**Then:** System runs Cursor exporter as part of pipeline
**And:** System exports all Cursor artifacts to `.cursor/`
**And:** System reports Cursor export status alongside other platforms
**And:** System exits with code 0 if all exporters succeed
**And:** Distribution packages include `.cursor/` directory

**Personas:** Agentic Framework Core Team
**Priority:** MUST

### Scenario 6: Agent Profile Transformation

**Context:** Engineer loads simplified agent profile in Cursor

**Given:** Exporter has transformed `doctrine/agents/python-pedro.agent.md`
**And:** Removed: YAML frontmatter, directive tables, bootstrap ceremony
**And:** Retained: Purpose, Specialization, Constraints, Tools
**When:** Engineer loads `@.cursor/agents/python-pedro.md` in Cursor
**Then:** Agent sees concise 45-line profile (vs 120-line source)
**And:** Agent understands Python specialization
**And:** Agent can invoke relevant tools
**And:** Agent does NOT see directive reference tables (irrelevant for Cursor)
**And:** Token cost reduced by 60%+

**Personas:** Software Engineer
**Priority:** MUST

### Scenario 7: Rules File Loading

**Context:** Engineer loading testing guidelines for TDD workflow

**Given:** Exporter generated `.cursor/rules/testing.md` from directives 016, 017
**When:** Engineer explicitly loads `@.cursor/rules/testing.md`
**Then:** Agent sees consolidated ATDD + TDD guidelines (~80 lines)
**And:** Agent understands RED-GREEN-REFACTOR cycle
**And:** Agent understands Given/When/Then acceptance test format
**And:** Agent does NOT see full directive preambles (stripped)
**And:** Token cost ~600 (vs 1,400 for loading both directives separately)

**Personas:** Software Engineer
**Priority:** MUST

### Scenario 8: Error Handling - Missing Source Directory

**Context:** Exporter run in repository without doctrine stack

**Given:** Repository has no `doctrine/` directory
**When:** Maintainer runs `npm run export:cursor`
**Then:** System checks for `doctrine/` directory
**And:** System errors: "❗️ doctrine/ directory not found"
**And:** System suggests: "Run from repository root with doctrine stack"
**And:** Command exits with code 1 (error)
**And:** No `.cursor/` directory created

**Personas:** Agentic Framework Core Team
**Priority:** MUST

---

## Constraints and Business Rules

### Business Rules

**BR1: Source of Truth - Doctrine Stack**
- **Rule:** `doctrine/` directory is canonical source; `.cursor/` is always generated, never edited manually
- **Applies to:** All export scenarios
- **Enforcement:** Export script overwrites `.cursor/` contents; Git ignore recommendations

**BR2: Backward Compatibility**
- **Rule:** Phase 2 export MUST NOT break Phase 1 manual artifacts (`.cursorrules`, existing Quick Reference)
- **Applies to:** Export pipeline
- **Enforcement:** Exporter preserves `.cursorrules` if exists; Quick Reference regenerated safely

**BR3: No Duplication of Content**
- **Rule:** Exported files reference `doctrine/` for deep dives; don't duplicate full content
- **Applies to:** Rules files, agent profiles
- **Enforcement:** Transformation logic strips redundant sections; keeps references

**BR4: Token Efficiency Preservation**
- **Rule:** Phase 2 export MUST NOT regress Phase 1 token efficiency (500-token auto-load)
- **Applies to:** `.cursorrules` updates, rules file generation
- **Enforcement:** Token count validation in export tests

### Technical Constraints

**TC1: File System Performance**
- **Constraint:** Export MUST complete in under 10 seconds for 21 agents + 36 directives
- **Measurement:** CI pipeline execution time
- **Rationale:** Fast iteration; acceptable as part of release process

**TC2: Node.js Compatibility**
- **Constraint:** Exporter MUST run on Node.js 18+ (repository standard)
- **Measurement:** CI test matrix (Node 18, 20, 22)
- **Rationale:** Consistent with existing exporters (Copilot, Claude, OpenCode)

**TC3: Cross-Platform**
- **Constraint:** Exporter MUST work on Linux, macOS, Windows (file path handling)
- **Measurement:** CI test on multiple OS
- **Rationale:** Repository used across platforms

**TC4: Markdown Spec Compliance**
- **Constraint:** Exported files MUST be valid CommonMark markdown
- **Measurement:** Markdown linter pass
- **Rationale:** Cursor renders markdown natively

### Non-Functional Requirements (MoSCoW)

**NFR-M1 (MUST): Export Idempotence**
- **Requirement:** Running export multiple times with unchanged source MUST produce identical output
- **Measurement:** File hash comparison (export1 == export2)
- **Verification:** Unit tests for deterministic generation

**NFR-M2 (MUST): Token Efficiency**
- **Requirement:** Exported agents MUST be 40-60 lines (vs 100-120 source lines)
- **Measurement:** Line count analysis in export metrics
- **Verification:** Automated line count validation

**NFR-S1 (SHOULD): Export Speed**
- **Requirement:** Incremental export SHOULD process 1 changed agent in under 500ms
- **Measurement:** Benchmark suite
- **Verification:** Performance regression tests

**NFR-C1 (COULD): Memory Efficiency**
- **Requirement:** Exporter COULD process large doctrine stacks (100+ agents) without memory issues
- **Measurement:** Max heap size during export
- **Verification:** Stress tests with synthetic large doctrine stacks

### Edge Cases and Limits

**Maximum Values:**
- Max agents: 100 (10x current, future-proofing)
- Max directives: 100 (3x current)
- Max single file size: 500 KB (large diagrams in directives)
- Max Quick Reference size: 250 lines (token cap: 1,000)

**Invalid Inputs:**
- Agent file missing YAML frontmatter → Export with warning, no transformation
- Agent file with malformed markdown → Validate, report, continue export
- Directive file with binary content → Skip, report error
- Empty `doctrine/` directory → Error, exit code 1

**Timeouts:**
- Export operation: 30 seconds max (CI timeout)
- File I/O per file: 1 second max
- Total pipeline (`export:all`): 2 minutes max

**Fallbacks:**
- Incremental export failure → Fall back to full export
- Validation failure → Continue export, report warnings
- Missing optional sections → Export without them, log notice

---

## Implementation Architecture

### Component Overview

```
tools/exporters/
├── cursor-exporter.js           # Main CLI entry point
├── cursor/
│   ├── transformer.js           # Agent/directive transformation logic
│   ├── rules-generator.js       # Rules file consolidation
│   ├── quick-reference-generator.js  # Index auto-generation
│   ├── validator.js             # Export validation
│   └── templates/               # Rules file templates
│       ├── guidelines.template.md
│       ├── testing.template.md
│       └── architecture.template.md
└── common/
    ├── file-utils.js            # Shared file I/O
    ├── markdown-parser.js       # YAML frontmatter extraction
    └── token-counter.js         # Token estimation
```

### Data Flow

```
1. Read Source
   doctrine/agents/*.agent.md  ─┐
   doctrine/directives/*.md    ─┼──► Transformer
   doctrine/tactics/           ─┘        │
                                         ▼
2. Transform                      Agent Simplifier
   - Strip YAML frontmatter           (remove ceremony)
   - Remove directive tables               │
   - Consolidate rules                     ▼
   - Generate indices               Rules Generator
                                     (consolidate)
                                         │
3. Write Output                          ▼
   .cursor/agents/*.md  ◄───── Quick Reference Gen
   .cursor/directives/  ◄───── (auto-index)
   .cursor/rules/       ◄─────
   .cursor/QUICK_REFERENCE.md
```

### Transformation Rules

**Agent Profile Transformation:**

| Source Section | Action | Rationale |
|----------------|--------|-----------|
| YAML frontmatter | REMOVE | Cursor doesn't parse YAML |
| Purpose | KEEP | Core specialization info |
| Specialization | KEEP | Defines role scope |
| Tools | KEEP | Cursor tool invocation |
| Key constraints | KEEP | Critical behavioral boundaries |
| Directive tables | REMOVE | Ceremony not used by Cursor |
| Bootstrap declarations | REMOVE | Handled by `.cursorrules` |
| Mode protocols | REMOVE | Not Cursor convention |
| Collaboration contracts | REMOVE | Boilerplate text |
| Context source listings | REMOVE | Metadata not needed |

**Rules File Consolidation:**

| Theme | Source Directives | Target File | Max Lines |
|-------|------------------|-------------|-----------|
| Guidelines | general_guidelines.md, operational_guidelines.md | `.cursor/rules/guidelines.md` | 80 |
| Testing | 016_atdd.md, 017_tdd.md | `.cursor/rules/testing.md` | 100 |
| Architecture | 018_traceable_decisions.md | `.cursor/rules/architecture.md` | 80 |
| Collaboration | 019_file_based_collaboration.md | `.cursor/rules/collaboration.md` | 80 |
| Coding | python-conventions.md | `.cursor/rules/coding-conventions.md` | 100 |

### Export Pipeline

**Execution Flow:**

```bash
npm run export:cursor
  ↓
package.json → node tools/exporters/cursor-exporter.js
  ↓
1. Validate preconditions (doctrine/ exists)
2. Create .cursor/ directory structure
3. Export agents (21 files)
4. Copy directives (36+ files)
5. Generate rules (5 files)
6. Generate Quick Reference (1 file)
7. Validate outputs
8. Report metrics
9. Exit 0
```

**Integration with `export:all`:**

```json
// package.json
{
  "scripts": {
    "export:cursor": "node tools/exporters/cursor-exporter.js",
    "export:all": "npm run export:claude && npm run export:copilot && npm run export:opencode && npm run export:cursor"
  }
}
```

---

## Testing Strategy

### Unit Tests

**Location:** `tests/unit/exporters/cursor/`

**Coverage:**
- `transformer.test.js` - Agent transformation logic
  - Test YAML frontmatter removal
  - Test section retention (Purpose, Specialization)
  - Test ceremony removal (directive tables, bootstrap)
  - Test line count reduction (target: 40-60 lines)
- `rules-generator.test.js` - Rules consolidation
  - Test multi-directive merging
  - Test template variable substitution
  - Test line count limits (target: <100 lines each)
- `quick-reference-generator.test.js` - Index generation
  - Test directive index extraction
  - Test agent roster extraction
  - Test decision tree embedding
- `validator.test.js` - Export validation
  - Test missing section detection
  - Test malformed markdown detection
  - Test warning/error reporting

### Integration Tests

**Location:** `tests/integration/exporters/cursor/`

**Coverage:**
- `end-to-end-export.test.js`
  - Test full export pipeline (doctrine → .cursor)
  - Verify all 21 agents exported
  - Verify all 36 directives copied
  - Verify 5 rules files generated
  - Verify Quick Reference regenerated
- `incremental-export.test.js`
  - Test modification time detection
  - Test skip unchanged files
  - Test single-file update

### Acceptance Tests

**Location:** `tests/acceptance/exporters/cursor/`

**Scenarios:**
- Scenario 1: First-time export (happy path)
- Scenario 3: Dry-run preview
- Scenario 4: Validation failure (non-blocking)
- Scenario 8: Error handling (missing source)

**Verification:**
- All MUST scenarios pass
- All SHOULD scenarios pass or documented workaround
- Token efficiency preserved (500-token auto-load)

---

## Deployment and Rollout

### Phase 2.1: Core Exporter (First PR)

**Deliverables:**
- [ ] `tools/exporters/cursor-exporter.js` (main script)
- [ ] Agent transformation logic (strip ceremony)
- [ ] Directive mirroring (copy files)
- [ ] NPM script integration (`npm run export:cursor`)
- [ ] Unit tests (transformer, validator)
- [ ] Integration test (end-to-end export)
- [ ] Documentation update (DOCTRINE_DISTRIBUTION.md)

**Success Criteria:**
- Export runs without errors
- 21 agents exported, 36 directives copied
- All tests passing
- Token efficiency preserved

### Phase 2.2: Rules Generation (Second PR)

**Deliverables:**
- [ ] Rules generator implementation
- [ ] 5 themed rules files (guidelines, testing, architecture, collaboration, coding)
- [ ] Template system for rules consolidation
- [ ] Unit tests (rules-generator)
- [ ] Documentation update (rules file usage guide)

**Success Criteria:**
- Rules files under 100 lines each
- Content distilled from source directives
- Token efficiency gains measured (consolidated vs separate directives)

### Phase 2.3: Quick Reference Auto-Generation (Third PR)

**Deliverables:**
- [ ] Quick Reference generator implementation
- [ ] Directive index extraction from `doctrine/directives/`
- [ ] Agent roster extraction from `doctrine/agents/`
- [ ] Tactics catalog extraction from `doctrine/tactics/README.md`
- [ ] Decision tree template embedding
- [ ] Unit tests (quick-reference-generator)

**Success Criteria:**
- Quick Reference under 200 lines
- All indices accurate (reflects current doctrine stack)
- Manual Quick Reference deprecated (replaced by auto-generated)

### Phase 2.4: Advanced Features (Optional)

**Deliverables:**
- [ ] Incremental export (modification time comparison)
- [ ] Dry-run mode (`--dry-run` flag)
- [ ] Export metrics (file counts, token reductions)
- [ ] Watch mode (`--watch` flag) - if demand

**Success Criteria:**
- Incremental export 5x faster for single-file updates
- Dry-run safe (no file writes)
- Metrics useful for monitoring efficiency

---

## Success Metrics

### Quantitative

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Export Time** | <10 seconds | CI pipeline duration |
| **Agent Size Reduction** | 40-60 lines (from 100-120) | Automated line count |
| **Token Efficiency** | Maintain Phase 1 (500 auto-load) | Token counter validation |
| **Export Coverage** | 100% (21 agents, 36 directives) | File count verification |
| **Rules File Size** | <100 lines each | Automated line count |
| **Quick Reference Size** | <200 lines | Automated line count |
| **Test Coverage** | 90%+ (exporter code) | Jest coverage report |

### Qualitative

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Maintenance Burden** | Low (no manual Quick Reference updates) | Maintainer feedback |
| **Ecosystem Parity** | High (comparable to Claude/Copilot) | Feature comparison |
| **Discoverability** | High (agents/directives in dedicated dirs) | User feedback |
| **Consistency** | High (uniform transformations) | Code review |

---

## Open Questions

### Unresolved Requirements

- [ ] **Q1:** Should `.cursor/tactics/` be mirrored or referenced from `doctrine/tactics/`?
  - **Assigned to:** Architect Alphonso
  - **Target Date:** Before Phase 2.1 PR
  - **Blocking:** Tactics export logic
  - **Options:** (A) Mirror to `.cursor/tactics/` for discoverability, (B) Reference `doctrine/tactics/` to avoid duplication

- [ ] **Q2:** Should rules files embed directive content or reference directive files?
  - **Assigned to:** Curator Claire
  - **Target Date:** Before Phase 2.2 PR
  - **Blocking:** Rules generator design
  - **Options:** (A) Embed distilled content (token-efficient), (B) Reference directives (single source of truth)

- [ ] **Q3:** Should Quick Reference be committed to git or always regenerated?
  - **Assigned to:** DevOps Danny
  - **Target Date:** Before Phase 2.3 PR
  - **Blocking:** Git workflow
  - **Options:** (A) Commit (stable, reviewable), (B) Gitignore + regenerate (always fresh)

### Design Decisions Needed

- [ ] **D1:** Template system for rules files - Custom templates or hardcoded logic?
  - **Options:** (A) Template files with variable substitution (flexible), (B) Hardcoded transformation (simple)
  - **Decision Maker:** Architect Alphonso
  - **Context:** Affects FR-C1 (custom templates)

- [ ] **D2:** Validation strictness - Block export on warnings or continue?
  - **Options:** (A) Block on warnings (strict quality), (B) Continue with warnings (permissive)
  - **Decision Maker:** Code Reviewer Cindy
  - **Context:** Scenario 4 behavior

### Clarifications Required

- [ ] **C1:** Does Cursor officially support `.cursor/` directory convention?
  - **Who to ask:** Cursor documentation / community forums
  - **Why it matters:** Validates Phase 2 approach; if unsupported, fallback to `.cursorrules` only

- [ ] **C2:** Should Phase 2 update `.cursorrules` or leave Phase 1 artifact unchanged?
  - **Who to ask:** User feedback (Software Engineers using Cursor)
  - **Why it matters:** Backward compatibility vs optimization opportunity

---

## Out of Scope

**Explicitly NOT included in Phase 2:**

1. **Cursor Plugin Development**
   - **Reason:** Requires Cursor extension API research; deferred to Phase 3
   - **Future:** If Cursor exposes native agent integration, revisit

2. **Dynamic Context Assembly**
   - **Reason:** Task-specific `.cursorrules` generation adds complexity without clear demand
   - **Future:** Reconsider if users report frequent context switching pain

3. **Custom Syntax Highlighting**
   - **Reason:** Standard markdown sufficient; no value-add
   - **Future:** N/A

4. **Cursor Marketplace Integration**
   - **Reason:** No evidence Cursor has marketplace; research needed
   - **Future:** If marketplace exists, explore distribution

5. **Multi-Language Support**
   - **Reason:** Framework currently Python-focused; expand as needed
   - **Future:** If Java/TypeScript agents added, extend exporters

---

## Acceptance Criteria Summary

**Phase 2 is DONE when:**

- [ ] All MUST requirements (FR-M1 through FR-M6) implemented
- [ ] All SHOULD requirements (FR-S1 through FR-S4) implemented OR workarounds documented
- [ ] Cursor exporter exists at `tools/exporters/cursor-exporter.js`
- [ ] NPM command `npm run export:cursor` works
- [ ] All 21 agents exported to `.cursor/agents/` (simplified)
- [ ] All 36 directives copied to `.cursor/directives/`
- [ ] 5 rules files generated in `.cursor/rules/`
- [ ] Quick Reference auto-generated in `.cursor/QUICK_REFERENCE.md`
- [ ] Unit tests passing (90%+ coverage)
- [ ] Integration tests passing (end-to-end export)
- [ ] Acceptance tests passing (Scenarios 1, 3, 4, 8)
- [ ] Documentation updated (DOCTRINE_DISTRIBUTION.md, bootstrap.md)
- [ ] Token efficiency preserved (Phase 1 baseline maintained)
- [ ] Export completes in <10 seconds
- [ ] Open questions Q1-Q3 resolved
- [ ] Software Engineer personas validate usability

---

## Traceability

### Derives From (Strategic)

- **Phase 1 Implementation:** `feature/dist-cursor` (manual `.cursorrules` + Quick Reference)
- **Parent Spec:** SPEC-DIST-001 (Multi-Tool Distribution Architecture)
- **Related Spec:** SPEC-DIST-002 (Claude Code Optimization - similar transformation approach)
- **Strategic Goal:** Ecosystem parity (Cursor = Claude = Copilot = OpenCode)

### Feeds Into (Tactical)

- **Implementation Tasks:**
  - `work/collaboration/inbox/2026-02-10-devops-danny-cursor-exporter-core.yaml` (Phase 2.1)
  - `work/collaboration/inbox/2026-02-10-devops-danny-cursor-rules-generator.yaml` (Phase 2.2)
  - `work/collaboration/inbox/2026-02-10-curator-claire-quick-reference-automation.yaml` (Phase 2.3)
- **Acceptance Tests:** `tests/acceptance/exporters/cursor/`
- **Documentation Updates:**
  - `docs/architecture/design/DOCTRINE_DISTRIBUTION.md` - Add Phase 2 section
  - `doctrine/guidelines/bootstrap.md` - Update Cursor export instructions
  - `AGENTS.md` - Note Cursor exporter in Section 2 (Context Stack)

### Related Specifications

- **Dependencies:** SPEC-DIST-001 (approved, defines multi-tool architecture)
- **Dependents:** None (Phase 2 is leaf node)
- **Cross-References:** SPEC-DIST-002 (Claude Code optimization - similar patterns)

---

## Change Log

| Date | Author | Change | Reason |
|------|--------|--------|--------|
| 2026-02-10 | Generic Cursor Agent | Initial draft created | Phase 1 complete, Phase 2 analysis requested |

---

## Approval

### Reviewers

| Role | Name | Date | Status | Comments |
|------|------|------|--------|----------|
| Target Persona | Software Engineer | Pending | ⏳ Pending | - |
| Architect | Architect Alphonso | Pending | ⏳ Pending | - |
| Implementer | DevOps Danny | Pending | ⏳ Pending | - |
| Curator | Curator Claire | Pending | ⏳ Pending | - |
| Stakeholder | Stijn | Pending | ⏳ Pending | - |

### Sign-Off

**Final Approval:**
- **Date:** Pending
- **Approved By:** Pending
- **Status:** Draft (awaiting review)

---

## Metadata

**Tags:** `#cursor` `#distribution` `#exporter` `#phase-2` `#automation` `#token-efficiency`

**Related Files:**
- Phase 1: `.cursorrules`, `.cursor/QUICK_REFERENCE.md`
- Template: `doctrine/templates/specifications/feature-spec-template.md`
- Parent Spec: `specifications/initiatives/framework-distribution/SPEC-DIST-001-multi-tool-distribution.md`
- Related Spec: `specifications/initiatives/framework-distribution/SPEC-DIST-002-claude-code-optimization.md`
- Exporters: `tools/exporters/copilot-generator.js`, `tools/exporters/opencode-generator.js`
- Tests: `tests/unit/exporters/`, `tests/integration/exporters/`

**Navigation:**
- Previous: SPEC-DIST-002 (Claude Code Optimization)
- Next: N/A (Phase 3 TBD)
- Parent: SPEC-DIST-001 (Multi-Tool Distribution)

---

## Notes for Reviewers

**Key Review Focus Areas:**

1. **Transformation Logic:** Is agent simplification approach correct? (Section: Scenarios 6-7, Implementation Architecture)
2. **Rules Consolidation:** Does rules file generation make sense? (FR-M6, Scenario 7)
3. **Token Efficiency:** Are we preserving Phase 1 gains? (NFR-M2, Success Metrics)
4. **Open Questions:** Need decisions on Q1-Q3 before implementation (Open Questions section)
5. **Export Pipeline:** Is integration with `export:all` appropriate? (Scenario 5, Deployment)

**Phase 1 Context:**
- `.cursorrules` (500 tokens) replaces AGENTS.md (3,850 tokens) = 87% reduction
- `.cursor/QUICK_REFERENCE.md` (800 tokens) manually created, needs automation
- Full doctrine stack accessible by reference (`@doctrine/agents/`, `@doctrine/directives/`)

**Phase 2 Goal:**
- Automate Quick Reference generation
- Export agents/directives to `.cursor/` for discoverability
- Generate consolidated rules files for modular loading
- Achieve ecosystem parity with Claude/Copilot distributions

**Open for Discussion:**
- Should we prioritize all SHOULD requirements or defer some to Phase 2.5?
- Is incremental export worth the complexity (FR-S3)?
- Should validation be strict (block) or permissive (warn)?

---

**Version:** 1.0.0  
**Status:** Draft  
**Ready for:** Architect review, stakeholder feedback
