# Implementation Plan: SPEC-DIST-002 — Claude Code Distribution Optimization

**Plan ID:** PLAN-DIST-002
**Date:** 2026-02-10
**Planner:** Planning Petra
**Specification:** `specifications/initiatives/framework-distribution/SPEC-DIST-002-claude-code-optimization.md`
**Technical Design:** `work/reports/architecture/2026-02-10-SPEC-DIST-002-technical-design.md`
**Status:** Ready for execution

---

## Executive Summary

3 batches, 6 tasks, estimated 18 hours total effort. All work uses the existing Node.js exporter pipeline. No new dependencies required.

**Critical Path:** Batch 1 (generator core) → Batch 2 (deployment integration) → Batch 3 (validation + cleanup)

---

## Batch 1: Generator Core (Foundation)

**Theme:** Build the claude-code-generator.js module with all three transformation functions
**Effort:** 8 hours
**Blocking:** Batches 2 and 3 depend on this

### Task 1.1: Implement simplifyAgent()

**Agent:** Backend Benny (Python/Node backend specialist)
**Priority:** Critical (blocks agent deployment)
**Effort:** 3 hours

**Scope:**
- Create `tools/exporters/claude-code-generator.js` module scaffold
- Implement `simplifyAgent(agentIR)` function per technical design section 2.1
- Implement tool name mapping (doctrine lowercase → Claude Code PascalCase)
- Implement model inference (architect→opus, dev→sonnet, etc.)
- Write unit tests: tool mapping, model inference, line count enforcement, ceremony stripping
- Test against at least 3 real agent IRs (architect, backend-dev, curator)

**Acceptance Criteria:**
- simplifyAgent produces output <40 lines for every doctrine agent
- No directive tables, bootstrap declarations, or mode protocols in output
- Tools mapped to Claude Code names (Read, Write, Edit, Bash, Grep, Glob)
- Unit tests pass with >85% function coverage

**Dependencies:** None (uses existing parser.js output)

---

### Task 1.2: Implement generateRulesFile()

**Agent:** Backend Benny
**Priority:** High
**Effort:** 2.5 hours

**Scope:**
- Implement `generateRulesFile(sourceFiles, ruleName)` function
- Implement content distillation: strip frontmatter, version history, metadata, glossary refs
- Implement the RULES_MAPPING configuration object
- Implement 80-line enforcement with truncation strategy
- Implement source attribution comments
- Write unit tests: distillation strips metadata, output under limit, source attribution present
- Test with real doctrine files (general_guidelines.md, python-conventions.md, directive 016)

**Acceptance Criteria:**
- Each generated rules file is under 80 lines
- Metadata sections (version history, "Last Updated", "Related Directives") stripped
- Source attribution comment present in each file
- Actionable instructions preserved (bullets, code examples, imperative statements)
- Unit tests pass

**Dependencies:** None

---

### Task 1.3: Implement generateClaudeMd()

**Agent:** Backend Benny
**Priority:** High
**Effort:** 2.5 hours

**Scope:**
- Implement `generateClaudeMd(config)` function
- Implement section extraction from VISION.md (purpose paragraph)
- Implement structure summary extraction from directive 003
- Implement conventions extraction from python-conventions.md
- Implement hardcoded common commands section
- Implement 120-line enforcement
- Implement graceful degradation when source files missing
- Write unit tests: output structure, line count, missing file handling, content accuracy

**Acceptance Criteria:**
- Generated CLAUDE.md under 120 lines
- Contains: project purpose, directory structure, coding conventions, common commands, pointers to deeper context
- Graceful warning (not crash) if a source file is missing
- Includes `<!-- Generated from doctrine/ — do not edit manually -->` header
- Unit tests pass

**Dependencies:** None

---

## Batch 2: Deployment Integration

**Theme:** Wire generator into deploy-skills.js pipeline
**Effort:** 5 hours
**Depends on:** Batch 1 complete

### Task 2.1: Update deploy-skills.js

**Agent:** DevOps Danny (build automation specialist)
**Priority:** High
**Effort:** 3 hours

**Scope:**
- Add `deployClaudeMd()` function calling `generateClaudeMd()`
- Add `deployClaudeRules()` function calling `generateRulesFile()` for each RULES_MAPPING entry
- Modify `deployClaudeAgents()` to use parser.js + `simplifyAgent()` instead of verbatim copy
- Add CLI flags: `--rules`, `--claude-md`
- Update `--all` default to include rules and CLAUDE.md
- Deprecate `deployClaudePrompts()` (retain behind `--prompts-legacy`)
- Update summary output to list new artifact locations

**Acceptance Criteria:**
- `npm run deploy:claude` produces: CLAUDE.md, .claude/rules/*, .claude/agents/* (simplified), .claude/skills/*
- `node tools/scripts/deploy-skills.js --rules` only generates rules
- `node tools/scripts/deploy-skills.js --claude-md` only generates CLAUDE.md
- `--agents` flag uses simplified agents (not verbatim)
- `.claude/prompts/` not created by default
- Existing `--claude` and `--copilot` and `--opencode` flags unaffected

**Dependencies:** Tasks 1.1, 1.2, 1.3

---

### Task 2.2: Update package.json scripts

**Agent:** DevOps Danny
**Priority:** Medium
**Effort:** 0.5 hours

**Scope:**
- Add `deploy:claude:rules` script
- Add `deploy:claude:md` script
- Update `deploy:claude` to include new artifacts
- Verify `build` script (`npm run export:all && npm run deploy:all`) still works end-to-end

**Acceptance Criteria:**
- All new npm scripts work
- `npm run build` succeeds with no errors
- No breaking changes to existing scripts

**Dependencies:** Task 2.1

---

### Task 2.3: Write integration tests

**Agent:** Code Reviewer Cindy (review + test quality)
**Priority:** High
**Effort:** 1.5 hours

**Scope:**
- Create `tests/integration/deploy-claude-code.test.js`
- Test full deployment produces all expected artifacts
- Test line count limits enforced (CLAUDE.md <120, rules <80, agents <40)
- Test idempotency (deploy twice → identical output)
- Test selective deployment flags (--rules, --claude-md, --agents)
- Test .claude/prompts/ not created
- Test backward compatibility of existing flags

**Acceptance Criteria:**
- All integration tests pass
- Tests run in <10 seconds
- Tests use temporary directories (no side effects on real .claude/)

**Dependencies:** Task 2.1

---

## Batch 3: Validation & Cleanup

**Theme:** End-to-end validation, documentation, cleanup
**Effort:** 5 hours
**Depends on:** Batch 2 complete

### Task 3.1: End-to-end validation and spec update

**Agent:** Analyst Annie (validation specialist)
**Priority:** High
**Effort:** 2 hours

**Scope:**
- Run `npm run deploy:claude` on the actual repository
- Verify all 6 acceptance criteria from SPEC-DIST-002
- Verify generated CLAUDE.md content is accurate and useful
- Verify generated rules files contain actionable instructions (not ceremony)
- Verify simplified agents are functional as Claude Code subagents
- Spot-check source attribution comments
- Update SPEC-DIST-002 status from `draft` to `implemented`
- Document any deviations or issues found

**Acceptance Criteria:**
- All 6 SPEC-DIST-002 acceptance criteria checked off
- Spec status updated to `implemented`
- Any issues documented and triaged

**Dependencies:** Tasks 2.1, 2.2, 2.3

---

### Task 3.2: Cleanup legacy prompts and update documentation

**Agent:** Curator Claire (content integrity)
**Priority:** Medium
**Effort:** 3 hours

**Scope:**
- Remove `.claude/prompts/` directory from repository
- Verify no prompt content is lost (already covered by skills or migrated)
- Update `.claude/agents/README.md` to reflect simplified agent format
- Update the technical design if any deviations occurred during implementation
- Update `work/reports/claude_code-fit.md` recommendations to mark completed items
- Update work log

**Acceptance Criteria:**
- `.claude/prompts/` removed
- No orphaned references to `.claude/prompts/` in codebase
- Documentation accurate and current

**Dependencies:** Task 3.1

---

## Summary

| Batch | Tasks | Agent(s) | Effort | Theme |
|---|---|---|---|---|
| **1** | 1.1, 1.2, 1.3 | Backend Benny | 8h | Generator core (simplify, rules, CLAUDE.md) |
| **2** | 2.1, 2.2, 2.3 | DevOps Danny, Code Reviewer Cindy | 5h | Pipeline integration + integration tests |
| **3** | 3.1, 3.2 | Analyst Annie, Curator Claire | 5h | Validation + cleanup |

**Total:** 18 hours across 6 tasks, 4 specialist agents

### Agent Assignment Rationale

| Agent | Why | Tasks |
|---|---|---|
| **Backend Benny** | Owns the existing exporter pipeline; Node.js specialist; understands parser.js IR format | 1.1, 1.2, 1.3 |
| **DevOps Danny** | Owns deploy-skills.js; pipeline integration specialist; understands npm script wiring | 2.1, 2.2 |
| **Code Reviewer Cindy** | Test quality specialist; writes integration tests that validate deployment correctness | 2.3 |
| **Analyst Annie** | Validation specialist; wrote original SPEC-DIST-001; can verify acceptance criteria | 3.1 |
| **Curator Claire** | Content integrity specialist; owns cleanup and documentation consistency | 3.2 |

### Parallelization

- **Batch 1:** Tasks 1.1, 1.2, 1.3 can run in parallel (no dependencies between them). All three are independent generator functions.
- **Batch 2:** Task 2.1 must complete first. Tasks 2.2 and 2.3 can run in parallel after 2.1.
- **Batch 3:** Task 3.1 must complete first. Task 3.2 runs after 3.1.

### Dependency Graph

```
Batch 1 (parallel):
  Task 1.1 (simplifyAgent) ──┐
  Task 1.2 (generateRules) ──┼──► Task 2.1 (deploy integration)
  Task 1.3 (generateClaudeMd)┘         │
                                        ├──► Task 2.2 (package.json) ──┐
                                        └──► Task 2.3 (integration tests)┼──► Task 3.1 (validation)
                                                                         │         │
                                                                         │         └──► Task 3.2 (cleanup)
                                                                         └─────────────────┘
```
