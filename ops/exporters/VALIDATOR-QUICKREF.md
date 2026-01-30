# Base Validator - Quick Reference

## Installation

```bash
npm install ajv ajv-formats
```

## Basic Usage

```javascript
const { validate, validateFile, Validator } = require('./tools/exporters/validator');
```

## Validate Data

```javascript
const result = validate(data, schema);

if (result.valid) {
  console.log('✅ Valid!');
} else {
  result.errors.forEach(err => {
    console.error(`❌ ${err.path}: ${err.message}`);
  });
}
```

## Validate File

```javascript
// JSON file
const result = await validateFile('data.json', schema);

// YAML file
const result = await validateFile('data.yaml', schema);

// With schema file
const result = await validateFile('data.json', 'schema.json');
```

## Custom Validator

```javascript
const validator = new Validator();

validator.addCustomValidator((data) => {
  if (data.name === 'forbidden') {
    return {
      valid: false,
      errors: [{
        path: 'name',
        message: 'Name is forbidden',
        keyword: 'custom'
      }]
    };
  }
  return { valid: true, errors: [] };
});

const result = validator.validate(data, schema);
```

## Format Errors

```javascript
const { formatErrors } = require('./tools/exporters/validator');

const formatted = formatErrors(result.errors, 'myfile.json');
console.log(formatted);

// Output:
// ❌ Validation failed for myfile.json
//
// Error 1: version
//   Expected: string
//   Actual: number (123)
//   Message: must be string
```

## ValidationResult

```typescript
{
  valid: boolean,
  errors: [
    {
      path: string,        // 'user.email'
      message: string,     // 'must be string'
      keyword: string,     // 'type'
      expected?: any,      // 'string'
      actual?: any         // 123
    }
  ]
}
```

## Supported Formats

- email
- date-time
- date
- time
- uri
- uuid
- ipv4
- ipv6
- hostname

## Run Tests

```bash
# All tests
npx jest tests/unit/validator.test.js

# With coverage
npx jest tests/unit/validator.test.js --coverage

# Manual validation
node tools/exporters/test-validator.js
```

## Files

- `tools/exporters/validator.js` - Production code
- `tests/unit/validator.test.js` - Test suite
- `tools/exporters/README.md` - Full documentation
- `tools/exporters/test-validator.js` - Manual tests

## Coverage

- Statements: 94.73%
- Branches: 92.15%
- Functions: 100%
- Tests: 36/36 passing

## Next Steps

See full documentation in `tools/exporters/README.md`
