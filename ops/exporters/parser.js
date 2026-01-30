/**
 * Markdown Parser for Agent Files
 * 
 * Parses .agent.md files and produces Intermediate Representation (IR) instances
 * following the schema defined in docs/technical/ir-structure.md
 * 
 * @module parser
 * @version 1.0.0
 * 
 * Following Directives:
 * - 016 (ATDD): Acceptance tests written first
 * - 017 (TDD): Unit tests with Red-Green-Refactor
 * - 018 (Documentation): JSDoc for all public functions
 */

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');
const yaml = require('js-yaml');
const matter = require('gray-matter');

const PARSER_VERSION = '1.0.0';
const IR_VERSION = '1.0.0';

/**
 * Custom error class for parsing errors
 */
class ParseError extends Error {
  constructor(message, filePath, cause) {
    super(message);
    this.name = 'ParseError';
    this.filePath = filePath;
    this.cause = cause;
  }
}

/**
 * Parse YAML frontmatter from markdown content
 * 
 * @param {string} content - Raw markdown content
 * @param {string} filePath - File path for error messages
 * @returns {Object} Parsed frontmatter object
 * @throws {ParseError} On invalid YAML or missing frontmatter
 */
function parseYAMLFrontmatter(content, filePath) {
  try {
    const parsed = matter(content);
    
    if (!parsed.data || Object.keys(parsed.data).length === 0) {
      throw new ParseError(
        `No frontmatter found in ${filePath}\n   Expected YAML frontmatter between --- delimiters`,
        filePath
      );
    }
    
    return parsed.data;
  } catch (error) {
    if (error instanceof ParseError) {
      throw error;
    }
    throw new ParseError(
      `Invalid YAML in ${filePath}\n   → ${error.message}`,
      filePath,
      error
    );
  }
}

/**
 * Extract a markdown section by heading pattern
 * 
 * @param {string} content - Full markdown content
 * @param {RegExp} headingPattern - Regex pattern to match heading
 * @returns {string|null} Section content or null if not found
 */
function extractSection(content, headingPattern) {
  const lines = content.split('\n');
  let inSection = false;
  let sectionLines = [];
  let sectionLevel = null;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // Check if this is the start of our target section
    if (headingPattern.test(line)) {
      inSection = true;
      // Determine heading level
      const match = line.match(/^(#{1,6})\s/);
      sectionLevel = match ? match[1].length : null;
      continue; // Skip the heading line itself
    }
    
    // If we're in the section
    if (inSection) {
      // Check if we've hit another heading of same or higher level
      const headingMatch = line.match(/^(#{1,6})\s/);
      if (headingMatch) {
        const currentLevel = headingMatch[1].length;
        // If same or higher level (lower number), we're done with this section
        if (currentLevel <= sectionLevel) {
          break;
        }
      }
      
      sectionLines.push(line);
    }
  }
  
  if (sectionLines.length === 0) {
    return null;
  }
  
  // Join and trim
  return sectionLines.join('\n').trim();
}

/**
 * Extract content sections from markdown
 * 
 * @param {string} content - Full markdown content
 * @returns {Object} Content sections
 */
function extractContentSections(content) {
  // Extract main content sections
  const purpose = extractSection(content, /^##\s+2\.\s+Purpose/i);
  const specialization = extractSection(content, /^##\s+3\.\s+Specialization/i);
  const collaborationContract = extractSection(content, /^##\s+4\.\s+Collaboration\s+Contract/i);
  
  // Extract success criteria - it's often within the specialization section or collaboration
  let successCriteria = null;
  if (specialization) {
    const match = specialization.match(/\*\*Success means:\*\*\s+(.+?)(?=\n|$)/i);
    if (match) {
      successCriteria = match[1].trim();
    }
  }
  
  // Extract output artifacts - often a subsection
  const outputArtifacts = extractSection(content, /^###\s+Output\s+Artifacts/i);
  const operatingProcedure = extractSection(content, /^###\s+Operating\s+Procedure/i);
  
  // Extract mode defaults table
  const modeDefaults = extractModeDefaults(content);
  
  return {
    purpose,
    specialization,
    collaboration_contract: collaborationContract,
    success_criteria: successCriteria,
    output_artifacts: outputArtifacts,
    operating_procedure: operatingProcedure,
    mode_defaults: modeDefaults
  };
}

/**
 * Parse mode defaults table from markdown
 * 
 * @param {string} content - Full markdown content
 * @returns {Array} Array of mode objects
 */
function extractModeDefaults(content) {
  const modeSection = extractSection(content, /^##\s+5\.\s+Mode\s+Defaults/i);
  if (!modeSection) {
    return [];
  }
  
  const modes = [];
  const lines = modeSection.split('\n');
  
  // Find table rows (skip header and separator)
  let inTable = false;
  for (const line of lines) {
    // Table separator line
    if (/^\|[\s\-:|]+\|$/.test(line)) {
      inTable = true;
      continue;
    }
    
    if (inTable && line.startsWith('|')) {
      const cells = line.split('|').map(c => c.trim()).filter(c => c);
      if (cells.length >= 3) {
        modes.push({
          mode: cells[0].trim(),
          description: cells[1].trim(),
          use_case: cells[2].trim()
        });
      }
    }
  }
  
  return modes;
}

/**
 * Extract directive references from markdown table
 * 
 * @param {string} content - Full markdown content
 * @returns {Array} Array of directive objects
 */
function extractDirectives(content) {
  // Find the Directive References section
  const directiveSection = extractSection(content, /^##\s+Directive\s+References/i);
  if (!directiveSection) {
    return [];
  }
  
  const directives = [];
  const lines = directiveSection.split('\n');
  
  let inTable = false;
  for (const line of lines) {
    // Table separator line
    if (/^\|[\s\-:|]+\|$/.test(line)) {
      inTable = true;
      continue;
    }
    
    if (inTable && line.startsWith('|')) {
      const cells = line.split('|').map(c => c.trim()).filter(c => c);
      if (cells.length >= 3) {
        const code = parseInt(cells[0]);
        if (!isNaN(code)) {
          directives.push({
            code: code,
            code_formatted: String(code).padStart(3, '0'),
            title: cells[1].replace(/\[(.+?)\]\(.+?\)/g, '$1').trim(), // Remove markdown links
            rationale: cells[2].trim(),
            required: false // Will be determined in governance section
          });
        }
      }
    }
  }
  
  // Also check for directives mentioned in "Test-First Requirement" or "Primer Requirement" sections
  // These are often 016 (ATDD) and 017 (TDD)
  // Look for patterns like: "Follow Directives 016 (ATDD) and 017 (TDD)"
  const testFirstMatch = content.match(/Follow\s+Directives?\s+(\d+)\s*\([^)]+\)\s+and\s+(\d+)\s*\([^)]+\)/i);
  if (testFirstMatch) {
    const codes = [parseInt(testFirstMatch[1]), parseInt(testFirstMatch[2])];
    codes.forEach(code => {
      if (!directives.find(d => d.code === code)) {
        // Extract the title from the parentheses
        const titleMatch = content.match(new RegExp(`Directives?\\s+${code}\\s*\\(([^)]+)\\)`, 'i'));
        const title = titleMatch ? titleMatch[1] : (code === 16 ? 'ATDD' : code === 17 ? 'TDD' : '');
        
        directives.push({
          code: code,
          code_formatted: String(code).padStart(3, '0'),
          title: title,
          rationale: `Follow Directives ${code} (${title}) whenever authoring or modifying executable code`,
          required: true
        });
      }
    });
  }
  
  return directives;
}

/**
 * Extract context sources from markdown
 * 
 * @param {string} content - Full markdown content
 * @returns {Array} Array of context source objects
 */
function extractContextSources(content) {
  const contextSection = extractSection(content, /^##\s+1\.\s+Context\s+Sources/i);
  if (!contextSection) {
    return [];
  }
  
  const sources = [];
  const lines = contextSection.split('\n');
  
  for (const line of lines) {
    // Match bullet points like: - **Type:** path
    const match = line.match(/^[-*]\s+\*\*(.+?):\*\*\s+(.+?)$/);
    if (match) {
      sources.push({
        type: match[1].trim(),
        location: match[2].trim()
      });
    }
  }
  
  return sources;
}

/**
 * Extract governance information
 * 
 * @param {string} content - Full markdown content
 * @param {Array} directives - Parsed directives
 * @returns {Object} Governance object
 */
function extractGovernance(content, directives) {
  const governance = {
    directive_requirements: {
      required: [],
      optional: []
    },
    uncertainty_threshold: null,
    escalation_rules: [],
    safety_criticality: null,
    primer_required: false,
    test_first_required: false
  };
  
  // Check for primer requirement
  if (/Primer\s+Requirement:/i.test(content)) {
    governance.primer_required = true;
  }
  
  // Check for test-first requirement
  if (/Test-First\s+Requirement:/i.test(content) || 
      /Follow\s+Directives?\s+016.*(?:ATDD|TDD)/i.test(content)) {
    governance.test_first_required = true;
  }
  
  // Extract uncertainty threshold
  const uncertaintyMatch = content.match(/uncertainty\s*[><=]+\s*(\d+%)/i);
  if (uncertaintyMatch) {
    governance.uncertainty_threshold = `>${uncertaintyMatch[1].replace('%', '')}%`;
  }
  
  // Extract escalation rules from collaboration contract
  const collabSection = extractSection(content, /^##\s+4\.\s+Collaboration\s+Contract/i);
  if (collabSection) {
    const rules = [];
    const lines = collabSection.split('\n');
    for (const line of lines) {
      if (/escalate|help when stuck|clarifying questions/i.test(line)) {
        const cleaned = line.replace(/^[-*]\s+/, '').trim();
        if (cleaned) {
          rules.push(cleaned);
        }
      }
    }
    governance.escalation_rules = rules;
  }
  
  // Categorize directives as required/optional
  // Check if directive 16 or 17 is mentioned (TDD/ATDD)
  directives.forEach(d => {
    if (d.code === 16 || d.code === 17) {
      governance.directive_requirements.required.push(d.code);
      d.required = true;
    } else {
      governance.directive_requirements.optional.push(d.code);
    }
  });
  
  // Set safety criticality based on content
  if (/safety|critical|production/i.test(content)) {
    governance.safety_criticality = 'medium';
  }
  
  return governance;
}

/**
 * Parse an agent markdown file into Intermediate Representation
 * 
 * @param {string} filePath - Path to .agent.md file
 * @returns {Promise<AgentIR>} Parsed IR object
 * @throws {ParseError} On invalid file structure
 */
async function parseAgentFile(filePath) {
  try {
    // Read file content
    const content = await fs.readFile(filePath, 'utf-8');
    
    // Parse frontmatter
    const frontmatter = parseYAMLFrontmatter(content, filePath);
    validateRequiredFields(frontmatter, filePath);
    
    // Apply defaults
    if (!frontmatter.version) {
      frontmatter.version = '1.0.0';
    }
    
    // Extract content sections
    const contentSections = extractContentSections(content);
    
    // Parse relationships
    const directives = extractDirectives(content);
    const contextSources = extractContextSources(content);
    
    const relationships = {
      directives,
      context_sources: contextSources,
      agent_references: [] // TODO: Extract agent references
    };
    
    // Extract governance
    const governance = extractGovernance(content, directives);
    
    // Generate metadata
    const stats = await fs.stat(filePath);
    const fileContent = await fs.readFile(filePath);
    const hash = crypto.createHash('sha256').update(fileContent).digest('hex');
    const relativePath = path.relative(process.cwd(), filePath);
    
    const metadata = {
      file_path: relativePath.replace(/\\/g, '/'),
      source_hash: hash,
      parsed_at: new Date().toISOString().replace(/\.\d{3}/, ''),
      file_size: stats.size,
      parser_version: PARSER_VERSION
    };
    
    // Assemble IR
    const ir = {
      ir_version: IR_VERSION,
      frontmatter,
      content: contentSections,
      relationships,
      governance,
      metadata
    };
    
    return ir;
  } catch (error) {
    if (error instanceof ParseError) {
      throw error;
    }
    throw new ParseError(
      `Failed to parse ${filePath}: ${error.message}`,
      filePath,
      error
    );
  }
}

/**
 * Validate required frontmatter fields
 * 
 * @param {Object} frontmatter - Parsed frontmatter
 * @param {string} filePath - File path for error messages
 * @throws {ParseError} If required fields are missing
 */
function validateRequiredFields(frontmatter, filePath) {
  const required = ['name', 'description', 'tools'];
  const missing = required.filter(field => !frontmatter[field]);
  
  if (missing.length > 0) {
    throw new ParseError(
      `Missing required field${missing.length > 1 ? 's' : ''} '${missing.join("', '")}' in ${filePath}\n   → Add to frontmatter`,
      filePath
    );
  }
  
  // Validate tools is an array
  if (!Array.isArray(frontmatter.tools)) {
    throw new ParseError(
      `Field 'tools' must be an array in ${filePath}`,
      filePath
    );
  }
}

/**
 * Parse all agent files in a directory
 * 
 * @param {string} dirPath - Directory containing .agent.md files
 * @returns {Promise<AgentIR[]>} Array of IR objects
 */
async function parseAgentDirectory(dirPath) {
  const files = await fs.readdir(dirPath);
  const agentFiles = files.filter(f => f.endsWith('.agent.md'));
  
  const results = [];
  for (const file of agentFiles) {
    const filePath = path.join(dirPath, file);
    try {
      const ir = await parseAgentFile(filePath);
      results.push(ir);
    } catch (error) {
      console.error(`Warning: Failed to parse ${file}:`, error.message);
      // Continue parsing other files
    }
  }
  
  return results;
}

module.exports = {
  parseAgentFile,
  parseAgentDirectory
};
