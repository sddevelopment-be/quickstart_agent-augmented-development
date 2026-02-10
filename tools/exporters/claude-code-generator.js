/**
 * Claude Code Generator
 *
 * Transforms doctrine IR into Claude Code-native artifacts:
 * - simplifyAgent(): Full agent IR → lean subagent definition (<40 lines)
 * - generateRulesFile(): Doctrine sources → concise .claude/rules/*.md (<80 lines)
 * - generateClaudeMd(): Source files → CLAUDE.md project instructions (<120 lines)
 *
 * @module claude-code-generator
 * @version 1.0.0
 * @see SPEC-DIST-002
 * @see work/reports/architecture/2026-02-10-SPEC-DIST-002-technical-design.md
 */

// Tool name mapping: doctrine lowercase/mixed → Claude Code PascalCase
const TOOL_MAP = {
  'read': 'Read',
  'write': 'Write',
  'search': 'Grep',
  'edit': 'Edit',
  'bash': 'Bash',
  'Bash': 'Bash',
  'Grep': 'Grep',
  'Glob': 'Glob',
  'MultiEdit': 'MultiEdit',
  'Python': 'Bash',
  'Java': 'Bash',
  'Docker': 'Bash',
  'Node': 'Bash',
  'plantuml': 'Bash',
  'markdown-linter': 'Bash',
  'todo': 'Bash',
  'github': 'Bash',
  'comment': 'Bash',
  'summarize': 'Bash',
  'cpell': 'Bash',
  'awk': 'Bash',
  'grep': 'Grep',
  'yaml': 'Bash',
  'custom-agent': 'Bash',
  'web': 'WebFetch',
  'mermaid-generator': 'Bash',
  'plantuml-generator': 'Bash',
  'graphviz-generator': 'Bash'
};

// Model inference from agent name/role
const OPUS_AGENTS = ['architect', 'reviewer', 'analyst', 'code-reviewer'];
const HAIKU_AGENTS = [];

/**
 * Map doctrine tool names to Claude Code native tool names, deduplicating.
 *
 * @param {string[]} tools - Array of doctrine tool names
 * @returns {string[]} Deduplicated Claude Code tool names
 */
function mapTools(tools) {
  if (!tools || !Array.isArray(tools) || tools.length === 0) {
    return [];
  }

  const mapped = tools.map(t => TOOL_MAP[t] || TOOL_MAP[t.toLowerCase()] || t);
  return [...new Set(mapped)];
}

/**
 * Infer model hint from agent name.
 *
 * @param {string} name - Agent name (e.g. 'architect-alphonso', 'backend-benny')
 * @returns {string} Model hint: 'opus', 'sonnet', or 'haiku'
 */
function inferModel(name) {
  const lower = (name || '').toLowerCase();
  if (OPUS_AGENTS.some(role => lower.includes(role))) {
    return 'opus';
  }
  if (HAIKU_AGENTS.some(role => lower.includes(role))) {
    return 'haiku';
  }
  return 'sonnet';
}

/**
 * Extract bullet items matching a label from specialization text.
 *
 * @param {string} specialization - Raw specialization section content
 * @param {string} label - Label to extract (e.g. 'Primary focus', 'Avoid')
 * @returns {string|null} Extracted content after the label, or null
 */
function extractBullet(specialization, label) {
  if (!specialization) return null;
  const regex = new RegExp(`\\*\\*${label}:\\*\\*\\s*(.+)`, 'i');
  const match = specialization.match(regex);
  return match ? match[1].trim() : null;
}

/**
 * Truncate a string to a maximum number of sentences.
 *
 * @param {string} text - Input text
 * @param {number} maxSentences - Maximum number of sentences
 * @returns {string} Truncated text
 */
function truncateSentences(text, maxSentences) {
  if (!text) return '';
  const sentences = text.match(/[^.!?]+[.!?]+/g);
  if (!sentences) return text;
  return sentences.slice(0, maxSentences).join(' ').trim();
}

/**
 * Simplify a full doctrine agent IR into a lean Claude Code subagent definition.
 *
 * Strips directive tables, bootstrap declarations, mode protocols, context sources,
 * collaboration contract boilerplate. Retains name, description, tools, model hint,
 * purpose, and key specialization bullets.
 *
 * @param {Object} agentIR - IR object from parser.js
 * @returns {string} Simplified markdown (<40 lines) for .claude/agents/*.md
 */
function simplifyAgent(agentIR) {
  const { frontmatter, content } = agentIR;

  // Map tools and infer model
  const tools = mapTools(frontmatter.tools);
  const model = inferModel(frontmatter.name);

  // Build YAML frontmatter
  const toolsStr = tools.length > 0
    ? `[${tools.join(', ')}]`
    : '[]';

  const lines = [
    '---',
    `name: ${frontmatter.name}`,
    `description: ${frontmatter.description}`,
    `tools: ${toolsStr}`,
    `model: ${model}`,
    '---',
    ''
  ];

  // Purpose (max 3 sentences)
  if (content.purpose) {
    lines.push(truncateSentences(content.purpose, 3));
    lines.push('');
  }

  // Specialization: primary focus
  const primaryFocus = extractBullet(content.specialization, 'Primary focus');
  if (primaryFocus) {
    lines.push('Focus on:');
    lines.push(`- ${primaryFocus}`);
    lines.push('');
  }

  // Specialization: avoid
  const avoid = extractBullet(content.specialization, 'Avoid');
  if (avoid) {
    lines.push('Avoid:');
    lines.push(`- ${avoid}`);
    lines.push('');
  }

  // Trim trailing empty lines, ensure single trailing newline
  while (lines.length > 0 && lines[lines.length - 1] === '') {
    lines.pop();
  }
  lines.push('');

  return lines.join('\n');
}

const fs = require('fs').promises;
const path = require('path');
const matter = require('gray-matter');

const MAX_RULES_LINES = 80;

/**
 * Read a file safely, returning empty string on failure.
 *
 * @param {string} filePath - Path to file
 * @returns {Promise<string>} File content or empty string
 */
async function safeReadFile(filePath) {
  try {
    return await fs.readFile(filePath, 'utf-8');
  } catch {
    return '';
  }
}

/**
 * Strip non-actionable content from a doctrine markdown file body.
 * Removes: version/date metadata, horizontal rules, blockquotes, H1 titles.
 * Preserves: section headings (H2+), bullet points, numbered lists, prose.
 *
 * @param {string} body - Markdown body (frontmatter already stripped)
 * @returns {string[]} Array of cleaned lines
 */
function stripMetadata(body) {
  const lines = body.split('\n');
  const cleaned = [];
  let inBlockquote = false;

  for (const line of lines) {
    // Skip version/date metadata lines (italic format)
    if (/^_(?:Version|Last updated|Format):/.test(line)) continue;
    // Skip standalone horizontal rules
    if (/^---\s*$/.test(line.trim())) continue;
    // Skip blockquote advisory notes (including continuation lines)
    if (/^>\s/.test(line)) {
      inBlockquote = true;
      continue;
    }
    if (inBlockquote) {
      // Continuation of blockquote: non-empty, non-heading line after a > line
      if (line.trim() !== '' && !line.startsWith('#') && !line.startsWith('-') && !line.startsWith('*') && !/^\d+\./.test(line)) {
        continue;
      }
      inBlockquote = false;
    }
    // Skip H1 headings (title of the source doc — we use our own)
    if (/^#\s+[^#]/.test(line)) continue;
    // Skip HTML comments
    if (/^<!--.*-->$/.test(line.trim())) continue;

    cleaned.push(line);
  }

  return cleaned;
}

/**
 * Convert a rule name to a title-case heading.
 *
 * @param {string} ruleName - Rule name (e.g. 'coding-conventions')
 * @returns {string} Title-cased heading (e.g. 'Coding Conventions')
 */
function ruleNameToTitle(ruleName) {
  return ruleName
    .split('-')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

/**
 * Generate a concise .claude/rules/*.md file from doctrine source files.
 *
 * Reads source files, strips metadata, merges actionable content,
 * adds source attribution, enforces 80-line limit.
 *
 * @param {string[]} sourceFiles - Array of absolute paths to doctrine source files
 * @param {string} ruleName - Rule identifier (e.g. 'guidelines', 'testing')
 * @returns {Promise<string>} Markdown string for the rules file (<80 lines)
 */
async function generateRulesFile(sourceFiles, ruleName) {
  const title = ruleNameToTitle(ruleName);

  // Build source attribution from basenames
  const fileNames = sourceFiles.map(f => path.basename(f));
  const attribution = `<!-- Source: ${fileNames.join(', ')} -->`;

  // Read and process each source file
  const allContentLines = [];
  for (const filePath of sourceFiles) {
    const raw = await safeReadFile(filePath);
    if (!raw) continue;

    // Strip YAML frontmatter using gray-matter
    const { content: body } = matter(raw);
    const cleaned = stripMetadata(body);
    allContentLines.push(...cleaned);
  }

  // Remove leading/trailing blank lines from merged content
  while (allContentLines.length > 0 && allContentLines[0].trim() === '') {
    allContentLines.shift();
  }
  while (allContentLines.length > 0 && allContentLines[allContentLines.length - 1].trim() === '') {
    allContentLines.pop();
  }

  // Assemble output: attribution + title + content
  const header = [attribution, `# ${title}`, ''];
  const headerLineCount = header.length;
  const maxContentLines = MAX_RULES_LINES - headerLineCount - 1; // -1 for trailing newline

  // Truncate content if needed
  const truncatedContent = allContentLines.slice(0, maxContentLines);

  // Remove trailing blank lines from truncated content
  while (truncatedContent.length > 0 && truncatedContent[truncatedContent.length - 1].trim() === '') {
    truncatedContent.pop();
  }

  const output = [...header, ...truncatedContent, ''];
  return output.join('\n');
}

const MAX_CLAUDE_MD_LINES = 120;

/**
 * Extract the first meaningful paragraph from VISION.md content.
 * Looks for the opening description (before first ## heading).
 *
 * @param {string} content - Raw VISION.md content
 * @returns {string} Purpose paragraph (3-4 lines max)
 */
function extractPurpose(content) {
  if (!content) return '';
  const { content: body } = matter(content);
  const lines = body.split('\n');
  const paragraphs = [];
  let current = [];

  for (const line of lines) {
    // Stop at first H2 heading
    if (/^##\s/.test(line)) break;
    // Skip H1, metadata, HRs, HTML comments
    if (/^#\s/.test(line)) continue;
    if (/^_(?:Version|Last updated|Format):/.test(line)) continue;
    if (/^---\s*$/.test(line.trim())) continue;
    if (/^<!--.*-->$/.test(line.trim())) continue;

    if (line.trim() === '') {
      if (current.length > 0) {
        paragraphs.push(current.join(' ').trim());
        current = [];
      }
    } else {
      current.push(line.trim());
    }
  }
  if (current.length > 0) {
    paragraphs.push(current.join(' ').trim());
  }

  return paragraphs[0] || '';
}

/**
 * Extract directory listing from quick reference content.
 * Keeps only top-level directory bullets.
 *
 * @param {string} content - Raw quick reference markdown
 * @returns {string[]} Array of directory description lines
 */
function extractStructure(content) {
  if (!content) return [];
  const { content: body } = matter(content);
  const lines = body.split('\n');
  const dirs = [];

  for (const line of lines) {
    // Match top-level bullet items with backtick-wrapped paths
    if (/^- `[^`]+\/`/.test(line)) {
      dirs.push(line);
    }
  }

  // Keep only key directories (max 8)
  return dirs.slice(0, 8);
}

/**
 * Extract top-level conventions from python-conventions.md.
 * Keeps the first few actionable bullet points.
 *
 * @param {string} content - Raw conventions markdown
 * @returns {string[]} Array of convention lines
 */
function extractConventions(content) {
  if (!content) return [];
  const { content: body } = matter(content);
  const lines = body.split('\n');
  const conventions = [];

  for (const line of lines) {
    if (/^- /.test(line) && conventions.length < 8) {
      conventions.push(line);
    }
  }

  return conventions;
}

/**
 * Generate CLAUDE.md project instructions from source doctrine files.
 *
 * Composes a concise project overview with purpose, structure, conventions,
 * common commands, and pointers to deeper context. Enforces 120-line limit.
 * Handles missing source files gracefully.
 *
 * @param {Object} config - Configuration with source file paths
 * @param {string} config.visionFile - Path to docs/VISION.md
 * @param {string} config.quickRefFile - Path to doctrine/directives/003_*.md
 * @param {string} config.pythonConventionsFile - Path to doctrine/guidelines/python-conventions.md
 * @param {string} config.projectRoot - Repository root path
 * @returns {Promise<string>} Markdown string for CLAUDE.md (<120 lines)
 */
async function generateClaudeMd(config) {
  const { visionFile, quickRefFile, pythonConventionsFile } = config;

  // Read source files (graceful degradation)
  const [visionRaw, quickRefRaw, conventionsRaw] = await Promise.all([
    safeReadFile(visionFile),
    safeReadFile(quickRefFile),
    safeReadFile(pythonConventionsFile)
  ]);

  const lines = [
    '<!-- Generated from doctrine/ — do not edit manually -->',
    '# Project Instructions',
    ''
  ];

  // Section 1: Purpose
  const purpose = extractPurpose(visionRaw);
  if (purpose) {
    lines.push('## Purpose', '', purpose, '');
  }

  // Section 2: Repository Structure
  const structure = extractStructure(quickRefRaw);
  if (structure.length > 0) {
    lines.push('## Repository Structure', '');
    lines.push(...structure);
    lines.push('');
  }

  // Section 3: Coding Conventions
  const conventions = extractConventions(conventionsRaw);
  if (conventions.length > 0) {
    lines.push('## Coding Conventions', '');
    lines.push(...conventions);
    lines.push('');
  }

  // Section 4: Common Commands (hardcoded per spec)
  lines.push('## Common Commands', '');
  lines.push('```bash');
  lines.push('python -m pytest                    # Run all tests');
  lines.push('python -m pytest tests/unit/        # Run unit tests');
  lines.push('npm run deploy:claude               # Deploy Claude Code artifacts');
  lines.push('npm run export:all                  # Export all distributions');
  lines.push('npm test                            # Run JS tests');
  lines.push('```');
  lines.push('');

  // Section 5: Deeper Context pointers
  lines.push('## Further Reference', '');
  lines.push('- `doctrine/` — Full governance stack (guidelines, directives, approaches)');
  lines.push('- `.claude/rules/` — Auto-loaded coding and collaboration rules');
  lines.push('- `.claude/agents/` — Specialist agent definitions');
  lines.push('- `.claude/skills/` — On-demand skill prompts');
  lines.push('- `docs/` — Architecture decisions, templates, vision');
  lines.push('');

  // Enforce line limit by truncating from the bottom if needed
  if (lines.length > MAX_CLAUDE_MD_LINES) {
    lines.length = MAX_CLAUDE_MD_LINES - 1;
    lines.push('');
  }

  return lines.join('\n');
}

// Source-to-rules mapping configuration (FR-2)
const RULES_MAPPING = {
  'guidelines': [
    'doctrine/guidelines/general_guidelines.md',
    'doctrine/guidelines/operational_guidelines.md'
  ],
  'coding-conventions': [
    'doctrine/guidelines/python-conventions.md'
  ],
  'testing': [
    'doctrine/directives/016_acceptance_test_driven_development.md',
    'doctrine/directives/017_test_driven_development.md'
  ],
  'architecture': [
    'doctrine/directives/018_traceable_decisions.md'
  ],
  'collaboration': [
    'doctrine/directives/019_file_based_collaboration.md'
  ]
};

module.exports = {
  simplifyAgent,
  generateRulesFile,
  generateClaudeMd,
  mapTools,
  inferModel,
  TOOL_MAP,
  RULES_MAPPING
};
