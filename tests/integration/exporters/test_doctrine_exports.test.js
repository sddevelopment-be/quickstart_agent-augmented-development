/**
 * Validation Tests for Doctrine Export Pipeline
 * Phase 4: Acceptance Tests (ATDD - Red Phase)
 * 
 * Specification: SPEC-DIST-001 v1.1.0
 * Created: 2026-02-08 by DevOps Danny
 * Expected: Tests WILL FAIL initially (red phase)
 */

const fs = require('fs');
const path = require('path');

describe('Doctrine Export - Source Path Validation', () => {
  test('copilot-generator reads from doctrine/agents/', () => {
    const exporterPath = path.join(__dirname, '../../../tools/exporters/copilot-generator.js');
    const content = fs.readFileSync(exporterPath, 'utf8');
    
    expect(content).toContain('doctrine/agents');
    expect(content).not.toContain("'.github/agents'");
  });

  test('opencode-exporter reads from doctrine/agents/', () => {
    const exporterPath = path.join(__dirname, '../../../tools/exporters/opencode-exporter.js');
    const content = fs.readFileSync(exporterPath, 'utf8');
    
    expect(content).toContain('doctrine/agents');
    expect(content).not.toContain("'.github/agents'");
  });

  test('doctrine/agents directory exists', () => {
    const doctrinePath = path.join(__dirname, '../../../doctrine/agents');
    expect(fs.existsSync(doctrinePath)).toBe(true);
    
    const agentFiles = fs.readdirSync(doctrinePath).filter(f => f.endsWith('.agent.md'));
    expect(agentFiles.length).toBeGreaterThan(15);
  });
});
