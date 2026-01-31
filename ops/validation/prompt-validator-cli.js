#!/usr/bin/env node
/**
 * Prompt Validator CLI
 * 
 * Command-line interface for validating AI agent prompt files against quality schema.
 * Supports batch validation of directories with CI-friendly output formats.
 * 
 * @module prompt-validator-cli
 * @version 1.0.0
 * @author DevOps Danny
 * @date 2026-01-30
 * 
 * Following Directives:
 * - Directive 001 (CLI & Shell Tooling): CI/CD-friendly exit codes and output
 * - Directive 018 (Traceable Decisions): Links to ADR-023
 * - Directive 021 (Locality of Change): Focused on CLI interface only
 * 
 * Related ADRs:
 * - ADR-023: Prompt Optimization Framework (Phase 2 CI/CD)
 * 
 * Usage:
 *   node prompt-validator-cli.js <directory> [options]
 *   npm run validate:prompts
 * 
 * Exit Codes:
 *   0 - All prompts valid (score >= threshold)
 *   1 - Validation failures (score < threshold)
 *   2 - CLI error (missing args, file not found, etc.)
 */

const fs = require('fs').promises;
const path = require('path');
const { PromptValidator, formatValidationResult } = require('./prompt-validator');

// Configuration
const DEFAULT_THRESHOLD = 70;
const SCHEMA_PATH = path.join(__dirname, '../../validation/schemas/prompt-schema.json');

/**
 * Parse command-line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  
  const config = {
    directories: [],
    threshold: DEFAULT_THRESHOLD,
    format: 'text', // text, json, markdown
    verbose: false,
    help: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--help' || arg === '-h') {
      config.help = true;
    } else if (arg === '--threshold' || arg === '-t') {
      config.threshold = parseInt(args[++i], 10);
    } else if (arg === '--format' || arg === '-f') {
      config.format = args[++i];
    } else if (arg === '--verbose' || arg === '-v') {
      config.verbose = true;
    } else if (!arg.startsWith('-')) {
      config.directories.push(arg);
    }
  }

  return config;
}

/**
 * Print CLI usage information
 */
function printUsage() {
  console.log(`
Prompt Validator CLI - Validate AI agent prompts against quality schema

Usage:
  node prompt-validator-cli.js <directory> [options]
  npm run validate:prompts [-- <directory>]

Arguments:
  <directory>           Directory containing .yaml prompt files
                        Can specify multiple directories

Options:
  -t, --threshold <n>   Minimum quality score to pass (default: 70)
  -f, --format <type>   Output format: text, json, markdown (default: text)
  -v, --verbose         Show detailed validation info
  -h, --help            Show this help message

Examples:
  # Validate prompts in default locations
  npm run validate:prompts

  # Validate specific directory
  node prompt-validator-cli.js docs/templates/prompts/

  # Validate with custom threshold
  node prompt-validator-cli.js docs/templates/prompts/ --threshold 80

  # Get JSON output for CI integration
  node prompt-validator-cli.js work/collaboration/ --format json

Exit Codes:
  0 - All prompts valid (score >= threshold)
  1 - Validation failures found
  2 - CLI error (invalid arguments, file not found, etc.)

Environment Variables:
  PROMPT_VALIDATOR_THRESHOLD  Override default threshold (default: 70)
  CI                          Enables CI-optimized output format
`);
}

/**
 * Find all YAML files in directory recursively
 */
async function findYamlFiles(directory) {
  const files = [];
  
  try {
    const entries = await fs.readdir(directory, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(directory, entry.name);
      
      if (entry.isDirectory()) {
        // Recurse into subdirectories
        const subFiles = await findYamlFiles(fullPath);
        files.push(...subFiles);
      } else if (entry.isFile() && /\.ya?ml$/i.test(entry.name)) {
        // Skip test fixtures (files starting with "invalid-")
        if (!entry.name.startsWith('invalid-')) {
          files.push(fullPath);
        }
      }
    }
  } catch (error) {
    if (error.code !== 'ENOENT') {
      throw error;
    }
    // Directory doesn't exist - return empty array
  }
  
  return files;
}

/**
 * Format validation results as JSON
 */
function formatAsJson(results) {
  const summary = {
    timestamp: new Date().toISOString(),
    total: results.length,
    passed: results.filter(r => r.passed).length,
    failed: results.filter(r => !r.passed).length,
    averageScore: Math.round(results.reduce((sum, r) => sum + r.result.score, 0) / results.length),
    details: results.map(r => ({
      file: r.file,
      passed: r.passed,
      score: r.result.score,
      errorCount: r.result.errors.length,
      warningCount: r.result.warnings.length,
      errors: r.result.errors,
      warnings: r.result.warnings
    }))
  };
  
  return JSON.stringify(summary, null, 2);
}

/**
 * Format validation results as Markdown (for PR comments)
 */
function formatAsMarkdown(results, threshold) {
  const passed = results.filter(r => r.passed);
  const failed = results.filter(r => !r.passed);
  const avgScore = Math.round(results.reduce((sum, r) => sum + r.result.score, 0) / results.length);
  
  let output = '## 🔍 Prompt Quality Report\n\n';
  
  // Overall status
  if (failed.length === 0) {
    output += `**Overall Status:** ✅ Pass (${passed.length}/${results.length} prompts valid)\n\n`;
  } else {
    output += `**Overall Status:** ❌ Fail (${passed.length}/${results.length} prompts valid)\n\n`;
  }
  
  // Summary
  output += '### Summary\n\n';
  output += `- **Prompts Validated:** ${results.length}\n`;
  output += `- **Passed:** ${passed.length} (${Math.round(passed.length / results.length * 100)}%)\n`;
  output += `- **Failed:** ${failed.length} (${Math.round(failed.length / results.length * 100)}%)\n`;
  output += `- **Average Quality Score:** ${avgScore}/100\n`;
  output += `- **Threshold:** ${threshold}/100\n\n`;
  
  // Details
  output += '### Details\n\n';
  
  // Show failed prompts first
  if (failed.length > 0) {
    output += '#### ❌ Failed Prompts\n\n';
    failed.forEach(r => {
      const fileName = path.basename(r.file);
      output += `##### ${fileName} (Score: ${r.result.score}/100)\n\n`;
      
      if (r.result.errors.length > 0) {
        output += '**Errors:**\n';
        r.result.errors.forEach(err => {
          output += `- **${err.path || 'root'}**: ${err.message}\n`;
          if (err.suggestion) {
            output += `  - 💡 ${err.suggestion}\n`;
          }
        });
        output += '\n';
      }
      
      if (r.result.warnings.length > 0) {
        output += '**Warnings:**\n';
        r.result.warnings.forEach(warn => {
          output += `- [${warn.type}] ${warn.message}\n`;
        });
        output += '\n';
      }
    });
  }
  
  // Show passed prompts
  if (passed.length > 0) {
    output += '#### ✅ Passed Prompts\n\n';
    passed.forEach(r => {
      const fileName = path.basename(r.file);
      output += `- **${fileName}** (Score: ${r.result.score}/100)`;
      
      if (r.result.warnings.length > 0) {
        output += ` - ${r.result.warnings.length} warning(s)`;
      }
      
      output += '\n';
    });
    output += '\n';
  }
  
  // Footer
  const duration = results.reduce((sum, r) => sum + (r.duration || 0), 0);
  output += '---\n';
  output += `*Validation took ${(duration / 1000).toFixed(2)} seconds*\n`;
  
  return output;
}

/**
 * Main CLI entry point
 */
async function main() {
  const config = parseArgs();
  
  // Show help if requested
  if (config.help) {
    printUsage();
    process.exit(0);
  }
  
  // Default directories if none specified
  if (config.directories.length === 0) {
    config.directories = [
      'docs/templates/prompts',
      'work/collaboration'
    ];
  }
  
  // Allow environment variable override
  const threshold = process.env.PROMPT_VALIDATOR_THRESHOLD 
    ? parseInt(process.env.PROMPT_VALIDATOR_THRESHOLD, 10)
    : config.threshold;
  
  // CI mode detection
  const isCI = process.env.CI === 'true';
  if (isCI && config.format === 'text') {
    config.format = 'markdown'; // Better for PR comments
  }
  
  try {
    // Initialize validator
    const validator = new PromptValidator();
    await validator.loadSchema(SCHEMA_PATH);
    
    if (config.verbose) {
      console.log(`Prompt Validator CLI v1.0.0`);
      console.log(`Schema: ${SCHEMA_PATH}`);
      console.log(`Threshold: ${threshold}`);
      console.log(`Directories: ${config.directories.join(', ')}`);
      console.log('');
    }
    
    // Find all YAML files
    const allFiles = [];
    for (const dir of config.directories) {
      const files = await findYamlFiles(dir);
      allFiles.push(...files);
    }
    
    if (allFiles.length === 0) {
      console.error('❌ No .yaml files found in specified directories');
      console.error(`Searched: ${config.directories.join(', ')}`);
      process.exit(2);
    }
    
    if (config.verbose) {
      console.log(`Found ${allFiles.length} prompt file(s)\n`);
    }
    
    // Validate each file
    const results = [];
    let hasFailures = false;
    
    for (const file of allFiles) {
      const startTime = Date.now();
      
      try {
        const result = await validator.validatePrompt(file);
        const duration = Date.now() - startTime;
        const passed = result.score >= threshold;
        
        if (!passed) {
          hasFailures = true;
        }
        
        results.push({
          file,
          result,
          passed,
          duration
        });
        
        // Show progress in text mode
        if (config.format === 'text') {
          const symbol = passed ? '✅' : '❌';
          const fileName = path.basename(file);
          console.log(`${symbol} ${fileName} (Score: ${result.score}/100)`);
          
          if (!passed || config.verbose) {
            console.log(formatValidationResult(result));
          }
        }
      } catch (error) {
        console.error(`❌ Error validating ${file}: ${error.message}`);
        hasFailures = true;
        
        results.push({
          file,
          result: {
            valid: false,
            errors: [{ type: 'error', message: error.message }],
            warnings: [],
            score: 0
          },
          passed: false,
          duration: Date.now() - startTime
        });
      }
    }
    
    // Output formatted results
    if (config.format === 'json') {
      console.log(formatAsJson(results));
    } else if (config.format === 'markdown') {
      console.log(formatAsMarkdown(results, threshold));
    } else {
      // Summary already printed in text mode
      console.log('');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log('Summary');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log(`Total: ${results.length}`);
      console.log(`Passed: ${results.filter(r => r.passed).length}`);
      console.log(`Failed: ${results.filter(r => !r.passed).length}`);
      console.log(`Average Score: ${Math.round(results.reduce((sum, r) => sum + r.result.score, 0) / results.length)}/100`);
      console.log(`Threshold: ${threshold}/100`);
      console.log('');
    }
    
    // Exit with appropriate code
    if (hasFailures) {
      if (config.format === 'text') {
        console.error(`❌ Validation failed - ${results.filter(r => !r.passed).length} prompt(s) below threshold`);
      }
      process.exit(1);
    } else {
      if (config.format === 'text') {
        console.log(`✅ All prompts passed validation`);
      }
      process.exit(0);
    }
    
  } catch (error) {
    console.error(`❌ Fatal error: ${error.message}`);
    if (config.verbose) {
      console.error(error.stack);
    }
    process.exit(2);
  }
}

// Run CLI if executed directly
if (require.main === module) {
  main().catch(error => {
    console.error(`❌ Unhandled error: ${error.message}`);
    process.exit(2);
  });
}

// Export for testing
module.exports = {
  parseArgs,
  findYamlFiles,
  formatAsJson,
  formatAsMarkdown
};
