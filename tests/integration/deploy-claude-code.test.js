/**
 * Integration Tests: Claude Code Deployment (SPEC-DIST-002)
 *
 * Following Directive 016 (ATDD): Acceptance tests for all 6 acceptance criteria.
 *
 * AC-1: CLAUDE.md exists and is well-formed
 * AC-2: Rules files exist and are well-formed
 * AC-3: Agent files are simplified
 * AC-4: Prompts directory not created
 * AC-5: Pipeline integration (selective flags)
 * AC-6: Idempotency
 */

const { execSync } = require('child_process');
const fs = require('fs').promises;
const path = require('path');

const ROOT = path.join(__dirname, '..', '..');
const DEPLOY_SCRIPT = path.join(ROOT, 'tools', 'scripts', 'deploy-skills.js');

// Helper: run deploy with specific flags
function runDeploy(flags = '') {
  return execSync(`node ${DEPLOY_SCRIPT} ${flags}`, {
    cwd: ROOT,
    encoding: 'utf-8',
    timeout: 30000
  });
}

describe('Claude Code Deployment Integration (SPEC-DIST-002)', () => {

  // Deploy once before all tests
  beforeAll(() => {
    runDeploy('--claude-md --rules --agents');
  });

  describe('AC-1: CLAUDE.md exists and is well-formed', () => {
    let content;

    beforeAll(async () => {
      content = await fs.readFile(path.join(ROOT, 'CLAUDE.md'), 'utf-8');
    });

    it('should exist at repository root', async () => {
      const exists = await fs.access(path.join(ROOT, 'CLAUDE.md')).then(() => true).catch(() => false);
      expect(exists).toBe(true);
    });

    it('should be under 120 lines', () => {
      const lines = content.split('\n');
      expect(lines.length).toBeLessThanOrEqual(120);
    });

    it('should contain project purpose', () => {
      expect(content).toContain('quickstart template');
    });

    it('should contain repository structure', () => {
      expect(content).toMatch(/doctrine\//);
    });

    it('should contain coding conventions', () => {
      expect(content).toMatch(/[Cc]onventions/);
    });

    it('should contain common commands', () => {
      expect(content).toMatch(/pytest|npm/);
    });

    it('should contain pointers to deeper context', () => {
      expect(content).toContain('.claude/rules/');
      expect(content).toContain('doctrine/');
    });

    it('should include generation header comment', () => {
      expect(content).toMatch(/<!--.*[Gg]enerated.*do not edit/i);
    });
  });

  describe('AC-2: Rules files exist and are well-formed', () => {
    const rulesDir = path.join(ROOT, '.claude', 'rules');
    const expectedRules = ['guidelines', 'coding-conventions', 'testing', 'architecture', 'collaboration'];

    it('should have at least 5 rules files', async () => {
      const files = await fs.readdir(rulesDir);
      const mdFiles = files.filter(f => f.endsWith('.md'));
      expect(mdFiles.length).toBeGreaterThanOrEqual(5);
    });

    for (const ruleName of expectedRules) {
      describe(`rules/${ruleName}.md`, () => {
        let content;

        beforeAll(async () => {
          content = await fs.readFile(path.join(rulesDir, `${ruleName}.md`), 'utf-8');
        });

        it('should be under 80 lines', () => {
          const lines = content.split('\n');
          expect(lines.length).toBeLessThanOrEqual(80);
        });

        it('should contain source attribution comment', () => {
          expect(content).toMatch(/<!--\s*Source:/);
        });

        it('should have a title heading', () => {
          expect(content).toMatch(/^# /m);
        });
      });
    }
  });

  describe('AC-3: Agent files are simplified', () => {
    const agentsDir = path.join(ROOT, '.claude', 'agents');

    it('should have agent files', async () => {
      const files = await fs.readdir(agentsDir);
      const agentFiles = files.filter(f => f.endsWith('.agent.md'));
      expect(agentFiles.length).toBeGreaterThan(10);
    });

    it('should have all agent files under 40 lines', async () => {
      const files = await fs.readdir(agentsDir);
      const agentFiles = files.filter(f => f.endsWith('.agent.md'));

      for (const file of agentFiles) {
        const content = await fs.readFile(path.join(agentsDir, file), 'utf-8');
        const lines = content.split('\n');
        expect(lines.length).toBeLessThanOrEqual(40);
      }
    });

    it('should retain name, description, tools in frontmatter', async () => {
      const content = await fs.readFile(path.join(agentsDir, 'architect.agent.md'), 'utf-8');
      expect(content).toMatch(/name:\s+architect-alphonso/);
      expect(content).toMatch(/description:\s+.+/);
      expect(content).toMatch(/tools:\s+\[/);
    });

    it('should include model hint in frontmatter', async () => {
      const content = await fs.readFile(path.join(agentsDir, 'architect.agent.md'), 'utf-8');
      expect(content).toMatch(/model:\s+(opus|sonnet|haiku)/);
    });

    it('should NOT contain directive tables', async () => {
      const content = await fs.readFile(path.join(agentsDir, 'architect.agent.md'), 'utf-8');
      expect(content).not.toMatch(/\|\s*Code\s*\|/);
      expect(content).not.toContain('Directive References');
    });

    it('should NOT contain mode defaults', async () => {
      const content = await fs.readFile(path.join(agentsDir, 'architect.agent.md'), 'utf-8');
      expect(content).not.toContain('/analysis-mode');
      expect(content).not.toContain('Mode Defaults');
    });

    it('should NOT contain initialization declaration', async () => {
      const content = await fs.readFile(path.join(agentsDir, 'architect.agent.md'), 'utf-8');
      expect(content).not.toContain('initialized');
    });

    it('should generate manifest.json', async () => {
      const manifest = JSON.parse(await fs.readFile(path.join(agentsDir, 'manifest.json'), 'utf-8'));
      expect(manifest.agents).toBeDefined();
      expect(manifest.agents.length).toBeGreaterThan(10);
    });
  });

  describe('AC-4: Prompts directory not created by default', () => {
    it('should NOT create .claude/prompts/ when deploying with default flags', () => {
      // Deploy only new artifacts (no --prompts or --prompts-legacy)
      runDeploy('--claude-md --rules --agents');

      // The prompts dir may exist from previous runs, but default deploy should not populate it
      // This test verifies the default deploy:claude script does not include prompts
      const output = runDeploy('--claude-md --rules --agents');
      expect(output).not.toContain('Deploying Claude prompts');
    });
  });

  describe('AC-5: Pipeline integration - selective flags', () => {
    it('--rules should only deploy rules files', () => {
      const output = runDeploy('--rules');
      expect(output).toContain('Deploying Claude Code rules');
      expect(output).not.toContain('Deploying CLAUDE.md');
      expect(output).not.toContain('Deploying Claude agents');
    });

    it('--claude-md should only deploy CLAUDE.md', () => {
      const output = runDeploy('--claude-md');
      expect(output).toContain('Deploying CLAUDE.md');
      expect(output).not.toContain('Deploying Claude Code rules');
      expect(output).not.toContain('Deploying Claude agents');
    });

    it('--agents should only deploy agents', () => {
      const output = runDeploy('--agents');
      expect(output).toContain('Deploying Claude agents');
      expect(output).not.toContain('Deploying CLAUDE.md');
      expect(output).not.toContain('Deploying Claude Code rules');
    });
  });

  describe('AC-6: Idempotency', () => {
    it('should produce identical CLAUDE.md on second run', async () => {
      runDeploy('--claude-md');
      const first = await fs.readFile(path.join(ROOT, 'CLAUDE.md'), 'utf-8');

      runDeploy('--claude-md');
      const second = await fs.readFile(path.join(ROOT, 'CLAUDE.md'), 'utf-8');

      expect(first).toBe(second);
    });

    it('should produce identical rules files on second run', async () => {
      runDeploy('--rules');
      const first = await fs.readFile(path.join(ROOT, '.claude', 'rules', 'guidelines.md'), 'utf-8');

      runDeploy('--rules');
      const second = await fs.readFile(path.join(ROOT, '.claude', 'rules', 'guidelines.md'), 'utf-8');

      expect(first).toBe(second);
    });

    it('should produce identical agent files on second run', async () => {
      runDeploy('--agents');
      const first = await fs.readFile(path.join(ROOT, '.claude', 'agents', 'architect.agent.md'), 'utf-8');

      runDeploy('--agents');
      const second = await fs.readFile(path.join(ROOT, '.claude', 'agents', 'architect.agent.md'), 'utf-8');

      expect(first).toBe(second);
    });
  });
});
