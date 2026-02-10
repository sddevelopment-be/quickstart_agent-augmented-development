---
id: SPEC-DIST-002
title: Claude Code Distribution Optimization
status: implemented
initiative: framework-distribution
version: 1.1.0
author: Claude Sonnet 4.5
architect_review: Architect Alphonso
created: 2026-02-10
updated: 2026-02-10
stakeholders: [stijn, architect-alphonso, devops-danny, backend-benny, code-reviewer-cindy, analyst-annie, curator-claire]
approved_by: stijn
approved_date: 2026-02-10
priority: high
type: feature
tags: [distribution, claude-code, exporter, optimization]
parent: SPEC-DIST-001
---

# Claude Code Distribution Optimization

## Executive Summary

The current Claude Code deployment (`deploy-skills.js`) copies doctrine content verbatim to `.claude/`. This produces agent files bloated with doctrine ceremony, populates a non-native `prompts/` directory, and omits the two highest-impact native artifacts: `CLAUDE.md` (auto-loaded project instructions) and `.claude/rules/` (auto-loaded modular guidelines). This specification defines a Claude Code-specific generator and updated deployment that produces artifacts optimized for how Claude Code actually consumes them.

**Parent Specification:** SPEC-DIST-001 (Multi-Tool Distribution Architecture, approved)

**Fit Analysis:** `work/reports/claude_code-fit.md`

---

## Problem Statement

### Current State

The `deploy-skills.js` script deploys to `.claude/` in three modes:

1. **Skills** (`deployClaudeSkills`): Converts JSON from `dist/skills/claude-code/` to `SKILL.md` format. Works correctly.
2. **Agents** (`deployClaudeAgents`): Copies `doctrine/agents/*.agent.md` verbatim. Produces ~100-line files with directive reference tables, bootstrap declarations, mode protocols, and initialization ceremony that Claude Code does not process. Wastes tokens.
3. **Prompts** (`deployClaudePrompts`): Copies prompt templates to `.claude/prompts/`. This directory is not natively recognized by Claude Code.

### What's Missing

| Artifact | Native? | Impact | Currently Generated? |
|---|---|---|---|
| `CLAUDE.md` | Yes (auto-loaded every session) | Highest | No |
| `.claude/rules/*.md` | Yes (auto-loaded, modular) | High | No |
| Simplified agents | Yes (subagent definitions) | Medium | No (verbatim copies instead) |
| `.claude/skills/` | Yes (on-demand) | Medium | Yes (working correctly) |
| `.claude/prompts/` | No | None | Yes (wasted effort) |

### Impact

- Every Claude Code session starts without project context (no CLAUDE.md)
- Agent subagent invocations waste tokens on ceremony Claude Code ignores
- Prompts directory content is invisible to Claude Code
- No auto-loaded coding conventions, testing guidelines, or collaboration norms

---

## Requirements

### Functional Requirements

**FR-1: CLAUDE.md Generation**
- The system SHALL generate a `CLAUDE.md` file at the repository root
- The system SHALL compose CLAUDE.md from: `docs/VISION.md` (purpose), `doctrine/directives/003_repository_quick_reference.md` (structure), `doctrine/guidelines/python-conventions.md` (coding conventions), and project commands
- The generated CLAUDE.md SHALL be under 120 lines to avoid context bloat
- The generated CLAUDE.md SHALL include pointers to deeper context (doctrine/ paths) rather than inlining full content

**FR-2: Rules Generation**
- The system SHALL generate `.claude/rules/*.md` files from doctrine content
- The system SHALL produce at minimum these rules files:
  - `guidelines.md` — distilled from `doctrine/guidelines/general_guidelines.md` + `doctrine/guidelines/operational_guidelines.md`
  - `coding-conventions.md` — distilled from `doctrine/guidelines/python-conventions.md`
  - `testing.md` — distilled from `doctrine/directives/016_acceptance_test_driven_development.md` + `doctrine/directives/017_test_driven_development.md`
  - `architecture.md` — distilled from `doctrine/directives/018_traceable_decisions.md`
  - `collaboration.md` — distilled from `doctrine/directives/019_file_based_collaboration.md`
- Each rules file SHALL be concise (under 80 lines) with actionable instructions, not philosophical preambles

**FR-3: Agent Simplification**
- The system SHALL transform `doctrine/agents/*.agent.md` into simplified Claude Code subagent definitions
- Simplified agents SHALL retain: name, description, tools list, model hint, and behavioral instructions (purpose + specialization + key constraints)
- Simplified agents SHALL remove: directive reference tables, bootstrap declarations, mode protocol tables, initialization declarations, context source listings, collaboration contract boilerplate, spec-driven phase authority tables
- Simplified agents SHALL be under 40 lines each

**FR-4: Prompts Deprecation**
- The system SHALL NOT deploy to `.claude/prompts/` (not natively recognized)
- The system SHOULD migrate any prompt content not already covered by skills into new skills

**FR-5: Pipeline Integration**
- The system SHALL integrate with the existing `npm run deploy:claude` pipeline
- The system SHALL add new deployment flags: `--rules`, `--claude-md`
- The system SHALL update `npm run deploy:claude` to include rules and CLAUDE.md generation
- The system SHALL preserve backward compatibility with existing `--claude`, `--agents` flags

### Non-Functional Requirements

**NFR-1: Token Efficiency**
- Generated CLAUDE.md SHALL consume <3000 tokens when loaded by Claude Code
- Generated rules files SHALL consume <1500 tokens each
- Simplified agent files SHALL consume <1000 tokens each (vs ~3000+ current)

**NFR-2: Idempotency**
- Running the deployment twice SHALL produce identical output
- Generated files SHALL not include timestamps or other non-deterministic content in their body (manifests may include generation timestamps)

**NFR-3: Source Fidelity**
- Generated content SHALL accurately represent the source doctrine content
- No behavioral instructions SHALL be invented or inferred beyond what exists in source files
- Generated content SHALL include source attribution comments (e.g., `<!-- Source: doctrine/guidelines/general_guidelines.md -->`)

---

## User Scenarios

### Scenario 1: Fresh Project Setup

**Given:** A developer clones this repository for the first time
**When:** They run `npm run deploy:claude`
**Then:** The following files are generated:
  - `CLAUDE.md` at repository root with project purpose, structure, conventions, and commands
  - `.claude/rules/guidelines.md` with distilled behavioral guidelines
  - `.claude/rules/coding-conventions.md` with Python conventions
  - `.claude/rules/testing.md` with ATDD/TDD essentials
  - `.claude/rules/architecture.md` with ADR conventions
  - `.claude/rules/collaboration.md` with file-based orchestration summary
  - `.claude/agents/*.md` with simplified agent definitions
  - `.claude/skills/*/SKILL.md` with skill definitions (unchanged)
**And:** `.claude/prompts/` is NOT created
**And:** Claude Code sessions auto-load CLAUDE.md and rules without user action

### Scenario 2: Doctrine Update Propagation

**Given:** A developer modifies `doctrine/guidelines/python-conventions.md`
**When:** They run `npm run deploy:claude`
**Then:** `.claude/rules/coding-conventions.md` reflects the updated content
**And:** Other rules files remain unchanged
**And:** CLAUDE.md remains unchanged (unless its source files were modified)

### Scenario 3: Agent Subagent Invocation

**Given:** Claude Code is running with the simplified agent files deployed
**When:** A user delegates a task to the backend-benny subagent
**Then:** The subagent receives a concise system prompt (~30 lines) containing name, purpose, specialization, key constraints, and tools
**And:** The subagent does NOT receive directive reference tables, bootstrap declarations, or mode protocols

### Scenario 4: Selective Deployment

**Given:** A developer wants to regenerate only rules files
**When:** They run `node tools/scripts/deploy-skills.js --rules`
**Then:** Only `.claude/rules/*.md` files are regenerated
**And:** Other `.claude/` content is not modified

### Scenario 5: Backward Compatibility

**Given:** Existing CI/CD scripts use `npm run deploy:claude`
**When:** The updated deployment script runs
**Then:** All previously generated artifacts (skills, agents) are still produced
**And:** New artifacts (CLAUDE.md, rules) are additionally produced
**And:** `.claude/prompts/` is no longer produced

---

## Technical Constraints

**C-1:** The generator MUST be implemented in Node.js to match the existing exporter pipeline (`tools/exporters/*.js`, `tools/scripts/*.js`)

**C-2:** The generator MUST read from `doctrine/` as source directory (per SPEC-DIST-001 decision)

**C-3:** The generator MUST NOT require additional npm dependencies beyond what `package.json` already declares (`gray-matter`, `js-yaml`, `glob`)

**C-4:** CLAUDE.md generation MUST work even if some source files are missing (graceful degradation with warnings)

**C-5:** The `CLAUDE.md` file is generated at repository root, not inside `.claude/` (Claude Code checks both locations; root is conventional)

---

## Implementation Guidance

### New Files

1. **`tools/exporters/claude-code-generator.js`** — Core generator with functions:
   - `generateClaudeMd(config)` — Composes CLAUDE.md from source files
   - `generateRulesFile(sourceFiles, outputName)` — Distills doctrine content into a rules file
   - `simplifyAgent(agentIR)` — Strips doctrine ceremony from agent IR, produces lean subagent markdown

2. **Updated `tools/scripts/deploy-skills.js`** — Extended with:
   - `deployClaudeRules()` — Generates `.claude/rules/*.md`
   - `deployClaudeMd()` — Generates root `CLAUDE.md`
   - Updated `deployClaudeAgents()` — Uses `simplifyAgent()` instead of verbatim copy
   - Removed `deployClaudePrompts()` (or retained behind `--prompts-legacy` flag)

### Agent Simplification Algorithm

```
Input: doctrine/agents/*.agent.md (full doctrine format)
Process:
  1. Parse YAML frontmatter (retain: name, description, tools)
  2. Extract Purpose section (section 2 in current format)
  3. Extract Specialization bullet points (section 3, primary + avoid)
  4. Map tools array to Claude Code tool names (Read, Write, Edit, Bash, Grep, Glob)
  5. Infer model hint from agent role (opus for architect/reviewer, sonnet for dev, haiku for simple tasks)
Output: Simplified .md with frontmatter + behavioral paragraph
```

### Rules Distillation Algorithm

```
Input: One or more doctrine source .md files
Process:
  1. Read source files
  2. Extract actionable content (strip preambles, version history, metadata sections)
  3. Condense to imperative instructions (<80 lines)
  4. Add source attribution comment
  5. Write to .claude/rules/{name}.md
Output: Concise rules file with only actionable instructions
```

### Source-to-Output Mapping

| Output File | Source File(s) | Distillation Strategy |
|---|---|---|
| `CLAUDE.md` | `docs/VISION.md`, `doctrine/directives/003_repository_quick_reference.md`, `doctrine/guidelines/python-conventions.md` | Extract purpose (3 lines), structure summary (key dirs only), conventions (top-level rules only), common commands |
| `.claude/rules/guidelines.md` | `doctrine/guidelines/general_guidelines.md`, `doctrine/guidelines/operational_guidelines.md` | Merge behavioral and operational norms into single actionable list |
| `.claude/rules/coding-conventions.md` | `doctrine/guidelines/python-conventions.md` | Extract formatting, test patterns, type hints, key conventions; drop examples and tooling setup |
| `.claude/rules/testing.md` | `doctrine/directives/016_*.md`, `doctrine/directives/017_*.md` | Merge ATDD + TDD into unified test-first workflow; keep cycle description, drop glossary references |
| `.claude/rules/architecture.md` | `doctrine/directives/018_traceable_decisions.md` | Extract ADR workflow essentials; drop templates (link to them instead) |
| `.claude/rules/collaboration.md` | `doctrine/directives/019_file_based_collaboration.md` | Extract orchestration norms; focus on work/ directory usage and YAML task format |
| `.claude/agents/*.md` | `doctrine/agents/*.agent.md` | Simplify per algorithm above |

---

## Acceptance Criteria

**AC-1: CLAUDE.md exists and is well-formed**
- [x] `CLAUDE.md` exists at repository root after `npm run deploy:claude`
- [x] Contains project purpose, repository structure, coding conventions, and common commands
- [x] Is under 120 lines
- [x] Does not inline full doctrine content (uses pointers/links)

**AC-2: Rules files exist and are well-formed**
- [x] `.claude/rules/` directory contains at least 5 rules files after deployment
- [x] Each rules file is under 80 lines
- [x] Each rules file contains a source attribution comment
- [x] Rules content matches source doctrine content (no invented instructions)

**AC-3: Agent files are simplified**
- [x] `.claude/agents/*.md` files are under 40 lines each after deployment
- [x] Each agent retains: name, description, tools, purpose, specialization
- [x] Each agent omits: directive tables, bootstrap declarations, mode protocols
- [x] Agent manifest.json is still generated

**AC-4: Prompts directory not created**
- [x] `.claude/prompts/` is NOT created by `npm run deploy:claude`
- [x] Existing `.claude/prompts/` content can be cleaned up manually

**AC-5: Pipeline integration**
- [x] `npm run deploy:claude` produces all artifacts (skills + agents + rules + CLAUDE.md)
- [x] `node tools/scripts/deploy-skills.js --rules` produces only rules
- [x] `node tools/scripts/deploy-skills.js --claude-md` produces only CLAUDE.md
- [x] Existing `--claude` and `--agents` flags still work

**AC-6: Idempotency**
- [x] Running `npm run deploy:claude` twice produces identical file content

---

## References

- **Parent Spec:** `specifications/initiatives/framework-distribution/SPEC-DIST-001-multi-tool-distribution.md`
- **Fit Analysis:** `work/reports/claude_code-fit.md`
- **Existing Deployment Script:** `tools/scripts/deploy-skills.js`
- **Existing Parser:** `tools/exporters/parser.js`
- **Directive 016:** `doctrine/directives/016_acceptance_test_driven_development.md`
- **Directive 017:** `doctrine/directives/017_test_driven_development.md`
