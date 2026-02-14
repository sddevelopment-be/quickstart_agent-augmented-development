# Technical Design: SPEC-DIST-002 — Claude Code Distribution Optimization

**Date:** 2026-02-10
**Author:** Architect Alphonso
**Specification:** `specifications/initiatives/framework-distribution/SPEC-DIST-002-claude-code-optimization.md`
**Status:** PROPOSED
**Mode:** /analysis-mode

---

## 1. Architecture Overview

This design introduces a **Claude Code Generator** into the existing exporter pipeline. It sits alongside the OpenCode and Copilot generators but produces Claude Code-native artifacts rather than generic JSON/YAML exports.

```
doctrine/                    (single source of truth)
    │
    ├─► parser.js            (existing: markdown → IR)
    │       │
    │       ├─► opencode-generator.js     (existing)
    │       ├─► copilot-generator.js      (existing)
    │       └─► claude-code-generator.js  (NEW)
    │               │
    │               ├── generateClaudeMd()      → CLAUDE.md
    │               ├── generateRulesFiles()    → .claude/rules/*.md
    │               └── simplifyAgent()         → .claude/agents/*.md (lean)
    │
    └─► deploy-skills.js     (updated: new deploy functions)
            │
            ├── deployClaudeMd()     (NEW)
            ├── deployClaudeRules()  (NEW)
            ├── deployClaudeAgents() (MODIFIED: uses simplifyAgent)
            ├── deployClaudeSkills() (UNCHANGED)
            └── deployClaudePrompts() (REMOVED)
```

### Key Design Decision: Generator vs. Deploy-time Transformation

**Decision:** Implement as a **generator** (`claude-code-generator.js`), not as logic inside `deploy-skills.js`.

**Rationale:**
- Consistent with existing pattern (opencode-generator, copilot-generator are separate modules)
- Testable in isolation (unit tests on generator functions without file I/O)
- Reusable (generator can be called from CLI, CI/CD, or other scripts)
- deploy-skills.js remains a thin orchestrator that calls generators and writes files

---

## 2. Component Design

### 2.1 claude-code-generator.js

**Location:** `tools/exporters/claude-code-generator.js`

**Exports:**

```javascript
module.exports = {
  generateClaudeMd,     // (config) → string
  generateRulesFile,    // (sourceFiles[], ruleName) → string
  simplifyAgent,        // (agentIR) → string
  RULES_MAPPING         // config object: rule name → source files
};
```

#### generateClaudeMd(config)

**Input:** Configuration object with paths to source files.

```javascript
const config = {
  visionFile: 'VISION.md',
  quickRefFile: 'doctrine/directives/003_repository_quick_reference.md',
  pythonConventionsFile: 'doctrine/guidelines/python-conventions.md',
  projectRoot: '/path/to/repo'
};
```

**Algorithm:**
1. Read `VISION.md`, extract first paragraph under `## Problem` or opening description (purpose, 3-4 lines)
2. Read `doctrine/directives/003_repository_quick_reference.md`, extract directory structure table (key dirs only: `src/`, `tools/`, `tests/`, `doctrine/`, `work/`, `docs/`)
3. Read `doctrine/guidelines/python-conventions.md`, extract top-level conventions (formatting tool, test pattern name, type hint rule — 5-6 lines max)
4. Append common commands section (hardcoded: `python -m pytest`, `npm run deploy:claude`, etc.)
5. Append pointers to deeper context (`doctrine/` for full guidelines, `.claude/rules/` for auto-loaded rules)
6. Assemble into markdown with `<!-- Generated from doctrine/ — do not edit manually -->` header

**Output:** String (markdown content for CLAUDE.md)

**Constraint:** Output MUST be under 120 lines. If source extraction exceeds this, truncate lower-priority sections (commands, pointers) first.

#### generateRulesFile(sourceFiles, ruleName)

**Input:** Array of source file paths + rule name identifier.

**Algorithm:**
1. Read each source file
2. For each file, extract **actionable content** by:
   - Stripping YAML frontmatter
   - Stripping version history, metadata sections, "Related" sections
   - Stripping glossary cross-references (`See [GLOSSARY.md]...`)
   - Keeping imperative instructions, bullet points, code examples
3. Merge extracted content from all source files
4. Prepend source attribution: `<!-- Source: {file1}, {file2} -->`
5. Add rule title as H1
6. Enforce 80-line limit by truncating least-actionable content (examples before rules, prose before bullets)

**Output:** String (markdown content for a rules file)

#### simplifyAgent(agentIR)

**Input:** AgentIR object (output of existing `parser.js`)

**Algorithm:**
1. Extract from IR: `frontmatter.name`, `frontmatter.description`, `frontmatter.tools`
2. Map tools array to Claude Code native tool names:
   ```
   "read" → "Read", "write" → "Write", "search" → "Grep",
   "edit" → "Edit", "bash" → "Bash", "Bash" → "Bash",
   "Grep" → "Grep", "Glob" → "Glob", "MultiEdit" → "MultiEdit",
   "Python" → "Bash", "Java" → "Bash", "Docker" → "Bash",
   "Node" → "Bash", "plantuml" → "Bash",
   "markdown-linter" → "Bash", "todo" → "Bash"
   ```
3. Deduplicate mapped tools
4. Infer model hint from agent category:
   - architect, reviewer, analyst → `opus` (complex reasoning)
   - backend-dev, frontend, python-pedro, java-jenny → `sonnet` (coding)
   - curator, scribe, translator, diagrammer → `sonnet` (content)
   - lexical, researcher → `sonnet` (analysis)
   - bootstrap-bill, manager → `sonnet` (orchestration)
5. Extract Purpose section (section 2 in IR content)
6. Extract Specialization primary focus + avoid bullets (section 3)
7. Compose simplified markdown:
   ```markdown
   ---
   name: {name}
   description: {description}
   tools: [{mapped tools}]
   model: {model hint}
   ---

   {Purpose paragraph, max 3 sentences}

   Focus on:
   - {Primary focus bullet}

   Avoid:
   - {Avoid bullet}

   {Any key constraint from collaboration contract, 1 line max}
   ```

**Output:** String (markdown content for simplified agent file)

---

### 2.2 deploy-skills.js Modifications

**Modified functions:**

#### deployClaudeAgents() — MODIFIED

Current: reads `.agent.md` verbatim, writes to `.claude/agents/`.
New: reads `.agent.md` via parser → IR → `simplifyAgent()` → writes simplified output.

```javascript
// Current (line 516-525)
const content = await fs.readFile(sourcePath, 'utf-8');
await fs.writeFile(targetPath, content);

// New
const ir = await parseAgentFile(sourcePath);
const simplified = simplifyAgent(ir);
await fs.writeFile(targetPath, simplified);
```

**Dependency:** Requires importing `parser.js` and `claude-code-generator.js`.

#### deployClaudeRules() — NEW

```javascript
async function deployClaudeRules() {
  const rulesDir = path.join(CLAUDE_DIR, 'rules');
  await fs.mkdir(rulesDir, { recursive: true });

  for (const [ruleName, sourcePaths] of Object.entries(RULES_MAPPING)) {
    const content = generateRulesFile(sourcePaths, ruleName);
    await fs.writeFile(path.join(rulesDir, `${ruleName}.md`), content);
  }
}
```

#### deployClaudeMd() — NEW

```javascript
async function deployClaudeMd() {
  const content = generateClaudeMd({
    visionFile: path.join(ROOT, 'docs', 'VISION.md'),
    quickRefFile: path.join(ROOT, 'doctrine', 'directives', '003_repository_quick_reference.md'),
    pythonConventionsFile: path.join(ROOT, 'doctrine', 'guidelines', 'python-conventions.md'),
    projectRoot: ROOT
  });
  await fs.writeFile(path.join(ROOT, 'CLAUDE.md'), content);
}
```

#### main() — MODIFIED

Add `--rules` and `--claude-md` flags. Update `--all` and default to include them.

Remove `deployClaudePrompts()` from the default flow. Retain behind `--prompts-legacy` flag for migration.

---

### 2.3 RULES_MAPPING Configuration

```javascript
const RULES_MAPPING = {
  'guidelines': [
    'doctrine/guidelines/general_guidelines.md',
    'doctrine/guidelines/operational_guidelines.md'
  ],
  'coding-conventions': [
    'doctrine/guidelines/python-conventions.md'
  ],
  'testing': [
    'doctrine/directives/016_acceptance_test_driven_development.md',
    'doctrine/directives/017_test_driven_development.md'
  ],
  'architecture': [
    'doctrine/directives/018_traceable_decisions.md'
  ],
  'collaboration': [
    'doctrine/directives/019_file_based_collaboration.md'
  ]
};
```

This mapping is exposed as a module export so it can be overridden or extended by consuming projects.

---

## 3. Data Flow

```
Batch deployment (npm run deploy:claude):

  1. deployClaudeMd()
     VISION.md ──────────────────────┐
     doctrine/directives/003*.md ────┤──► generateClaudeMd() ──► ./CLAUDE.md
     doctrine/guidelines/python*.md──┘

  2. deployClaudeRules()
     doctrine/guidelines/*.md ────┐
     doctrine/directives/016*.md ─┤──► generateRulesFile() ──► .claude/rules/*.md
     doctrine/directives/017*.md ─┤     (×5 rule files)
     doctrine/directives/018*.md ─┤
     doctrine/directives/019*.md ─┘

  3. deployClaudeAgents()
     doctrine/agents/*.agent.md ──► parser.js ──► simplifyAgent() ──► .claude/agents/*.md

  4. deployClaudeSkills()  (UNCHANGED)
     dist/skills/claude-code/*.json ──► generateClaudeSkillMd() ──► .claude/skills/*/SKILL.md
```

---

## 4. Testing Strategy

### Unit Tests (`tests/unit/exporters/claude-code-generator.test.js`)

| Test | Input | Expected Output |
|---|---|---|
| `generateClaudeMd` produces valid markdown | Config with real file paths | Markdown string <120 lines, contains project purpose |
| `generateClaudeMd` handles missing files | Config with missing visionFile | Markdown with warning comment, no crash |
| `generateRulesFile` distills guidelines | guidelines source files | Markdown <80 lines, contains behavioral norms |
| `generateRulesFile` strips metadata | source with version history | Output lacks "Version History", "Last Updated" |
| `simplifyAgent` strips ceremony | Full architect IR | Markdown <40 lines, no directive tables |
| `simplifyAgent` maps tools correctly | IR with ["plantuml", "bash", "read"] | Tools: [Bash, Read] (deduped, mapped) |
| `simplifyAgent` infers model` | Architect IR | model: opus |
| `simplifyAgent` infers model` | Backend-dev IR | model: sonnet |

### Integration Tests (`tests/integration/deploy-claude-code.test.js`)

| Test | Setup | Assertion |
|---|---|---|
| Full deployment produces all artifacts | Run deploy with temp dir | CLAUDE.md + 5 rules + simplified agents exist |
| CLAUDE.md under 120 lines | Run deployClaudeMd | Line count assertion |
| Rules files under 80 lines each | Run deployClaudeRules | Line count assertion per file |
| Agent files under 40 lines each | Run deployClaudeAgents | Line count assertion per file |
| Idempotent deployment | Run deploy twice | File content identical |
| No prompts directory created | Run deploy:claude | .claude/prompts/ does not exist |

---

## 5. Risk Assessment

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| Content distillation loses critical instructions | High | Medium | Source attribution comments enable manual verification; acceptance tests validate key content present |
| Parser changes break existing generators | High | Low | simplifyAgent operates on existing IR output; no parser changes needed |
| Line count limits too aggressive | Medium | Medium | Limits are configurable constants; can be adjusted post-review |
| CLAUDE.md conflicts with user customizations | Medium | Low | Generated file includes "do not edit" comment; users can create CLAUDE.local.md for overrides |

---

## 6. Architectural Decisions

**AD-1: Generator as separate module, not inline in deploy script**
- Enables unit testing without file I/O mocking
- Consistent with opencode-generator.js / copilot-generator.js pattern
- Reusable across different deployment contexts

**AD-2: Static RULES_MAPPING over dynamic discovery**
- Explicit mapping is auditable and predictable
- Dynamic discovery would need heuristics to decide what maps where
- Configuration can be overridden by consuming projects

**AD-3: Hard line-count limits**
- Claude Code auto-loads CLAUDE.md and rules every session
- Bloated files cause context waste and instruction dilution
- Limits enforce discipline; can be relaxed with justification

**AD-4: Tool name mapping rather than passthrough**
- Doctrine uses lowercase tool names ("read", "write", "bash")
- Claude Code subagents use PascalCase tool names (Read, Write, Bash)
- Mapping ensures subagents declare tools Claude Code recognizes
- Non-mappable tools (plantuml, markdown-linter) map to Bash (CLI invocation)

---

## 7. Compatibility Notes

- **Existing skills pipeline:** Completely unchanged. `deployClaudeSkills()` is not modified.
- **Existing npm scripts:** `npm run deploy:claude:skills` continues to work. New scripts added for `deploy:claude:rules` and `deploy:claude:md`.
- **Backward compatibility:** `--prompts-legacy` flag retains old behavior for migration period.
- **Consuming repos:** RULES_MAPPING export allows other projects using this framework to customize which doctrine files map to which rules.

---

**Reviewer:** Architect Alphonso
**Status:** PROPOSED — awaiting Planning Petra task breakdown and human approval
