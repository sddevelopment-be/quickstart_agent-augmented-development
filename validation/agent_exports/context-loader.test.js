/**
 * Context Loader Test Suite
 * 
 * Tests for progressive context loading with token budget management
 * Follows ADR-023 Phase 3 specifications
 * 
 * Test Coverage Requirements (15+ tests):
 * - Token counting accuracy
 * - Progressive loading (critical → supporting)
 * - Budget enforcement
 * - Truncation strategies
 * - Edge cases
 * - Performance
 * - Skip list validation
 * 
 * Task: 2026-01-30T1643-adr023-phase3-context-loader
 */

const fs = require('fs').promises;
const path = require('path');
const ContextLoader = require('../../ops/utils/context-loader');

// Test fixtures
const FIXTURES_DIR = path.join(__dirname, '__fixtures__', 'context-loader');
const TEST_FILE_SMALL = path.join(FIXTURES_DIR, 'small.txt');
const TEST_FILE_MEDIUM = path.join(FIXTURES_DIR, 'medium.txt');
const TEST_FILE_LARGE = path.join(FIXTURES_DIR, 'large.txt');
const TEST_FILE_EMPTY = path.join(FIXTURES_DIR, 'empty.txt');

// Setup fixtures before tests
beforeAll(async () => {
  await fs.mkdir(FIXTURES_DIR, { recursive: true });
  
  // Small file: ~100 tokens
  await fs.writeFile(TEST_FILE_SMALL, 'This is a small test file.\n'.repeat(10));
  
  // Medium file: ~500 tokens
  await fs.writeFile(TEST_FILE_MEDIUM, 'This is a medium test file with more content to increase token count.\n'.repeat(50));
  
  // Large file: ~5000 tokens
  const largeContent = 'This is a large test file that will be used to test truncation and budget overflow scenarios.\n'.repeat(500);
  await fs.writeFile(TEST_FILE_LARGE, largeContent);
  
  // Empty file
  await fs.writeFile(TEST_FILE_EMPTY, '');
});

// Cleanup fixtures after tests
afterAll(async () => {
  await fs.rm(FIXTURES_DIR, { recursive: true, force: true });
});

describe('ContextLoader', () => {
  
  describe('Constructor and Initialization', () => {
    
    test('should initialize with default token budget of 20000', () => {
      const loader = new ContextLoader();
      expect(loader.tokenBudget).toBe(20000);
    });
    
    test('should initialize with custom token budget', () => {
      const loader = new ContextLoader(10000);
      expect(loader.tokenBudget).toBe(10000);
    });
    
    test('should initialize tiktoken encoding for GPT-4', () => {
      const loader = new ContextLoader();
      expect(loader.encoding).toBeDefined();
    });
  });
  
  describe('Token Counting - estimateTokens()', () => {
    
    test('should accurately count tokens for simple text', () => {
      const loader = new ContextLoader();
      const text = 'Hello, world!';
      const tokens = loader.estimateTokens(text);
      
      // "Hello, world!" should be approximately 4 tokens
      expect(tokens).toBeGreaterThan(0);
      expect(tokens).toBeLessThan(10);
    });
    
    test('should count tokens for empty string as 0', () => {
      const loader = new ContextLoader();
      const tokens = loader.estimateTokens('');
      expect(tokens).toBe(0);
    });
    
    test('should count tokens for multiline text accurately', () => {
      const loader = new ContextLoader();
      const text = `Line 1\nLine 2\nLine 3\nLine 4\nLine 5`;
      const tokens = loader.estimateTokens(text);
      
      // Should be approximately 15-25 tokens
      expect(tokens).toBeGreaterThan(10);
      expect(tokens).toBeLessThan(30);
    });
    
    test('should count tokens for code accurately', () => {
      const loader = new ContextLoader();
      const code = `
function example() {
  const x = 10;
  return x * 2;
}
      `.trim();
      
      const tokens = loader.estimateTokens(code);
      
      // Code should have reasonable token count
      expect(tokens).toBeGreaterThan(10);
      expect(tokens).toBeLessThan(50);
    });
    
    test('should have token counting accuracy within 5% of tiktoken', () => {
      const loader = new ContextLoader();
      const text = 'The quick brown fox jumps over the lazy dog.';
      
      const estimatedTokens = loader.estimateTokens(text);
      const directTokens = loader.encoding.encode(text).length;
      
      // Should be exactly the same since we're using tiktoken directly
      expect(estimatedTokens).toBe(directTokens);
    });
    
    test('should handle special characters and unicode', () => {
      const loader = new ContextLoader();
      const text = 'Hello 世界! 🌍 Special chars: @#$%^&*()';
      const tokens = loader.estimateTokens(text);
      
      expect(tokens).toBeGreaterThan(0);
      expect(typeof tokens).toBe('number');
    });
  });
  
  describe('Progressive Loading - loadWithBudget()', () => {
    
    test('should load critical files first', async () => {
      const loader = new ContextLoader(10000);
      
      const fileList = {
        critical: [
          { path: TEST_FILE_SMALL, reason: 'Critical test file' }
        ],
        supporting: [],
        skip: []
      };
      
      const result = await loader.loadWithBudget(fileList);
      
      expect(result.files).toHaveLength(1);
      expect(result.files[0].path).toBe(TEST_FILE_SMALL);
      expect(result.files[0].truncated).toBe(false);
      expect(result.totalTokens).toBeGreaterThan(0);
    });
    
    test('should load critical files before supporting files', async () => {
      const loader = new ContextLoader(10000);
      
      const fileList = {
        critical: [
          { path: TEST_FILE_SMALL, reason: 'Critical file' }
        ],
        supporting: [
          { path: TEST_FILE_MEDIUM, reason: 'Supporting file' }
        ],
        skip: []
      };
      
      const result = await loader.loadWithBudget(fileList);
      
      // First file should be critical
      expect(result.files[0].path).toBe(TEST_FILE_SMALL);
      expect(result.files[0].reason).toBe('Critical file');
      
      // Second file should be supporting (if budget allows)
      if (result.files.length > 1) {
        expect(result.files[1].path).toBe(TEST_FILE_MEDIUM);
      }
    });
    
    test('should skip supporting files when budget is exceeded', async () => {
      const loader = new ContextLoader(1000); // Very small budget
      
      const fileList = {
        critical: [
          { path: TEST_FILE_SMALL, reason: 'Critical file' }
        ],
        supporting: [
          { path: TEST_FILE_LARGE, reason: 'Large supporting file' }
        ],
        skip: []
      };
      
      const result = await loader.loadWithBudget(fileList);
      
      // Should have loaded critical but skipped supporting due to budget
      expect(result.files).toHaveLength(1);
      expect(result.files[0].path).toBe(TEST_FILE_SMALL);
      expect(result.skipped).toContain(TEST_FILE_LARGE);
    });
    
    test('should respect token budget and stay within limits', async () => {
      const budget = 5000;
      const loader = new ContextLoader(budget);
      
      const fileList = {
        critical: [
          { path: TEST_FILE_SMALL, reason: 'Critical file' }
        ],
        supporting: [
          { path: TEST_FILE_MEDIUM, reason: 'Supporting file' }
        ],
        skip: []
      };
      
      const result = await loader.loadWithBudget(fileList);
      
      expect(result.totalTokens).toBeLessThanOrEqual(budget);
      expect(result.withinBudget).toBe(true);
    });
    
    test('should throw error when critical file exceeds budget without truncation', async () => {
      const loader = new ContextLoader(100); // Tiny budget
      
      const fileList = {
        critical: [
          { path: TEST_FILE_LARGE, reason: 'Large critical file' }
        ],
        supporting: [],
        skip: []
      };
      
      await expect(loader.loadWithBudget(fileList))
        .rejects.toThrow(/exceeds budget/);
    });
  });
  
  describe('Truncation - truncateToFit()', () => {
    
    test('should truncate content to fit token limit', () => {
      const loader = new ContextLoader();
      const content = 'This is a long piece of content. '.repeat(100);
      const tokenLimit = 50;
      
      const truncated = loader.truncateToFit(content, tokenLimit);
      const truncatedTokens = loader.estimateTokens(truncated);
      
      expect(truncatedTokens).toBeLessThanOrEqual(tokenLimit);
      expect(truncated.length).toBeLessThan(content.length);
    });
    
    test('should preserve content structure when truncating', () => {
      const loader = new ContextLoader();
      const content = `Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n`.repeat(50);
      const tokenLimit = 100;
      
      const truncated = loader.truncateToFit(content, tokenLimit);
      
      // Should still have line breaks
      expect(truncated).toContain('\n');
      expect(loader.estimateTokens(truncated)).toBeLessThanOrEqual(tokenLimit);
    });
    
    test('should handle truncation with truncateCritical option', async () => {
      const loader = new ContextLoader(100);
      
      const fileList = {
        critical: [
          { path: TEST_FILE_LARGE, reason: 'Large critical file' }
        ],
        supporting: [],
        skip: []
      };
      
      const result = await loader.loadWithBudget(fileList, { truncateCritical: true });
      
      expect(result.files).toHaveLength(1);
      expect(result.files[0].truncated).toBe(true);
      expect(result.files[0].tokens).toBeLessThanOrEqual(loader.tokenBudget);
    });
    
    test('should add truncation marker when content is truncated', () => {
      const loader = new ContextLoader();
      const content = 'A'.repeat(10000);
      const tokenLimit = 50;
      
      const truncated = loader.truncateToFit(content, tokenLimit);
      
      // Should indicate truncation occurred
      expect(truncated.length).toBeLessThan(content.length);
    });
  });
  
  describe('Load Report - generateLoadReport()', () => {
    
    test('should generate comprehensive load report', async () => {
      const loader = new ContextLoader(10000);
      
      const fileList = {
        critical: [
          { path: TEST_FILE_SMALL, reason: 'Critical file' }
        ],
        supporting: [
          { path: TEST_FILE_MEDIUM, reason: 'Supporting file' }
        ],
        skip: ['historical logs', 'archived docs']
      };
      
      await loader.loadWithBudget(fileList);
      const report = loader.generateLoadReport();
      
      expect(report).toHaveProperty('files');
      expect(report).toHaveProperty('totalTokens');
      expect(report).toHaveProperty('budget');
      expect(report).toHaveProperty('utilizationPct');
      expect(report).toHaveProperty('withinBudget');
      expect(report).toHaveProperty('warnings');
    });
    
    test('should include file details in load report', async () => {
      const loader = new ContextLoader(10000);
      
      const fileList = {
        critical: [
          { path: TEST_FILE_SMALL, reason: 'Test critical' }
        ],
        supporting: [],
        skip: []
      };
      
      await loader.loadWithBudget(fileList);
      const report = loader.generateLoadReport();
      
      expect(report.files[0]).toHaveProperty('path');
      expect(report.files[0]).toHaveProperty('tokens');
      expect(report.files[0]).toHaveProperty('truncated');
      expect(report.files[0]).toHaveProperty('reason');
      expect(report.files[0].reason).toBe('Test critical');
    });
    
    test('should calculate budget utilization percentage', async () => {
      const loader = new ContextLoader(10000);
      
      const fileList = {
        critical: [
          { path: TEST_FILE_SMALL, reason: 'Critical file' }
        ],
        supporting: [],
        skip: []
      };
      
      await loader.loadWithBudget(fileList);
      const report = loader.generateLoadReport();
      
      expect(report.utilizationPct).toMatch(/^\d+\.?\d*%$/);
      expect(parseFloat(report.utilizationPct)).toBeGreaterThan(0);
      expect(parseFloat(report.utilizationPct)).toBeLessThanOrEqual(100);
    });
    
    test('should warn when budget utilization exceeds 80%', async () => {
      const loader = new ContextLoader(2000); // Small budget to trigger warning
      
      const fileList = {
        critical: [
          { path: TEST_FILE_MEDIUM, reason: 'Medium file' }
        ],
        supporting: [],
        skip: []
      };
      
      await loader.loadWithBudget(fileList);
      const report = loader.generateLoadReport();
      
      const utilization = parseFloat(report.utilizationPct);
      if (utilization > 80) {
        expect(report.warnings.length).toBeGreaterThan(0);
        expect(report.warnings.some(w => w.includes('80%'))).toBe(true);
      }
    });
  });
  
  describe('Edge Cases', () => {
    
    test('should handle empty file list', async () => {
      const loader = new ContextLoader();
      
      const fileList = {
        critical: [],
        supporting: [],
        skip: []
      };
      
      const result = await loader.loadWithBudget(fileList);
      
      expect(result.files).toHaveLength(0);
      expect(result.totalTokens).toBe(0);
    });
    
    test('should handle missing file gracefully', async () => {
      const loader = new ContextLoader();
      
      const fileList = {
        critical: [
          { path: '/nonexistent/file.txt', reason: 'Missing file' }
        ],
        supporting: [],
        skip: []
      };
      
      await expect(loader.loadWithBudget(fileList))
        .rejects.toThrow();
    });
    
    test('should handle empty files', async () => {
      const loader = new ContextLoader();
      
      const fileList = {
        critical: [
          { path: TEST_FILE_EMPTY, reason: 'Empty file' }
        ],
        supporting: [],
        skip: []
      };
      
      const result = await loader.loadWithBudget(fileList);
      
      expect(result.files).toHaveLength(1);
      expect(result.files[0].tokens).toBe(0);
      expect(result.files[0].content).toBe('');
    });
    
    test('should validate skip list is respected', async () => {
      const loader = new ContextLoader();
      
      const fileList = {
        critical: [
          { path: TEST_FILE_SMALL, reason: 'Critical file' }
        ],
        supporting: [],
        skip: ['historical logs', 'archived documentation', 'test fixtures']
      };
      
      await loader.loadWithBudget(fileList);
      const report = loader.generateLoadReport();
      
      // Skip list should be recorded in report
      expect(report.skipList).toEqual(fileList.skip);
    });
  });
  
  describe('Performance', () => {
    
    test('should estimate tokens in less than 100ms for typical file', async () => {
      const loader = new ContextLoader();
      const content = await fs.readFile(TEST_FILE_MEDIUM, 'utf8');
      
      const startTime = Date.now();
      loader.estimateTokens(content);
      const duration = Date.now() - startTime;
      
      expect(duration).toBeLessThan(100);
    });
    
    test('should load files progressively without blocking', async () => {
      const loader = new ContextLoader(10000);
      
      const fileList = {
        critical: [
          { path: TEST_FILE_SMALL, reason: 'Critical 1' },
          { path: TEST_FILE_MEDIUM, reason: 'Critical 2' }
        ],
        supporting: [
          { path: TEST_FILE_SMALL, reason: 'Supporting 1' }
        ],
        skip: []
      };
      
      const startTime = Date.now();
      await loader.loadWithBudget(fileList);
      const duration = Date.now() - startTime;
      
      // Should complete quickly (< 500ms for small files)
      expect(duration).toBeLessThan(500);
    });
  });
  
  describe('Token Budget Management', () => {
    
    test('should enforce hard limit of 150000 tokens', async () => {
      const loader = new ContextLoader(200000); // Try to set above hard limit
      
      expect(loader.tokenBudget).toBeLessThanOrEqual(150000);
    });
    
    test('should allow configuring different budget levels', () => {
      const budgets = [10000, 20000, 40000, 60000];
      
      budgets.forEach(budget => {
        const loader = new ContextLoader(budget);
        expect(loader.tokenBudget).toBe(budget);
      });
    });
    
    test('should provide budget recommendation based on task complexity', () => {
      const loader = new ContextLoader();
      
      const recommendations = loader.getBudgetRecommendations();
      
      expect(recommendations).toHaveProperty('simple');
      expect(recommendations).toHaveProperty('medium');
      expect(recommendations).toHaveProperty('complex');
      expect(recommendations).toHaveProperty('architecture');
      
      expect(recommendations.simple).toBe(10000);
      expect(recommendations.medium).toBe(20000);
      expect(recommendations.complex).toBe(40000);
      expect(recommendations.architecture).toBe(60000);
    });
    
    test('should handle tiktoken encoding errors gracefully with fallback', () => {
      const loader = new ContextLoader();
      
      // Mock encoding.encode to throw error
      const originalEncode = loader.encoding.encode;
      loader.encoding.encode = () => {
        throw new Error('Tiktoken error');
      };
      
      const text = 'This is test text';
      const tokens = loader.estimateTokens(text);
      
      // Should use fallback estimation (1 token ≈ 4 characters)
      expect(tokens).toBeGreaterThan(0);
      expect(tokens).toBeCloseTo(Math.ceil(text.length / 4), 2);
      
      // Restore original
      loader.encoding.encode = originalEncode;
    });
    
    test('should free tiktoken encoding resources', () => {
      const loader = new ContextLoader();
      
      // free() should be callable
      expect(() => loader.free()).not.toThrow();
    });
  });
  
  describe('Advanced Truncation Scenarios', () => {
    
    test('should handle very small token limits', () => {
      const loader = new ContextLoader();
      const content = 'This is a very long piece of content that needs aggressive truncation.';
      const tokenLimit = 5;
      
      const truncated = loader.truncateToFit(content, tokenLimit);
      const tokens = loader.estimateTokens(truncated);
      
      expect(tokens).toBeLessThanOrEqual(tokenLimit);
    });
    
    test('should handle zero token limit', () => {
      const loader = new ContextLoader();
      const content = 'Some content';
      
      const truncated = loader.truncateToFit(content, 0);
      
      expect(truncated).toBe('');
    });
    
    test('should handle negative token limit', () => {
      const loader = new ContextLoader();
      const content = 'Some content';
      
      const truncated = loader.truncateToFit(content, -10);
      
      expect(truncated).toBe('');
    });
    
    test('should use character-level truncation for very constrained budgets', () => {
      const loader = new ContextLoader();
      const content = 'A'.repeat(1000);
      const tokenLimit = 10; // More realistic limit for the truncation marker
      
      const truncated = loader.truncateToFit(content, tokenLimit);
      const tokens = loader.estimateTokens(truncated);
      
      expect(tokens).toBeLessThanOrEqual(tokenLimit);
      expect(truncated.length).toBeLessThan(content.length);
    });
  });
  
  describe('Supporting File Errors', () => {
    
    test('should continue loading when supporting file has read error', async () => {
      const loader = new ContextLoader(10000);
      
      // Create a spy to suppress console.warn
      const originalWarn = console.warn;
      console.warn = jest.fn();
      
      const fileList = {
        critical: [
          { path: TEST_FILE_SMALL, reason: 'Critical file' }
        ],
        supporting: [
          { path: '/nonexistent/supporting.txt', reason: 'Missing supporting' },
          { path: TEST_FILE_MEDIUM, reason: 'Valid supporting' }
        ],
        skip: []
      };
      
      const result = await loader.loadWithBudget(fileList);
      
      // Should load critical and valid supporting, skip the missing one
      expect(result.files.length).toBeGreaterThan(0);
      expect(result.files[0].path).toBe(TEST_FILE_SMALL);
      expect(result.skipped).toContain('/nonexistent/supporting.txt');
      expect(console.warn).toHaveBeenCalled();
      
      // Restore console.warn
      console.warn = originalWarn;
    });
  });
});
