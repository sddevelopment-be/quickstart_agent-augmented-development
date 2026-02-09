/**
 * Validation Tests for Doctrine Export Pipeline
 * Phase 4: Acceptance Tests (ATDD - Green Phase)
 * 
 * Specification: SPEC-DIST-001 v1.1.0
 * Created: 2026-02-08 by DevOps Danny
 * Updated: 2026-02-09 - Added content validation and coverage checks
 */

const fs = require('fs');
const path = require('path');

describe('Doctrine Export - Source Path Validation', () => {
  test('opencode-exporter reads from doctrine/agents/', () => {
    const exporterPath = path.join(__dirname, '../../../tools/exporters/opencode-exporter.js');
    const content = fs.readFileSync(exporterPath, 'utf8');
    
    expect(content).toMatch(/AGENTS_DIR.*doctrine.*agents/);
  });

  test('deploy-skills reads agents from doctrine/agents/', () => {
    const deployPath = path.join(__dirname, '../../../tools/scripts/deploy-skills.js');
    const content = fs.readFileSync(deployPath, 'utf8');
    
    expect(content).toMatch(/AGENTS_SOURCE_DIR.*doctrine.*agents/);
  });

  test('skills-exporter reads approaches from doctrine/approaches/', () => {
    const exporterPath = path.join(__dirname, '../../../tools/scripts/skills-exporter.js');
    const content = fs.readFileSync(exporterPath, 'utf8');
    
    expect(content).toMatch(/APPROACHES_DIR.*doctrine.*approaches/);
  });

  test('doctrine/agents directory exists', () => {
    const doctrinePath = path.join(__dirname, '../../../doctrine/agents');
    expect(fs.existsSync(doctrinePath)).toBe(true);
    
    const agentFiles = fs.readdirSync(doctrinePath).filter(f => f.endsWith('.agent.md'));
    expect(agentFiles.length).toBeGreaterThan(15);
  });
});

describe('Doctrine Export - Content Validation', () => {
  const doctrinePath = path.join(__dirname, '../../../doctrine/agents');
  
  test('all agent files have valid frontmatter', () => {
    const agentFiles = fs.readdirSync(doctrinePath).filter(f => f.endsWith('.agent.md'));
    
    expect(agentFiles.length).toBeGreaterThan(0);
    
    agentFiles.forEach(file => {
      const content = fs.readFileSync(path.join(doctrinePath, file), 'utf8');
      
      // Check for YAML frontmatter
      expect(content).toMatch(/^---\s*\n/);
      
      // Check for required fields in frontmatter
      expect(content).toMatch(/name:\s*.+/);
      expect(content).toMatch(/description:\s*.+/);
    });
  });
  
  test('all agent files have unique names', () => {
    const agentFiles = fs.readdirSync(doctrinePath).filter(f => f.endsWith('.agent.md'));
    const names = new Set();
    
    agentFiles.forEach(file => {
      const content = fs.readFileSync(path.join(doctrinePath, file), 'utf8');
      const nameMatch = content.match(/^name:\s*(.+)$/m);
      
      if (nameMatch) {
        const name = nameMatch[1].trim();
        expect(names.has(name)).toBe(false);
        names.add(name);
      }
    });
    
    expect(names.size).toBe(agentFiles.length);
  });
  
  test('all agent files have proper structure', () => {
    const agentFiles = fs.readdirSync(doctrinePath).filter(f => f.endsWith('.agent.md'));
    
    agentFiles.forEach(file => {
      const content = fs.readFileSync(path.join(doctrinePath, file), 'utf8');
      
      // Check for key sections (most agents should have these)
      const hasContextSources = content.includes('Context Sources') || content.includes('## 1.');
      const hasDirectives = content.includes('Directive') || content.includes('## 2.');
      
      // At least one section should be present
      expect(hasContextSources || hasDirectives).toBe(true);
    });
  });
  
  test('agent names follow naming convention', () => {
    const agentFiles = fs.readdirSync(doctrinePath).filter(f => f.endsWith('.agent.md'));
    
    agentFiles.forEach(file => {
      const content = fs.readFileSync(path.join(doctrinePath, file), 'utf8');
      const nameMatch = content.match(/^name:\s*(.+)$/m);
      
      if (nameMatch) {
        const name = nameMatch[1].trim();
        
        // Name should be lowercase with hyphens (kebab-case)
        expect(name).toMatch(/^[a-z]+(-[a-z]+)*$/);
      }
    });
  });
});

describe('Doctrine Export - Coverage Validation', () => {
  test('all agents in doctrine are exportable', () => {
    const doctrinePath = path.join(__dirname, '../../../doctrine/agents');
    const agentFiles = fs.readdirSync(doctrinePath).filter(f => f.endsWith('.agent.md'));
    
    // Each agent file should be processable
    agentFiles.forEach(file => {
      const filePath = path.join(doctrinePath, file);
      const stat = fs.statSync(filePath);
      
      // File should not be empty
      expect(stat.size).toBeGreaterThan(100);
      
      // File should be readable
      const content = fs.readFileSync(filePath, 'utf8');
      expect(content.length).toBeGreaterThan(100);
    });
  });
  
  test('exporters handle all agent formats', () => {
    const exporterPath = path.join(__dirname, '../../../tools/exporters/opencode-exporter.js');
    const exporterContent = fs.readFileSync(exporterPath, 'utf8');
    
    // Exporter should handle YAML frontmatter
    expect(exporterContent).toMatch(/yaml|frontmatter/i);
    
    // Exporter should handle markdown content
    expect(exporterContent).toMatch(/\.md|markdown/i);
  });
  
  test('minimum agent count is maintained', () => {
    const doctrinePath = path.join(__dirname, '../../../doctrine/agents');
    const agentFiles = fs.readdirSync(doctrinePath).filter(f => f.endsWith('.agent.md'));
    
    // Should have at least 20 agents (as per design)
    expect(agentFiles.length).toBeGreaterThanOrEqual(20);
  });
});
