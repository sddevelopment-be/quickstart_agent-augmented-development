# Doctrine Stack: Source vs. Tool-Specific Distribution

**Date:** 2026-02-08  
**Author:** Curator Claire  
**Purpose:** Explain how `doctrine/` (source) relates to tool-specific directories (distribution)

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    DOCTRINE (Source of Truth)                     │
│                     doctrine/ directory                           │
│                                                                    │
│  ├── agents/        (21 agent profiles)                          │
│  ├── approaches/    (18 mental models)                           │
│  ├── directives/    (35+ instructions)                           │
│  ├── tactics/       (2 procedures)                               │
│  ├── guidelines/    (5 principles)                               │
│  ├── templates/     (boilerplates)                               │
│  └── examples/      (reference implementations)                   │
│                                                                    │
│                          ↓ EXPORT                                 │
│                  npm run export:all                               │
│                          ↓                                        │
│                      dist/ (generated)                            │
│                          ↓ DEPLOY                                 │
│                  npm run deploy:all                               │
│                          ↓                                        │
└──────────────────────────────────────────────────────────────────┘
                             ↓
     ┌──────────────┬──────────────┬──────────────┬──────────────┐
     ↓              ↓              ↓              ↓              ↓
  .github/      .claude/      .opencode/      .cursor/      .codex/
  (Copilot)     (Claude)      (OpenCode)     (Future)      (Future)
```

---

## Source: doctrine/ (Single Source of Truth)

**Total Files:** 221 files

### Directory Structure

```
doctrine/
├── AGENTS.md                    # Core agent specification
├── CHANGELOG.md                 # Version history
├── DOCTRINE_MAP.md              # Directory map
├── DOCTRINE_STACK.md            # Architecture documentation
├── GLOSSARY.md                  # Terminology standards
│
├── agents/                      # 21 agent profiles
│   ├── analyst-annie.agent.md
│   ├── architect.agent.md
│   ├── curator.agent.md
│   └── ... (18 more)
│
├── approaches/                  # 18 mental models/philosophies
│   ├── spec-driven-development.md
│   ├── trunk-based-development.md
│   ├── ralph-wiggum-loop.md
│   └── ... (15 more)
│
├── directives/                  # 35+ instructions/constraints
│   ├── 001_cli_shell_tooling.md
│   ├── 016_acceptance_test_driven_development.md
│   ├── 034_spec_driven_development.md
│   └── ... (32+ more)
│
├── tactics/                     # Procedural execution guides
│   ├── phase-checkpoint-protocol.md
│   ├── 6-phase-spec-driven-implementation-flow.md
│   └── ... (more to come)
│
├── guidelines/                  # Broad principles
│   ├── general_guidelines.md
│   ├── operational_guidelines.md
│   ├── commit-message-phase-declarations.md
│   └── ... (2 more)
│
├── templates/                   # Output structure contracts
│   ├── architecture/
│   ├── specifications/
│   └── prompts/
│
└── examples/                    # Reference implementations
    └── ... (various examples)
```

**Key Characteristic:** ALL content authored and maintained here. Never edit distribution directories directly.

---

## Distribution 1: .github/ (GitHub Copilot)

**Purpose:** GitHub Copilot CLI integration  
**Format:** Markdown with YAML frontmatter (Copilot schema)

### Directory Structure

```
.github/
├── copilot-instructions.md      # Consolidated AGENTS.md (generated)
│
└── instructions/                # Approaches exported as skills
    ├── architect-adr.instructions.md
    ├── bootstrap-repo.instructions.md
    ├── curate-directory.instructions.md
    ├── decision-first-development.instructions.md
    ├── ralph-wiggum-loop.instructions.md
    ├── spec-driven-development.instructions.md  # (if exported)
    └── ... (~25 instruction files)
```

### Mapping: doctrine/ → .github/

| Doctrine Source | GitHub Copilot Output | Transformation |
|-----------------|----------------------|----------------|
| `doctrine/AGENTS.md` | `.github/copilot-instructions.md` | Consolidated core spec |
| `doctrine/approaches/*.md` | `.github/instructions/*.instructions.md` | YAML frontmatter → Copilot schema |
| `doctrine/agents/*.agent.md` | (Not directly exported) | Agent profiles stay in doctrine |

**Export Script:** `tools/scripts/deploy-skills.js` (function `generateConsolidatedCopilotInstructions`)

**Notes:**
- GitHub Copilot uses `.instructions.md` files as "skills"
- Each approach becomes a separate instruction file
- Frontmatter transformed to match Copilot's schema: `https://aka.ms/copilot-skill-schema`

---

## Distribution 2: .claude/ (Claude Desktop)

**Purpose:** Claude Desktop MCP integration  
**Format:** Markdown with YAML frontmatter

### Directory Structure

```
.claude/
├── agents/                      # Agent profiles (21 files)
│   ├── analyst-annie.agent.md
│   ├── architect.agent.md
│   ├── curator.agent.md
│   ├── manifest.json            # Agent registry
│   └── README.md
│
├── skills/                      # Approaches as skills (18 directories)
│   ├── architect-adr/
│   │   └── SKILL.md
│   ├── bootstrap-repo/
│   │   └── SKILL.md
│   ├── decision-first-development/
│   │   └── SKILL.md
│   └── ... (~18 skill directories)
│
└── prompts/                     # Prompt templates (8 files)
    ├── ARCHITECT_ADR.prompt.md
    ├── BOOTSTRAP_REPO.prompt.md
    ├── NEW_AGENT.prompt.md
    ├── manifest.json
    └── ... (5 more prompt files)
```

### Mapping: doctrine/ → .claude/

| Doctrine Source | Claude Desktop Output | Transformation |
|-----------------|----------------------|----------------|
| `doctrine/agents/*.agent.md` | `.claude/agents/*.agent.md` | Direct copy (minimal transform) |
| `doctrine/approaches/*.md` | `.claude/skills/*/SKILL.md` | Markdown → SKILL.md format |
| `docs/templates/prompts/*.prompt.md` | `.claude/prompts/*.prompt.md` | Direct copy |

**Export Script:** `tools/scripts/deploy-skills.js` (functions `deployClaudeAgents`, `deployClaudeSkills`, `deployClaudePrompts`)

**Notes:**
- Claude Desktop discovers agents via `.claude/agents/` directory
- Skills organized in subdirectories (one per skill)
- Each skill has `SKILL.md` with frontmatter and instructions

---

## Distribution 3: .opencode/ (OpenCode)

**Purpose:** OpenCode AI integration  
**Format:** JSON (discovery) + YAML (definitions)

### Directory Structure

```
.opencode/
├── agents/                      # Agent definitions (21 agents)
│   ├── analyst-annie.opencode.json
│   ├── analyst-annie.definition.yaml
│   ├── architect.opencode.json
│   ├── architect.definition.yaml
│   └── ... (~42 files: JSON + YAML pairs)
│
├── skills/                      # Approach definitions
│   ├── architect-adr.opencode-skill.json
│   ├── decision-first-development.opencode-approach.json
│   ├── ralph-wiggum-loop.opencode-approach.json
│   └── ... (~25 JSON files)
│
├── manifest.opencode.json       # Tool registry
└── tools.opencode.json          # Available tools
```

### Mapping: doctrine/ → .opencode/

| Doctrine Source | OpenCode Output | Transformation |
|-----------------|----------------|----------------|
| `doctrine/agents/*.agent.md` | `.opencode/agents/*.opencode.json` | Markdown → JSON (discovery) |
| `doctrine/agents/*.agent.md` | `.opencode/agents/*.definition.yaml` | Markdown → YAML (details) |
| `doctrine/approaches/*.md` | `.opencode/skills/*.opencode-approach.json` | Markdown → JSON |

**Export Script:** `tools/exporters/opencode-exporter.js`

**Notes:**
- OpenCode uses **dual-file format**: JSON for discovery, YAML for definitions
- Agent metadata extracted from YAML frontmatter → JSON schema
- Each agent gets TWO files: `*.opencode.json` + `*.definition.yaml`

---

## Distribution 4: .cursor/ (Future)

**Purpose:** Cursor IDE integration  
**Status:** **Not yet implemented** (deferred to Phase 2-3 per architectural decision)

### Planned Structure

```
.cursor/
└── rules/                       # Agent profiles as markdown
    ├── analyst-annie.md
    ├── architect.md
    └── ... (~21 rule files)
```

### Planned Mapping: doctrine/ → .cursor/

| Doctrine Source | Cursor Output | Transformation |
|-----------------|--------------|----------------|
| `doctrine/agents/*.agent.md` | `.cursor/rules/*.md` | Minimal transform (remove frontmatter?) |

**Export Script:** To be created (e.g., `tools/exporters/cursor-exporter.js`)

**Notes:**
- Cursor uses `.cursorrules` file or `.cursor/rules/` directory
- Likely minimal transformation (Cursor accepts markdown)
- Prioritization: Phase 2-3 (80% coverage with Copilot/Claude/OpenCode)

---

## Distribution 5: .codex/ (Future)

**Purpose:** Codex integration  
**Status:** **Not yet implemented** (deferred to Phase 2-3)

### Planned Structure

```
.codex/
├── system-prompt.md             # Consolidated AGENTS.md
└── agents/                      # Agent definitions (JSON)
    ├── analyst-annie.json
    ├── architect.json
    └── ... (~21 JSON files)
```

### Planned Mapping: doctrine/ → .codex/

| Doctrine Source | Codex Output | Transformation |
|-----------------|-------------|----------------|
| `doctrine/AGENTS.md` | `.codex/system-prompt.md` | Consolidated core spec |
| `doctrine/agents/*.agent.md` | `.codex/agents/*.json` | Markdown → JSON |

**Export Script:** To be created (e.g., `tools/exporters/codex-exporter.js`)

**Notes:**
- Codex format similar to OpenCode (JSON-based)
- May need custom schema for Codex API requirements
- Prioritization: Phase 3 (after Cursor)

---

## Export/Deploy Pipeline

### Step 1: Export (Generate dist/ artifacts)

```bash
npm run export:all
```

**What it does:**
1. `npm run export:agents` → `tools/exporters/opencode-exporter.js`
   - Reads `doctrine/agents/*.agent.md`
   - Generates `dist/opencode/agents/*.opencode.json` + `*.definition.yaml`
   - Generates `dist/opencode/manifest.opencode.json`

2. `npm run export:skills` → `tools/scripts/skills-exporter.js`
   - Reads `docs/templates/prompts/*.prompt.md`
   - Reads `doctrine/approaches/*.md`
   - Generates `dist/skills/claude-code/*.json`
   - Generates `dist/skills/copilot/*.json`
   - Generates `dist/skills/opencode/*.json`

**Output:** `dist/` directory with tool-specific artifacts (not checked into git)

---

### Step 2: Deploy (Copy to tool-specific locations)

```bash
npm run deploy:all
```

**What it does:**
1. `deployClaudeSkills()` → `.claude/skills/*/SKILL.md`
2. `deployClaudeAgents()` → `.claude/agents/*.agent.md`
3. `deployClaudePrompts()` → `.claude/prompts/*.prompt.md`
4. `deployCopilotInstructions()` → `.github/instructions/*.instructions.md`
5. `deployOpenCodeConfiguration()` → `.opencode/agents/`, `.opencode/skills/`

**Script:** `tools/scripts/deploy-skills.js` (single orchestrator)

**Output:** Tool-specific directories populated with current doctrine content

---

## Format Transformations

### Transformation 1: YAML Frontmatter → JSON Schema

**Input (doctrine/agents/analyst-annie.agent.md):**
```yaml
---
name: analyst-annie
description: Requirements and validation specialist
tools: [ "read", "write", "search" ]
---
```

**Output (.opencode/agents/analyst-annie.opencode.json):**
```json
{
  "id": "analyst-annie",
  "name": "Analyst Annie",
  "description": "Requirements and validation specialist",
  "tools": ["read", "write", "search"],
  "version": "1.0.0"
}
```

**Transformation Logic:** `tools/exporters/opencode-exporter.js` (function `parseAgentProfile`)

---

### Transformation 2: Markdown Narrative → Structured Sections

**Input (doctrine/approaches/ralph-wiggum-loop.md):**
```markdown
# Ralph Wiggum Loop

The Ralph Wiggum Loop is a self-observation pattern...

## When to Use
- Long-running tasks
- Multi-step workflows
...
```

**Output (.claude/skills/ralph-wiggum-loop/SKILL.md):**
```markdown
# ralph-wiggum-loop

Ralph Wiggum Loop: Self-Observation and Correction Pattern

## Capabilities
- self-observation
- meta-cognition

## Instructions
The Ralph Wiggum Loop is a self-observation pattern...
...
```

**Transformation Logic:** `tools/scripts/deploy-skills.js` (function `generateClaudeSkillMd`)

---

### Transformation 3: Directive References → Embedded Content (Tool-Specific)

**Challenge:** Some tools don't support external file references

**Current Approach:** 
- Copilot: References preserved (tools can read `.github/` structure)
- Claude: References preserved (MCP can read `.claude/` structure)
- OpenCode: References embedded in JSON (no external file support)

**Future Enhancement:** May need to embed directive content for Codex/Cursor depending on their capabilities

---

## Validation: Source vs. Distribution Consistency

### Rule: Distribution Files are Generated (Never Manually Edit)

**✅ CORRECT Workflow:**
1. Edit source: `doctrine/agents/analyst-annie.agent.md`
2. Run export: `npm run export:all`
3. Run deploy: `npm run deploy:all`
4. Commit both: `doctrine/agents/` AND `.claude/agents/`, `.github/instructions/`, etc.

**❌ INCORRECT Workflow:**
1. Edit distribution: `.claude/agents/analyst-annie.agent.md`
2. Commit distribution only
3. **Result:** Next export/deploy OVERWRITES manual changes (data loss!)

---

### Validation Script (Proposed)

```bash
# Check if distribution files are newer than source
npm run validate:distribution
```

**Logic:**
- For each file in `.claude/agents/`, `.github/instructions/`, `.opencode/agents/`
- Find corresponding source in `doctrine/`
- Compare timestamps
- If distribution newer than source → ⚠️ WARNING (manual edit detected)

**Status:** Not yet implemented (would be useful for CI/CD)

---

## Summary: Key Principles

### Principle 1: Single Source of Truth
- `doctrine/` is canonical
- Tool-specific directories are **generated artifacts** (like compiled code)
- Never edit distribution files directly

### Principle 2: Transformation Preserves Meaning
- Format may change (Markdown → JSON), but semantic content preserved
- Tool-specific optimizations allowed (e.g., embedded references)
- Validation: Distribution should contain all information from source

### Principle 3: Export/Deploy Pipeline is Deterministic
- Same source → same distribution (reproducible)
- Pipeline can be re-run anytime without data loss
- CI/CD can automate: commit to doctrine/ → auto export/deploy

### Principle 4: Tool-Specific Directories Are Checked Into Git
- Unlike traditional build artifacts (e.g., `dist/` ignored)
- Distribution files committed for tool discovery (e.g., Copilot reads `.github/`)
- **Rationale:** Each tool needs its format present in repository

### Principle 5: Curation Happens at Source
- Curator Claire audits `doctrine/` (not distribution directories)
- After doctrine changes: re-export, re-deploy, commit all changes
- Distribution consistency maintained by pipeline (not manual curation)

---

## Related Documentation

- **Doctrine Stack:** [doctrine/DOCTRINE_STACK.md](./DOCTRINE_STACK.md) - Architecture
- **Doctrine Map:** [doctrine/DOCTRINE_MAP.md](./DOCTRINE_MAP.md) - Directory structure
- **Curator Profile:** [doctrine/agents/curator.agent.md](./agents/curator.agent.md) - Section 2.1
- **Export Code:** `tools/exporters/` - Export scripts
- **Deploy Code:** `tools/scripts/deploy-skills.js` - Deployment orchestrator

---

**Version:** 1.0.0  
**Date:** 2026-02-08  
**Author:** Curator Claire  
**Status:** Complete ✅
