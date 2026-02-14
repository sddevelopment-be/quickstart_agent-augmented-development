# Initiative: Lightweight Reference-Based Distribution Directories

**Date:** 2026-02-14
**Status:** Planned
**Branch:** feature/design_update
**Predecessor:** Model router migration to doctrine templates (committed ab8c7f9)

## Context

The current distribution pipeline (`npm run deploy:*`) generates full or simplified copies of doctrine content into `.claude/`, `.github/agents/`, `.opencode/`. This creates:

- **Drift risk** between source (`doctrine/`) and generated copies
- **Bloat** (~1.9 MB of generated content across targets)
- **Complex export pipeline** (multiple generators, parsers, validators)
- **Maintenance burden** — every doctrine change requires re-export

The distribution feature is undergoing rework. This is an opportunity to replace generated copies with lightweight reference files that preserve discoverability while eliminating duplication.

## Current State Analysis

| Directory | Size | Content Type | Issue |
|-----------|------|-------------|-------|
| `.claude/agents/` | ~12 KB | 23 simplified agent copies | Drift from doctrine source |
| `.claude/skills/` | ~80 KB | 30+ SKILL.md files | Tool-native format, works well |
| `.claude/rules/` | ~15 KB | 5 project rules | Auto-loaded, works well |
| `.claude/prompts/` | ~20 KB | 8 prompt templates | Could reference doctrine |
| `.github/agents/` | ~1.4 MB | Full doctrine copies | Largest duplication source |
| `.github/instructions/` | ~20 KB | Generated Copilot skills | Copilot-specific format |
| `.opencode/` | ~142 KB | JSON manifests | Already uses back-references |
| `.cursor/` | ~12 KB | Reference index | Already lightweight |

## Design Decisions

### What to keep as-is
- `.claude/rules/` — Auto-loaded by Claude Code, small, stable
- `.claude/skills/` — Tool-native SKILL.md format required for slash commands
- `.cursor/QUICK_REFERENCE.md` — Already a lightweight reference index

### What to replace with references
- `.claude/agents/` — Stub files pointing to `doctrine/agents/`
- `.claude/prompts/` — Stub files pointing to doctrine source
- `.github/agents/` — Single reference document instead of 1.4 MB of copies
- `.github/instructions/` — Reference-based skill files
- `.opencode/` — Minimal manifest with doctrine paths

## Implementation Plan

### Phase 1: `.claude/agents/` stub migration

**Goal:** Replace 23 simplified agent copies with stub files that preserve discoverability.

**Tasks:**
1. Design stub format (name, role, doctrine path, model hint)
2. Create stub files for all 23 agents in `.claude/agents/`
3. Update `manifest.json` to reflect stub format
4. Verify Claude Code agent discovery still works with stubs
5. Remove simplified agent generator from `claude-code-generator.js`

**Stub format (proposed):**
```markdown
---
name: architect-alphonso
role: architecture
model: opus
source: doctrine/agents/architect.agent.md
---
# Architect Alphonso

Load full profile from `doctrine/agents/architect.agent.md`.

Focus: Architecture decisions, ADRs, system design, trade-off analysis.
Tools: Read, Write, Grep, Edit, Bash, MultiEdit
```

### Phase 2: `.claude/prompts/` stub migration

**Goal:** Replace prompt template copies with references.

**Tasks:**
1. Create stub format for prompts referencing doctrine source
2. Replace prompt files with stubs
3. Update prompt manifest

### Phase 3: `.github/agents/` deduplication

**Goal:** Eliminate 1.4 MB of full doctrine copies.

**Tasks:**
1. Determine Copilot's file-reference capabilities (can it follow includes?)
2. If yes: replace with `copilot-instructions.md` that references doctrine stack
3. If no: create a consolidated single-file summary instead of per-file copies
4. Update `deploy:copilot` script accordingly
5. Remove full-copy generator from `copilot-generator.js`

**Risk:** Copilot may need inline content rather than references. Test before committing.

### Phase 4: `.github/instructions/` simplification

**Tasks:**
1. Make instruction files reference doctrine approaches instead of inlining
2. Keep Copilot-specific format (capabilities, inputs/outputs sections)
3. Update generator

### Phase 5: `.opencode/` minimal manifest

**Tasks:**
1. Reduce JSON files to essential discovery metadata
2. Ensure `profile_url` references point to `doctrine/` paths
3. Update `opencode-exporter.js`

### Phase 6: Export pipeline cleanup

**Tasks:**
1. Simplify `claude-code-generator.js` — remove `simplifyAgent`, generate stubs
2. Simplify `copilot-generator.js` — remove full-copy logic
3. Simplify `opencode-generator.js` — minimal manifest only
4. Update `deploy-skills.js` to match new generation strategy
5. Update `npm run build` pipeline
6. Remove dead code from parsers/validators

### Phase 7: Validation

**Tasks:**
1. Verify `.claude/` slash commands still work (skills preserved)
2. Verify agent discoverability in Claude Code
3. Verify Copilot instructions work with references
4. Verify OpenCode discovery with minimal manifest
5. Run full test suite
6. Measure size reduction

## Constraints

- **Commands/shorthands must remain available** — `.claude/skills/` stays intact
- **Agent profiles must be discoverable** — stubs preserve name, role, path
- **Directory structure preserved** — same layout, lighter content
- **No breaking changes to consuming repos** — stub format must be forward-compatible

## Success Criteria

- Distribution directories reduced from ~1.9 MB to < 200 KB
- All slash commands still functional
- Agent profiles discoverable by all supported tools
- Single source of truth in `doctrine/` with no content duplication
- Simplified export pipeline (fewer generators, less code)

## Dependencies

- Model router migration (done, ab8c7f9)
- Understanding of each tool's file-reference capabilities (Phase 3 risk)

## Estimated Effort

- Phase 1-2: Small (stub generation, straightforward)
- Phase 3-4: Medium (requires Copilot capability testing)
- Phase 5: Small (OpenCode already partially reference-based)
- Phase 6: Medium (pipeline refactoring)
- Phase 7: Small (validation)
