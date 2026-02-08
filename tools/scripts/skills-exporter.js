#!/usr/bin/env node
/**
 * Skills Exporter CLI
 *
 * Exports prompt templates and approaches as reusable skills for
 * Claude Code, GitHub Copilot, and OpenCode formats.
 *
 * Usage:
 *   node ops/skills-exporter.js [--prompts] [--approaches] [--all]
 *
 * Output:
 *   dist/skills/
 *     ├── claude-code/     # Claude Code skill definitions
 *     ├── copilot/         # GitHub Copilot skills
 *     ├── opencode/        # OpenCode skill definitions
 *     └── *-manifest.json  # Export manifests
 */

const path = require('path');
const { exportPromptTemplates } = require('./exporters/prompt-template-exporter');
const { exportApproaches } = require('./exporters/approach-exporter');

const PROMPTS_DIR = path.join(__dirname, '..', 'docs', 'templates', 'prompts');
const APPROACHES_DIR = path.join(__dirname, '..', '.github', 'agents', 'approaches');
const OUTPUT_DIR = path.join(__dirname, '..', 'dist', 'skills');

async function main() {
  const args = process.argv.slice(2);
  const exportAll = args.includes('--all') || args.length === 0;
  const exportPrompts = exportAll || args.includes('--prompts');
  const exportApproachesFlag = exportAll || args.includes('--approaches');

  console.log('🚀 Starting Skills Export...\n');

  let totalExported = 0;
  let totalErrors = 0;

  // Export prompt templates
  if (exportPrompts) {
    console.log('📝 Exporting Prompt Templates...');
    console.log(`   Source: ${PROMPTS_DIR}`);

    try {
      const promptResults = await exportPromptTemplates(PROMPTS_DIR, OUTPUT_DIR);

      console.log(`   ✅ Exported ${promptResults.exported.length} prompt templates`);
      promptResults.exported.forEach(e => {
        console.log(`      └─ ${e.id}`);
      });

      if (promptResults.errors.length > 0) {
        console.log(`   ⚠️  ${promptResults.errors.length} errors:`);
        promptResults.errors.forEach(e => {
          console.log(`      └─ ${e.id}: ${e.error}`);
        });
      }

      totalExported += promptResults.exported.length;
      totalErrors += promptResults.errors.length;
    } catch (error) {
      console.error(`   ❌ Failed to export prompts: ${error.message}`);
      totalErrors++;
    }

    console.log();
  }

  // Export approaches
  if (exportApproachesFlag) {
    console.log('📚 Exporting Approaches...');
    console.log(`   Source: ${APPROACHES_DIR}`);

    try {
      const approachResults = await exportApproaches(APPROACHES_DIR, OUTPUT_DIR);

      console.log(`   ✅ Exported ${approachResults.exported.length} approaches`);
      approachResults.exported.forEach(e => {
        console.log(`      └─ ${e.id}: ${e.title}`);
      });

      if (approachResults.errors.length > 0) {
        console.log(`   ⚠️  ${approachResults.errors.length} errors:`);
        approachResults.errors.forEach(e => {
          console.log(`      └─ ${e.id}: ${e.error}`);
        });
      }

      totalExported += approachResults.exported.length;
      totalErrors += approachResults.errors.length;
    } catch (error) {
      console.error(`   ❌ Failed to export approaches: ${error.message}`);
      totalErrors++;
    }

    console.log();
  }

  // Summary
  console.log('✨ Skills Export Complete!');
  console.log(`📦 Output directory: ${OUTPUT_DIR}`);
  console.log(`   Total skills exported: ${totalExported}`);
  if (totalErrors > 0) {
    console.log(`   Errors: ${totalErrors}`);
  }
  console.log();
  console.log('Generated formats:');
  console.log('   └─ Claude Code:  dist/skills/claude-code/*.json');
  console.log('   └─ Copilot:      dist/skills/copilot/*.json');
  console.log('   └─ OpenCode:     dist/skills/opencode/*.json');
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
