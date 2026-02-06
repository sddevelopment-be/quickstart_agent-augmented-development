/**
 * Dashboard Markdown Rendering Utility
 * 
 * Provides secure markdown-to-HTML rendering for task detail modals.
 * Implements ADR-036: Dashboard Markdown Rendering
 * 
 * Security: All HTML is sanitized through DOMPurify before DOM insertion.
 * Performance: Target <50ms for typical tasks, <200ms P95 for large tasks.
 * 
 * @module dashboard-markdown
 * @version 1.0.0
 * @requires marked.js v11.1.1+ (CDN or npm)
 * @requires DOMPurify v3.0.8+ (CDN or npm)
 */

(function(window) {
    'use strict';

    /**
     * Fields that should be rendered as markdown (not plain text)
     * Per ADR-036 technical design
     */
    const MARKDOWN_FIELDS = [
        'description',
        'context',
        'acceptance_criteria',
        'notes',
        'technical_notes'
    ];

    /**
     * Fields that should remain as plain text for easy copy-paste
     */
    const TECHNICAL_FIELDS = [
        'id',
        'title',
        'agent',
        'status',
        'priority',
        'created',
        'updated',
        'estimated_hours',
        'tags'
    ];

    /**
     * DOMPurify sanitization configuration
     * Whitelist only safe HTML tags and attributes
     */
    const SANITIZE_CONFIG = {
        ALLOWED_TAGS: [
            // Headings
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            // Text formatting
            'p', 'br', 'hr', 'strong', 'em', 'code', 'pre',
            // Lists
            'ul', 'ol', 'li',
            // Quotes
            'blockquote',
            // Links (sanitized URLs only)
            'a',
            // Tables
            'table', 'thead', 'tbody', 'tr', 'th', 'td',
            // Strikethrough
            'del',
            // Task list checkboxes (GFM)
            'input'
        ],
        ALLOWED_ATTR: [
            'href',      // Links
            'class',     // Styling classes
            'type',      // Input type (checkbox)
            'disabled',  // Disabled checkboxes
            'checked'    // Checked state
        ],
        // Only allow HTTP/HTTPS URLs (block javascript:, data:, etc.)
        ALLOWED_URI_REGEXP: /^https?:\/\//,
        // No data attributes (potential XSS vector)
        ALLOW_DATA_ATTR: false,
        // Return safe HTML string
        RETURN_DOM: false,
        RETURN_DOM_FRAGMENT: false,
        // Block external resources
        FORBID_TAGS: ['style', 'script', 'iframe', 'object', 'embed', 'link'],
        FORBID_ATTR: ['onclick', 'onerror', 'onload', 'onmouseover']
    };

    /**
     * Marked.js configuration for GitHub Flavored Markdown
     * Per ADR-036 specification
     */
    const MARKED_CONFIG = {
        gfm: true,              // GitHub Flavored Markdown
        breaks: true,           // Convert \n to <br> (GFM style)
        tables: true,           // Table support
        smartLists: true,       // Improved list parsing
        headerIds: false,       // Don't auto-generate header IDs (security)
        mangle: false,          // Don't obfuscate email addresses
        pedantic: false,        // Don't use original markdown.pl quirks
        sanitize: false         // We handle sanitization with DOMPurify
    };

    /**
     * Initialize markdown rendering configuration
     * Must be called after marked and DOMPurify are loaded
     * 
     * @returns {boolean} True if initialization successful
     */
    function initialize() {
        // Check for required libraries
        if (typeof marked === 'undefined') {
            console.error('❌ marked.js not loaded. Include: <script src="https://cdn.jsdelivr.net/npm/marked@11.1.1/marked.min.js"></script>');
            return false;
        }
        
        if (typeof DOMPurify === 'undefined') {
            console.error('❌ DOMPurify not loaded. Include: <script src="https://cdn.jsdelivr.net/npm/dompurify@3.0.8/dist/purify.min.js"></script>');
            return false;
        }

        // Configure marked
        marked.setOptions(MARKED_CONFIG);
        
        console.log('✅ Markdown rendering initialized (marked.js + DOMPurify)');
        return true;
    }

    /**
     * Render markdown string to sanitized HTML
     * 
     * @param {string} markdownText - Raw markdown text to render
     * @param {Object} options - Optional configuration overrides
     * @returns {string} Sanitized HTML string safe for innerHTML
     * 
     * @example
     * const html = renderMarkdown('## Hello\nThis is **bold**.');
     * element.innerHTML = html;
     */
    function renderMarkdown(markdownText, options = {}) {
        // Performance timing (development only)
        const startTime = performance.now();

        try {
            // Handle null/undefined/empty input
            if (!markdownText || typeof markdownText !== 'string') {
                return '';
            }

            // Trim whitespace
            const trimmed = markdownText.trim();
            if (trimmed.length === 0) {
                return '';
            }

            // Step 1: Parse markdown to HTML (marked.js)
            const rawHtml = marked.parse(trimmed);

            // Step 2: Sanitize HTML (DOMPurify)
            const sanitizeOptions = { ...SANITIZE_CONFIG, ...options.sanitize };
            const cleanHtml = DOMPurify.sanitize(rawHtml, sanitizeOptions);

            // Performance logging
            const duration = performance.now() - startTime;
            if (duration > 50) {
                console.warn(`⚠️ Slow markdown render: ${duration.toFixed(2)}ms (target: <50ms)`);
            }

            return cleanHtml;

        } catch (error) {
            console.error('❌ Markdown rendering error:', error);
            // Graceful degradation: return escaped plain text
            return escapeHtml(markdownText);
        }
    }

    /**
     * Render a task field based on its type (markdown vs. technical)
     * 
     * @param {HTMLElement} element - DOM element to render into
     * @param {string} fieldName - Field name (e.g., 'description', 'id')
     * @param {any} fieldValue - Field value to render
     * @param {Object} options - Optional rendering options
     * 
     * @example
     * renderField(descElement, 'description', task.description);
     * renderField(idElement, 'id', task.id);
     */
    function renderField(element, fieldName, fieldValue, options = {}) {
        if (!element) {
            console.error('❌ renderField: Invalid element');
            return;
        }

        // Handle null/undefined
        if (fieldValue === null || fieldValue === undefined) {
            element.textContent = '';
            return;
        }

        // Convert to string (handle objects properly)
        let value;
        if (typeof fieldValue === 'object') {
            // Convert object to YAML-like format for readability
            value = Object.entries(fieldValue)
                .map(([key, val]) => {
                    if (Array.isArray(val)) {
                        return `${key}:\n  - ${val.join('\n  - ')}`;
                    } else if (typeof val === 'object' && val !== null) {
                        return `${key}: ${JSON.stringify(val, null, 2)}`;
                    } else {
                        return `${key}: ${val}`;
                    }
                })
                .join('\n');
        } else {
            value = String(fieldValue);
        }

        // Determine rendering strategy
        if (MARKDOWN_FIELDS.includes(fieldName)) {
            // Render as markdown
            const html = renderMarkdown(value, options);
            element.innerHTML = html;
            element.classList.add('markdown-rendered');
        } else {
            // Render as plain text (safe for technical fields)
            element.textContent = value;
            element.classList.add('plain-text');
        }
    }

    /**
     * Render all fields of a task object into a container
     * Automatically determines which fields are markdown vs. technical
     * 
     * @param {Object} task - Task object with various fields
     * @param {HTMLElement} container - Container element for rendering
     * @param {Object} fieldMapping - Map of field names to element selectors
     * 
     * @example
     * renderTaskFields(taskData, modalBody, {
     *   'description': '#task-description',
     *   'id': '#task-id',
     *   'priority': '#task-priority'
     * });
     */
    function renderTaskFields(task, container, fieldMapping) {
        if (!task || typeof task !== 'object') {
            console.error('❌ renderTaskFields: Invalid task object');
            return;
        }

        if (!container) {
            console.error('❌ renderTaskFields: Invalid container element');
            return;
        }

        Object.keys(fieldMapping).forEach(fieldName => {
            const selector = fieldMapping[fieldName];
            const element = container.querySelector(selector);
            
            if (element) {
                const value = task[fieldName];
                renderField(element, fieldName, value);
            } else {
                console.warn(`⚠️ Element not found for field '${fieldName}' (selector: ${selector})`);
            }
        });
    }

    /**
     * Check if a field should be rendered as markdown
     * 
     * @param {string} fieldName - Field name to check
     * @returns {boolean} True if field should be rendered as markdown
     */
    function isMarkdownField(fieldName) {
        return MARKDOWN_FIELDS.includes(fieldName);
    }

    /**
     * Check if a field should be rendered as plain text
     * 
     * @param {string} fieldName - Field name to check
     * @returns {boolean} True if field should be rendered as plain text
     */
    function isTechnicalField(fieldName) {
        return TECHNICAL_FIELDS.includes(fieldName);
    }

    /**
     * Escape HTML special characters (fallback for error cases)
     * 
     * @param {string} text - Text to escape
     * @returns {string} HTML-escaped text
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Performance benchmark for markdown rendering
     * Used for testing and optimization
     * 
     * @param {string} markdownText - Text to benchmark
     * @param {number} iterations - Number of iterations (default: 100)
     * @returns {Object} Performance metrics
     */
    function benchmark(markdownText, iterations = 100) {
        const times = [];
        
        for (let i = 0; i < iterations; i++) {
            const start = performance.now();
            renderMarkdown(markdownText);
            const end = performance.now();
            times.push(end - start);
        }

        times.sort((a, b) => a - b);
        
        return {
            iterations,
            mean: times.reduce((a, b) => a + b, 0) / times.length,
            median: times[Math.floor(times.length / 2)],
            p95: times[Math.floor(times.length * 0.95)],
            p99: times[Math.floor(times.length * 0.99)],
            min: times[0],
            max: times[times.length - 1]
        };
    }

    // Public API
    const MarkdownRenderer = {
        initialize,
        renderMarkdown,
        renderField,
        renderTaskFields,
        isMarkdownField,
        isTechnicalField,
        benchmark,
        
        // Configuration access (read-only)
        config: {
            markdownFields: MARKDOWN_FIELDS,
            technicalFields: TECHNICAL_FIELDS,
            sanitizeConfig: SANITIZE_CONFIG,
            markedConfig: MARKED_CONFIG
        }
    };

    // Expose to global scope
    window.MarkdownRenderer = MarkdownRenderer;

    // Auto-initialize when libraries are available
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            // Small delay to ensure CDN scripts loaded
            setTimeout(() => MarkdownRenderer.initialize(), 100);
        });
    } else {
        setTimeout(() => MarkdownRenderer.initialize(), 100);
    }

})(window);
