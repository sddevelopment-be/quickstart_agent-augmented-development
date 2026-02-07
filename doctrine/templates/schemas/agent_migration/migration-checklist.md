# Agent Schema Migration Checklist

**Document Type:** Migration Guide  
**Version:** 1.0.0  
**Date:** 2026-01-29  
**Author:** Architect Alphonso  
**Audience:** Agent Authors, Contributors  
**Related Documents:**

- `docs/schemas/schema-conventions.md` (Schema Conventions)
- `docs/schemas/agent-schema-template.json` (Schema Template)
- `docs/technical/ir-structure.md` (IR Specification)

---

## Overview

This checklist guides you through adding input/output schemas to existing agent profiles. Follow these steps to ensure consistent, valid schemas that integrate smoothly with the export pipeline.

**Estimated Time:** 30-90 minutes per agent (depending on complexity)

**Prerequisites:**

- Agent profile exists (agent profile files)
- Familiarity with JSON Schema basics
- Access to schema conventions and template

---

## Pre-Migration

### 1. Read Schema Conventions

**Time:** 15 minutes

- [ ] Read `docs/schemas/schema-conventions.md` in full
- [ ] Understand the 5 key decisions (location, extraction, format, validation, compatibility)
- [ ] Review decision tree for frontmatter vs. separate file
- [ ] Bookmark FAQ section for reference

**Resources:**

- Schema conventions: `docs/schemas/schema-conventions.md`
- JSON Schema documentation: <https://json-schema.org/draft-07/schema>

---

### 2. Analyze Your Agent

**Time:** 10 minutes

Understand what your agent consumes and produces:

- [ ] Open agent profile: `agents/[your-agent].agent.md`
- [ ] Read **Section 4: Collaboration Contract**
  - Note: What does this agent expect to receive?
  - Note: What parameters are mentioned?
- [ ] Read **Section 4: Output Artifacts**
  - List: All artifact types produced
  - Note: File formats and metadata
- [ ] Read **Section 5: Operating Procedure** (if present)
  - Note: Configuration options
  - Note: Modes or flags

**Output:** Notes on inputs and outputs

---

### 3. Review Similar Agents

**Time:** 10 minutes

Find patterns from agents with similar roles:

- [ ] Identify 2-3 agents with similar responsibilities
- [ ] Review their IR examples in `work/schemas/examples/ir/`
  - What input patterns do they use?
  - What output structures do they have?
- [ ] Note common patterns to reuse

**Similar Agents:**

- **Architecture:** Architect Alphonso, Diagrammer Dave
- **Backend:** Backend Benny, Build Automation
- **Content:** Curator Claire, Lexical Lex, Scribe Sienna
- **Review:** Reviewer Rachel, Editor Eddy
- **Planning:** Planning Petra, Project Manager

---

### 4. Decide: Frontmatter or Separate File?

**Time:** 5 minutes

Use the decision tree from conventions:

```
Is schema >5 root properties? → YES → Separate file
Has nesting >2 levels deep? → YES → Separate file
Is schema reused by others? → YES → Separate file
Likely to change frequently? → YES → Separate file
Otherwise → Frontmatter
```

- [ ] Count root-level properties in your input/output
- [ ] Check nesting depth
- [ ] Decide: ☐ Frontmatter ☐ Separate file
- [ ] Document decision in notes

**Decision:** _______________________

---

## Migration Steps

### 5. Create Input Schema

**Time:** 20-30 minutes

#### Option A: Frontmatter Input Schema

- [ ] Open agent file in editor
- [ ] Add `inputs:` field to YAML frontmatter
- [ ] Define schema inline using YAML

**Example:**

```yaml
---
name: my-agent
description: My agent description
tools: ["read", "write"]
inputs:
  type: object
  properties:
    task_id:
      type: string
      description: Unique task identifier
      pattern: "^[a-z0-9-]+$"
    priority:
      type: string
      enum: [LOW, MEDIUM, HIGH, CRITICAL]
      default: MEDIUM
  required: [task_id]
---
```

#### Option B: Separate Input Schema File

- [ ] Create file: `docs/schemas/[agent-name].input.schema.json`
- [ ] Copy template from `docs/schemas/agent-schema-template.json`
- [ ] Update `$id` field with your schema URL
- [ ] Update `title` and `description`
- [ ] Define input properties
- [ ] Reference from agent frontmatter

**Agent frontmatter:**

```yaml
---
name: my-agent
inputs: "file://schemas/my-agent.input.schema.json"
---
```

**Schema file structure:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://example.com/schemas/my-agent.input.schema.json",
  "title": "My Agent Input",
  "type": "object",
  "properties": {
    // Define properties here
  },
  "required": []
}
```

#### Input Schema Checklist

- [ ] All input parameters from narrative documented
- [ ] Property names use `snake_case`
- [ ] Each property has `type` and `description`
- [ ] Required fields listed in `required` array
- [ ] Enums defined for fixed value sets
- [ ] Patterns defined for string formats
- [ ] Examples added for complex properties
- [ ] Defaults specified where applicable

---

### 6. Create Output Schema

**Time:** 20-30 minutes

Follow same process as input schema.

#### Common Output Properties

Include these standard properties:

- [ ] `task_id` (string, required)
- [ ] `status` (enum: success/partial/failed, required)
- [ ] `artifacts` (array of objects, required)
  - [ ] Each artifact has `path`, `type`
  - [ ] Optional: `hash`, `size_bytes`, `format`
- [ ] `metrics` (object, optional)
  - [ ] `duration_seconds`
  - [ ] `coverage_percent`
  - [ ] `quality_score`
- [ ] `warnings` (array, optional)
- [ ] `errors` (array, optional)
- [ ] `work_log` (string path, optional)
- [ ] `notes` (string, optional)

#### Output Schema Checklist

- [ ] All output artifacts from narrative documented
- [ ] Standard properties included
- [ ] Property names use `snake_case`
- [ ] Each property has `type` and `description`
- [ ] Required fields listed in `required` array
- [ ] Artifact structure matches template
- [ ] Examples added for complex properties

---

### 7. Validate Schema Syntax

**Time:** 5 minutes

- [ ] Run syntax validation: `npm run validate:schema -- agents/[agent].agent.md`
- [ ] Fix any JSON Schema syntax errors
- [ ] Verify all `$ref` references resolve
- [ ] Check for typos in property names

**Common Syntax Errors:**

- Missing commas in JSON
- Incorrect `$ref` paths
- Invalid regex patterns
- Misspelled keywords (`reqiured` → `required`)

---

### 8. Test Schema with Sample Data

**Time:** 10 minutes

- [ ] Create sample input: `tests/fixtures/[agent]-input-sample.json`
- [ ] Create sample output: `tests/fixtures/[agent]-output-sample.json`
- [ ] Validate samples against schemas
- [ ] Verify validation passes for valid data
- [ ] Verify validation fails for invalid data

**Test Commands:**

```bash
# Test input schema
npm run schema:test -- docs/schemas/[agent].input.schema.json tests/fixtures/[agent]-input-sample.json

# Test output schema
npm run schema:test -- docs/schemas/[agent].output.schema.json tests/fixtures/[agent]-output-sample.json
```

---

### 9. Update Agent Narrative

**Time:** 10 minutes

Ensure narrative aligns with schema:

- [ ] Review **Collaboration Contract** section
  - Does it mention all input parameters?
  - Are parameter descriptions consistent with schema?
- [ ] Review **Output Artifacts** section
  - Are all artifact types listed?
  - Do descriptions match schema?
- [ ] Add note about schema location (if separate file)

**Example note:**

```markdown
### Input/Output Schemas

Input and output schemas are defined in:
- `docs/schemas/my-agent.input.schema.json`
- `docs/schemas/my-agent.output.schema.json`

See schema conventions: `docs/schemas/schema-conventions.md`
```

---

### 10. Create Work Log

**Time:** 10 minutes

Document your migration:

- [ ] Create work log: `work/reports/logs/[agent]/[date]-schema-migration.md`
- [ ] Document decisions made
  - Why frontmatter vs. separate file?
  - Any deviations from conventions?
- [ ] List challenges encountered
- [ ] Note any ambiguities in original narrative

**Work Log Template:**

```markdown
# Work Log: Schema Migration for [Agent Name]

**Date:** YYYY-MM-DD  
**Agent:** [Agent Name]  
**Task:** Add input/output schemas per schema conventions

## Decisions

- **Schema Location:** [Frontmatter / Separate file]
  - Rationale: [Reason]
- **Deviations:** [None / List any deviations]

## Input Schema

- **Properties:** [Count]
- **Required Fields:** [List]
- **Notes:** [Any special considerations]

## Output Schema

- **Properties:** [Count]
- **Required Fields:** [List]
- **Artifact Types:** [List]

## Challenges

- [Challenge 1 and resolution]
- [Challenge 2 and resolution]

## Validation

- [x] Schema syntax valid
- [x] Sample data validates
- [x] Narrative updated
- [x] No conflicts with conventions

## Time Spent

**Estimated:** 60 minutes  
**Actual:** [Actual time]
```

---

## Post-Migration

### 11. Commit Changes

**Time:** 5 minutes

- [ ] Stage changes: `git add agents/[agent].agent.md docs/schemas/`
- [ ] Commit with descriptive message
- [ ] Include schema files if separate
- [ ] Include work log

**Commit Message Template:**

```
feat(schema): Add input/output schemas for [agent-name]

- Define input schema with [N] properties
- Define output schema with [M] properties
- Schema location: [frontmatter/separate file]
- Add work log documenting migration

Relates to: Task 1.3 (Schema Conventions)
```

---

### 12. Request Review

**Time:** Variable

- [ ] Create PR with schema changes
- [ ] Tag reviewers: Architect Alphonso, Backend Benny
- [ ] Request validation check
- [ ] Address review feedback

**PR Description Template:**

```markdown
## Schema Migration: [Agent Name]

**Agent:** [agent-name]  
**Schema Type:** [Frontmatter / Separate files]  
**Complexity:** [Simple / Medium / Complex]

### Changes

- Added input schema with [N] properties
- Added output schema with [M] properties
- Updated agent narrative for consistency

### Validation

- [x] Schema syntax valid
- [x] Sample data validates
- [x] Conventions followed
- [x] Work log created

### Reviewers

- [ ] @architect-alphonso (schema conventions)
- [ ] @backend-benny (integration feasibility)

### Related

- Task: mfd-task-1.3-schema-conventions
- Conventions: docs/schemas/schema-conventions.md
```

---

## Validation Checklist

Use this final checklist before submitting:

### Schema Quality

- [ ] Property names use `snake_case` consistently
- [ ] All properties have `type` and `description`
- [ ] Required fields marked in `required` array
- [ ] Enums defined for fixed value sets
- [ ] Patterns defined for string formats (kebab-case, hashes, etc.)
- [ ] Ranges defined for numbers (`minimum`, `maximum`)
- [ ] Examples provided for complex properties
- [ ] Defaults specified where applicable
- [ ] No `additionalProperties` unless intentional

### Schema Structure

- [ ] Follows template structure
- [ ] Uses `$ref` for reusable types
- [ ] Includes standard output properties (task_id, status, artifacts)
- [ ] Artifact structure matches template
- [ ] Metrics structure matches template (if used)

### Documentation

- [ ] Schema has `title` and `description`
- [ ] Complex properties explained
- [ ] Examples demonstrate valid usage
- [ ] Deviations from conventions documented

### Integration

- [ ] Schema location decision documented
- [ ] Agent narrative consistent with schema
- [ ] Work log created
- [ ] Sample data validates successfully

### Validation Commands

- [ ] `npm run validate:schema` passes
- [ ] `npm run schema:test` passes with samples
- [ ] CI/CD validation passes

---

## Common Pitfalls and Solutions

### Pitfall 1: Missing Descriptions

**Problem:** Properties lack descriptions

**Solution:**

```json
// ❌ Bad
"task_id": {
  "type": "string"
}

// ✅ Good
"task_id": {
  "type": "string",
  "description": "Unique identifier for the task in kebab-case format",
  "pattern": "^[a-z0-9-]+$",
  "examples": ["mfd-task-1.3-schema"]
}
```

---

### Pitfall 2: Inconsistent Naming

**Problem:** Mixing naming conventions

**Solution:**

```json
// ❌ Bad
{
  "taskID": "...",       // camelCase
  "task-name": "...",    // kebab-case
  "task_description": "..." // snake_case
}

// ✅ Good
{
  "task_id": "...",
  "task_name": "...",
  "task_description": "..."
}
```

---

### Pitfall 3: Over-Specification

**Problem:** Making everything required

**Solution:**

```json
// ❌ Bad - Everything required
{
  "required": [
    "task_id", "task_description", "priority", 
    "deadline", "mode", "context_files", "dependencies"
  ]
}

// ✅ Good - Only essentials required
{
  "required": ["task_id", "task_description"]
}
```

---

### Pitfall 4: Missing Constraints

**Problem:** No validation constraints

**Solution:**

```json
// ❌ Bad
"priority": {
  "type": "string"
}

// ✅ Good
"priority": {
  "type": "string",
  "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
  "default": "MEDIUM"
}
```

---

### Pitfall 5: Deep Nesting Without $ref

**Problem:** Complex nested structures inline

**Solution:**

```json
// ❌ Bad - Deep inline nesting
{
  "artifacts": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "path": {"type": "string"},
        "metadata": {
          "type": "object",
          "properties": {
            "hash": {"type": "string"},
            "size": {"type": "integer"}
          }
        }
      }
    }
  }
}

// ✅ Good - Use definitions
{
  "definitions": {
    "Artifact": {
      "type": "object",
      "properties": {
        "path": {"type": "string"},
        "metadata": {"$ref": "#/definitions/Metadata"}
      }
    },
    "Metadata": {
      "type": "object",
      "properties": {
        "hash": {"type": "string"},
        "size": {"type": "integer"}
      }
    }
  },
  "properties": {
    "artifacts": {
      "type": "array",
      "items": {"$ref": "#/definitions/Artifact"}
    }
  }
}
```

---

### Pitfall 6: Schema-Narrative Drift

**Problem:** Schema doesn't match agent description

**Solution:**

1. Review agent narrative sections
2. List all mentioned inputs and outputs
3. Compare with schema properties
4. Update schema or narrative to align
5. Document in work log

---

## Quick Reference

### Validation Commands

```bash
# Validate single agent schema
npm run validate:schema -- agents/[agent].agent.md

# Validate all agent schemas
npm run validate:schemas

# Test schema with sample data
npm run schema:test -- [schema-file] [data-file]

# Generate schema stub (helper)
npm run schema:stub -- agents/[agent].agent.md
```

### File Locations

- **Agent profiles:** agent profile files
- **Schema files:** `docs/schemas/[agent-name].{input|output}.schema.json`
- **Common schemas:** `docs/schemas/common/*.schema.json`
- **Work logs:** `work/reports/logs/[agent]/[date]-schema-migration.md`
- **Sample data:** `tests/fixtures/[agent]-{input|output}-sample.json`

### Resources

- **Conventions:** `docs/schemas/schema-conventions.md`
- **Template:** `docs/schemas/agent-schema-template.json`
- **IR Spec:** `docs/technical/ir-structure.md`
- **JSON Schema Docs:** <https://json-schema.org/draft-07/schema>

---

## Success Criteria

You've successfully migrated your agent schema when:

- ✅ Schema validates without errors
- ✅ Sample data validates against schema
- ✅ Agent narrative consistent with schema
- ✅ Follows naming and structure conventions
- ✅ Work log documents decisions
- ✅ CI/CD checks pass
- ✅ Review approved by team

---

## Next Steps

After migrating one agent:

1. **Reflect:** What worked well? What was challenging?
2. **Improve:** Update this checklist with lessons learned
3. **Share:** Help others with similar agents
4. **Iterate:** Apply to remaining agents

---

**Document Status:** ✅ Ready for Use  
**Last Updated:** 2026-01-29  
**Feedback:** Submit improvements to Architect Alphonso
