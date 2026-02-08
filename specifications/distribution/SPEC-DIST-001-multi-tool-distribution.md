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

**✅ SOLUTION B: EXPORTER STRATEGIC APPROACH WITH SYMLINKS**

**Analyst Annie Recommendation:** Based on stakeholder input, **Solution B (Exporters)** is the only viable option that meets all critical requirements:

### Why Solution B

**Critical Requirements Met:**
1. ✅ **Windows Support:** Exporters work cross-platform without special permissions
2. ✅ **Format Transformation:** Can generate JSON (OpenCode), optimized markdown (Claude), instruction files (Copilot)
3. ✅ **CI/CD Integration:** Leverages existing pipelines (`npm run export:all && npm run deploy:all`)
4. ✅ **Permanent Architecture:** Designed for long-term use, not tactical workaround

**Implementation Strategy:**
```bash
# Create symlinks: .github/agents → doctrine/agents (backward compatibility)
# Keep existing exporters reading from .github/agents/ (no changes needed!)
# Exporters automatically pick up doctrine/ content via symlinks
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

**Decision:** Solution B (Exporters with Symlinks for Compatibility)

**Next Actions:**
1. ✅ Create symlinks: `.github/agents` → `doctrine/agents` (backward compatibility)
2. ✅ Create symlinks: `.github/directives`, `.github/approaches`, etc.
3. ✅ Verify existing exporters work via symlinks (no updates needed)
4. ✅ Run CI/CD pipeline: `npm run export:all && npm run deploy:all`
5. ✅ Validate outputs in `.github/instructions/`, `.claude/`, `.opencode/`
6. ✅ Document in `doctrine/README.md`
7. ✅ Create ADR documenting this architecture decision

**Implementation Owner:** DevOps Danny (distribution automation specialist)

**Validation Owner:** Analyst Annie (acceptance criteria verification)

**Blocked By:** None (all stakeholder questions answered, decision clear)
