# Reusable Prompts for Agent Workflows

This directory contains structured, reusable prompts to streamline common agent-driven tasks. Each prompt begins with context clearing and agent bootstrap to prevent context leakage and degradation.

## Prompt Format

All prompts follow this structure:

```markdown
---
description: '<brief description>'
agent: <target-agent-name>
category: <workflow-category>
complexity: <low|medium|high>
inputs_required: <comma-separated list of critical inputs>
outputs: <comma-separated list of expected outputs>
tags: [<tag1>, <tag2>, ...]
version: <YYYY-MM-DD>
---

Clear context. Bootstrap as <Agent Name>. When ready:

[Prompt content with Inputs / Task / Output / Constraints sections]
```

## Metadata Header Fields

| Field             | Required | Description                        | Example                                             |
|-------------------|----------|------------------------------------|-----------------------------------------------------|
| `description`     | ✅        | Brief one-line description         | `'Prompt for creating new specialized agents'`      |
| `agent`           | ✅        | Target agent name (slug)           | `manager-mike`                                      |
| `category`        | ✅        | Workflow category                  | `agent-management`, `documentation`, `architecture` |
| `complexity`      | ✅        | Effort level                       | `low`, `medium`, `high`                             |
| `inputs_required` | ✅        | Critical input fields (comma list) | `NAME, PURPOSE, PRIMARY_FOCUS`                      |
| `outputs`         | ✅        | Expected output artifacts          | `agent file, status update`                         |
| `tags`            | ⚠️       | Searchable keywords (array)        | `[agent, creation, coordination]`                   |
| `version`         | ⚠️       | Last updated date                  | `2025-11-22`                                        |

## Available Prompts

### Agent Management

#### [NEW_AGENT.prompt.md](NEW_AGENT.prompt.md)

**Agent:** Manager Mike  
**Purpose:** Create a new specialized agent definition  
**Complexity:** Medium  
**Key Inputs:** Agent name, purpose, focus areas, tools  
**Outputs:** Agent profile file, optional references doc, coordination status update

**Use when:**

- Need a new specialist for a specific domain
- Extending the agent ecosystem
- Defining custom agent behavior

---

### Repository Structure

#### [BOOTSTRAP_REPO.prompt.md](BOOTSTRAP_REPO.prompt.md)

**Agent:** Bootstrap Bill  
**Purpose:** Bootstrap a cloned repository for local/project context  
**Complexity:** Medium  
**Key Inputs:** Vision, scope, tech stack, constraints  
**Outputs:** Vision doc, guidelines, repo map, surfaces, workflows

**Use when:**

- Setting up a new repository
- Adapting this template to your project
- Defining repository vision and boundaries

---

#### [CURATE_DIRECTORY.prompt.md](CURATE_DIRECTORY.prompt.md)

**Agent:** Curator Claire  
**Purpose:** Audit and normalize structure/tone/metadata in target directory  
**Complexity:** Medium  
**Key Inputs:** Target path, scope, style anchors, rules  
**Outputs:** Curation report, proposed deltas, metrics

**Use when:**

- Ensuring consistency across documentation
- Detecting structural or tonal drift
- Validating metadata completeness

---

### Architecture & Design

#### [ARCHITECT_ADR.prompt.md](ARCHITECT_ADR.prompt.md)

**Agent:** Architect Alphonso  
**Purpose:** Perform architectural analysis and draft a Proposed ADR  
**Complexity:** High  
**Key Inputs:** Decision title, context, forces, options, preferred choice  
**Outputs:** ADR markdown, option impact matrix, success metrics

**Use when:**

- Making architectural decisions
- Documenting trade-offs and rationale
- Evaluating design alternatives

---

### Content & Documentation

#### [LEXICAL_ANALYSIS.prompt.md](LEXICAL_ANALYSIS.prompt.md)

**Agent:** Lexical Larry  
**Purpose:** Perform lexical style diagnostic and minimal diff proposal  
**Complexity:** Low  
**Key Inputs:** Target files, style anchor, tone objectives  
**Outputs:** LEX_REPORT, LEX_DELTAS, metrics summary

**Use when:**

- Checking style compliance
- Detecting tone drift
- Preparing minimal style corrections

---

#### [EDITOR_REVISION.prompt.md](EDITOR_REVISION.prompt.md)

**Agent:** Editor Eddy  
**Purpose:** Refine draft document using lexical analysis outputs  
**Complexity:** Medium  
**Key Inputs:** Draft file, lexical report/deltas, style anchor  
**Outputs:** Revised draft, patch/diff, rationale summary

**Use when:**

- Polishing drafts based on lexical analysis
- Applying tone and clarity improvements
- Preserving voice while enhancing readability

**Typical workflow:** LEXICAL_ANALYSIS → EDITOR_REVISION

---

### Automation & Tooling

#### [AUTOMATION_SCRIPT.prompt.md](AUTOMATION_SCRIPT.prompt.md)

**Agent:** DevOps Danny  
**Purpose:** Generate automation script from requirements or direct prompt  
**Complexity:** Medium to High  
**Key Inputs:** Purpose, platform, tools, constraints  
**Outputs:** Script file, runbook, optional CI snippet

**Use when:**

- Automating repetitive tasks
- Creating CI/CD workflows
- Building deployment or validation scripts

---

## Usage Guidelines

### How to Use a Prompt

1. **Copy the prompt content** from the desired `.prompt.md` file
2. **Replace placeholder values** (e.g., `<NAME>`, `<PURPOSE>`) with your specifics
3. **Paste into your AI assistant** conversation
4. **Review outputs** in the designated `work/` or `output/` directories

### Best Practices

- **Start fresh:** The "Clear context" directive prevents context leakage
- **Complete inputs:** Fill all required fields; agents will ask for clarification if critical inputs missing
- **Review outputs:** Agent outputs are proposals; review before integrating
- **Iterate:** Use prompts multiple times with refinements
- **Compose workflows:** Chain prompts (e.g., LEXICAL_ANALYSIS → EDITOR_REVISION)

### Prompt Composition Patterns

**Documentation Quality Pass:**

```
1. LEXICAL_ANALYSIS (detect issues)
2. EDITOR_REVISION (apply fixes)
3. CURATE_DIRECTORY (validate consistency)
```

**New Feature Setup:**

```
1. ARCHITECT_ADR (design decision)
2. NEW_AGENT (create specialist if needed)
3. AUTOMATION_SCRIPT (generate tooling)
```

**Repository Initialization:**

```
1. BOOTSTRAP_REPO (structure and vision)
2. CURATE_DIRECTORY (validate setup)
3. NEW_AGENT (add required specialists)
```

---

## Extending This Collection

### Adding New Prompts

1. Create file: `.github/prompts/<NAME>.prompt.md`
2. Follow metadata header format (see above)
3. Structure content: Inputs / Task / Output / Constraints
4. Start with: `Clear context. Bootstrap as <Agent>. When ready:`
5. Update this README with new entry
6. Test with target agent

### Metadata Conventions

- **agent:** Use slug from `agents/<agent>.agent.md` filename
- **category:** Choose from: `agent-management`, `documentation`, `architecture`, `automation`, `analysis`, `coordination`
- **complexity:**
    - `low`: < 5 inputs, single output, < 5 min
    - `medium`: 5-10 inputs, multiple outputs, 5-15 min
    - `high`: > 10 inputs, complex analysis, > 15 min
- **tags:** Use lowercase, hyphenated keywords for search

### Quality Checklist

- [ ] Metadata header complete
- [ ] Clear context + bootstrap directive present
- [ ] Inputs section with placeholders
- [ ] Task section with numbered steps
- [ ] Output section with artifacts list
- [ ] Constraints section with boundaries
- [ ] Clarifying questions trigger defined
- [ ] Agent-specific directives referenced
- [ ] No hype, flattery, or subjective claims
- [ ] Tested with target agent

---

## Related Documentation

- [Issue Templates Guide](../../docs/HOW_TO_USE/ISSUE_TEMPLATES_GUIDE.md) - GitHub issue-based agent workflows
- [Quickstart Guide](../../docs/HOW_TO_USE/QUICKSTART.md) - General agent usage
- [Agent Profiles](../../agents/) - Specialist agent definitions
- [Directives](../../agents/directives/) - Operational directives
- [Templates](../../docs/templates/) - Output templates for agents

---

## Troubleshooting

**Prompt not working:**

- Verify agent name matches profile in `agents/`
- Check all required inputs are provided
- Ensure placeholders (`<NAME>`) are replaced

**Wrong output location:**

- Agents default to `work/<agent>/` or `output/`
- Check agent profile for operating procedure

**Need customization:**

- Copy prompt as template
- Modify Inputs/Task/Constraints sections
- Keep metadata header pattern

**Agent doesn't respond:**

- Use exact agent name from profile
- Try issue template workflow instead (see [ISSUE_TEMPLATES_GUIDE.md](../../docs/HOW_TO_USE/ISSUE_TEMPLATES_GUIDE.md))

---

**Last Updated:** 2025-11-22  
**Maintainer:** Synthesizer Sam  
**Status:** Active

