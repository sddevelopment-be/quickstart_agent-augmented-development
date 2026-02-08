---
id: SPEC-DIST-001
title: Doctrine Framework Multi-Tool Distribution Architecture
status: ready-for-implementation
version: 1.0.0
author: Analyst Annie
created: 2026-02-08
updated: 2026-02-08
stakeholders: [stijn, devops-danny, bootstrap-bill]
priority: high
type: architecture
tags: [distribution, doctrine, cross-tool, exporters, symlinks]
decision: solution-b-exporters-with-symlinks
---

# Doctrine Framework Multi-Tool Distribution Architecture

## Executive Summary

Define how the standalone `doctrine/` framework (single source of truth, zero dependencies) distributes to multiple AI development tools while maintaining consistency, minimizing maintenance burden, and enabling validation.

**Current State:** `doctrine/` extracted from `.github/agents/`, needs cross-tool distribution.

**Required Tools:**
- GitHub Copilot (`.github/instructions/`)
- Claude Desktop (`.claude/`)
- Cursor (`.cursor/`)
- Windsurf (`.windsurf/`)
- OpenCode (`.opencode/`)

---

## Problem Statement

### Context

The SDD Agentic Framework has been extracted from `.github/agents/` into a standalone `doctrine/` directory with:
- 201 framework files (agents, directives, approaches, guidelines, tactics, templates)
- Zero external dependencies
- Path parameterization for portability
- Ready for git subtree distribution

### Challenge

Different AI development tools expect framework content in tool-specific locations:

| Tool | Expected Location | Discovery Mechanism |
|------|------------------|---------------------|
| GitHub Copilot | `.github/instructions/*.md` | Automatic discovery |
| Claude Desktop | `.claude/skills/*/SKILL.md` | Manual or auto-import |
| Cursor | `.cursor/docs/` | Settings configuration |
| Windsurf | `.windsurf/rules/` | CASCADE.md references |
| OpenCode | `.opencode/agents/*.json` | Manifest-based |

**Problem:** How do we distribute `doctrine/` → tool-specific locations while:
1. Maintaining `doctrine/` as single source of truth
2. Minimizing manual maintenance overhead
3. Enabling validation (exporters vs symlinks working correctly)
4. Supporting multiple consumption patterns (local dev, CI/CD, git subtree)

---

## Requirements

### Functional Requirements

**FR-1: Single Source of Truth**
- `doctrine/` MUST be the canonical location for all framework content
- Changes to framework content MUST only occur in `doctrine/`
- Tool-specific locations MUST reflect `doctrine/` content accurately

**FR-2: Cross-Tool Compatibility**
- MUST support GitHub Copilot discovery via `.github/`
- MUST support Claude Desktop discovery via `.claude/`
- SHOULD support Cursor discovery via `.cursor/`
- SHOULD support Windsurf discovery via `.windsurf/`
- MUST support OpenCode standard via `.opencode/`

**FR-3: Distribution Mechanism**
- MUST provide mechanism to distribute `doctrine/` → tool locations
- MUST support both local development and CI/CD execution
- MUST preserve file structure and metadata
- SHOULD minimize latency between source update and tool availability

**FR-4: Validation**
- MUST provide validation that tool locations match `doctrine/`
- MUST detect stale or missing distributed content
- SHOULD provide automated validation in CI/CD

### Non-Functional Requirements

**NFR-1: Maintenance Burden**
- Distribution mechanism SHOULD require minimal manual intervention
- Distribution mechanism SHOULD NOT require developer expertise to maintain
- Distribution failures SHOULD provide clear diagnostic information

**NFR-2: Performance**
- Distribution MUST complete in <30 seconds for full framework
- Distribution SHOULD support incremental updates (changed files only)
- Tool discovery latency SHOULD be <1 second

**NFR-3: Portability**
- Distribution mechanism MUST work on Linux, macOS, Windows
- Distribution mechanism MUST work in CI/CD environments
- Distribution mechanism SHOULD NOT require administrative privileges

**NFR-4: Reversibility**
- Distribution mechanism SHOULD be easy to replace if requirements change
- Distribution mechanism SHOULD NOT modify `doctrine/` source files
- Distribution mechanism failures SHOULD NOT corrupt tool-specific locations

---

## Constraints

**C-1: Existing Infrastructure**
- Exporters already exist: `tools/exporters/opencode-exporter.js`, `tools/scripts/deploy-skills.js`
- Exporters currently read from `.github/agents/` (not `doctrine/`)
- Package.json scripts reference existing exporters

**C-2: Tool Discovery Limitations**
- GitHub Copilot: Only discovers `.github/instructions/` and `.github/copilot-instructions.md`
- Claude Desktop: Requires specific `SKILL.md` format in `.claude/skills/<name>/`
- OpenCode: Requires JSON format with specific schema

**C-3: Repository State**
- Branch `refactor/generic_core_files` ready to merge (32 commits)
- Symlinks already created in `.github/` pointing to `doctrine/` (uncommitted)
- No tool-specific distributions currently exist

---

## Proposed Solutions

### Solution A: Symlink Tactical Approach

**Description:** Create symlinks in tool-specific locations pointing to `doctrine/` directories.

**Implementation:**
```bash
# GitHub Copilot
.github/agents -> ../doctrine/agents/
.github/directives -> ../doctrine/directives/
.github/approaches -> ../doctrine/approaches/

# Claude Desktop
.claude/framework -> ../doctrine/

# Cursor
.cursor/framework -> ../doctrine/

# Windsurf
.windsurf/framework -> ../doctrine/
```

**Advantages:**
- ✅ Zero maintenance (automatic synchronization)
- ✅ Zero latency (changes immediately visible)
- ✅ Simple implementation (<5 minutes)
- ✅ Reversible (easy to change strategy)
- ✅ Validation phase (test `doctrine/` usage before committing to architecture)

**Disadvantages:**
- ⚠️ Windows requires Developer Mode for symlinks (non-admin)
- ⚠️ Cannot transform formats (e.g., JSON for OpenCode)
- ⚠️ Cannot optimize for tool-specific token limits
- ⚠️ Symlinks break in zip archives (distribution concern)

**Validation:**
```bash
# Test symlink resolution
ls -la .github/agents/*.agent.md  # Should list doctrine/agents/ contents
test -L .github/agents && echo "Symlink exists"

# Test exporter compatibility
npm run export:agents  # Should read via symlink
```

---

### Solution B: Exporter Strategic Approach

**Description:** Update existing exporters to read from `doctrine/` and generate tool-specific formats.

**Implementation:**
```javascript
// Update AGENTS_DIR in tools/exporters/opencode-exporter.js
const AGENTS_DIR = path.join(__dirname, '..', 'doctrine', 'agents');

// Run exporters
npm run export:agents  // → dist/opencode/
npm run deploy:all     // → .github/, .claude/, .opencode/
```

**Advantages:**
- ✅ Cross-platform (works on Windows without special permissions)
- ✅ Format transformation (JSON, YAML, optimized markdown)
- ✅ Token optimization (flatten for context limits)
- ✅ Selective distribution (filter by tool capabilities)

**Disadvantages:**
- ⚠️ Requires running exporters after doctrine changes
- ⚠️ Maintenance overhead (keep exporters synchronized with doctrine evolution)
- ⚠️ Latency (must run npm scripts to update)
- ⚠️ Complexity (multiple scripts, potential failure modes)

**Validation:**
```bash
# Export validation
npm run export:all && npm run deploy:all
diff -r doctrine/agents/ .github/agents/  # Should match structure

# CI/CD validation
# Add GitHub Actions workflow to auto-export on doctrine changes
```

---

### Solution C: Hybrid Approach

**Description:** Symlinks for development (local), exporters for distribution (CI/CD, releases).

**Implementation:**
```bash
# Local development: symlinks
.github/agents -> ../doctrine/agents/

# CI/CD: exporters
# .github/workflows/export-doctrine.yml runs npm run export:all
```

**Advantages:**
- ✅ Fast local development (zero latency)
- ✅ Optimized distributions (CI/CD generates tool-specific formats)
- ✅ Best of both worlds

**Disadvantages:**
- ⚠️ Complexity (two mechanisms to maintain)
- ⚠️ Inconsistency risk (local vs CI/CD divergence)
- ⚠️ Testing burden (validate both paths)

---

## Doctrine → Toolstack Mapping Matrix

Based on research from:
- `work/reports/research/2026-02-07-ai-tool-config-directory-analysis.md`
- `work/analysis/ADR-013-multi-format-distribution.md`
- `work/analysis/tech-design-export-pipeline.md`
- Existing exporter implementations in `tools/exporters/`

### Canonical Mapping Table

| Doctrine Source | GitHub Copilot | Claude Desktop | OpenCode | Cursor | Codex | Format Transformation |
|-----------------|----------------|----------------|----------|--------|-------|----------------------|
| **AGENTS.md** | `.github/copilot-instructions.md` (custom instructions) | `.claude/system-prompt.md` | `.opencode/system-prompt.md` | `.cursorrules` (root file) | `.codex/system-prompt.md` | ⚠️ **Optional**: Can inline or reference; core initialization protocol |
| **doctrine/agents/*.agent.md** | `.github/instructions/*.instructions.md` | `.claude/skills/*/SKILL.md` | `.opencode/agents/*.opencode.json` + `*.definition.yaml` | `.cursor/rules/*.md` | `.codex/agents/*.json` | ✅ **Required**: YAML frontmatter → JSON schema (Copilot, OpenCode, Codex), Markdown with YAML (Claude, Cursor) |
| **doctrine/directives/*.md** | Embedded in `instructions` field | Embedded in SKILL.md content | Embedded in definition YAML | Embedded in rules markdown | Embedded in agent JSON | ✅ **Advised**: Extract to structured sections for machine readability |
| **doctrine/approaches/*.md** | Embedded in `instructions` field | Embedded in SKILL.md content | Embedded in definition YAML | Embedded in rules markdown | Embedded in agent JSON | ✅ **Advised**: Extract to structured sections for machine readability |
| **doctrine/guidelines/*.md** | Embedded in `instructions` field or separate files | Separate files in `.claude/guidelines/` | Embedded in definition YAML | Separate files in `.cursor/guidelines/` | Separate files in `.codex/guidelines/` | ⚠️ **Optional**: Can reference or inline |
| **doctrine/tactics/*.md** | Embedded in `instructions` field | Embedded in SKILL.md content | Embedded in definition YAML | Embedded in rules markdown | Embedded in agent JSON | ⚠️ **Optional**: Flatten into parent directives |
| **doctrine/templates/*.md** | Not applicable (no template concept) | `.claude/prompts/*/template.md` | `.opencode/templates/*.yaml` | Not applicable | `.codex/templates/*.json` | ✅ **Required**: YAML extraction + schema generation |
| **doctrine/examples/**  | `.github/instructions/*.examples.md` (inline) | `.claude/skills/*/examples/` | `.opencode/examples/*.json` | `.cursor/examples/*.md` | `.codex/examples/*.json` | ✅ **Required**: Markdown → JSON (OpenCode, Codex), Markdown (others) |

### Tool-Specific Requirements

#### GitHub Copilot
**Discovery Mechanism:** Schema-based validation with `$schema` URL  
**Primary Format:** JSON (`.copilot-skill.json`) or Markdown (`.instructions.md`)  
**Location:** `.github/instructions/` or `.github/copilot/`  
**Transformation:** YAML frontmatter → JSON schema with `extensions` field for governance  
**Current Exporter:** `tools/exporters/copilot-generator.js`  
**Source Read Location:** Currently `.github/agents/` (line 21) — **NEEDS UPDATE to `doctrine/agents/`**

#### Claude Desktop
**Discovery Mechanism:** Manifest-based with directory scanning  
**Primary Format:** Markdown with YAML frontmatter  
**Location:** `.claude/skills/*/SKILL.md`, `.claude/agents/manifest.json`  
**Transformation:** Minimal (markdown-to-markdown with frontmatter normalization)  
**Current Exporter:** `tools/exporters/prompt-template-exporter.js`  
**Source Read Location:** Currently `.github/agents/` — **NEEDS UPDATE to `doctrine/agents/`**

#### OpenCode
**Discovery Mechanism:** Manifest + schema validation  
**Primary Format:** JSON discovery (`.opencode.json`) + YAML definition (`.definition.yaml`)  
**Location:** `.opencode/agents/`, `.opencode/manifest.opencode.json`  
**Transformation:** YAML frontmatter → JSON + YAML with schema extraction  
**Current Exporter:** `tools/exporters/opencode-exporter.js`, `tools/exporters/opencode-generator.js`  
**Source Read Location:** Currently `.github/agents/` (line 21 in opencode-exporter.js) — **NEEDS UPDATE to `doctrine/agents/`**

#### Cursor
**Discovery Mechanism:** Convention-based (file naming patterns)  
**Primary Format:** Markdown (`.cursorrules`) or directory-based rules  
**Location:** `.cursor/rules/`, `.cursorrules` (root)  
**Transformation:** Markdown-to-markdown with Cursor-specific formatting  
**Current Exporter:** **NOT IMPLEMENTED** (planned)  
**Source Read Location:** N/A — **TO BE CREATED reading from `doctrine/agents/`**

#### Codex
**Discovery Mechanism:** JSON-based configuration files  
**Primary Format:** JSON with schema validation  
**Location:** `.codex/agents/*.json`, `.codex/system-prompt.md`  
**Transformation:** YAML frontmatter → JSON with agent definitions, structured prompts  
**Current Exporter:** **NOT IMPLEMENTED** (planned)  
**Source Read Location:** N/A — **TO BE CREATED reading from `doctrine/agents/` and `AGENTS.md`**

### Format Transformation Requirements

#### ✅ CRITICAL TRANSFORMATIONS (Must Implement)

1. **YAML Frontmatter → JSON Schema (GitHub Copilot, OpenCode)**
   - Extract `inputs`, `outputs` from frontmatter
   - Generate JSON Schema Draft 7 structures
   - Add `$schema` reference for validation
   - Preserve governance metadata in `extensions` field

2. **Markdown Narrative → Structured Sections (All Tools)**
   - Parse markdown headings to extract Purpose, Specialization, Collaboration Contract
   - Map to tool-specific fields (e.g., `description`, `instructions`, `behavior`)

3. **Directive References → Embedded Content (All Tools)**
   - Resolve `directives: [001, 018, 020]` references
   - Inline directive content where tools don't support external references
   - Maintain traceability metadata

#### ⚠️ ADVISED TRANSFORMATIONS (Optimize User Experience)

1. **Examples → Tool-Specific Format**
   - GitHub Copilot: Inline in `instructions` field with formatting
   - Claude Desktop: Separate `examples/` directory
   - OpenCode: JSON structured examples with schema
   - Cursor: Inline markdown examples

2. **Tool/Command References → Platform-Specific Syntax**
   - Bash commands: No transformation
   - Tool names: Map to platform equivalents (e.g., `rg` → `ripgrep`)
   - Paths: Use parameterized variables (`${WORKSPACE_ROOT}`)

3. **Governance Metadata → Extension Fields**
   - GitHub Copilot: `extensions.saboteurs_governance`
   - OpenCode: `extensions.sdd_framework`
   - Claude Desktop: Custom frontmatter fields
   - Cursor: YAML frontmatter (no standard extension field)

#### ⚪ OPTIONAL TRANSFORMATIONS (Future Enhancement)

1. **Cross-Agent References → Hyperlinks**
   - Tool-specific navigation links (if supported)
   - Preserve as text references otherwise

2. **Diagrams → Image Embeds**
   - PlantUML/Mermaid → PNG/SVG (if tools support)
   - Keep as code blocks otherwise

3. **Version-Specific Optimizations**
   - Adapt output based on detected tool version
   - Use latest features when available

---

## Decision Criteria (Updated with Stakeholder Input)

| Criterion | Weight | Requirement | Symlinks (A) | Exporters (B) | Hybrid (C) |
|-----------|--------|-------------|-------------|---------------|-----------|
| **Windows Support** | **CRITICAL** | Native, no special permissions | ❌ 2/10 | ✅ 10/10 | ⚠️ 5/10 |
| **Format Transformation** | **CRITICAL** | Required for stack optimization | ❌ 2/10 | ✅ 10/10 | ✅ 10/10 |
| **CI/CD Integration** | **HIGH** | Use existing pipelines | ⚠️ 5/10 | ✅ 10/10 | ✅ 10/10 |
| Maintenance Burden | Medium | Minimize manual work | 10/10 | 6/10 | 7/10 |
| Latency | Low | Acceptable (CI/CD) | 10/10 | 7/10 | 9/10 |
| **Total Score** | | | **29/50** | **43/50** | **41/50** |

**Critical Requirements Analysis:**
- ❌ **Solution A (Symlinks):** FAILS Windows requirement, FAILS format transformation requirement
- ✅ **Solution B (Exporters):** MEETS all critical requirements
- ⚠️ **Solution C (Hybrid):** Partial Windows support, adds complexity

---

## Recommendation

**✅ SOLUTION B: EXPORTER-BASED DISTRIBUTION**

**Analyst Annie Recommendation:** Based on stakeholder input, **Solution B (Exporters)** is the only viable option that meets all critical requirements.

**Critical Directive:** Symlinks are a TEMPORARY CRUTCH and NOT part of the permanent architecture.

### Why Solution B

**Critical Requirements Met:**
1. ✅ **Windows Support:** Exporters work cross-platform without special permissions
2. ✅ **Format Transformation:** Can generate JSON (OpenCode), optimized markdown (Claude), instruction files (Copilot)
3. ✅ **CI/CD Integration:** Leverages existing pipelines (`npm run export:all && npm run deploy:all`)
4. ✅ **Permanent Architecture:** Designed for long-term use, not tactical workaround

**Implementation Strategy:**
```bash
# STEP 1: Update exporters to read from doctrine/ (not .github/agents/)
# - tools/exporters/copilot-generator.js: line 21 AGENTS_DIR
# - tools/exporters/opencode-exporter.js: line 21 AGENTS_DIR
# - tools/exporters/prompt-template-exporter.js: source path

# STEP 2: Run export pipeline
npm run export:all && npm run deploy:all

# STEP 3: Remove temporary symlinks (not part of architecture)
rm .github/approaches .github/directives .github/guidelines .github/tactics .github/templates

# STEP 4: Validate outputs
ls .github/instructions/     # GitHub Copilot
ls .claude/skills/           # Claude Desktop
ls .opencode/agents/         # OpenCode standard
```
# CI/CD runs: npm run export:all && npm run deploy:all

Result: 
  doctrine/ (source) 
    → .github/agents/ (symlink for exporter compatibility)
    → dist/ (exporters generate)
    → .github/instructions/, .claude/, .opencode/ (deploy scripts)
```

**Why NOT Solution A (Symlinks Alone):**
- ❌ Windows requires Developer Mode (fails critical requirement)
- ❌ Cannot transform formats (fails critical requirement)
- ❌ Cannot optimize for tool-specific token limits

**Why NOT Solution C (Hybrid):**
- ⚠️ Adds complexity without benefit (Solution B already uses symlinks + exporters)
- ⚠️ Risk of local/CI divergence
- ⚠️ Two mechanisms to maintain vs one

### Architecture Decision

**Pattern: Symlinked Source + Exporter Distribution**

```
doctrine/ (canonical source, zero dependencies)
    ↓ symlink
.github/agents/ (backward compatibility for existing exporters)
    ↓ read by exporters
dist/opencode/, dist/skills/ (generated formats)
    ↓ deployed by scripts
.github/instructions/, .claude/, .opencode/ (tool-specific locations)
```

**Key Insight:** We don't need to choose between symlinks and exporters. Use BOTH:
- Symlinks for exporter compatibility (`.github/agents` → `doctrine/agents`)
- Exporters for format transformation and distribution
- **Zero exporter updates needed** (they already read from `.github/agents/`)

---

## Open Questions

~~**Q-1:** Do current exporters (`tools/exporters/*.js`) need updates, or can they consume via symlinks?~~
**A-1:** ✅ **ANSWERED** - Exporters should NOT be updated, they read from `.github/agents/` via symlinks.

~~**Q-2:** What is the expected Windows development workflow? (WSL, native, Docker?)~~
**A-2:** ✅ **ANSWERED** - Windows support is **CRITICAL**. Must work natively without special permissions.

~~**Q-3:** Are tool-specific format transformations required, or can all tools consume markdown?~~
**A-3:** ✅ **ANSWERED** - **YES**, format/location transformations are **REQUIRED** to optimize for different stacks.

~~**Q-4:** Should distribution be manual (developer-triggered) or automated (CI/CD)?~~
**A-4:** ✅ **ANSWERED** - **YES**, CI/CD pipelines already exist and should be used.

~~**Q-5:** What is acceptable latency between doctrine update and tool availability?~~
**A-5:** ✅ **ANSWERED** - CI/CD latency acceptable (seconds to minutes). This is **permanent architecture** being dogfooded.

---

## Acceptance Criteria

**AC-1: Single Source of Truth**
- [ ] All framework content exists in `doctrine/` only
- [ ] No duplicate content in tool-specific locations
- [ ] Changes to tool locations fail (immutable distribution)

**AC-2: Tool Discovery**
- [ ] GitHub Copilot discovers agents via `.github/`
- [ ] Claude Desktop discovers skills via `.claude/`
- [ ] OpenCode manifest valid and complete

**AC-3: Validation**
- [ ] Validation script confirms tool locations match `doctrine/`
- [ ] CI/CD validates distributions on every PR
- [ ] Mismatch detection provides actionable error messages

**AC-4: Performance**
- [ ] Full distribution completes in <30 seconds
- [ ] Incremental updates (if applicable) complete in <5 seconds
- [ ] Tool discovery latency <1 second after distribution

**AC-5: Documentation**
- [ ] Distribution mechanism documented in `doctrine/README.md`
- [ ] Troubleshooting guide for distribution failures
- [ ] CI/CD setup instructions

---

## Related Documents

- **ADR-XXX:** Doctrine extraction decision (pending)
- **SPEC-REPO-001:** Repository structure specification (pending)
- **Directive 013:** Tooling Setup & Fallbacks
- **Bootstrap Bill Profile:** Doctrine configuration responsibilities

---

## Validation Plan

**Phase 1: Local Testing (1 hour)**
1. Create symlinks in `.github/`, `.claude/`
2. Test GitHub Copilot agent discovery
3. Test exporter compatibility with symlinks
4. Document failures and edge cases

**Phase 2: Exporter Testing (2 hours)**
1. Run existing exporters via symlinks
2. Validate output in `dist/`, `.github/instructions/`, `.claude/skills/`
3. Test CI/CD deployment scripts
4. Document failures and edge cases

**Phase 3: Decision (30 minutes)**
1. Present findings to stakeholder
2. Select solution (A, B, or C)
3. Capture decision in ADR

**Phase 4: Implementation (2-4 hours)**
1. Implement selected solution
2. Create validation script
3. Update documentation
4. Commit and merge

---

## Status: READY FOR IMPLEMENTATION

**Decision:** Exporter-Based Distribution with Doctrine-to-Toolstack Mapping

**Critical Revision:** Remove symlinks as temporary crutch. Use proper exporter-based transformation with format optimization per toolstack.

**Next Actions:**
1. ✅ Document canonical doctrine → toolstack mapping (see below)
2. ✅ Update exporters to read from `doctrine/` instead of `.github/agents/`
3. ✅ Add format transformation logic where required
4. ✅ Run CI/CD pipeline: `npm run export:all && npm run deploy:all`
5. ✅ Validate outputs in `.github/instructions/`, `.claude/`, `.opencode/`
6. ✅ Remove temporary symlinks (not part of permanent architecture)
7. ✅ Document in `doctrine/README.md`
8. ✅ Create ADR documenting this architecture decision

**Implementation Owner:** DevOps Danny (distribution automation specialist)

**Validation Owner:** Analyst Annie (acceptance criteria verification)

**Blocked By:** None (all stakeholder questions answered, decision clear)
