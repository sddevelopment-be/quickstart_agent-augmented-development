#!/usr/bin/env node
/**
 * OpenCode Exporter
 * 
 * Converts agent profiles from markdown format to OpenCode standard format.
 * Keeps markdown files as single source of truth.
 * 
 * Usage:
 *   node tools/opencode-exporter.js
 *   node tools/opencode-exporter.js --agent architect
 *   node tools/opencode-exporter.js --output dist/opencode
 * 
 * @see https://opencode.ai/docs/agents/
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml'); // Note: requires installation

const OPENCODE_VERSION = '1.0';
const AGENTS_DIR = path.join(__dirname, '..', '.github', 'agents');
const DEFAULT_OUTPUT_DIR = path.join(__dirname, '..', 'dist', 'opencode');

/**
 * Parse markdown file with YAML frontmatter
 */
function parseAgentProfile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  
  // Extract YAML frontmatter
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) {
    throw new Error(`No frontmatter found in ${filePath}`);
  }
  
  const frontmatter = yaml.load(frontmatterMatch[1]);
  const markdownContent = content.substring(frontmatterMatch[0].length);
  
  return {
    frontmatter,
    content: markdownContent,
    filePath
  };
}

/**
 * Generate OpenCode discovery file (agent.opencode.json)
 */
function generateDiscoveryFile(profile) {
  const { frontmatter } = profile;
  
  return {
    opencode_version: OPENCODE_VERSION,
    agent: {
      id: frontmatter.name || path.basename(profile.filePath, '.agent.md'),
      name: frontmatter.name || 'Unknown Agent',
      version: frontmatter.version || '1.0.0',
      description: frontmatter.description || '',
      capabilities: frontmatter.tags || [],
      category: frontmatter.category || 'general',
      tools: frontmatter.tools || [],
      profile_url: `./${path.basename(profile.filePath)}`,
      metadata: {
        last_updated: frontmatter.last_updated || new Date().toISOString().split('T')[0],
        api_version: frontmatter.api_version || '1.0.0',
        directives: frontmatter.directives || [],
        styleguides: frontmatter.styleguides || []
      }
    }
  };
}

/**
 * Generate OpenCode definition file (agent.definition.yaml)
 */
function generateDefinitionFile(profile) {
  const { frontmatter } = profile;
  
  const definition = {
    opencode_version: OPENCODE_VERSION,
    agent: {
      metadata: {
        id: frontmatter.name || path.basename(profile.filePath, '.agent.md'),
        version: frontmatter.version || '1.0.0',
        category: frontmatter.category || 'general',
        tags: frontmatter.tags || []
      },
      specification: {
        inputs: frontmatter.inputs || [],
        outputs: frontmatter.outputs || [],
        examples: frontmatter.examples || [],
        tools: frontmatter.tools || []
      },
      governance: {
        directives: frontmatter.directives || [],
        styleguides: frontmatter.styleguides || [],
        safety_critical: frontmatter.safety_critical || false
      }
    }
  };
  
  return definition;
}

/**
 * Generate tool registry from all agents
 */
function generateToolRegistry(profiles) {
  const toolsSet = new Set();
  
  profiles.forEach(profile => {
    const tools = profile.frontmatter.tools || [];
    tools.forEach(tool => toolsSet.add(tool));
  });
  
  const tools = Array.from(toolsSet).map(toolName => ({
    id: toolName,
    name: toolName,
    type: inferToolType(toolName),
    // Schema would need to be defined separately
    schema: {
      type: 'object',
      properties: {},
      required: []
    }
  }));
  
  return {
    opencode_version: OPENCODE_VERSION,
    tools
  };
}

/**
 * Infer tool type from name (basic heuristic)
 */
function inferToolType(toolName) {
  const typeMap = {
    'read': 'file-io',
    'write': 'file-io',
    'search': 'search',
    'edit': 'file-io',
    'bash': 'execution',
    'plantuml': 'diagramming',
    'MultiEdit': 'file-io',
    'markdown-linter': 'validation',
    'report_progress': 'workflow'
  };
  
  return typeMap[toolName] || 'utility';
}

/**
 * Generate manifest file
 */
function generateManifest(profiles) {
  const agents = profiles.map(profile => {
    const frontmatter = profile.frontmatter;
    return {
      id: frontmatter.name || path.basename(profile.filePath, '.agent.md'),
      name: frontmatter.name || 'Unknown',
      version: frontmatter.version || '1.0.0',
      description: frontmatter.description || '',
      discovery_file: `./agents/${frontmatter.name || path.basename(profile.filePath, '.agent.md')}.opencode.json`,
      definition_file: `./agents/${frontmatter.name || path.basename(profile.filePath, '.agent.md')}.definition.yaml`
    };
  });
  
  return {
    opencode_version: OPENCODE_VERSION,
    generated_at: new Date().toISOString(),
    framework: {
      name: 'saboteurs-agents-framework',
      version: '1.0.0',
      description: 'Enterprise-grade multi-agent framework with governance',
      source_url: 'https://github.com/stijn-dejongh/saboteurs'
    },
    agents,
    extensions: {
      directives_supported: true,
      multi_agent_orchestration: true,
      governance_framework: true
    }
  };
}

/**
 * Main export function
 */
function exportToOpenCode(options = {}) {
  const {
    agentFilter = null,
    outputDir = DEFAULT_OUTPUT_DIR
  } = options;
  
  console.log('🚀 Starting OpenCode export...');
  
  // Find all agent profile files
  const agentFiles = fs.readdirSync(AGENTS_DIR)
    .filter(file => file.endsWith('.agent.md'))
    .filter(file => !agentFilter || file.startsWith(agentFilter));
  
  if (agentFiles.length === 0) {
    console.error('❌ No agent files found');
    return;
  }
  
  console.log(`📁 Found ${agentFiles.length} agent profile(s)`);
  
  // Parse all profiles
  const profiles = agentFiles.map(file => {
    const filePath = path.join(AGENTS_DIR, file);
    console.log(`  ├─ Parsing ${file}...`);
    return parseAgentProfile(filePath);
  });
  
  // Create output directory
  const agentsOutputDir = path.join(outputDir, 'agents');
  fs.mkdirSync(agentsOutputDir, { recursive: true });
  
  // Generate files for each agent
  profiles.forEach(profile => {
    const agentId = profile.frontmatter.name || path.basename(profile.filePath, '.agent.md');
    
    // Discovery file (JSON)
    const discoveryFile = generateDiscoveryFile(profile);
    const discoveryPath = path.join(agentsOutputDir, `${agentId}.opencode.json`);
    fs.writeFileSync(discoveryPath, JSON.stringify(discoveryFile, null, 2));
    console.log(`  ✅ Generated ${path.relative(process.cwd(), discoveryPath)}`);
    
    // Definition file (YAML)
    const definitionFile = generateDefinitionFile(profile);
    const definitionPath = path.join(agentsOutputDir, `${agentId}.definition.yaml`);
    fs.writeFileSync(definitionPath, yaml.dump(definitionFile));
    console.log(`  ✅ Generated ${path.relative(process.cwd(), definitionPath)}`);
  });
  
  // Generate tool registry
  const toolRegistry = generateToolRegistry(profiles);
  const toolsPath = path.join(outputDir, 'tools.opencode.json');
  fs.writeFileSync(toolsPath, JSON.stringify(toolRegistry, null, 2));
  console.log(`  ✅ Generated ${path.relative(process.cwd(), toolsPath)}`);
  
  // Generate manifest
  const manifest = generateManifest(profiles);
  const manifestPath = path.join(outputDir, 'manifest.opencode.json');
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  console.log(`  ✅ Generated ${path.relative(process.cwd(), manifestPath)}`);
  
  console.log('\n✨ OpenCode export complete!');
  console.log(`📦 Output directory: ${path.relative(process.cwd(), outputDir)}`);
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};
  
  for (let i = 0; i < args.length; i += 2) {
    const flag = args[i];
    const value = args[i + 1];
    
    if (flag === '--agent') {
      options.agentFilter = value;
    } else if (flag === '--output') {
      options.outputDir = value;
    }
  }
  
  try {
    exportToOpenCode(options);
  } catch (error) {
    console.error('❌ Export failed:', error.message);
    process.exit(1);
  }
}

module.exports = { exportToOpenCode, parseAgentProfile, generateDiscoveryFile, generateDefinitionFile };
