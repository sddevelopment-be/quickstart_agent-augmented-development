#!/usr/bin/env node
/**
 * Skills Deployment Script
 *
 * Deploys exported skills from dist/ to tool-specific locations:
 * - Claude Code: .claude/skills/<name>/SKILL.md
 * - GitHub Copilot: .github/instructions/<name>.instructions.md
 * - OpenCode: .opencode/agents/, .opencode/skills/
 *
 * Usage:
 *   node ops/deploy-skills.js [--claude] [--copilot] [--opencode] [--all]
 *   npm run deploy:skills
 *
 * Prerequisites:
 *   Run `npm run export:all` first to generate dist/ files
 */

const fs = require('fs').promises;
const path = require('path');

// Source directories (from export)
const DIST_DIR = path.join(__dirname, '..', 'dist');
const SKILLS_DIR = path.join(DIST_DIR, 'skills');
const OPENCODE_DIR = path.join(DIST_DIR, 'opencode');

// Target directories (tool-specific)
const CLAUDE_SKILLS_DIR = path.join(__dirname, '..', '.claude', 'skills');
const COPILOT_INSTRUCTIONS_DIR = path.join(__dirname, '..', '.github', 'instructions');
const OPENCODE_TARGET_DIR = path.join(__dirname, '..', '.opencode');

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
 * Main deployment function
 */
async function main() {
  const args = process.argv.slice(2);
  const deployAll = args.includes('--all') || args.length === 0;
  const deployClaude = deployAll || args.includes('--claude');
  const deployCopilot = deployAll || args.includes('--copilot');
  const deployOpenCodeFlag = deployAll || args.includes('--opencode');

  console.log('🚀 Deploying skills to tool-specific locations...\n');

  let totalDeployed = 0;
  let totalErrors = 0;

  // Check if dist/ exists
  try {
    await fs.access(DIST_DIR);
  } catch {
    console.error('❌ dist/ directory not found.');
    console.error('   Run `npm run export:all` first to generate exports.');
    process.exit(1);
  }

  if (deployClaude) {
    const results = await deployClaudeSkills();
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
  if (deployClaude) console.log('   └─ Claude Code:  .claude/skills/*/SKILL.md');
  if (deployCopilot) console.log('   └─ Copilot:      .github/instructions/*.instructions.md');
  if (deployOpenCodeFlag) console.log('   └─ OpenCode:     .opencode/agents/, .opencode/skills/');
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
