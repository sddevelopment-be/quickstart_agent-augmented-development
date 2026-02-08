/**
 * Validation Tests for Doctrine Export Pipeline
 * Phase 4: Acceptance Tests (ATDD - Green Phase)
 * 
 * Specification: SPEC-DIST-001 v1.1.0
 * Created: 2026-02-08 by DevOps Danny
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
