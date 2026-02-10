/**
 * Unit Tests: claude-code-generator.js — generateClaudeMd()
 *
 * Following Directive 017 (TDD): RED phase — tests before implementation.
 * Following Directive 016 (ATDD): Tests define acceptance criteria from SPEC-DIST-002 FR-1.
 *
 * Acceptance Criteria (AC-1):
 * - CLAUDE.md exists and is well-formed
 * - Contains project purpose, repository structure, coding conventions, common commands
 * - Under 120 lines
 * - Does not inline full doctrine content (uses pointers/links)
 * - Includes generation header comment
 */

const fs = require('fs').promises;
const path = require('path');
const os = require('os');
const { generateClaudeMd } = require('../../../tools/exporters/claude-code-generator');

let tmpDir;

beforeEach(async () => {
  tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'claudemd-test-'));
});

afterEach(async () => {
  await fs.rm(tmpDir, { recursive: true, force: true });
});

async function writeFixture(name, content) {
  const filePath = path.join(tmpDir, name);
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, content, 'utf-8');
  return filePath;
}

function makeConfig(overrides = {}) {
  return {
    visionFile: overrides.visionFile || path.join(tmpDir, 'VISION.md'),
    quickRefFile: overrides.quickRefFile || path.join(tmpDir, 'quickref.md'),
    pythonConventionsFile: overrides.pythonConventionsFile || path.join(tmpDir, 'python-conventions.md'),
    projectRoot: tmpDir,
    ...overrides
  };
}

describe('generateClaudeMd', () => {

  describe('Output structure', () => {
    it('should include generation header comment', async () => {
      await writeFixture('VISION.md', '# Vision\n\nThis is a quickstart template.\n');
      await writeFixture('quickref.md', '# Quick Ref\n\n- `src/` — Source code\n');
      await writeFixture('python-conventions.md', '# Conventions\n\n- Use Black formatting.\n');

      const result = await generateClaudeMd(makeConfig());

      expect(result).toMatch(/<!--.*[Gg]enerated.*do not edit/i);
    });

    it('should be under 120 lines', async () => {
      await writeFixture('VISION.md', '# Vision\n\nThis is a quickstart template for agent-augmented development.\n');
      await writeFixture('quickref.md', '# Quick Ref\n\n- `src/` — Source\n- `tests/` — Tests\n- `doctrine/` — Governance\n');
      await writeFixture('python-conventions.md', '# Conventions\n\n- Black formatting\n- Ruff linting\n- Type hints required\n');

      const result = await generateClaudeMd(makeConfig());
      const lines = result.split('\n');

      expect(lines.length).toBeLessThanOrEqual(120);
    });

    it('should start with a project heading', async () => {
      await writeFixture('VISION.md', '# Vision\n\nA quickstart template.\n');
      await writeFixture('quickref.md', '');
      await writeFixture('python-conventions.md', '');

      const result = await generateClaudeMd(makeConfig());

      // Should have an H1 heading
      expect(result).toMatch(/^<!-- .+-->\n# /m);
    });
  });

  describe('Content sections', () => {
    it('should contain project purpose from VISION.md', async () => {
      await writeFixture('VISION.md', `# Repository Vision

This repository serves as a quickstart template and reference implementation for agent-augmented development workflows.

## Problem

Teams face challenges with token inefficiency and maintenance overhead.
`);
      await writeFixture('quickref.md', '# QR\n\n- `src/`\n');
      await writeFixture('python-conventions.md', '# Conv\n\n- Black\n');

      const result = await generateClaudeMd(makeConfig());

      expect(result).toContain('quickstart template');
    });

    it('should contain repository structure from quick reference', async () => {
      await writeFixture('VISION.md', '# Vision\n\nA template.\n');
      await writeFixture('quickref.md', `# Repository Quick Reference

Key Directories:

- \`src/\` — Source code
- \`tests/\` — Test suites
- \`doctrine/\` — Agent governance
- \`work/\` — Orchestration workspace
- \`docs/\` — Documentation
`);
      await writeFixture('python-conventions.md', '# Conv\n\n- Black\n');

      const result = await generateClaudeMd(makeConfig());

      expect(result).toContain('src/');
      expect(result).toContain('doctrine/');
    });

    it('should contain coding conventions from python-conventions.md', async () => {
      await writeFixture('VISION.md', '# Vision\n\nA template.\n');
      await writeFixture('quickref.md', '# QR\n\n- `src/`\n');
      await writeFixture('python-conventions.md', `# Python Conventions

## Formatting

- Use Black for formatting (line length 120).
- Use Ruff for linting.
- Type hints required for public functions.
`);

      const result = await generateClaudeMd(makeConfig());

      expect(result).toContain('Black');
    });

    it('should contain common commands section', async () => {
      await writeFixture('VISION.md', '# Vision\n\nA template.\n');
      await writeFixture('quickref.md', '# QR\n\n- `src/`\n');
      await writeFixture('python-conventions.md', '# Conv\n\n- Black\n');

      const result = await generateClaudeMd(makeConfig());

      expect(result).toMatch(/[Cc]omm(?:on\s+)?[Cc]ommands/);
      expect(result).toMatch(/pytest|npm/);
    });

    it('should contain pointers to deeper context', async () => {
      await writeFixture('VISION.md', '# Vision\n\nA template.\n');
      await writeFixture('quickref.md', '# QR\n\n- `src/`\n');
      await writeFixture('python-conventions.md', '# Conv\n\n- Black\n');

      const result = await generateClaudeMd(makeConfig());

      expect(result).toContain('doctrine/');
      expect(result).toMatch(/\.claude\/rules\//);
    });
  });

  describe('Graceful degradation', () => {
    it('should handle missing VISION.md gracefully', async () => {
      await writeFixture('quickref.md', '# QR\n\n- `src/`\n');
      await writeFixture('python-conventions.md', '# Conv\n\n- Black\n');

      const config = makeConfig({ visionFile: path.join(tmpDir, 'missing-vision.md') });
      const result = await generateClaudeMd(config);

      expect(typeof result).toBe('string');
      expect(result.split('\n').length).toBeLessThanOrEqual(120);
    });

    it('should handle missing quickref file gracefully', async () => {
      await writeFixture('VISION.md', '# Vision\n\nA template.\n');
      await writeFixture('python-conventions.md', '# Conv\n\n- Black\n');

      const config = makeConfig({ quickRefFile: path.join(tmpDir, 'missing-qr.md') });
      const result = await generateClaudeMd(config);

      expect(typeof result).toBe('string');
      expect(result).toContain('template');
    });

    it('should handle missing conventions file gracefully', async () => {
      await writeFixture('VISION.md', '# Vision\n\nA template.\n');
      await writeFixture('quickref.md', '# QR\n\n- `src/`\n');

      const config = makeConfig({ pythonConventionsFile: path.join(tmpDir, 'missing-conv.md') });
      const result = await generateClaudeMd(config);

      expect(typeof result).toBe('string');
      expect(result).toContain('template');
    });

    it('should handle all files missing gracefully', async () => {
      const config = makeConfig({
        visionFile: path.join(tmpDir, 'nope1.md'),
        quickRefFile: path.join(tmpDir, 'nope2.md'),
        pythonConventionsFile: path.join(tmpDir, 'nope3.md')
      });

      const result = await generateClaudeMd(config);

      expect(typeof result).toBe('string');
      expect(result).toMatch(/<!--.*[Gg]enerated/);
      expect(result.split('\n').length).toBeLessThanOrEqual(120);
    });
  });

  describe('Content quality', () => {
    it('should NOT inline full doctrine content', async () => {
      // Create a large conventions file
      const longConventions = '# Python Conventions\n\n' +
        Array.from({ length: 100 }, (_, i) => `- Convention ${i + 1}: Detail ${i + 1} with explanatory text.`).join('\n');
      await writeFixture('VISION.md', '# Vision\n\nA template.\n');
      await writeFixture('quickref.md', '# QR\n\n- `src/`\n');
      await writeFixture('python-conventions.md', longConventions);

      const result = await generateClaudeMd(makeConfig());
      const lines = result.split('\n');

      // Even with 100-line source, output must stay under 120
      expect(lines.length).toBeLessThanOrEqual(120);
    });
  });
});
