/**
 * GitHub Copilot Skills Generator
 * 
 * Generates GitHub Copilot Skills format JSON files from Agent IR.
 * This is the SECOND major export format (GitHub Copilot ecosystem integration).
 * 
 * @module copilot-generator
 * @version 1.0.0
 * 
 * Following Directives:
 * - 016 (ATDD): Acceptance tests written first
 * - 017 (TDD): Unit tests with Red-Green-Refactor
 * - 018 (Documentation): JSDoc for all public functions
 */

const fs = require('fs').promises;
const path = require('path');

const COPILOT_SCHEMA = 'https://aka.ms/copilot-skill-schema';

/**
 * Tool to VS Code extension ID mapping
 * Maps agent tools to their corresponding VS Code extension IDs
 */
const TOOL_EXTENSION_MAP = {
  'plantuml': 'jebbs.plantuml',
  'mermaid': 'bierner.markdown-mermaid',
  'markdown-linter': 'DavidAnson.vscode-markdownlint',
  'bash': 'timonwong.shellcheck',
  'Docker': 'ms-azuretools.vscode-docker',
  'Java': 'vscjava.vscode-java-pack',
  'Python': 'ms-python.python',
  'JavaScript': 'dbaeumer.vscode-eslint',
  'TypeScript': 'ms-vscode.vscode-typescript-next',
  'edit': 'ms-vscode.vscode-language-server-protocol',
  'search': 'ms-vscode.search-result',
  'MultiEdit': 'dbaeumer.vscode-eslint'
};

/**
 * Role-based conversation starters
 * Provides contextual conversation starters based on agent role
 */
const ROLE_STARTERS = {
  'architect': [
    'Help me design a scalable architecture for this system',
    'Review this architectural decision and suggest improvements',
    'Create a technical design document for a new feature',
    'Evaluate trade-offs between different architectural patterns',
    'Document this system design with ADRs'
  ],
  'backend': [
    'Help me design a RESTful API for this service',
    'Review this backend architecture for performance',
    'Design a database schema for these requirements',
    'Help me implement clean service boundaries',
    'Suggest improvements for this API design'
  ],
  'reviewer': [
    'Review this code for quality and maintainability',
    'Check this pull request for potential issues',
    'Suggest improvements for code clarity',
    'Evaluate test coverage for this module',
    'Review this architecture for best practices'
  ],
  'frontend': [
    'Help me design a user interface component',
    'Review this React component for best practices',
    'Suggest accessibility improvements',
    'Design a responsive layout for this feature',
    'Help me implement state management'
  ],
  'tester': [
    'Help me write unit tests for this function',
    'Design test cases for this feature',
    'Review this test suite for completeness',
    'Suggest edge cases to test',
    'Help me implement integration tests'
  ],
  'documentation': [
    'Help me write documentation for this API',
    'Review this README for clarity',
    'Create a user guide for this feature',
    'Document this system architecture',
    'Improve this technical documentation'
  ],
  'generic': [
    'Help me with this task',
    'Review my approach to this problem',
    'Suggest improvements for this solution',
    'Explain this concept to me',
    'Guide me through this workflow'
  ]
};

/**
 * Extract capabilities from IR content
 * Capabilities are derived from specialization, purpose, and tools
 * 
 * @param {Object} ir - Agent Intermediate Representation
 * @returns {Array<string>} Array of capability keywords
 */
function extractCapabilities(ir) {
  const capabilities = new Set();
  
  // Extract from tools
  const toolCapabilityMap = {
    'plantuml': 'diagramming',
    'mermaid': 'diagramming',
    'Docker': 'containerization',
    'Java': 'backend-development',
    'Python': 'scripting',
    'Bash': 'automation',
    'markdown-linter': 'validation',
    'report_progress': 'workflow'
  };
  
  if (ir.frontmatter.tools) {
    ir.frontmatter.tools.forEach(tool => {
      if (toolCapabilityMap[tool]) {
        capabilities.add(toolCapabilityMap[tool]);
      }
    });
  }
  
  // Extract from content
  const content = [
    ir.content.purpose || '',
    ir.content.specialization || '',
    ir.content.success_criteria || ''
  ].join(' ').toLowerCase();
  
  // Only extract if substantial content exists
  if (content.length < 30) {
    return Array.from(capabilities);
  }
  
  // Capability keywords mapping
  const capabilityKeywords = {
    'architecture': 'architecture',
    'architectural': 'architecture',
    'design': 'design',
    'adr': 'decision-records',
    'testing': 'testing',
    'review': 'code-review',
    'backend': 'backend-development',
    'api': 'api-design',
    'database': 'data-persistence',
    'documentation': 'documentation',
    'governance': 'governance',
    'workflow': 'workflow-management',
    'bootstrap': 'initialization',
    'security': 'security',
    'performance': 'performance-optimization'
  };
  
  Object.entries(capabilityKeywords).forEach(([keyword, capability]) => {
    const regex = new RegExp(`\\b${keyword}\\b`, 'i');
    if (regex.test(content)) {
      capabilities.add(capability);
    }
  });
  
  return Array.from(capabilities);
}

/**
 * Infer agent role from name and content
 * Used to determine appropriate conversation starters
 * 
 * @param {Object} ir - Agent Intermediate Representation
 * @returns {string} Role identifier (architect, backend, reviewer, etc.)
 */
function inferRole(ir) {
  const name = ir.frontmatter.name.toLowerCase();
  const content = [
    ir.content.purpose || '',
    ir.content.specialization || ''
  ].join(' ').toLowerCase();
  
  const hasSubstantialContent = content.length > 30;
  
  // Check name-based role mapping first
  if (name.includes('architect')) return 'architect';
  if (name.includes('backend') || name.includes('backend-dev')) return 'backend';
  if (name.includes('review')) return 'reviewer';
  if (name.includes('frontend') || name.includes('ui')) return 'frontend';
  if (name.includes('test') || name.includes('qa')) return 'tester';
  if (name.includes('doc') || name.includes('scribe')) return 'documentation';
  
  // Check content-based role
  if (hasSubstantialContent) {
    if (/\barchitecture\b/i.test(content)) return 'architect';
    if (/\bbackend\b/i.test(content)) return 'backend';
    if (/\breview\b/i.test(content)) return 'reviewer';
    if (/\bfrontend\b/i.test(content)) return 'frontend';
    if (/\btest\b/i.test(content)) return 'tester';
    if (/\bdocumentation\b/i.test(content)) return 'documentation';
  }
  
  return 'generic';
}

/**
 * Generate conversation starters based on agent role and capabilities
 * 
 * @param {Object} ir - Agent Intermediate Representation
 * @returns {Array<string>} Array of conversation starter strings
 */
function generateConversationStarters(ir) {
  const role = inferRole(ir);
  const starters = ROLE_STARTERS[role] || ROLE_STARTERS.generic;
  
  // Return a subset of starters (3-5) to keep it focused
  return starters.slice(0, Math.min(5, starters.length));
}

/**
 * Map tools to VS Code extension IDs
 * 
 * @param {Array<string>} tools - Array of tool names from IR
 * @returns {Array<string>} Array of VS Code extension IDs
 */
function mapToolsToExtensions(tools) {
  const extensions = new Set();
  
  // Always include these base extensions for agents
  extensions.add('GitHub.copilot');
  extensions.add('GitHub.copilot-chat');
  
  // Map tools to extensions
  if (tools && Array.isArray(tools)) {
    tools.forEach(tool => {
      if (TOOL_EXTENSION_MAP[tool]) {
        extensions.add(TOOL_EXTENSION_MAP[tool]);
      }
    });
  }
  
  return Array.from(extensions);
}

/**
 * Generate workspace settings for agent
 * 
 * @param {Object} ir - Agent Intermediate Representation
 * @returns {Object} VS Code workspace settings
 */
function generateWorkspaceSettings(ir) {
  const settings = {
    'editor.formatOnSave': true,
    'editor.codeActionsOnSave': {
      'source.fixAll': true
    },
    'files.autoSave': 'onFocusChange'
  };
  
  // Add role-specific settings
  const role = inferRole(ir);
  
  if (role === 'backend' || role === 'architect') {
    settings['editor.rulers'] = [80, 120];
  }
  
  if (role === 'documentation' || role === 'scribe') {
    settings['markdown.preview.breaks'] = true;
    settings['markdown.preview.linkify'] = true;
  }
  
  return settings;
}

/**
 * Format instructions from IR content
 * Combines purpose, specialization, and key directives into instructions
 * 
 * @param {Object} ir - Agent Intermediate Representation
 * @returns {string} Formatted instructions text
 */
function formatInstructions(ir) {
  const parts = [];
  
  // Add purpose
  if (ir.content.purpose) {
    parts.push(ir.content.purpose);
  }
  
  // Add specialization
  if (ir.content.specialization) {
    parts.push('\n\n## Specialization\n\n' + ir.content.specialization);
  }
  
  // Add collaboration contract if present
  if (ir.content.collaboration_contract) {
    parts.push('\n\n## Collaboration Guidelines\n\n' + ir.content.collaboration_contract);
  }
  
  // Add key directives
  if (ir.relationships.directives && ir.relationships.directives.length > 0) {
    const directiveList = ir.relationships.directives
      .filter(d => d.required)
      .map(d => `- **${d.code_formatted}**: ${d.title}`)
      .join('\n');
    
    if (directiveList) {
      parts.push('\n\n## Required Directives\n\n' + directiveList);
    }
  }
  
  // Fallback for minimal content
  if (parts.length === 0) {
    return `You are ${ir.frontmatter.name}, an AI agent specialized in ${ir.frontmatter.description}`;
  }
  
  return parts.join('\n');
}

/**
 * Extract governance metadata from IR
 * Similar to OpenCode generator but adapted for Copilot format
 * 
 * @param {Object} ir - Agent Intermediate Representation
 * @returns {Object} Governance extensions object
 */
function extractGovernanceMetadata(ir) {
  // Determine priority level
  let priorityLevel = 'medium';
  if (ir.content.specialization) {
    const spec = ir.content.specialization.toLowerCase();
    if (spec.includes('critical') || spec.includes('production') || spec.includes('primary')) {
      priorityLevel = 'high';
    } else if (spec.includes('secondary') || spec.includes('optional')) {
      priorityLevel = 'low';
    }
  }
  
  // Format directives
  const directivesWithFlags = ir.relationships.directives.map(d => ({
    code: d.code_formatted,
    title: d.title,
    required: d.required,
    rationale: d.rationale
  }));
  
  // Determine orchestration capability
  const content = [
    ir.content.purpose || '',
    ir.content.specialization || '',
    ir.content.collaboration_contract || ''
  ].join(' ').toLowerCase();
  
  const orchestrationCapable = content.includes('orchestrat') || 
                                content.includes('coordinat') || 
                                content.includes('workflow') ||
                                (content.includes('manage') && content.includes('agent'));
  
  return {
    saboteurs_governance: {
      directives: directivesWithFlags,
      priority_level: priorityLevel,
      uncertainty_threshold: ir.governance.uncertainty_threshold || 'not specified',
      escalation_required: ir.governance.escalation_rules.length > 0,
      primer_required: ir.governance.primer_required,
      test_first_required: ir.governance.test_first_required,
      safety_criticality: ir.governance.safety_criticality
    },
    multi_agent: {
      orchestration_capable: orchestrationCapable,
      handoff_protocols: ['file-based'],
      specialization_boundaries: ir.content.specialization ? 'explicit' : 'flexible'
    }
  };
}

/**
 * Map IR to Copilot Skill structure
 * 
 * @param {Object} ir - Agent Intermediate Representation
 * @returns {Object} Copilot Skill structure
 */
function mapIRToCopilotSkill(ir) {
  const capabilities = extractCapabilities(ir);
  const conversationStarters = generateConversationStarters(ir);
  const extensions = mapToolsToExtensions(ir.frontmatter.tools);
  const settings = generateWorkspaceSettings(ir);
  const instructions = formatInstructions(ir);
  const governance = extractGovernanceMetadata(ir);
  
  return {
    $schema: COPILOT_SCHEMA,
    name: ir.frontmatter.name,
    description: ir.frontmatter.description,
    capabilities: capabilities,
    instructions: instructions,
    conversation_starters: conversationStarters,
    workspace: {
      extensions: extensions,
      settings: settings
    },
    extensions: governance
  };
}

/**
 * Generate Copilot Skill file from Agent IR
 * 
 * @param {Object} ir - Parsed agent IR
 * @param {string} outputDir - Directory where to write file
 * @returns {Promise<string>} Path to generated file
 */
async function generateCopilotSkill(ir, outputDir) {
  // Ensure output directory exists
  await fs.mkdir(outputDir, { recursive: true });
  
  const agentId = ir.frontmatter.name;
  
  // Generate Copilot Skill structure
  const skillData = mapIRToCopilotSkill(ir);
  
  // Write file
  const skillPath = path.join(outputDir, `${agentId}.copilot-skill.json`);
  await fs.writeFile(skillPath, JSON.stringify(skillData, null, 2), 'utf-8');
  
  return skillPath;
}

module.exports = {
  generateCopilotSkill,
  mapIRToCopilotSkill,
  generateConversationStarters,
  mapToolsToExtensions,
  extractCapabilities,
  inferRole,
  formatInstructions,
  extractGovernanceMetadata,
  generateWorkspaceSettings
};
