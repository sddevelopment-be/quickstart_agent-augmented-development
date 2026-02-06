# Specification: Dashboard Markdown Rendering in Task Details

**Status:** Draft  
**Created:** 2026-02-06  
**Last Updated:** 2026-02-06  
**Author:** Analyst Annie  
**Stakeholders:** Human-in-Charge, Software Engineers, Agentic Framework Core Team

---

## User Story

**As a** Software Engineer reviewing tasks in the dashboard  
**I want** task descriptions and context rendered as formatted markdown  
**So that** I can read complex task details with proper formatting instead of raw text

**Alternative: Acceptance Criterion Format**  
**Given** I am viewing a task detail modal  
**When** The task has markdown formatting in description or context fields  
**Then** The markdown is rendered as HTML with proper formatting (headers, lists, code blocks, emphasis)  
**Unless** The field contains only plain text (no markdown syntax detected)

**Target Personas:**
- Software Engineer (Primary) - Needs readable task descriptions with code examples
- Agentic Framework Core Team (Primary) - Writes complex task descriptions with structured content
- Documentation Writer (Secondary) - Creates well-formatted task specifications

---

## Overview

Markdown rendering transforms raw text task descriptions into properly formatted HTML, improving readability for complex tasks that include code blocks, numbered steps, bullet lists, and emphasis. This solves the "raw text wall" problem where markdown syntax makes task details harder to read instead of easier.

**Context:**
- **Problem Solved:** Task descriptions with markdown syntax (###, ```, **, etc.) display as raw text, reducing readability
- **Why Needed Now:** Dashboard is primary task review interface; tasks increasingly include formatted content
- **Constraints:**
  - MUST sanitize HTML to prevent XSS attacks
  - MUST support CommonMark standard + GitHub Flavored Markdown extensions
  - MUST preserve technical fields as plain text (IDs, file paths, commands)
  - MUST work offline (no external CDN dependencies for critical rendering)

**Related Documentation:**
- Related ADRs: [ADR-032: Real-Time Execution Dashboard](../../docs/architecture/adrs/ADR-032-real-time-execution-dashboard.md)
- Related Specifications: [Real-Time Execution Dashboard](real-time-execution-dashboard.md)
- Standards:
  - [CommonMark Specification](https://spec.commonmark.org/)
  - [GitHub Flavored Markdown (GFM)](https://github.github.com/gfm/)

---

## Functional Requirements (MoSCoW)

### MUST Have (Critical - Feature unusable without these)

**FR-M1:** System MUST render CommonMark syntax in task description and context fields
- **Rationale:** Core feature purpose—make formatted text readable
- **Personas Affected:** Software Engineer, Agentic Framework Core Team
- **Success Criteria:** Headers (#), bold (**), italic (*), links ([text](url)), code blocks (```), lists rendered as HTML

**FR-M2:** System MUST support GitHub Flavored Markdown (GFM) extensions
- **Rationale:** Tables, task lists, and strikethrough are commonly used in task descriptions
- **Personas Affected:** Software Engineer, Documentation Writer
- **Success Criteria:** Tables (|), task lists (- [ ]), strikethrough (~~), footnotes render correctly

**FR-M3:** System MUST sanitize rendered HTML to prevent XSS attacks
- **Rationale:** Security—user-generated content must not execute scripts
- **Personas Affected:** All users (security constraint)
- **Success Criteria:** `<script>`, `<iframe>`, `onclick`, and other dangerous tags/attributes stripped

**FR-M4:** System MUST syntax highlight code blocks
- **Rationale:** Code examples are frequent in technical tasks; highlighting improves comprehension
- **Personas Affected:** Software Engineer, Backend developers
- **Success Criteria:** ```python, ```javascript, ```bash code blocks render with syntax colors

**FR-M5:** System MUST render specific fields only (description, context, notes)
- **Rationale:** Technical fields (IDs, file paths, agent names) should remain plain for copy-paste
- **Personas Affected:** Software Engineer (needs to copy exact values)
- **Success Criteria:** `description`, `context`, `notes`, `acceptance_criteria` render as markdown; `id`, `agent`, `title`, `status`, `priority` remain plain text

**FR-M6:** System MUST fall back gracefully if markdown parsing fails
- **Rationale:** Malformed markdown shouldn't break task display
- **Personas Affected:** All users
- **Success Criteria:** Parse errors display original raw text with warning: "Markdown rendering failed"

### SHOULD Have (Important - Feature degraded without these)

**FR-S1:** System SHOULD support mermaid diagram rendering
- **Rationale:** Architectural diagrams and flowcharts enhance task clarity
- **Personas Affected:** Architect Alphonso, Diagrammer agents
- **Success Criteria:** ````mermaid code blocks render as SVG diagrams
- **Workaround if omitted:** Display raw mermaid syntax (users can copy to external renderer)

**FR-S2:** System SHOULD linkify URLs in plain text fields
- **Rationale:** Convenience—make references clickable even in non-markdown fields
- **Personas Affected:** Software Engineer
- **Success Criteria:** Plain text URLs in title/technical fields auto-convert to clickable links
- **Workaround if omitted:** Users manually copy-paste URLs into browser

**FR-S3:** System SHOULD preserve whitespace in code blocks
- **Rationale:** Indentation matters for Python, YAML, and other syntax-sensitive code
- **Personas Affected:** Software Engineer
- **Success Criteria:** Code blocks use `<pre>` tag with preserved spaces/tabs
- **Workaround if omitted:** Code formatting distorted, potentially misleading

**FR-S4:** System SHOULD indicate when markdown rendering is active
- **Rationale:** User awareness—distinguish rendered vs. raw text
- **Personas Affected:** Software Engineer
- **Success Criteria:** Toggle button: "Show Raw" / "Show Rendered" in task detail modal
- **Workaround if omitted:** Rendered mode is default, no way to see original markdown

### COULD Have (Nice to have - Enhances experience)

**FR-C1:** System COULD support LaTeX math rendering
- **Rationale:** Useful for data science or algorithm-heavy tasks
- **Personas Affected:** Data Science engineers (future persona)
- **Success Criteria:** `$equation$` and `$$block$$` render as formatted math
- **If omitted:** Math displays as plain LaTeX syntax

**FR-C2:** System COULD support collapsible sections
- **Rationale:** Long task descriptions could be organized with expandable sections
- **Personas Affected:** Documentation Writer
- **Success Criteria:** `<details>` HTML tags or custom `:::details` syntax render as collapsible
- **If omitted:** All content visible at once (potential scroll fatigue)

**FR-C3:** System COULD cache rendered HTML
- **Rationale:** Performance optimization for frequently viewed tasks
- **Personas Affected:** All users (faster load times)
- **Success Criteria:** Rendered HTML stored in memory; re-render only when YAML changes
- **If omitted:** Re-render on every modal open (acceptable performance impact)

**FR-C4:** System COULD support custom markdown extensions
- **Rationale:** Framework-specific syntax (e.g., `@backend-dev` mentions)
- **Personas Affected:** Agentic Framework Core Team
- **Success Criteria:** Custom syntax parser transforms `@agent-name` to clickable agent profile links
- **If omitted:** Custom syntax displays as plain text

### WON'T Have (Explicitly out of scope)

**FR-W1:** System will NOT support rich text editing (WYSIWYG editor)
- **Rationale:** Tasks are YAML files; editing happens in text editor, not dashboard
- **Future Consideration:** Could add inline editing in future

**FR-W2:** System will NOT render markdown in task titles
- **Rationale:** Titles should be plain text for consistency in lists and tables
- **Future Consideration:** N/A (intentional constraint)

**FR-W3:** System will NOT support PDF export of rendered markdown
- **Rationale:** Out of scope for MVP; users can print browser view
- **Future Consideration:** Could add export feature later

---

## Scenarios and Behavior

### Scenario 1: Happy Path - Render Formatted Description

**Given** I open the task detail modal for task "Implement Telemetry Database"  
**And** The task YAML contains:
```yaml
description: |
  Implement SQLite database for telemetry tracking.
  
  ## Requirements
  - Schema for invocation logs
  - **Token counts** and *cost tracking*
  - Migration support
  
  ```python
  class TelemetryLogger:
      def log_invocation(self, model, tokens, cost):
          pass
  ```
```
**When** The modal renders the description field  
**Then** The markdown is converted to HTML:
- "## Requirements" renders as `<h2>Requirements</h2>`
- Bullet list renders as `<ul><li>` elements
- **Token counts** renders as bold
- *cost tracking* renders as italic
- Python code block renders with syntax highlighting
**And** The rendered HTML is sanitized (no script tags)

### Scenario 2: Plain Text Fallback

**Given** I open a task with no markdown syntax in the description  
**When** The modal renders the description  
**Then** The plain text displays normally (no HTML formatting)  
**And** Line breaks are preserved  
**And** URLs are auto-linkified (FR-S2)

### Scenario 3: XSS Attack Prevention

**Given** A malicious task YAML contains:
```yaml
description: |
  Click here: <script>alert('XSS')</script>
  Or this: <img src=x onerror="alert('XSS')">
```
**When** The modal renders the description  
**Then** The `<script>` tag is stripped  
**And** The `<img>` tag with `onerror` is stripped or sanitized  
**And** The rendered output is safe: "Click here: [removed] Or this: [removed]"  
**And** A security log entry is created

### Scenario 4: Code Block Syntax Highlighting

**Given** I open a task with multiple code blocks:
```yaml
context: |
  Python example:
  ```python
  def hello():
      print("world")
  ```
  
  Bash example:
  ```bash
  npm install marked highlight.js
  ```
```
**When** The modal renders the context  
**Then** Python code block has syntax highlighting (keywords, strings, functions colored)  
**And** Bash code block has syntax highlighting (commands, flags colored)  
**And** Both blocks use monospace font in `<pre><code>` tags

### Scenario 5: GFM Table Rendering

**Given** I open a task with a GitHub Flavored Markdown table:
```yaml
description: |
  Priority matrix:
  
  | Task | Priority | Estimate |
  |------|----------|----------|
  | DB Schema | HIGH | 2h |
  | Tests | MEDIUM | 1h |
```
**When** The modal renders the description  
**Then** The table renders as HTML `<table>` with headers and rows  
**And** Borders and cell padding are styled for readability

### Scenario 6: Task List (Checkboxes)

**Given** I open a task with a GFM task list:
```yaml
acceptance_criteria: |
  - [x] Schema created
  - [x] Unit tests passing
  - [ ] Integration tests
  - [ ] Documentation
```
**When** The modal renders the acceptance_criteria  
**Then** Checked items render with ✓ checkmark symbol (or CSS checkbox)  
**And** Unchecked items render with ☐ empty box symbol  
**And** Checkboxes are read-only (not interactive)

### Scenario 7: Toggle Raw/Rendered View

**Given** I am viewing a task detail modal with rendered markdown  
**When** I click the "Show Raw" button  
**Then** The rendered HTML is replaced with original markdown syntax  
**And** Code blocks show triple backticks  
**And** Headers show `##` prefix  
**When** I click "Show Rendered" again  
**Then** The markdown is re-rendered to HTML

### Scenario 8: Mermaid Diagram (Optional FR-S1)

**Given** I open a task with a mermaid diagram:
```yaml
context: |
  Architecture flow:
  
  ```mermaid
  graph LR
    A[Dashboard] --> B[WebSocket]
    B --> C[File Watcher]
  ```
```
**When** The modal renders the context (and FR-S1 is implemented)  
**Then** The mermaid syntax is converted to an SVG diagram  
**And** The diagram is interactive (clickable nodes, zoom)

### Scenario 9: Malformed Markdown Graceful Degradation

**Given** I open a task with malformed markdown (unclosed code block):
```yaml
description: |
  This is broken:
  ```python
  def unclosed():
  # Missing closing backticks
  
  More text here.
```
**When** The modal attempts to render the description  
**Then** The markdown parser detects the error  
**And** Falls back to displaying raw text  
**And** Shows warning banner: "Markdown rendering failed. Showing raw text."

---

## Data Model

### Fields to Render as Markdown

```yaml
# YAML Task Structure
id: 2026-02-06T1500-task-id              # Plain text (no rendering)
title: "Task Title"                       # Plain text (no rendering)
agent: backend-dev                        # Plain text (no rendering)
priority: HIGH                            # Plain text (no rendering)
status: pending                           # Plain text (no rendering)

description: |                            # ✅ RENDER AS MARKDOWN
  # Task Overview
  This task implements **feature X**.
  
  ## Requirements
  - Item 1
  - Item 2

context: |                                # ✅ RENDER AS MARKDOWN
  Background information with *emphasis*.
  
  ```python
  code_example()
  ```

acceptance_criteria: |                   # ✅ RENDER AS MARKDOWN
  - [x] Test 1 passing
  - [ ] Test 2 pending

technical_notes: |                       # ✅ RENDER AS MARKDOWN (optional)
  Implementation details.

deliverables:                            # Plain text list (no rendering)
  - file1.py
  - file2.py

references:                              # Plain text list (no rendering)
  - docs/adr-032.md
```

---

## Technical Constraints

### Security (Critical)

1. **XSS Prevention:** Use DOMPurify or equivalent HTML sanitizer
2. **Allowed Tags:** `<h1-h6>`, `<p>`, `<ul>`, `<ol>`, `<li>`, `<code>`, `<pre>`, `<strong>`, `<em>`, `<a>`, `<table>`, `<tr>`, `<td>`, `<th>`, `<blockquote>`, `<hr>`, `<br>`
3. **Blocked Tags:** `<script>`, `<iframe>`, `<object>`, `<embed>`, `<link>`, `<style>` (inline styles allowed, external stylesheets blocked)
4. **Blocked Attributes:** `onclick`, `onerror`, `onload`, `javascript:` URLs

### Performance

1. **Rendering Speed:** <50ms for typical task description (500 words)
2. **Large Documents:** Warn if description >10KB, render with pagination
3. **Caching:** Optional (FR-C3)—cache rendered HTML keyed by task ID + YAML hash

### Browser Compatibility

1. **Target Browsers:** Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
2. **Fallback:** Plain text display if JavaScript fails (progressive enhancement)

---

## UI/UX Specifications

### Rendered Markdown Styling

**Typography:**
- Headers: Lato or system sans-serif, bold
- Body text: System default, 16px, 1.6 line-height
- Code inline: `Source Code Pro` or monospace, gray background
- Code blocks: Dark theme (Dracula or GitHub Dark), syntax colors

**Spacing:**
- Paragraph margin: 1em bottom
- List item margin: 0.5em bottom
- Code block padding: 1em all sides

**Colors (Dark Theme Dashboard):**
- Text: #e5e7eb (light gray)
- Headers: #ffffff (white)
- Links: #3b82f6 (blue), hover: #60a5fa
- Code background: #1e293b (darker gray)
- Table borders: #374151 (medium gray)

### Raw/Rendered Toggle

**Position:** Top-right corner of task detail modal  
**Button Design:** Toggle switch with labels "Rendered" / "Raw"  
**Default State:** Rendered  
**Behavior:** Instant switch (no loading), preserves scroll position

### Code Block Features

**Copy Button:** Top-right corner of each code block, "Copy" tooltip  
**Language Label:** Top-left corner, e.g., "Python"  
**Line Numbers:** Optional (FR-C feature), off by default

---

## Acceptance Criteria

### Definition of Done

- [ ] Description, context, acceptance_criteria, technical_notes fields render as markdown
- [ ] CommonMark syntax (headers, bold, italic, links, code, lists) renders correctly
- [ ] GFM extensions (tables, task lists, strikethrough) render correctly
- [ ] Code blocks have syntax highlighting for 10+ languages (Python, JS, Bash, YAML, etc.)
- [ ] HTML is sanitized—XSS test cases pass (no script execution)
- [ ] Plain text fields (ID, agent, title, status, priority) remain unrendered
- [ ] Raw/Rendered toggle button works and preserves scroll position
- [ ] URLs in plain text fields auto-linkify (FR-S2)
- [ ] Malformed markdown falls back to raw text with warning
- [ ] Rendering speed <50ms for typical tasks (performance test)
- [ ] Unit tests: Markdown parsing, HTML sanitization
- [ ] Integration tests: End-to-end rendering in task detail modal
- [ ] Security audit: XSS prevention validated
- [ ] Manual test: View 10+ real tasks with various markdown complexity
- [ ] Documentation: User guide section added

---

## Implementation Notes

### Recommended Approach

**Phase 1: Core Markdown Rendering (3-4 hours)**
1. Choose library: `marked` (JS) for CommonMark parsing
2. Add GFM plugin: `marked-gfm-heading-id` + table support
3. Integrate HTML sanitizer: `DOMPurify`
4. Create rendering function: `renderMarkdown(text, options)`
5. Unit tests for parsing and sanitization

**Phase 2: Syntax Highlighting (2 hours)**
1. Integrate `highlight.js` or `Prism.js`
2. Configure language support (Python, JS, Bash, YAML, etc.)
3. Apply dark theme CSS
4. Add copy button to code blocks
5. Test code block rendering

**Phase 3: UI Integration (2-3 hours)**
1. Identify markdown fields in task detail modal
2. Apply `renderMarkdown()` to description, context, acceptance_criteria
3. Add Raw/Rendered toggle button
4. Wire toggle to switch between raw text and rendered HTML
5. Style rendered HTML with dark theme CSS

**Phase 4: Polish & Testing (2 hours)**
1. Auto-linkify URLs in plain text fields
2. Add warning banner for malformed markdown
3. Performance test with large documents
4. Security audit: Attempt XSS injections
5. Manual testing with real tasks

**Total Estimated Effort:** 9-11 hours

### Technical Design Considerations

- **Library Choice:** `marked` (lightweight, fast, CommonMark compliant) vs. `markdown-it` (more extensible, plugins)
- **Sanitization:** Use `DOMPurify.sanitize(html, { ALLOWED_TAGS: [...], ALLOWED_ATTR: [...] })`
- **Syntax Highlighting:** `highlight.js` (auto-detect) vs. `Prism.js` (explicit language)
- **Caching Strategy:** In-memory Map keyed by `${taskId}-${yamlHash}` (optional optimization)
- **Mermaid Support (Optional):** Use `mermaid.js` library, render on client side

### Security Checklist

- [ ] DOMPurify configured with strict whitelist
- [ ] Script tags stripped
- [ ] Event handlers (onclick, onerror) stripped
- [ ] `javascript:` URLs blocked
- [ ] `<iframe>`, `<object>`, `<embed>` tags blocked
- [ ] External stylesheets blocked (inline styles OK)
- [ ] Content Security Policy (CSP) header set: `default-src 'self'`

---

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| XSS Vulnerabilities | CRITICAL | LOW | Use DOMPurify, security audit, CSP headers |
| Malformed Markdown Breaks UI | MEDIUM | MEDIUM | Graceful fallback to raw text |
| Performance Degradation (Large Docs) | MEDIUM | LOW | Pagination or truncation for >10KB |
| Syntax Highlighting Fails | LOW | LOW | Fall back to plain code block |

---

## Success Metrics

- **Adoption:** 90% of tasks with markdown syntax render correctly (no fallback warnings)
- **Performance:** 95th percentile rendering time <50ms
- **Security:** Zero XSS exploits in production (quarterly audit)
- **User Satisfaction:** Positive feedback on readability improvement (dogfooding survey)

---

## References

- **CommonMark Spec:** https://spec.commonmark.org/
- **GitHub Flavored Markdown:** https://github.github.com/gfm/
- **marked.js:** https://marked.js.org/
- **DOMPurify:** https://github.com/cure53/DOMPurify
- **highlight.js:** https://highlightjs.org/
- **Dashboard UI:** `src/llm_service/dashboard/static/index.html`

---

**Prepared by:** Analyst Annie  
**Date:** 2026-02-06  
**Status:** Draft (ready for Architect Alphonso technical design review)
