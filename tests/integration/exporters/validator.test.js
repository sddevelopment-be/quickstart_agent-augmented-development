/**
 * Validator Test Suite
 * 
 * Test-Driven Development (TDD) following Directive 017
 * Acceptance Test-Driven Development (ATDD) following Directive 016
 * 
 * Test Structure:
 * 1. Acceptance Tests - End-to-end validation scenarios
 * 2. Unit Tests - Core validation functions
 * 3. Integration Tests - File validation and schema loading
 * 4. Edge Cases - Error handling and boundary conditions
 */

const fs = require('fs').promises;
const path = require('path');
const { Validator, validate, validateFile, formatErrors } = require('../../ops/exporters/validator');

// ============================================================================
// ACCEPTANCE TESTS (Write First - Directive 016)
// ============================================================================

describe('Validator Acceptance Tests', () => {
  
  describe('Basic Validation', () => {
    it('validates correct data against inline schema', () => {
      const data = { 
        name: 'test-agent', 
        version: '1.0.0',
        description: 'Test agent description'
      };
      
      const schema = {
        type: 'object',
        properties: {
          name: { type: 'string' },
          version: { type: 'string' },
          description: { type: 'string' }
        },
        required: ['name', 'version', 'description']
      };
      
      const result = validate(data, schema);
      
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
    
    it('reports validation errors with clear messages', () => {
      const data = { 
        name: 'test-agent', 
        version: 123,  // Should be string
        description: 'Test'
      };
      
      const schema = {
        type: 'object',
        properties: {
          name: { type: 'string' },
          version: { type: 'string' },
          description: { type: 'string' }
        },
        required: ['name', 'version', 'description']
      };
      
      const result = validate(data, schema);
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
      expect(result.errors[0].path).toBe('version');
      expect(result.errors[0].message).toContain('string');
    });
    
    it('lists all validation errors, not just first', () => {
      const data = { 
        name: 123,      // Should be string
        version: 456,   // Should be string
        // description missing
      };
      
      const schema = {
        type: 'object',
        properties: {
          name: { type: 'string' },
          version: { type: 'string' },
          description: { type: 'string' }
        },
        required: ['name', 'version', 'description']
      };
      
      const result = validate(data, schema);
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThanOrEqual(3);
    });
  });
  
  describe('File Validation', () => {
    const testDir = path.join(__dirname, '../fixtures/validator');
    
    it('validates JSON file against schema', async () => {
      const testFile = path.join(testDir, 'valid.json');
      
      const schema = {
        type: 'object',
        properties: {
          name: { type: 'string' },
          version: { type: 'string' }
        },
        required: ['name', 'version']
      };
      
      const result = await validateFile(testFile, schema);
      
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
    
    it('validates YAML file against schema', async () => {
      const testFile = path.join(testDir, 'valid.yaml');
      
      const schema = {
        type: 'object',
        properties: {
          name: { type: 'string' },
          version: { type: 'string' }
        },
        required: ['name', 'version']
      };
      
      const result = await validateFile(testFile, schema);
      
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
    
    it('reports file validation errors', async () => {
      const testFile = path.join(testDir, 'invalid.json');
      
      const schema = {
        type: 'object',
        properties: {
          name: { type: 'string' },
          version: { type: 'string' }
        },
        required: ['name', 'version']
      };
      
      const result = await validateFile(testFile, schema);
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });
  });
  
  describe('Real Schema Validation', () => {
    const schemasDir = path.join(__dirname, '../../work/schemas');
    const examplesDir = path.join(schemasDir, 'examples');
    
    it('validates architect-alphonso example against schema', async () => {
      const schemaPath = path.join(schemasDir, 'architect-alphonso.input.schema.json');
      const examplesPath = path.join(examplesDir, 'architect-alphonso.examples.json');
      
      const schemaContent = await fs.readFile(schemaPath, 'utf8');
      const schema = JSON.parse(schemaContent);
      
      const examplesContent = await fs.readFile(examplesPath, 'utf8');
      const examples = JSON.parse(examplesContent);
      
      // Validate first example input
      const result = validate(examples.examples[0].input, schema);
      
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
    
    it('validates IR fixture against hypothetical schema', async () => {
      const irPath = path.join(examplesDir, 'ir/architect-alphonso.ir.json');
      
      const irContent = await fs.readFile(irPath, 'utf8');
      const irData = JSON.parse(irContent);
      
      // Simple schema to validate IR structure
      const irSchema = {
        type: 'object',
        properties: {
          ir_version: { type: 'string' },
          frontmatter: { type: 'object' },
          content: { type: 'object' },
          relationships: { type: 'object' },
          metadata: { type: 'object' }
        },
        required: ['ir_version', 'frontmatter', 'content', 'metadata']
      };
      
      const result = validate(irData, irSchema);
      
      expect(result.valid).toBe(true);
    });
  });
  
  describe('Schema Loading', () => {
    it('loads schema from file system', async () => {
      const schemaPath = path.join(__dirname, '../../work/schemas/architect-alphonso.input.schema.json');
      
      const validator = new Validator();
      const schema = await validator.loadSchema(schemaPath);
      
      expect(schema).toBeDefined();
      expect(schema.$schema).toBe('http://json-schema.org/draft-07/schema#');
      expect(schema.title).toBe('Architect Alphonso Input Schema');
    });
    
    it('validates file against schema file', async () => {
      const schemaPath = path.join(__dirname, '../../work/schemas/architect-alphonso.input.schema.json');
      const dataPath = path.join(__dirname, '../../work/schemas/examples/architect-alphonso.examples.json');
      
      const result = await validateFile(dataPath, schemaPath);
      
      // This validates the examples file structure, first example should be valid
      expect(result).toBeDefined();
    });
  });
});

// ============================================================================
// UNIT TESTS - Core Validator Functions
// ============================================================================

describe('Validator Core Functions', () => {
  
  describe('Validator Class', () => {
    it('creates validator instance', () => {
      const validator = new Validator();
      expect(validator).toBeDefined();
      expect(validator.ajv).toBeDefined();
    });
    
    it('validates simple object', () => {
      const validator = new Validator();
      const schema = {
        type: 'object',
        properties: {
          name: { type: 'string' }
        },
        required: ['name']
      };
      
      const result = validator.validate({ name: 'test' }, schema);
      
      expect(result.valid).toBe(true);
      expect(result.errors).toEqual([]);
    });
    
    it('detects type mismatch', () => {
      const validator = new Validator();
      const schema = {
        type: 'object',
        properties: {
          age: { type: 'number' }
        }
      };
      
      const result = validator.validate({ age: 'not a number' }, schema);
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });
    
    it('detects missing required field', () => {
      const validator = new Validator();
      const schema = {
        type: 'object',
        properties: {
          name: { type: 'string' }
        },
        required: ['name']
      };
      
      const result = validator.validate({}, schema);
      
      expect(result.valid).toBe(false);
      expect(result.errors[0].path).toBe('name');
      expect(result.errors[0].message).toContain('required');
    });
  });
  
  describe('Error Formatting', () => {
    it('formats error with path', () => {
      const validator = new Validator();
      const schema = {
        type: 'object',
        properties: {
          user: {
            type: 'object',
            properties: {
              name: { type: 'string' }
            },
            required: ['name']
          }
        }
      };
      
      const result = validator.validate({ user: {} }, schema);
      
      expect(result.valid).toBe(false);
      expect(result.errors[0].path).toBe('user');
    });
    
    it('formats errors with clear messages', () => {
      const validator = new Validator();
      const schema = {
        type: 'object',
        properties: {
          count: { type: 'number', minimum: 0, maximum: 100 }
        }
      };
      
      const result = validator.validate({ count: 150 }, schema);
      
      expect(result.valid).toBe(false);
      expect(result.errors[0].path).toBe('count');
      expect(result.errors[0].message).toContain('<=');
    });
  });
  
  describe('Format Validation', () => {
    it('validates email format', () => {
      const validator = new Validator();
      const schema = {
        type: 'object',
        properties: {
          email: { type: 'string', format: 'email' }
        }
      };
      
      const validResult = validator.validate({ email: 'test@example.com' }, schema);
      expect(validResult.valid).toBe(true);
      
      const invalidResult = validator.validate({ email: 'not-an-email' }, schema);
      expect(invalidResult.valid).toBe(false);
    });
    
    it('validates date-time format', () => {
      const validator = new Validator();
      const schema = {
        type: 'object',
        properties: {
          timestamp: { type: 'string', format: 'date-time' }
        }
      };
      
      const validResult = validator.validate({ timestamp: '2026-01-29T18:00:00Z' }, schema);
      expect(validResult.valid).toBe(true);
      
      const invalidResult = validator.validate({ timestamp: 'not-a-date' }, schema);
      expect(invalidResult.valid).toBe(false);
    });
  });
});

// ============================================================================
// INTEGRATION TESTS - File Operations
// ============================================================================

describe('File Validation Integration', () => {
  
  describe('JSON File Loading', () => {
    it('reads and parses JSON file', async () => {
      const testFile = path.join(__dirname, '../../work/schemas/examples/architect-alphonso.examples.json');
      
      const content = await fs.readFile(testFile, 'utf8');
      const data = JSON.parse(content);
      
      expect(data.examples).toBeDefined();
      expect(Array.isArray(data.examples)).toBe(true);
    });
  });
  
  describe('YAML File Loading', () => {
    it('reads and parses YAML file', async () => {
      const yaml = require('js-yaml');
      
      // Create test data
      const yamlContent = 'name: test\nversion: 1.0.0';
      const data = yaml.load(yamlContent);
      
      expect(data.name).toBe('test');
      expect(data.version).toBe('1.0.0');
    });
  });
});

// ============================================================================
// EDGE CASES AND ERROR HANDLING
// ============================================================================

describe('Validator Edge Cases', () => {
  
  describe('Error Handling', () => {
    it('handles invalid schema gracefully', () => {
      const validator = new Validator();
      const invalidSchema = {
        type: 'invalid-type'
      };
      
      expect(() => {
        validator.validate({ name: 'test' }, invalidSchema);
      }).toThrow();
    });
    
    it('handles non-existent file', async () => {
      const schema = { type: 'object' };
      
      await expect(validateFile('/non/existent/file.json', schema)).rejects.toThrow();
    });
    
    it('handles malformed JSON file', async () => {
      const testDir = path.join(__dirname, '../fixtures/validator');
      const testFile = path.join(testDir, 'malformed.json');
      const schema = { type: 'object' };
      
      await expect(validateFile(testFile, schema)).rejects.toThrow();
    });
  });
  
  describe('Empty and Null Values', () => {
    it('validates empty object', () => {
      const validator = new Validator();
      const schema = { type: 'object' };
      
      const result = validator.validate({}, schema);
      expect(result.valid).toBe(true);
    });
    
    it('validates null value', () => {
      const validator = new Validator();
      const schema = { type: 'null' };
      
      const result = validator.validate(null, schema);
      expect(result.valid).toBe(true);
    });
    
    it('rejects null when object expected', () => {
      const validator = new Validator();
      const schema = { type: 'object' };
      
      const result = validator.validate(null, schema);
      expect(result.valid).toBe(false);
    });
  });
});

// ============================================================================
// EXTENSIBILITY TESTS
// ============================================================================

describe('Validator Extensibility', () => {
  
  describe('Custom Validators', () => {
    it('allows adding custom validator function', () => {
      const validator = new Validator();
      
      const customValidator = (data) => {
        if (data.name && data.name.includes('invalid')) {
          return {
            valid: false,
            errors: [{
              path: 'name',
              message: 'Name cannot contain "invalid"',
              keyword: 'custom'
            }]
          };
        }
        return { valid: true, errors: [] };
      };
      
      validator.addCustomValidator(customValidator);
      
      expect(validator.customValidators).toHaveLength(1);
    });
    
    it('runs custom validators alongside schema validation', () => {
      const validator = new Validator();
      
      const customValidator = (data) => {
        if (data.name && data.name === 'reserved') {
          return {
            valid: false,
            errors: [{
              path: 'name',
              message: 'Name "reserved" is not allowed',
              keyword: 'custom'
            }]
          };
        }
        return { valid: true, errors: [] };
      };
      
      validator.addCustomValidator(customValidator);
      
      const schema = {
        type: 'object',
        properties: {
          name: { type: 'string' }
        }
      };
      
      const result = validator.validate({ name: 'reserved' }, schema);
      
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.message.includes('reserved'))).toBe(true);
    });
  });
  
  describe('Format Errors Function', () => {
    it('formats errors with file name', () => {
      const errors = [
        { path: 'name', message: 'must be string', expected: 'string', actual: 123 }
      ];
      
      const formatted = formatErrors(errors, 'test.json');
      
      expect(formatted).toContain('test.json');
      expect(formatted).toContain('❌');
      expect(formatted).toContain('name');
      expect(formatted).toContain('string');
    });
    
    it('formats errors without file name', () => {
      const errors = [
        { path: 'age', message: 'must be number' }
      ];
      
      const formatted = formatErrors(errors);
      
      expect(formatted).toContain('❌');
      expect(formatted).toContain('age');
    });
    
    it('returns success message for empty errors', () => {
      const formatted = formatErrors([]);
      
      expect(formatted).toContain('✅');
      expect(formatted).toContain('passed');
    });
    
    it('handles errors with root path', () => {
      const errors = [
        { path: '', message: 'invalid root', expected: 'object' }
      ];
      
      const formatted = formatErrors(errors);
      
      expect(formatted).toContain('(root)');
    });
  });
});

// ============================================================================
// ADDITIONAL COVERAGE TESTS
// ============================================================================

describe('Validator Additional Coverage', () => {
  
  describe('Error Formatting Edge Cases', () => {
    it('formats enum validation errors', () => {
      const validator = new Validator();
      const schema = {
        type: 'object',
        properties: {
          status: { type: 'string', enum: ['active', 'inactive', 'pending'] }
        }
      };
      
      const result = validator.validate({ status: 'unknown' }, schema);
      
      expect(result.valid).toBe(false);
      expect(result.errors[0].path).toBe('status');
    });
    
    it('formats minimum/maximum validation errors', () => {
      const validator = new Validator();
      const schema = {
        type: 'object',
        properties: {
          age: { type: 'number', minimum: 0 }
        }
      };
      
      const result = validator.validate({ age: -5 }, schema);
      
      expect(result.valid).toBe(false);
      expect(result.errors[0].expected).toContain('minimum');
    });
  });
  
  describe('Schema Cache', () => {
    it('caches loaded schemas', async () => {
      const validator = new Validator();
      const schemaPath = path.join(__dirname, '../../work/schemas/architect-alphonso.input.schema.json');
      
      // Load once
      const schema1 = await validator.loadSchema(schemaPath);
      
      // Load again - should use cache
      const schema2 = await validator.loadSchema(schemaPath);
      
      expect(schema1).toBe(schema2); // Same object reference
      expect(validator.schemaCache.size).toBe(1);
    });
  });
  
  describe('File Extension Handling', () => {
    it('validates .yml extension', async () => {
      const testFile = path.join(__dirname, '../fixtures/validator/valid.yaml');
      const schema = {
        type: 'object',
        properties: {
          name: { type: 'string' },
          version: { type: 'string' }
        }
      };
      
      // Create a .yml file
      await fs.writeFile(testFile.replace('.yaml', '.yml'), 'name: test\nversion: "1.0.0"');
      
      const result = await validateFile(testFile.replace('.yaml', '.yml'), schema);
      
      expect(result.valid).toBe(true);
      
      // Cleanup
      await fs.unlink(testFile.replace('.yaml', '.yml'));
    });
  });
});
