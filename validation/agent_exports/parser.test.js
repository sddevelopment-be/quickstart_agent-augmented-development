/**
 * Parser Acceptance Tests
 * 
 * Following Directive 016 (ATDD) - Acceptance tests written FIRST
 * These tests define the expected behavior of the complete parser system
 * 
 * Test Strategy:
 * 1. Parse complete agent files with all fields
 * 2. Handle missing optional fields gracefully
 * 3. Handle malformed input with clear errors
 * 4. Performance requirements (<2 seconds for all agents)
 * 5. Validate against example IR fixtures
 */

const { parseAgentFile, parseAgentDirectory } = require('../../ops/exporters/parser');
const fs = require('fs').promises;
const path = require('path');

describe('Parser Acceptance Tests', () => {
  const agentsDir = path.join(__dirname, '../../.github/agents');
  const fixturesDir = path.join(__dirname, '../fixtures/ir');

  describe('Parse complete agent files', () => {
    it('should parse architect.agent.md and match expected IR structure', async () => {
      const filePath = path.join(agentsDir, 'architect.agent.md');
      const ir = await parseAgentFile(filePath);

      // Validate top-level structure
      expect(ir).toHaveProperty('ir_version', '1.0.0');
      expect(ir).toHaveProperty('frontmatter');
      expect(ir).toHaveProperty('content');
      expect(ir).toHaveProperty('relationships');
      expect(ir).toHaveProperty('governance');
      expect(ir).toHaveProperty('metadata');

      // Validate frontmatter
      expect(ir.frontmatter.name).toBe('architect-alphonso');
      expect(ir.frontmatter.description).toBe('Clarify complex systems with contextual trade-offs.');
      expect(ir.frontmatter.tools).toContain('plantuml');
      expect(Array.isArray(ir.frontmatter.tools)).toBe(true);

      // Validate content sections
      expect(ir.content.purpose).toBeTruthy();
      expect(ir.content.purpose).toContain('Clarify and decompose');
      expect(ir.content.specialization).toBeTruthy();
      expect(ir.content.collaboration_contract).toBeTruthy();
      expect(ir.content.success_criteria).toBeTruthy();
      expect(Array.isArray(ir.content.mode_defaults)).toBe(true);
      expect(ir.content.mode_defaults.length).toBeGreaterThan(0);

      // Validate relationships
      expect(Array.isArray(ir.relationships.directives)).toBe(true);
      expect(ir.relationships.directives.length).toBeGreaterThan(0);
      expect(ir.relationships.directives[0]).toHaveProperty('code');
      expect(ir.relationships.directives[0]).toHaveProperty('title');

      // Validate governance
      expect(ir.governance).toHaveProperty('directive_requirements');
      expect(ir.governance).toHaveProperty('uncertainty_threshold');
      expect(ir.governance.primer_required).toBeDefined();
      expect(ir.governance.test_first_required).toBeDefined();

      // Validate metadata
      expect(ir.metadata.file_path).toBe('.github/agents/architect.agent.md');
      expect(ir.metadata.source_hash).toMatch(/^[a-f0-9]{64}$/);
      expect(ir.metadata.parsed_at).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/);
      expect(ir.metadata.file_size).toBeGreaterThan(0);
      expect(ir.metadata.parser_version).toBe('1.0.0');
    });

    it('should parse backend-dev.agent.md successfully', async () => {
      const filePath = path.join(agentsDir, 'backend-dev.agent.md');
      const ir = await parseAgentFile(filePath);

      expect(ir.frontmatter.name).toBe('backend-benny');
      expect(ir.frontmatter.description).toBeTruthy();
      expect(ir.frontmatter.tools).toContain('Bash');
      expect(ir.content.purpose).toBeTruthy();
      expect(ir.metadata.source_hash).toMatch(/^[a-f0-9]{64}$/);
    });

    it('should parse curator.agent.md successfully', async () => {
      const filePath = path.join(agentsDir, 'curator.agent.md');
      const ir = await parseAgentFile(filePath);

      expect(ir.frontmatter.name).toBe('curator-claire');
      expect(ir.content.purpose).toBeTruthy();
      expect(Array.isArray(ir.relationships.directives)).toBe(true);
    });
  });

  describe('Handle missing optional fields', () => {
    it('should apply default version when frontmatter.version is missing', async () => {
      // We'll create a minimal test fixture
      const minimalAgent = `---
name: test-agent
description: A test agent
tools: ["read", "write"]
---

## 2. Purpose

Test purpose content.

## 3. Specialization

Test specialization.

## 4. Collaboration Contract

Test contract.

## 5. Mode Defaults

| Mode | Description | Use Case |
|------|-------------|----------|
| /analysis-mode | Testing | Test cases |
`;
      const testPath = path.join(__dirname, '../fixtures/agents/minimal-agent.md');
      await fs.writeFile(testPath, minimalAgent, 'utf-8');

      const ir = await parseAgentFile(testPath);
      
      expect(ir.frontmatter.version).toBe('1.0.0');
      expect(ir.frontmatter.name).toBe('test-agent');
    });

    it('should handle missing optional content sections gracefully', async () => {
      const minimalAgent = `---
name: minimal-test
description: Minimal agent
tools: ["read"]
---

## 2. Purpose

Minimal purpose.

## 3. Specialization

Minimal spec.

## 4. Collaboration Contract

Minimal contract.

## 5. Mode Defaults

| Mode | Description | Use Case |
|------|-------------|----------|
| /analysis-mode | Test | Test |
`;
      const testPath = path.join(__dirname, '../fixtures/agents/minimal-no-optional.md');
      await fs.writeFile(testPath, minimalAgent, 'utf-8');

      const ir = await parseAgentFile(testPath);
      
      // Optional fields should be null or empty
      expect(ir.content.output_artifacts).toBeNull();
      expect(ir.content.operating_procedure).toBeNull();
    });
  });

  describe('Error handling', () => {
    it('should fail with clear error on malformed YAML', async () => {
      const malformedAgent = `---
name: test
description: [unclosed array
tools: ["read"]
---

## 2. Purpose
Test`;
      const testPath = path.join(__dirname, '../fixtures/agents/malformed-yaml.md');
      await fs.writeFile(testPath, malformedAgent, 'utf-8');

      await expect(parseAgentFile(testPath)).rejects.toThrow(/YAML/);
    });

    it('should fail with clear error on missing frontmatter', async () => {
      const noFrontmatter = `## 2. Purpose

Test purpose without frontmatter.`;
      const testPath = path.join(__dirname, '../fixtures/agents/no-frontmatter.md');
      await fs.writeFile(testPath, noFrontmatter, 'utf-8');

      await expect(parseAgentFile(testPath)).rejects.toThrow(/frontmatter/);
    });

    it('should fail with clear error on missing required fields', async () => {
      const missingRequired = `---
name: test-agent
---

## 2. Purpose
Test`;
      const testPath = path.join(__dirname, '../fixtures/agents/missing-required.md');
      await fs.writeFile(testPath, missingRequired, 'utf-8');

      await expect(parseAgentFile(testPath)).rejects.toThrow(/required field/);
    });
  });

  describe('Directory parsing', () => {
    it('should parse all agent files in directory', async () => {
      const agents = await parseAgentDirectory(agentsDir);

      expect(Array.isArray(agents)).toBe(true);
      expect(agents.length).toBeGreaterThan(10); // Should have ~16 agents
      
      // All agents should have valid structure
      agents.forEach(agent => {
        expect(agent.frontmatter.name).toBeTruthy();
        expect(agent.metadata.source_hash).toMatch(/^[a-f0-9]{64}$/);
      });
    });

    it('should complete parsing in under 2 seconds', async () => {
      const startTime = Date.now();
      await parseAgentDirectory(agentsDir);
      const duration = Date.now() - startTime;

      expect(duration).toBeLessThan(2000);
    });
  });

  describe('IR validation against fixtures', () => {
    it('should match architect-alphonso.ir.json structure', async () => {
      const filePath = path.join(agentsDir, 'architect.agent.md');
      const expectedPath = path.join(__dirname, '../../work/schemas/examples/ir/architect-alphonso.ir.json');
      
      const ir = await parseAgentFile(filePath);
      const expected = JSON.parse(await fs.readFile(expectedPath, 'utf-8'));

      // Compare key structure (hashes and timestamps will differ)
      expect(ir.frontmatter.name).toBe(expected.frontmatter.name);
      expect(ir.frontmatter.description).toBe(expected.frontmatter.description);
      expect(ir.frontmatter.tools).toEqual(expected.frontmatter.tools);
      expect(ir.content.purpose).toBe(expected.content.purpose);
      expect(ir.relationships.directives.length).toBe(expected.relationships.directives.length);
    });
  });

  describe('Unit Tests - Edge Cases', () => {
    it('should handle agent with no directive table', async () => {
      const noDirectives = `---
name: no-directives
description: Agent without directives
tools: ["read"]
---

## 2. Purpose

Purpose without directives.

## 3. Specialization

Specialization.

## 4. Collaboration Contract

Contract.

## 5. Mode Defaults

| Mode | Description | Use Case |
|------|-------------|----------|
| /analysis-mode | Test | Test |
`;
      const testPath = path.join(__dirname, '../fixtures/agents/no-directives.md');
      await fs.writeFile(testPath, noDirectives, 'utf-8');

      const ir = await parseAgentFile(testPath);
      
      expect(ir.relationships.directives).toEqual([]);
    });

    it('should handle agent with Test-First requirement', async () => {
      const testFirst = `---
name: test-first-only
description: Agent with test-first requirement
tools: ["read"]
---

**Test-First Requirement:** Follow Directives 016 (ATDD) and 017 (TDD) whenever authoring or modifying executable code.

## 2. Purpose

Purpose.

## 3. Specialization

Specialization.

## 4. Collaboration Contract

Contract with uncertainty >30%.

## 5. Mode Defaults

| Mode | Description | Use Case |
|------|-------------|----------|
| /analysis-mode | Test | Test |
`;
      const testPath = path.join(__dirname, '../fixtures/agents/test-first-only.md');
      await fs.writeFile(testPath, testFirst, 'utf-8');

      const ir = await parseAgentFile(testPath);
      
      // Should detect test-first requirement
      expect(ir.governance.test_first_required).toBe(true);
      expect(ir.governance.uncertainty_threshold).toBe('>30%');
    });

    it('should handle agent with subsections properly', async () => {
      const withSubsections = `---
name: subsections-test
description: Agent with subsections
tools: ["read", "write"]
---

## 2. Purpose

Main purpose.

## 3. Specialization

Specialization content.

## 4. Collaboration Contract

Contract content.

### Output Artifacts

These are the artifacts.

## 5. Mode Defaults

| Mode | Description | Use Case |
|------|-------------|----------|
| /analysis-mode | Test | Test |
`;
      const testPath = path.join(__dirname, '../fixtures/agents/subsections.md');
      await fs.writeFile(testPath, withSubsections, 'utf-8');

      const ir = await parseAgentFile(testPath);
      
      expect(ir.content.output_artifacts).toBeTruthy();
      expect(ir.content.output_artifacts).toContain('artifacts');
    });

    it('should handle empty mode defaults table', async () => {
      const noModes = `---
name: no-modes
description: Agent without modes
tools: ["read"]
---

## 2. Purpose

Purpose.

## 3. Specialization

Specialization.

## 4. Collaboration Contract

Contract.

## 5. Mode Defaults

No modes defined.
`;
      const testPath = path.join(__dirname, '../fixtures/agents/no-modes.md');
      await fs.writeFile(testPath, noModes, 'utf-8');

      const ir = await parseAgentFile(testPath);
      
      expect(ir.content.mode_defaults).toEqual([]);
    });
  });
});
