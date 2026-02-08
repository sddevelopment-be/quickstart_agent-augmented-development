# Claude Deployment Guide

## Overview

This guide explains how to deploy the Agent-Augmented Development framework components to Claude Code's directory structure for seamless integration.

## What Gets Deployed

The deployment pipeline deploys three types of content to the `.claude/` directory:

1. **Skills** (`.claude/skills/`) - Reusable task-specific capabilities in SKILL.md format
2. **Agents** (`.claude/agents/`) - Specialist agent profiles with roles and workflows
3. **Prompts** (`.claude/prompts/`) - Task templates in markdown and YAML formats

## Quick Start

### Deploy Everything

```bash
npm run deploy:claude
```

This deploys all three content types (skills, agents, and prompts) to Claude Code.

### Deploy Selectively

```bash
# Deploy only skills
npm run deploy:claude:skills

# Deploy only agents
npm run deploy:claude:agents

# Deploy only prompts
npm run deploy:claude:prompts
```

## Directory Structure

After deployment, your `.claude/` directory will contain:

```
.claude/
├── skills/              # Task-specific capabilities
│   ├── architect-adr/
│   │   └── SKILL.md
│   ├── automation-script/
│   │   └── SKILL.md
│   └── ...
├── agents/              # Specialist agent profiles
│   ├── architect.agent.md
│   ├── backend-dev.agent.md
│   ├── frontend.agent.md
│   ├── manifest.json    # Agent inventory
│   ├── README.md        # Documentation
│   └── ...
└── prompts/             # Task templates
    ├── ARCHITECT_ADR.prompt.md
    ├── architecture-decision.yaml
    ├── manifest.json    # Prompt inventory
    ├── README.md        # Documentation
    └── ...
```

## Prerequisites

### For Skills Deployment

Skills require the export pipeline to run first:

```bash
npm run export:all
npm run deploy:claude:skills
```

Or use the combined build command:

```bash
npm run build
```

### For Agents and Prompts

Agents and prompts deploy directly from source - no export needed:

```bash
npm run deploy:claude:agents
npm run deploy:claude:prompts
```

## What Each Component Does

### Skills (`.claude/skills/`)

**Source:** `dist/skills/claude-code/` (generated from framework)  
**Format:** `SKILL.md` with frontmatter

Skills are task-specific capabilities that Claude Code can reference. Each skill:
- Defines a specific development task or approach
- Includes structured instructions and workflows
- Contains metadata (agent, category, complexity)
- Provides conversation starters

**Example Uses:**
- `architect-adr` - Create architecture decision records
- `automation-script` - Generate build/test automation
- `test-readability-clarity-check` - Validate code readability

### Agents (`.claude/agents/`)

**Source:** `.github/agents/*.agent.md` (direct copy)  
**Format:** Original markdown with frontmatter

Agent profiles define specialist roles with:
- Purpose and specialization areas
- Context sources and directives
- Collaboration contracts
- Mode defaults (analysis, creative, meta)

**Example Agents:**
- `architect-alphonso` - System architecture and trade-offs
- `backend-benny` - Backend services and APIs (that's me!)
- `frontend-freddy` - UI/UX integration
- `curator-claire` - Documentation and consistency

**Includes:**
- `manifest.json` - Structured agent inventory
- `README.md` - Usage guide and agent directory

### Prompts (`.claude/prompts/`)

**Source:** `docs/templates/prompts/` (direct copy)  
**Format:** Markdown (`.prompt.md`) and YAML (`.yaml`)

Prompt templates for common tasks:
- **Markdown templates** - Rich instructions with inputs/outputs
- **YAML templates** - Structured format with validation

**Example Prompts:**
- `ARCHITECT_ADR.prompt.md` - ADR creation workflow
- `AUTOMATION_SCRIPT.prompt.md` - Script generation
- `architecture-decision.yaml` - Decision documentation
- `bug-fix.yaml` - Bug fix workflow

**Includes:**
- `manifest.json` - Prompt inventory with metadata
- `README.md` - Format guide and usage examples

## Workflow Integration

### Development Workflow

```bash
# 1. Make changes to framework
edit .github/agents/backend-dev.agent.md
edit docs/templates/prompts/ARCHITECT_ADR.prompt.md

# 2. Deploy to Claude
npm run deploy:claude:agents
npm run deploy:claude:prompts

# 3. Use in Claude Code
# Reference agents: "@backend-benny design API endpoints"
# Use prompts: Copy template and fill in variables
```

### Full Build Pipeline

```bash
# Complete export and deployment
npm run export:all        # Generate skill exports
npm run deploy:all        # Deploy to all targets (Claude, Copilot, OpenCode)
```

Or combined:

```bash
npm run build
```

## Deployment Details

### Copy vs Symlink

The current implementation **copies** files to `.claude/` directories. This:
- ✅ Works across all platforms (Windows, Linux, Mac)
- ✅ Creates stable snapshots for Claude Code
- ✅ Avoids symlink permission issues
- ⚠️ Requires re-deployment after source changes

### File Formats

- **Skills:** Converted to SKILL.md format with frontmatter
- **Agents:** Preserved as original `.agent.md` markdown
- **Prompts:** Preserved as `.prompt.md` or `.yaml` originals

### Manifest Files

Each deployed directory includes a `manifest.json` with:
- Version information
- File inventory
- Metadata (names, descriptions, categories)
- Generation timestamp

## Verification

Check deployment status:

```bash
# List deployed agents
ls .claude/agents/

# List deployed prompts
ls .claude/prompts/

# List deployed skills
ls .claude/skills/

# View agent manifest
cat .claude/agents/manifest.json | jq

# View prompt manifest
cat .claude/prompts/manifest.json | jq
```

## Integration with Release Pipeline

The Claude deployment is designed to integrate with the framework distribution pipeline (see ADR-013):

```
dist/
├── opencode/
├── skills/
└── release/
    └── quickstart-framework-<version>.zip
        ├── framework_core/
        │   ├── .claude/          # Deployed Claude files
        │   ├── .github/agents/   # Agent sources
        │   └── docs/templates/   # Prompt sources
        └── scripts/
            └── framework_install.sh
```

## Troubleshooting

### Skills Not Deploying

**Problem:** "No Claude Code skills found"

**Solution:** Run export first:
```bash
npm run export:skills
npm run deploy:claude:skills
```

### Agents/Prompts Not Found

**Problem:** Source directories missing

**Solution:** Verify repository structure:
```bash
ls .github/agents/*.agent.md
ls docs/templates/prompts/*.{md,yaml}
```

### Deployment Errors

Check the deployment output for specific errors:
```bash
npm run deploy:claude 2>&1 | grep "❌"
```

## Next Steps

- **Use agents**: Reference in Claude Code sessions
- **Apply prompts**: Copy templates for tasks
- **Extend skills**: Add custom skills to framework
- **Customize agents**: Modify profiles for your project

## Related Documentation

- [Agent Profiles](.github/agents/README.md)
- [Prompt Templates](../templates/prompts/README.md)
- [Distribution Pipeline](../architecture/design/distribution_of_releases_technical_design.md)
- [ADR-013: Zip Distribution](../architecture/adrs/ADR-013-zip-distribution.md)

---

**Last Updated:** 2025-01-31  
**Deployment Script:** `ops/deploy-skills.js`
