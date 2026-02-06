# ADR-036: Dashboard Markdown Rendering

**Status:** Accepted  
**Date:** 2026-02-06  
**Deciders:** Architect Alphonso, Human-in-Charge  
**Related Specs:** [Markdown Rendering Specification](../../specifications/llm-dashboard/markdown-rendering.md)  
**Related ADRs:** [ADR-032: Real-Time Execution Dashboard](ADR-032-real-time-execution-dashboard.md)

---

## Context

Task detail modals in the dashboard currently display all fields as plain text. Fields like `description`, `context`, and `acceptance_criteria` often contain structured markdown (headings, lists, code blocks) that renders as unformatted raw strings. This degrades readability and makes task comprehension time-consuming.

**Problem Statement:**  
Users need formatted markdown rendering in task detail views to quickly understand structured task information.

**Constraints:**
- MUST sanitize HTML to prevent XSS attacks
- MUST support CommonMark + GitHub Flavored Markdown (GFM)
- MUST preserve technical field copy-paste (IDs, agent names, statuses)
- MUST NOT slow down modal rendering (<50ms typical, <200ms P95)

---

## Decision

Implement client-side markdown rendering using **Marked.js** (parser) and **DOMPurify** (sanitizer) with the following architecture:

### Solution Components

**1. Markdown Parser Selection**

| Library | Size | Performance | Extensibility | Decision |
|---------|------|-------------|---------------|----------|
| marked.js | 25KB | Fast | Excellent | ✅ **Selected** |
| markdown-it | 85KB | Moderate | Good | ❌ Too heavy |
| showdown | 75KB | Slow | Fair | ❌ Performance issues |
| micromark | 15KB | Fastest | Complex API | ❌ Overkill for needs |

**Rationale:** `marked.js` provides best balance of size, speed, and GFM extension support.

**2. HTML Sanitization**

| Library | XSS Protection | Whitelist Control | Decision |
|---------|----------------|-------------------|----------|
| DOMPurify | Excellent | Comprehensive | ✅ **Selected** |
| sanitize-html | Good | Manual config | ❌ More complex |
| xss | Fair | Limited control | ❌ Less robust |

**Rationale:** DOMPurify is industry-standard with battle-tested XSS protection.

**3. Rendering Strategy**

```javascript
// Selective rendering—only markdown-compatible fields
const MARKDOWN_FIELDS = ['description', 'context', 'acceptance_criteria', 'notes'];

function renderTaskModal(task) {
  Object.keys(task).forEach(field => {
    if (MARKDOWN_FIELDS.includes(field)) {
      // Parse markdown → sanitize HTML → render
      const html = marked.parse(task[field]);
      const clean = DOMPurify.sanitize(html);
      document.querySelector(`#task-${field}`).innerHTML = clean;
    } else {
      // Technical fields: plain text for easy copying
      document.querySelector(`#task-${field}`).textContent = task[field];
    }
  });
}
```

**4. GFM Extensions Configuration**

```javascript
marked.setOptions({
  gfm: true,                // GitHub Flavored Markdown
  breaks: true,             // Treat \n as <br> (GFM style)
  tables: true,             // Table support
  smartLists: true,         // Better list parsing
  headerIds: false,         // No auto-ID generation (security)
  mangle: false             // Don't obfuscate emails
});
```

**5. Content Security Policy (CSP)**

Add CSP header to prevent inline script execution:
```
Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'
```

---

## Alternatives Considered

### Alternative 1: Server-Side Rendering (Rejected)
**Approach:** Parse markdown in Flask backend, send HTML to frontend  
**Pros:** Centralized sanitization, cached results possible  
**Cons:** Increases server load, adds network latency, complicates caching  
**Decision:** Client-side rendering faster and scales better

### Alternative 2: Raw Markdown Display with Syntax Highlighting (Rejected)
**Approach:** Show raw markdown with syntax colors (like code editor)  
**Pros:** No XSS risk, preserves exact formatting  
**Cons:** Users still read raw syntax; doesn't solve readability problem  
**Decision:** Rendering provides actual usability improvement

### Alternative 3: Full WYSIWYG Markdown Editor (Rejected)
**Approach:** Replace text areas with markdown editor like SimpleMDE  
**Pros:** Live preview while editing  
**Cons:** Massive complexity increase; tasks not edited in dashboard  
**Decision:** Read-only rendering sufficient for current needs

---

## Consequences

### Positive

- ✅ **Improved Readability:** Structured information easier to scan and understand
- ✅ **Professional Appearance:** Renders code blocks, tables, and lists properly
- ✅ **GFM Compatibility:** Tasks written with GFM syntax render correctly
- ✅ **No Server Changes:** Pure client-side implementation, no backend modifications

### Negative

- ⚠️ **Security Surface:** Markdown parsing + HTML rendering increases XSS risk
- ⚠️ **Bundle Size:** Adds ~40KB to frontend bundle (marked + DOMPurify)
- ⚠️ **Rendering Performance:** Complex markdown may slow modal opening

### Mitigations

- **Security:** DOMPurify sanitization with strict whitelist (tested against OWASP XSS payloads)
- **Bundle Size:** Load libraries asynchronously, cache aggressively
- **Performance:** Render markdown only on modal open (lazy rendering)

---

## Implementation Plan

### Phase 1: Library Integration (2 hours)
- Add marked.js and DOMPurify via CDN (or npm)
- Configure marked with GFM extensions
- Create markdown rendering utility module
- Unit tests for XSS prevention

### Phase 2: Selective Rendering (3 hours)
- Identify markdown fields vs. technical fields
- Update task detail modal rendering logic
- Add CSS styling for markdown elements
- Handle edge cases (empty fields, malformed markdown)

### Phase 3: Security Hardening (2 hours)
- Configure DOMPurify sanitizer whitelist
- Add CSP headers to Flask app
- XSS attack testing (OWASP payloads)
- Fuzzing with malformed markdown

### Phase 4: Visual Polish & Testing (2 hours)
- Style code blocks with syntax highlighting
- Responsive table styling
- Cross-browser testing (Chrome, Firefox, Safari)
- Performance profiling (<50ms typical tasks)

**Total Effort:** 9-11 hours

---

## Technical Design

### Rendering Pipeline

```
┌─────────────────────────────────────────────────┐
│         Task Detail Modal Opened                │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│    Identify Field Type (Technical vs Markdown)  │
│    Technical: id, agent, title, status, priority│
│    Markdown: description, context, notes, AC    │
└─────────────────┬───────────────────────────────┘
                  │
       ┌──────────┴───────────┐
       │                      │
       ▼                      ▼
┌──────────────┐      ┌──────────────────┐
│ Technical    │      │ Markdown Field   │
│ Field        │      │                  │
│              │      │ 1. Parse (marked)│
│ Render as    │      │ 2. Sanitize      │
│ plain text   │      │    (DOMPurify)   │
│ (textContent)│      │ 3. Render HTML   │
│              │      │    (innerHTML)   │
└──────────────┘      └──────────────────┘
       │                      │
       └──────────┬───────────┘
                  ▼
         ┌─────────────────┐
         │ Apply CSS       │
         │ Styling         │
         └─────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Measure Render  │
         │ Performance     │
         │ (<50ms target)  │
         └─────────────────┘
```

### Security Architecture

```
User Input (YAML field)
       │
       ▼
┌──────────────────────────────────────┐
│ Marked.js Parser                     │
│ (Converts markdown → HTML AST)       │
└──────────────┬───────────────────────┘
               │ Raw HTML
               ▼
┌──────────────────────────────────────┐
│ DOMPurify Sanitizer                  │
│ - Remove <script> tags               │
│ - Strip javascript: URLs             │
│ - Block data: URIs (except images)   │
│ - Whitelist safe HTML tags           │
└──────────────┬───────────────────────┘
               │ Safe HTML
               ▼
┌──────────────────────────────────────┐
│ DOM Insertion (.innerHTML)           │
│ Protected by CSP header              │
└──────────────────────────────────────┘
               │
               ▼
         Rendered in Browser
```

### Field Classification

| Field | Type | Rendering | Rationale |
|-------|------|-----------|-----------|
| `id` | Technical | Plain text | Copy-paste for referencing tasks |
| `title` | Technical | Plain text | Short, no formatting needed |
| `agent` | Technical | Plain text | Copy-paste for agent names |
| `status` | Technical | Badge component | Visual indicator, not text |
| `priority` | Technical | Badge/dropdown | Interactive component |
| `description` | Markdown | Rendered | Often multi-paragraph with structure |
| `context` | Markdown | Rendered | May contain links, code snippets |
| `acceptance_criteria` | Markdown | Rendered | Usually bulleted lists |
| `notes` | Markdown | Rendered | Free-form text with formatting |
| `created` | Technical | Formatted date | Date formatting, not markdown |
| `updated` | Technical | Formatted date | Date formatting, not markdown |

---

## Security Considerations

### XSS Attack Vectors

| Attack Type | Example Payload | Mitigation |
|-------------|-----------------|------------|
| Script injection | `<script>alert(1)</script>` | DOMPurify removes `<script>` |
| Event handlers | `<img onerror="alert(1)">` | DOMPurify strips event attributes |
| JavaScript URLs | `[Click](javascript:alert(1))` | DOMPurify blocks `javascript:` protocol |
| Data URLs | `[File](data:text/html,<script>...)` | DOMPurify blocks `data:` (except images) |
| Malformed HTML | `<div><script>alert(1)` | Marked parser handles gracefully |
| Unicode attacks | `\u003cscript\u003e` | DOMPurify normalizes Unicode |

### DOMPurify Configuration

```javascript
DOMPurify.sanitize(html, {
  ALLOWED_TAGS: [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'br', 'hr',
    'strong', 'em', 'code', 'pre',
    'ul', 'ol', 'li',
    'blockquote',
    'a', 'img',
    'table', 'thead', 'tbody', 'tr', 'th', 'td'
  ],
  ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class'],
  ALLOWED_URI_REGEXP: /^https?:\/\//,  // Only http/https links
  ALLOW_DATA_ATTR: false
});
```

### Content Security Policy

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline';  # Allow markdown-generated inline styles
  img-src 'self' https:;             # Allow HTTPS images
  connect-src 'self' ws://localhost:8080;  # WebSocket connection
```

---

## Performance Characteristics

### Benchmarks (Target)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Typical task (500 chars) | <50ms | Parse + sanitize + render |
| Large task (5000 chars) | <200ms | Parse + sanitize + render |
| Initial library load | <100ms | CDN cached, async loaded |
| Bundle size impact | +40KB | marked (25KB) + DOMPurify (15KB) |

### Optimization Strategies

1. **Lazy Loading:** Load marked/DOMPurify only when modal first opened
2. **Caching:** Cache rendered HTML (keyed by task ID + updated timestamp)
3. **Incremental Rendering:** Render above-fold content first
4. **Web Workers:** Move parsing to background thread for large tasks (future)

---

## Testing Strategy

### Unit Tests
- Markdown parsing (headings, lists, code blocks, tables)
- XSS payload rejection (OWASP Top 10)
- Field classification (technical vs. markdown)
- Empty/null field handling

### Integration Tests
- End-to-end: YAML → rendered HTML in modal
- Cross-browser rendering consistency
- Performance benchmarks (typical + large tasks)

### Security Tests
- **XSS Payloads:** Test OWASP XSS filter evasion cheat sheet
- **Malformed Markdown:** Fuzz testing with random input
- **CSP Violations:** Attempt to inject scripts, verify blocked

### Manual Tests
- Visual comparison: raw vs. rendered markdown
- Mobile responsive rendering
- Link clicking (external links open in new tab)

---

## Open Questions

✅ None—all resolved with stakeholder.

---

## References

- **Specification:** `specifications/llm-dashboard/markdown-rendering.md`
- **Marked.js Documentation:** https://marked.js.org/
- **DOMPurify Documentation:** https://github.com/cure53/DOMPurify
- **OWASP XSS Prevention:** https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- **CommonMark Spec:** https://commonmark.org/
- **GFM Spec:** https://github.github.com/gfm/

---

**Author:** Architect Alphonso  
**Reviewers:** Human-in-Charge, Frontend Specialist  
**Status:** Accepted (awaiting approval)  
**Next Steps:** Approval → Create implementation tasks → Assign to Frontend
