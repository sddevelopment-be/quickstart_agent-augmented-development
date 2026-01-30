# Agent Export Tools

**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Author:** Backend Benny  
**Date:** 2026-01-29

## Overview

This directory contains tools for the multi-format agent distribution pipeline:

1. **Parser** - Extracts structured data from `.agent.md` files into Intermediate Representation (IR)
2. **Validator** - Validates JSON/YAML files against JSON Schema specifications
3. **OpenCode Generator** - Generates OpenCode discovery and definition files from IR (PRIMARY export format)
4. **Copilot Generator** - Generates GitHub Copilot Skills JSON files from IR (SECONDARY export format)

---

## OpenCode Generator

**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Coverage:** 94.04%  
**Performance:** <2ms per agent  
**Date:** 2026-01-29

### Purpose

The OpenCode Generator is the **PRIMARY export format** for the multi-format agent distribution pipeline (70/100 compatibility, cross-platform standard). It generates:

1. **Discovery files** (`.opencode.json`) - Agent metadata and capabilities
2. **Definition files** (`.definition.yaml`) - Detailed specifications and governance

### Features

- ✅ Generates OpenCode 1.0 compliant files
- ✅ Uses IR from parser (no direct markdown parsing)
- ✅ Includes Saboteurs governance extensions
- ✅ Multi-agent orchestration metadata
- ✅ Automatic capability extraction
- ✅ Category inference
- ✅ 94% test coverage with ATDD/TDD
- ✅ <2ms per agent performance

### Quick Start

```javascript
const { parseAgentFile } = require('./tools/exporters/parser');
const { generateOpenCode } = require('./tools/exporters/opencode-generator');

async function exportAgent() {
  // Parse agent file to IR
  const ir = await parseAgentFile('.github/agents/architect.agent.md');
  
  // Generate OpenCode files
  const { discovery, definition } = await generateOpenCode(ir, 'output/opencode');
  
  console.log(`Generated: ${discovery}`);
  console.log(`Generated: ${definition}`);
}
```

### Discovery File Structure

```json
{
  "opencode_version": "1.0",
  "agent": {
    "id": "backend-benny",
    "name": "Backend Benny",
    "version": "1.0.0",
    "description": "Shape resilient service backends...",
    "capabilities": ["architecture", "backend", "api-design"],
    "category": "design",
    "tools": ["read", "write", "Bash", "Docker", "Java"],
    "profile_url": "./backend-dev.agent.md",
    "metadata": {
      "last_updated": "2026-01-29",
      "api_version": "1.0.0",
      "directives": ["001", "016", "017"],
      "styleguides": []
    }
  },
  "extensions": {
    "agentic_governance": { /* ... */ },
    "multi_agent": { /* ... */ }
  }
}
```

### Definition File Structure

```yaml
opencode_version: '1.0'
agent:
  metadata:
    id: backend-benny
    version: 1.0.0
    category: design
    tags: [architecture, backend]
  specification:
    inputs: []
    outputs: []
    examples: []
    tools: [read, write, Bash]
  governance:
    directives:
      - code: '016'
        title: ATDD
        required: true
    safety_critical: true
    primer_required: true
    uncertainty_threshold: '>30%'
```

### Governance Extensions

#### Saboteurs Governance

```json
{
  "agentic_governance": {
    "directives": [
      {
        "code": "016",
        "title": "ATDD",
        "required": true,
        "rationale": "Ensure solution fitness..."
      }
    ],
    "priority_level": "high",
    "uncertainty_threshold": ">30%",
    "escalation_required": true,
    "primer_required": true,
    "test_first_required": true,
    "safety_criticality": "medium"
  }
}
```

#### Multi-Agent Orchestration

```json
{
  "multi_agent": {
    "orchestration_capable": false,
    "handoff_protocols": ["file-based"],
    "specialization_boundaries": "explicit"
  }
}
```

### API Reference

#### `generateOpenCode(ir, outputDir)`

Generate OpenCode discovery and definition files from Agent IR.

**Parameters:**
- `ir` (AgentIR) - Parsed agent IR from parser
- `outputDir` (string) - Directory where to write files

**Returns:** `Promise<{discovery: string, definition: string}>`
- `discovery` - Path to generated `.opencode.json` file
- `definition` - Path to generated `.definition.yaml` file

**Example:**
```javascript
const { discovery, definition } = await generateOpenCode(ir, 'output/opencode');
```

#### `mapIRToDiscovery(ir)`

Map IR to OpenCode discovery file structure (in-memory).

**Parameters:**
- `ir` (AgentIR) - Parsed agent IR

**Returns:** `Object` - Discovery file structure

#### `mapIRToDefinition(ir)`

Map IR to OpenCode definition file structure (in-memory).

**Parameters:**
- `ir` (AgentIR) - Parsed agent IR

**Returns:** `Object` - Definition file structure

#### `extractGovernanceMetadata(ir)`

Extract governance extensions from IR.

**Parameters:**
- `ir` (AgentIR) - Parsed agent IR

**Returns:** `Object` - Governance extensions object with `agentic_governance` and `multi_agent`

### Capability Extraction

Capabilities are automatically extracted from:

1. **Tools**: Mapped to capability categories (e.g., `plantuml` → `diagramming`)
2. **Content**: Keywords in purpose, specialization, success criteria
3. **Context**: Word boundary matching for accurate detection

**Tool Capability Mapping:**
- `plantuml` → `diagramming`
- `Docker` → `containerization`
- `Java` → `backend`
- `Python` → `scripting`
- `Bash` → `automation`
- `markdown-linter` → `validation`
- `report_progress` → `workflow`

**Content Keywords:**
- `architecture`, `architectural` → `architecture`
- `design` → `design`
- `testing` → `testing`
- `review` → `code-review`
- `backend` → `backend`
- `api` → `api-design`
- And more...

### Category Inference

Categories are inferred from agent name and content:

- `architect*`, `architecture` → `design`
- `backend-*`, `*-dev` → `development`
- `review*` → `quality-assurance`
- `test*` → `testing`
- `doc*`, `documentation` → `documentation`
- `bootstrap*` → `initialization`
- `curator*`, `governance` → `governance`
- Default: `general`

### Testing

```bash
# Run OpenCode generator tests
npx jest tests/unit/opencode-generator.test.js

# With coverage
npx jest tests/unit/opencode-generator.test.js --coverage

# Watch mode
npx jest tests/unit/opencode-generator.test.js --watch
```

**Test Results:**
- 21/21 tests passing
- 94.04% statement coverage
- 82.79% branch coverage
- 93.33% function coverage

**Test Categories:**
1. Acceptance tests (8 tests) - End-to-end file generation
2. Unit tests (13 tests) - Individual function validation

### Performance

**Benchmark:** Export all 16 agents  
**Result:** 30ms total (2ms avg per agent)  
**Requirement:** <1000ms per agent ✅  
**Status:** **500x faster than requirement**

### Sample Exports

Sample exports are available in `tests/fixtures/opencode/`:

- `architect-alphonso.opencode.json` / `.definition.yaml`
- `backend-benny.opencode.json` / `.definition.yaml`
- `reviewer-rachel.opencode.json` / `.definition.yaml`

### Edge Cases Handled

- ✅ Missing optional frontmatter fields (uses defaults)
- ✅ Empty directives array (not null)
- ✅ Special characters in descriptions (proper JSON escaping)
- ✅ Minimal content (no false capability detection)
- ✅ Category name conflicts (specific matching)

### Export All Agents

```javascript
const { parseAgentDirectory } = require('./tools/exporters/parser');
const { generateOpenCode } = require('./tools/exporters/opencode-generator');

async function exportAll() {
  const irs = await parseAgentDirectory('.github/agents');
  
  for (const ir of irs) {
    await generateOpenCode(ir, 'output/opencode');
  }
  
  console.log(`Exported ${irs.length} agents`);
}
```

### Dependencies

```json
{
  "js-yaml": "^4.1.0"  // YAML generation
}
```

### Future Enhancements

Potential improvements for v2.0:

- [ ] Input/output extraction from content
- [ ] Example generation from content
- [ ] JSON Schema validation integration
- [ ] Batch export CLI tool
- [ ] Manifest file generation
- [ ] Tool registry generation

---

## GitHub Copilot Skills Generator

**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Coverage:** 84.54%  
**Performance:** <2ms per agent  
**Date:** 2026-01-29

### Purpose

The GitHub Copilot Skills Generator is the **SECONDARY export format** for the multi-format agent distribution pipeline (GitHub Copilot ecosystem integration). It generates `.copilot-skill.json` files that enable agents to be used as GitHub Copilot Skills in VS Code.

### Features

- ✅ Generates valid GitHub Copilot Skills JSON
- ✅ Role-based conversation starters (7 role types)
- ✅ VS Code extension mapping from agent tools
- ✅ Workspace settings configuration
- ✅ Governance extensions preserved
- ✅ Multi-agent orchestration metadata
- ✅ 84.54% test coverage with ATDD/TDD
- ✅ <2ms per agent performance (500x faster than target)

### Quick Start

```javascript
const { parseAgentFile } = require('./tools/exporters/parser');
const { generateCopilotSkill } = require('./tools/exporters/copilot-generator');

async function exportAgent() {
  // Parse agent file to IR
  const ir = await parseAgentFile('.github/agents/architect.agent.md');
  
  // Generate Copilot Skill file
  const skillPath = await generateCopilotSkill(ir, 'output/copilot');
  
  console.log(`Generated: ${skillPath}`);
}
```

### Copilot Skills File Structure

```json
{
  "$schema": "https://aka.ms/copilot-skill-schema",
  "name": "backend-benny",
  "description": "Shape resilient service backends and integration surfaces...",
  "capabilities": [
    "automation",
    "containerization",
    "backend-development",
    "api-design"
  ],
  "instructions": "Provide grounded backend architecture...",
  "conversation_starters": [
    "Help me design a RESTful API for this service",
    "Review this backend architecture for performance",
    "Design a database schema for these requirements"
  ],
  "workspace": {
    "extensions": [
      "GitHub.copilot",
      "GitHub.copilot-chat",
      "ms-azuretools.vscode-docker",
      "vscjava.vscode-java-pack"
    ],
    "settings": {
      "editor.formatOnSave": true,
      "editor.codeActionsOnSave": {
        "source.fixAll": true
      },
      "editor.rulers": [80, 120]
    }
  },
  "extensions": {
    "agentic_governance": { /* ... */ },
    "multi_agent": { /* ... */ }
  }
}
```

### Conversation Starters

The generator creates role-specific conversation starters based on agent characteristics:

**Supported Roles:**
- **Architect**: Architecture design, ADRs, system design
- **Backend**: API design, service boundaries, database schemas
- **Reviewer**: Code review, quality checks, best practices
- **Frontend**: UI components, accessibility, state management
- **Tester**: Unit tests, test cases, edge cases
- **Documentation**: Technical writing, user guides, API docs
- **Generic**: Fallback for unrecognized roles

**Example Starters for Backend:**
```json
[
  "Help me design a RESTful API for this service",
  "Review this backend architecture for performance",
  "Design a database schema for these requirements",
  "Help me implement clean service boundaries",
  "Suggest improvements for this API design"
]
```

### Tool to Extension Mapping

The generator maps agent tools to VS Code extension IDs:

| Tool | VS Code Extension |
|------|------------------|
| `plantuml` | `jebbs.plantuml` |
| `mermaid` | `bierner.markdown-mermaid` |
| `markdown-linter` | `DavidAnson.vscode-markdownlint` |
| `bash` | `timonwong.shellcheck` |
| `Docker` | `ms-azuretools.vscode-docker` |
| `Java` | `vscjava.vscode-java-pack` |
| `Python` | `ms-python.python` |
| `JavaScript` | `dbaeumer.vscode-eslint` |
| `TypeScript` | `ms-vscode.vscode-typescript-next` |

**Base Extensions** (always included):
- `GitHub.copilot`
- `GitHub.copilot-chat`

### Workspace Settings

Generated workspace settings include:

**Default Settings:**
```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  },
  "files.autoSave": "onFocusChange"
}
```

**Role-Specific Settings:**
- **Architect/Backend**: `"editor.rulers": [80, 120]`
- **Documentation**: `"markdown.preview.breaks": true`

### API Reference

#### `generateCopilotSkill(ir, outputDir)`

Generate GitHub Copilot Skill file from Agent IR.

**Parameters:**
- `ir` (AgentIR) - Parsed agent IR from parser
- `outputDir` (string) - Directory where to write file

**Returns:** `Promise<string>` - Path to generated `.copilot-skill.json` file

**Example:**
```javascript
const skillPath = await generateCopilotSkill(ir, 'output/copilot');
// Returns: 'output/copilot/backend-benny.copilot-skill.json'
```

#### `mapIRToCopilotSkill(ir)`

Map IR to Copilot Skill structure (in-memory).

**Parameters:**
- `ir` (AgentIR) - Parsed agent IR

**Returns:** `Object` - Copilot Skill structure

#### `generateConversationStarters(ir)`

Generate role-appropriate conversation starters.

**Parameters:**
- `ir` (AgentIR) - Parsed agent IR

**Returns:** `Array<string>` - Array of conversation starter strings (3-5 starters)

#### `mapToolsToExtensions(tools)`

Map tool names to VS Code extension IDs.

**Parameters:**
- `tools` (Array<string>) - Array of tool names from IR

**Returns:** `Array<string>` - Array of VS Code extension IDs

### Testing

```bash
# Run Copilot generator tests
npx jest tests/unit/copilot-generator.test.js

# With coverage
npx jest tests/unit/copilot-generator.test.js --coverage
```

**Test Results:**
- 26/26 tests passing
- 84.54% statement coverage
- 80.55% branch coverage
- 100% function coverage

### Performance

**Benchmark:** Export all 16 agents  
**Result:** 38ms total (2ms avg per agent)  
**Requirement:** <1000ms per agent ✅  
**Status:** **500x faster than requirement**

### Sample Exports

Sample exports are available in `tests/fixtures/copilot/`:

- `architect-alphonso.copilot-skill.json`
- `backend-benny.copilot-skill.json`
- `reviewer-rachel.copilot-skill.json`

### Related Documentation

- **Copilot Skills Spec**: https://aka.ms/copilot-skill-schema
- **Task Document**: `work/collaboration/assigned/backend-dev/2026-01-29T0730-mfd-task-2.2-copilot-generator.yaml`
- **Work Log**: `work/reports/logs/backend-dev/2026-01-29-copilot-generator.md`
- **IR Specification**: `docs/technical/ir-structure.md`

---

- **OpenCode Spec**: https://opencode.ai/docs/agents/
- **Task Document**: `work/collaboration/assigned/backend-dev/2026-01-29T0730-mfd-task-2.1-opencode-generator.yaml`
- **IR Specification**: `docs/technical/ir-structure.md`
- **ADR-013**: `work/analysis/ADR-013-multi-format-distribution.md`

---

## Base Validator Framework

### Purpose

The base validator provides JSON Schema validation for agent data with clear error messages and extensibility for custom validation rules.

### Features

- ✅ JSON Schema Draft 7 validation
- ✅ Support for JSON and YAML files
- ✅ Clear, actionable error messages
- ✅ Schema loading from file system
- ✅ Custom validator plugins
- ✅ Format validation (email, date-time, URI, etc.)
- ✅ Schema caching for performance
- ✅ 94%+ test coverage

### Quick Start

```javascript
const { validate, validateFile, Validator } = require('./tools/exporters/validator');

// Validate data against inline schema
const result = validate(data, schema);
if (!result.valid) {
  console.error('Validation failed:', result.errors);
}

// Validate JSON/YAML file
const fileResult = await validateFile('agent.json', schema);

// Load schema from file
const schemaResult = await validateFile('data.json', './schema.json');
```

### API Reference

#### `validate(data, schema)`

Validate data against a JSON Schema.

**Parameters:**
- `data` (any) - Data to validate
- `schema` (Object) - JSON Schema object

**Returns:** `ValidationResult`
- `valid` (boolean) - True if validation passed
- `errors` (ValidationError[]) - Array of validation errors

**Example:**
```javascript
const result = validate(
  { name: 'test', version: '1.0.0' },
  {
    type: 'object',
    properties: {
      name: { type: 'string' },
      version: { type: 'string' }
    },
    required: ['name', 'version']
  }
);

if (result.valid) {
  console.log('✅ Valid!');
} else {
  console.error('❌ Errors:', result.errors);
}
```

#### `validateFile(filePath, schema)`

Validate a JSON or YAML file against a schema.

**Parameters:**
- `filePath` (string) - Path to JSON or YAML file
- `schema` (Object|string) - JSON Schema object or path to schema file

**Returns:** `Promise<ValidationResult>`

**Example:**
```javascript
// Validate against inline schema
const result = await validateFile('./agent.yaml', {
  type: 'object',
  properties: {
    name: { type: 'string' }
  }
});

// Validate against schema file
const result = await validateFile(
  './data.json',
  './schemas/input.schema.json'
);
```

#### `formatErrors(errors, fileName?)`

Format validation errors for human-readable output.

**Parameters:**
- `errors` (ValidationError[]) - Array of validation errors
- `fileName` (string, optional) - File name to include in output

**Returns:** `string` - Formatted error message

**Example:**
```javascript
const formatted = formatErrors(result.errors, 'agent.json');
console.log(formatted);

// Output:
// ❌ Validation failed for agent.json
//
// Error 1: version
//   Expected: string
//   Actual: number (123)
//   Message: must be string
```

#### `Validator` Class

Main validator class with extensibility support.

**Methods:**
- `validate(data, schema)` - Validate data
- `loadSchema(schemaPath)` - Load schema from file (with caching)
- `addCustomValidator(fn)` - Add custom validation function

**Example:**
```javascript
const validator = new Validator();

// Add custom validation rule
validator.addCustomValidator((data) => {
  if (data.name === 'forbidden') {
    return {
      valid: false,
      errors: [{
        path: 'name',
        message: 'Name "forbidden" is not allowed',
        keyword: 'custom'
      }]
    };
  }
  return { valid: true, errors: [] };
});

// Validate with custom rules
const result = validator.validate(data, schema);
```

### Error Format

Validation errors include:

```typescript
interface ValidationError {
  path: string;        // JSON path: 'user.email' or 'items.0.name'
  message: string;     // Human-readable message
  keyword: string;     // JSON Schema keyword that failed
  expected?: any;      // Expected type/value
  actual?: any;        // Actual value (if not object)
}
```

**Example output:**
```
❌ Validation failed for architect-input.json

Error 1: task.task_id
  Expected: string
  Actual: number (123)
  Message: must be string

Error 2: task
  Expected: required property 'task_description'
  Message: must have required property 'task_description'

Error 3: mode
  Expected: analysis-mode,creative-mode,meta-mode
  Message: must be equal to one of the allowed values
```

### Extensibility

#### Custom Validators

Add custom validation logic beyond JSON Schema:

```javascript
const validator = new Validator();

// Add business logic validation
validator.addCustomValidator((data) => {
  const errors = [];
  
  // Example: Check version format
  if (data.version && !/^\d+\.\d+\.\d+$/.test(data.version)) {
    errors.push({
      path: 'version',
      message: 'Version must follow semantic versioning (X.Y.Z)',
      keyword: 'custom'
    });
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
});
```

#### Plugin Pattern

Custom validators can be packaged as plugins:

```javascript
// validators/opencode-validator.js
module.exports = function opencodeValidator(data) {
  // OpenCode-specific validation
  if (data.format === 'opencode') {
    // Validate OpenCode structure
  }
  return { valid: true, errors: [] };
};

// Usage
const opencodeValidator = require('./validators/opencode-validator');
validator.addCustomValidator(opencodeValidator);
```

### Testing

```bash
# Run validator tests
npx jest tests/unit/validator.test.js

# With coverage
npx jest tests/unit/validator.test.js --coverage

# Watch mode
npx jest tests/unit/validator.test.js --watch
```

**Coverage:**
- Statements: 94.73%
- Branches: 92.15%
- Functions: 100%

### Performance

- **Schema caching**: Loaded schemas are cached for reuse
- **Batch validation**: Validate multiple files efficiently
- **Fast validation**: Built on AJV, the fastest JSON Schema validator

### Dependencies

```json
{
  "ajv": "^8.x",           // JSON Schema validator
  "ajv-formats": "^2.x",   // Format validators (email, URI, etc.)
  "js-yaml": "^4.1.x"      // YAML parsing
}
```

---

## Agent Markdown Parser

**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Author:** Backend Benny  
**Date:** 2026-01-29

## Overview

This parser extracts structured data from `.agent.md` files and produces Intermediate Representation (IR) instances following the schema defined in `docs/technical/ir-structure.md`.

## Purpose

The parser is the **single source of truth** for agent data extraction in the multi-format export pipeline. It:

- Parses YAML frontmatter and validates required fields
- Extracts markdown content sections (Purpose, Specialization, etc.)
- Parses directive references and relationships
- Generates file metadata (SHA-256 hash, timestamps)
- Extracts governance information
- Produces valid IR instances ready for format-specific generators

## Usage

### Parse a Single Agent File

```javascript
const { parseAgentFile } = require('./tools/exporters/parser');

async function example() {
  const ir = await parseAgentFile('.github/agents/architect.agent.md');
  console.log(ir.frontmatter.name); // "architect-alphonso"
  console.log(ir.metadata.source_hash); // SHA-256 hash
}
```

### Parse All Agents in a Directory

```javascript
const { parseAgentDirectory } = require('./tools/exporters/parser');

async function parseAll() {
  const agents = await parseAgentDirectory('.github/agents');
  console.log(`Parsed ${agents.length} agents`);
}
```

### Error Handling

The parser throws `ParseError` instances with detailed information:

```javascript
try {
  await parseAgentFile('invalid.md');
} catch (error) {
  console.error(error.name);      // "ParseError"
  console.error(error.message);   // Detailed error message
  console.error(error.filePath);  // Path to problematic file
}
```

## IR Structure

The parser produces IR objects with the following structure:

```typescript
interface AgentIR {
  ir_version: string;           // "1.0.0"
  frontmatter: {
    name: string;               // Required: agent identifier
    description: string;        // Required: short purpose
    tools: string[];            // Required: array of tool names
    version?: string;           // Optional: defaults to "1.0.0"
    category?: string;
    tags?: string[];
  };
  content: {
    purpose: string;            // Main mission statement
    specialization: string;     // Focus areas
    collaboration_contract: string;
    success_criteria: string | null;
    output_artifacts: string | null;
    operating_procedure: string | null;
    mode_defaults: ModeDefault[];
  };
  relationships: {
    directives: Directive[];
    context_sources: ContextSource[];
    agent_references: any[];
  };
  governance: {
    directive_requirements: {
      required: number[];
      optional: number[];
    };
    uncertainty_threshold: string | null;
    escalation_rules: string[];
    safety_criticality: string | null;
    primer_required: boolean;
    test_first_required: boolean;
  };
  metadata: {
    file_path: string;          // Relative path from repo root
    source_hash: string;        // SHA-256 (64 hex chars)
    parsed_at: string;          // ISO 8601 timestamp
    file_size: number;          // Bytes
    parser_version: string;     // Parser version
  };
}
```

## Features

### ✅ Implemented

- **YAML Frontmatter Parsing**: Using `gray-matter` library
- **Markdown Section Extraction**: Regex-based heading detection
- **Directive Table Parsing**: Extracts code, title, rationale
- **Mode Defaults Parsing**: Extracts mode configuration table
- **Context Sources Extraction**: Parses context reference bullets
- **Governance Detection**: Identifies requirements and thresholds
- **File Metadata Generation**: SHA-256 hash, timestamps, file size
- **Error Handling**: Clear, actionable error messages
- **Performance**: Parses 16 agents in <30ms

### 📋 Parsing Rules

1. **Required Frontmatter Fields**: `name`, `description`, `tools`
2. **Default Values**: `version` defaults to "1.0.0" if missing
3. **Section Extraction**: Matches headings like `## 2. Purpose`
4. **Directive Parsing**: Extracts from directive table AND Test-First sections
5. **Hash Generation**: SHA-256 of entire file content
6. **Timestamps**: ISO 8601 format without milliseconds

## Test Coverage

- **Statements**: 97.7%
- **Branches**: 84.09%
- **Functions**: 100%
- **Lines**: 97.59%

### Test Suite

```bash
npm run test:parser          # Run all tests
npm run test:parser:watch    # Watch mode
npm run test:parser:coverage # Coverage report
```

### Test Categories

1. **Acceptance Tests** (11 tests)
   - Parse complete agent files
   - Handle missing optional fields
   - Error handling (malformed YAML, missing fields)
   - Directory parsing
   - Performance validation (<2 seconds)
   - IR fixture validation

2. **Unit Tests - Edge Cases** (4 tests)
   - Agents without directive tables
   - Test-First requirement detection
   - Subsection handling
   - Empty mode defaults

## Performance

**Benchmark:** Parse all 16 agent files  
**Result:** 26ms (avg)  
**Requirement:** <2000ms ✅  
**Status:** **77x faster than requirement**

## Error Messages

The parser provides clear, actionable error messages:

```
❌ ParseError: No frontmatter found in .github/agents/test.agent.md
   Expected YAML frontmatter between --- delimiters

❌ ParseError: Invalid YAML in .github/agents/test.agent.md:3
   → mapping values are not allowed here

❌ ParseError: Missing required field 'name' in .github/agents/test.agent.md
   → Add 'name: agent-name' to frontmatter
```

## Generated Fixtures

Test fixtures are available in `tests/fixtures/ir/`:

- `architect-alphonso.ir.json` - Complex agent with 12 directives
- `backend-benny.ir.json` - Technical agent with build tools
- `reviewer-rachel.ir.json` - QA agent with cross-references

These fixtures serve as:
- Expected output for acceptance tests
- Input for generator tests
- Documentation examples
- Schema validation test cases

## Dependencies

```json
{
  "js-yaml": "^4.1.0",      // YAML parsing
  "gray-matter": "^4.0.3",  // Frontmatter extraction
  "jest": "^29.7.0"         // Testing (devDependency)
}
```

## Future Enhancements

Potential improvements for v2.0:

- [ ] Agent reference extraction (mentioned agents)
- [ ] Link validation for directive references
- [ ] Markdown AST parsing for richer content
- [ ] Incremental parsing (only changed files)
- [ ] Parallel file processing
- [ ] JSON Schema validation integration
- [ ] Source map generation for error reporting

## Related Documentation

- **IR Specification**: `docs/technical/ir-structure.md`
- **Tech Design**: `work/analysis/tech-design-export-pipeline.md`
- **ADR-013**: `work/analysis/ADR-013-multi-format-distribution.md`
- **Task Document**: `work/collaboration/assigned/backend-dev/2026-01-29T0730-mfd-task-1.2-implement-parser.yaml`

## Maintenance

**Maintainer:** Backend Benny  
**Review Frequency:** Per ADR-013 review cycle  
**Versioning**: Semantic versioning (major.minor.patch)

### Breaking Changes Require

1. Increment parser version
2. Update IR version if structure changes
3. Migration guide documentation
4. Backward compatibility tests
5. Generator updates

---

**Status:** ✅ Complete  
**Tests:** ✅ 15/15 passing  
**Coverage:** ✅ >97%  
**Performance:** ✅ <30ms for 16 agents  
**Production Ready:** Yes
