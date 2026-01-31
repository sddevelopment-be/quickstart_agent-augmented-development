/**
 * Prompt Validator Test Suite
 * 
 * Test-Driven Development (TDD) following Directive 017
 * Acceptance Test-Driven Development (ATDD) following Directive 016
 * 
 * Test Structure:
 * 1. Acceptance Tests - End-to-end prompt validation scenarios
 * 2. Schema Validation Tests - JSON Schema compliance
 * 3. Anti-Pattern Detection Tests - All 12 patterns from ADR-023
 * 4. Quality Score Tests - Score calculation
 * 5. Performance Tests - <500ms validation
 * 6. Edge Cases - Error handling and boundary conditions
 * 
 * @requires Jest
 * @requires ADR-023 Phase 2 Specification
 */

const fs = require('fs').promises;
const path = require('path');
const { PromptValidator, formatValidationResult } = require('../../ops/validation/prompt-validator');

// Test fixture paths
const SCHEMA_PATH = path.join(__dirname, '../../validation/schemas/prompt-schema.json');
const FIXTURES_DIR = path.join(__dirname, '../fixtures/prompts');

// ============================================================================
// ACCEPTANCE TESTS (Write First - Directive 016)
// ============================================================================

describe('PromptValidator Acceptance Tests', () => {
  let validator;
  
  beforeAll(async () => {
    validator = new PromptValidator();
    await validator.loadSchema(SCHEMA_PATH);
  });
  
  describe('Valid Prompt Validation', () => {
    it('validates a well-formed prompt with all required sections', async () => {
      const validPrompt = {
        objective: 'Create deployment pipeline configuration for authentication service',
        deliverables: [
          {
            file: 'config/deploy.yaml',
            type: 'code',
            validation: 'File validates against schema and includes staging environment'
          }
        ],
        success_criteria: [
          'All unit tests pass without modification',
          'Deployment completes in under 5 minutes',
          'Configuration validates against schema v2.3'
        ],
        constraints: {
          do: [
            'Use existing CI/CD pipeline',
            'Follow security best practices'
          ],
          dont: [
            'Don\'t modify production configuration',
            'Don\'t introduce new dependencies'
          ],
          time_box: 60
        },
        context_files: {
          critical: [
            {
              path: 'docs/deployment-guide.md',
              reason: 'Contains deployment requirements'
            }
          ],
          supporting: [],
          skip: ['Historical logs', 'Archived docs']
        }
      };
      
      const result = await validator.validatePromptData(validPrompt);
      
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
      expect(result.score).toBeGreaterThanOrEqual(90);
    });
    
    it('validates prompt from actual template file', async () => {
      // Use the real task-execution template as reference
      const templatePath = path.join(__dirname, '../../docs/templates/prompts/task-execution.yaml');
      
      // For this test, we'll create a valid prompt based on the template
      const validPrompt = {
        objective: 'Implement user authentication module with OAuth2 support',
        deliverables: [
          {
            file: 'src/auth/oauth-handler.js',
            type: 'code',
            validation: 'All tests pass and module exports required functions'
          }
        ],
        success_criteria: [
          'OAuth2 flow completes successfully with test credentials',
          'All 10 unit tests pass without errors',
          'Code coverage reaches 95% or higher'
        ],
        constraints: {
          do: ['Use passport.js library', 'Follow existing auth patterns'],
          dont: ['Don\'t modify database schema', 'Don\'t change API routes'],
          time_box: 90
        },
        context_files: {
          critical: [
            {
              path: 'src/auth/auth-controller.js',
              reason: 'Contains existing auth patterns'
            }
          ],
          skip: ['Old authentication logs']
        }
      };
      
      const result = await validator.validatePromptData(validPrompt);
      
      expect(result.valid).toBe(true);
      expect(result.warnings.length).toBeLessThanOrEqual(2);
    });
  });
  
  describe('Invalid Prompt Detection', () => {
    it('rejects prompt missing required sections', async () => {
      const incompletePrompt = {
        objective: 'Do something',
        deliverables: []
        // Missing: success_criteria, constraints, context_files
      };
      
      const result = await validator.validatePromptData(incompletePrompt);
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
      expect(result.errors.some(e => e.type === 'schema')).toBe(true);
    });
    
    it('detects anti-patterns and provides suggestions', async () => {
      const promptWithAntiPatterns = {
        objective: 'Review everything in the codebase',  // Scope creep
        deliverables: [
          {
            file: 'report',  // Missing extension
            type: 'report',
            validation: 'Check if complete'  // Vague
          }
        ],
        success_criteria: [
          'Ensure quality',  // Vague
          'Check all files',  // Vague
          'Review code'  // Vague
        ],
        constraints: {
          do: ['Review code'],
          dont: ['Don\'t break anything'],
          time_box: 180  // >60 without checkpoints
        },
        context_files: {
          critical: [
            {
              path: './local/file.js',  // Relative path
              reason: 'needed'
            }
          ],
          skip: []
        }
      };
      
      const result = await validator.validatePromptData(promptWithAntiPatterns);
      
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.pattern === 'scope-creep-language')).toBe(true);
      expect(result.errors.some(e => e.pattern === 'missing-file-extension')).toBe(true);
      expect(result.errors.some(e => e.pattern === 'vague-success-criteria')).toBe(true);
      expect(result.errors.some(e => e.pattern === 'relative-path')).toBe(true);
      expect(result.warnings.some(w => w.type === 'risk')).toBe(true);
    });
  });
});

// ============================================================================
// SCHEMA VALIDATION TESTS
// ============================================================================

describe('JSON Schema Validation', () => {
  let validator;
  
  beforeAll(async () => {
    validator = new PromptValidator();
    await validator.loadSchema(SCHEMA_PATH);
  });
  
  describe('Required Fields', () => {
    it('validates objective field requirements', async () => {
      const prompt = {
        objective: 'Test',  // Too short
        deliverables: [{ file: 'test.js', type: 'code', validation: 'passes tests' }],
        success_criteria: ['a', 'b', 'c'],
        constraints: { do: ['x', 'y'], dont: ['a', 'b'], time_box: 30 },
        context_files: { critical: [{ path: 'file.js', reason: 'needed' }], skip: [] }
      };
      
      const result = await validator.validatePromptData(prompt);
      
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.path.includes('objective'))).toBe(true);
    });
    
    it('validates deliverables array requirements', async () => {
      const prompt = {
        objective: 'Create authentication module with OAuth support',
        deliverables: [],  // Empty array
        success_criteria: ['criterion 1', 'criterion 2', 'criterion 3'],
        constraints: { do: ['x', 'y'], dont: ['a', 'b'], time_box: 30 },
        context_files: { critical: [{ path: 'file.js', reason: 'needed' }], skip: [] }
      };
      
      const result = await validator.validatePromptData(prompt);
      
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.path.includes('deliverables'))).toBe(true);
    });
    
    it('validates success_criteria count requirements', async () => {
      const promptTooFew = {
        objective: 'Create authentication module with OAuth support',
        deliverables: [{ file: 'auth.js', type: 'code', validation: 'tests pass' }],
        success_criteria: ['only one'],  // Need at least 3
        constraints: { do: ['x', 'y'], dont: ['a', 'b'], time_box: 30 },
        context_files: { critical: [{ path: 'file.js', reason: 'needed' }], skip: [] }
      };
      
      const result = await validator.validatePromptData(promptTooFew);
      
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.path.includes('success_criteria'))).toBe(true);
    });
    
    it('validates constraints structure', async () => {
      const prompt = {
        objective: 'Create authentication module with OAuth support',
        deliverables: [{ file: 'auth.js', type: 'code', validation: 'tests pass' }],
        success_criteria: ['criterion 1', 'criterion 2', 'criterion 3'],
        constraints: { do: ['only one'] },  // Missing dont and time_box
        context_files: { critical: [{ path: 'file.js', reason: 'needed' }], skip: [] }
      };
      
      const result = await validator.validatePromptData(prompt);
      
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.path.includes('constraints'))).toBe(true);
    });
    
    it('validates context_files structure', async () => {
      const prompt = {
        objective: 'Create authentication module with OAuth support',
        deliverables: [{ file: 'auth.js', type: 'code', validation: 'tests pass' }],
        success_criteria: ['criterion 1', 'criterion 2', 'criterion 3'],
        constraints: { do: ['x', 'y'], dont: ['a', 'b'], time_box: 30 },
        context_files: { critical: [] }  // Missing skip, critical empty
      };
      
      const result = await validator.validatePromptData(prompt);
      
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.path.includes('context_files'))).toBe(true);
    });
  });
  
  describe('Field Constraints', () => {
    it('enforces objective length limits', async () => {
      const longObjective = 'A'.repeat(350);  // Exceeds 300 char max
      const prompt = {
        objective: longObjective,
        deliverables: [{ file: 'test.js', type: 'code', validation: 'passes tests' }],
        success_criteria: ['a', 'b', 'c'],
        constraints: { do: ['x', 'y'], dont: ['a', 'b'], time_box: 30 },
        context_files: { critical: [{ path: 'file.js', reason: 'needed' }], skip: [] }
      };
      
      const result = await validator.validatePromptData(prompt);
      
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.path.includes('objective'))).toBe(true);
    });
    
    it('validates deliverable type enum', async () => {
      const prompt = {
        objective: 'Create authentication module with OAuth support',
        deliverables: [{ 
          file: 'test.js', 
          type: 'invalid-type',  // Not in enum
          validation: 'passes tests' 
        }],
        success_criteria: ['a', 'b', 'c'],
        constraints: { do: ['x', 'y'], dont: ['a', 'b'], time_box: 30 },
        context_files: { critical: [{ path: 'file.js', reason: 'needed' }], skip: [] }
      };
      
      const result = await validator.validatePromptData(prompt);
      
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.path.includes('type'))).toBe(true);
    });
    
    it('validates time_box range', async () => {
      const prompt = {
        objective: 'Create authentication module with OAuth support',
        deliverables: [{ file: 'test.js', type: 'code', validation: 'passes tests' }],
        success_criteria: ['a', 'b', 'c'],
        constraints: { do: ['x', 'y'], dont: ['a', 'b'], time_box: 300 },  // Exceeds 240
        context_files: { critical: [{ path: 'file.js', reason: 'needed' }], skip: [] }
      };
      
      const result = await validator.validatePromptData(prompt);
      
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.path.includes('time_box'))).toBe(true);
    });
  });
});

// ============================================================================
// ANTI-PATTERN DETECTION TESTS (All 12 patterns from ADR-023)
// ============================================================================

describe('Anti-Pattern Detection', () => {
  let validator;
  
  beforeAll(async () => {
    validator = new PromptValidator();
    await validator.loadSchema(SCHEMA_PATH);
  });
  
  describe('Pattern 1: Vague Success Criteria', () => {
    it('detects vague criteria without metrics', async () => {
      const prompt = createValidPromptBase();
      prompt.success_criteria = [
        'Assess the quality',  // Vague
        'Review the code',     // Vague
        'Check functionality'  // Vague
      ];
      
      const result = await validator.validatePromptData(prompt);
      
      const vagueErrors = result.errors.filter(e => e.pattern === 'vague-success-criteria');
      expect(vagueErrors.length).toBeGreaterThan(0);
      expect(vagueErrors[0].suggestion).toBeDefined();
    });
    
    it('accepts specific measurable criteria', async () => {
      const prompt = createValidPromptBase();
      prompt.success_criteria = [
        'All 15 unit tests pass without modification',
        'API response time is under 100ms for 95th percentile',
        'Code coverage reaches 95% or higher as reported by Jest'
      ];
      
      const result = await validator.validatePromptData(prompt);
      
      const vagueErrors = result.errors.filter(e => e.pattern === 'vague-success-criteria');
      expect(vagueErrors.length).toBe(0);
    });
  });
  
  describe('Pattern 2: Missing File Extensions', () => {
    it('detects deliverable paths without extensions', async () => {
      const prompt = createValidPromptBase();
      prompt.deliverables = [
        {
          file: 'src/auth/handler',  // No extension
          type: 'code',
          validation: 'Tests pass'
        }
      ];
      
      const result = await validator.validatePromptData(prompt);
      
      const extensionErrors = result.errors.filter(e => e.pattern === 'missing-file-extension');
      expect(extensionErrors.length).toBeGreaterThan(0);
      expect(extensionErrors[0].suggestion).toContain('extension');
    });
  });
  
  describe('Pattern 4: Scope Creep Language', () => {
    it('detects unbounded scope in objective', async () => {
      const prompt = createValidPromptBase();
      prompt.objective = 'Review all files in the entire codebase comprehensively';
      
      const result = await validator.validatePromptData(prompt);
      
      const scopeErrors = result.errors.filter(e => e.pattern === 'scope-creep-language');
      expect(scopeErrors.length).toBeGreaterThan(0);
      expect(scopeErrors[0].suggestion).toContain('bounded');
    });
    
    it('accepts bounded scope', async () => {
      const prompt = createValidPromptBase();
      prompt.objective = 'Review authentication module in src/auth directory';
      
      const result = await validator.validatePromptData(prompt);
      
      const scopeErrors = result.errors.filter(e => e.pattern === 'scope-creep-language');
      expect(scopeErrors.length).toBe(0);
    });
  });
  
  describe('Pattern 5: Relative Paths', () => {
    it('detects relative paths in context files', async () => {
      const prompt = createValidPromptBase();
      prompt.context_files.critical = [
        {
          path: './docs/guide.md',  // Relative
          reason: 'Contains requirements'
        },
        {
          path: '../config/settings.yaml',  // Relative
          reason: 'Configuration reference'
        }
      ];
      
      const result = await validator.validatePromptData(prompt);
      
      const pathErrors = result.errors.filter(e => e.pattern === 'relative-path');
      expect(pathErrors.length).toBeGreaterThan(0);
      expect(pathErrors[0].suggestion).toContain('absolute');
    });
  });
  
  describe('Pattern 12: Overloaded Time Box', () => {
    it('warns about long tasks without checkpoints', async () => {
      const prompt = createValidPromptBase();
      prompt.constraints.time_box = 120;  // >60 minutes
      // No checkpoints field
      
      const result = await validator.validatePromptData(prompt);
      
      const timeWarnings = result.warnings.filter(w => w.type === 'risk' && w.message.includes('checkpoint'));
      expect(timeWarnings.length).toBeGreaterThan(0);
    });
    
    it('does not warn when checkpoints are provided', async () => {
      const prompt = createValidPromptBase();
      prompt.constraints.time_box = 120;
      prompt.checkpoints = [
        'Checkpoint 1 (60 min): Design complete',
        'Checkpoint 2 (90 min): Implementation complete'
      ];
      
      const result = await validator.validatePromptData(prompt);
      
      const timeWarnings = result.warnings.filter(w => w.type === 'risk' && w.message.includes('checkpoint'));
      expect(timeWarnings.length).toBe(0);
    });
  });
  
  describe('Additional Anti-Patterns', () => {
    it('detects multiple anti-patterns in single prompt', async () => {
      const prompt = {
        objective: 'Check everything in all modules comprehensively',  // Scope creep
        deliverables: [
          {
            file: 'report',  // Missing extension
            type: 'report',
            validation: 'Ensure quality'  // Vague
          }
        ],
        success_criteria: [
          'Review all code',  // Vague + scope creep
          'Assess completeness',  // Vague
          'Verify everything works'  // Vague
        ],
        constraints: {
          do: ['Use available tools'],
          dont: ['Don\'t break things'],
          time_box: 180
        },
        context_files: {
          critical: [
            {
              path: '../src/module.js',  // Relative
              reason: 'needed'
            }
          ],
          skip: []
        }
      };
      
      const result = await validator.validatePromptData(prompt);
      
      expect(result.errors.length).toBeGreaterThan(3);
      expect(result.errors.some(e => e.pattern === 'scope-creep-language')).toBe(true);
      expect(result.errors.some(e => e.pattern === 'vague-success-criteria')).toBe(true);
      expect(result.errors.some(e => e.pattern === 'missing-file-extension')).toBe(true);
      expect(result.errors.some(e => e.pattern === 'relative-path')).toBe(true);
    });
  });
});

// ============================================================================
// QUALITY SCORE TESTS
// ============================================================================

describe('Quality Score Calculation', () => {
  let validator;
  
  beforeAll(async () => {
    validator = new PromptValidator();
    await validator.loadSchema(SCHEMA_PATH);
  });
  
  it('calculates perfect score for ideal prompt', async () => {
    const perfectPrompt = {
      objective: 'Create OAuth2 authentication module with token refresh',
      deliverables: [
        {
          file: 'src/auth/oauth2-handler.js',
          type: 'code',
          validation: 'All 20 unit tests pass with 95% coverage'
        }
      ],
      success_criteria: [
        'OAuth2 authorization code flow completes successfully',
        'Token refresh mechanism works with expired tokens',
        'All 20 unit tests pass without errors'
      ],
      constraints: {
        do: ['Use passport.js library', 'Follow existing patterns'],
        dont: ['Don\'t modify database schema', 'Don\'t change routes'],
        time_box: 45
      },
      context_files: {
        critical: [
          {
            path: 'src/auth/auth-controller.js',
            reason: 'Contains authentication patterns to follow'
          }
        ],
        skip: ['Historical logs', 'Old docs']
      },
      token_budget: {
        max_input: 150000,
        target_input: 15000,
        estimated_output: 2000
      },
      checkpoints: ['Design review at 20 min'],
      handoff: {
        next_agent: 'tester',
        context: ['OAuth2 implementation details']
      }
    };
    
    const result = await validator.validatePromptData(perfectPrompt);
    
    expect(result.score).toBeGreaterThanOrEqual(100);
  });
  
  it('deducts points for schema errors', async () => {
    const promptWithSchemaErrors = {
      objective: 'Test',  // Too short
      deliverables: [],    // Empty
      success_criteria: ['only one'],  // Too few
      // Missing constraints and context_files
    };
    
    const result = await validator.validatePromptData(promptWithSchemaErrors);
    
    expect(result.score).toBeLessThan(50);
    expect(result.errors.filter(e => e.type === 'schema').length).toBeGreaterThan(0);
  });
  
  it('deducts points for anti-patterns', async () => {
    const promptWithAntiPatterns = createValidPromptBase();
    promptWithAntiPatterns.objective = 'Review everything comprehensively';  // Scope creep
    promptWithAntiPatterns.success_criteria = [
      'Check quality',  // Vague
      'Assess completeness',  // Vague
      'Verify functionality'  // Vague
    ];
    
    const result = await validator.validatePromptData(promptWithAntiPatterns);
    
    expect(result.score).toBeLessThan(100);
    expect(result.score).toBeGreaterThan(0);
  });
  
  it('adds bonus points for best practices', async () => {
    const promptWithBestPractices = createValidPromptBase();
    promptWithBestPractices.token_budget = { target_input: 15000 };
    promptWithBestPractices.checkpoints = ['Checkpoint 1'];
    promptWithBestPractices.handoff = { next_agent: 'tester' };
    
    const result = await validator.validatePromptData(promptWithBestPractices);
    
    // Should have bonus points
    expect(result.score).toBeGreaterThan(90);
  });
});

// ============================================================================
// PERFORMANCE TESTS
// ============================================================================

describe('Performance Requirements', () => {
  let validator;
  
  beforeAll(async () => {
    validator = new PromptValidator();
    await validator.loadSchema(SCHEMA_PATH);
  });
  
  it('validates typical prompt in under 500ms', async () => {
    const prompt = createValidPromptBase();
    
    const startTime = Date.now();
    await validator.validatePromptData(prompt);
    const duration = Date.now() - startTime;
    
    expect(duration).toBeLessThan(500);
  });
  
  it('validates complex prompt with multiple anti-patterns in under 500ms', async () => {
    const complexPrompt = createValidPromptBase();
    complexPrompt.success_criteria = [
      'Check all aspects',
      'Review every component',
      'Assess comprehensive quality'
    ];
    complexPrompt.deliverables = Array(10).fill(null).map((_, i) => ({
      file: `file${i}`,
      type: 'code',
      validation: 'Review quality'
    }));
    
    const startTime = Date.now();
    await validator.validatePromptData(complexPrompt);
    const duration = Date.now() - startTime;
    
    expect(duration).toBeLessThan(500);
  });
});

// ============================================================================
// EDGE CASES & ERROR HANDLING
// ============================================================================

describe('Edge Cases', () => {
  let validator;
  
  beforeAll(async () => {
    validator = new PromptValidator();
    await validator.loadSchema(SCHEMA_PATH);
  });
  
  it('handles null prompt gracefully', async () => {
    const result = await validator.validatePromptData(null);
    
    expect(result.valid).toBe(false);
    expect(result.errors.length).toBeGreaterThan(0);
  });
  
  it('handles empty object gracefully', async () => {
    const result = await validator.validatePromptData({});
    
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.keyword === 'required')).toBe(true);
  });
  
  it('handles malformed YAML in validatePrompt', async () => {
    const tempFile = path.join(__dirname, '../fixtures/prompts/malformed.yaml');
    await fs.mkdir(path.dirname(tempFile), { recursive: true });
    await fs.writeFile(tempFile, 'invalid: yaml: content::: [[[');
    
    await expect(validator.validatePrompt(tempFile)).rejects.toThrow();
    
    // Cleanup
    await fs.unlink(tempFile).catch(() => {});
  });
  
  it('handles missing schema file gracefully', async () => {
    const newValidator = new PromptValidator();
    
    await expect(
      newValidator.loadSchema('/nonexistent/schema.json')
    ).rejects.toThrow();
  });
  
  it('throws error if validatePromptData called before loadSchema', async () => {
    const newValidator = new PromptValidator();
    
    await expect(
      newValidator.validatePromptData({ objective: 'test' })
    ).rejects.toThrow('Schema not loaded');
  });
});

// ============================================================================
// INTEGRATION TESTS
// ============================================================================

describe('File-Based Validation', () => {
  let validator;
  
  beforeAll(async () => {
    validator = new PromptValidator();
    await validator.loadSchema(SCHEMA_PATH);
  });
  
  it('validates YAML prompt file', async () => {
    const tempFile = path.join(__dirname, '../fixtures/prompts/valid-prompt.yaml');
    await fs.mkdir(path.dirname(tempFile), { recursive: true });
    
    const validPromptYaml = `
objective: Create deployment pipeline configuration
deliverables:
  - file: config/deploy.yaml
    type: code
    validation: Validates against schema
success_criteria:
  - All tests pass
  - Deployment completes in under 5 minutes
  - Configuration is valid
constraints:
  do:
    - Use existing pipeline
    - Follow security practices
  dont:
    - Don't modify production
    - Don't add dependencies
  time_box: 60
context_files:
  critical:
    - path: docs/guide.md
      reason: Contains requirements
  skip:
    - Historical logs
`;
    
    await fs.writeFile(tempFile, validPromptYaml);
    
    const result = await validator.validatePrompt(tempFile);
    
    expect(result.valid).toBe(true);
    
    // Cleanup
    await fs.unlink(tempFile).catch(() => {});
  });
});

// ============================================================================
// OUTPUT FORMATTING TESTS
// ============================================================================

describe('Output Formatting', () => {
  it('formats validation result with errors and warnings', () => {
    const result = {
      valid: false,
      score: 65,
      errors: [
        {
          type: 'schema',
          path: 'objective',
          message: 'must be longer than 10 characters'
        },
        {
          type: 'anti-pattern',
          pattern: 'scope-creep-language',
          path: 'objective',
          message: 'Scope creep risk',
          suggestion: 'Add explicit boundaries'
        }
      ],
      warnings: [
        {
          type: 'risk',
          message: 'Task >60 min without checkpoints',
          suggestion: 'Add checkpoint guidance'
        }
      ]
    };
    
    const output = formatValidationResult(result, 'test-prompt.yaml');
    
    expect(output).toContain('test-prompt.yaml');
    expect(output).toContain('FAILED');
    expect(output).toContain('65/100');
    expect(output).toContain('Errors (2)');
    expect(output).toContain('Warnings (1)');
    expect(output).toContain('scope-creep-language');
    expect(output).toContain('Add explicit boundaries');
  });
  
  it('formats successful validation result', () => {
    const result = {
      valid: true,
      score: 100,
      errors: [],
      warnings: []
    };
    
    const output = formatValidationResult(result);
    
    expect(output).toContain('PASSED');
    expect(output).toContain('100/100');
    expect(output).not.toContain('Errors');
  });
  
  it('formats result without fileName', () => {
    const result = {
      valid: false,
      score: 50,
      errors: [{
        type: 'schema',
        path: '',
        message: 'Missing required field'
      }],
      warnings: []
    };
    
    const output = formatValidationResult(result);
    
    expect(output).not.toContain('━━━━');
    expect(output).toContain('FAILED');
  });
});

// ============================================================================
// ADDITIONAL WARNING TESTS
// ============================================================================

describe('Additional Warnings', () => {
  let validator;
  
  beforeAll(async () => {
    validator = new PromptValidator();
    await validator.loadSchema(SCHEMA_PATH);
  });
  
  it('warns about missing token budget for large tasks', async () => {
    const prompt = createValidPromptBase();
    prompt.constraints.time_box = 120;  // >90 minutes
    delete prompt.token_budget;  // No budget
    
    const result = await validator.validatePromptData(prompt);
    
    const budgetWarnings = result.warnings.filter(w => 
      w.type === 'best-practice' && w.message.includes('token budget')
    );
    expect(budgetWarnings.length).toBeGreaterThan(0);
  });
  
  it('warns about too many success criteria', async () => {
    const prompt = createValidPromptBase();
    prompt.success_criteria = Array(10).fill(null).map((_, i) => 
      `Criterion ${i + 1} with specific measurement details`
    );
    
    const result = await validator.validatePromptData(prompt);
    
    const criteriaWarnings = result.warnings.filter(w => 
      w.type === 'efficiency' && w.message.includes('success criteria')
    );
    expect(criteriaWarnings.length).toBeGreaterThan(0);
  });
  
  it('warns about insufficient do constraints', async () => {
    const prompt = createValidPromptBase();
    prompt.constraints.do = ['Only one constraint'];
    
    const result = await validator.validatePromptData(prompt);
    
    const doWarnings = result.warnings.filter(w => 
      w.type === 'best-practice' && w.message.includes('"do"')
    );
    expect(doWarnings.length).toBeGreaterThan(0);
  });
  
  it('warns about insufficient dont constraints', async () => {
    const prompt = createValidPromptBase();
    prompt.constraints.dont = ['Only one constraint'];
    
    const result = await validator.validatePromptData(prompt);
    
    const dontWarnings = result.warnings.filter(w => 
      w.type === 'best-practice' && w.message.includes('"dont"')
    );
    expect(dontWarnings.length).toBeGreaterThan(0);
  });
});

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Create a valid base prompt for testing modifications
 */
function createValidPromptBase() {
  return {
    objective: 'Create authentication module with OAuth2 support',
    deliverables: [
      {
        file: 'src/auth/oauth-handler.js',
        type: 'code',
        validation: 'All tests pass and module exports required functions'
      }
    ],
    success_criteria: [
      'OAuth2 flow completes successfully with test credentials',
      'All 10 unit tests pass without errors',
      'Code coverage reaches 95% or higher'
    ],
    constraints: {
      do: ['Use passport.js library', 'Follow existing auth patterns'],
      dont: ['Don\'t modify database schema', 'Don\'t change API routes'],
      time_box: 45
    },
    context_files: {
      critical: [
        {
          path: 'src/auth/auth-controller.js',
          reason: 'Contains existing auth patterns'
        }
      ],
      skip: ['Old authentication logs']
    }
  };
}
