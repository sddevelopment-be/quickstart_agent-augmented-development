/**
 * Progressive Context Loader
 * 
 * Smart file loading with token budget management
 * Addresses Pattern 6 (incomplete context loading) from ADR-023
 * 
 * @module context-loader
 * @version 1.0.0
 * 
 * Features:
 * - Accurate token counting via tiktoken (GPT-4 encoding)
 * - Progressive loading strategy: Critical → Supporting → Skip validation
 * - Budget management with configurable limits
 * - Graceful truncation when files exceed budget
 * - Comprehensive load reporting
 * 
 * Task: 2026-01-30T1643-adr023-phase3-context-loader
 */

const fs = require('fs').promises;
const tiktoken = require('tiktoken');

/**
 * ContextLoader class for managing file loading with token budgets
 */
class ContextLoader {
  /**
   * Initialize the context loader with a token budget
   * 
   * @param {number} tokenBudget - Maximum tokens to load (default: 20000)
   */
  constructor(tokenBudget = 20000) {
    // Enforce hard limit of 150,000 tokens (model maximum)
    this.tokenBudget = Math.min(tokenBudget, 150000);
    
    // Initialize tiktoken encoding for GPT-4
    this.encoding = tiktoken.encoding_for_model('gpt-4');
    
    // Track loaded and skipped files
    this.loaded = [];
    this.skipped = [];
    this.skipList = [];
    
    // Warning threshold (80% of budget)
    this.warningThreshold = this.tokenBudget * 0.8;
  }
  
  /**
   * Estimate token count for given text using tiktoken
   * 
   * @param {string} text - Text to count tokens for
   * @returns {number} Token count
   */
  estimateTokens(text) {
    if (!text || text.length === 0) {
      return 0;
    }
    
    try {
      return this.encoding.encode(text).length;
    } catch (error) {
      console.error('Error estimating tokens:', error);
      // Fallback: rough estimation (1 token ≈ 4 characters)
      return Math.ceil(text.length / 4);
    }
  }
  
  /**
   * Load files progressively with budget management
   * 
   * @param {Object} fileList - File list with critical, supporting, and skip categories
   * @param {Array} fileList.critical - Critical files that MUST be loaded
   * @param {Array} fileList.supporting - Supporting files loaded if budget allows
   * @param {Array} fileList.skip - Files/patterns to skip
   * @param {Object} options - Loading options
   * @param {boolean} options.truncateCritical - Allow truncating critical files if needed
   * @returns {Promise<Object>} Load result with files, tokens, and metadata
   */
  async loadWithBudget(fileList, options = {}) {
    const { critical = [], supporting = [], skip = [] } = fileList;
    const { truncateCritical = false } = options;
    
    let currentTokens = 0;
    this.loaded = [];
    this.skipped = [];
    this.skipList = skip;
    
    // Phase 1: Load critical files (must fit or error/truncate)
    for (const fileSpec of critical) {
      try {
        const content = await fs.readFile(fileSpec.path, 'utf8');
        const tokens = this.estimateTokens(content);
        
        if (currentTokens + tokens > this.tokenBudget) {
          // Critical file exceeds budget
          if (truncateCritical) {
            const availableTokens = this.tokenBudget - currentTokens;
            const truncated = this.truncateToFit(content, availableTokens);
            const truncatedTokens = this.estimateTokens(truncated);
            
            this.loaded.push({
              path: fileSpec.path,
              content: truncated,
              tokens: truncatedTokens,
              truncated: true,
              reason: fileSpec.reason || 'Critical file'
            });
            currentTokens += truncatedTokens;
          } else {
            throw new Error(
              `Critical file ${fileSpec.path} (${tokens} tokens) exceeds budget. ` +
              `Available: ${this.tokenBudget - currentTokens} tokens. ` +
              `Use truncateCritical: true option to allow truncation.`
            );
          }
        } else {
          // File fits within budget
          this.loaded.push({
            path: fileSpec.path,
            content,
            tokens,
            truncated: false,
            reason: fileSpec.reason || 'Critical file'
          });
          currentTokens += tokens;
        }
      } catch (error) {
        // Re-throw with more context
        throw new Error(`Failed to load critical file ${fileSpec.path}: ${error.message}`);
      }
    }
    
    // Phase 2: Load supporting files (best effort within budget)
    for (const fileSpec of supporting || []) {
      try {
        const content = await fs.readFile(fileSpec.path, 'utf8');
        const tokens = this.estimateTokens(content);
        
        if (currentTokens + tokens <= this.tokenBudget) {
          this.loaded.push({
            path: fileSpec.path,
            content,
            tokens,
            truncated: false,
            reason: fileSpec.reason || 'Supporting file'
          });
          currentTokens += tokens;
        } else {
          // Skip supporting file if it doesn't fit
          this.skipped.push(fileSpec.path);
        }
      } catch (error) {
        // Supporting files can fail silently - just skip them
        console.warn(`Could not load supporting file ${fileSpec.path}: ${error.message}`);
        this.skipped.push(fileSpec.path);
      }
    }
    
    // Build result object
    const result = {
      files: this.loaded,
      totalTokens: currentTokens,
      budget: this.tokenBudget,
      utilizationPct: ((currentTokens / this.tokenBudget) * 100).toFixed(1) + '%',
      withinBudget: currentTokens <= this.tokenBudget,
      skipped: this.skipped,
      warnings: this._generateWarnings(currentTokens)
    };
    
    return result;
  }
  
  /**
   * Truncate content to fit within token limit
   * Uses smart truncation: keep beginning and end, mark middle as truncated
   * 
   * @param {string} content - Content to truncate
   * @param {number} tokenLimit - Maximum tokens allowed
   * @returns {string} Truncated content
   */
  truncateToFit(content, tokenLimit) {
    if (tokenLimit <= 0) {
      return '';
    }
    
    // Check if content already fits
    const currentTokens = this.estimateTokens(content);
    if (currentTokens <= tokenLimit) {
      return content;
    }
    
    // Split content into lines for better preservation of structure
    const lines = content.split('\n');
    
    // Define truncation marker
    const truncationMarker = '\n\n[... TRUNCATED: Middle section removed to fit token budget ...]\n\n';
    const markerTokens = this.estimateTokens(truncationMarker);
    
    // Reserve space for the marker
    const availableTokens = tokenLimit - markerTokens;
    
    if (availableTokens <= 0) {
      // Not even enough space for marker, return minimal content
      return '[TRUNCATED]';
    }
    
    // Try smart truncation: keep first 40%, last 30%, mark middle 30% as truncated
    const firstLineCount = Math.floor(lines.length * 0.4);
    const lastLineCount = Math.floor(lines.length * 0.3);
    
    // Build truncated content
    const firstLines = lines.slice(0, firstLineCount);
    const lastLines = lines.slice(-lastLineCount);
    
    let truncated = firstLines.join('\n') + truncationMarker + lastLines.join('\n');
    let tokens = this.estimateTokens(truncated);
    
    // If still too large, do line-by-line truncation from the beginning
    if (tokens > tokenLimit) {
      truncated = '';
      tokens = 0;
      const endMarker = '\n[... TRUNCATED: Remaining content removed to fit token budget ...]';
      const endMarkerTokens = this.estimateTokens(endMarker);
      
      for (const line of lines) {
        const lineWithNewline = line + '\n';
        const lineTokens = this.estimateTokens(lineWithNewline);
        
        // Check if adding this line plus the marker would exceed limit
        if (tokens + lineTokens + endMarkerTokens > tokenLimit) {
          truncated += endMarker;
          break;
        }
        
        truncated += lineWithNewline;
        tokens += lineTokens;
      }
      
      // Final check: ensure we're actually within limit
      tokens = this.estimateTokens(truncated);
      
      // If still over, do aggressive character-level truncation
      if (tokens > tokenLimit) {
        const charsPerToken = Math.floor(content.length / currentTokens);
        const targetChars = Math.floor(tokenLimit * charsPerToken * 0.9); // 90% safety margin
        truncated = content.substring(0, targetChars) + '\n[... TRUNCATED ...]';
      }
    }
    
    return truncated;
  }
  
  /**
   * Generate comprehensive load report
   * 
   * @returns {Object} Detailed report of loading operation
   */
  generateLoadReport() {
    const totalTokens = this.loaded.reduce((sum, file) => sum + file.tokens, 0);
    const utilizationPct = ((totalTokens / this.tokenBudget) * 100).toFixed(1) + '%';
    
    return {
      files: this.loaded.map(file => ({
        path: file.path,
        tokens: file.tokens,
        truncated: file.truncated,
        reason: file.reason
      })),
      totalTokens,
      budget: this.tokenBudget,
      utilizationPct,
      withinBudget: totalTokens <= this.tokenBudget,
      skipped: this.skipped,
      skipList: this.skipList,
      warnings: this._generateWarnings(totalTokens)
    };
  }
  
  /**
   * Get budget recommendations by task complexity
   * 
   * @returns {Object} Recommended token budgets for different task types
   */
  getBudgetRecommendations() {
    return {
      simple: 10000,      // Simple tasks: bug fixes, small features
      medium: 20000,      // Medium tasks: feature implementation, refactoring
      complex: 40000,     // Complex tasks: architecture changes, large features
      architecture: 60000 // Architecture: system design, major refactors
    };
  }
  
  /**
   * Generate warnings based on token usage
   * 
   * @private
   * @param {number} currentTokens - Current token count
   * @returns {Array<string>} List of warnings
   */
  _generateWarnings(currentTokens) {
    const warnings = [];
    
    const utilizationPct = (currentTokens / this.tokenBudget) * 100;
    
    if (utilizationPct > 80) {
      warnings.push(
        `Token budget utilization is ${utilizationPct.toFixed(1)}% (exceeds 80% threshold). ` +
        `Consider increasing budget or reducing context files.`
      );
    }
    
    if (currentTokens > this.tokenBudget) {
      warnings.push(
        `Token budget exceeded: ${currentTokens} tokens used, ` +
        `${this.tokenBudget} budget (${(currentTokens - this.tokenBudget)} over).`
      );
    }
    
    if (this.skipped.length > 0) {
      warnings.push(
        `${this.skipped.length} supporting file(s) skipped due to budget constraints.`
      );
    }
    
    return warnings;
  }
  
  /**
   * Free the tiktoken encoding resources
   */
  free() {
    if (this.encoding && typeof this.encoding.free === 'function') {
      this.encoding.free();
    }
  }
}

module.exports = ContextLoader;
