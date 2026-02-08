/**
 * Approach Exporter
 *
 * Parses approach documentation files and exports them as reusable
 * operational skills/guides for Claude Code, GitHub Copilot, and OpenCode.
 *
 * @module ops/exporters/approach-exporter
 * @version 1.0.0
 *
 * Following Directives:
 * - 016 (ATDD): Acceptance tests written first
 * - 017 (TDD): Unit tests with Red-Green-Refactor
 */

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

const EXPORTER_VERSION = '1.0.0';

/**
 * Custom error class for parsing errors
 */
class ApproachParseError extends Error {
  constructor(message, filePath, cause) {
    super(message);
    this.name = 'ApproachParseError';
    this.filePath = filePath;
    this.cause = cause;
  }
}

/**
 * Parse an approach documentation file
 *
 * @param {string} filePath - Path to the approach .md file
 * @returns {Promise<Object>} Parsed approach
 */
async function parseApproach(filePath) {
  const content = await fs.readFile(filePath, 'utf-8');
  const filename = path.basename(filePath, '.md');

  // Skip README files
  if (filename.toLowerCase() === 'readme') {
    return null;
  }

  // Extract header metadata (not YAML frontmatter, but markdown metadata block)
  const metadata = extractHeaderMetadata(content);

  // Extract sections
  const title = extractTitle(content);
  const overview = extractSection(content, /^##\s*(Overview|Purpose)/i);
  const principles = extractListSection(content, /^##\s*Core Principles/i);
  const whenToUse = extractWhenToUse(content);
  const workflow = extractWorkflow(content);
  const implementation = extractImplementationSteps(content);
  const references = extractReferences(content);
  const troubleshooting = extractTroubleshooting(content);

  // Generate slug from filename
  const slug = filename.toLowerCase().replace(/_/g, '-');

  return {
    id: slug,
    filename,
    title: title || formatTitle(filename),
    metadata: {
      type: metadata.approachType || 'Operational Pattern',
      version: metadata.version || '1.0.0',
      last_updated: metadata.lastUpdated || 'unknown',
      status: metadata.status || 'Active'
    },
    content: {
      overview: overview || '',
      principles,
      when_to_use: whenToUse.use,
      when_not_to_use: whenToUse.avoid,
      workflow,
      implementation_steps: implementation,
      references,
      troubleshooting
    },
    file_metadata: {
      file_path: path.relative(process.cwd(), filePath),
      source_hash: crypto.createHash('sha256').update(content).digest('hex'),
      parsed_at: new Date().toISOString(),
      exporter_version: EXPORTER_VERSION,
      word_count: content.split(/\s+/).length
    }
  };
}

/**
 * Extract header metadata from approach document
 * Format: **Key:** Value or **Key** Value
 */
function extractHeaderMetadata(content) {
  const metadata = {};
  const lines = content.split('\n').slice(0, 20); // Check first 20 lines

  for (const line of lines) {
    // Match **Approach Type:** Value or similar patterns
    const match = line.match(/^\*\*([^:*]+)(?:\*\*)?:?\*?\*?\s*(.+)$/);
    if (match) {
      const key = match[1].trim().toLowerCase().replace(/\s+/g, '_');
      const value = match[2].trim();

      if (key === 'approach_type') metadata.approachType = value;
      else if (key === 'version') metadata.version = value;
      else if (key === 'last_updated') metadata.lastUpdated = value;
      else if (key === 'status') metadata.status = value;
    }
  }

  return metadata;
}

/**
 * Extract the main title from the document
 */
function extractTitle(content) {
  const match = content.match(/^#\s+(.+)$/m);
  return match ? match[1].trim() : null;
}

/**
 * Extract a section by heading pattern
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
 * Extract a section and parse it into list items
 */
function extractListSection(content, headingPattern) {
  const section = extractSection(content, headingPattern);
  if (!section) return [];

  const items = [];
  const lines = section.split('\n');

  let currentItem = null;

  for (const line of lines) {
    // Match numbered items or ### subheadings
    const numberedMatch = line.match(/^###?\s*(\d+)\.\s*(.+)/);
    const bulletMatch = line.match(/^-\s+\*\*(.+?)\*\*\s*[–-]\s*(.+)/);

    if (numberedMatch) {
      if (currentItem) items.push(currentItem);
      currentItem = {
        number: parseInt(numberedMatch[1], 10),
        title: numberedMatch[2].trim(),
        description: ''
      };
    } else if (bulletMatch) {
      items.push({
        title: bulletMatch[1].trim(),
        description: bulletMatch[2].trim()
      });
    } else if (currentItem && line.trim() && !line.startsWith('#')) {
      currentItem.description += (currentItem.description ? ' ' : '') + line.trim();
    }
  }

  if (currentItem) items.push(currentItem);
  return items;
}

/**
 * Extract "When to Use" and "When NOT to Use" sections
 */
function extractWhenToUse(content) {
  const result = { use: [], avoid: [] };

  // Extract "When to Use" section
  const useSection = extractSection(content, /^##\s*When to Use/i);
  if (useSection) {
    const useMatch = useSection.match(/\*\*Use.*?when:\*\*([\s\S]*?)(?=\*\*Do NOT|$)/i);
    if (useMatch) {
      result.use = extractBulletPoints(useMatch[1]);
    } else {
      result.use = extractBulletPoints(useSection);
    }
  }

  // Extract "When NOT to Use" or "Do NOT use" section
  const avoidMatch = content.match(/\*\*Do NOT use.*?when:\*\*([\s\S]*?)(?=##|$)/i);
  if (avoidMatch) {
    result.avoid = extractBulletPoints(avoidMatch[1]);
  }

  return result;
}

/**
 * Extract bullet points from text
 */
function extractBulletPoints(text) {
  const points = [];
  const lines = text.split('\n');

  for (const line of lines) {
    const match = line.match(/^-\s+(.+)$/);
    if (match) {
      points.push(match[1].trim());
    }
  }

  return points;
}

/**
 * Extract workflow/phases from the document
 */
function extractWorkflow(content) {
  const workflow = [];

  // Look for Phase sections
  const phasePattern = /###\s*Phase\s*(\d+):\s*(.+)/g;
  let match;

  while ((match = phasePattern.exec(content)) !== null) {
    const phaseNum = parseInt(match[1], 10);
    const phaseName = match[2].trim();

    // Extract phase content
    const phaseStart = match.index;
    const nextPhaseMatch = content.slice(phaseStart + match[0].length).match(/###\s*Phase\s*\d+:/);
    const phaseEnd = nextPhaseMatch
      ? phaseStart + match[0].length + nextPhaseMatch.index
      : content.length;

    const phaseContent = content.slice(phaseStart, phaseEnd);

    // Extract objective
    const objectiveMatch = phaseContent.match(/\*\*Objective:\*\*\s*(.+)/);

    // Extract activities
    const activitiesSection = extractSection(phaseContent, /\*\*Activities:\*\*/i);
    const activities = activitiesSection ? extractBulletPoints(activitiesSection) : [];

    // Extract artifacts
    const artifactsSection = extractSection(phaseContent, /\*\*Artifacts:\*\*/i);
    const artifacts = artifactsSection ? extractBulletPoints(artifactsSection) : [];

    workflow.push({
      phase: phaseNum,
      name: phaseName,
      objective: objectiveMatch ? objectiveMatch[1].trim() : null,
      activities,
      artifacts
    });
  }

  return workflow;
}

/**
 * Extract implementation steps
 */
function extractImplementationSteps(content) {
  const steps = {};

  // Look for "For Human Contributors", "For AI Agents", etc.
  const rolePatterns = [
    { pattern: /###\s*For Human Contributors/i, key: 'human' },
    { pattern: /###\s*For AI Agents/i, key: 'ai_agent' },
    { pattern: /###\s*For Agent Orchestrator/i, key: 'orchestrator' }
  ];

  for (const { pattern, key } of rolePatterns) {
    const section = extractSection(content, pattern);
    if (section) {
      steps[key] = extractBulletPoints(section);
    }
  }

  return steps;
}

/**
 * Extract references section
 */
function extractReferences(content) {
  const section = extractSection(content, /^##\s*References/i);
  if (!section) return [];

  const references = [];
  const lines = section.split('\n');

  for (const line of lines) {
    // Match "- ADR-XXX — Description" or "- Directive NNN" patterns
    const match = line.match(/^-\s+(?:\[([^\]]+)\]\([^)]+\)|([^–—]+))\s*[–—]\s*(.+)$/);
    if (match) {
      references.push({
        name: (match[1] || match[2]).trim(),
        description: match[3].trim()
      });
    } else {
      const simpleMatch = line.match(/^-\s+(.+)$/);
      if (simpleMatch) {
        references.push({ name: simpleMatch[1].trim() });
      }
    }
  }

  return references;
}

/**
 * Extract troubleshooting section
 */
function extractTroubleshooting(content) {
  const section = extractSection(content, /^##\s*Troubleshooting/i);
  if (!section) return [];

  const issues = [];

  // Look for ### Symptom/Issue subheadings or table rows
  const issuePattern = /###\s*(.+?)(?=###|$)/gs;
  let match;

  while ((match = issuePattern.exec(section)) !== null) {
    const issueContent = match[1];
    const titleMatch = issueContent.match(/^(.+)/);

    if (titleMatch) {
      const symptomMatch = issueContent.match(/\*\*Symptoms?:\*\*\s*(.+)/i);
      const causeMatch = issueContent.match(/\*\*(?:Likely )?Causes?:\*\*\s*([\s\S]*?)(?=\*\*Solutions?|$)/i);
      const solutionMatch = issueContent.match(/\*\*Solutions?:\*\*\s*([\s\S]*?)$/i);

      issues.push({
        title: titleMatch[1].trim(),
        symptoms: symptomMatch ? symptomMatch[1].trim() : null,
        causes: causeMatch ? extractBulletPoints(causeMatch[1]) : [],
        solutions: solutionMatch ? extractBulletPoints(solutionMatch[1]) : []
      });
    }
  }

  return issues;
}

/**
 * Format filename to readable title
 */
function formatTitle(filename) {
  return filename
    .replace(/[-_]/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase());
}

/**
 * Generate Claude Code skill format from parsed approach
 *
 * @param {Object} approach - Parsed approach
 * @returns {Object} Claude Code skill definition
 */
function generateClaudeCodeSkill(approach) {
  return {
    skill_version: '1.0',
    skill: {
      id: approach.id,
      name: approach.title,
      description: summarizeOverview(approach.content.overview),
      type: 'approach',
      category: approach.metadata.type.toLowerCase().replace(/\s+/g, '-'),
      invoke: `/approach-${approach.id}`,
      principles: approach.content.principles.map(p => p.title || p.description).slice(0, 5),
      when_to_use: approach.content.when_to_use.slice(0, 5),
      when_not_to_use: approach.content.when_not_to_use.slice(0, 3),
      workflow_phases: approach.content.workflow.map(w => ({
        phase: w.phase,
        name: w.name,
        objective: w.objective
      })),
      references: approach.content.references.map(r => r.name)
    },
    instructions: approach.content.overview,
    full_content_url: approach.file_metadata.file_path,
    metadata: {
      version: approach.metadata.version,
      status: approach.metadata.status,
      source_hash: approach.file_metadata.source_hash,
      exported_at: new Date().toISOString(),
      exporter_version: EXPORTER_VERSION
    }
  };
}

/**
 * Generate GitHub Copilot skill format from parsed approach
 *
 * @param {Object} approach - Parsed approach
 * @returns {Object} Copilot skill definition
 */
function generateCopilotSkill(approach) {
  return {
    $schema: 'https://aka.ms/copilot-skill-schema',
    name: `approach-${approach.id}`,
    description: summarizeOverview(approach.content.overview),
    capabilities: [
      approach.metadata.type.toLowerCase().replace(/\s+/g, '-'),
      'operational-guide',
      ...approach.content.principles.slice(0, 2).map(p =>
        (p.title || '').toLowerCase().replace(/\s+/g, '-')
      )
    ].filter(Boolean),
    instructions: buildCopilotInstructions(approach),
    conversation_starters: generateApproachStarters(approach),
    workspace: {
      settings: {}
    },
    extensions: {
      agentic_framework: {
        type: approach.metadata.type,
        version: approach.metadata.version,
        principles: approach.content.principles.map(p => p.title || p.description),
        workflow_phases: approach.content.workflow.length,
        references: approach.content.references.map(r => r.name)
      }
    }
  };
}

/**
 * Generate OpenCode skill format from parsed approach
 *
 * @param {Object} approach - Parsed approach
 * @returns {Object} OpenCode skill definition
 */
function generateOpenCodeSkill(approach) {
  return {
    opencode_version: '1.0',
    skill: {
      id: approach.id,
      name: approach.title,
      version: approach.metadata.version,
      description: summarizeOverview(approach.content.overview),
      type: 'approach',
      category: approach.metadata.type,
      status: approach.metadata.status,
      invoke_pattern: `/approach ${approach.id}`,
      principles: approach.content.principles,
      applicability: {
        when_to_use: approach.content.when_to_use,
        when_not_to_use: approach.content.when_not_to_use
      },
      workflow: approach.content.workflow,
      implementation: approach.content.implementation_steps,
      references: approach.content.references,
      troubleshooting: approach.content.troubleshooting,
      profile_url: approach.file_metadata.file_path
    },
    metadata: {
      last_updated: approach.metadata.last_updated,
      source_hash: approach.file_metadata.source_hash,
      word_count: approach.file_metadata.word_count,
      exported_at: new Date().toISOString(),
      exporter_version: EXPORTER_VERSION
    }
  };
}

/**
 * Summarize overview to first 200 chars
 */
function summarizeOverview(overview) {
  if (!overview) return '';
  const clean = overview.replace(/\n/g, ' ').trim();
  return clean.length > 200 ? clean.slice(0, 197) + '...' : clean;
}

/**
 * Build Copilot instructions from approach content
 */
function buildCopilotInstructions(approach) {
  let instructions = approach.content.overview + '\n\n';

  if (approach.content.principles.length > 0) {
    instructions += '## Core Principles\n\n';
    approach.content.principles.forEach((p, i) => {
      instructions += `${i + 1}. **${p.title || 'Principle'}**: ${p.description || ''}\n`;
    });
    instructions += '\n';
  }

  if (approach.content.when_to_use.length > 0) {
    instructions += '## When to Use\n\n';
    approach.content.when_to_use.forEach(item => {
      instructions += `- ${item}\n`;
    });
    instructions += '\n';
  }

  return instructions.trim();
}

/**
 * Generate conversation starters for approach
 */
function generateApproachStarters(approach) {
  const starters = [];
  const title = approach.title.toLowerCase();

  if (title.includes('decision') || title.includes('adr')) {
    starters.push(
      'Help me document an architectural decision',
      'What\'s the best way to capture design rationale?'
    );
  } else if (title.includes('orchestration') || title.includes('coordination')) {
    starters.push(
      'How do I set up task-based agent coordination?',
      'Explain the file-based orchestration workflow'
    );
  } else if (title.includes('test') || title.includes('tdd')) {
    starters.push(
      'Guide me through test-driven development',
      'How should I structure my tests?'
    );
  } else if (title.includes('trunk') || title.includes('development')) {
    starters.push(
      'How do I follow trunk-based development?',
      'Best practices for avoiding merge conflicts'
    );
  }

  // Generic starters
  starters.push(
    `Explain the ${approach.title} approach`,
    `When should I use ${approach.title}?`
  );

  return starters.slice(0, 4);
}

/**
 * Parse all approaches in a directory
 *
 * @param {string} directory - Path to approaches directory
 * @returns {Promise<Array>} Array of parsed approaches
 */
async function parseApproachDirectory(directory) {
  const files = await fs.readdir(directory);
  const mdFiles = files.filter(f => f.endsWith('.md') && f.toLowerCase() !== 'readme.md');

  const approaches = [];
  for (const file of mdFiles) {
    try {
      const approach = await parseApproach(path.join(directory, file));
      if (approach) {
        approaches.push(approach);
      }
    } catch (error) {
      console.error(`Warning: Failed to parse ${file}: ${error.message}`);
    }
  }

  return approaches;
}

/**
 * Export all approaches to skill formats
 *
 * @param {string} inputDir - Directory containing approach .md files
 * @param {string} outputDir - Output directory for generated files
 * @returns {Promise<Object>} Export results
 */
async function exportApproaches(inputDir, outputDir) {
  const approaches = await parseApproachDirectory(inputDir);

  // Create output directories
  const claudeDir = path.join(outputDir, 'claude-code');
  const copilotDir = path.join(outputDir, 'copilot');
  const opencodeDir = path.join(outputDir, 'opencode');

  await fs.mkdir(claudeDir, { recursive: true });
  await fs.mkdir(copilotDir, { recursive: true });
  await fs.mkdir(opencodeDir, { recursive: true });

  const results = {
    total: approaches.length,
    exported: [],
    errors: []
  };

  for (const approach of approaches) {
    try {
      // Generate Claude Code skill
      const claudeSkill = generateClaudeCodeSkill(approach);
      const claudePath = path.join(claudeDir, `${approach.id}.approach.json`);
      await fs.writeFile(claudePath, JSON.stringify(claudeSkill, null, 2));

      // Generate Copilot skill
      const copilotSkill = generateCopilotSkill(approach);
      const copilotPath = path.join(copilotDir, `${approach.id}.copilot-approach.json`);
      await fs.writeFile(copilotPath, JSON.stringify(copilotSkill, null, 2));

      // Generate OpenCode skill
      const opencodeSkill = generateOpenCodeSkill(approach);
      const opencodePath = path.join(opencodeDir, `${approach.id}.opencode-approach.json`);
      await fs.writeFile(opencodePath, JSON.stringify(opencodeSkill, null, 2));

      results.exported.push({
        id: approach.id,
        title: approach.title,
        files: {
          claude: claudePath,
          copilot: copilotPath,
          opencode: opencodePath
        }
      });
    } catch (error) {
      results.errors.push({
        id: approach.id,
        error: error.message
      });
    }
  }

  // Generate manifest
  const manifest = {
    manifest_version: '1.0',
    type: 'approaches',
    generated_at: new Date().toISOString(),
    exporter_version: EXPORTER_VERSION,
    skills: results.exported.map(e => ({
      id: e.id,
      title: e.title,
      formats: ['claude-code', 'copilot', 'opencode']
    })),
    total_skills: results.exported.length
  };

  await fs.writeFile(
    path.join(outputDir, 'approach-skills-manifest.json'),
    JSON.stringify(manifest, null, 2)
  );

  return results;
}

module.exports = {
  parseApproach,
  parseApproachDirectory,
  generateClaudeCodeSkill,
  generateCopilotSkill,
  generateOpenCodeSkill,
  exportApproaches,
  ApproachParseError
};
