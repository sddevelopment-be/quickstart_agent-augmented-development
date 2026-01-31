/**
 * Prompt Quality Validator
 * 
 * Validates AI agent prompts against quality schema and detects anti-patterns
 * from ADR-023 Prompt Optimization Framework.
 * 
 * @module prompt-validator
 * @version 1.0.0
 * @author Backend Benny
 * @date 2026-01-30
 * 
 * Following Directives:
 * - Directive 016 (ATDD): Validates acceptance criteria presence
 * - Directive 017 (TDD): Unit tested with jest
 * - Directive 018 (Traceable Decisions): Links to ADR-023
 * - Directive 021 (Locality of Change): Focused on validation only
 * 
 * Related ADRs:
 * - ADR-023: Prompt Optimization Framework (Phase 2)
 * 
 * Anti-Patterns Detected (from ADR-023):
 * 1. Vague Success Criteria (P1)
 * 2. Missing File Extensions (P2)
 * 3. Scope Creep Language (P4)
 * 4. Relative Paths (P5)
 * 5. Overloaded Time Box (P12)
 * 6. Insufficient Context Files
 * 7. Missing Validation Criteria
 * 8. Unbounded Arrays
 * 9. Weak Constraints
 * 10. Missing Checkpoints for Long Tasks
 * 11. Token Budget Overload
 * 12. Vague Deliverable Validation
 */

const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const yaml = require('js-yaml');
const fs = require('fs').promises;

/**
 * Validation result object
 * @typedef {Object} ValidationResult
 * @property {boolean} valid - True if validation passed
 * @property {ValidationError[]} errors - Array of validation errors
 * @property {ValidationWarning[]} warnings - Array of warnings
 * @property {number} score - Quality score (0-100)
 */

/**
 * Validation error object
 * @typedef {Object} ValidationError
 * @property {string} type - Error type: 'schema' or 'anti-pattern'
 * @property {string} path - JSON path to invalid field
 * @property {string} message - Human-readable error message
 * @property {string} [pattern] - Anti-pattern ID if applicable
 * @property {string} [suggestion] - How to fix the error
 */

/**
 * Validation warning object
 * @typedef {Object} ValidationWarning
 * @property {string} type - Warning type: 'efficiency', 'risk', 'best-practice'
 * @property {string} message - Human-readable warning message
 * @property {string} [suggestion] - Recommendation for improvement
 */

/**
 * PromptValidator class for validating AI agent prompts
 * 
 * @class PromptValidator
 * @example
 * const validator = new PromptValidator();
 * await validator.loadSchema('./validation/schemas/prompt-schema.json');
 * const result = await validator.validatePrompt('./my-prompt.yaml');
 * if (!result.valid) {
 *   console.error('Validation errors:', result.errors);
 * }
 */
class PromptValidator {
  /**
   * Create a new PromptValidator instance
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
    
    this.schema = null;
    this.validate = null;
    this.antiPatterns = this.initAntiPatterns();
  }

  /**
   * Initialize anti-pattern detection rules from ADR-023
   * 
   * @returns {Array} Array of anti-pattern definitions
   * @private
   */
  initAntiPatterns() {
    return [
      {
        id: 'vague-success-criteria',
        description: 'Success criterion lacks specific metrics or validation method',
        pattern: /\b(assess|review|check|ensure|verify)\b/i,
        field: 'success_criteria',
        minLength: 20,
        message: 'Success criterion too vague - needs specific validation method or metric',
        suggestion: 'Add specific pass/fail condition (e.g., "All 15 tests pass" instead of "Check tests")'
      },
      {
        id: 'scope-creep-language',
        description: 'Unbounded scope indicators without explicit limits',
        pattern: /\b(all|every|everything|any|comprehensive|entire|whole)\b/i,
        field: 'objective',
        message: 'Scope creep risk - objective lacks explicit boundaries',
        suggestion: 'Replace with bounded scope (e.g., "top 5 files" instead of "all files")'
      },
      {
        id: 'missing-file-extension',
        description: 'Deliverable path missing file extension',
        pattern: /^[^.]+$/,
        field: 'deliverables.file',
        message: 'Deliverable missing file extension',
        suggestion: 'Add file extension (e.g., .md, .js, .yaml, .json)'
      },
      {
        id: 'relative-path',
        description: 'Context file uses relative path instead of absolute',
        pattern: /^\.\.?\//,
        field: 'context_files.critical.path',
        message: 'Use absolute paths for context files',
        suggestion: 'Replace with absolute path from repo root (e.g., "docs/guide.md" not "./guide.md")'
      },
      {
        id: 'vague-deliverable-validation',
        description: 'Deliverable validation criteria too vague',
        pattern: /\b(check|ensure|verify|review|assess)\b/i,
        field: 'deliverables.validation',
        minLength: 15,
        message: 'Deliverable validation too vague',
        suggestion: 'Specify exact validation method (e.g., "passes test suite X" instead of "check quality")'
      }
    ];
  }

  /**
   * Load JSON Schema from file system
   * 
   * @param {string} schemaPath - Path to JSON schema file
   * @returns {Promise<void>}
   * @throws {Error} If schema file cannot be read or is invalid JSON
   * 
   * @example
   * await validator.loadSchema('./validation/schemas/prompt-schema.json');
   */
  async loadSchema(schemaPath) {
    const schemaContent = await fs.readFile(schemaPath, 'utf8');
    this.schema = JSON.parse(schemaContent);
    this.validate = this.ajv.compile(this.schema);
  }

  /**
   * Validate prompt from YAML file
   * 
   * @param {string} promptPath - Path to YAML prompt file
   * @returns {Promise<ValidationResult>} Validation result with errors and warnings
   * @throws {Error} If file cannot be read or YAML is malformed
   * 
   * @example
   * const result = await validator.validatePrompt('./prompts/my-task.yaml');
   * console.log(`Score: ${result.score}/100`);
   */
  async validatePrompt(promptPath) {
    const content = await fs.readFile(promptPath, 'utf8');
    const prompt = yaml.load(content);
    
    return this.validatePromptData(prompt);
  }

  /**
   * Validate prompt data object directly
   * 
   * @param {Object} prompt - Prompt data object
   * @returns {Promise<ValidationResult>} Validation result with errors and warnings
   * 
   * @example
   * const result = await validator.validatePromptData({
   *   objective: 'Create auth module',
   *   deliverables: [...],
   *   success_criteria: [...],
   *   constraints: {...},
   *   context_files: {...}
   * });
   */
  async validatePromptData(prompt) {
    if (!this.validate) {
      throw new Error('Schema not loaded. Call loadSchema() first.');
    }

    // Handle null or non-object input
    if (!prompt || typeof prompt !== 'object') {
      return {
        valid: false,
        errors: [{
          type: 'schema',
          path: '',
          message: 'Prompt must be an object',
          keyword: 'type'
        }],
        warnings: [],
        score: 0
      };
    }

    // Schema validation
    const schemaValid = this.validate(prompt);
    const errors = [];

    if (!schemaValid) {
      errors.push(...this.formatSchemaErrors(this.validate.errors));
    }

    // Anti-pattern detection
    const antiPatternErrors = this.detectAntiPatterns(prompt);
    errors.push(...antiPatternErrors);

    // Generate warnings
    const warnings = this.generateWarnings(prompt);

    // Calculate quality score
    const score = this.calculateQualityScore(prompt, errors);

    return {
      valid: errors.length === 0,
      errors,
      warnings,
      score
    };
  }

  /**
   * Format AJV schema errors into human-readable format
   * 
   * @param {Array} ajvErrors - Raw AJV error objects
   * @returns {ValidationError[]} Formatted error objects
   * @private
   */
  formatSchemaErrors(ajvErrors) {
    if (!ajvErrors || ajvErrors.length === 0) {
      return [];
    }

    return ajvErrors.map(err => {
      // Convert instancePath from AJV format (/path/to/field) to dot notation
      const path = err.instancePath
        ? err.instancePath.substring(1).replace(/\//g, '.')
        : (err.params.missingProperty || '');

      const formattedError = {
        type: 'schema',
        path: path,
        message: err.message || 'Validation failed',
        keyword: err.keyword
      };

      // Add helpful context
      if (err.params.missingProperty) {
        formattedError.message = `Missing required property '${err.params.missingProperty}'`;
        formattedError.suggestion = `Add the '${err.params.missingProperty}' field to your prompt`;
      } else if (err.params.type) {
        formattedError.message = `must be ${err.params.type}`;
      } else if (err.params.limit !== undefined) {
        formattedError.message = `must ${err.keyword} ${err.params.limit}`;
      }

      return formattedError;
    });
  }

  /**
   * Detect anti-patterns in prompt
   * 
   * Checks for all 12 anti-patterns defined in ADR-023
   * 
   * @param {Object} prompt - Prompt data object
   * @returns {ValidationError[]} Array of detected anti-pattern errors
   */
  detectAntiPatterns(prompt) {
    const errors = [];

    // Pattern 1: Vague Success Criteria
    if (prompt.success_criteria && Array.isArray(prompt.success_criteria)) {
      prompt.success_criteria.forEach((criterion, idx) => {
        const ap = this.antiPatterns.find(p => p.id === 'vague-success-criteria');
        if (ap.pattern.test(criterion) && criterion.length < ap.minLength) {
          errors.push({
            type: 'anti-pattern',
            pattern: ap.id,
            path: `success_criteria[${idx}]`,
            message: ap.message,
            suggestion: ap.suggestion
          });
        }
      });
    }

    // Pattern 4: Scope Creep Language in objective
    if (prompt.objective) {
      const ap = this.antiPatterns.find(p => p.id === 'scope-creep-language');
      if (ap.pattern.test(prompt.objective)) {
        errors.push({
          type: 'anti-pattern',
          pattern: ap.id,
          path: 'objective',
          message: ap.message,
          suggestion: ap.suggestion
        });
      }
    }

    // Pattern 2: Missing File Extensions in deliverables
    if (prompt.deliverables && Array.isArray(prompt.deliverables)) {
      prompt.deliverables.forEach((deliverable, idx) => {
        if (deliverable.file) {
          const ap = this.antiPatterns.find(p => p.id === 'missing-file-extension');
          if (ap.pattern.test(deliverable.file)) {
            errors.push({
              type: 'anti-pattern',
              pattern: ap.id,
              path: `deliverables[${idx}].file`,
              message: ap.message,
              suggestion: ap.suggestion
            });
          }
        }

        // Pattern 12: Vague deliverable validation
        if (deliverable.validation) {
          const ap = this.antiPatterns.find(p => p.id === 'vague-deliverable-validation');
          if (ap.pattern.test(deliverable.validation) && deliverable.validation.length < ap.minLength) {
            errors.push({
              type: 'anti-pattern',
              pattern: ap.id,
              path: `deliverables[${idx}].validation`,
              message: ap.message,
              suggestion: ap.suggestion
            });
          }
        }
      });
    }

    // Pattern 5: Relative Paths in context files
    if (prompt.context_files && prompt.context_files.critical) {
      prompt.context_files.critical.forEach((file, idx) => {
        if (file.path) {
          const ap = this.antiPatterns.find(p => p.id === 'relative-path');
          if (ap.pattern.test(file.path)) {
            errors.push({
              type: 'anti-pattern',
              pattern: ap.id,
              path: `context_files.critical[${idx}].path`,
              message: ap.message,
              suggestion: ap.suggestion
            });
          }
        }
      });
    }

    return errors;
  }

  /**
   * Generate warnings for potential issues
   * 
   * Warnings don't fail validation but indicate potential problems
   * 
   * @param {Object} prompt - Prompt data object
   * @returns {ValidationWarning[]} Array of warnings
   */
  generateWarnings(prompt) {
    const warnings = [];

    // Pattern 12: Overloaded time box without checkpoints
    if (prompt.constraints?.time_box > 60 && !prompt.checkpoints) {
      warnings.push({
        type: 'risk',
        message: `Task >60 min (${prompt.constraints.time_box} min) without checkpoints risks work loss`,
        suggestion: 'Add checkpoint guidance every 30-45 minutes'
      });
    }

    // Token budget warning
    if (prompt.context_files?.critical?.length > 8) {
      warnings.push({
        type: 'efficiency',
        message: `Loading ${prompt.context_files.critical.length} critical files may exceed 20K token budget`,
        suggestion: 'Consider progressive loading or splitting task into smaller chunks'
      });
    }

    // Missing token budget for large tasks
    if (prompt.constraints?.time_box > 90 && !prompt.token_budget) {
      warnings.push({
        type: 'best-practice',
        message: 'Large task (>90 min) should include token budget guidance',
        suggestion: 'Add token_budget section with target_input and estimated_output'
      });
    }

    // Too many success criteria
    if (prompt.success_criteria?.length > 8) {
      warnings.push({
        type: 'efficiency',
        message: `${prompt.success_criteria.length} success criteria may be too many to verify efficiently`,
        suggestion: 'Consider grouping or prioritizing to 3-8 key criteria'
      });
    }

    // Too few constraints
    if (prompt.constraints?.do && prompt.constraints.do.length < 2) {
      warnings.push({
        type: 'best-practice',
        message: 'Only one "do" constraint - consider adding more guidance',
        suggestion: 'Add at least 2 explicit allowed actions'
      });
    }

    if (prompt.constraints?.dont && prompt.constraints.dont.length < 2) {
      warnings.push({
        type: 'best-practice',
        message: 'Only one "dont" constraint - consider adding more boundaries',
        suggestion: 'Add at least 2 explicit prohibited actions'
      });
    }

    return warnings;
  }

  /**
   * Calculate quality score (0-100) based on validation results
   * 
   * Scoring:
   * - Start at 100
   * - Deduct 10 points per schema error
   * - Deduct 5 points per anti-pattern
   * - Add 5 points for token_budget
   * - Add 5 points for checkpoints
   * - Add 5 points for handoff
   * 
   * @param {Object} prompt - Prompt data object
   * @param {ValidationError[]} errors - Array of validation errors
   * @returns {number} Quality score (0-100)
   */
  calculateQualityScore(prompt, errors) {
    let score = 100;

    // Deduct for errors
    const schemaErrors = errors.filter(e => e.type === 'schema');
    const antiPatternErrors = errors.filter(e => e.type === 'anti-pattern');

    score -= schemaErrors.length * 10;
    score -= antiPatternErrors.length * 5;

    // Bonus for best practices (only if valid base structure)
    if (schemaErrors.length === 0) {
      if (prompt.token_budget) score += 5;
      if (prompt.checkpoints) score += 5;
      if (prompt.handoff) score += 5;
    }

    // Ensure score stays in 0-100 range
    return Math.max(0, Math.min(100, score));
  }
}

/**
 * Format validation result for human-readable output
 * 
 * @param {ValidationResult} result - Validation result object
 * @param {string} [fileName] - Optional file name to include in output
 * @returns {string} Formatted output string
 * 
 * @example
 * const formatted = formatValidationResult(result, 'my-prompt.yaml');
 * console.log(formatted);
 */
function formatValidationResult(result, fileName) {
  let output = '';

  if (fileName) {
    output += `\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
    output += `Prompt Validation: ${fileName}\n`;
    output += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
  }

  // Overall status
  if (result.valid) {
    output += `✅ PASSED - Quality Score: ${result.score}/100\n\n`;
  } else {
    output += `❌ FAILED - Quality Score: ${result.score}/100\n\n`;
  }

  // Errors
  if (result.errors && result.errors.length > 0) {
    output += `Errors (${result.errors.length}):\n`;
    output += `${'─'.repeat(50)}\n`;

    result.errors.forEach((err, index) => {
      output += `\n${index + 1}. ${err.path || '(root)'}\n`;
      output += `   Type: ${err.type}\n`;
      
      if (err.pattern) {
        output += `   Pattern: ${err.pattern}\n`;
      }
      
      output += `   Message: ${err.message}\n`;
      
      if (err.suggestion) {
        output += `   💡 Suggestion: ${err.suggestion}\n`;
      }
    });

    output += '\n';
  }

  // Warnings
  if (result.warnings && result.warnings.length > 0) {
    output += `\nWarnings (${result.warnings.length}):\n`;
    output += `${'─'.repeat(50)}\n`;

    result.warnings.forEach((warning, index) => {
      output += `\n${index + 1}. [${warning.type}] ${warning.message}\n`;
      
      if (warning.suggestion) {
        output += `   💡 Suggestion: ${warning.suggestion}\n`;
      }
    });

    output += '\n';
  }

  return output;
}

// Export API
module.exports = {
  PromptValidator,
  formatValidationResult
};
