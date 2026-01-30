/**
 * OpenCode Generator
 * 
 * Generates OpenCode discovery and definition files from Agent IR.
 * This is the PRIMARY export format (70/100 compatibility, cross-platform standard).
 * 
 * @module opencode-generator
 * @version 1.0.0
 * 
 * Following Directives:
 * - 016 (ATDD): Acceptance tests written first
 * - 017 (TDD): Unit tests with Red-Green-Refactor
 * - 018 (Documentation): JSDoc for all public functions
 */

const fs = require('fs').promises;
const path = require('path');
const yaml = require('js-yaml');

const OPENCODE_VERSION = '1.0';
const API_VERSION = '1.0.0';

/**
 * Extract capabilities from IR content
 * Capabilities are derived from specialization, purpose, and tools
 * 
 * @param {Object} ir - Agent Intermediate Representation
 * @returns {Array<string>} Array of capability keywords
 */
function extractCapabilities(ir) {
  const capabilities = new Set();
  
  // Extract from tools (some tools indicate capabilities)
  const toolCapabilityMap = {
    'plantuml': 'diagramming',
    'Docker': 'containerization',
    'Java': 'backend',
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
  
  // Extract from specialization/purpose (look for key terms)
  // Only extract if there's meaningful content
  const content = [
    ir.content.purpose || '',
    ir.content.specialization || '',
    ir.content.success_criteria || ''
  ].join(' ').toLowerCase();
  
  // Only extract capabilities if content has substantial information
  // (more than just "Test purpose" or similar minimal content)
  if (content.length < 30) {
    return Array.from(capabilities);
  }
  
  // Common capability keywords with word boundary matching
  const capabilityKeywords = {
    'architecture': 'architecture',
    'architectural': 'architecture',
    'design': 'design',
    'adr': 'decision-records',
    'testing': 'testing',
    'review': 'code-review',
    'backend': 'backend',
    'api': 'api-design',
    'database': 'data-persistence',
    'documentation': 'documentation',
    'governance': 'governance',
    'workflow': 'workflow',
    'bootstrap': 'initialization',
    'security': 'security',
    'performance': 'performance'
  };
  
  Object.entries(capabilityKeywords).forEach(([keyword, capability]) => {
    // Use word boundary matching to avoid partial matches
    const regex = new RegExp(`\\b${keyword}\\b`, 'i');
    if (regex.test(content)) {
      capabilities.add(capability);
    }
  });
  
  return Array.from(capabilities);
}

/**
 * Infer category from agent name, purpose, and specialization
 * 
 * @param {Object} ir - Agent Intermediate Representation
 * @returns {string} Category name
 */
function inferCategory(ir) {
  const name = ir.frontmatter.name.toLowerCase();
  const content = [
    ir.content.purpose || '',
    ir.content.specialization || ''
  ].join(' ').toLowerCase();
  
  // Only infer from content if there's substantial information
  const hasSubstantialContent = content.length > 30;
  
  // Category mapping - check most specific first
  if (name.includes('architect') || (hasSubstantialContent && /\barchitecture\b/i.test(content))) {
    return 'design';
  }
  if (name.includes('backend') || (name.includes('dev') && !name.includes('test-'))) {
    return 'development';
  }
  if (name.includes('review') || (hasSubstantialContent && /\breview\b/i.test(content))) {
    return 'quality-assurance';
  }
  if (name.includes('tester') || name.includes('qa-')) {
    return 'testing';
  }
  if (name.includes('doc') || (hasSubstantialContent && /\bdocumentation\b/i.test(content))) {
    return 'documentation';
  }
  if (name.includes('bootstrap') || name.includes('init')) {
    return 'initialization';
  }
  if (name.includes('curator') || (hasSubstantialContent && /\bgovernance\b/i.test(content))) {
    return 'governance';
  }
  
  return 'general';
}

/**
 * Format agent name from ID
 * Converts 'backend-benny' to 'Backend Benny'
 * 
 * @param {string} id - Agent ID
 * @returns {string} Formatted name
 */
function formatAgentName(id) {
  return id
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

/**
 * Map IR to OpenCode discovery file structure
 * 
 * @param {Object} ir - Agent Intermediate Representation
 * @returns {Object} OpenCode discovery structure
 */
function mapIRToDiscovery(ir) {
  const agentId = ir.frontmatter.name;
  const capabilities = extractCapabilities(ir);
  const category = inferCategory(ir);
  
  // Extract last updated from metadata
  const lastUpdated = ir.metadata.parsed_at.split('T')[0];
  
  // Format directives as array of code strings
  const directives = ir.relationships.directives.map(d => d.code_formatted);
  
  // Extract styleguides if present in context sources
  const styleguides = ir.relationships.context_sources
    .filter(s => s.type.toLowerCase().includes('style') || s.location.includes('style'))
    .map(s => path.basename(s.location));
  
  const discovery = {
    opencode_version: OPENCODE_VERSION,
    agent: {
      id: agentId,
      name: formatAgentName(agentId),
      version: ir.frontmatter.version || '1.0.0',
      description: ir.frontmatter.description,
      capabilities: capabilities,
      category: category,
      tools: ir.frontmatter.tools,
      profile_url: `./${path.basename(ir.metadata.file_path)}`,
      metadata: {
        last_updated: lastUpdated,
        api_version: API_VERSION,
        directives: directives,
        styleguides: styleguides
      }
    },
    extensions: extractGovernanceMetadata(ir)
  };
  
  return discovery;
}

/**
 * Map IR to OpenCode definition file structure
 * 
 * @param {Object} ir - Agent Intermediate Representation
 * @returns {Object} OpenCode definition structure
 */
function mapIRToDefinition(ir) {
  const agentId = ir.frontmatter.name;
  const capabilities = extractCapabilities(ir);
  
  // Format directives for governance section
  const directives = ir.relationships.directives.map(d => ({
    code: d.code_formatted,
    title: d.title,
    required: d.required
  }));
  
  const definition = {
    opencode_version: OPENCODE_VERSION,
    agent: {
      metadata: {
        id: agentId,
        version: ir.frontmatter.version || '1.0.0',
        category: inferCategory(ir),
        tags: capabilities
      },
      specification: {
        inputs: [],  // TODO: Extract from content if present
        outputs: [],  // TODO: Extract from content if present
        examples: [],  // TODO: Extract from content if present
        tools: ir.frontmatter.tools
      },
      governance: {
        directives: directives,
        safety_critical: ir.governance.safety_criticality !== null,
        primer_required: ir.governance.primer_required,
        test_first_required: ir.governance.test_first_required,
        uncertainty_threshold: ir.governance.uncertainty_threshold || 'not specified',
        escalation_rules: ir.governance.escalation_rules
      }
    }
  };
  
  return definition;
}

/**
 * Extract governance metadata for OpenCode extensions
 * 
 * @param {Object} ir - Agent Intermediate Representation
 * @returns {Object} Governance extensions object
 */
function extractGovernanceMetadata(ir) {
  // Determine priority level from specialization
  let priorityLevel = 'medium';
  if (ir.content.specialization) {
    const spec = ir.content.specialization.toLowerCase();
    if (spec.includes('critical') || spec.includes('production') || spec.includes('primary')) {
      priorityLevel = 'high';
    } else if (spec.includes('secondary') || spec.includes('optional')) {
      priorityLevel = 'low';
    }
  }
  
  // Determine if orchestration capable (look for workflow/coordination keywords)
  const content = [
    ir.content.purpose || '',
    ir.content.specialization || '',
    ir.content.collaboration_contract || ''
  ].join(' ').toLowerCase();
  
  const orchestrationCapable = content.includes('orchestrat') || 
                               content.includes('coordinat') || 
                               content.includes('workflow') ||
                               content.includes('manage') && content.includes('agent');
  
  // Determine handoff protocols (file-based is default, message-queue if mentioned)
  const handoffProtocols = ['file-based'];
  if (content.includes('message') || content.includes('queue') || content.includes('event')) {
    handoffProtocols.push('message-queue');
  }
  
  // Determine specialization boundaries
  const specializationBoundaries = ir.content.specialization && 
                                  (ir.content.specialization.includes('**Primary focus:**') ||
                                   ir.content.specialization.includes('**Avoid:**'))
                                  ? 'explicit'
                                  : 'flexible';
  
  // Determine if escalation required
  const escalationRequired = ir.governance.escalation_rules.length > 0;
  
  // Format directives with required/optional flags
  const directivesWithFlags = ir.relationships.directives.map(d => ({
    code: d.code_formatted,
    title: d.title,
    required: d.required,
    rationale: d.rationale
  }));
  
  return {
    saboteurs_governance: {
      directives: directivesWithFlags,
      priority_level: priorityLevel,
      uncertainty_threshold: ir.governance.uncertainty_threshold || 'not specified',
      escalation_required: escalationRequired,
      primer_required: ir.governance.primer_required,
      test_first_required: ir.governance.test_first_required,
      safety_criticality: ir.governance.safety_criticality
    },
    multi_agent: {
      orchestration_capable: orchestrationCapable,
      handoff_protocols: handoffProtocols,
      specialization_boundaries: specializationBoundaries
    }
  };
}

/**
 * Generate OpenCode files from Agent IR
 * 
 * @param {Object} ir - Parsed agent IR
 * @param {string} outputDir - Directory where to write files
 * @returns {Promise<{discovery: string, definition: string}>} Paths to generated files
 */
async function generateOpenCode(ir, outputDir) {
  // Ensure output directory exists
  await fs.mkdir(outputDir, { recursive: true });
  
  const agentId = ir.frontmatter.name;
  
  // Generate discovery file
  const discoveryData = mapIRToDiscovery(ir);
  const discoveryPath = path.join(outputDir, `${agentId}.opencode.json`);
  await fs.writeFile(discoveryPath, JSON.stringify(discoveryData, null, 2), 'utf-8');
  
  // Generate definition file
  const definitionData = mapIRToDefinition(ir);
  const definitionPath = path.join(outputDir, `${agentId}.definition.yaml`);
  await fs.writeFile(definitionPath, yaml.dump(definitionData, { lineWidth: 120 }), 'utf-8');
  
  return {
    discovery: discoveryPath,
    definition: definitionPath
  };
}

module.exports = {
  generateOpenCode,
  mapIRToDiscovery,
  mapIRToDefinition,
  extractGovernanceMetadata,
  extractCapabilities,
  inferCategory,
  formatAgentName
};
