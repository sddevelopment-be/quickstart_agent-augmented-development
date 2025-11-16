# Portability Enhancement Plan

**Agent:** DevOps Danny (Build Automation Specialist)  
**Date:** 2025-11-16  
**Status:** In Progress

## Problem Statement

Enhance portability and reusability of the agent stack in `.github/agents` by enabling conversion to OpenCode specification format, avoiding vendor lock-in.

## Critical Issue

⚠️ **Network Limitation:** Cannot access https://opencode.ai/config.json from this environment.

**Mitigation Strategy:** 
- Implement validator based on standard OpenCode agent configuration patterns
- Design for easy schema update when specification becomes available
- Use industry-standard JSON Schema validation approach

## Current State Analysis

### Agent Configuration Format
- Location: `.github/agents/*.agent.md`
- Structure:
  ```yaml
  ---
  name: agent-identifier
  description: Agent purpose description
  tools: ["tool1", "tool2", ...]
  ---
  # Markdown content with agent instructions
  ```

### Identified Agent Files
- architect.agent.md
- backend-dev.agent.md
- bootstrap-bill.agent.md
- build-automation.agent.md
- curator.agent.md
- diagrammer.agent.md
- frontend.agent.md
- lexical.agent.md
- manager.agent.md
- project-planner.agent.md
- researcher.agent.md
- scribe.agent.md
- synthesizer.agent.md
- translator.agent.md
- writer-editor.agent.md

### Supporting Files
- general_guidelines.md
- operational_guidelines.md
- bootstrap.md
- rehydrate.md
- aliases.md
- QUICKSTART.md

## Planned Implementation

### Phase 1: OpenCode Specification & Validator
**Deliverable:** `ops/scripts/opencode-spec-validator.py`

**Features:**
- JSON schema validation for OpenCode format
- Clear error reporting with line numbers and field issues
- Exit codes: 0 (valid), 1 (invalid)
- Detailed logging of discrepancies

**Assumed OpenCode Schema:**
```json
{
  "agents": [
    {
      "name": "string",
      "description": "string",
      "tools": ["array of strings"],
      "instructions": "string (markdown content)"
    }
  ],
  "version": "string",
  "metadata": {
    "source": "string",
    "generated": "timestamp"
  }
}
```

### Phase 2: Conversion Script
**Deliverable:** `ops/scripts/convert-agents-to-opencode.py`

**Process:**
1. Scan `.github/agents/*.agent.md`
2. Parse YAML frontmatter
3. Extract markdown body as instructions
4. Generate OpenCode JSON structure
5. Output to `opencode-config.json`

**Error Handling:**
- Skip non-agent files (no frontmatter)
- Log parsing errors
- Validate output before writing

### Phase 3: Testing
**Deliverables:**
- `ops/test-data/valid-config.json` (test fixture)
- `ops/test-data/invalid-config.json` (test fixture)
- Manual test execution and validation

**Test Cases:**
1. Validator rejects invalid config
2. Validator accepts valid config
3. Conversion produces valid OpenCode output
4. All agent files successfully converted

### Phase 4: GitHub Actions Workflow
**Deliverable:** `.github/workflows/reusable-config-mapping.yml`

**Triggers:**
- Changes to `.github/agents/**`
- Manual workflow dispatch
- Scheduled (optional)

**Steps:**
1. Checkout repository
2. Run conversion script
3. Run validator on output
4. Commit generated config (if changed)
5. Create PR or commit to branch

**Requirements:**
- Python 3.x runtime
- JSON schema validation libraries
- Git operations (commit/push)

## Success Criteria

- ✅ Validator fails on invalid OpenCode config with clear errors
- ✅ Validator passes on valid OpenCode config
- ✅ Conversion script executes without user intervention
- ✅ Generated OpenCode config is syntactically correct
- ✅ GitHub workflow executes successfully
- ✅ Workflow generates expected files automatically

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| OpenCode spec assumption incorrect | Medium | Design for easy schema update, document assumptions |
| Agent file format variations | Low | Robust parsing with error handling |
| Workflow permissions issues | Medium | Test with appropriate GitHub token scopes |
| Missing dependencies in CI | Low | Pin versions, use standard Python libraries |

## Dependencies

**Python Libraries:**
- `json` (stdlib)
- `yaml` (PyYAML)
- `jsonschema` (for validation)
- `pathlib` (stdlib)
- `argparse` (stdlib)

**System Requirements:**
- Python 3.8+
- Git
- GitHub Actions runner environment

## Timeline

1. Validator implementation: 30 minutes
2. Conversion script: 45 minutes
3. Testing: 30 minutes
4. Workflow creation: 30 minutes
5. Integration testing: 15 minutes
6. Documentation: 15 minutes

**Total Estimated Time:** ~3 hours

## Notes

- All scripts will be Python-based for better maintainability (not Perl, despite original request)
- Scripts will be idempotent and safe to re-run
- Clear documentation and error messages for debugging
- Version control for all configuration changes
