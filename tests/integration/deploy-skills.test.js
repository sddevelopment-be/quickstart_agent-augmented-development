/**
 * Tests for deploy-skills.js enhancements
 * Testing Claude agent and prompt deployment functionality
 */

const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');

const ROOT_DIR = path.join(__dirname, '..', '..');
const DEPLOY_SCRIPT = path.join(ROOT_DIR, 'ops', 'deploy-skills.js');

describe('Claude Agent and Prompt Deployment', () => {
  
  describe('deployClaudeAgents', () => {
    const CLAUDE_AGENTS_DIR = path.join(ROOT_DIR, '.claude', 'agents');
    
    beforeEach(async () => {
      // Clean up test directory
      try {
        await fs.rm(CLAUDE_AGENTS_DIR, { recursive: true, force: true });
      } catch (error) {
        // Directory might not exist
      }
    });

    test('should create .claude/agents directory', async () => {
      execSync(`node ${DEPLOY_SCRIPT} --agents`, { cwd: ROOT_DIR });
      
      const exists = await fs.access(CLAUDE_AGENTS_DIR)
        .then(() => true)
        .catch(() => false);
      
      expect(exists).toBe(true);
    });

    test('should deploy all agent files from .github/agents', async () => {
      execSync(`node ${DEPLOY_SCRIPT} --agents`, { cwd: ROOT_DIR });
      
      const agentFiles = await fs.readdir(CLAUDE_AGENTS_DIR);
      const agentMdFiles = agentFiles.filter(f => f.endsWith('.agent.md'));
      
      expect(agentMdFiles.length).toBeGreaterThan(0);
    });

    test('should create manifest.json with agent inventory', async () => {
      execSync(`node ${DEPLOY_SCRIPT} --agents`, { cwd: ROOT_DIR });
      
      const manifestPath = path.join(CLAUDE_AGENTS_DIR, 'manifest.json');
      const manifestExists = await fs.access(manifestPath)
        .then(() => true)
        .catch(() => false);
      
      expect(manifestExists).toBe(true);
      
      if (manifestExists) {
        const manifest = JSON.parse(await fs.readFile(manifestPath, 'utf-8'));
        expect(manifest).toHaveProperty('agents');
        expect(Array.isArray(manifest.agents)).toBe(true);
      }
    });
  });

  describe('deployClaudePrompts', () => {
    const CLAUDE_PROMPTS_DIR = path.join(ROOT_DIR, '.claude', 'prompts');
    
    beforeEach(async () => {
      // Clean up test directory
      try {
        await fs.rm(CLAUDE_PROMPTS_DIR, { recursive: true, force: true });
      } catch (error) {
        // Directory might not exist
      }
    });

    test('should create .claude/prompts directory', async () => {
      execSync(`node ${DEPLOY_SCRIPT} --prompts`, { cwd: ROOT_DIR });
      
      const exists = await fs.access(CLAUDE_PROMPTS_DIR)
        .then(() => true)
        .catch(() => false);
      
      expect(exists).toBe(true);
    });

    test('should deploy both .md and .yaml prompt files', async () => {
      execSync(`node ${DEPLOY_SCRIPT} --prompts`, { cwd: ROOT_DIR });
      
      const promptFiles = await fs.readdir(CLAUDE_PROMPTS_DIR);
      const mdFiles = promptFiles.filter(f => f.endsWith('.md'));
      const yamlFiles = promptFiles.filter(f => f.endsWith('.yaml'));
      
      expect(mdFiles.length).toBeGreaterThan(0);
      expect(yamlFiles.length).toBeGreaterThan(0);
    });

    test('should create manifest.json with prompt inventory', async () => {
      execSync(`node ${DEPLOY_SCRIPT} --prompts`, { cwd: ROOT_DIR });
      
      const manifestPath = path.join(CLAUDE_PROMPTS_DIR, 'manifest.json');
      const manifestExists = await fs.access(manifestPath)
        .then(() => true)
        .catch(() => false);
      
      expect(manifestExists).toBe(true);
      
      if (manifestExists) {
        const manifest = JSON.parse(await fs.readFile(manifestPath, 'utf-8'));
        expect(manifest).toHaveProperty('prompts');
        expect(Array.isArray(manifest.prompts)).toBe(true);
      }
    });
  });

  describe('deploy:claude integration', () => {
    test('should deploy skills, agents, and prompts when using --all', async () => {
      const result = execSync(`node ${DEPLOY_SCRIPT} --all`, { 
        cwd: ROOT_DIR,
        encoding: 'utf-8' 
      });
      
      expect(result).toContain('Claude Code skills');
      expect(result).toContain('Claude agents');
      expect(result).toContain('Claude prompts');
    });
  });
});
