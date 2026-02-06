# Dashboard Markdown Rendering - Test Cases

**Document:** Manual Test Cases for ADR-036  
**Created:** 2026-02-06  
**Status:** In Progress  
**Related:** specifications/llm-dashboard/markdown-rendering.md

---

## Test Category 1: Markdown Syntax

### TC-1.1: Headers (H1-H6)
**Input:**
```markdown
# Header 1
## Header 2
### Header 3
#### Header 4
##### Header 5
###### Header 6
```

**Expected Output:**
- H1-H6 tags rendered with proper hierarchy
- Headers styled with bold font, appropriate sizes
- No `#` characters visible

**Status:** ⏳ Pending  
**Result:** 

---

### TC-1.2: Emphasis (Bold, Italic, Strikethrough)
**Input:**
```markdown
**bold text**
*italic text*
~~strikethrough text~~
***bold and italic***
```

**Expected Output:**
- Bold: `<strong>` tags
- Italic: `<em>` tags
- Strikethrough: `<del>` tags
- Combined styling works

**Status:** ⏳ Pending  
**Result:** 

---

### TC-1.3: Lists (Unordered, Ordered)
**Input:**
```markdown
- Item 1
- Item 2
  - Nested item
  - Nested item 2
    
1. First
2. Second
3. Third
```

**Expected Output:**
- Unordered: `<ul><li>` with proper nesting
- Ordered: `<ol><li>` with sequential numbers
- Proper indentation for nested lists

**Status:** ⏳ Pending  
**Result:** 

---

### TC-1.4: Code Blocks (Inline and Fenced)
**Input:**
```markdown
Inline code: `const x = 42;`

Fenced code block:
```python
def hello_world():
    print("Hello, World!")
    return True
\```

```javascript
const greet = () => {
  console.log("Hello!");
};
\```
```

**Expected Output:**
- Inline code: `<code>` with monospace font, gray background
- Fenced blocks: `<pre><code class="language-python">` with syntax highlighting
- Language label visible (Python, JavaScript)
- Preserved whitespace/indentation

**Status:** ⏳ Pending  
**Result:** 

---

### TC-1.5: Tables (GFM)
**Input:**
```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Row 1    | Data A   | Data B   |
| Row 2    | Data C   | Data D   |
```

**Expected Output:**
- `<table><thead><tbody>` structure
- Borders visible
- Header row styled differently
- Cell padding applied

**Status:** ⏳ Pending  
**Result:** 

---

### TC-1.6: Task Lists (GFM)
**Input:**
```markdown
- [x] Completed task
- [ ] Pending task
- [x] Another completed task
- [ ] Another pending task
```

**Expected Output:**
- Checked: ✓ or checked checkbox (read-only)
- Unchecked: ☐ or empty checkbox (read-only)
- No interactive behavior (not clickable)

**Status:** ⏳ Pending  
**Result:** 

---

### TC-1.7: Links and Autolinks
**Input:**
```markdown
[Google](https://google.com)
https://github.com/example/repo
<user@example.com>
```

**Expected Output:**
- Links: `<a href="https://google.com">Google</a>`
- Autolinks: URLs converted to clickable links
- Links open in new tab (`target="_blank"`)
- Email links: `mailto:` protocol

**Status:** ⏳ Pending  
**Result:** 

---

### TC-1.8: Blockquotes
**Input:**
```markdown
> This is a blockquote.
> It can span multiple lines.
>
> And multiple paragraphs.
```

**Expected Output:**
- `<blockquote>` with left border
- Indented text
- Distinct styling (different background or border)

**Status:** ⏳ Pending  
**Result:** 

---

### TC-1.9: Horizontal Rules
**Input:**
```markdown
Text above

---

Text below
```

**Expected Output:**
- `<hr>` tag rendered
- Visible horizontal line separator
- Proper margins above/below

**Status:** ⏳ Pending  
**Result:** 

---

## Test Category 2: Security (XSS Prevention)

### TC-2.1: Script Tag Injection
**Input:**
```markdown
<script>alert('XSS');</script>
```

**Expected Output:**
- Script tag stripped completely
- No JavaScript execution
- Text may show "[removed]" or nothing

**Status:** ⏳ Pending  
**Result:** 

---

### TC-2.2: Image with Onerror Handler
**Input:**
```markdown
<img src=x onerror="alert('XSS')">
```

**Expected Output:**
- `onerror` attribute stripped
- Image tag may remain without handler
- No JavaScript execution

**Status:** ⏳ Pending  
**Result:** 

---

### TC-2.3: JavaScript URL in Link
**Input:**
```markdown
[Click me](javascript:alert('XSS'))
```

**Expected Output:**
- `javascript:` URL blocked
- Link either stripped or href changed to `#`
- No JavaScript execution

**Status:** ⏳ Pending  
**Result:** 

---

### TC-2.4: Data URI with Script
**Input:**
```markdown
[File](data:text/html,<script>alert('XSS')</script>)
```

**Expected Output:**
- `data:` URI blocked (except images)
- Link href stripped or changed
- No JavaScript execution

**Status:** ⏳ Pending  
**Result:** 

---

### TC-2.5: Onclick Event Handler
**Input:**
```markdown
<div onclick="alert('XSS')">Click me</div>
```

**Expected Output:**
- `onclick` attribute stripped
- `<div>` may be stripped entirely (not in whitelist)
- No JavaScript execution

**Status:** ⏳ Pending  
**Result:** 

---

### TC-2.6: SVG with Script
**Input:**
```markdown
<svg onload="alert('XSS')"></svg>
```

**Expected Output:**
- `<svg>` tag stripped (not in whitelist)
- No JavaScript execution

**Status:** ⏳ Pending  
**Result:** 

---

### TC-2.7: Iframe Injection
**Input:**
```markdown
<iframe src="https://evil.com"></iframe>
```

**Expected Output:**
- `<iframe>` tag stripped completely
- No embedded content loaded

**Status:** ⏳ Pending  
**Result:** 

---

### TC-2.8: Object/Embed Tags
**Input:**
```markdown
<object data="malicious.swf"></object>
<embed src="malicious.pdf">
```

**Expected Output:**
- Both tags stripped completely
- No embedded objects rendered

**Status:** ⏳ Pending  
**Result:** 

---

### TC-2.9: Link with javascript: Protocol (Encoded)
**Input:**
```markdown
[Click](&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;alert('XSS'))
```

**Expected Output:**
- Entity-encoded `javascript:` detected and blocked
- Link href stripped or changed
- No JavaScript execution

**Status:** ⏳ Pending  
**Result:** 

---

### TC-2.10: Form with Action
**Input:**
```markdown
<form action="https://evil.com">
  <input type="submit" value="Submit">
</form>
```

**Expected Output:**
- `<form>` tag stripped (not in whitelist)
- No form submission possible

**Status:** ⏳ Pending  
**Result:** 

---

## Test Category 3: Edge Cases

### TC-3.1: Empty Field
**Input:**
```markdown
(empty string)
```

**Expected Output:**
- No error thrown
- Empty container or minimal padding displayed
- No "undefined" or null text

**Status:** ⏳ Pending  
**Result:** 

---

### TC-3.2: Null Field
**Input:**
```javascript
null
```

**Expected Output:**
- No error thrown
- Handled gracefully (empty or placeholder text)
- No "null" text displayed

**Status:** ⏳ Pending  
**Result:** 

---

### TC-3.3: Malformed Markdown (Unclosed Code Block)
**Input:**
```markdown
Here's some code:
```python
def broken():
    print("Missing closing backticks")
More text here.
```

**Expected Output:**
- Parser recovers gracefully
- Either shows as code block or plain text
- No UI breakage or infinite loading

**Status:** ⏳ Pending  
**Result:** 

---

### TC-3.4: Very Large Content (5000+ chars)
**Input:**
```markdown
(5000 character markdown string with mixed content)
```

**Expected Output:**
- Renders without blocking UI
- Render time < 200ms (P95 target)
- No browser freeze or lag

**Status:** ⏳ Pending  
**Result:** 

---

### TC-3.5: Plain Text (No Markdown)
**Input:**
```
This is plain text with no markdown syntax.
Just regular sentences.
```

**Expected Output:**
- Renders as plain paragraphs
- Line breaks preserved
- No formatting applied unnecessarily

**Status:** ⏳ Pending  
**Result:** 

---

### TC-3.6: Mixed HTML and Markdown
**Input:**
```markdown
# Header

<strong>HTML bold</strong> mixed with **markdown bold**.

<p>HTML paragraph</p>
```

**Expected Output:**
- Both HTML and markdown rendered
- HTML sanitized (no unsafe tags)
- Styling applied consistently

**Status:** ⏳ Pending  
**Result:** 

---

## Test Category 4: Performance

### TC-4.1: Typical Task (500 chars)
**Measurement:** Console timing
```javascript
console.time('markdown-render');
renderMarkdown(typicalTask.description);
console.timeEnd('markdown-render');
```

**Expected:** < 50ms  
**Actual:** ___ ms  
**Status:** ⏳ Pending

---

### TC-4.2: Large Task (5000 chars)
**Measurement:** Console timing
```javascript
console.time('markdown-render-large');
renderMarkdown(largeTask.description);
console.timeEnd('markdown-render-large');
```

**Expected:** < 200ms (P95)  
**Actual:** ___ ms  
**Status:** ⏳ Pending

---

### TC-4.3: Multiple Fields Rendering
**Measurement:** Time to render all markdown fields in modal
```javascript
console.time('modal-render');
// Render description, context, acceptance_criteria, notes
console.timeEnd('modal-render');
```

**Expected:** < 150ms total  
**Actual:** ___ ms  
**Status:** ⏳ Pending

---

## Test Category 5: Field Classification

### TC-5.1: Technical Fields Remain Plain Text
**Fields to Test:**
- `id`: "2026-02-06T1148-task-id"
- `agent`: "backend-dev-benny"
- `status`: "in_progress"
- `priority`: "HIGH"
- `title`: "Implement API Endpoint"

**Expected Output:**
- All rendered with `.textContent` (plain text)
- Copy-paste preserves exact value
- No HTML formatting applied

**Status:** ⏳ Pending  
**Result:** 

---

### TC-5.2: Markdown Fields Rendered as HTML
**Fields to Test:**
- `description`: Contains markdown
- `context`: Contains markdown
- `acceptance_criteria`: Contains markdown
- `notes`: Contains markdown

**Expected Output:**
- All rendered with `.innerHTML` (formatted HTML)
- Markdown syntax converted
- Proper styling applied

**Status:** ⏳ Pending  
**Result:** 

---

## Test Category 6: Browser Compatibility

### TC-6.1: Chrome (Latest)
**Version:** _______  
**Status:** ⏳ Pending  
**Issues:** 

---

### TC-6.2: Firefox (Latest)
**Version:** _______  
**Status:** ⏳ Pending  
**Issues:** 

---

### TC-6.3: Safari (15+)
**Version:** _______  
**Status:** ⏳ Pending  
**Issues:** 

---

## Test Category 7: Responsive Design

### TC-7.1: Mobile (375px width)
**Expected:**
- Tables scroll horizontally
- Code blocks wrap or scroll
- Modal fits screen
- Touch-friendly clickable areas

**Status:** ⏳ Pending  
**Result:** 

---

### TC-7.2: Tablet (768px width)
**Expected:**
- Readable font sizes
- Tables fit or scroll gracefully
- Modal properly sized

**Status:** ⏳ Pending  
**Result:** 

---

### TC-7.3: Desktop (1920px width)
**Expected:**
- Optimal layout utilization
- Readable without excessive line length
- Proper whitespace

**Status:** ⏳ Pending  
**Result:** 

---

## Test Summary

| Category | Total | Passed | Failed | Pending |
|----------|-------|--------|--------|---------|
| Markdown Syntax | 9 | 0 | 0 | 9 |
| Security (XSS) | 10 | 0 | 0 | 10 |
| Edge Cases | 6 | 0 | 0 | 6 |
| Performance | 3 | 0 | 0 | 3 |
| Field Classification | 2 | 0 | 0 | 2 |
| Browser Compatibility | 3 | 0 | 0 | 3 |
| Responsive Design | 3 | 0 | 0 | 3 |
| **TOTAL** | **36** | **0** | **0** | **36** |

---

## Test Execution Log

### 2026-02-06 - Initial Test Suite Creation
- Created comprehensive test case documentation
- 36 test cases across 7 categories
- Focus on security (10 XSS test cases)
- Performance benchmarks defined

### [Date] - Test Execution
- [Execution notes to be added]

---

**Next Steps:**
1. Implement Phase 1 (Library Integration)
2. Execute TC-2.* (Security tests) immediately after integration
3. Execute remaining tests after each phase
4. Document all failures and fixes
5. Update summary table as tests complete
