/**
 * Base Validator Framework
 * 
 * Validates JSON/YAML files against JSON Schema specifications.
 * Provides clear error messages and extensibility for custom validators.
 * 
 * @module tools/exporters/validator
 * @version 1.0.0
 * @author Backend Benny
 * @date 2026-01-29
 * 
 * Directives:
 * - Directive 016: ATDD - Acceptance tests written first
 * - Directive 017: TDD - Red-Green-Refactor cycle
 * - Directive 021: Locality of Change - Focus on validation only
 */

const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const fs = require('fs').promises;
const yaml = require('js-yaml');
const path = require('path');

/**
 * Validation result object
 * @typedef {Object} ValidationResult
 * @property {boolean} valid - True if validation passed
 * @property {ValidationError[]} errors - Array of validation errors
 */

/**
 * Validation error object
 * @typedef {Object} ValidationError
 * @property {string} path - JSON path to invalid field (e.g., 'user.name')
 * @property {string} message - Human-readable error message
 * @property {string} keyword - JSON Schema keyword that failed
 * @property {*} [expected] - Expected type or value
 * @property {*} [actual] - Actual value that failed validation
 */

/**
 * Validator class for JSON Schema validation
 * 
 * @class Validator
 * @example
 * const validator = new Validator();
 * const result = validator.validate(data, schema);
 * if (!result.valid) {
 *   console.error(result.errors);
 * }
 */
class Validator {
  /**
   * Create a new Validator instance
   * 
   * @constructor
   */
  constructor() {
    // Initialize AJV with full error reporting
    this.ajv = new Ajv({ 
      allErrors: true,        // Report all errors, not just first
      verbose: true,          // Include data in errors
      strict: false           // Allow unknown keywords for flexibility
    });
    
    // Add format validators (email, date-time, uri, etc.)
    addFormats(this.ajv);
    
    // Storage for custom validators
    this.customValidators = [];
    
    // Schema cache for performance
    this.schemaCache = new Map();
  }
  
  /**
   * Validate data against a JSON Schema
   * 
   * @param {*} data - Data to validate
   * @param {Object} schema - JSON Schema object
   * @returns {ValidationResult} Validation result with errors if any
   * 
   * @example
   * const result = validator.validate({ name: 'test' }, {
   *   type: 'object',
   *   properties: { name: { type: 'string' } }
   * });
   */
  validate(data, schema) {
    // Compile and validate with JSON Schema
    const validate = this.ajv.compile(schema);
    const valid = validate(data);
    
    // Format schema validation errors
    const schemaErrors = valid ? [] : this.formatErrors(validate.errors);
    
    // Run custom validators
    const customResults = this.customValidators.map(fn => fn(data));
    const customErrors = customResults.flatMap(r => r.errors || []);
    
    // Combine results
    const allErrors = [...schemaErrors, ...customErrors];
    const allValid = valid && customResults.every(r => r.valid);
    
    return {
      valid: allValid,
      errors: allErrors
    };
  }
  
  /**
   * Format AJV errors into human-readable format
   * 
   * @param {Array} ajvErrors - Raw AJV error objects
   * @returns {ValidationError[]} Formatted error objects
   * @private
   */
  formatErrors(ajvErrors) {
    if (!ajvErrors || ajvErrors.length === 0) {
      return [];
    }
    
    return ajvErrors.map(err => {
      // Convert instancePath from AJV format (/path/to/field) to dot notation (path.to.field)
      const path = err.instancePath
        ? err.instancePath.substring(1).replace(/\//g, '.')
        : '';
      
      // Build formatted error
      const formattedError = {
        path: path || (err.params.missingProperty || ''),
        message: err.message || 'Validation failed',
        keyword: err.keyword
      };
      
      // Add expected value info
      if (err.params.type) {
        formattedError.expected = err.params.type;
      } else if (err.params.missingProperty) {
        formattedError.expected = `required property '${err.params.missingProperty}'`;
      } else if (err.params.allowedValues) {
        formattedError.expected = err.params.allowedValues;
      } else if (err.params.limit !== undefined) {
        formattedError.expected = `${err.keyword} ${err.params.limit}`;
      }
      
      // Add actual value (if available and not sensitive)
      if (err.data !== undefined && typeof err.data !== 'object') {
        formattedError.actual = err.data;
      }
      
      return formattedError;
    });
  }
  
  /**
   * Add custom validator function
   * 
   * Custom validators should return { valid: boolean, errors: ValidationError[] }
   * 
   * @param {Function} validatorFn - Custom validator function
   * 
   * @example
   * validator.addCustomValidator((data) => {
   *   if (data.name === 'forbidden') {
   *     return {
   *       valid: false,
   *       errors: [{ path: 'name', message: 'Name is forbidden' }]
   *     };
   *   }
   *   return { valid: true, errors: [] };
   * });
   */
  addCustomValidator(validatorFn) {
    this.customValidators.push(validatorFn);
  }
  
  /**
   * Load schema from file system
   * 
   * @param {string} schemaPath - Path to JSON schema file
   * @returns {Promise<Object>} Parsed JSON schema
   * 
   * @example
   * const schema = await validator.loadSchema('./schema.json');
   */
  async loadSchema(schemaPath) {
    // Check cache first
    if (this.schemaCache.has(schemaPath)) {
      return this.schemaCache.get(schemaPath);
    }
    
    // Read and parse schema file
    const content = await fs.readFile(schemaPath, 'utf8');
    const schema = JSON.parse(content);
    
    // Cache for future use
    this.schemaCache.set(schemaPath, schema);
    
    return schema;
  }
}

/**
 * Validate data against schema (convenience function)
 * 
 * @param {*} data - Data to validate
 * @param {Object|string} schema - JSON Schema object or path to schema file
 * @returns {ValidationResult} Validation result
 * 
 * @example
 * const result = validate({ name: 'test' }, { type: 'object' });
 */
function validate(data, schema) {
  const validator = new Validator();
  return validator.validate(data, schema);
}

/**
 * Validate file against schema
 * 
 * Supports both JSON and YAML files.
 * 
 * @param {string} filePath - Path to JSON or YAML file
 * @param {Object|string} schema - JSON Schema object or path to schema file
 * @returns {Promise<ValidationResult>} Validation result
 * 
 * @example
 * const result = await validateFile('./data.yaml', schema);
 * if (!result.valid) {
 *   console.error('Validation failed:', result.errors);
 * }
 */
async function validateFile(filePath, schema) {
  const validator = new Validator();
  
  // Load schema if it's a file path
  let schemaObject = schema;
  if (typeof schema === 'string') {
    schemaObject = await validator.loadSchema(schema);
  }
  
  // Read file content
  const content = await fs.readFile(filePath, 'utf8');
  
  // Parse based on file extension
  let data;
  const ext = path.extname(filePath).toLowerCase();
  
  if (ext === '.yaml' || ext === '.yml') {
    // Parse YAML
    data = yaml.load(content);
  } else if (ext === '.json') {
    // Parse JSON
    data = JSON.parse(content);
  } else {
    // Try JSON first, then YAML
    try {
      data = JSON.parse(content);
    } catch {
      data = yaml.load(content);
    }
  }
  
  // Validate parsed data
  return validator.validate(data, schemaObject);
}

/**
 * Format validation errors for human-readable output
 * 
 * @param {ValidationError[]} errors - Array of validation errors
 * @param {string} [fileName] - Optional file name to include in output
 * @returns {string} Formatted error message
 * 
 * @example
 * const formatted = formatErrors(result.errors, 'data.json');
 * console.error(formatted);
 */
function formatErrors(errors, fileName) {
  if (!errors || errors.length === 0) {
    return '✅ Validation passed';
  }
  
  let output = '';
  
  if (fileName) {
    output += `❌ Validation failed for ${fileName}\n\n`;
  } else {
    output += `❌ Validation failed\n\n`;
  }
  
  errors.forEach((err, index) => {
    output += `Error ${index + 1}: ${err.path || '(root)'}\n`;
    
    if (err.expected) {
      output += `  Expected: ${err.expected}\n`;
    }
    
    if (err.actual !== undefined) {
      const actualType = typeof err.actual;
      output += `  Actual: ${actualType} (${JSON.stringify(err.actual)})\n`;
    }
    
    output += `  Message: ${err.message}\n`;
    output += '\n';
  });
  
  return output.trimEnd();
}

// Export API
module.exports = {
  Validator,
  validate,
  validateFile,
  formatErrors
};
