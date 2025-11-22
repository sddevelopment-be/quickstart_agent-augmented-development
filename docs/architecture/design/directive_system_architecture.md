# Directive System Architecture

**Version:** 1.0.0  
**Last Updated:** 2025-11-17  
**Type:** Technical Architecture Document

---

## Purpose

This document describes the **technical architecture of the modular directive system
** used to govern agent behavior in this repository. It covers structure, loading mechanisms, validation, dependencies, and future evolution paths.

## System Overview

The directive system is a **modular governance framework** that allows:

- Selective loading of operational guidance based on agent role and task
- Version-controlled, human-readable governance content
- Automated validation of structural integrity
- Dependency tracking between related directives
- Safety-critical content flagging

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Core Specification                      │
│                        (AGENTS.md)                          │
│  - Initialization protocol                                   │
│  - Runtime behavior defaults                                 │
│  - Extended Directives Index                                │
│  - Safety & escalation protocol                             │
└──────────────────────┬──────────────────────────────────────┘
                       │ references
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Directive Suite (directives/)                   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ 001: Tooling │  │ 002: Context │  │ 003: Repo    │     │
│  │              │  │   Notes      │  │   Reference  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ 004: Docs    │  │ 005: Agent   │  │ 006: Version │     │
│  │   Context    │  │   Profiles   │  │   Governance │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ 007: Agent   │  │ 008: Artifact│  │ 009: Role    │     │
│  │   Declaration│  │   Templates  │  │   Capabilities│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ 010: Mode    │  │ 011: Risk &  │  │ 012: Common  │     │
│  │   Protocol   │  │   Escalation │  │   Operating  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
└──────────────────────┬──────────────────────────────────────┘
                       │ described by
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Manifest (manifest.json)                    │
│  - Directive metadata (code, slug, title, purpose)          │
│  - Dependency graph                                          │
│  - Safety flags (requiredInAgents, safetyCritical)          │
│  - File references                                           │
└──────────────────────┬──────────────────────────────────────┘
                       │ consumed by
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           Agent Profiles (*.agent.md)                        │
│  - Role specialization                                       │
│  - Directive reference table                                │
│  - Collaboration contracts                                   │
│  - Mode defaults                                            │
└──────────────────────┬──────────────────────────────────────┘
                       │ loaded by
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         Loading & Validation Tooling                         │
│  - load_directives.sh (context assembly)                    │
│  - validate_directives.sh (integrity checks)                │
└─────────────────────────────────────────────────────────────┘
```

## Directive File Structure

Each directive file follows a standardized format:

```markdown
# <code> <title>

> **Purpose:** <one-line description>

## 1. <Section Name>

<content>

## 2. <Section Name>

<content>
```

### Required Elements

1. **Heading:** Must start with `# <code> ` (e.g., `# 001 CLI & Shell Tooling`)
2. **Purpose:** Blockquote with directive purpose (matches manifest)
3. **Numbered Sections:** Clear hierarchical structure
4. **Content:** Operational guidance specific to directive's concern

### Naming Convention

- **Pattern:** `<code>_<slug>.md`
- **Code:** Zero-padded 3-digit number (001, 002, ..., 012)
- **Slug:** Lowercase with underscores (e.g., `cli_shell_tooling`)

## Manifest Schema

The `manifest.json` file provides machine-readable metadata about the directive suite.

### Structure

```json
{
  "version": "1.0.0",
  "generated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "description": "Manifest of externalized agent directives",
  "directives": [
	{
	  "code": "001",
	  "slug": "cli_shell_tooling",
	  "title": "CLI & Shell Tooling",
	  "file": "001_cli_shell_tooling.md",
	  "purpose": "Detailed tool usage rubric (fd/rg/ast-grep/jq/yq/fzf)",
	  "dependencies": [],
	  "requiredInAgents": false,
	  "safetyCritical": true
	}
  ]
}
```

### Field Definitions

| Field              | Type    | Description                                      |
|--------------------|---------|--------------------------------------------------|
| `code`             | string  | Zero-padded 3-digit identifier (e.g., "001")     |
| `slug`             | string  | URL-friendly identifier (lowercase, underscores) |
| `title`            | string  | Human-readable name                              |
| `file`             | string  | Relative path to directive markdown file         |
| `purpose`          | string  | One-line description of directive's function     |
| `dependencies`     | array   | List of prerequisite directive codes             |
| `requiredInAgents` | boolean | Must all agents load this directive?             |
| `safetyCritical`   | boolean | Contains critical behavioral/safety guidance?    |

### Future Fields (Planned)

As documented in Curator Claire's assessment:

```json
{
  "directive_version": "1.0.0",
  "checksum_sha256": "<hash>",
  "status": "active",
  "replaces": null
}
```

## Dependency Graph

Directives can depend on other directives to ensure proper context ordering.

### Current Dependencies

```
001: CLI & Shell Tooling
  └─ (no dependencies)

002: Context Notes
  └─ (no dependencies)

003: Repository Quick Reference
  └─ depends on: 002

004: Documentation & Context Files
  └─ depends on: 003

005: Agent Profiles
  └─ (no dependencies)

006: Version Governance
  └─ (no dependencies)

007: Agent Declaration
  └─ depends on: 006

008: Artifact Templates
  └─ depends on: 004

009: Role Capabilities
  └─ depends on: 005, 002

010: Mode Protocol
  └─ depends on: 006

011: Risk & Escalation
  └─ depends on: 010, 006

012: Common Operating Procedures
  └─ depends on: 010, 011
```

### Dependency Resolution

**Current State:** Manual loading in agent profiles or via explicit `/require-directive` commands.

**Planned Enhancement (Phase 1):** Automatic dependency resolution via loader script with `--with-deps` flag.

## Loading Mechanisms

### Manual Loading (Current)

Agents explicitly load directives in their profile's "Directive References" section:

```markdown
| Code | Directive | Usage Rationale |
|------|-----------|-----------------|
| 001  | CLI & Shell Tooling | Repo/file discovery |
| 003  | Repository Quick Reference | Fast topology recall |
| 006  | Version Governance | Validate architecture decisions |
```

### Explicit Load Command

Within an agent session, directives can be loaded on-demand:

```
/require-directive 001
/require-directive 006
```

### Script-Based Loading

The `load_directives.sh` script concatenates specified directives:

```bash
#!/usr/bin/env bash
# Usage: load_directives.sh 001 003 006

for code in "$@"; do
  cat ".github/agents/directives/${code}_*.md"
  echo ""
done
```

**Current Limitations:**

- No dependency resolution
- No deduplication
- No load summary or version reporting

**Planned Enhancements (Phase 1):**

- `--with-deps` flag for automatic dependency inclusion
- Visited set for deduplication
- Summary header with loaded codes, versions, checksums

## Validation Architecture

### Validation Script (`validation/validate_directives.sh`)

The validation script performs structural integrity checks on the directive suite.

#### Current Checks

1. **Sequencing:**
    - All directives sequentially numbered (001, 002, ..., 012)
    - No gaps in sequence
    - Correct zero-padding

2. **Heading Conformity:**
    - Each file starts with `# <code> `
    - Title matches manifest entry

3. **Dependency File Existence:**
    - All dependency codes reference existing files
    - Dependency graph is acyclic (manual verification)

4. **Index Presence:**
    - Core `AGENTS.md` contains Extended Directives Index
    - Index entries match manifest

5. **Required Behavioral Lines:**
    - Safety-critical phrases present where expected
    - Clarifying question threshold documented

#### Planned Enhancements (Phase 2)

6. **Purpose Section Check:**
    - Directive contains `> **Purpose:**` blockquote
    - Purpose matches manifest

7. **Orphan Detection:**
    - Directive is referenced by at least one agent profile or index
    - No unreferenced directive files

8. **Index Order Verification:**
    - Extended Directives Index table rows in ascending numerical order

9. **JSON Validation Report:**
    - Output validation results in machine-readable format
    - Enable CI integration

### Validation Workflow

```
Developer modifies directive
        ↓
Run validate_directives.sh
        ↓
   ┌────────────┐
   │ All checks │ YES → Commit changes
   │   pass?    │
   └────────────┘
        │ NO
        ↓
Review error report
        ↓
Fix structural issues
        ↓
Re-run validation
```

## Safety Mechanisms

### Critical Directive Flags

Directives flagged `safetyCritical: true` in manifest contain behavioral guardrails essential for system integrity.

**Current Safety-Critical Directives:**

- 001: CLI & Shell Tooling (prevents destructive operations)
- 002: Context Notes (prevents misinterpretation)
- 003: Repository Quick Reference (prevents wrong directory operations)
- 004: Documentation & Context Files (prevents unauthorized doc changes)
- 006: Version Governance (ensures version discipline)
- 007: Agent Declaration (ensures authority confirmation)
- 009: Role Capabilities (prevents boundary violations)
- 010: Mode Protocol (prevents mode misuse)
- 011: Risk & Escalation (ensures proper escalation)
- 012: Common Operating Procedures (centralized safety norms)

### Required Directive Loading

Directives flagged `requiredInAgents: true` must be loaded by all agents regardless of specialization.

**Current Required Directives:**

- 006: Version Governance
- 007: Agent Declaration
- 012: Common Operating Procedures

### Integrity Markers

All directives instruct agents to use integrity markers in outputs:

- ✅ **Alignment confirmed** — Operation successful within guidelines
- ⚠️ **Low confidence** — Assumption-based, needs validation
- ❗️ **Critical issue** — Misalignment detected, escalation required

## Evolution and Extensibility

### Adding New Directives

**Process:**

1. Assign next sequential code (e.g., 013)
2. Create `<code>_<slug>.md` in `.github/agents/directives/`
3. Follow standard structure (heading, purpose, numbered sections)
4. Add entry to `manifest.json` with metadata and dependencies
5. Update Extended Directives Index in `AGENTS.md`
6. Run `validate_directives.sh` to verify conformity
7. Update relevant agent profiles to reference new directive

**Example: Adding Directive 013 (Tooling Setup)**

1. Create `013_tooling_setup.md`
2. Add manifest entry:

```json
{
  "code": "013",
  "slug": "tooling_setup",
  "title": "Tooling Setup & Fallbacks",
  "file": "013_tooling_setup.md",
  "purpose": "Install commands, version pins, fallback strategies",
  "dependencies": [
	"001"
  ],
  "requiredInAgents": false,
  "safetyCritical": false
}
```

3. Update `AGENTS.md` Extended Directives Index table
4. Validate and commit

### Deprecating Directives

**Planned Status Field Values:**

- `active`: Current, stable directive in use
- `deprecated`: Superseded, maintained for backward compatibility
- `pending`: Draft directive under review

**Deprecation Process (Future):**

1. Update manifest: set `status: "deprecated"`, populate `replaces` field
2. Mark directive file with deprecation notice
3. Update agent profiles to use replacement directive
4. After grace period (2-3 releases), archive deprecated directive

### Version Evolution

**Current Versioning:**

- Manifest has single `version` field (e.g., "1.0.0")
- Directives implicitly share this version

**Planned Per-Directive Versioning (Phase 1):**

- Each directive has `directive_version` field
- Core `AGENTS.md` has `core_version` field
- Composite meta-version tracks synchronized state

**Version Update Rules:**

- **Patch (X.Y.Z+1):** Typo fixes, clarifications, non-semantic changes
- **Minor (X.Y+1.0):** New sections, additional guidance, backward-compatible
- **Major (X+1.0.0):** Structural changes, removed sections, breaking changes

## Integration with Other Systems

### OpenCode Configuration

The repository includes OpenCode mapping for agent profiles:

- `docs/opencode_config.json`: Agent profile metadata
- `ops/scripts/convert-agents-to-opencode.py`: Conversion utility
- `ops/scripts/opencode-spec-validator.py`: Validation utility

**Integration Point:** Directives remain markdown-first; OpenCode configuration maps to agent profiles for toolchain compatibility.

### CI/CD Integration

**Current State:** Manual validation via `validate_directives.sh`

**Planned Enhancement (Phase 2):**

- GitHub Actions workflow on directive changes
- JSON validation output for automated checks
- Fail build on structural violations
- Automated manifest regeneration

### Template System

Directives reference templates from `docs/templates/`:

- Architecture templates (ADR, design vision, roadmap, technical design)
- Structure templates (repo map, surfaces, workflows)
- LEX templates (style rules, deltas, reports)

**Integration Point:** Directive 008 (Artifact Templates) documents template locations and usage rules.

## Performance Characteristics

### Token Efficiency

**Baseline (Monolithic):**

- Single large specification: ~15KB
- Every agent loads all content
- Redundant loading of irrelevant guidance

**Optimized (Modular):**

- Core specification: ~3KB
- Average directive: ~1-2KB
- Typical agent profile: 3-5 directives
- **Total context: ~5-13KB (40-60% reduction)**

### Initialization Time

- Core specification parsing: <100ms
- Directive loading (5 directives): <500ms
- Validation (full suite): <1s

### Validation Performance

- Structural checks (12 directives): ~500ms
- Semantic checks (planned): ~1s
- JSON report generation (planned): ~200ms

## Future Architectural Enhancements

### Phase 1: Integrity (Critical)

1. **Per-Directive Versioning**
    - Add `directive_version` to manifest
    - Update loader to report loaded versions
    - Add version mismatch detection

2. **Checksum Verification**
    - Add `checksum_sha256` to manifest
    - Compute hash on load, compare to manifest
    - Flag tampering with ❗️

3. **Dependency Resolution**
    - Enhance `load_directives.sh` with `--with-deps`
    - Auto-include dependencies from manifest
    - Deduplicate loaded directives

### Phase 2: Validation (High)

4. **Semantic Validation**
    - Verify Purpose section existence
    - Check directive is referenced (no orphans)
    - Validate index ordering

5. **CI Integration**
    - JSON validation output format
    - GitHub Actions workflow
    - Automated feedback on PRs

### Phase 3: Governance (Medium)

6. **Recovery Protocols**
    - Directive 014: Integrity & Recovery
    - Fallback mechanisms for missing directives
    - Rehydration checksums

7. **Meta-Versioning**
    - Composite version (core + directive set)
    - Synchronized state tracking
    - Update rules and compatibility matrix

### Phase 4: Developer Experience (Low)

8. **Automated Tooling**
    - Manifest regeneration script
    - Checksum computation automation
    - Index synchronization tool

9. **Linting and Formatting**
    - Prose linter (trailing whitespace, line length)
    - Dash/punctuation normalization
    - Consistent heading capitalization

## Related Documentation

- ADR-001 Modular Directive System: [`ADR-001-modular-agent-directive-system.md`](../adrs/ADR-001-modular-agent-directive-system.md)
- Architectural Vision: [`architectural_vision.md`](../architectural_vision.md)
- Agent Specialization Patterns: [`agent_specialization_patterns.md`](../agent_specialization_patterns.md)
- Core Specification: [`AGENTS.md`](/AGENTS.md)
- Directive Manifest: [`.github/agents/directives/manifest.json`](/.github/agents/directives/manifest.json)
- Validation Script: [`validation/validate_directives.sh`](/validation/validate_directives.sh)
- Loader Script: [`.github/agents/load_directives.sh`](/.github/agents/load_directives.sh)

---

_Prepared by: Architect Alphonso_  
_Mode: `/analysis-mode`_  
_Version: 1.0.0_
