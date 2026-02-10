#!/usr/bin/env node
/**
 * Skills Deployment Script
 *
 * Deploys exported skills from dist/ to tool-specific locations:
 * - Claude Code: .claude/skills/<name>/SKILL.md
 * - Claude Agents: .claude/agents/*.agent.md
 * - Claude Prompts: .claude/prompts/*.{md,yaml}
 * - GitHub Copilot: .github/instructions/<name>.instructions.md
 * - OpenCode: .opencode/agents/, .opencode/skills/
 *
 * Usage:
 *   node ops/deploy-skills.js [--claude] [--agents] [--prompts] [--copilot] [--opencode] [--all]
 *   npm run deploy:skills
 *   npm run deploy:claude:agents
 *   npm run deploy:claude:prompts
 *
 * Prerequisites:
 *   Run `npm run export:all` first to generate dist/ files (for skills)
 *   Agents and prompts deploy directly from source
 */

const fs = require('fs').promises;
const path = require('path');

// Claude Code generator (SPEC-DIST-002)
const { simplifyAgent, generateRulesFile, generateClaudeMd, RULES_MAPPING } = require('../exporters/claude-code-generator');
const { parseAgentFile } = require('../exporters/parser');

// Repository root
const ROOT = path.join(__dirname, '..', '..');

// Source directories (from export)
const DIST_DIR = path.join(__dirname, '..', 'dist');
const SKILLS_DIR = path.join(DIST_DIR, 'skills');
const OPENCODE_DIR = path.join(DIST_DIR, 'opencode');

// Source directories (direct)
const AGENTS_SOURCE_DIR = path.join(ROOT, 'doctrine', 'agents');
const PROMPTS_SOURCE_DIR = path.join(ROOT, 'docs', 'templates', 'prompts');

// Target directories (tool-specific)
const CLAUDE_DIR = path.join(ROOT, '.claude');
const CLAUDE_SKILLS_DIR = path.join(CLAUDE_DIR, 'skills');
const CLAUDE_AGENTS_DIR = path.join(CLAUDE_DIR, 'agents');
const CLAUDE_PROMPTS_DIR = path.join(CLAUDE_DIR, 'prompts');
const CLAUDE_RULES_DIR = path.join(CLAUDE_DIR, 'rules');
const COPILOT_INSTRUCTIONS_DIR = path.join(ROOT, '.github', 'instructions');
const OPENCODE_TARGET_DIR = path.join(ROOT, '.opencode');

/**
 * Deploy Claude Code skills
 * Converts JSON skill definitions to SKILL.md format
 */
async function deployClaudeSkills() {
  console.log('🤖 Deploying Claude Code skills...');

  const claudeSourceDir = path.join(SKILLS_DIR, 'claude-code');

  try {
    await fs.access(claudeSourceDir);
  } catch {
    console.log('   ⚠️  No Claude Code skills found in dist/skills/claude-code/');
    console.log('      Run `npm run export:skills` first');
    return { deployed: 0, errors: [] };
  }

  const files = await fs.readdir(claudeSourceDir);
  const skillFiles = files.filter(f => f.endsWith('.json'));

  const results = { deployed: 0, errors: [] };

  for (const file of skillFiles) {
    try {
      const content = await fs.readFile(path.join(claudeSourceDir, file), 'utf-8');
      const skill = JSON.parse(content);

      // Determine skill name from file or content
      const skillId = skill.skill?.id || file.replace('.skill.json', '').replace('.approach.json', '');
      const skillDir = path.join(CLAUDE_SKILLS_DIR, skillId);

      // Create skill directory
      await fs.mkdir(skillDir, { recursive: true });

      // Generate SKILL.md content
      const skillMd = generateClaudeSkillMd(skill, file);

      // Write SKILL.md
      await fs.writeFile(path.join(skillDir, 'SKILL.md'), skillMd);

      console.log(`   ✅ ${skillId}/SKILL.md`);
      results.deployed++;
    } catch (error) {
      console.log(`   ❌ ${file}: ${error.message}`);
      results.errors.push({ file, error: error.message });
    }
  }

  return results;
}

/**
 * Generate SKILL.md content from JSON skill definition
 */
function generateClaudeSkillMd(skill, filename) {
  const s = skill.skill || skill;
  const isApproach = filename.includes('approach');

  // Build frontmatter
  const frontmatter = {
    name: s.name || s.id,
    description: s.description || '',
    version: s.version || '1.0.0',
    type: isApproach ? 'approach' : 'prompt-template'
  };

  if (s.agent) frontmatter.agent = s.agent;
  if (s.category) frontmatter.category = s.category;
  if (s.tags?.length) frontmatter.tags = s.tags;

  // Build markdown content
  let content = '---\n';
  content += Object.entries(frontmatter)
    .map(([k, v]) => {
      if (Array.isArray(v)) return `${k}: [${v.map(i => `"${i}"`).join(', ')}]`;
      return `${k}: "${v}"`;
    })
    .join('\n');
  content += '\n---\n\n';

  // Title
  content += `# ${s.name || s.id}\n\n`;

  // Description
  if (s.description) {
    content += `${s.description}\n\n`;
  }

  // Instructions (main content)
  if (skill.instructions) {
    content += `## Instructions\n\n${skill.instructions}\n\n`;
  }

  // Workflow/Steps
  if (s.workflow?.length) {
    content += `## Workflow\n\n`;
    s.workflow.forEach((step, i) => {
      content += `${i + 1}. ${step}\n`;
    });
    content += '\n';
  }

  if (s.workflow_steps?.length) {
    content += `## Workflow Steps\n\n`;
    s.workflow_steps.forEach(step => {
      content += `${step.step}. ${step.description}\n`;
    });
    content += '\n';
  }

  // Principles (for approaches)
  if (s.principles?.length) {
    content += `## Principles\n\n`;
    s.principles.forEach((p, i) => {
      if (typeof p === 'string') {
        content += `${i + 1}. ${p}\n`;
      } else {
        content += `### ${p.number || i + 1}. ${p.title}\n\n${p.description}\n\n`;
      }
    });
  }

  // When to use
  if (s.when_to_use?.length) {
    content += `## When to Use\n\n`;
    s.when_to_use.forEach(item => {
      content += `- ${item}\n`;
    });
    content += '\n';
  }

  // Inputs (for prompt templates)
  if (s.inputs?.length) {
    content += `## Inputs\n\n`;
    s.inputs.forEach(input => {
      const desc = input.description ? ` - ${input.description}` : '';
      const req = input.required ? ' (required)' : '';
      content += `- **${input.name}**${req}${desc}\n`;
    });
    content += '\n';
  }

  // Outputs
  if (s.outputs?.length) {
    content += `## Outputs\n\n`;
    s.outputs.forEach(output => {
      content += `- ${output}\n`;
    });
    content += '\n';
  }

  // Constraints
  if (s.constraints?.length) {
    content += `## Constraints\n\n`;
    s.constraints.forEach(constraint => {
      content += `- ${constraint}\n`;
    });
    content += '\n';
  }

  return content;
}

/**
 * Deploy GitHub Copilot instructions
 * Converts JSON to .instructions.md format
 */
async function deployCopilotInstructions() {
  console.log('🐙 Deploying GitHub Copilot instructions...');

  const copilotSourceDir = path.join(SKILLS_DIR, 'copilot');

  try {
    await fs.access(copilotSourceDir);
  } catch {
    console.log('   ⚠️  No Copilot skills found in dist/skills/copilot/');
    console.log('      Run `npm run export:skills` first');
    return { deployed: 0, errors: [] };
  }

  // Create instructions directory
  await fs.mkdir(COPILOT_INSTRUCTIONS_DIR, { recursive: true });

  const files = await fs.readdir(copilotSourceDir);
  const skillFiles = files.filter(f => f.endsWith('.json'));

  const results = { deployed: 0, errors: [] };

  for (const file of skillFiles) {
    try {
      const content = await fs.readFile(path.join(copilotSourceDir, file), 'utf-8');
      const skill = JSON.parse(content);

      // Generate instruction filename
      const baseName = file
        .replace('.copilot-skill.json', '')
        .replace('.copilot-approach.json', '');
      const instructionFile = `${baseName}.instructions.md`;

      // Generate markdown instructions
      const instructionMd = generateCopilotInstructionMd(skill, baseName);

      // Write instruction file
      await fs.writeFile(
        path.join(COPILOT_INSTRUCTIONS_DIR, instructionFile),
        instructionMd
      );

      console.log(`   ✅ ${instructionFile}`);
      results.deployed++;
    } catch (error) {
      console.log(`   ❌ ${file}: ${error.message}`);
      results.errors.push({ file, error: error.message });
    }
  }

  // Also generate consolidated copilot-instructions.md
  await generateConsolidatedCopilotInstructions(copilotSourceDir);

  return results;
}

/**
 * Generate .instructions.md content from Copilot skill JSON
 */
function generateCopilotInstructionMd(skill, name) {
  let content = `# ${skill.name || name}\n\n`;

  if (skill.description) {
    content += `${skill.description}\n\n`;
  }

  // Capabilities
  if (skill.capabilities?.length) {
    content += `## Capabilities\n\n`;
    skill.capabilities.forEach(cap => {
      content += `- ${cap}\n`;
    });
    content += '\n';
  }

  // Main instructions
  if (skill.instructions) {
    content += `## Instructions\n\n${skill.instructions}\n\n`;
  }

  // Conversation starters
  if (skill.conversation_starters?.length) {
    content += `## Example Prompts\n\n`;
    skill.conversation_starters.forEach(starter => {
      content += `- "${starter}"\n`;
    });
    content += '\n';
  }

  // Extensions metadata (as reference)
  if (skill.extensions) {
    const ext = skill.extensions.agentic_governance || skill.extensions.agentic_framework;
    if (ext) {
      content += `## Metadata\n\n`;
      if (ext.agent) content += `- **Agent**: ${ext.agent}\n`;
      if (ext.category) content += `- **Category**: ${ext.category}\n`;
      if (ext.complexity) content += `- **Complexity**: ${ext.complexity}\n`;
      content += '\n';
    }
  }

  return content;
}

/**
 * Generate consolidated .github/copilot-instructions.md
 */
async function generateConsolidatedCopilotInstructions(sourceDir) {
  const files = await fs.readdir(sourceDir);
  const skillFiles = files.filter(f => f.endsWith('.json'));

  let content = `# Copilot Custom Instructions

This file provides custom instructions for GitHub Copilot based on the agent framework.

## Available Skills

`;

  // Group by type
  const promptSkills = [];
  const approachSkills = [];

  for (const file of skillFiles) {
    const data = JSON.parse(await fs.readFile(path.join(sourceDir, file), 'utf-8'));
    if (file.includes('approach')) {
      approachSkills.push(data);
    } else {
      promptSkills.push(data);
    }
  }

  // Prompt templates section
  if (promptSkills.length > 0) {
    content += `### Prompt Templates\n\n`;
    content += `These are reusable task-specific prompts:\n\n`;
    promptSkills.forEach(skill => {
      content += `- **${skill.name}**: ${skill.description}\n`;
    });
    content += '\n';
  }

  // Approaches section
  if (approachSkills.length > 0) {
    content += `### Operational Approaches\n\n`;
    content += `These are workflow patterns and operational guides:\n\n`;
    approachSkills.forEach(skill => {
      content += `- **${skill.name}**: ${skill.description}\n`;
    });
    content += '\n';
  }

  content += `## Detailed Instructions

For detailed instructions, see the individual files in \`.github/instructions/\`.

## Framework Reference

This project uses the Agent-Augmented Development framework. Key references:
- Agent profiles: \`.github/agents/*.agent.md\`
- Directives: \`.github/agents/directives/\`
- Approaches: \`.github/agents/approaches/\`
`;

  await fs.writeFile(
    path.join(__dirname, '..', '.github', 'copilot-instructions.md'),
    content
  );

  console.log('   ✅ copilot-instructions.md (consolidated)');
}

/**
 * Deploy OpenCode configuration
 * Copies agent and skill JSONs to .opencode/ with manifest
 */
async function deployOpenCode() {
  console.log('📦 Deploying OpenCode configuration...');

  try {
    await fs.access(OPENCODE_DIR);
  } catch {
    console.log('   ⚠️  No OpenCode exports found in dist/opencode/');
    console.log('      Run `npm run export:agents` first');
    return { deployed: 0, errors: [] };
  }

  // Create target directories
  const agentsDir = path.join(OPENCODE_TARGET_DIR, 'agents');
  const skillsDir = path.join(OPENCODE_TARGET_DIR, 'skills');
  await fs.mkdir(agentsDir, { recursive: true });
  await fs.mkdir(skillsDir, { recursive: true });

  const results = { deployed: 0, errors: [] };
  const manifest = {
    $schema: 'https://opencode.ai/schemas/config.json',
    version: '1.0',
    agents: [],
    skills: []
  };

  // Deploy agent files from dist/opencode/agents/
  const agentSourceDir = path.join(OPENCODE_DIR, 'agents');
  try {
    const agentFiles = await fs.readdir(agentSourceDir);
    const jsonFiles = agentFiles.filter(f => f.endsWith('.opencode.json'));

    for (const file of jsonFiles) {
      try {
        const content = await fs.readFile(path.join(agentSourceDir, file), 'utf-8');
        const agent = JSON.parse(content);

        // Copy to target
        await fs.writeFile(path.join(agentsDir, file), content);

        // Add to manifest
        manifest.agents.push({
          id: agent.agent?.id || file.replace('.opencode.json', ''),
          path: `./agents/${file}`
        });

        console.log(`   ✅ agents/${file}`);
        results.deployed++;
      } catch (error) {
        console.log(`   ❌ ${file}: ${error.message}`);
        results.errors.push({ file, error: error.message });
      }
    }
  } catch {
    console.log('   ⚠️  No agent files in dist/opencode/agents/');
  }

  // Deploy skill files from dist/skills/opencode/
  const skillSourceDir = path.join(SKILLS_DIR, 'opencode');
  try {
    const skillFiles = await fs.readdir(skillSourceDir);
    const jsonFiles = skillFiles.filter(f => f.endsWith('.json'));

    for (const file of jsonFiles) {
      try {
        const content = await fs.readFile(path.join(skillSourceDir, file), 'utf-8');
        const skill = JSON.parse(content);

        // Copy to target
        await fs.writeFile(path.join(skillsDir, file), content);

        // Add to manifest
        manifest.skills.push({
          id: skill.skill?.id || file.replace('.opencode-skill.json', '').replace('.opencode-approach.json', ''),
          path: `./skills/${file}`
        });

        console.log(`   ✅ skills/${file}`);
        results.deployed++;
      } catch (error) {
        console.log(`   ❌ ${file}: ${error.message}`);
        results.errors.push({ file, error: error.message });
      }
    }
  } catch {
    console.log('   ⚠️  No skill files in dist/skills/opencode/');
  }

  // Copy manifest and tools
  try {
    const distManifest = await fs.readFile(path.join(OPENCODE_DIR, 'manifest.opencode.json'), 'utf-8');
    await fs.writeFile(path.join(OPENCODE_TARGET_DIR, 'manifest.json'), distManifest);
    console.log('   ✅ manifest.json');
  } catch {
    // Generate our own manifest
    await fs.writeFile(
      path.join(OPENCODE_TARGET_DIR, 'opencode.json'),
      JSON.stringify(manifest, null, 2)
    );
    console.log('   ✅ opencode.json (generated)');
  }

  return results;
}

/**
 * Deploy Claude Agents
 * Copies agent files from .github/agents/*.agent.md to .claude/agents/
 */
async function deployClaudeAgents() {
  console.log('🤖 Deploying Claude agents...');

  try {
    await fs.access(AGENTS_SOURCE_DIR);
  } catch {
    console.log('   ⚠️  No agents found in .github/agents/');
    return { deployed: 0, errors: [] };
  }

  // Create target directory
  await fs.mkdir(CLAUDE_AGENTS_DIR, { recursive: true });

  const files = await fs.readdir(AGENTS_SOURCE_DIR);
  const agentFiles = files.filter(f => f.endsWith('.agent.md'));

  const results = { deployed: 0, errors: [] };
  const manifest = {
    version: '1.0.0',
    description: 'Claude agent profiles for specialist roles',
    generated: new Date().toISOString(),
    agents: []
  };

  for (const file of agentFiles) {
    try {
      const sourcePath = path.join(AGENTS_SOURCE_DIR, file);
      const targetPath = path.join(CLAUDE_AGENTS_DIR, file);

      // Parse via IR and simplify (SPEC-DIST-002)
      const ir = await parseAgentFile(sourcePath);
      const simplified = simplifyAgent(ir);

      // Write simplified agent
      await fs.writeFile(targetPath, simplified);

      // Add to manifest
      manifest.agents.push({
        id: file.replace('.agent.md', ''),
        name: ir.frontmatter.name,
        description: ir.frontmatter.description,
        file: file
      });

      console.log(`   ✅ ${file} (simplified)`);
      results.deployed++;
    } catch (error) {
      console.log(`   ❌ ${file}: ${error.message}`);
      results.errors.push({ file, error: error.message });
    }
  }

  // Write manifest
  try {
    await fs.writeFile(
      path.join(CLAUDE_AGENTS_DIR, 'manifest.json'),
      JSON.stringify(manifest, null, 2)
    );
    console.log('   ✅ manifest.json');
  } catch (error) {
    console.log(`   ⚠️  Could not write manifest: ${error.message}`);
  }

  // Write README
  const readme = generateAgentsReadme(manifest);
  try {
    await fs.writeFile(
      path.join(CLAUDE_AGENTS_DIR, 'README.md'),
      readme
    );
    console.log('   ✅ README.md');
  } catch (error) {
    console.log(`   ⚠️  Could not write README: ${error.message}`);
  }

  return results;
}

/**
 * Generate README for agents directory
 */
function generateAgentsReadme(manifest) {
  let content = `# Claude Agents

Specialist agent profiles for Claude Code integration.

## Overview

This directory contains ${manifest.agents.length} specialist agent profiles that define roles, capabilities, and workflows for different development tasks.

## Available Agents

`;

  manifest.agents.forEach(agent => {
    content += `### ${agent.name}\n\n`;
    if (agent.description) {
      content += `${agent.description}\n\n`;
    }
    content += `**File:** \`${agent.file}\`\n\n`;
  });

  content += `
## Usage

These agent profiles can be used with Claude Code to:
- Bootstrap specialized development contexts
- Ensure consistent workflows across tasks
- Reference domain-specific directives and approaches
- Maintain alignment with project architecture

## Integration

Agents reference:
- **Directives:** \`.github/agents/directives/\` - Operational guidelines
- **Approaches:** \`.github/agents/approaches/\` - Workflow patterns
- **Guidelines:** \`.github/agents/guidelines/\` - General principles

## Manifest

See \`manifest.json\` for structured metadata including agent IDs, names, and descriptions.

---
*Generated: ${manifest.generated}*
`;

  return content;
}

/**
 * Deploy Claude Prompts
 * Copies prompt templates from docs/templates/prompts/ to .claude/prompts/
 */
async function deployClaudePrompts() {
  console.log('📝 Deploying Claude prompts...');

  try {
    await fs.access(PROMPTS_SOURCE_DIR);
  } catch {
    console.log('   ⚠️  No prompts found in docs/templates/prompts/');
    return { deployed: 0, errors: [] };
  }

  // Create target directory
  await fs.mkdir(CLAUDE_PROMPTS_DIR, { recursive: true });

  const files = await fs.readdir(PROMPTS_SOURCE_DIR);
  const promptFiles = files.filter(f => 
    (f.endsWith('.prompt.md') || f.endsWith('.yaml')) && f !== 'README.md'
  );

  const results = { deployed: 0, errors: [] };
  const manifest = {
    version: '1.0.0',
    description: 'Claude prompt templates for common development tasks',
    generated: new Date().toISOString(),
    prompts: []
  };

  for (const file of promptFiles) {
    try {
      const sourcePath = path.join(PROMPTS_SOURCE_DIR, file);
      const targetPath = path.join(CLAUDE_PROMPTS_DIR, file);
      
      // Read source content
      const content = await fs.readFile(sourcePath, 'utf-8');
      
      // Copy to target
      await fs.writeFile(targetPath, content);

      // Parse metadata (frontmatter for .md, YAML for .yaml)
      let metadata = { 
        id: file.replace('.prompt.md', '').replace('.yaml', ''),
        description: '',
        agent: '',
        category: ''
      };
      
      if (file.endsWith('.prompt.md')) {
        const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
        if (frontmatterMatch) {
          const fm = frontmatterMatch[1];
          const descMatch = fm.match(/description:\s*['"]?(.+?)['"]?\n/);
          const agentMatch = fm.match(/agent:\s*(.+)/);
          const catMatch = fm.match(/category:\s*(.+)/);
          if (descMatch) metadata.description = descMatch[1].trim();
          if (agentMatch) metadata.agent = agentMatch[1].trim();
          if (catMatch) metadata.category = catMatch[1].trim();
        }
      } else if (file.endsWith('.yaml')) {
        // Basic YAML parsing for name/description
        const nameMatch = content.match(/name:\s*(.+)/);
        const descMatch = content.match(/description:\s*['"]?(.+?)['"]?\n/);
        if (nameMatch) metadata.id = nameMatch[1].trim();
        if (descMatch) metadata.description = descMatch[1].trim();
      }

      // Add to manifest
      manifest.prompts.push({
        id: metadata.id,
        file: file,
        type: file.endsWith('.yaml') ? 'yaml' : 'markdown',
        description: metadata.description,
        agent: metadata.agent,
        category: metadata.category
      });

      console.log(`   ✅ ${file}`);
      results.deployed++;
    } catch (error) {
      console.log(`   ❌ ${file}: ${error.message}`);
      results.errors.push({ file, error: error.message });
    }
  }

  // Write manifest
  try {
    await fs.writeFile(
      path.join(CLAUDE_PROMPTS_DIR, 'manifest.json'),
      JSON.stringify(manifest, null, 2)
    );
    console.log('   ✅ manifest.json');
  } catch (error) {
    console.log(`   ⚠️  Could not write manifest: ${error.message}`);
  }

  // Write README
  const readme = generatePromptsReadme(manifest);
  try {
    await fs.writeFile(
      path.join(CLAUDE_PROMPTS_DIR, 'README.md'),
      readme
    );
    console.log('   ✅ README.md');
  } catch (error) {
    console.log(`   ⚠️  Could not write README: ${error.message}`);
  }

  return results;
}

/**
 * Generate README for prompts directory
 */
function generatePromptsReadme(manifest) {
  let content = `# Claude Prompts

Task-specific prompt templates for Claude Code integration.

## Overview

This directory contains ${manifest.prompts.length} prompt templates for common development tasks.

## Available Prompts

### Markdown Templates (.prompt.md)

`;

  const mdPrompts = manifest.prompts.filter(p => p.type === 'markdown');
  const yamlPrompts = manifest.prompts.filter(p => p.type === 'yaml');

  mdPrompts.forEach(prompt => {
    content += `#### ${prompt.id}\n`;
    if (prompt.description) {
      content += `${prompt.description}\n\n`;
    }
    if (prompt.agent) {
      content += `**Agent:** ${prompt.agent}  \n`;
    }
    if (prompt.category) {
      content += `**Category:** ${prompt.category}  \n`;
    }
    content += `**File:** \`${prompt.file}\`\n\n`;
  });

  content += `### YAML Templates (.yaml)

`;

  yamlPrompts.forEach(prompt => {
    content += `#### ${prompt.id}\n`;
    if (prompt.description) {
      content += `${prompt.description}\n\n`;
    }
    content += `**File:** \`${prompt.file}\`\n\n`;
  });

  content += `
## Usage

These prompts can be used:
1. **Direct execution** - Copy and fill in template variables
2. **Agent context** - Reference in agent workflows
3. **Tool integration** - Import into Claude Code or other AI tools

## Format

- **Markdown templates** (.prompt.md): Include frontmatter with metadata and structured instructions
- **YAML templates** (.yaml): Structured format with sections, inputs, outputs, and constraints

## Manifest

See \`manifest.json\` for structured metadata including prompt IDs, types, agents, and categories.

---
*Generated: ${manifest.generated}*
`;

  return content;
}

/**
 * Deploy Claude Code rules files (SPEC-DIST-002)
 * Generates .claude/rules/*.md from doctrine source files
 */
async function deployClaudeRules() {
  console.log('📏 Deploying Claude Code rules...');

  await fs.mkdir(CLAUDE_RULES_DIR, { recursive: true });

  const results = { deployed: 0, errors: [] };

  for (const [ruleName, sourcePaths] of Object.entries(RULES_MAPPING)) {
    try {
      const absolutePaths = sourcePaths.map(p => path.join(ROOT, p));
      const content = await generateRulesFile(absolutePaths, ruleName);
      await fs.writeFile(path.join(CLAUDE_RULES_DIR, `${ruleName}.md`), content);

      console.log(`   ✅ rules/${ruleName}.md`);
      results.deployed++;
    } catch (error) {
      console.log(`   ❌ rules/${ruleName}.md: ${error.message}`);
      results.errors.push({ file: `${ruleName}.md`, error: error.message });
    }
  }

  return results;
}

/**
 * Deploy CLAUDE.md project instructions (SPEC-DIST-002)
 * Generates CLAUDE.md at repository root from doctrine sources
 */
async function deployClaudeMd() {
  console.log('📋 Deploying CLAUDE.md...');

  const results = { deployed: 0, errors: [] };

  try {
    const content = await generateClaudeMd({
      visionFile: path.join(ROOT, 'docs', 'VISION.md'),
      quickRefFile: path.join(ROOT, 'doctrine', 'directives', '003_repository_quick_reference.md'),
      pythonConventionsFile: path.join(ROOT, 'doctrine', 'guidelines', 'python-conventions.md'),
      projectRoot: ROOT
    });

    await fs.writeFile(path.join(ROOT, 'CLAUDE.md'), content);
    console.log('   ✅ CLAUDE.md');
    results.deployed++;
  } catch (error) {
    console.log(`   ❌ CLAUDE.md: ${error.message}`);
    results.errors.push({ file: 'CLAUDE.md', error: error.message });
  }

  return results;
}

/**
 * Main deployment function
 */
async function main() {
  const args = process.argv.slice(2);
  const deployAll = args.includes('--all') || args.length === 0;
  const deployClaude = deployAll || args.includes('--claude');
  const deployAgentsFlag = deployAll || args.includes('--agents');
  const deployPromptsLegacy = args.includes('--prompts-legacy') || args.includes('--prompts');
  const deployCopilot = deployAll || args.includes('--copilot');
  const deployOpenCodeFlag = deployAll || args.includes('--opencode');
  const deployRulesFlag = deployAll || args.includes('--rules');
  const deployClaudeMdFlag = deployAll || args.includes('--claude-md');

  console.log('🚀 Deploying to Claude Code...\n');

  let totalDeployed = 0;
  let totalErrors = 0;

  // Check if dist/ exists (only needed for skills deployment)
  if (deployClaude || deployAll) {
    try {
      await fs.access(DIST_DIR);
    } catch {
      console.error('⚠️  dist/ directory not found for skills deployment.');
      console.error('   Run `npm run export:all` first if deploying skills.');
      if (deployClaude && !deployAgentsFlag && !deployRulesFlag && !deployClaudeMdFlag) {
        process.exit(1);
      }
    }
  }

  // CLAUDE.md (SPEC-DIST-002)
  if (deployClaudeMdFlag) {
    const results = await deployClaudeMd();
    totalDeployed += results.deployed;
    totalErrors += results.errors.length;
    console.log();
  }

  // Rules files (SPEC-DIST-002)
  if (deployRulesFlag) {
    const results = await deployClaudeRules();
    totalDeployed += results.deployed;
    totalErrors += results.errors.length;
    console.log();
  }

  if (deployClaude) {
    const results = await deployClaudeSkills();
    totalDeployed += results.deployed;
    totalErrors += results.errors.length;
    console.log();
  }

  if (deployAgentsFlag) {
    const results = await deployClaudeAgents();
    totalDeployed += results.deployed;
    totalErrors += results.errors.length;
    console.log();
  }

  // Prompts deprecated (SPEC-DIST-002 FR-4), retained behind --prompts-legacy
  if (deployPromptsLegacy) {
    const results = await deployClaudePrompts();
    totalDeployed += results.deployed;
    totalErrors += results.errors.length;
    console.log();
  }

  if (deployCopilot) {
    const results = await deployCopilotInstructions();
    totalDeployed += results.deployed;
    totalErrors += results.errors.length;
    console.log();
  }

  if (deployOpenCodeFlag) {
    const results = await deployOpenCode();
    totalDeployed += results.deployed;
    totalErrors += results.errors.length;
    console.log();
  }

  // Summary
  console.log('✨ Deployment Complete!');
  console.log(`   Total deployed: ${totalDeployed}`);
  if (totalErrors > 0) {
    console.log(`   Errors: ${totalErrors}`);
  }
  console.log();
  console.log('Deployed locations:');
  if (deployClaudeMdFlag) console.log('   └─ CLAUDE.md:       ./CLAUDE.md');
  if (deployRulesFlag) console.log('   └─ Claude Rules:    .claude/rules/*.md');
  if (deployClaude) console.log('   └─ Claude Skills:   .claude/skills/*/SKILL.md');
  if (deployAgentsFlag) console.log('   └─ Claude Agents:   .claude/agents/*.agent.md (simplified)');
  if (deployPromptsLegacy) console.log('   └─ Claude Prompts:  .claude/prompts/*.{md,yaml} (legacy)');
  if (deployCopilot) console.log('   └─ Copilot:         .github/instructions/*.instructions.md');
  if (deployOpenCodeFlag) console.log('   └─ OpenCode:        .opencode/agents/, .opencode/skills/');
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
