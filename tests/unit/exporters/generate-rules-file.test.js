/**
 * Unit Tests: claude-code-generator.js — generateRulesFile()
 *
 * Following Directive 017 (TDD): RED phase — tests before implementation.
 * Following Directive 016 (ATDD): Tests define acceptance criteria from SPEC-DIST-002 FR-2.
 *
 * Acceptance Criteria (AC-2):
 * - Each rules file under 80 lines
 * - Contains source attribution comment
 * - Rules content matches source doctrine (no invented instructions)
 * - Metadata stripped (version history, timestamps, related sections)
 * - Actionable content preserved
 */

const fs = require('fs').promises;
const path = require('path');
const os = require('os');
const { generateRulesFile } = require('../../../tools/exporters/claude-code-generator');

let tmpDir;

beforeEach(async () => {
  tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'rules-test-'));
});

afterEach(async () => {
  await fs.rm(tmpDir, { recursive: true, force: true });
});

// Helper to write a temp doctrine file
async function writeFixture(name, content) {
  const filePath = path.join(tmpDir, name);
  await fs.writeFile(filePath, content, 'utf-8');
  return filePath;
}

describe('generateRulesFile', () => {

  describe('Output structure', () => {
    it('should return a string with source attribution comment', async () => {
      const src = await writeFixture('guidelines.md', `# General Guidelines

## Behaviour

- Act as a careful assistant.
- Prefer clarity over cleverness.
`);
      const result = await generateRulesFile([src], 'guidelines');

      expect(typeof result).toBe('string');
      expect(result).toMatch(/<!--\s*Source:/);
    });

    it('should include rule name as H1 heading', async () => {
      const src = await writeFixture('guidelines.md', `# General Guidelines

## Behaviour

- Act carefully.
`);
      const result = await generateRulesFile([src], 'guidelines');

      expect(result).toMatch(/^# Guidelines\n/m);
    });

    it('should be under 80 lines', async () => {
      // Create a large source file (200+ lines)
      const longContent = '# Long Document\n\n' +
        Array.from({ length: 200 }, (_, i) => `- Rule ${i + 1}: Do thing ${i + 1}.`).join('\n');
      const src = await writeFixture('long.md', longContent);

      const result = await generateRulesFile([src], 'testing');
      const lines = result.split('\n');

      expect(lines.length).toBeLessThanOrEqual(80);
    });
  });

  describe('Metadata stripping', () => {
    it('should strip YAML frontmatter', async () => {
      const src = await writeFixture('with-frontmatter.md', `---
version: 1.0.0
last_updated: 2025-11-23
---

# Guidelines

## Rules

- Do good things.
- Avoid bad things.
`);
      const result = await generateRulesFile([src], 'guidelines');

      expect(result).not.toContain('version: 1.0.0');
      expect(result).not.toContain('last_updated');
      expect(result).not.toContain('---\nversion');
    });

    it('should strip version/date metadata lines', async () => {
      const src = await writeFixture('with-version.md', `# General Agent Guidelines

_Version: 1.1.0_
_Last updated: 2025-11-23_
_Format: Markdown protocol for agent initialization and governance_

---

## Behaviour

- Act as a careful assistant.
- Prefer clarity.
`);
      const result = await generateRulesFile([src], 'guidelines');

      expect(result).not.toContain('Version: 1.1.0');
      expect(result).not.toContain('Last updated');
      expect(result).not.toContain('Format: Markdown protocol');
    });

    it('should strip horizontal rules used as separators', async () => {
      const src = await writeFixture('with-hr.md', `# Guidelines

---

## Rules

- Rule one.

---

## More Rules

- Rule two.
`);
      const result = await generateRulesFile([src], 'guidelines');

      // Should not have standalone --- lines (except in frontmatter of output)
      const bodyLines = result.split('\n').filter(l => !l.startsWith('<!--'));
      const hrLines = bodyLines.filter(l => /^---$/.test(l.trim()));
      expect(hrLines.length).toBe(0);
    });

    it('should strip blockquote advisory notes', async () => {
      const src = await writeFixture('with-blockquote.md', `# Operational Guidelines

> For runtime brevity, reference
> some other file instead of pasting full sections.

## Rules

- Keep output structured.
- Always reference guidelines.
`);
      const result = await generateRulesFile([src], 'guidelines');

      expect(result).not.toContain('> For runtime');
      expect(result).toContain('Keep output structured');
    });
  });

  describe('Content preservation', () => {
    it('should preserve bullet-point instructions', async () => {
      const src = await writeFixture('instructions.md', `# Guidelines

## Behaviour

- Act as a careful, cooperative assistant.
- Prefer clarity over cleverness.
- Be explicit about assumptions.
- Keep changes small and reviewable.
`);
      const result = await generateRulesFile([src], 'guidelines');

      expect(result).toContain('Act as a careful, cooperative assistant');
      expect(result).toContain('Prefer clarity over cleverness');
      expect(result).toContain('Keep changes small and reviewable');
    });

    it('should preserve section headings (as H2 or H3)', async () => {
      const src = await writeFixture('with-sections.md', `# Guidelines

## Behaviour

- Be careful.

## Communication

- Be clear.
`);
      const result = await generateRulesFile([src], 'guidelines');

      expect(result).toMatch(/##\s+Behaviour/);
      expect(result).toMatch(/##\s+Communication/);
    });

    it('should preserve numbered list items', async () => {
      const src = await writeFixture('numbered.md', `# Decisions

## Guidelines for Agents

1. Document why decisions were made
2. Document architectural intent
3. Document key relationships
`);
      const result = await generateRulesFile([src], 'architecture');

      expect(result).toContain('Document why decisions were made');
      expect(result).toContain('Document architectural intent');
    });
  });

  describe('Multi-source merging', () => {
    it('should merge content from multiple source files', async () => {
      const src1 = await writeFixture('general.md', `# General Guidelines

## Behaviour

- Act carefully.
- Be explicit.
`);
      const src2 = await writeFixture('operational.md', `# Operational Guidelines

## Files and directories

- Use work/ for scratch notes.
- Prefer small incremental changes.
`);
      const result = await generateRulesFile([src1, src2], 'guidelines');

      expect(result).toContain('Act carefully');
      expect(result).toContain('scratch notes');
    });

    it('should include attribution for all source files', async () => {
      const src1 = await writeFixture('file-a.md', '# File A\n\n- Rule A.\n');
      const src2 = await writeFixture('file-b.md', '# File B\n\n- Rule B.\n');

      const result = await generateRulesFile([src1, src2], 'testing');

      expect(result).toContain('file-a.md');
      expect(result).toContain('file-b.md');
    });
  });

  describe('Edge cases', () => {
    it('should handle missing source files gracefully', async () => {
      const missing = path.join(tmpDir, 'nonexistent.md');

      const result = await generateRulesFile([missing], 'guidelines');

      expect(typeof result).toBe('string');
      expect(result).toMatch(/# Guidelines/);
    });

    it('should handle empty source files', async () => {
      const src = await writeFixture('empty.md', '');

      const result = await generateRulesFile([src], 'guidelines');

      expect(typeof result).toBe('string');
      expect(result).toMatch(/# Guidelines/);
    });

    it('should handle source with only frontmatter and no body', async () => {
      const src = await writeFixture('frontmatter-only.md', `---
version: 1.0.0
---
`);
      const result = await generateRulesFile([src], 'guidelines');

      expect(typeof result).toBe('string');
      expect(result).toMatch(/# Guidelines/);
    });
  });
});
