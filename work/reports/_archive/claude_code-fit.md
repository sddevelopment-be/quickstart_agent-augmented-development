# Claude Code Fit Analysis

**Date:** 2026-02-10
**Scope:** Evaluate `config/`, `.claude/`, and `doctrine/` for Claude Code compatibility
**Status:** Analysis complete — recommendations 1-3, 5 implemented via SPEC-DIST-002

---

## 1. Config Directory — Model Accuracy

The `config/models.yaml` is significantly outdated. All downstream files (`agents.yaml`, `policies.yaml`, `tools.yaml`) inherit the same stale model IDs.

### Anthropic Models

| Listed (Stale)            | Current Model          | Current ID                     |
|---------------------------|------------------------|--------------------------------|
| `claude-opus-20240229`    | Claude Opus 4.6        | `claude-opus-4-6`             |
| `claude-sonnet-20240229`  | Claude Sonnet 4.5      | `claude-sonnet-4-5-20250929`  |
| `claude-haiku-20240307`   | Claude Haiku 4.5       | `claude-haiku-4-5-20251001`   |

### OpenAI Models

| Listed (Stale)      | Status                                                        |
|---------------------|---------------------------------------------------------------|
| `code-davinci-002`  | Retired (Codex shut down March 2023)                          |
| `gpt-4` (8k)       | Superseded by `gpt-4o`, `gpt-4.1`                            |
| `gpt-3.5-turbo`    | Superseded by `gpt-4o-mini`                                  |

### Tools Configuration

`tools.yaml` lists Codex as a standalone CLI binary. OpenAI relaunched "Codex" in 2025 as a cloud-based coding agent, not a local binary. The command template and platform paths are invalid.

---

## 2. .claude Directory vs. Claude Code Best Practices

### Native Recognition Matrix

| Directory                 | Native? | Present? | Status                         |
|---------------------------|---------|----------|--------------------------------|
| `skills/<name>/SKILL.md`  | Yes     | Yes (26) | Used correctly                 |
| `agents/<name>.md`        | Yes     | Yes (21) | **Simplified** (SPEC-DIST-002) |
| `CLAUDE.md`               | Yes     | Yes      | **Created** (SPEC-DIST-002)    |
| `rules/*.md`              | Yes     | Yes (5)  | **Created** (SPEC-DIST-002)    |
| `settings.local.json`     | Yes     | Yes      | Correct                        |
| `prompts/`                | **No**  | Legacy   | **Deprecated** (SPEC-DIST-002) |

### Key Findings

**No `CLAUDE.md`.** This is the most impactful file Claude Code consumes. It is auto-loaded at the start of every session and provides persistent project-level instructions. The `AGENTS.md` file attempts to serve this purpose but is not auto-loaded by Claude Code.

**Agent files are overbuilt.** The `.claude/agents/` files contain doctrine-specific ceremony (bootstrap declarations, directive reference tables, mode protocols, initialization declarations) that Claude Code does not process. Claude Code subagents receive the file content as a system prompt. The current format (~100+ lines each) wastes tokens on structure Claude Code ignores. Subagents need: a name, description, tools list, and behavioral instructions.

**Prompts directory is invisible.** Claude Code does not scan `.claude/prompts/`. These prompts only work if something explicitly reads them. The content either already exists in skills (which are recognized) or should be migrated there.

**Skills reference stale paths.** Several skills reference `.github/agents/directives/...` (the old path structure), not `doctrine/directives/...`.

---

## 3. Transformation Recommendations

### 3.1 Create a `CLAUDE.md`

This is the single most impactful change. It should be concise (under ~100 lines) because Claude loads it every session. Bloat causes instructions to be ignored.

**Should contain:**
- Project purpose (2-3 lines from `docs/VISION.md`)
- Repository structure summary (key directories only)
- Coding conventions (Python style, test approach)
- Common commands (`python -m pytest`, etc.)
- Pointers to where deeper context lives

**Should not contain:**
- Full doctrine stack content
- File-by-file descriptions
- Long tutorials or process documentation

### 3.2 Use `.claude/rules/` for Doctrine Layers

Rules files are auto-loaded by Claude Code. They act as persistent, modular project instructions. This is the natural home for frequently-needed guidelines, approaches, and directives.

```
.claude/rules/
  guidelines.md          <- Distilled from doctrine/guidelines/general_guidelines.md
  coding-conventions.md  <- From doctrine/guidelines/python-conventions.md + operational_guidelines.md
  testing.md             <- Distilled from directives 016 (ATDD) + 017 (TDD)
  architecture.md        <- Key ADR patterns, from directive 018
  collaboration.md       <- File-based orchestration summary, from directive 019
```

### 3.3 Simplify Agent Files

Strip down to what Claude Code subagents actually consume:

```markdown
---
name: backend-benny
description: Backend development specialist for Python services, APIs, and data persistence.
tools: [Read, Write, Edit, Bash, Grep, Glob]
model: sonnet
---

You are a backend development specialist. Focus on:
- Clean service boundaries and API design
- Test-first development (write failing test, then implement)
- Python conventions: type hints, dataclasses, pytest
- Minimal changes — avoid speculative refactoring

When fixing bugs, always reproduce with a failing test first.
```

**Remove from agent files:**
- Bootstrap declarations and initialization ceremony
- Directive reference tables (move relevant content to rules/)
- Mode protocol tables (/analysis-mode, /creative-mode, /meta-mode)
- Context source listings
- Collaboration contract boilerplate
- Spec-driven development phase authority tables

### 3.4 Trim Skills

Skills are well-structured but should:
- Update path references from `.github/agents/` to `doctrine/`
- Remove doctrine-specific ceremony ("Initialize as Architect Alphonso")
- Focus on what to do, not who to be

### 3.5 Drop `.claude/prompts/`

Not natively recognized. Content should be migrated to skills or removed if already duplicated there.

---

## 4. Doctrine-to-Claude-Code Mapping

### Loading Model

Claude Code has two loading modes:

- **Always-on:** `CLAUDE.md`, `.claude/rules/` — loaded every session automatically
- **On-demand:** `.claude/skills/`, `.claude/agents/` — loaded when invoked

The doctrine stack should split accordingly: values and conventions go in always-on files, procedures and specialized behaviors go in on-demand files.

### Layer Mapping

| Doctrine Layer             | Claude Code Target                          | Rationale                                              |
|----------------------------|---------------------------------------------|--------------------------------------------------------|
| Guidelines (values)        | `CLAUDE.md` + `.claude/rules/`              | Auto-loaded every session                              |
| Approaches (models)        | `.claude/rules/` or `.claude/skills/`       | Rules for persistent context, skills for invocable workflows |
| Directives (instructions)  | `.claude/rules/` (frequent) or skill instructions (on-demand) | Rules auto-load; skills load on invocation |
| Tactics (procedures)       | `.claude/skills/<name>/SKILL.md`            | Skills are the exact equivalent — invocable procedural guides |
| Templates (structure)      | Supporting files inside skill directories   | Skills can include templates, examples, scripts        |
| Agent profiles             | `.claude/agents/<name>.md` (simplified)     | Lean subagent definitions, not full doctrine profiles  |

### Priority Order for Implementation

1. ~~Create `CLAUDE.md`~~ — **DONE** (SPEC-DIST-002, 43 lines)
2. ~~Create `.claude/rules/` with distilled doctrine content~~ — **DONE** (5 rules files, 75-79 lines each)
3. ~~Simplify `.claude/agents/` files~~ — **DONE** (21 agents, ~14 lines each)
4. Fix stale paths in skills — low effort, prevents confusion
5. ~~Remove `.claude/prompts/` from default deploy~~ — **DONE** (deprecated behind --prompts-legacy)
6. Update `config/models.yaml` and downstream files — correctness, moderate effort
