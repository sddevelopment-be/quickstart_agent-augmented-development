/**
 * GitHub Copilot Skills Generator - Acceptance and Unit Tests
 * 
 * Following Directive 016 (ATDD) - Acceptance tests written FIRST
 * Following Directive 017 (TDD) - Red-Green-Refactor cycle
 * 
 * Test Strategy:
 * 1. Generate valid Copilot Skills JSON from IR
 * 2. Include conversation starters relevant to agent role
 * 3. Map workspace extensions correctly
 * 4. Preserve governance extensions
 * 5. Handle edge cases (missing fields, special chars)
 * 6. Performance requirements (<1 second per agent)
 */

const {
  generateCopilotSkill,
  mapIRToCopilotSkill,
  generateConversationStarters,
  mapToolsToExtensions
} = require('../../ops/exporters/copilot-generator');
const { parseAgentFile } = require('../../ops/exporters/parser');
const fs = require('fs').promises;
const path = require('path');

describe('Copilot Generator - Acceptance Tests', () => {
  const agentsDir = path.join(__dirname, '../../.github/agents');
  const outputDir = path.join(__dirname, '../../tmp/copilot-test-output');
  
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

  describe('ACCEPTANCE: Generate valid Copilot Skills JSON from IR', () => {
    it('should generate valid Copilot Skills JSON for architect-alphonso', async () => {
      const filePath = path.join(agentsDir, 'architect.agent.md');
      const ir = await parseAgentFile(filePath);
      const skillPath = await generateCopilotSkill(ir, outputDir);
      
      // File should exist
      const skillContent = await fs.readFile(skillPath, 'utf-8');
      const skill = JSON.parse(skillContent);
      
      // Validate Copilot Skills structure
      expect(skill.$schema).toBe('https://aka.ms/copilot-skill-schema');
      expect(skill.name).toBe('architect-alphonso');
      expect(skill.description).toBe('Clarify complex systems with contextual trade-offs.');
      expect(Array.isArray(skill.capabilities)).toBe(true);
      expect(skill.capabilities.length).toBeGreaterThan(0);
      expect(skill.instructions).toBeTruthy();
      expect(typeof skill.instructions).toBe('string');
    });

    it('should generate valid Copilot Skills JSON for backend-benny', async () => {
      const filePath = path.join(agentsDir, 'backend-dev.agent.md');
      const ir = await parseAgentFile(filePath);
      const skillPath = await generateCopilotSkill(ir, outputDir);
      
      const skillContent = await fs.readFile(skillPath, 'utf-8');
      const skill = JSON.parse(skillContent);
      
      expect(skill.$schema).toBe('https://aka.ms/copilot-skill-schema');
      expect(skill.name).toBe('backend-benny');
      expect(skill.description).toBeTruthy();
    });

    it('should generate valid Copilot Skills JSON for curator-claire', async () => {
      const filePath = path.join(agentsDir, 'curator.agent.md');
      const ir = await parseAgentFile(filePath);
      const skillPath = await generateCopilotSkill(ir, outputDir);
      
      const skillContent = await fs.readFile(skillPath, 'utf-8');
      const skill = JSON.parse(skillContent);
      
      expect(skill.$schema).toBe('https://aka.ms/copilot-skill-schema');
      expect(skill.name).toBe('curator-claire');
    });
  });

  describe('ACCEPTANCE: Include conversation starters', () => {
    it('should include conversation starters in generated skill', async () => {
      const filePath = path.join(agentsDir, 'architect.agent.md');
      const ir = await parseAgentFile(filePath);
      const skillPath = await generateCopilotSkill(ir, outputDir);
      
      const skillContent = await fs.readFile(skillPath, 'utf-8');
      const skill = JSON.parse(skillContent);
      
      expect(Array.isArray(skill.conversation_starters)).toBe(true);
      expect(skill.conversation_starters.length).toBeGreaterThan(0);
      expect(typeof skill.conversation_starters[0]).toBe('string');
    });

    it('should generate architect-specific conversation starters', async () => {
      const filePath = path.join(agentsDir, 'architect.agent.md');
      const ir = await parseAgentFile(filePath);
      const skillPath = await generateCopilotSkill(ir, outputDir);
      
      const skillContent = await fs.readFile(skillPath, 'utf-8');
      const skill = JSON.parse(skillContent);
      
      // Should include architecture-related starters
      const startersText = skill.conversation_starters.join(' ').toLowerCase();
      expect(
        startersText.includes('architecture') || 
        startersText.includes('design') || 
        startersText.includes('adr')
      ).toBe(true);
    });

    it('should generate backend-specific conversation starters', async () => {
      const filePath = path.join(agentsDir, 'backend-dev.agent.md');
      const ir = await parseAgentFile(filePath);
      const skillPath = await generateCopilotSkill(ir, outputDir);
      
      const skillContent = await fs.readFile(skillPath, 'utf-8');
      const skill = JSON.parse(skillContent);
      
      // Should include backend-related starters
      const startersText = skill.conversation_starters.join(' ').toLowerCase();
      expect(
        startersText.includes('backend') || 
        startersText.includes('api') || 
        startersText.includes('service')
      ).toBe(true);
    });
  });

  describe('ACCEPTANCE: Map workspace extensions correctly', () => {
    it('should include workspace configuration in generated skill', async () => {
      const filePath = path.join(agentsDir, 'architect.agent.md');
      const ir = await parseAgentFile(filePath);
      const skillPath = await generateCopilotSkill(ir, outputDir);
      
      const skillContent = await fs.readFile(skillPath, 'utf-8');
      const skill = JSON.parse(skillContent);
      
      expect(skill.workspace).toBeDefined();
      expect(Array.isArray(skill.workspace.extensions)).toBe(true);
    });

    it('should map plantuml tool to jebbs.plantuml extension', async () => {
      const filePath = path.join(agentsDir, 'architect.agent.md');
      const ir = await parseAgentFile(filePath);
      const skillPath = await generateCopilotSkill(ir, outputDir);
      
      const skillContent = await fs.readFile(skillPath, 'utf-8');
      const skill = JSON.parse(skillContent);
      
      expect(skill.workspace.extensions).toContain('jebbs.plantuml');
    });

    it('should include workspace settings', async () => {
      const filePath = path.join(agentsDir, 'backend-dev.agent.md');
      const ir = await parseAgentFile(filePath);
      const skillPath = await generateCopilotSkill(ir, outputDir);
      
      const skillContent = await fs.readFile(skillPath, 'utf-8');
      const skill = JSON.parse(skillContent);
      
      expect(skill.workspace.settings).toBeDefined();
      expect(typeof skill.workspace.settings).toBe('object');
    });
  });

  describe('ACCEPTANCE: Preserve governance extensions', () => {
    it('should include governance extensions in generated skill', async () => {
      const filePath = path.join(agentsDir, 'architect.agent.md');
      const ir = await parseAgentFile(filePath);
      const skillPath = await generateCopilotSkill(ir, outputDir);
      
      const skillContent = await fs.readFile(skillPath, 'utf-8');
      const skill = JSON.parse(skillContent);
      
      expect(skill.extensions).toBeDefined();
      expect(skill.extensions.saboteurs_governance).toBeDefined();
    });

    it('should include multi-agent extensions', async () => {
      const filePath = path.join(agentsDir, 'backend-dev.agent.md');
      const ir = await parseAgentFile(filePath);
      const skillPath = await generateCopilotSkill(ir, outputDir);
      
      const skillContent = await fs.readFile(skillPath, 'utf-8');
      const skill = JSON.parse(skillContent);
      
      expect(skill.extensions.multi_agent).toBeDefined();
    });

    it('should preserve directive information in governance', async () => {
      const filePath = path.join(agentsDir, 'architect.agent.md');
      const ir = await parseAgentFile(filePath);
      const skillPath = await generateCopilotSkill(ir, outputDir);
      
      const skillContent = await fs.readFile(skillPath, 'utf-8');
      const skill = JSON.parse(skillContent);
      
      expect(Array.isArray(skill.extensions.saboteurs_governance.directives)).toBe(true);
    });
  });
});

describe('Copilot Generator - Unit Tests', () => {
  describe('mapIRToCopilotSkill()', () => {
    it('should map basic IR fields to Copilot Skill structure', () => {
      const mockIR = {
        frontmatter: {
          name: 'test-agent',
          description: 'Test description',
          tools: ['read', 'write']
        },
        content: {
          purpose: 'Test purpose',
          specialization: 'Test specialization'
        },
        relationships: {
          directives: []
        },
        governance: {
          safety_criticality: null,
          primer_required: false,
          test_first_required: false,
          uncertainty_threshold: null,
          escalation_rules: []
        }
      };
      
      const skill = mapIRToCopilotSkill(mockIR);
      
      expect(skill.$schema).toBe('https://aka.ms/copilot-skill-schema');
      expect(skill.name).toBe('test-agent');
      expect(skill.description).toBe('Test description');
      expect(Array.isArray(skill.capabilities)).toBe(true);
      expect(skill.instructions).toBeTruthy();
      expect(Array.isArray(skill.conversation_starters)).toBe(true);
      expect(skill.workspace).toBeDefined();
      expect(skill.extensions).toBeDefined();
    });

    it('should handle missing optional fields gracefully', () => {
      const mockIR = {
        frontmatter: {
          name: 'minimal-agent',
          description: 'Minimal',
          tools: []
        },
        content: {},
        relationships: {
          directives: []
        },
        governance: {
          safety_criticality: null,
          primer_required: false,
          test_first_required: false,
          uncertainty_threshold: null,
          escalation_rules: []
        }
      };
      
      const skill = mapIRToCopilotSkill(mockIR);
      
      expect(skill.name).toBe('minimal-agent');
      expect(skill.instructions).toBeTruthy(); // Should have fallback
      expect(Array.isArray(skill.capabilities)).toBe(true);
    });

    it('should handle special characters in description', () => {
      const mockIR = {
        frontmatter: {
          name: 'special-agent',
          description: 'Description with "quotes" and \'apostrophes\' & symbols',
          tools: []
        },
        content: {
          purpose: 'Purpose text'
        },
        relationships: {
          directives: []
        },
        governance: {
          safety_criticality: null,
          primer_required: false,
          test_first_required: false,
          uncertainty_threshold: null,
          escalation_rules: []
        }
      };
      
      const skill = mapIRToCopilotSkill(mockIR);
      
      expect(skill.description).toContain('quotes');
      expect(skill.description).toContain('apostrophes');
      expect(skill.description).toContain('&');
    });
  });

  describe('generateConversationStarters()', () => {
    it('should generate conversation starters for architect role', () => {
      const mockIR = {
        frontmatter: {
          name: 'architect-alphonso',
          description: 'Architecture specialist'
        },
        content: {
          purpose: 'System design and architecture',
          specialization: 'Design interfaces, ADRs'
        }
      };
      
      const starters = generateConversationStarters(mockIR);
      
      expect(Array.isArray(starters)).toBe(true);
      expect(starters.length).toBeGreaterThan(0);
      
      const startersText = starters.join(' ').toLowerCase();
      expect(
        startersText.includes('architecture') || 
        startersText.includes('design')
      ).toBe(true);
    });

    it('should generate conversation starters for backend role', () => {
      const mockIR = {
        frontmatter: {
          name: 'backend-benny',
          description: 'Backend specialist'
        },
        content: {
          purpose: 'API and service design',
          specialization: 'Backend architecture'
        }
      };
      
      const starters = generateConversationStarters(mockIR);
      
      expect(Array.isArray(starters)).toBe(true);
      expect(starters.length).toBeGreaterThan(0);
      
      const startersText = starters.join(' ').toLowerCase();
      expect(
        startersText.includes('api') || 
        startersText.includes('backend') ||
        startersText.includes('service')
      ).toBe(true);
    });

    it('should generate generic starters for unknown roles', () => {
      const mockIR = {
        frontmatter: {
          name: 'unknown-agent',
          description: 'Generic agent'
        },
        content: {
          purpose: 'General purpose'
        }
      };
      
      const starters = generateConversationStarters(mockIR);
      
      expect(Array.isArray(starters)).toBe(true);
      expect(starters.length).toBeGreaterThan(0);
    });
  });

  describe('mapToolsToExtensions()', () => {
    it('should map plantuml to jebbs.plantuml', () => {
      const tools = ['plantuml'];
      const extensions = mapToolsToExtensions(tools);
      
      expect(Array.isArray(extensions)).toBe(true);
      expect(extensions).toContain('jebbs.plantuml');
    });

    it('should map mermaid to bierner.markdown-mermaid', () => {
      const tools = ['mermaid'];
      const extensions = mapToolsToExtensions(tools);
      
      expect(extensions).toContain('bierner.markdown-mermaid');
    });

    it('should handle empty tools array', () => {
      const tools = [];
      const extensions = mapToolsToExtensions(tools);
      
      expect(Array.isArray(extensions)).toBe(true);
      expect(extensions.length).toBeGreaterThanOrEqual(0);
    });

    it('should handle unknown tools gracefully', () => {
      const tools = ['unknown-tool', 'another-unknown'];
      const extensions = mapToolsToExtensions(tools);
      
      expect(Array.isArray(extensions)).toBe(true);
    });

    it('should map multiple tools correctly', () => {
      const tools = ['plantuml', 'mermaid', 'bash'];
      const extensions = mapToolsToExtensions(tools);
      
      expect(Array.isArray(extensions)).toBe(true);
      expect(extensions.length).toBeGreaterThan(0);
    });
  });
});

describe('Copilot Generator - Edge Cases', () => {
  it('should handle agents with minimal content', async () => {
    const mockIR = {
      frontmatter: {
        name: 'minimal',
        description: 'Min',
        tools: []
      },
      content: {},
      relationships: {
        directives: []
      },
      governance: {
        safety_criticality: null,
        primer_required: false,
        test_first_required: false,
        uncertainty_threshold: null,
        escalation_rules: []
      },
      metadata: {
        file_path: 'test.md'
      }
    };
    
    const skill = mapIRToCopilotSkill(mockIR);
    
    expect(skill.name).toBe('minimal');
    expect(skill.$schema).toBeTruthy();
  });

  it('should handle very long descriptions', () => {
    const longDesc = 'A'.repeat(1000);
    const mockIR = {
      frontmatter: {
        name: 'long-agent',
        description: longDesc,
        tools: []
      },
      content: {
        purpose: 'Purpose'
      },
      relationships: {
        directives: []
      },
      governance: {
        safety_criticality: null,
        primer_required: false,
        test_first_required: false,
        uncertainty_threshold: null,
        escalation_rules: []
      }
    };
    
    const skill = mapIRToCopilotSkill(mockIR);
    
    expect(skill.description.length).toBeGreaterThan(0);
  });
});

describe('Copilot Generator - Performance', () => {
  it('should generate skill in less than 1 second', async () => {
    const filePath = path.join(__dirname, '../../.github/agents/architect.agent.md');
    const ir = await parseAgentFile(filePath);
    const outputDir = path.join(__dirname, '../../tmp/copilot-perf-test');
    
    await fs.mkdir(outputDir, { recursive: true });
    
    const startTime = Date.now();
    await generateCopilotSkill(ir, outputDir);
    const endTime = Date.now();
    
    const duration = endTime - startTime;
    expect(duration).toBeLessThan(1000);
    
    // Cleanup
    await fs.rm(outputDir, { recursive: true, force: true });
  });
});
