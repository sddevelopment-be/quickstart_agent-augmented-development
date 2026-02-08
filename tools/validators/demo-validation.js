const { PromptValidator, formatValidationResult } = require('./prompt-validator');
const path = require('path');

async function demo() {
  console.log('🚀 Prompt Validator Demo\n');
  
  // Create validator
  const validator = new PromptValidator();
  const schemaPath = path.join(__dirname, 'src/framework/schemas/prompt-schema.json');
  await validator.loadSchema(schemaPath);
  console.log('✓ Schema loaded\n');
  
  // Test 1: Valid prompt
  console.log('Test 1: Valid Prompt');
  console.log('─'.repeat(50));
  const validPrompt = {
    objective: 'Create OAuth2 authentication module with token refresh',
    deliverables: [{
      file: 'src/auth/oauth-handler.js',
      type: 'code',
      validation: 'All 20 unit tests pass with 95% coverage'
    }],
    success_criteria: [
      'OAuth2 flow completes successfully',
      'Token refresh works correctly',
      'All 20 tests pass without errors'
    ],
    constraints: {
      do: ['Use passport.js', 'Follow patterns'],
      dont: ['Don\'t modify schema', 'Don\'t change routes'],
      time_box: 60
    },
    context_files: {
      critical: [{ path: 'src/auth/controller.js', reason: 'Auth patterns' }],
      skip: ['Old logs']
    }
  };
  
  const result1 = await validator.validatePromptData(validPrompt);
  console.log(`Result: ${result1.valid ? '✅ VALID' : '❌ INVALID'}`);
  console.log(`Score: ${result1.score}/100`);
  console.log(`Errors: ${result1.errors.length}`);
  console.log(`Warnings: ${result1.warnings.length}\n`);
  
  // Test 2: Prompt with anti-patterns
  console.log('Test 2: Prompt with Anti-Patterns');
  console.log('─'.repeat(50));
  const badPrompt = {
    objective: 'Review everything in all modules',  // Scope creep
    deliverables: [{
      file: 'report',  // Missing extension
      type: 'report',
      validation: 'Check quality'  // Vague
    }],
    success_criteria: [
      'Assess completeness',  // Vague
      'Review all code',      // Vague
      'Verify quality'        // Vague
    ],
    constraints: {
      do: ['Review code', 'Check files'],
      dont: ['Don\'t break', 'Don\'t change'],
      time_box: 180  // >60 without checkpoints
    },
    context_files: {
      critical: [{ path: './local/file.js', reason: 'needed' }],  // Relative path
      skip: []
    }
  };
  
  const result2 = await validator.validatePromptData(badPrompt);
  console.log(`Result: ${result2.valid ? '✅ VALID' : '❌ INVALID'}`);
  console.log(`Score: ${result2.score}/100`);
  console.log(`Errors: ${result2.errors.length}`);
  console.log(`Warnings: ${result2.warnings.length}\n`);
  
  console.log('Anti-patterns detected:');
  result2.errors.forEach(err => {
    if (err.pattern) {
      console.log(`  • ${err.pattern}: ${err.message}`);
    }
  });
  
  console.log('\n🎉 Demo complete!');
}

demo().catch(console.error);
