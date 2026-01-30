#!/usr/bin/env node

const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const fs = require('fs');
const path = require('path');

// Create AJV instance with formats support
const ajv = new Ajv({ allErrors: true, strict: false });
addFormats(ajv);

const schemasDir = path.join(__dirname, 'work/schemas');
const schemaFiles = fs.readdirSync(schemasDir)
  .filter(f => f.endsWith('.schema.json'))
  .sort();

console.log('=== Validating All Schemas ===\n');

let passedCount = 0;
let failedCount = 0;
const results = [];

for (const file of schemaFiles) {
  const schemaPath = path.join(schemasDir, file);
  try {
    const schemaData = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
    ajv.compile(schemaData);
    console.log(`✅ ${file}`);
    passedCount++;
    results.push({ file, status: 'PASS' });
  } catch (error) {
    console.log(`❌ ${file}`);
    console.log(`   Error: ${error.message}\n`);
    failedCount++;
    results.push({ file, status: 'FAIL', error: error.message });
  }
}

console.log(`\n=== Summary ===`);
console.log(`Total: ${schemaFiles.length}`);
console.log(`Passed: ${passedCount}`);
console.log(`Failed: ${failedCount}`);

if (failedCount > 0) {
  process.exit(1);
}
