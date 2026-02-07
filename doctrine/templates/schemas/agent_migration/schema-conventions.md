# Agent Schema Conventions

**Document Type:** Technical Convention  
**Version:** 1.0.0  
**Date:** 2026-01-29  
**Status:** Proposed  
**Author:** Architect Alphonso  
**Audience:** Contributors, Developers, Agent Authors  
**Related Documents:**

- `docs/technical/ir-structure.md` (Intermediate Representation Specification)
- `work/analysis/tech-design-export-pipeline.md` (Export Pipeline Design)
- `work/analysis/ADR-013-multi-format-distribution.md` (Multi-Format Strategy)

---

## Overview

This document defines conventions for defining, extracting, and documenting input/output schemas for agent profiles. These conventions enable validation, tooling support, and consistency across 17+ agents in the multi-format export pipeline.

**Why These Conventions Matter:**

- **Validation:** Schemas enable automated validation of agent inputs/outputs
- **Tooling:** Schema-driven tools can generate boilerplate, validators, and type definitions
- **Consistency:** Standardized schemas improve collaboration and reduce cognitive load
- **Documentation:** Schemas serve as precise, machine-readable specifications
- **Migration:** Clear conventions enable safe evolution of agent definitions

---

## Design Principles

1. **Clarity Over Brevity:** Explicit schemas are better than inferred ones
2. **Progressive Enhancement:** Schemas are optional; agents work without them
3. **Convention Over Configuration:** Follow patterns; deviate with rationale
4. **Backward Compatibility:** New conventions don't break existing agents
5. **Validation at Build Time:** Catch errors early, not at runtime

---

## Key Decisions

### Decision 1: Schema Location

**DECISION:** Use YAML frontmatter for simple schemas, separate JSON files for complex schemas.

**Rationale:**

**Option A: YAML Frontmatter Only**

- ✅ Co-located with agent definition
- ✅ Single file to maintain
- ❌ Large frontmatter becomes unwieldy
- ❌ Harder to validate independently

**Option B: Separate JSON Files**

- ✅ Clean separation of concerns
- ✅ Independent validation
- ❌ Multiple files to maintain
- ❌ Schema-agent sync required

**Option C: Mixed Approach (CHOSEN)**

- ✅ Co-location for simple schemas (frontmatter)
- ✅ Separation for complex schemas (JSON files)
- ✅ Progressive enhancement path
- ⚠️ Requires decision heuristic

**Decision Heuristic:**

Use **frontmatter** when:

- Schema has ≤5 properties at root level
- No deeply nested structures (≤2 levels)
- Properties are simple types (string, boolean, number, array of strings)
- Schema is stable and unlikely to be reused

Use **separate JSON files** when:

- Schema has >5 properties at root level
- Complex nested structures (>2 levels deep)
- Contains reusable type definitions
- Shared across multiple agents
- Benefits from independent validation

**Implementation:**

```yaml
# Simple schema in frontmatter
---
name: simple-agent
inputs:
  type: object
  properties:
    task_id:
      type: string
      description: Unique task identifier
    priority:
      type: string
      enum: [LOW, MEDIUM, HIGH]
  required: [task_id]
outputs:
  type: object
  properties:
    result:
      type: string
---
```

```yaml
# Complex schema via reference
---
name: complex-agent
inputs: "file://schemas/complex-agent.input.schema.json"
outputs: "file://schemas/complex-agent.output.schema.json"
---
```

**Trade-offs:**

- ✅ Flexibility for simple and complex cases
- ⚠️ Introduces decision point (use checklist above)
- ⚠️ Requires schema file management for complex cases

---

### Decision 2: Schema Extraction Strategy

**DECISION:** Manual schema authoring with parser-assisted validation.

**Rationale:**

**Option A: Fully Manual**

- ✅ Maximum control
- ✅ Human insight captures nuance
- ❌ Time-consuming
- ❌ Inconsistent quality

**Option B: Semi-Automated (CHOSEN)**

- ✅ Human authoring ensures quality
- ✅ Parser validates structure
- ✅ Tools suggest missing fields
- ⚠️ Requires validation tooling

**Option C: Fully Automated**

- ✅ Fast
- ❌ Loses context and intent
- ❌ Cannot infer semantics from narrative
- ❌ Requires perfect source structure

**Implementation:**

1. **Manual Phase:** Agent author writes schema based on narrative content
2. **Validation Phase:** Parser validates schema against JSON Schema Draft 7
3. **Suggestion Phase:** Parser identifies potential missing fields from narrative
4. **Review Phase:** Author refines based on suggestions

**Extraction Heuristics:**

When inferring schemas from narrative:

1. **Inputs:** Examine "Collaboration Contract" and "Operating Procedure"
   - Look for required parameters
   - Identify configuration options
   - Note file paths, modes, flags

2. **Outputs:** Examine "Output Artifacts" section
   - List all artifact types
   - Identify file formats
   - Note metadata requirements

3. **Examples:** Extract from existing IR instances
   - Review `work/schemas/examples/ir/*.ir.json`
   - Identify common patterns
   - Reuse established type definitions

**Trade-offs:**

- ✅ Balances speed and quality
- ✅ Leverages human insight
- ⚠️ Requires initial manual effort
- ⚠️ Tooling dependency for validation

---

### Decision 3: Schema Format

**DECISION:** Use JSON Schema Draft 7 with conventions for naming and constraints.

**Rationale:**

- JSON Schema Draft 7 is mature, widely supported, and well-documented
- Compatible with existing validation tools
- Supports rich constraints (enums, patterns, ranges)
- Extensible for custom metadata

**Property Naming Convention:** `snake_case`

**Rationale:**

- Consistent with frontmatter fields (`last_updated`, `api_version`)
- Readable and unambiguous
- Compatible with YAML and JSON
- Avoids camelCase/kebab-case confusion

**Required vs. Optional Fields:**

Mark fields as **required** when:

- Field is essential for agent operation
- Absence would cause agent to fail or produce invalid output
- No reasonable default value exists

Mark fields as **optional** when:

- Field has a sensible default
- Agent can function without it
- Field is contextual or environment-specific

**Constraints:**

Always define constraints when known:

- `enum` for fixed value sets
- `pattern` for string formats (e.g., `^[a-z0-9-]+$` for kebab-case)
- `minimum`, `maximum` for numeric ranges
- `minItems`, `maxItems` for arrays

**Annotations:**

Include rich annotations:

- `title`: Human-readable name
- `description`: Detailed explanation (1-2 sentences)
- `examples`: Concrete example values
- `default`: Default value if applicable

**Example:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://example.com/schemas/agent-input.schema.json",
  "title": "Agent Input Schema",
  "description": "Common input schema for agent task definitions",
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "title": "Task Identifier",
      "description": "Unique identifier for the task in kebab-case format",
      "pattern": "^[a-z0-9-]+$",
      "examples": ["mfd-task-1.3-schema-conventions"]
    },
    "priority": {
      "type": "string",
      "title": "Task Priority",
      "description": "Priority level determining execution order",
      "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
      "default": "MEDIUM"
    },
    "estimated_effort_hours": {
      "type": "number",
      "title": "Estimated Effort",
      "description": "Estimated hours to complete task",
      "minimum": 0.25,
      "maximum": 40,
      "examples": [1, 2.5, 8]
    }
  },
  "required": ["task_id"],
  "additionalProperties": false
}
```

**Trade-offs:**

- ✅ Industry standard, widely supported
- ✅ Rich constraint vocabulary
- ✅ Good tooling ecosystem
- ⚠️ Verbose for simple cases (mitigated by frontmatter option)

---

### Decision 4: Validation Timing

**DECISION:** Build-time validation with CI/CD enforcement, optional runtime validation.

**Rationale:**

**Option A: Build-Time Only (CHOSEN for CI)**

- ✅ Fail-fast during development
- ✅ Prevents invalid schemas from merging
- ✅ No runtime performance penalty
- ❌ Doesn't catch runtime data issues

**Option B: Runtime Only**

- ✅ Validates actual data
- ❌ Errors discovered too late
- ❌ Performance overhead
- ❌ Harder to debug

**Option C: Both (RECOMMENDED)**

- ✅ Catches schema errors at build time
- ✅ Validates data at runtime
- ✅ Comprehensive coverage
- ⚠️ Requires dual validation setup

**Implementation:**

**Build-Time Validation (Required):**

```bash
# Validate all agent schemas
npm run validate:schemas

# Validate specific agent
npm run validate:schema -- .github/agents/architect.agent.md

# CI/CD integration
# Runs automatically on PR, blocks merge if invalid
```

**Runtime Validation (Optional):**

```javascript
// Generator validates IR against schema before export
const Ajv = require('ajv');
const ajv = new Ajv();
const validate = ajv.compile(schema);

if (!validate(ir)) {
  throw new ValidationError(validate.errors);
}
```

**Validation Workflow:**

1. **Pre-commit:** Validate modified agent schemas (fast feedback)
2. **CI/CD:** Validate all schemas on PR (comprehensive check)
3. **Runtime:** Generators validate IR before export (safety net)

**Trade-offs:**

- ✅ Layered validation catches errors early and late
- ✅ Build-time validation has zero runtime cost
- ⚠️ Requires CI/CD configuration
- ⚠️ Runtime validation adds complexity

---

### Decision 5: Backward Compatibility

**DECISION:** Schemas are optional; phased adoption with graceful degradation.

**Rationale:**

**Option A: Schemas Required**

- ✅ Forces standardization
- ❌ Breaks all existing agents
- ❌ High migration cost

**Option B: Schemas Optional (CHOSEN)**

- ✅ Zero breaking changes
- ✅ Incremental adoption
- ✅ Graceful degradation
- ⚠️ Partial coverage during transition

**Option C: Phased (schemas optional → required)**

- ✅ Smooth transition
- ✅ Clear timeline
- ⚠️ Requires enforcement mechanism

**Implementation:**

**Phase 1: Optional (Current)**

- Schemas are opt-in
- Parser works without schemas
- Generators handle missing schemas gracefully
- Documentation encourages schema adoption

**Phase 2: Encouraged (3 months)**

- New agents should include schemas
- Migration guide available
- Tooling to generate schema stubs
- Review process checks for schemas

**Phase 3: Required (6+ months)**

- All agents must have schemas
- CI/CD enforces schema presence
- Parser emits warnings for missing schemas
- Deprecation notices in docs

**Graceful Degradation:**

```javascript
// Parser handles missing schemas
function parseAgent(file) {
  const ir = parseMarkdown(file);
  
  if (ir.frontmatter.inputs) {
    // Schema present, validate
    validateSchema(ir.frontmatter.inputs);
  } else {
    // Schema absent, emit warning, continue
    console.warn(`No input schema for ${ir.frontmatter.name}`);
  }
  
  return ir;
}
```

**Trade-offs:**

- ✅ Zero breaking changes
- ✅ Smooth adoption curve
- ⚠️ Temporary inconsistency across agents
- ⚠️ Requires tracking adoption progress

---

## Schema Structure

### Input Schema Template

Inputs define what an agent receives to perform a task.

**Common Input Patterns:**

1. **Task Definition:** task_id, priority, deadline, dependencies
2. **Configuration:** mode, strictness_level, output_format
3. **Context:** file_paths, related_artifacts, constraints
4. **Parameters:** agent-specific settings

**Example Input Schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Task Input",
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "description": "Unique task identifier",
      "pattern": "^[a-z0-9-]+$"
    },
    "task_description": {
      "type": "string",
      "description": "Human-readable task description"
    },
    "priority": {
      "type": "string",
      "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
      "default": "MEDIUM"
    },
    "mode": {
      "type": "string",
      "description": "Reasoning mode",
      "enum": ["/analysis-mode", "/creative-mode", "/meta-mode"],
      "default": "/analysis-mode"
    },
    "dependencies": {
      "type": "array",
      "description": "Task IDs that must complete before this task",
      "items": {
        "type": "string"
      }
    },
    "context_files": {
      "type": "array",
      "description": "Relevant files for task context",
      "items": {
        "type": "string"
      }
    }
  },
  "required": ["task_id", "task_description"]
}
```

### Output Schema Template

Outputs define what an agent produces upon task completion.

**Common Output Patterns:**

1. **Artifacts:** File paths, content, metadata
2. **Status:** success, warnings, errors
3. **Metrics:** duration, coverage, quality scores
4. **Results:** Agent-specific outcomes

**Example Output Schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Task Output",
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "description": "Task identifier (matches input)"
    },
    "status": {
      "type": "string",
      "enum": ["success", "partial", "failed"],
      "description": "Task completion status"
    },
    "artifacts": {
      "type": "array",
      "description": "Files or documents produced",
      "items": {
        "type": "object",
        "properties": {
          "path": {
            "type": "string",
            "description": "File path relative to repo root"
          },
          "type": {
            "type": "string",
            "description": "Artifact type",
            "examples": ["ADR", "test", "code", "diagram"]
          },
          "hash": {
            "type": "string",
            "description": "SHA-256 hash of artifact"
          }
        },
        "required": ["path", "type"]
      }
    },
    "metrics": {
      "type": "object",
      "properties": {
        "duration_seconds": {
          "type": "number",
          "minimum": 0
        },
        "coverage_percent": {
          "type": "number",
          "minimum": 0,
          "maximum": 100
        }
      }
    },
    "notes": {
      "type": "string",
      "description": "Additional context or warnings"
    }
  },
  "required": ["task_id", "status", "artifacts"]
}
```

---

## Edge Cases and Decision Tree

### When to Deviate from Conventions

Deviate with documented rationale when:

1. **Legacy Compatibility:** Existing format conflicts with conventions
2. **Performance Critical:** Schema overhead impacts runtime
3. **External Standards:** Third-party format has different conventions
4. **Experimental Features:** Testing new patterns before standardization

**Document deviations in schema comments:**

```json
{
  "x-deviation": {
    "reason": "Legacy compatibility with OpenCode format",
    "convention": "snake_case",
    "actual": "camelCase",
    "approved_by": "Architect Alphonso",
    "date": "2026-01-29"
  }
}
```

### Decision Tree: Frontmatter vs. Separate File

```
START: Need to define agent schema

↓
Is schema >5 root properties? 
├─ YES → Use separate JSON file
└─ NO → Continue

↓
Has nesting >2 levels deep?
├─ YES → Use separate JSON file  
└─ NO → Continue

↓
Is schema reused by other agents?
├─ YES → Use separate JSON file
└─ NO → Continue

↓
Is schema likely to change frequently?
├─ YES → Use separate JSON file
└─ NO → Use frontmatter

END: Decision made
```

### Handling Ambiguous Narratives

When agent narrative doesn't clearly specify inputs/outputs:

1. **Review Similar Agents:** Check schemas of agents with similar roles
2. **Examine Output Artifacts Section:** Lists often imply output schema
3. **Check Collaboration Contract:** Often specifies input expectations
4. **Ask Agent Author:** When uncertainty >30%, escalate
5. **Start Minimal:** Define conservative schema, expand iteratively

### Complex Nested Objects

For deeply nested structures:

1. **Use `$ref`:** Reference reusable type definitions
2. **Create Type Library:** Store common types in `docs/schemas/types/`
3. **Flatten When Possible:** Prefer flat structures over deep nesting
4. **Document Structure:** Add ASCII diagrams for complex hierarchies

**Example with `$ref`:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "Artifact": {
      "type": "object",
      "properties": {
        "path": {"type": "string"},
        "type": {"type": "string"}
      },
      "required": ["path", "type"]
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

## FAQ

### Q: What if my agent has no inputs?

**A:** Define a minimal schema or omit it. Document in the agent profile why no inputs are needed.

```yaml
inputs:
  type: "null"
  description: "Agent operates autonomously with no external inputs"
```

### Q: Can I use JSON Schema Draft 2020-12?

**A:** No, use Draft 7 for consistency. Draft 2020-12 has limited tooling support. If you need newer features, document the rationale and ensure validators support it.

### Q: How do I version schemas?

**A:** Include version in `$id` field:

```json
{
  "$id": "https://example.com/schemas/agent-input.v1.schema.json"
}
```

For breaking changes, increment version and maintain old versions.

### Q: What about polymorphic outputs?

**A:** Use `oneOf` or `anyOf`:

```json
{
  "outputs": {
    "oneOf": [
      {"$ref": "#/definitions/SuccessOutput"},
      {"$ref": "#/definitions/ErrorOutput"}
    ]
  }
}
```

### Q: Can I validate YAML with JSON Schema?

**A:** Yes, YAML is a superset of JSON. Parse YAML to JSON, then validate.

### Q: How do I document enums?

**A:** Use `enum` with `description`:

```json
{
  "priority": {
    "type": "string",
    "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
    "description": "Task priority: LOW (backlog), MEDIUM (planned), HIGH (sprint), CRITICAL (urgent)"
  }
}
```

### Q: What if narrative conflicts with schema?

**A:** Schema is authoritative. Update narrative to match schema, or vice versa. Document resolution in work log.

### Q: How granular should schemas be?

**A:** Balance precision and maintainability:

- ✅ Specify required fields and types
- ✅ Add constraints for critical fields
- ⚠️ Avoid over-specifying optional fields
- ❌ Don't specify internal implementation details

### Q: Can agents share schemas?

**A:** Yes, store shared schemas in `docs/schemas/common/`:

```yaml
# Agent A
inputs: "file://schemas/common/task-input.schema.json"

# Agent B  
inputs: "file://schemas/common/task-input.schema.json"
```

---

## Examples

### Example 1: Simple Agent (Frontmatter Schema)

```yaml
---
name: formatter-felix
description: Format code according to style guidelines
tools: ["read", "write", "bash"]
inputs:
  type: object
  properties:
    file_paths:
      type: array
      items:
        type: string
      description: Paths to files to format
    style_guide:
      type: string
      enum: ["google", "airbnb", "standard"]
      default: "standard"
  required: [file_paths]
outputs:
  type: object
  properties:
    formatted_files:
      type: array
      items:
        type: string
      description: Paths to formatted files
    changes_made:
      type: integer
      description: Number of formatting changes
  required: [formatted_files]
---
```

### Example 2: Complex Agent (Separate Schema Files)

```yaml
---
name: reviewer-rachel
description: Quality assurance specialist conducting systematic reviews
tools: ["read", "write", "search"]
inputs: "file://schemas/reviewer-rachel.input.schema.json"
outputs: "file://schemas/reviewer-rachel.output.schema.json"
---
```

**File: `docs/schemas/reviewer-rachel.input.schema.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Reviewer Rachel Input",
  "type": "object",
  "properties": {
    "review_type": {
      "type": "string",
      "enum": ["persona-based", "structural", "editorial", "technical", "comprehensive"],
      "description": "Type of review to conduct"
    },
    "content_paths": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Paths to content to review"
    },
    "rigor_level": {
      "type": "string",
      "enum": ["light", "standard", "comprehensive"],
      "default": "standard"
    },
    "personas": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Persona IDs for persona-based review"
    }
  },
  "required": ["review_type", "content_paths"]
}
```

### Example 3: Shared Type Definitions

**File: `docs/schemas/common/artifact.schema.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://example.com/schemas/common/artifact.schema.json",
  "title": "Artifact Definition",
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "File path relative to repo root"
    },
    "type": {
      "type": "string",
      "description": "Artifact type (ADR, code, diagram, etc.)"
    },
    "hash": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$",
      "description": "SHA-256 hash of artifact content"
    },
    "size_bytes": {
      "type": "integer",
      "minimum": 0,
      "description": "File size in bytes"
    }
  },
  "required": ["path", "type"]
}
```

**Usage in agent schema:**

```json
{
  "properties": {
    "artifacts": {
      "type": "array",
      "items": {"$ref": "file://schemas/common/artifact.schema.json"}
    }
  }
}
```

---

## Validation Commands

### Validate Single Agent

```bash
npm run validate:schema -- .github/agents/architect.agent.md
```

### Validate All Agents

```bash
npm run validate:schemas
```

### Generate Schema Stub

```bash
npm run schema:stub -- .github/agents/new-agent.agent.md
```

### Test Schema Against Sample Data

```bash
npm run schema:test -- docs/schemas/agent.input.schema.json tests/fixtures/sample-input.json
```

---

## Common Pitfalls

### 1. Over-Specifying Optional Fields

**Problem:** Schema is too restrictive, requiring fields that should be optional.

**Solution:** Mark fields as optional unless they're truly required for agent operation.

### 2. Inconsistent Naming

**Problem:** Mixing camelCase, snake_case, kebab-case.

**Solution:** Always use `snake_case` for property names.

### 3. Missing Descriptions

**Problem:** Schema properties lack descriptions, making them hard to understand.

**Solution:** Every property should have a `description` (1-2 sentences).

### 4. No Examples

**Problem:** Abstract schemas without concrete examples.

**Solution:** Add `examples` to complex properties.

### 5. Ignoring Constraints

**Problem:** String fields without patterns, numbers without ranges.

**Solution:** Add constraints (`pattern`, `minimum`, `maximum`, `enum`) when values are constrained.

### 6. Deep Nesting Without `$ref`

**Problem:** Deeply nested schemas that are hard to read and maintain.

**Solution:** Extract nested types into `definitions` and use `$ref`.

### 7. Unclear Required Fields

**Problem:** Missing or incorrect `required` array.

**Solution:** Explicitly list required fields in `required` array.

### 8. Schema-Narrative Drift

**Problem:** Schema diverges from agent narrative over time.

**Solution:** Review schema when updating agent narrative. Document in work log.

---

## Next Steps

1. **Review conventions:** Team review (Architect, Backend Benny, Reviewer Rachel)
2. **Create template:** `docs/schemas/agent-schema-template.json`
3. **Create migration checklist:** `docs/schemas/migration-checklist.md`
4. **Test on sample agent:** Apply conventions to one agent, validate usability
5. **Iterate:** Refine based on feedback
6. **Document:** Update this document with lessons learned

---

## References

- **JSON Schema Draft 7:** <https://json-schema.org/draft-07/schema>
- **JSON Schema Best Practices:** <https://json-schema.org/understanding-json-schema/reference/generic.html>
- **IR Structure:** `docs/technical/ir-structure.md`
- **Export Pipeline:** `work/analysis/tech-design-export-pipeline.md`

---

**Document Status:** ✅ Proposed for Review  
**Next Actions:** Team review, create supporting artifacts (template, checklist)  
**Approval Required:** Architect Alphonso ✅, Backend Benny ⏳, Reviewer Rachel ⏳
