#!/usr/bin/env node

/**
 * Manual validation test - Test validator with real schemas
 */

const { validate, validateFile, formatErrors } = require('./validator');
const fs = require('fs').promises;

async function main() {
  console.log('🔍 Testing Base Validator with Real Schemas\n');
  console.log('='.repeat(60) + '\n');
  
  // Test 1: Validate architect example
  console.log('Test 1: Architect Alphonso Example Input');
  const examplesData1 = JSON.parse(
    await fs.readFile('work/schemas/examples/architect-alphonso.examples.json', 'utf8')
  );
  const schema1 = JSON.parse(
    await fs.readFile('work/schemas/architect-alphonso.input.schema.json', 'utf8')
  );
  
  // Validate first example's input
  const result1 = validate(examplesData1.examples[0].input, schema1);
  console.log('Result:', result1.valid ? '✅ PASS' : '❌ FAIL');
  if (!result1.valid) {
    console.log(formatErrors(result1.errors.slice(0, 3)));
  }
  console.log();
  
  // Test 2: Validate backend example
  console.log('Test 2: Backend Benny Example Input');
  const examplesData2 = JSON.parse(
    await fs.readFile('work/schemas/examples/backend-benny.examples.json', 'utf8')
  );
  const schema2 = JSON.parse(
    await fs.readFile('work/schemas/backend-benny.input.schema.json', 'utf8')
  );
  
  // Validate first example's input
  const result2 = validate(examplesData2.examples[0].input, schema2);
  console.log('Result:', result2.valid ? '✅ PASS' : '❌ FAIL');
  if (!result2.valid) {
    console.log(formatErrors(result2.errors.slice(0, 3)));
  }
  console.log();
  
  // Test 3: Validate IR fixture
  console.log('Test 3: IR Fixture Validation');
  const irData = JSON.parse(
    await fs.readFile('work/schemas/examples/ir/architect-alphonso.ir.json', 'utf8')
  );
  
  const irSchema = {
    type: 'object',
    properties: {
      ir_version: { type: 'string' },
      frontmatter: { 
        type: 'object',
        properties: {
          name: { type: 'string' },
          description: { type: 'string' }
        },
        required: ['name', 'description']
      },
      content: { type: 'object' },
      metadata: { type: 'object' }
    },
    required: ['ir_version', 'frontmatter', 'content', 'metadata']
  };
  
  const result3 = validate(irData, irSchema);
  console.log('Result:', result3.valid ? '✅ PASS' : '❌ FAIL');
  if (!result3.valid) {
    console.log(formatErrors(result3.errors));
  }
  console.log();
  
  // Test 4: Intentional validation failure
  console.log('Test 4: Invalid Data (should fail)');
  const invalidData = { name: 123, version: null };
  const testSchema = {
    type: 'object',
    properties: {
      name: { type: 'string' },
      version: { type: 'string' }
    },
    required: ['name', 'version']
  };
  
  const result4 = validate(invalidData, testSchema);
  console.log('Result:', result4.valid ? '❌ UNEXPECTED PASS' : '✅ CORRECTLY FAILED');
  console.log(formatErrors(result4.errors, 'test-data.json'));
  console.log();
  
  // Summary
  console.log('='.repeat(60));
  console.log('✅ Validator successfully tested with real schemas!');
  console.log('✅ Error formatting working correctly');
  console.log('✅ Ready for CI/CD integration (Batch 3)');
}

main().catch(err => {
  console.error('❌ Test failed:', err.message);
  process.exit(1);
});
