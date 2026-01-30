/**
 * Prompt Template Exporter
 *
 * Parses .prompt.md files and exports them as reusable skills for
 * Claude Code, GitHub Copilot, and OpenCode formats.
 *
 * @module ops/exporters/prompt-template-exporter
 * @version 1.0.0
 *
 * Following Directives:
 * - 016 (ATDD): Acceptance tests written first
 * - 017 (TDD): Unit tests with Red-Green-Refactor
 */

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');
const matter = require('gray-matter');

const EXPORTER_VERSION = '1.0.0';

/**
 * Custom error class for parsing errors
 */
class PromptParseError extends Error {
  constructor(message, filePath, cause) {
    super(message);
    this.name = 'PromptParseError';
    this.filePath = filePath;
    this.cause = cause;
  }
}

/**
 * Parse a prompt template file
 *
 * @param {string} filePath - Path to the .prompt.md file
 * @returns {Promise<Object>} Parsed prompt template
 */
async function parsePromptTemplate(filePath) {
  const content = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(content);

  // Validate required frontmatter fields
  const requiredFields = ['description', 'agent', 'category', 'complexity', 'inputs_required', 'outputs'];
  for (const field of requiredFields) {
    if (!frontmatter[field]) {
      throw new PromptParseError(
        `Missing required field '${field}' in ${filePath}`,
        filePath
      );
    }
  }

  // Parse inputs from markdown body
  const inputs = extractInputs(body);
  const tasks = extractTasks(body);
  const outputs = extractOutputs(body);
  const constraints = extractConstraints(body);

  // Generate slug from filename
  const filename = path.basename(filePath, '.prompt.md');
  const slug = filename.toLowerCase().replace(/_/g, '-');

  return {
    id: slug,
    filename,
    frontmatter: {
      description: frontmatter.description,
      agent: frontmatter.agent,
      category: frontmatter.category,
      complexity: frontmatter.complexity,
      inputs_required: parseCommaSeparated(frontmatter.inputs_required),
      outputs: parseCommaSeparated(frontmatter.outputs),
      tags: frontmatter.tags || [],
      version: frontmatter.version || 'unknown'
    },
    content: {
      raw_body: body.trim(),
      inputs,
      tasks,
      outputs,
      constraints
    },
    metadata: {
      file_path: path.relative(process.cwd(), filePath),
      source_hash: crypto.createHash('sha256').update(content).digest('hex'),
      parsed_at: new Date().toISOString(),
      exporter_version: EXPORTER_VERSION
    }
  };
}

/**
 * Parse comma-separated string or return array as-is
 */
function parseCommaSeparated(value) {
  if (Array.isArray(value)) return value;
  if (typeof value === 'string') {
    return value.split(',').map(s => s.trim()).filter(Boolean);
  }
  return [];
}

/**
 * Extract inputs section from prompt body
 */
function extractInputs(body) {
  const inputSection = extractSection(body, /^##\s*Inputs/i);
  if (!inputSection) return [];

  const inputs = [];
  const lines = inputSection.split('\n');

  for (const line of lines) {
    // Match "- Name (description): <PLACEHOLDER>" pattern
    const match = line.match(/^-\s*(.+?)(?:\s*\(([^)]+)\))?:\s*\\?<(\w+)>/);
    if (match) {
      inputs.push({
        name: match[1].trim(),
        description: match[2] ? match[2].trim() : null,
        placeholder: match[3]
      });
    }
  }

  return inputs;
}

/**
 * Extract tasks section from prompt body
 */
function extractTasks(body) {
  const taskSection = extractSection(body, /^##\s*Task/i);
  if (!taskSection) return [];

  const tasks = [];
  const lines = taskSection.split('\n');

  for (const line of lines) {
    // Match numbered task steps "1. Do something"
    const match = line.match(/^(\d+)\.\s*(.+)$/);
    if (match) {
      tasks.push({
        step: parseInt(match[1], 10),
        description: match[2].trim()
      });
    }
  }

  return tasks;
}

/**
 * Extract outputs section from prompt body
 */
function extractOutputs(body) {
  const outputSection = extractSection(body, /^##\s*Output/i);
  if (!outputSection) return [];

  const outputs = [];
  const lines = outputSection.split('\n');

  for (const line of lines) {
    // Match "- Output item" pattern
    const match = line.match(/^-\s*(.+)$/);
    if (match) {
      outputs.push(match[1].trim());
    }
  }

  return outputs;
}

/**
 * Extract constraints section from prompt body
 */
function extractConstraints(body) {
  const constraintSection = extractSection(body, /^##\s*Constraints/i);
  if (!constraintSection) return [];

  const constraints = [];
  const lines = constraintSection.split('\n');

  for (const line of lines) {
    // Match "- Constraint" pattern
    const match = line.match(/^-\s*(.+)$/);
    if (match) {
      constraints.push(match[1].trim());
    }
  }

  return constraints;
}

/**
 * Extract a markdown section by heading pattern
 */
function extractSection(content, headingPattern) {
  const lines = content.split('\n');
  let inSection = false;
  let sectionLines = [];
  let sectionLevel = null;

  for (const line of lines) {
    if (headingPattern.test(line)) {
      inSection = true;
      const match = line.match(/^(#{1,6})\s/);
      sectionLevel = match ? match[1].length : 2;
      continue;
    }

    if (inSection) {
      const headingMatch = line.match(/^(#{1,6})\s/);
      if (headingMatch && headingMatch[1].length <= sectionLevel) {
        break;
      }
      sectionLines.push(line);
    }
  }

  return sectionLines.length > 0 ? sectionLines.join('\n').trim() : null;
}

/**
 * Generate Claude Code skill format from parsed prompt
 *
 * @param {Object} prompt - Parsed prompt template
 * @returns {Object} Claude Code skill definition
 */
function generateClaudeCodeSkill(prompt) {
  return {
    skill_version: '1.0',
    skill: {
      id: prompt.id,
      name: formatSkillName(prompt.filename),
      description: prompt.frontmatter.description,
      type: 'prompt-template',
      category: prompt.frontmatter.category,
      complexity: prompt.frontmatter.complexity,
      invoke: `/${prompt.id}`,
      agent: prompt.frontmatter.agent,
      inputs: prompt.content.inputs.map(i => ({
        name: i.placeholder,
        description: i.description || i.name,
        required: true
      })),
      workflow: prompt.content.tasks.map(t => t.description),
      outputs: prompt.content.outputs,
      constraints: prompt.content.constraints,
      tags: prompt.frontmatter.tags
    },
    instructions: prompt.content.raw_body,
    metadata: {
      source_file: prompt.metadata.file_path,
      source_hash: prompt.metadata.source_hash,
      exported_at: new Date().toISOString(),
      exporter_version: EXPORTER_VERSION
    }
  };
}

/**
 * Generate GitHub Copilot skill format from parsed prompt
 *
 * @param {Object} prompt - Parsed prompt template
 * @returns {Object} Copilot skill definition
 */
function generateCopilotSkill(prompt) {
  return {
    $schema: 'https://aka.ms/copilot-skill-schema',
    name: prompt.id,
    description: prompt.frontmatter.description,
    capabilities: [
      prompt.frontmatter.category,
      `complexity-${prompt.frontmatter.complexity}`,
      ...prompt.frontmatter.tags.slice(0, 3)
    ],
    instructions: prompt.content.raw_body,
    conversation_starters: generateConversationStarters(prompt),
    workspace: {
      settings: {}
    },
    extensions: {
      agentic_framework: {
        agent: prompt.frontmatter.agent,
        category: prompt.frontmatter.category,
        complexity: prompt.frontmatter.complexity,
        inputs: prompt.frontmatter.inputs_required,
        outputs: prompt.frontmatter.outputs
      }
    }
  };
}

/**
 * Generate OpenCode skill format from parsed prompt
 *
 * @param {Object} prompt - Parsed prompt template
 * @returns {Object} OpenCode skill definition
 */
function generateOpenCodeSkill(prompt) {
  return {
    opencode_version: '1.0',
    skill: {
      id: prompt.id,
      name: formatSkillName(prompt.filename),
      version: prompt.frontmatter.version,
      description: prompt.frontmatter.description,
      type: 'prompt-template',
      category: prompt.frontmatter.category,
      agent: prompt.frontmatter.agent,
      invoke_pattern: `/${prompt.id} <inputs>`,
      inputs: prompt.content.inputs.map(i => ({
        name: i.placeholder,
        label: i.name,
        description: i.description,
        required: true,
        type: 'string'
      })),
      workflow_steps: prompt.content.tasks,
      expected_outputs: prompt.content.outputs,
      constraints: prompt.content.constraints,
      tags: prompt.frontmatter.tags,
      profile_url: prompt.metadata.file_path
    },
    metadata: {
      source_hash: prompt.metadata.source_hash,
      exported_at: new Date().toISOString(),
      exporter_version: EXPORTER_VERSION
    }
  };
}

/**
 * Generate conversation starters based on prompt content
 */
function generateConversationStarters(prompt) {
  const starters = [];
  const category = prompt.frontmatter.category.toLowerCase();

  // Category-specific starters
  if (category === 'architecture') {
    starters.push(
      `Help me create an ADR for a design decision`,
      `Analyze trade-offs for ${prompt.frontmatter.inputs_required[0] || 'this decision'}`
    );
  } else if (category === 'automation') {
    starters.push(
      `Generate a script for ${prompt.frontmatter.inputs_required[0] || 'automation'}`,
      `Create CI/CD workflow for this task`
    );
  } else if (category === 'documentation') {
    starters.push(
      `Help me document this ${prompt.frontmatter.inputs_required[0] || 'component'}`,
      `Review and improve this documentation`
    );
  } else if (category === 'agent-management') {
    starters.push(
      `Create a new agent for ${prompt.frontmatter.inputs_required[0] || 'this domain'}`,
      `Help me define agent responsibilities`
    );
  }

  // Generic starter based on description
  starters.push(`${prompt.frontmatter.description.replace(/^Prompt for .+ to /, 'Help me ')}`);

  return starters.slice(0, 4);
}

/**
 * Format filename to readable skill name
 */
function formatSkillName(filename) {
  return filename
    .replace(/_/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase());
}

/**
 * Parse all prompt templates in a directory
 *
 * @param {string} directory - Path to prompts directory
 * @returns {Promise<Array>} Array of parsed prompt templates
 */
async function parsePromptDirectory(directory) {
  const files = await fs.readdir(directory);
  const promptFiles = files.filter(f => f.endsWith('.prompt.md'));

  const prompts = [];
  for (const file of promptFiles) {
    try {
      const prompt = await parsePromptTemplate(path.join(directory, file));
      prompts.push(prompt);
    } catch (error) {
      console.error(`Warning: Failed to parse ${file}: ${error.message}`);
    }
  }

  return prompts;
}

/**
 * Export all prompt templates to skill formats
 *
 * @param {string} inputDir - Directory containing .prompt.md files
 * @param {string} outputDir - Output directory for generated files
 * @returns {Promise<Object>} Export results
 */
async function exportPromptTemplates(inputDir, outputDir) {
  const prompts = await parsePromptDirectory(inputDir);

  // Create output directories
  const claudeDir = path.join(outputDir, 'claude-code');
  const copilotDir = path.join(outputDir, 'copilot');
  const opencodeDir = path.join(outputDir, 'opencode');

  await fs.mkdir(claudeDir, { recursive: true });
  await fs.mkdir(copilotDir, { recursive: true });
  await fs.mkdir(opencodeDir, { recursive: true });

  const results = {
    total: prompts.length,
    exported: [],
    errors: []
  };

  for (const prompt of prompts) {
    try {
      // Generate Claude Code skill
      const claudeSkill = generateClaudeCodeSkill(prompt);
      const claudePath = path.join(claudeDir, `${prompt.id}.skill.json`);
      await fs.writeFile(claudePath, JSON.stringify(claudeSkill, null, 2));

      // Generate Copilot skill
      const copilotSkill = generateCopilotSkill(prompt);
      const copilotPath = path.join(copilotDir, `${prompt.id}.copilot-skill.json`);
      await fs.writeFile(copilotPath, JSON.stringify(copilotSkill, null, 2));

      // Generate OpenCode skill
      const opencodeSkill = generateOpenCodeSkill(prompt);
      const opencodePath = path.join(opencodeDir, `${prompt.id}.opencode-skill.json`);
      await fs.writeFile(opencodePath, JSON.stringify(opencodeSkill, null, 2));

      results.exported.push({
        id: prompt.id,
        files: {
          claude: claudePath,
          copilot: copilotPath,
          opencode: opencodePath
        }
      });
    } catch (error) {
      results.errors.push({
        id: prompt.id,
        error: error.message
      });
    }
  }

  // Generate manifest
  const manifest = {
    manifest_version: '1.0',
    type: 'prompt-templates',
    generated_at: new Date().toISOString(),
    exporter_version: EXPORTER_VERSION,
    skills: results.exported.map(e => ({
      id: e.id,
      formats: ['claude-code', 'copilot', 'opencode']
    })),
    total_skills: results.exported.length
  };

  await fs.writeFile(
    path.join(outputDir, 'prompt-skills-manifest.json'),
    JSON.stringify(manifest, null, 2)
  );

  return results;
}

module.exports = {
  parsePromptTemplate,
  parsePromptDirectory,
  generateClaudeCodeSkill,
  generateCopilotSkill,
  generateOpenCodeSkill,
  exportPromptTemplates,
  PromptParseError
};
