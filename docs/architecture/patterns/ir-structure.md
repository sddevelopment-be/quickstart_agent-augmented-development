# Intermediate Representation (IR) Structure Specification

**Document Type:** Technical Specification  
**Version:** 1.0.0  
**Date:** 2026-01-29  
**Status:** Proposed  
**Author:** Architect Alphonso  
**Related Documents:**
- `work/analysis/tech-design-export-pipeline.md` (Export Pipeline Design)
- `work/analysis/ADR-013-multi-format-distribution.md` (Multi-Format Strategy)

---

## Overview

The Intermediate Representation (IR) is a structured data format that serves as the common contract between the markdown parser and format-specific generators in the multi-format export pipeline.

**Design Principles:**

- **Self-Contained:** IR includes all data needed for generation (no external lookups)
- **Format-Agnostic:** IR structure does not favor any specific export format
- **Extensible:** New fields can be added without breaking existing generators
- **Validatable:** IR conforms to JSON Schema for automated validation
- **Human-Readable:** IR can be inspected as JSON for debugging

**Purpose:**

The IR abstracts away markdown parsing complexity, allowing generators to focus on format-specific transformations. This separation enables:

1. Independent testing of parser and generators
2. Addition of new export formats without modifying parser
3. Validation of data completeness before generation
4. Schema evolution without breaking changes

---

## TypeScript Interface Definition

The complete TypeScript interface definition and JSON Schema are extensive. See:
- Full TypeScript interfaces: `docs/technical/ir-structure-typescript.md`
- JSON Schema: `work/schemas/agent-ir-v1.schema.json` (to be created)

**Core Structure:**

```typescript
interface AgentIR {
  ir_version: string;           // Semver format (e.g., "1.0.0")
  frontmatter: { ... };          // YAML frontmatter metadata
  content: { ... };              // Narrative content sections
  relationships: { ... };        // Parsed relationships (directives, agents)
  governance: { ... };           // Governance metadata
  metadata: { ... };             // Source file metadata (hash, path, etc.)
}
```

### Key Nested Structures

**frontmatter** (YAML metadata):
- `name` (required): Agent identifier (kebab-case)
- `description` (required): Short purpose statement
- `tools` (required): Array of tool names
- `version`, `api_version`, `tags`, `category` (optional)

**content** (Narrative sections):
- `purpose` (required): Mission statement from Section 2
- `specialization` (required): Focus areas from Section 3
- `collaboration_contract` (required): Rules from Section 4
- `success_criteria` (required): Success definition
- `mode_defaults` (required): Array of reasoning modes
- `output_artifacts`, `operating_procedure` (optional)

**relationships** (Parsed connections):
- `directives` (required): Array of DirectiveReference objects
- `agent_references` (optional): Other agents mentioned
- `context_sources` (optional): Referenced files/locations

**governance** (Compliance metadata):
- `directive_requirements`: Classify directives as required/optional
- `escalation_rules`: Array of escalation conditions
- `uncertainty_threshold`: When to escalate (e.g., ">30%")
- `primer_required`, `test_first_required`: Boolean flags

**metadata** (Source tracking):
- `file_path`: Relative path from repo root
- `source_hash`: SHA-256 hash (64-char hex)
- `parsed_at`: ISO 8601 timestamp
- `file_size`: Bytes
- `parser_version`: Semver of parser

---

## Field Descriptions

### Required Fields

All IR instances MUST include:

1. `ir_version`: Format version (currently "1.0.0")
2. `frontmatter.name`, `frontmatter.description`, `frontmatter.tools`
3. `content.purpose`, `content.specialization`, `content.collaboration_contract`
4. `content.success_criteria`, `content.mode_defaults`
5. `relationships.directives` (may be empty array)
6. Complete `governance` section
7. Complete `metadata` section

### Optional Fields

Recommended when available:
- `frontmatter.version` (defaults to "1.0.0")
- `frontmatter.tags`, `frontmatter.category`
- `content.output_artifacts`
- `relationships.agent_references`
- `governance.uncertainty_threshold`, `governance.safety_criticality`

### Field Constraints

- **name**: Lowercase kebab-case (e.g., "architect-alphonso")
- **source_hash**: 64-character hexadecimal
- **parsed_at**: ISO 8601 with timezone
- **version fields**: Semantic versioning (major.minor.patch)
- **mode**: Prefix with "/" (e.g., "/analysis-mode")

---

## Export Format Mappings

### OpenCode

```typescript
// Discovery File
{
  opencode_version: "1.0",
  agent: {
    id: ir.frontmatter.name,
    version: ir.frontmatter.version || "1.0.0",
    description: ir.frontmatter.description,
    tools: ir.frontmatter.tools,
    // ...
  }
}
```

### GitHub Copilot

```yaml
name: ${ir.frontmatter.name}
description: ${ir.frontmatter.description}
tags: ${ir.frontmatter.tags}
capabilities: ${ir.frontmatter.tools}
```

### MCP

```json
{
  "name": "${ir.frontmatter.name}",
  "version": "${ir.frontmatter.version}",
  "tools": "${ir.frontmatter.tools}",
  "x-governance": { ... }
}
```

---

## Design Rationale

### TypeScript + JSON Schema Approach

**Decision:** Provide both TypeScript interfaces and JSON Schema

**Rationale:**
- TypeScript: IDE autocomplete, type checking, inline docs
- JSON Schema: Runtime validation, contract enforcement
- Generators use TypeScript; validation uses JSON Schema

**Trade-off:** Double maintenance vs. comprehensive validation + developer ergonomics

### Nested Structure

**Decision:** Use nested objects (frontmatter, content, relationships, governance, metadata)

**Rationale:**
- Semantic grouping improves comprehension
- Generators access logical domains independently
- Extensibility: add fields within appropriate domain
- Matches conceptual model

**Trade-off:** More verbose paths vs. better organization

### Minimal Required Fields

**Decision:** Only essential fields required; most optional

**Rationale:**
- Flexibility for diverse agent definitions
- Graceful degradation
- Reduces parser failure surface area
- Enables iterative development

**Trade-off:** Potential incomplete data vs. resilience

### Parsed vs. String Content

**Decision:** Parse semantically valuable content (directives, modes); preserve strings elsewhere

**Rationale:**
- Parsed directives enable governance tracking
- Mode defaults need structured access
- Markdown strings preserve rich context
- Balance usability vs. fidelity

**Trade-off:** Parser complexity vs. generator usability

---

## Extensibility Strategy

### Adding New Fields

1. Add to optional fields in TypeScript and JSON Schema
2. Update schema to allow (not require) new field
3. Document in this specification
4. Update example IRs
5. Generators ignore unknown fields (forward compatibility)

### Version Evolution

For breaking changes:
1. Increment `ir_version` (e.g., "1.0.0" → "2.0.0")
2. Create new schema version
3. Maintain N-1 parser compatibility
4. Document migration path
5. Provide conversion utilities

### Custom Extensions

Use "x-" prefix for format-specific extensions:

```typescript
interface OpenCodeIR extends AgentIR {
  "x-opencode": {
    profile_url: string;
    manifest_path: string;
  }
}
```

---

## Validation Strategy

### Parser-Side

1. Validate YAML syntax
2. Check required frontmatter fields
3. Extract content sections (warn if missing)
4. Parse directive table gracefully
5. Generate valid SHA-256 hash

### Schema Validation

1. Validate against JSON Schema
2. Check types and constraints
3. Verify semver format
4. Validate hash format
5. Check timestamp formats

### Generator-Side

1. Verify required fields exist
2. Check target format compatibility
3. Handle missing optional fields gracefully
4. Log warnings
5. Validate export against target schema

---

## Usage Example

### Parsing

```typescript
const parser = new MarkdownParser();
const ir = parser.parse('.github/agents/architect.agent.md');
const validation = validateIR(ir);
if (!validation.valid) {
  console.error('Validation failed:', validation.errors);
}
```

### Generation

```typescript
const generator = new OpenCodeGenerator({ outputDir: 'dist/opencode' });
const result = generator.generate(ir);
```

---

## See Also

- **Tech Design:** `work/analysis/tech-design-export-pipeline.md`
- **ADR-013:** `work/analysis/ADR-013-multi-format-distribution.md`
- **Example IRs:** `work/schemas/examples/ir/*.ir.json`
- **Full TypeScript:** `docs/technical/ir-structure-typescript.md` (detailed interfaces)
- **JSON Schema:** `work/schemas/agent-ir-v1.schema.json` (Task 1.4)

---

**Document Status:** ✅ Complete  
**Next Steps:** Create example IR instances  
**Handoff To:** Backend Benny (Task 1.2 - Parser Implementation)
