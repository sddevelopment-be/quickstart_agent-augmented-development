# Claude Prompts

Task-specific prompt templates for Claude Code integration.

## Overview

This directory contains 13 prompt templates for common development tasks.

## Available Prompts

### Markdown Templates (.prompt.md)

#### ARCHITECT_ADR
**File:** `ARCHITECT_ADR.prompt.md`

#### AUTOMATION_SCRIPT
**File:** `AUTOMATION_SCRIPT.prompt.md`

#### BOOTSTRAP_REPO
**File:** `BOOTSTRAP_REPO.prompt.md`

#### CURATE_DIRECTORY
**File:** `CURATE_DIRECTORY.prompt.md`

#### EDITOR_REVISION
**File:** `EDITOR_REVISION.prompt.md`

#### LEXICAL_ANALYSIS
**File:** `LEXICAL_ANALYSIS.prompt.md`

#### NEW_AGENT
Prompt to request creation of a new specialized agent (Manager Mike runs it)

**Agent:** manager-mike  
**Category:** agent-management  
**File:** `NEW_AGENT.prompt.md`

#### TEST_READABILITY_CHECK
**File:** `TEST_READABILITY_CHECK.prompt.md`

### YAML Templates (.yaml)

#### architecture-decision
**File:** `architecture-decision.yaml`

#### assessment
**File:** `assessment.yaml`

#### bug-fix
**File:** `bug-fix.yaml`

#### documentation
**File:** `documentation.yaml`

#### task-execution
**File:** `task-execution.yaml`


## Usage

These prompts can be used:
1. **Direct execution** - Copy and fill in template variables
2. **Agent context** - Reference in agent workflows
3. **Tool integration** - Import into Claude Code or other AI tools

## Format

- **Markdown templates** (.prompt.md): Include frontmatter with metadata and structured instructions
- **YAML templates** (.yaml): Structured format with sections, inputs, outputs, and constraints

## Manifest

See `manifest.json` for structured metadata including prompt IDs, types, agents, and categories.

---
*Generated: 2026-02-10T11:42:31.714Z*
