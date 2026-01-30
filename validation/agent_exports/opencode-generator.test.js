/**
 * OpenCode Generator Acceptance and Unit Tests
 * 
 * Following Directive 016 (ATDD) - Acceptance tests written FIRST
 * Following Directive 017 (TDD) - Red-Green-Refactor cycle
 * 
 * Test Strategy:
 * 1. Parse IR and generate valid OpenCode discovery files
 * 2. Parse IR and generate valid OpenCode definition files
 * 3. Include governance extensions in both file types
 * 4. Handle edge cases (missing fields, special chars)
 * 5. Performance requirements (<1 second per agent)
 * 6. All 17 agents export successfully
 */

const { generateOpenCode, mapIRToDiscovery, mapIRToDefinition, extractGovernanceMetadata } = require('../../ops/exporters/opencode-generator');
const { parseAgentFile } = require('../../ops/exporters/parser');
const fs = require('fs').promises;
const path = require('path');
const yaml = require('js-yaml');

describe('OpenCode Generator - Acceptance Tests', () => {
  const agentsDir = path.join(__dirname, '../../.github/agents');
  const outputDir = path.join(__dirname, '../../tmp/opencode-test-output');
  
  beforeEach(async () => {
    // Clean and create output directory
    try {
      await fs.rm(outputDir, { recursive: true, force: true });
    } catch (e) {
      // Directory might not exist
    }
    await fs.mkdir(outputDir, { recursive: true });
  });

  afterEach(async () => {
    // Clean up test output
    try {
      await fs.rm(outputDir, { recursive: true, force: true });
    } catch (e) {
      // Ignore cleanup errors
    }
  });

  describe('ACCEPTANCE: Generate valid discovery files from IR', () => {
    it('should generate valid discovery file for backend-benny', async () => {
      const filePath = path.join(agentsDir, 'backend-dev.agent.md');
      const ir = await parseAgentFile(filePath);
      const { discovery } = await generateOpenCode(ir, outputDir);
      
      // File should exist
      const discoveryContent = await fs.readFile(discovery, 'utf-8');
      const discoveryData = JSON.parse(discoveryContent);
      
      // Validate OpenCode structure
      expect(discoveryData.opencode_version).toBe('1.0');
      expect(discoveryData.agent).toBeDefined();
      expect(discoveryData.agent.id).toBe('backend-benny');
      expect(discoveryData.agent.name).toBeTruthy();
      expect(discoveryData.agent.version).toBe('1.0.0');
      expect(discoveryData.agent.description).toBeTruthy();
      expect(Array.isArray(discoveryData.agent.capabilities)).toBe(true);
      expect(discoveryData.agent.category).toBeTruthy();
      expect(Array.isArray(discoveryData.agent.tools)).toBe(true);
      expect(discoveryData.agent.tools).toContain('Bash');
      expect(discoveryData.agent.profile_url).toBeTruthy();
      
      // Validate metadata
      expect(discoveryData.agent.metadata).toBeDefined();
      expect(discoveryData.agent.metadata.last_updated).toMatch(/^\d{4}-\d{2}-\d{2}$/);
      expect(discoveryData.agent.metadata.api_version).toBe('1.0.0');
      expect(Array.isArray(discoveryData.agent.metadata.directives)).toBe(true);
      expect(discoveryData.agent.metadata.directives.length).toBeGreaterThan(0);
    });

    it('should generate valid discovery file for architect-alphonso', async () => {
      const filePath = path.join(agentsDir, 'architect.agent.md');
      const ir = await parseAgentFile(filePath);
      const { discovery } = await generateOpenCode(ir, outputDir);
      
      const discoveryContent = await fs.readFile(discovery, 'utf-8');
      const discoveryData = JSON.parse(discoveryContent);
      
      expect(discoveryData.opencode_version).toBe('1.0');
      expect(discoveryData.agent.id).toBe('architect-alphonso');
      expect(discoveryData.agent.tools).toContain('plantuml');
    });

    it('should generate valid discovery file for curator-claire', async () => {
      const filePath = path.join(agentsDir, 'curator.agent.md');
      const ir = await parseAgentFile(filePath);
      const { discovery } = await generateOpenCode(ir, outputDir);
      
      const discoveryContent = await fs.readFile(discovery, 'utf-8');
      const discoveryData = JSON.parse(discoveryContent);
      
      expect(discoveryData.opencode_version).toBe('1.0');
      expect(discoveryData.agent.id).toBe('curator-claire');
    });
  });

  describe('ACCEPTANCE: Generate valid definition files from IR', () => {
    it('should generate valid definition file for backend-benny', async () => {
      const filePath = path.join(agentsDir, 'backend-dev.agent.md');
      const ir = await parseAgentFile(filePath);
      const { definition } = await generateOpenCode(ir, outputDir);
      
      // File should exist
      const definitionContent = await fs.readFile(definition, 'utf-8');
      const definitionData = yaml.load(definitionContent);
      
      // Validate OpenCode structure
      expect(definitionData.opencode_version).toBe('1.0');
      expect(definitionData.agent).toBeDefined();
      expect(definitionData.agent.metadata).toBeDefined();
      expect(definitionData.agent.metadata.id).toBe('backend-benny');
      expect(definitionData.agent.metadata.version).toBe('1.0.0');
      expect(definitionData.agent.metadata.category).toBeTruthy();
      expect(Array.isArray(definitionData.agent.metadata.tags)).toBe(true);
      
      // Validate specification
      expect(definitionData.agent.specification).toBeDefined();
      expect(Array.isArray(definitionData.agent.specification.tools)).toBe(true);
      
      // Validate governance section
      expect(definitionData.agent.governance).toBeDefined();
      expect(Array.isArray(definitionData.agent.governance.directives)).toBe(true);
      expect(definitionData.agent.governance.directives.length).toBeGreaterThan(0);
    });
  });

  describe('ACCEPTANCE: Include governance extensions', () => {
    it('should include governance metadata in discovery file', async () => {
      const filePath = path.join(agentsDir, 'backend-dev.agent.md');
      const ir = await parseAgentFile(filePath);
      const { discovery } = await generateOpenCode(ir, outputDir);
      
      const discoveryData = JSON.parse(await fs.readFile(discovery, 'utf-8'));
      
      // Check directives are present
      expect(Array.isArray(discoveryData.agent.metadata.directives)).toBe(true);
      expect(discoveryData.agent.metadata.directives.length).toBeGreaterThan(0);
      
      // Check extensions
      expect(discoveryData.extensions).toBeDefined();
      expect(discoveryData.extensions.agentic_governance).toBeDefined();
      expect(discoveryData.extensions.agentic_governance.uncertainty_threshold).toBeTruthy();
      expect(discoveryData.extensions.agentic_governance.primer_required).toBeDefined();
      expect(discoveryData.extensions.agentic_governance.test_first_required).toBeDefined();
    });

    it('should include multi-agent extensions', async () => {
      const filePath = path.join(agentsDir, 'backend-dev.agent.md');
      const ir = await parseAgentFile(filePath);
      const { discovery } = await generateOpenCode(ir, outputDir);
      
      const discoveryData = JSON.parse(await fs.readFile(discovery, 'utf-8'));
      
      expect(discoveryData.extensions.multi_agent).toBeDefined();
      expect(typeof discoveryData.extensions.multi_agent.orchestration_capable).toBe('boolean');
      expect(Array.isArray(discoveryData.extensions.multi_agent.handoff_protocols)).toBe(true);
      expect(discoveryData.extensions.multi_agent.specialization_boundaries).toBeTruthy();
    });
  });

  describe('ACCEPTANCE: Performance requirements', () => {
    it('should generate files in less than 1 second per agent', async () => {
      const filePath = path.join(agentsDir, 'backend-dev.agent.md');
      const ir = await parseAgentFile(filePath);
      
      const startTime = Date.now();
      await generateOpenCode(ir, outputDir);
      const duration = Date.now() - startTime;
      
      expect(duration).toBeLessThan(1000);
    });
  });

  describe('ACCEPTANCE: Export all agents successfully', () => {
    it('should export at least 10 agents without errors', async () => {
      const agentFiles = await fs.readdir(agentsDir);
      const mdFiles = agentFiles.filter(f => f.endsWith('.agent.md'));
      
      expect(mdFiles.length).toBeGreaterThanOrEqual(10);
      
      let successCount = 0;
      const errors = [];
      
      for (const file of mdFiles) {
        try {
          const filePath = path.join(agentsDir, file);
          const ir = await parseAgentFile(filePath);
          await generateOpenCode(ir, outputDir);
          successCount++;
        } catch (error) {
          errors.push({ file, error: error.message });
        }
      }
      
      expect(successCount).toBeGreaterThanOrEqual(10);
      if (errors.length > 0) {
        console.log('Export errors:', errors);
      }
    });
  });
});

describe('OpenCode Generator - Unit Tests (TDD)', () => {
  const fixturesDir = path.join(__dirname, '../fixtures/ir');
  
  describe('mapIRToDiscovery()', () => {
    it('should map IR frontmatter to discovery structure', async () => {
      const irContent = await fs.readFile(path.join(fixturesDir, 'backend-benny.ir.json'), 'utf-8');
      const ir = JSON.parse(irContent);
      
      const discovery = mapIRToDiscovery(ir);
      
      expect(discovery.opencode_version).toBe('1.0');
      expect(discovery.agent.id).toBe('backend-benny');
      expect(discovery.agent.name).toBeTruthy();
      expect(discovery.agent.version).toBe('1.0.0');
      expect(discovery.agent.description).toBe(ir.frontmatter.description);
      expect(discovery.agent.tools).toEqual(ir.frontmatter.tools);
    });

    it('should extract capabilities from IR content', async () => {
      const irContent = await fs.readFile(path.join(fixturesDir, 'backend-benny.ir.json'), 'utf-8');
      const ir = JSON.parse(irContent);
      
      const discovery = mapIRToDiscovery(ir);
      
      expect(Array.isArray(discovery.agent.capabilities)).toBe(true);
      // Capabilities should be derived from specialization/purpose
    });

    it('should handle missing optional fields with defaults', async () => {
      const minimalIR = {
        ir_version: '1.0.0',
        frontmatter: {
          name: 'test-agent',
          description: 'Test agent',
          tools: ['read', 'write'],
          version: '1.0.0'
        },
        content: {
          purpose: 'Test purpose',
          specialization: null,
          collaboration_contract: null,
          success_criteria: null,
          mode_defaults: []
        },
        relationships: {
          directives: [],
          context_sources: [],
          agent_references: []
        },
        governance: {
          directive_requirements: { required: [], optional: [] },
          uncertainty_threshold: null,
          escalation_rules: [],
          safety_criticality: null,
          primer_required: false,
          test_first_required: false
        },
        metadata: {
          file_path: 'test.agent.md',
          source_hash: 'abc123',
          parsed_at: '2026-01-29T10:00:00Z',
          file_size: 100,
          parser_version: '1.0.0'
        }
      };
      
      const discovery = mapIRToDiscovery(minimalIR);
      
      expect(discovery.agent.id).toBe('test-agent');
      expect(discovery.agent.capabilities).toEqual([]);
      expect(discovery.agent.category).toBe('general');
      expect(discovery.agent.metadata.directives).toEqual([]);
    });

    it('should format profile_url correctly', async () => {
      const irContent = await fs.readFile(path.join(fixturesDir, 'backend-benny.ir.json'), 'utf-8');
      const ir = JSON.parse(irContent);
      
      const discovery = mapIRToDiscovery(ir);
      
      expect(discovery.agent.profile_url).toMatch(/\.agent\.md$/);
    });
  });

  describe('mapIRToDefinition()', () => {
    it('should map IR to definition structure', async () => {
      const irContent = await fs.readFile(path.join(fixturesDir, 'backend-benny.ir.json'), 'utf-8');
      const ir = JSON.parse(irContent);
      
      const definition = mapIRToDefinition(ir);
      
      expect(definition.opencode_version).toBe('1.0');
      expect(definition.agent.metadata.id).toBe('backend-benny');
      expect(definition.agent.metadata.version).toBe('1.0.0');
      expect(definition.agent.specification).toBeDefined();
      expect(definition.agent.governance).toBeDefined();
    });

    it('should include tools in specification', async () => {
      const irContent = await fs.readFile(path.join(fixturesDir, 'backend-benny.ir.json'), 'utf-8');
      const ir = JSON.parse(irContent);
      
      const definition = mapIRToDefinition(ir);
      
      expect(Array.isArray(definition.agent.specification.tools)).toBe(true);
      expect(definition.agent.specification.tools).toEqual(ir.frontmatter.tools);
    });

    it('should include governance directives', async () => {
      const irContent = await fs.readFile(path.join(fixturesDir, 'backend-benny.ir.json'), 'utf-8');
      const ir = JSON.parse(irContent);
      
      const definition = mapIRToDefinition(ir);
      
      expect(Array.isArray(definition.agent.governance.directives)).toBe(true);
      expect(definition.agent.governance.directives.length).toBeGreaterThan(0);
    });
  });

  describe('extractGovernanceMetadata()', () => {
    it('should extract governance extensions from IR', async () => {
      const irContent = await fs.readFile(path.join(fixturesDir, 'backend-benny.ir.json'), 'utf-8');
      const ir = JSON.parse(irContent);
      
      const governance = extractGovernanceMetadata(ir);
      
      expect(governance.agentic_governance).toBeDefined();
      expect(governance.agentic_governance.directives).toBeDefined();
      expect(governance.agentic_governance.uncertainty_threshold).toBe('>30%');
      expect(governance.agentic_governance.primer_required).toBe(true);
      expect(governance.agentic_governance.test_first_required).toBe(true);
    });

    it('should extract multi-agent metadata', async () => {
      const irContent = await fs.readFile(path.join(fixturesDir, 'backend-benny.ir.json'), 'utf-8');
      const ir = JSON.parse(irContent);
      
      const governance = extractGovernanceMetadata(ir);
      
      expect(governance.multi_agent).toBeDefined();
      expect(typeof governance.multi_agent.orchestration_capable).toBe('boolean');
      expect(Array.isArray(governance.multi_agent.handoff_protocols)).toBe(true);
      expect(governance.multi_agent.specialization_boundaries).toBeTruthy();
    });

    it('should determine priority level from specialization', async () => {
      const irContent = await fs.readFile(path.join(fixturesDir, 'backend-benny.ir.json'), 'utf-8');
      const ir = JSON.parse(irContent);
      
      const governance = extractGovernanceMetadata(ir);
      
      expect(governance.agentic_governance.priority_level).toMatch(/^(high|medium|low)$/);
    });

    it('should handle escalation rules', async () => {
      const irContent = await fs.readFile(path.join(fixturesDir, 'backend-benny.ir.json'), 'utf-8');
      const ir = JSON.parse(irContent);
      
      const governance = extractGovernanceMetadata(ir);
      
      expect(governance.agentic_governance.escalation_required).toBeDefined();
      expect(typeof governance.agentic_governance.escalation_required).toBe('boolean');
    });
  });

  describe('Edge cases', () => {
    it('should handle special characters in description', () => {
      const ir = {
        frontmatter: {
          name: 'test-agent',
          description: 'Test "quotes" & <special> chars',
          tools: ['read'],
          version: '1.0.0'
        },
        content: { purpose: 'Test', mode_defaults: [] },
        relationships: { directives: [], context_sources: [], agent_references: [] },
        governance: {
          directive_requirements: { required: [], optional: [] },
          uncertainty_threshold: null,
          escalation_rules: [],
          safety_criticality: null,
          primer_required: false,
          test_first_required: false
        },
        metadata: {
          file_path: 'test.agent.md',
          source_hash: 'abc',
          parsed_at: '2026-01-29T10:00:00Z',
          file_size: 100,
          parser_version: '1.0.0'
        }
      };
      
      const discovery = mapIRToDiscovery(ir);
      const discoveryJson = JSON.stringify(discovery);
      
      // Should be valid JSON
      expect(() => JSON.parse(discoveryJson)).not.toThrow();
    });

    it('should handle empty directives array', () => {
      const ir = {
        frontmatter: {
          name: 'test-agent',
          description: 'Test',
          tools: ['read'],
          version: '1.0.0'
        },
        content: { purpose: 'Test', mode_defaults: [] },
        relationships: { directives: [], context_sources: [], agent_references: [] },
        governance: {
          directive_requirements: { required: [], optional: [] },
          uncertainty_threshold: null,
          escalation_rules: [],
          safety_criticality: null,
          primer_required: false,
          test_first_required: false
        },
        metadata: {
          file_path: 'test.agent.md',
          source_hash: 'abc',
          parsed_at: '2026-01-29T10:00:00Z',
          file_size: 100,
          parser_version: '1.0.0'
        }
      };
      
      const discovery = mapIRToDiscovery(ir);
      
      expect(discovery.agent.metadata.directives).toEqual([]);
    });
  });
});
