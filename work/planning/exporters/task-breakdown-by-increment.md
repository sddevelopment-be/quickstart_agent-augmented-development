# Task Breakdown by Increment: Multi-Format Distribution

**Document ID:** TASK-MFD-001  
**Date:** 2026-01-29  
**Status:** Draft (Pending Review)  
**Related Plan:** `work/planning/multi-format-distribution-implementation-plan.md`  
**Related ADR:** ADR-013 (Multi-Format Distribution Strategy)

---

## Purpose

This document provides a granular, task-level breakdown of work for each batch/increment in the Multi-Format Distribution implementation. Each task includes:
- **Agent assignment** with rationale
- **Detailed description** of work to be performed
- **Inputs** required to start the task
- **Outputs** delivered upon completion
- **Dependencies** (within and across increments)
- **Effort estimate** in hours
- **Success criteria** for task completion

---

## Batch 1: Foundation & Infrastructure (Week 1, 16 hours)

**Objective:** Build parsing infrastructure, formalize schema conventions, and validate feasibility with 5 representative agents.

---

### Task 1.1: Design Intermediate Representation (IR) Structure

**Agent:** Architect Alphonso  
**Effort:** 2 hours  
**Dependencies:** None (starting point)

**Rationale:** Architect specializes in data flow design and technical architecture; IR is foundational contract between parser and generators.

**Description:**
Design the intermediate representation (IR) data structure that serves as the common format between the parser (input: markdown) and generators (output: OpenCode/Copilot/MCP). The IR must capture:
- YAML frontmatter metadata (name, description, tools, directives, specialization)
- Narrative content sections (purpose, collaboration contract, operating procedure)
- Source file metadata (path, hash, last modified)
- Parsed directive relationships
- Tool specifications

**Inputs:**
- Sample agent files (`.github/agents/*.agent.md`)
- ADR-013 requirements (governance preservation, custom extensions)
- Tech design document (`work/analysis/tech-design-export-pipeline.md`)

**Outputs:**
- IR schema specification (TypeScript interface or JSON Schema)
- Example IR instances for 3 sample agents
- Documentation: `docs/technical/ir-structure.md`

**Success Criteria:**
- ✅ IR captures all fields needed for OpenCode, Copilot, MCP exports
- ✅ IR is self-contained (no external references needed during generation)
- ✅ Team review and approval (Architect + Backend Benny)

---

### Task 1.2: Implement Markdown Parser

**Agent:** Backend Benny  
**Effort:** 6 hours  
**Dependencies:** Task 1.1 (IR structure defined)

**Rationale:** Backend Benny specializes in service logic and data transformations; parser is core data extraction logic.

**Description:**
Implement a Node.js parser component that extracts structured data from `.agent.md` files and produces IR instances. The parser must:
- Parse YAML frontmatter (using `js-yaml` or equivalent)
- Extract markdown sections (using regex or markdown parser library)
- Handle edge cases (missing fields, malformed YAML, multi-line descriptions)
- Generate source file hash (using `crypto` module)
- Validate basic structure (required fields present)

**Inputs:**
- IR structure specification (from Task 1.1)
- All agent files (`.github/agents/*.agent.md`)
- Prototype parser logic (from `tools/opencode-exporter.js`)

**Outputs:**
- `tools/exporters/parser.js` (production-ready parser module)
- Unit tests: `tests/unit/parser.test.js`
- Fixtures: sample IR outputs for 3 agents (`tests/fixtures/ir/*.json`)

**Success Criteria:**
- ✅ Parser successfully processes all 17 agent files without errors
- ✅ Generated IR validates against IR schema
- ✅ Unit tests pass with >85% code coverage
- ✅ Error handling for malformed inputs (graceful failures with clear messages)

---

### Task 1.3: Define Schema Conventions and Document

**Agent:** Architect Alphonso  
**Effort:** 3 hours  
**Dependencies:** Task 1.2 (parser available to test schema extraction)

**Rationale:** Architect defines technical standards and conventions; schema design is architectural decision.

**Description:**
Formalize the conventions for defining input/output schemas in agent profiles. Since existing agents lack explicit schemas, establish patterns for:
- **Schema extraction heuristics** (infer from narrative content, examples)
- **Schema format** (JSON Schema Draft 7 or similar)
- **Required vs. optional properties** (defaults, validations)
- **Schema placement** (YAML frontmatter? separate section? inline examples?)
- **Documentation requirements** (schema annotations, examples)

Document conventions in `docs/schemas/schema-conventions.md` with:
- Rationale for decisions
- Examples (good and bad)
- Migration path (how to add schemas to existing agents)
- Validation checklist

**Inputs:**
- Sample agent profiles (representative complexity: Architect, Backend Benny, Reviewer Rachel, Curator Claire, Planning Petra)
- Tech design section on schema formalization
- JSON Schema specification

**Outputs:**
- `docs/schemas/schema-conventions.md` (convention documentation)
- Schema template (JSON Schema skeleton for new agents)
- Migration checklist (for adding schemas to existing agents)

**Success Criteria:**
- ✅ Conventions cover 80% of common agent input/output patterns
- ✅ Team review and approval (Architect + Backend Benny + Reviewer Rachel)
- ✅ Conventions are clear enough for contributors to follow independently

---

### Task 1.4: Create Schemas for 5 Representative Agents

**Agent:** Backend Benny (primary) + Architect Alphonso (review)  
**Effort:** 4 hours  
**Dependencies:** Task 1.3 (schema conventions defined)

**Rationale:** Backend Benny implements schemas following Architect's conventions; validates feasibility of conventions.

**Description:**
Apply schema conventions to create input/output JSON Schemas for 5 representative agents:
1. **Architect Alphonso** (complex: ADRs, diagrams, technical design)
2. **Backend Benny** (medium: code, tests, services)
3. **Reviewer Rachel** (structured: checklists, test reports, approvals)
4. **Curator Claire** (content-focused: docs, organization)
5. **Planning Petra** (process-oriented: plans, milestones, tasks)

For each agent, define:
- **Input schema:** Parameters required to invoke the agent
- **Output schema:** Artifacts produced by the agent
- **Examples:** Valid request/response pairs

**Inputs:**
- Schema conventions (from Task 1.3)
- Agent profiles (narrative content to extract schemas from)
- JSON Schema validator (for testing schemas)

**Outputs:**
- 5 schema files: `work/schemas/{agent-id}.input.schema.json`, `work/schemas/{agent-id}.output.schema.json`
- Example instances: `work/schemas/{agent-id}.examples.json`
- Validation report (schemas validate against JSON Schema spec)

**Success Criteria:**
- ✅ All 5 schemas validate against JSON Schema Draft 7
- ✅ Schemas cover 80% of typical agent invocations (based on narrative content)
- ✅ Examples validate against schemas
- ✅ Schemas reviewed and approved by Architect

---

### Task 1.5: Implement Base Validator Framework

**Agent:** Backend Benny  
**Effort:** 2 hours  
**Dependencies:** Task 1.4 (sample schemas available for testing)

**Rationale:** Backend Benny implements core validation logic; needed for Batch 3 CI/CD integration.

**Description:**
Create a base validator module that can:
- Validate JSON/YAML files against JSON Schema specifications
- Report validation errors with clear messages (path, expected vs. actual)
- Load schemas from file system or inline
- Support format-specific validation extensions (OpenCode, Copilot, MCP)

The validator will be extended in Batch 3 with format compliance checks, hash verification, and integration tests.

**Inputs:**
- Sample schemas (from Task 1.4)
- JSON Schema specification
- Validation requirements (from tech design document)

**Outputs:**
- `tools/exporters/validator.js` (base validator module)
- Unit tests: `tests/unit/validator.test.js`
- Documentation: JSDoc comments in code

**Success Criteria:**
- ✅ Validator successfully validates sample schemas
- ✅ Error messages are clear and actionable
- ✅ Unit tests pass with >80% coverage
- ✅ Validator extensible for format-specific checks (design reviewed)

---

### Batch 1 Summary

| Task | Agent | Effort | Dependencies | Output |
|------|-------|--------|--------------|--------|
| 1.1 | Architect Alphonso | 2h | None | IR structure spec |
| 1.2 | Backend Benny | 6h | 1.1 | Parser module |
| 1.3 | Architect Alphonso | 3h | 1.2 | Schema conventions |
| 1.4 | Backend Benny + Architect | 4h | 1.3 | 5 agent schemas |
| 1.5 | Backend Benny | 2h | 1.4 | Base validator |
| **Total** | | **16h** | | **Foundation Complete** |

**Milestone 1 Validation:**
- Run parser on all 17 agents → validate IR generation
- Review schemas with team → approve conventions
- Validate base validator on sample schemas

---

## Batch 2: Export Pipeline Core (Week 2, 28 hours)

**Objective:** Implement format-specific generators (OpenCode, Copilot, MCP), complete schemas for all agents, and add governance extensions.

---

### Task 2.1: Enhance OpenCode Generator (Production-Ready)

**Agent:** Backend Benny  
**Effort:** 6 hours  
**Dependencies:** Batch 1 complete (parser + IR + schemas available)

**Rationale:** Backend Benny implements generator logic; OpenCode is primary format with existing prototype.

**Description:**
Enhance the prototype OpenCode exporter (`tools/opencode-exporter.js`) to production quality:
- Refactor to use IR from parser (decouple from direct markdown reading)
- Add governance extensions (`extensions.saboteurs_governance`, `extensions.multi_agent`)
- Generate both discovery (`.opencode.json`) and definition (`.definition.yaml`) files
- Handle edge cases (missing tools, optional directives, complex descriptions)
- Add error handling and validation hooks
- Optimize for performance (parallel file writes, streaming)

**Inputs:**
- IR from parser (Batch 1, Task 1.2)
- Prototype exporter (`tools/opencode-exporter.js`)
- OpenCode specification (external standard)
- Governance extension requirements (from ADR-013)

**Outputs:**
- `tools/exporters/opencode-generator.js` (production generator module)
- Unit tests: `tests/unit/opencode-generator.test.js`
- Sample exports: `tests/fixtures/opencode/` (3 sample agents)

**Success Criteria:**
- ✅ Generates valid OpenCode discovery + definition files
- ✅ Governance extensions present in all exports
- ✅ Exports validate against OpenCode schema (manual validation)
- ✅ Unit tests pass with >80% coverage
- ✅ Performance: <1 second per agent

---

### Task 2.2: Implement GitHub Copilot Skills Generator

**Agent:** Backend Benny  
**Effort:** 5 hours  
**Dependencies:** Task 2.1 (generator pattern established)

**Rationale:** Backend Benny reuses generator pattern from OpenCode; Copilot has well-documented spec.

**Description:**
Implement a GitHub Copilot Skills generator that transforms IR into Copilot-compatible YAML skill definitions:
- Map agent metadata to Copilot skill format (`name`, `description`, `tags`, `examples`)
- Include governance metadata in custom fields (if Copilot supports extensions)
- Generate examples from agent narrative content (use `operating_procedure`, `collaboration_contract`)
- Add tool mappings (map agent `tools` to Copilot capabilities)
- Follow Copilot Skills specification format

**Inputs:**
- IR from parser
- GitHub Copilot Skills specification
- OpenCode generator (reference implementation pattern)
- Sample Copilot skills (for format validation)

**Outputs:**
- `tools/exporters/copilot-generator.js` (generator module)
- Unit tests: `tests/unit/copilot-generator.test.js`
- Sample exports: `tests/fixtures/copilot/` (3 sample agents)

**Success Criteria:**
- ✅ Generates valid Copilot YAML skill files
- ✅ Skills include examples and metadata
- ✅ Exports validate against Copilot schema (if available)
- ✅ Unit tests pass with >80% coverage

---

### Task 2.3: Implement MCP Generator

**Agent:** Backend Benny  
**Effort:** 5 hours  
**Dependencies:** Task 2.2 (generator pattern mature)

**Rationale:** Backend Benny reuses generator pattern; MCP is emerging standard with JSON format.

**Description:**
Implement a Model Context Protocol (MCP) generator that transforms IR into MCP server definitions:
- Map agent to MCP server specification (`name`, `version`, `tools`, `resources`)
- Include governance metadata in custom extensions (MCP supports `x-*` extensions)
- Define tool specifications (inputs, outputs, schemas)
- Add resource specifications (agent artifacts, documentation)
- Follow MCP specification format (JSON)

**Inputs:**
- IR from parser
- Model Context Protocol specification
- OpenCode/Copilot generators (reference patterns)

**Outputs:**
- `tools/exporters/mcp-generator.js` (generator module)
- Unit tests: `tests/unit/mcp-generator.test.js`
- Sample exports: `tests/fixtures/mcp/` (3 sample agents)

**Success Criteria:**
- ✅ Generates valid MCP JSON server definitions
- ✅ Governance extensions present in `x-saboteurs` fields
- ✅ Exports validate against MCP schema (if available)
- ✅ Unit tests pass with >80% coverage

---

### Task 2.4: Complete Schemas for Remaining 12 Agents

**Agent:** Architect Alphonso (6 agents) + Scribe (6 agents)  
**Effort:** 8 hours (4h Architect + 4h Scribe)  
**Dependencies:** Task 1.4 (schema conventions validated with 5 agents)

**Rationale:** Distribute schema work across agents with content expertise; Architect handles complex technical agents, Scribe handles documentation-focused agents.

**Description:**
Apply schema conventions to create input/output JSON Schemas for the remaining 12 agents:

**Architect Alphonso:** (complex technical agents)
- Backend Benny (code, services, APIs)
- Build Automation Specialist (CI/CD, workflows)
- Frontend Specialist (UI, components)
- DevOps Specialist (infrastructure, deployment)
- Security Specialist (security analysis, threat modeling)
- Performance Specialist (optimization, benchmarking)

**Scribe:** (content and process agents)
- Curator Claire (content organization, documentation)
- Scribe (user guides, technical writing)
- Reviewer Rachel (checklists, test reports)
- Synthesizer Sam (integration, coordination)
- LEX Specialist (legal, compliance)
- Researcher (analysis, investigation)

For each agent, define input/output schemas and examples (same format as Task 1.4).

**Inputs:**
- Schema conventions (from Task 1.3)
- Agent profiles (narrative content)
- Sample schemas from Batch 1 (reference format)

**Outputs:**
- 12 schema files: `work/schemas/{agent-id}.input.schema.json`, `work/schemas/{agent-id}.output.schema.json`
- Example instances: `work/schemas/{agent-id}.examples.json`
- Schema index: `work/schemas/index.md` (catalog of all schemas)

**Success Criteria:**
- ✅ All 12 schemas validate against JSON Schema Draft 7
- ✅ Schemas reviewed by Architect (quality check)
- ✅ Examples validate against schemas
- ✅ Total: 17 agents with complete schemas

---

### Task 2.5: Implement Governance Extensions

**Agent:** Backend Benny  
**Effort:** 3 hours  
**Dependencies:** Tasks 2.1-2.3 (generators functional)

**Rationale:** Backend Benny implements cross-cutting logic for all generators.

**Description:**
Implement a shared module that injects governance metadata into all export formats:
- **Directive mappings:** Extract directive codes from agent frontmatter; map to structured format
- **Uncertainty threshold:** Extract from `collaboration_contract` narrative
- **Escalation rules:** Derive from narrative content
- **Priority level:** Infer from agent specialization (security → high, content → medium)
- **Multi-agent orchestration:** Extract handoff protocols, specialization boundaries
- **Quality gates:** Reference ATDD/TDD requirements from directives

Create a `GovernanceExtractor` class that analyzes IR and produces governance metadata for injection into all formats.

**Inputs:**
- IR from parser
- Directive registry (`.github/agents/directives/`)
- Governance requirements (from ADR-013)

**Outputs:**
- `tools/exporters/governance-extractor.js` (shared module)
- Unit tests: `tests/unit/governance-extractor.test.js`
- Sample governance metadata: `tests/fixtures/governance/*.json`

**Success Criteria:**
- ✅ Governance metadata extracted for all 17 agents
- ✅ Generators integrate governance extensions
- ✅ Manual validation: 3 sample exports reviewed for completeness
- ✅ Unit tests pass with >80% coverage

---

### Task 2.6: Implement Manifest Generators

**Agent:** Backend Benny  
**Effort:** 2 hours  
**Dependencies:** Tasks 2.1-2.3 (format generators complete)

**Rationale:** Backend Benny implements aggregation logic; manifests are format-specific catalogs.

**Description:**
Implement manifest generator modules for each format:
- **OpenCode:** `manifest.opencode.json` (catalog of all agents with discovery file paths)
- **Copilot:** `skills-index.yaml` (list of all skills with metadata)
- **MCP:** `servers-registry.json` (registry of all MCP servers)

Manifests enable discovery and batch processing by tools.

**Inputs:**
- Generated exports (from Tasks 2.1-2.3)
- Manifest format specifications (from OpenCode/Copilot/MCP specs)

**Outputs:**
- `tools/exporters/manifest-generator.js` (manifest module)
- Unit tests: `tests/unit/manifest-generator.test.js`
- Sample manifests: `tests/fixtures/manifests/`

**Success Criteria:**
- ✅ Manifests list all 17 agents with correct metadata
- ✅ Manifests validate against format specifications
- ✅ Unit tests pass with >80% coverage

---

### Batch 2 Summary

| Task | Agent | Effort | Dependencies | Output |
|------|-------|--------|--------------|--------|
| 2.1 | Backend Benny | 6h | Batch 1 | OpenCode generator |
| 2.2 | Backend Benny | 5h | 2.1 | Copilot generator |
| 2.3 | Backend Benny | 5h | 2.2 | MCP generator |
| 2.4 | Architect + Scribe | 8h | 1.4 | 12 agent schemas |
| 2.5 | Backend Benny | 3h | 2.1-2.3 | Governance extensions |
| 2.6 | Backend Benny | 2h | 2.1-2.3 | Manifest generators |
| **Total** | | **28h** | | **Export Pipeline Functional** |

**Milestone 2 Validation:**
- Generate exports for all 17 agents → validate output files
- Review 3 sample exports (Architect, Backend Benny, Reviewer Rachel) → verify governance metadata
- Manual integration test (use OpenCode export to integrate 1 agent)

---

## Batch 3: Automation & Validation (Week 3, 24 hours)

**Objective:** Automate export generation via CI/CD, implement comprehensive test suite, and add hash verification.

---

### Task 3.1: Create GitHub Actions Workflow

**Agent:** Build Automation Specialist  
**Effort:** 4 hours  
**Dependencies:** Batch 2 complete (generators functional)

**Rationale:** Build Automation Specialist specializes in CI/CD workflows and GitHub Actions.

**Description:**
Implement a GitHub Actions workflow (`.github/workflows/generate-exports.yml`) that:
- **Triggers:** On commit to `.github/agents/`, on PR, on tag/release
- **Steps:**
  1. Checkout code
  2. Install dependencies (`npm ci`)
  3. Run parser on all agents
  4. Generate all exports (OpenCode, Copilot, MCP)
  5. Validate exports (schema validation, hash verification)
  6. Upload artifacts (GitHub Actions artifacts, GitHub Releases on tag)
- **Optimization:** Cache dependencies, parallel processing where possible
- **Error handling:** Fail fast on validation errors, clear error messages

**Inputs:**
- Generator modules (from Batch 2)
- Validator module (from Batch 1 + enhancements in Task 3.3)
- GitHub Actions documentation

**Outputs:**
- `.github/workflows/generate-exports.yml` (workflow file)
- Workflow documentation: `docs/ci-cd/workflow-guide.md`
- Sample workflow run (manual trigger to test)

**Success Criteria:**
- ✅ Workflow runs successfully on commit
- ✅ Build time <5 minutes (from commit to artifacts)
- ✅ Artifacts downloadable from GitHub Actions
- ✅ Workflow fails on validation errors (negative test)

---

### Task 3.2: Implement Unit Tests for All Components

**Agent:** Reviewer Rachel (primary) + Backend Benny (support)  
**Effort:** 8 hours  
**Dependencies:** Batch 2 complete (all components implemented)

**Rationale:** Reviewer Rachel specializes in testing and quality assurance; Backend Benny supports with component-specific test logic.

**Description:**
Create comprehensive unit test suite for all export pipeline components:
- **Parser tests:** Edge cases (missing fields, malformed YAML, multi-line content)
- **Generator tests:** OpenCode, Copilot, MCP (valid IR → valid exports)
- **Validator tests:** Schema validation, error reporting, format compliance
- **Governance extractor tests:** Directive extraction, uncertainty thresholds, priority inference
- **Manifest generator tests:** Catalog generation, metadata completeness

Use Jest framework with:
- Fixtures for test data (`tests/fixtures/`)
- Mocks for file I/O (avoid dependency on actual files during tests)
- Coverage reporting (target >80%)

**Inputs:**
- All generator modules (from Batch 2)
- Parser and validator (from Batch 1)
- Test requirements (from tech design document)

**Outputs:**
- Unit test files: `tests/unit/{component}.test.js`
- Fixtures: `tests/fixtures/` (IR, schemas, sample exports)
- Coverage report: Jest HTML coverage report

**Success Criteria:**
- ✅ Unit tests pass with 100% success rate
- ✅ Code coverage >80% for parser, generators, validator
- ✅ Tests run in <30 seconds (fast feedback loop)
- ✅ Tests catch intentional errors (negative test cases included)

---

### Task 3.3: Implement Integration Tests (End-to-End Pipeline)

**Agent:** Reviewer Rachel  
**Effort:** 4 hours  
**Dependencies:** Task 3.2 (unit tests complete)

**Rationale:** Reviewer Rachel designs integration test scenarios; validates full pipeline.

**Description:**
Create integration tests that validate the entire export pipeline from markdown files to validated exports:
- **Test Scenario 1:** Parse all 17 agents → generate all formats → validate all exports
- **Test Scenario 2:** Modify 1 agent → re-generate exports → verify only affected files changed
- **Test Scenario 3:** Intentional error (malformed YAML) → verify pipeline fails gracefully
- **Test Scenario 4:** Hash verification (manual edit to generated file) → verify detection

Use test harness that:
- Sets up temporary directories for generated files
- Runs full pipeline (parser → generators → validators)
- Asserts on expected outputs (file existence, validation pass/fail)
- Cleans up after tests

**Inputs:**
- All pipeline components (parser, generators, validator)
- Agent files (`.github/agents/*.agent.md`)

**Outputs:**
- Integration test file: `tests/integration/export-pipeline.test.js`
- Test documentation: `docs/testing/integration-test-guide.md`

**Success Criteria:**
- ✅ Integration tests pass with 100% success rate
- ✅ Tests validate end-to-end pipeline (markdown → exports)
- ✅ Tests catch pipeline failures (error handling validated)
- ✅ Tests run in <2 minutes

---

### Task 3.4: Implement Acceptance Tests (User Integration Scenarios)

**Agent:** Reviewer Rachel (test design) + Scribe (scenario authoring)  
**Effort:** 4 hours (2h Rachel + 2h Scribe)  
**Dependencies:** Batch 2 complete (exports available for user simulation)

**Rationale:** Reviewer Rachel designs acceptance criteria; Scribe authors user-facing scenarios.

**Description:**
Create acceptance tests that simulate real user integration workflows:
- **Scenario 1:** User discovers agents using OpenCode manifest → loads agent definition → validates inputs/outputs
- **Scenario 2:** User integrates Architect agent in <30 minutes → follows user guide → successful invocation
- **Scenario 3:** User checks governance requirements → accesses directive metadata → validates escalation rules
- **Scenario 4:** User navigates multi-agent workflows → discovers handoff protocols → validates orchestration

Tests should:
- Use generated exports (not source markdown files)
- Follow documented user guides (validate documentation accuracy)
- Measure integration time (automated timing assertions)
- Validate user-facing outputs (manifests, schemas, examples)

**Inputs:**
- Generated exports (from Batch 2)
- User guides (from Batch 4, early drafts)
- Acceptance criteria (from ADR-013)

**Outputs:**
- Acceptance test file: `tests/acceptance/user-integration.test.js`
- Test scenarios documentation: `docs/testing/acceptance-scenarios.md`

**Success Criteria:**
- ✅ Acceptance tests pass with 100% success rate
- ✅ Integration time <30 minutes validated (automated timing)
- ✅ Tests validate user-facing documentation accuracy
- ✅ Tests catch documentation gaps (if guide incomplete, test fails)

---

### Task 3.5: Implement Hash Verification

**Agent:** Backend Benny  
**Effort:** 2 hours  
**Dependencies:** Task 3.1 (CI/CD workflow where hash verification will run)

**Rationale:** Backend Benny implements integrity checking logic.

**Description:**
Enhance validator with hash verification that:
- Computes hash of source markdown file (SHA-256)
- Embeds truncated hash (first 16 chars) in generated exports (metadata field)
- Validates that embedded hash matches source file hash during CI/CD
- Detects manual edits to generated files (hash mismatch indicates tampering)
- Reports hash mismatches with clear error messages (which file, expected vs. actual)

Add hash verification to:
- OpenCode exports (`.agent.metadata.source_hash`)
- Copilot exports (custom field `x-source-hash`)
- MCP exports (custom field `x-source-hash`)

**Inputs:**
- Generated exports (from Batch 2)
- Source markdown files
- Validator framework (from Batch 1)

**Outputs:**
- Enhanced validator: `tools/exporters/validator.js` (hash verification logic added)
- Unit tests: `tests/unit/hash-verification.test.js`
- CI/CD integration: Hash verification step in workflow

**Success Criteria:**
- ✅ Hash verification detects manual edits (negative test)
- ✅ Hash verification passes for unmodified exports (positive test)
- ✅ CI/CD fails build if hash mismatch detected
- ✅ Error messages clearly indicate which file has mismatch

---

### Task 3.6: Optimize Pipeline Performance

**Agent:** Backend Benny  
**Effort:** 2 hours  
**Dependencies:** Tasks 3.1-3.5 (full pipeline functional)

**Rationale:** Backend Benny optimizes service logic and performance.

**Description:**
Optimize export pipeline to meet <5 minute build time requirement:
- **Parallel processing:** Generate OpenCode, Copilot, MCP exports concurrently
- **Incremental exports:** (Future enhancement) Only regenerate changed agents (deferred to v1.1 per plan)
- **Caching:** Reuse parsed IR if source file unchanged (cache invalidation via hash)
- **Streaming:** Use streams for large manifest files
- **Profiling:** Identify bottlenecks (parser, generators, validators)

Run benchmarks:
- Baseline: Sequential processing
- Optimized: Parallel processing + caching
- Target: <5 minutes for 17 agents, all 3 formats

**Inputs:**
- Full pipeline (all components)
- Profiling tools (Node.js profiler, benchmarking scripts)

**Outputs:**
- Optimized pipeline code (refactored generators, parallelization logic)
- Benchmark report: `docs/performance/benchmark-results.md`
- Performance documentation: `docs/performance/optimization-guide.md`

**Success Criteria:**
- ✅ Build time <5 minutes (measured in CI/CD)
- ✅ Benchmarks show performance improvement (baseline vs. optimized)
- ✅ No regression in test pass rates (optimization doesn't break functionality)

---

### Batch 3 Summary

| Task | Agent | Effort | Dependencies | Output |
|------|-------|--------|--------------|--------|
| 3.1 | Build Automation | 4h | Batch 2 | GitHub Actions workflow |
| 3.2 | Reviewer Rachel + Benny | 8h | Batch 2 | Unit tests |
| 3.3 | Reviewer Rachel | 4h | 3.2 | Integration tests |
| 3.4 | Reviewer Rachel + Scribe | 4h | Batch 2 | Acceptance tests |
| 3.5 | Backend Benny | 2h | 3.1 | Hash verification |
| 3.6 | Backend Benny | 2h | 3.1-3.5 | Performance optimization |
| **Total** | | **24h** | | **Automation Complete** |

**Milestone 3 Validation:**
- Run CI/CD workflow on commit → validate <5 minute build time
- Run all tests (unit, integration, acceptance) → validate 100% pass rate
- Trigger intentional error → validate CI/CD fails gracefully
- Measure performance → validate benchmarks meet targets

---

## Batch 4: Documentation & Release (Week 4, 20 hours)

**Objective:** Complete user-facing documentation, validate integration experience, and prepare v1.0.0 release.

---

### Task 4.1: Write OpenCode Integration User Guide

**Agent:** Scribe  
**Effort:** 3 hours  
**Dependencies:** Batch 2 complete (OpenCode exports available)

**Rationale:** Scribe specializes in user-facing technical documentation.

**Description:**
Write comprehensive user guide for integrating agents using OpenCode exports:
- **Audience:** Developers unfamiliar with saboteurs framework
- **Goal:** Enable <30 minute integration
- **Content:**
  1. Introduction: What is OpenCode? Why use it?
  2. Prerequisites: Tools, environments, dependencies
  3. Quick Start: 5-minute walkthrough (discover → load → invoke)
  4. Detailed Guide: Discovery, definition files, governance extensions
  5. Examples: Architect agent integration (step-by-step)
  6. Troubleshooting: Common issues, error messages
  7. Advanced: Custom governance tooling, multi-agent workflows

**Inputs:**
- OpenCode exports (from Batch 2)
- OpenCode specification (for reference)
- Acceptance test scenarios (from Task 3.4)

**Outputs:**
- `docs/user-guides/opencode-integration-guide.md`
- Code examples: `examples/opencode/` (sample integration scripts)

**Success Criteria:**
- ✅ Guide enables <30 minute integration (validated via acceptance test)
- ✅ Guide reviewed by Reviewer Rachel (clarity, accuracy)
- ✅ Guide includes troubleshooting section (common errors addressed)

---

### Task 4.2: Write GitHub Copilot Skills Integration User Guide

**Agent:** Scribe  
**Effort:** 2 hours  
**Dependencies:** Batch 2 complete (Copilot exports available)

**Rationale:** Scribe reuses guide structure from Task 4.1 for consistency.

**Description:**
Write user guide for integrating agents using GitHub Copilot Skills exports (similar structure to Task 4.1):
- Quick Start: Load skill into Copilot
- Examples: Backend Benny skill usage
- Governance: Accessing directive metadata in Copilot
- Troubleshooting: Copilot-specific issues

**Inputs:**
- Copilot exports (from Batch 2)
- GitHub Copilot Skills documentation
- OpenCode guide (reference structure)

**Outputs:**
- `docs/user-guides/copilot-integration-guide.md`
- Code examples: `examples/copilot/`

**Success Criteria:**
- ✅ Guide enables <30 minute integration
- ✅ Guide reviewed by Reviewer Rachel
- ✅ Copilot-specific features documented (examples, native integration)

---

### Task 4.3: Write MCP Integration User Guide

**Agent:** Scribe  
**Effort:** 2 hours  
**Dependencies:** Batch 2 complete (MCP exports available)

**Rationale:** Scribe completes guide trilogy for all 3 formats.

**Description:**
Write user guide for integrating agents using Model Context Protocol exports (similar structure):
- Quick Start: MCP server setup
- Examples: Reviewer Rachel MCP integration
- Governance: Custom extensions in MCP
- Troubleshooting: MCP server issues

**Inputs:**
- MCP exports (from Batch 2)
- MCP specification documentation
- OpenCode/Copilot guides (reference structure)

**Outputs:**
- `docs/user-guides/mcp-integration-guide.md`
- Code examples: `examples/mcp/`

**Success Criteria:**
- ✅ Guide enables <30 minute integration
- ✅ Guide reviewed by Reviewer Rachel
- ✅ MCP-specific features documented (servers, resources, tools)

---

### Task 4.4: Write Migration Guide (Adding Schemas to Agents)

**Agent:** Scribe  
**Effort:** 2 hours  
**Dependencies:** Task 1.3 (schema conventions defined)

**Rationale:** Scribe documents contributor workflows.

**Description:**
Write migration guide for contributors who want to add or update schemas in agent profiles:
- **Audience:** Framework contributors, agent authors
- **Goal:** Enable adding schemas to existing agents or new agents
- **Content:**
  1. Schema conventions overview
  2. Step-by-step: Add input/output schema to existing agent
  3. Examples: Before/after (agent profile with/without schemas)
  4. Validation: How to test schemas
  5. Schema checklist: Required elements, validations
  6. Best practices: Schema design, examples, documentation

**Inputs:**
- Schema conventions (from Task 1.3)
- Sample schemas (from Batch 1 and Batch 2)
- JSON Schema specification

**Outputs:**
- `docs/migration-guide.md`
- Schema templates: `templates/schema-template.json`

**Success Criteria:**
- ✅ Contributors can add schemas independently (validated via peer review)
- ✅ Guide includes examples and checklist
- ✅ Guide reviewed by Architect Alphonso (technical accuracy)

---

### Task 4.5: Write Custom Extension Schema Documentation

**Agent:** Scribe  
**Effort:** 2 hours  
**Dependencies:** Task 2.5 (governance extensions implemented)

**Rationale:** Scribe documents technical specifications for developers.

**Description:**
Document the custom governance extensions schema for developers building tooling around saboteurs exports:
- **Audience:** Tool developers, platform integrators
- **Goal:** Enable custom tooling that leverages governance metadata
- **Content:**
  1. Extension overview: Why custom extensions? What data do they contain?
  2. Schema specifications: `extensions.saboteurs_governance`, `extensions.multi_agent`
  3. Field reference: Directive structure, uncertainty thresholds, orchestration protocols
  4. Examples: Sample governance metadata from 3 agents
  5. Use cases: Building governance dashboards, compliance tools, orchestration engines

**Inputs:**
- Governance extensions implementation (from Task 2.5)
- Sample exports with extensions (from Batch 2)

**Outputs:**
- `docs/technical/custom-extensions.md`
- JSON Schema: `schemas/saboteurs-extensions.schema.json` (formal spec)

**Success Criteria:**
- ✅ Extension schema documented with examples
- ✅ Tool developers can parse governance metadata (validated via review)
- ✅ Documentation reviewed by Backend Benny (technical accuracy)

---

### Task 4.6: Write Contributing Guide (Agent Authoring)

**Agent:** Scribe  
**Effort:** 2 hours  
**Dependencies:** Tasks 4.4, 4.5 (migration guide, extension docs available)

**Rationale:** Scribe documents contributor workflows.

**Description:**
Write comprehensive contributing guide for adding or modifying agents:
- **Audience:** New contributors, agent authors
- **Goal:** Enable adding new agents with complete schemas and governance metadata
- **Content:**
  1. Agent profile structure (YAML frontmatter, narrative sections)
  2. Schema requirements (input/output schemas, examples)
  3. Governance metadata (directives, collaboration contracts)
  4. Testing: How to validate new agents (parser, exports, CI/CD)
  5. PR checklist: Required elements for agent PRs
  6. Style guide: Naming conventions, documentation standards

**Inputs:**
- Agent profile samples (existing `.agent.md` files)
- Migration guide (from Task 4.4)
- Custom extensions docs (from Task 4.5)

**Outputs:**
- `docs/contributing.md`
- PR checklist template: `.github/PULL_REQUEST_TEMPLATE/agent-addition.md`

**Success Criteria:**
- ✅ Contributors can add agents independently (validated via peer review)
- ✅ Guide covers schema, governance, testing requirements
- ✅ Guide reviewed by Curator Claire (style, organization)

---

### Task 4.7: Update README with Badges, Quick-Start, Download Links

**Agent:** Curator Claire  
**Effort:** 2 hours  
**Dependencies:** Batch 3 complete (CI/CD functional)

**Rationale:** Curator Claire specializes in content organization and README quality.

**Description:**
Update repository README to showcase multi-format distribution:
- **Badges:** CI/CD status, test coverage, release version, format support
- **Quick-Start:** 5-minute "Get Started" section (discover agents, download exports)
- **Download Links:** GitHub Releases, format-specific downloads (OpenCode, Copilot, MCP)
- **Format Support:** Table showing supported formats with links to user guides
- **Governance Highlight:** Brief mention of governance sophistication (key differentiator)
- **Contributing:** Link to contributing guide

**Inputs:**
- Existing README
- User guides (from Tasks 4.1-4.3)
- CI/CD status (from Batch 3)

**Outputs:**
- Updated `README.md`
- README review by Reviewer Rachel (quality check)

**Success Criteria:**
- ✅ README is compelling and informative (first impression)
- ✅ Quick-start enables discovery in <5 minutes
- ✅ Download links are correct and functional
- ✅ README reviewed by Reviewer Rachel (clarity, accuracy)

---

### Task 4.8: Create CHANGELOG and Release Notes

**Agent:** Curator Claire  
**Effort:** 1 hour  
**Dependencies:** All Batches complete (full feature set implemented)

**Rationale:** Curator Claire documents release history and features.

**Description:**
Create CHANGELOG documenting v1.0.0 release:
- **Format:** Keep a Changelog (https://keepachangelog.com/)
- **Content:**
  - **Added:** Multi-format distribution (OpenCode, Copilot, MCP), CI/CD automation, schemas for all agents, governance extensions
  - **Changed:** Agent profiles now include schemas (backward-compatible)
  - **Fixed:** N/A (initial release)
  - **Known Issues:** Incremental exports not supported (future enhancement)

Write release notes for GitHub Release v1.0.0:
- High-level overview (what's new, why it matters)
- Installation instructions (download, integrate)
- Links to documentation (user guides, contributing)
- Acknowledgments (contributors, reviewers)

**Inputs:**
- Implementation plan (this document)
- ADR-013 (strategic context)
- User guides (for documentation links)

**Outputs:**
- `CHANGELOG.md`
- Release notes: `docs/releases/v1.0.0-release-notes.md`

**Success Criteria:**
- ✅ CHANGELOG follows standard format
- ✅ Release notes are clear and comprehensive
- ✅ Documentation links are correct

---

### Task 4.9: Prepare v1.0.0 Release Package

**Agent:** Build Automation Specialist  
**Effort:** 2 hours  
**Dependencies:** All Batches complete; Tasks 4.7, 4.8 (README, CHANGELOG ready)

**Rationale:** Build Automation Specialist manages release workflows.

**Description:**
Prepare v1.0.0 release artifacts for GitHub Releases:
- **Tag:** Create Git tag `v1.0.0`
- **Artifacts:** Build distribution packages:
  - `saboteurs-agents-framework-v1.0.0.tar.gz` (source + all exports)
  - `opencode-exports-v1.0.0.zip` (OpenCode only)
  - `copilot-exports-v1.0.0.zip` (Copilot only)
  - `mcp-exports-v1.0.0.zip` (MCP only)
- **GitHub Release:** Create draft release with:
  - Release notes (from Task 4.8)
  - Attached artifacts (downloadable)
  - Documentation links (README, user guides)

**Inputs:**
- Generated exports (from CI/CD)
- CHANGELOG and release notes (from Task 4.8)
- README (from Task 4.7)

**Outputs:**
- Git tag `v1.0.0`
- GitHub Release (draft, ready for approval)
- Release artifacts (validated, downloadable)

**Success Criteria:**
- ✅ Release artifacts are complete and validated
- ✅ GitHub Release draft is ready for approval
- ✅ Artifacts are downloadable and functional
- ✅ Release correlates to CI/CD build (traceable)

---

### Task 4.10: Final Quality Review and Acceptance

**Agent:** Reviewer Rachel + Curator Claire  
**Effort:** 2 hours (1h Rachel + 1h Claire)  
**Dependencies:** Tasks 4.1-4.9 (all documentation and release artifacts ready)

**Rationale:** Reviewer Rachel validates quality; Curator Claire reviews content organization.

**Description:**
Conduct final quality review before v1.0.0 release:
- **Reviewer Rachel:**
  - Validate all acceptance tests pass
  - Verify integration time <30 minutes (manual walkthrough)
  - Check CI/CD pipeline (stable, <5 min build time)
  - Review test coverage reports (>80%)
  - Validate hash verification (manual edit detection)

- **Curator Claire:**
  - Review all documentation (user guides, contributing, README)
  - Check documentation consistency (terminology, formatting)
  - Validate links (internal, external)
  - Review CHANGELOG and release notes (clarity, completeness)
  - Assess documentation organization (findability, structure)

**Inputs:**
- All documentation (from Tasks 4.1-4.8)
- Release artifacts (from Task 4.9)
- Test reports (from Batch 3)

**Outputs:**
- Quality review report: `work/planning/v1.0.0-quality-review.md`
- Go/no-go recommendation for release
- List of any critical issues (if found, delay release)

**Success Criteria:**
- ✅ All acceptance criteria met (from implementation plan)
- ✅ Documentation is complete and accurate
- ✅ No critical issues identified
- ✅ Recommendation: GO for v1.0.0 release

---

### Batch 4 Summary

| Task | Agent | Effort | Dependencies | Output |
|------|-------|--------|--------------|--------|
| 4.1 | Scribe | 3h | Batch 2 | OpenCode user guide |
| 4.2 | Scribe | 2h | Batch 2 | Copilot user guide |
| 4.3 | Scribe | 2h | Batch 2 | MCP user guide |
| 4.4 | Scribe | 2h | 1.3 | Migration guide |
| 4.5 | Scribe | 2h | 2.5 | Custom extensions docs |
| 4.6 | Scribe | 2h | 4.4, 4.5 | Contributing guide |
| 4.7 | Curator Claire | 2h | Batch 3 | README update |
| 4.8 | Curator Claire | 1h | All batches | CHANGELOG + release notes |
| 4.9 | Build Automation | 2h | 4.7, 4.8 | v1.0.0 release package |
| 4.10 | Reviewer + Curator | 2h | 4.1-4.9 | Final quality review |
| **Total** | | **20h** | | **Release Ready** |

**Milestone 4 Validation:**
- Manual integration test (follow user guides) → validate <30 min time
- Documentation review (peer review) → validate completeness
- Release artifacts validation → verify downloads work
- Final go/no-go decision → approve v1.0.0 release

---

## Cross-Batch Coordination

### Dependency Map (Visual)

```
Batch 1: Foundation
  ├── 1.1 IR Structure (Architect) → 1.2, 2.1-2.3
  ├── 1.2 Parser (Benny) → 1.3, 2.1-2.6, 3.1-3.6
  ├── 1.3 Schema Conventions (Architect) → 1.4, 2.4
  ├── 1.4 5 Agent Schemas (Benny + Architect) → 2.4, 3.2
  └── 1.5 Base Validator (Benny) → 3.2, 3.3, 3.5

Batch 2: Export Pipeline
  ├── 2.1 OpenCode Generator (Benny) → 2.2, 2.3, 3.1-3.4
  ├── 2.2 Copilot Generator (Benny) → 2.3, 3.1-3.4
  ├── 2.3 MCP Generator (Benny) → 3.1-3.4
  ├── 2.4 12 Agent Schemas (Architect + Scribe) → 3.2, 4.4
  ├── 2.5 Governance Extensions (Benny) → 3.2, 4.5
  └── 2.6 Manifest Generators (Benny) → 3.2, 3.3

Batch 3: Automation
  ├── 3.1 CI/CD Workflow (Build Auto) → 3.5, 3.6, 4.7, 4.9
  ├── 3.2 Unit Tests (Rachel + Benny) → 3.3, 4.10
  ├── 3.3 Integration Tests (Rachel) → 4.10
  ├── 3.4 Acceptance Tests (Rachel + Scribe) → 4.1-4.3, 4.10
  ├── 3.5 Hash Verification (Benny) → 4.10
  └── 3.6 Performance Optimization (Benny) → 4.10

Batch 4: Documentation
  ├── 4.1-4.3 User Guides (Scribe) → 4.10
  ├── 4.4 Migration Guide (Scribe) → 4.6, 4.10
  ├── 4.5 Extensions Docs (Scribe) → 4.6, 4.10
  ├── 4.6 Contributing Guide (Scribe) → 4.10
  ├── 4.7 README (Curator) → 4.9
  ├── 4.8 CHANGELOG (Curator) → 4.9
  ├── 4.9 Release Package (Build Auto) → 4.10
  └── 4.10 Final Review (Rachel + Curator) → v1.0.0 Release
```

### Parallel Work Opportunities

**Week 1 (Batch 1):**
- Sequential (no parallelization due to foundational dependencies)

**Week 2 (Batch 2):**
- **Parallel Stream A:** Backend Benny → OpenCode generator (2.1) → Copilot generator (2.2) → MCP generator (2.3)
- **Parallel Stream B:** Architect Alphonso + Scribe → Schema completion (2.4) [6 agents each, concurrent]
- **Sequential:** Governance extensions (2.5) → Manifest generators (2.6) [depends on 2.1-2.3]

**Week 3 (Batch 3):**
- **Parallel Stream A:** Build Automation → CI/CD workflow (3.1)
- **Parallel Stream B:** Reviewer Rachel + Backend Benny → Unit tests (3.2) [concurrent with 3.1]
- **Sequential:** Integration tests (3.3) → Acceptance tests (3.4) [depends on 3.2]
- **Parallel Stream C:** Backend Benny → Hash verification (3.5) + Performance optimization (3.6) [concurrent with 3.3-3.4]

**Week 4 (Batch 4):**
- **Parallel Stream A:** Scribe → User guides (4.1, 4.2, 4.3) [concurrent]
- **Parallel Stream B:** Scribe → Migration guide (4.4) + Extensions docs (4.5) → Contributing guide (4.6) [sequential within stream]
- **Parallel Stream C:** Curator Claire → README (4.7) + CHANGELOG (4.8) [concurrent]
- **Sequential:** Release package (4.9) → Final review (4.10) [depends on all previous tasks]

---

## Effort Summary by Agent

| Agent | Batch 1 | Batch 2 | Batch 3 | Batch 4 | Total |
|-------|---------|---------|---------|---------|-------|
| **Architect Alphonso** | 5h (1.1, 1.3) | 8h (2.4, reviews) | — | — | **13h** |
| **Backend Benny** | 10h (1.2, 1.4, 1.5) | 21h (2.1-2.3, 2.5, 2.6) | 12h (3.2, 3.5, 3.6) | — | **43h** |
| **Build Automation** | — | — | 4h (3.1) | 2h (4.9) | **6h** |
| **Reviewer Rachel** | — | — | 12h (3.2-3.4) | 1h (4.10) | **13h** |
| **Scribe** | — | 4h (2.4) | 2h (3.4) | 11h (4.1-4.6) | **17h** |
| **Curator Claire** | — | — | — | 5h (4.7, 4.8, 4.10) | **5h** |
| **Total** | **16h** | **28h** | **24h** | **20h** | **88h** |

---

## Task Status Tracking Template

Use this template to track task completion:

```markdown
## Task [ID]: [Task Name]

**Agent:** [Agent Name]  
**Status:** ⏳ Not Started / 🔄 In Progress / ✅ Complete / ❌ Blocked  
**Progress:** [0-100]%  
**Started:** [Date]  
**Completed:** [Date]  
**Effort (Actual):** [Hours]  

**Blockers:**
- ❗️ [Blocker description] (Owner: [Agent], ETA: [Date])

**Notes:**
- [Any relevant notes, decisions, or issues]
```

---

## Success Criteria by Batch

### Batch 1 Success Criteria
- ✅ Parser processes all 17 agents without errors
- ✅ 5 agent schemas validate against JSON Schema spec
- ✅ IR structure documented and approved
- ✅ Base validator functional (schema validation capability)

### Batch 2 Success Criteria
- ✅ All 16 agents export to OpenCode, Copilot, MCP
- ✅ Governance extensions present in all exports
- ✅ 17 agent schemas complete and validated
- ✅ Manual integration test successful (1 agent)

### Batch 3 Success Criteria
- ✅ CI/CD workflow runs successfully (<5 min build time)
- ✅ Unit test coverage >80% (parser, generators, validator)
- ✅ Integration and acceptance tests pass (100%)
- ✅ Hash verification detects manual edits

### Batch 4 Success Criteria
- ✅ User guides complete (OpenCode, Copilot, MCP)
- ✅ Integration time <30 minutes (validated)
- ✅ Documentation reviewed and approved
- ✅ v1.0.0 release package ready

---

## References

**Related Planning Documents:**
- Implementation Plan: `work/planning/multi-format-distribution-implementation-plan.md`
- Milestone Checklist: `work/planning/milestone-checklist.md`

**Related Analysis Documents:**
- ADR-013: `work/analysis/ADR-013-multi-format-distribution.md`
- Technical Design: `work/analysis/tech-design-export-pipeline.md`
- Formal Technical Assessment: `work/analysis/formal-technical-assessment.md`

**Agent Profiles:**
- Architect Alphonso: `.github/agents/architect-alphonso.agent.md`
- Backend Benny: `.github/agents/backend-benny.agent.md`
- Build Automation Specialist: `.github/agents/build-automation-specialist.agent.md`
- Reviewer Rachel: `.github/agents/reviewer-rachel.agent.md`
- Scribe: `.github/agents/scribe.agent.md`
- Curator Claire: `.github/agents/curator-claire.agent.md`

---

**Document Version:** 1.0.0  
**Date:** 2026-01-29  
**Status:** Draft (Pending Review)  
**Author:** Planning Petra
