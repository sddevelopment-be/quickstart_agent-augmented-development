# Cursor-Doctrine Stack Optimization Analysis

**Date:** 2026-02-10  
**Task:** Analyze how to optimize doctrine stack for Cursor-based agents  
**Status:** IN PROGRESS

---

## Executive Summary

**Current State:**
- ✅ Doctrine stack fully implemented (`doctrine/` directory with 5-layer system)
- ✅ Claude Code integration via `.claude/` directory (69 files)
- ✅ Export pipeline for Copilot and OpenCode formats
- ❌ **NO Cursor-specific integration** (no `.cursorrules` or `.cursor/` directory)
- ⚠️ CLAUDE.md and AGENTS.md used as auto-loaded rules via Cursor's project instructions feature

**Discovery:**
Cursor appears to be loading `AGENTS.md` and `CLAUDE.md` automatically as project-level context, allowing the doctrine stack to work "as-is" without explicit Cursor-specific transformation.

---

## Research Findings

### 1. Cursor Context Loading Mechanisms

Based on repository evidence and current session initialization:

#### A. Project Instructions (Auto-loaded)
- **Files:** `AGENTS.md`, `CLAUDE.md` in repo root
- **Evidence:** Current session shows both files in `<always_applied_workspace_rule>` tags
- **Status:** ✅ WORKING - This session loaded both automatically
- **Format:** Markdown with full doctrine stack references

#### B. `.cursorrules` File (Not Present)
- **Location:** Repository root (`.cursorrules`)
- **Status:** ❌ NOT IMPLEMENTED
- **Purpose:** Single-file rules that Cursor loads automatically
- **Use Case:** Simplified alternative to AGENTS.md/CLAUDE.md

#### C. `.cursor/` Directory (Not Present)
- **Location:** `.cursor/rules/*.md`
- **Status:** ❌ NOT IMPLEMENTED  
- **Purpose:** Modular rule files (similar to `.claude/rules/`)
- **Evidence:** Spec mentions this pattern but unclear if officially supported

### 2. How This Repository Currently Works with Cursor

**Mechanism:** Cursor's "Project Instructions" feature auto-discovers:
1. `AGENTS.md` (432 lines) - Agent initialization protocol + doctrine stack overview
2. `CLAUDE.md` (44 lines) - Quick reference for coding conventions and structure

**Result:** Agents can access:
- ✅ Bootstrap protocol (via AGENTS.md § "MANDATORY BOOTSTRAP REQUIREMENT")
- ✅ Context stack layers (via AGENTS.md § "Context Stack Overview")
- ✅ Extended directives index (via AGENTS.md § "Extended Directives Index")
- ✅ Repository structure (via CLAUDE.md)
- ⚠️ Full doctrine stack available by reference (must explicitly load from `doctrine/`)

**Token Cost:**
- AGENTS.md: ~432 lines ≈ 3,500 tokens
- CLAUDE.md: ~44 lines ≈ 350 tokens
- **Total auto-load: ~3,850 tokens per session**

---

## Cursor vs Claude Code: Key Differences

| Aspect | Claude Code (`.claude/`) | Cursor (current approach) |
|--------|-------------------------|---------------------------|
| **Auto-load mechanism** | Manifest-based (prompts, agents) | File-based (AGENTS.md, CLAUDE.md) |
| **Format** | Directory structure with SKILL.md | Markdown files in root |
| **Agent switching** | Via manifest + UI | Via manual profile loading |
| **Modular rules** | `.claude/rules/*.md` | Potentially `.cursor/rules/*.md` (unverified) |
| **Token efficiency** | Skills loaded on-demand | Full AGENTS.md loaded upfront |
| **Discoverability** | High (manifest + UI) | Medium (must know to reference doctrine/) |

---

## Gap Analysis: What's Missing for Cursor Optimization

### A. Token Efficiency
**Problem:** AGENTS.md loads full specification (~3,850 tokens) every session
**Impact:** High token cost for simple tasks that don't need full governance

**Solution Options:**
1. **Runtime Sheet Mode (Recommended):** Create minimal `.cursorrules` that references `doctrine/guidelines/runtime_sheet.md` (~150 tokens)
2. **Tiered Loading:** Multiple `.cursorrules` variants (minimal, standard, full)
3. **Status Quo:** Keep AGENTS.md auto-load (works but expensive)

### B. Specialized Agent Profiles
**Problem:** No Cursor-native way to switch between specialist agents (Architect, Python Pedro, etc.)
**Impact:** All agents get same generic context; can't leverage specialization

**Solution Options:**
1. **Cursor Rules Directory:** Export agents to `.cursor/rules/agent-*.md` (not verified if supported)
2. **Manual Loading:** Agents explicitly load profiles via `@doctrine/agents/python-pedro.agent.md`
3. **Hybrid:** Minimal `.cursorrules` + explicit profile loading when needed

### C. Directive Discovery
**Problem:** Extended directives (001-036) not exposed to Cursor except by manual reference
**Impact:** Agents must know to look in `doctrine/directives/` directory

**Solution Options:**
1. **Export to `.cursor/directives/`:** Mirror structure (if supported)
2. **Embed in `.cursorrules`:** Inline critical directives (token-heavy)
3. **Index File:** Create `.cursor/DIRECTIVES_INDEX.md` for quick reference

### D. Tactics & Approaches Accessibility
**Problem:** Tactics and approaches buried in `doctrine/` structure
**Impact:** Agents rarely discover or propose tactics

**Solution Options:**
1. **Quick Reference:** Create `.cursor/TACTICS_CATALOG.md` with one-liner summaries
2. **Embed Common Ones:** Include 5-10 most-used tactics in `.cursorrules`
3. **On-Demand Loading:** Keep current approach (explicit loading via `@doctrine/tactics/`)

---

## Recommendations

### Phase 1: Optimize Current Approach (Low Effort, High Impact)

**Goal:** Reduce token cost while maintaining full doctrine stack access

#### Option A: Replace AGENTS.md with Runtime Sheet Reference (RECOMMENDED)

Create `.cursorrules` file:

```markdown
# Agent Runtime Reference

Load minimal context + full doctrine stack by reference.

**Bootstrap:** `doctrine/guidelines/bootstrap.md` (58 lines)
**Core Guidelines:** `doctrine/guidelines/runtime_sheet.md` (~150 lines)
**Full Spec:** `AGENTS.md` (load on-demand for high-stakes tasks)

## Key Paths
- Directives: `doctrine/directives/` (load via `/require-directive NNN`)
- Agents: `doctrine/agents/*.agent.md` (load when specializing)
- Tactics: `doctrine/tactics/` (discover via README.md)

## Default Mode
- Small-footprint protocol (bootstrap.md § "Choose the Path First")
- Analysis mode by default
- Work directory: `work/`
- Integrity symbol: ✅/⚠️/❗️

## Common Commands
- `/require-directive NNN` - Load extended directive
- `/validate-alignment` - Check integrity
- `@doctrine/agents/AGENT.agent.md` - Load specialist profile
```

**Impact:**
- Token reduction: 3,850 → ~500 tokens (87% reduction)
- Maintains full doctrine stack access by reference
- Compatible with existing bootstrap protocol

#### Option B: Keep Status Quo + Add Quick Reference

Keep AGENTS.md auto-load, add `.cursor/QUICK_REFERENCE.md`:

```markdown
# Doctrine Stack Quick Reference

## Frequently Used Directives
- 016: ATDD workflow
- 017: TDD workflow
- 018: Traceable decisions (ADRs)
- 020: Locality of change
- 028: Bug fixing techniques
- 036: Boy Scout Rule

## Common Tactics
- `stopping-conditions.tactic.md` - Define exit criteria
- `ATDD_adversarial-acceptance.tactic.md` - Red team acceptance tests
- `premortem-risk-identification.tactic.md` - Find failure modes

## Specialist Agents
- `python-pedro.agent.md` - Python + testing
- `architect.agent.md` - System design + ADRs
- `curator-claire.agent.md` - Consistency + metadata
```

**Impact:**
- No token reduction (keeps full AGENTS.md load)
- Improves discoverability
- Easy maintenance

---

### Phase 2: Cursor-Specific Distribution (Medium Effort)

**Goal:** Create Cursor-native distribution similar to `.claude/`

#### Create `.cursor/` Directory Structure

```
.cursor/
├── rules/
│   ├── guidelines.md              # Consolidated general + operational
│   ├── architecture.md            # ADR and design practices
│   ├── testing.md                 # ATDD + TDD workflows
│   └── collaboration.md           # Multi-agent coordination
├── agents/
│   ├── python-pedro.md            # Specialist profiles (markdown)
│   ├── architect.md
│   └── ... (21 profiles)
└── QUICK_REFERENCE.md             # Directives + tactics index
```

**Export Script:** `tools/exporters/cursor-exporter.js`

**Transformation:**
- Agents: Markdown → Markdown (remove YAML frontmatter)
- Directives: Embed into `rules/*.md` by category
- Approaches: Embed into relevant rule files
- Guidelines: Consolidate into minimal files

**Integration:**
- Update `.cursorrules` to reference `.cursor/` directory
- Maintain `AGENTS.md` as canonical source
- Export via `npm run export:cursor`

---

### Phase 3: Advanced Features (Low Priority)

#### A. Cursor Agent Profiles (If Supported)
- Investigate if Cursor supports multiple profile switching
- Export agents to format Cursor can discover
- Requires Cursor documentation research

#### B. Dynamic Context Assembly
- Script to generate custom `.cursorrules` based on task type
- Example: `./ops/scripts/cursor-context.sh --agent python-pedro --directives 016,017`
- Outputs: Temporary `.cursorrules` with relevant context only

#### C. Cursor-Specific Skills/Commands
- Map doctrine shorthands (`/architect-adr`, `/fix-bug`) to Cursor commands
- Create `.cursor/commands/` directory (if supported)
- Investigate Cursor command extensibility

---

## Decision Matrix

| Approach | Token Cost | Effort | Doctrine Access | Discoverability | Maintenance |
|----------|-----------|--------|----------------|----------------|-------------|
| **A: Runtime Sheet .cursorrules** | 🟢 Low (~500) | 🟢 Low (1 file) | 🟢 Full (by ref) | 🟡 Medium | 🟢 Low |
| **B: Status Quo + Quick Ref** | 🔴 High (~3,850) | 🟢 Low (1 file) | 🟢 Full (loaded) | 🟢 High | 🟢 Low |
| **C: .cursor/ Distribution** | 🟡 Medium (~1,500) | 🔴 High (exporter) | 🟢 Full (exported) | 🟢 High | 🟡 Medium |

---

## Proposed Next Steps

### Immediate (This Session)
1. ✅ Document current Cursor integration mechanism
2. ⬜ Create `.cursorrules` with runtime sheet approach (Option A)
3. ⬜ Test token reduction impact
4. ⬜ Verify doctrine stack still accessible by reference

### Short-Term (Next Session)
1. ⬜ Create `.cursor/QUICK_REFERENCE.md` for discoverability
2. ⬜ Update bootstrap.md to document Cursor-specific path
3. ⬜ Add Cursor integration section to DOCTRINE_DISTRIBUTION.md

### Medium-Term (Sprint Planning)
1. ⬜ Design `.cursor/` directory structure specification
2. ⬜ Implement `cursor-exporter.js` similar to copilot/opencode exporters
3. ⬜ Add `npm run export:cursor` command
4. ⬜ Test exported artifacts with Cursor agents

---

## Open Questions

1. **Does Cursor officially support `.cursor/rules/` directory?**
   - Evidence suggests yes (spec mentions it)
   - Needs verification with Cursor documentation

2. **Can Cursor load multiple rule files selectively?**
   - Unknown if Cursor has agent profile switching
   - May need manual `@.cursor/agents/AGENT.md` loading

3. **What's the token limit before Cursor performance degrades?**
   - Current 3,850 tokens seems acceptable
   - Runtime sheet approach (500 tokens) would be safer

4. **Should we maintain parallel .cursor/ and .claude/ distributions?**
   - Increases maintenance burden (2x exports)
   - May be worth it for ecosystem coverage

---

## Conclusion

**Recommended Path: Hybrid Approach**

1. **Short-term:** Create minimal `.cursorrules` with runtime sheet reference (87% token reduction)
2. **Medium-term:** Build `.cursor/` distribution for full ecosystem parity
3. **Long-term:** Investigate Cursor-specific features (commands, profiles, etc.)

**Key Insight:** The existing doctrine stack works well with Cursor via AGENTS.md auto-load. The optimization is about token efficiency and discoverability, not fundamental compatibility.

---

**Next Action:** Propose `.cursorrules` content to user for review before implementation.
