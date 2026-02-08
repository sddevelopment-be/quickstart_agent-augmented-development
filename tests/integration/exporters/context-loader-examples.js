/**
 * Context Loader Usage Example
 * 
 * This example demonstrates how to use the ContextLoader
 * for progressive context loading with token budget management.
 * 
 * Task: 2026-01-30T1643-adr023-phase3-context-loader
 */

const ContextLoader = require('../../ops/utils/context-loader');
const path = require('path');

// Example 1: Basic Usage
async function basicExample() {
  console.log('\n=== Example 1: Basic Usage ===\n');
  
  const loader = new ContextLoader(20000); // 20K token budget
  
  const fileList = {
    critical: [
      { 
        path: path.join(__dirname, '../../package.json'), 
        reason: 'Package configuration' 
      }
    ],
    supporting: [
      { 
        path: path.join(__dirname, '../../README.md'), 
        reason: 'Project documentation' 
      }
    ],
    skip: ['node_modules', 'coverage', 'build artifacts']
  };
  
  try {
    const result = await loader.loadWithBudget(fileList);
    
    console.log('✓ Files loaded:', result.files.length);
    console.log('✓ Total tokens:', result.totalTokens);
    console.log('✓ Budget utilization:', result.utilizationPct);
    console.log('✓ Within budget:', result.withinBudget);
    
    if (result.warnings.length > 0) {
      console.log('\n⚠️  Warnings:');
      result.warnings.forEach(w => console.log('  -', w));
    }
    
    if (result.skipped.length > 0) {
      console.log('\n⏭  Skipped files:', result.skipped.length);
    }
    
  } catch (error) {
    console.error('✗ Error:', error.message);
  } finally {
    loader.free(); // Clean up resources
  }
}

// Example 2: Token Estimation
function tokenEstimationExample() {
  console.log('\n=== Example 2: Token Estimation ===\n');
  
  const loader = new ContextLoader();
  
  const texts = [
    'Hello, world!',
    'The quick brown fox jumps over the lazy dog.',
    'function example() { return 42; }'
  ];
  
  texts.forEach(text => {
    const tokens = loader.estimateTokens(text);
    console.log(`"${text}"`);
    console.log(`  → ${tokens} tokens\n`);
  });
  
  loader.free();
}

// Example 3: With Truncation
async function truncationExample() {
  console.log('\n=== Example 3: Truncation Enabled ===\n');
  
  const loader = new ContextLoader(1000); // Very small budget
  
  const fileList = {
    critical: [
      { 
        path: path.join(__dirname, '../../README.md'), 
        reason: 'Large critical file' 
      }
    ],
    supporting: [],
    skip: []
  };
  
  try {
    const result = await loader.loadWithBudget(fileList, { 
      truncateCritical: true 
    });
    
    console.log('✓ Files loaded:', result.files.length);
    console.log('✓ File truncated:', result.files[0].truncated);
    console.log('✓ Tokens after truncation:', result.files[0].tokens);
    console.log('✓ Budget:', result.budget);
    
  } catch (error) {
    console.error('✗ Error:', error.message);
  } finally {
    loader.free();
  }
}

// Example 4: Budget Recommendations
function recommendationsExample() {
  console.log('\n=== Example 4: Budget Recommendations ===\n');
  
  const loader = new ContextLoader();
  const recommendations = loader.getBudgetRecommendations();
  
  console.log('Recommended token budgets by task type:');
  console.log('  Simple tasks:       ', recommendations.simple, 'tokens');
  console.log('  Medium tasks:       ', recommendations.medium, 'tokens');
  console.log('  Complex tasks:      ', recommendations.complex, 'tokens');
  console.log('  Architecture tasks: ', recommendations.architecture, 'tokens');
  
  loader.free();
}

// Example 5: Load Report
async function loadReportExample() {
  console.log('\n=== Example 5: Comprehensive Load Report ===\n');
  
  const loader = new ContextLoader(20000);
  
  const fileList = {
    critical: [
      { 
        path: path.join(__dirname, '../../package.json'), 
        reason: 'Package configuration' 
      }
    ],
    supporting: [
      { 
        path: path.join(__dirname, '../../jest.config.js'), 
        reason: 'Test configuration' 
      }
    ],
    skip: ['logs', 'temp files', 'caches']
  };
  
  try {
    await loader.loadWithBudget(fileList);
    const report = loader.generateLoadReport();
    
    console.log('Load Report:');
    console.log('─────────────────────────────────────');
    console.log('Files loaded:      ', report.files.length);
    console.log('Total tokens:      ', report.totalTokens);
    console.log('Budget:            ', report.budget);
    console.log('Utilization:       ', report.utilizationPct);
    console.log('Within budget:     ', report.withinBudget);
    console.log('Files skipped:     ', report.skipped.length);
    console.log('Skip list items:   ', report.skipList.length);
    console.log('Warnings:          ', report.warnings.length);
    
    console.log('\nFile Details:');
    report.files.forEach((file, idx) => {
      console.log(`  ${idx + 1}. ${path.basename(file.path)}`);
      console.log(`     Tokens: ${file.tokens}, Truncated: ${file.truncated}`);
      console.log(`     Reason: ${file.reason}`);
    });
    
  } catch (error) {
    console.error('✗ Error:', error.message);
  } finally {
    loader.free();
  }
}

// Run all examples
async function main() {
  console.log('\n╔═══════════════════════════════════════════════════════════╗');
  console.log('║                                                           ║');
  console.log('║         Context Loader Usage Examples                     ║');
  console.log('║         ADR-023 Phase 3 Implementation                    ║');
  console.log('║                                                           ║');
  console.log('╚═══════════════════════════════════════════════════════════╝');
  
  await basicExample();
  tokenEstimationExample();
  await truncationExample();
  recommendationsExample();
  await loadReportExample();
  
  console.log('\n✓ All examples completed successfully!\n');
}

// Run examples if executed directly
if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = {
  basicExample,
  tokenEstimationExample,
  truncationExample,
  recommendationsExample,
  loadReportExample
};
