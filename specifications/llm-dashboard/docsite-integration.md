---
id: "SPEC-DASH-004"
title: "Dashboard-Docsite Content Integration"
status: "draft"
initiative: "Dashboard Enhancements"
priority: "MEDIUM"
epic: "Dashboard Usability"
target_personas: ["devops-danny", "backend-dev-benny", "architect-alphonso"]
features:
  - id: "FEAT-DASH-004-01"
    title: "Context-Aware Documentation Links"
    status: "draft"
  - id: "FEAT-DASH-004-02"
    title: "Help Toolbar with Docsite Access"
    status: "draft"
completion: null
created: "2026-02-06"
updated: "2026-02-06"
author: "analyst-annie"
---

# Specification: Dashboard-Docsite Content Integration

**Status:** Draft  
**Created:** 2026-02-06  
**Last Updated:** 2026-02-06  
**Author:** Analyst Annie  
**Stakeholders:** Human-in-Charge, Architect Alphonso, Backend-dev Benny

---

## User Story

**As a** developer using the agent dashboard  
**I want** quick access to relevant documentation from within the dashboard  
**So that** I can understand agent capabilities, ADRs, and workflows without leaving my monitoring session

**Target Personas:**
- DevOps Danny (Primary) - Uses dashboard to monitor orchestration, needs quick reference to agent profiles
- Backend-dev Benny (Secondary) - Reviews ADRs and technical decisions while monitoring tasks
- Architect Alphonso (Secondary) - References architecture docs while reviewing dashboard metrics

---

## Overview

The dashboard currently operates as a standalone monitoring tool with no connection to the project's documentation site. Users must manually navigate to GitHub or the local docsite to find agent profiles, ADRs, guides, or architectural documentation. This context-switching friction slows down decision-making and reduces situational awareness during active development sessions.

**Problem:**
- Dashboard shows agent names but no quick access to agent profiles
- ADR references in tasks don't link to actual ADR documents
- No obvious path from dashboard to documentation site
- New users don't know where to find help resources

**Solution:**
Integrate minimal documentation links into the dashboard:
1. **Context-aware links:** Agent names → agent profiles, ADR IDs → ADR pages
2. **Help toolbar:** Persistent documentation access with common shortcuts
3. **External docsite link:** Quick access to full documentation site on GitHub

**Context:**
- Docsite exists at docs-site/ (MkDocs structure)
- Agent profiles in .github/agents/*.agent.md
- ADRs in docs/architecture/adrs/ADR-*.md
- Dashboard already displays agent names, task IDs, and metadata

**Related Documentation:**
- Related ADRs: ADR-032 (Real-Time Dashboard), ADR-036 (Markdown Rendering)
- Related Specifications: specifications/llm-dashboard/markdown-rendering.md
- Background: MkDocs documentation structure at docs-site/

---

## Functional Requirements (MoSCoW)

### MUST Have (Critical - Feature unusable without these)

**FR-M1:** Context-aware agent profile links
- **Rationale:** Agent names appear throughout dashboard (task assignments, status views). Users need immediate access to agent capabilities without leaving dashboard.
- **Personas Affected:** DevOps Danny (primary), Backend-dev Benny, Architect Alphonso
- **Success Criteria:** Clicking agent name opens agent profile document (in new tab or sidebar)

**FR-M2:** Help toolbar with documentation shortcuts
- **Rationale:** New users need discoverable path to documentation. Toolbar provides persistent access without cluttering main dashboard.
- **Personas Affected:** All personas (especially new users)
- **Success Criteria:** Help toolbar visible on all dashboard pages with links to key documentation sections

**FR-M3:** External docsite link
- **Rationale:** Context-aware links cover common cases, but users need escape hatch to full documentation site.
- **Personas Affected:** All personas
- **Success Criteria:** "Documentation" button in toolbar opens docsite on GitHub (configurable URL)

### SHOULD Have (Important - Feature degraded without these)

**FR-S1:** Context-aware ADR links
- **Rationale:** Tasks and specifications reference ADRs (e.g., "ADR-035"). Linking these provides instant architectural context.
- **Personas Affected:** Architect Alphonso (primary), Backend-dev Benny
- **Success Criteria:** ADR references (ADR-XXX pattern) become clickable links to ADR documents
- **Workaround if omitted:** Users manually search for ADR in file system or GitHub

**FR-S2:** Tooltip help icons on complex UI elements
- **Rationale:** Dashboard has specialized terminology (inbox/assigned/done, priority values, progress calculations). Tooltips reduce cognitive load.
- **Personas Affected:** New users, occasional dashboard users
- **Success Criteria:** Help icons (?) next to complex terms, hover shows brief explanation with "Learn more" link to docsite
- **Workaround if omitted:** Users consult dashboard user guide separately

**FR-S3:** Context-aware specification links
- **Rationale:** Tasks link to specifications via `specification:` field. Users should access spec from task detail view.
- **Personas Affected:** Backend-dev Benny, Frontend specialist
- **Success Criteria:** Task detail modal shows specification link that opens spec file
- **Workaround if omitted:** Users manually navigate to specifications/ directory

### COULD Have (Nice to have - Enhances experience)

**FR-C1:** Embedded docsite viewer
- **Rationale:** Opening external tabs disrupts flow. Embedded viewer keeps user in dashboard.
- **Personas Affected:** All personas (especially during long monitoring sessions)
- **Success Criteria:** Sidebar or modal displays docsite content without leaving dashboard
- **If omitted:** Users use new tabs, acceptable for MVP

**FR-C2:** Search bar for documentation content
- **Rationale:** Users searching for specific topics could search dashboard and docsite simultaneously.
- **Personas Affected:** All personas
- **Success Criteria:** Search bar returns results from both dashboard data and docsite markdown files
- **If omitted:** Users search dashboard and docsite separately, acceptable for MVP

**FR-C3:** Breadcrumb navigation to documentation
- **Rationale:** Show user's current context in documentation hierarchy (e.g., "Agents > Backend-dev Benny")
- **Personas Affected:** All personas
- **Success Criteria:** Breadcrumbs appear when viewing documentation within dashboard
- **If omitted:** Users rely on browser back button, acceptable for MVP

### WON'T Have (Explicitly out of scope)

**FR-W1:** Inline documentation editing
- **Rationale:** Dashboard is monitoring tool, not documentation CMS. Editing should remain file-based for Git audit trail.
- **Future Consideration:** Could add markdown editor for agent profiles in Feature C (Configuration Management)

**FR-W2:** Documentation version switching
- **Rationale:** Dashboard always shows current documentation. Historical versions handled by Git.
- **Future Consideration:** Could add dropdown to view docs from specific Git tags/branches

**FR-W3:** Multi-language documentation support
- **Rationale:** Documentation currently English-only. I18n out of scope.
- **Future Consideration:** If documentation translated, dashboard links should honor locale

---

## Scenarios and Behavior

### Scenario 1: Developer views agent profile from task list

**Context:** DevOps Danny is monitoring the dashboard task list and sees a task assigned to "backend-dev-benny". He wants to verify what tools Backend-dev Benny has access to.

**Given** the dashboard displays task list with agent names  
**When** user hovers over agent name "backend-dev-benny"  
**Then** name becomes underlined (indicates clickable link)  
**And** cursor changes to pointer

**When** user clicks agent name  
**Then** agent profile opens in new browser tab  
**And** profile shows at `.github/agents/backend-dev-benny.agent.md` content

**Success Criteria:**
- ✅ Agent names in task list are clickable links
- ✅ Links point to correct agent profile file
- ✅ Profile opens in new tab (doesn't navigate away from dashboard)
- ✅ Broken links handled gracefully (if agent profile missing)

---

### Scenario 2: New user accesses documentation via help toolbar

**Context:** A new developer opens the dashboard for the first time and doesn't know how to interpret the "portfolio view" feature.

**Given** user is viewing any dashboard page  
**When** user looks for help  
**Then** help toolbar is visible in header (persistent across pages)

**When** user clicks "Documentation" link in toolbar  
**Then** docsite opens in new tab (GitHub Pages or local MkDocs server)  
**And** docsite homepage displays

**Alternative path - Help icon:**

**When** user clicks help icon (?) next to "Portfolio View" heading  
**Then** tooltip appears with brief explanation  
**And** tooltip includes "Learn more" link to docs-site/features/portfolio-view.md

**Success Criteria:**
- ✅ Help toolbar visible on all dashboard pages
- ✅ "Documentation" link opens docsite successfully
- ✅ Docsite URL configurable (environment variable or config file)
- ✅ Tooltip help icons placed strategically on complex UI elements
- ✅ Tooltip links point to relevant docsite sections

---

### Scenario 3: Architect reviews ADR from task specification

**Context:** Architect Alphonso is reviewing a task and sees reference to "ADR-035" in the task description. He wants to read the full ADR to understand technical decisions.

**Given** task detail modal displays task description with markdown rendering  
**And** description contains text "ADR-035"  
**When** dashboard renders markdown  
**Then** "ADR-035" is automatically converted to clickable link

**When** user clicks "ADR-035" link  
**Then** ADR document opens in new tab  
**And** document shows content of `docs/architecture/adrs/ADR-035-dashboard-task-priority-editing.md`

**Edge case - Non-existent ADR:**

**Given** task references "ADR-999" (doesn't exist)  
**When** user clicks link  
**Then** browser shows 404 page or file-not-found error  
**And** dashboard logs warning (for debugging)

**Success Criteria:**
- ✅ ADR patterns (ADR-\d{3}) detected in markdown content
- ✅ ADR links generated automatically during markdown rendering
- ✅ Links point to correct ADR file path
- ✅ Broken links handled gracefully (don't break dashboard)

---

### Scenario 4: Developer accesses specification from task

**Context:** Backend-dev Benny is implementing a task and wants to review the full specification for acceptance criteria details.

**Given** task has `specification:` field populated  
**When** user opens task detail modal  
**Then** "Specification" section displays with link icon

**When** user clicks specification link  
**Then** specification file opens in new tab  
**And** file shows content of linked specification markdown file

**Edge case - Missing specification file:**

**Given** task references specification file that doesn't exist  
**When** user clicks specification link  
**Then** error message displays: "Specification file not found: [path]"  
**And** link is disabled (not clickable)

**Success Criteria:**
- ✅ Specification link visible in task detail modal (if field populated)
- ✅ Link opens specification file successfully
- ✅ Missing files show user-friendly error message
- ✅ Link respects markdown rendering (if spec content rendered inline, link goes to source)

---

## Data Model

### Link Resolution Configuration

```yaml
# Dashboard configuration (e.g., config/dashboard-links.yaml)
documentation:
  docsite_url: "https://github.com/user/repo/tree/main/docs-site"  # External docsite
  local_docsite_url: "http://localhost:8000"  # MkDocs dev server (optional)
  
  link_patterns:
    agent_profile:
      path_template: ".github/agents/{agent_name}.agent.md"
      url_template: "{docsite_url}/agents/{agent_name}"
    
    adr:
      path_template: "docs/architecture/adrs/ADR-{adr_number}-{adr_slug}.md"
      url_template: "{docsite_url}/architecture/adrs/ADR-{adr_number}"
      regex: "ADR-\\d{3}"
    
    specification:
      path_template: "{specification_path}"  # From task YAML field
      url_template: "{docsite_url}/specifications/{spec_path}"
```

### Help Toolbar Structure

```javascript
// Dashboard help toolbar configuration
const helpToolbar = {
  links: [
    {
      label: "Documentation",
      icon: "book",
      url: config.docsite_url,
      target: "_blank"
    },
    {
      label: "Agent Profiles",
      icon: "users",
      url: `${config.docsite_url}/agents/`,
      target: "_blank"
    },
    {
      label: "ADRs",
      icon: "file-text",
      url: `${config.docsite_url}/architecture/adrs/`,
      target: "_blank"
    },
    {
      label: "Quick Start",
      icon: "zap",
      url: `${config.docsite_url}/guides/dashboard-quickstart`,
      target: "_blank"
    }
  ],
  
  tooltips: {
    "portfolio-view": {
      text: "Portfolio view shows initiatives linked to specifications and tasks.",
      learnMoreUrl: `${config.docsite_url}/features/portfolio-view`
    },
    "priority-values": {
      text: "Priority: CRITICAL > HIGH > MEDIUM > LOW > normal",
      learnMoreUrl: `${config.docsite_url}/guides/task-management#priority`
    }
  }
};
```

---

## UI Specifications

### Help Toolbar (Header)

```
┌────────────────────────────────────────────────────────────┐
│  Dashboard Logo    [Tasks] [Portfolio] [Config] [Metrics]  │
│                                                              │
│                             [📚 Documentation] [❓ Help] ▾  │
└────────────────────────────────────────────────────────────┘
                                 └─ Dropdown menu:
                                    - Agent Profiles
                                    - ADRs
                                    - Quick Start Guide
                                    - Report Issue
```

**Visual Specifications:**
- Toolbar: Right-aligned in header, always visible
- Documentation icon: Book emoji or icon font
- Help dropdown: Appears on click, auto-closes on blur
- Links: Open in new tab (target="_blank")

### Context-Aware Links (Task Detail Modal)

```
┌──────────────────────────────────────────────────────────┐
│  Task: Implement Priority Edit API                       │
│                                                           │
│  Assigned to: backend-dev-benny  [👤 View Profile]       │
│                     └─ Clickable link to agent profile   │
│                                                           │
│  Description:                                            │
│  Implement PATCH endpoint as specified in ADR-035.       │
│                                        └─ Clickable link │
│                                                           │
│  Specification: task-priority-editing.md [📄 View]       │
│                                           └─ Link        │
└──────────────────────────────────────────────────────────┘
```

**Visual Specifications:**
- Agent link: Underlined on hover, blue color (standard link styling)
- ADR links: Automatically detected and styled as inline code + link
- Specification link: Icon + filename, clickable area covers entire element

### Tooltip Help Icons

```
Portfolio View (?)  ← Help icon
       └─ Hover triggers tooltip:
          ┌────────────────────────────────────────┐
          │ Shows initiatives linked to specs and  │
          │ tasks with progress rollup.            │
          │                                        │
          │ [Learn more →]                         │
          └────────────────────────────────────────┘
```

**Visual Specifications:**
- Help icon: Small (?) in light gray, positioned inline with heading
- Tooltip: White background, drop shadow, max-width 300px
- "Learn more" link: Opens docsite in new tab
- Animation: Fade in on hover, 200ms transition

---

## Non-Functional Requirements

### Performance

**NFR-1:** Link generation performance
- Context-aware links must not slow down dashboard rendering
- Target: <10ms to process links in typical task description (500 chars)
- Link resolution should be client-side (no additional HTTP requests)

**NFR-2:** Docsite availability
- Dashboard must function if docsite is unavailable
- Broken links should fail gracefully (don't crash dashboard)
- Timeout for docsite health check: 2 seconds

### Usability

**NFR-3:** Link discoverability
- Links must be visually distinguishable from plain text (underline, color)
- Hover states should indicate clickability (cursor change, style change)
- Keyboard navigation supported (tab to links, enter to activate)

**NFR-4:** Tooltip accessibility
- Tooltips must be keyboard-accessible (focus triggers tooltip)
- Screen readers should announce tooltip content
- Tooltips should not block interaction with underlying content

### Security

**NFR-5:** URL sanitization
- All generated links must be sanitized to prevent XSS
- Only allow http://, https://, and relative URLs (no javascript:, data:)
- External links should include rel="noopener noreferrer"

**NFR-6:** Docsite URL configuration
- Docsite URL should be configurable via environment variable
- No hardcoded URLs in client-side code
- Support both GitHub Pages and local MkDocs server URLs

### Maintainability

**NFR-7:** Link pattern configurability
- Link resolution patterns should be configurable (YAML or JSON)
- Adding new link types shouldn't require code changes
- Regex patterns for link detection should be externalized

---

## Acceptance Criteria

### Feature Acceptance

**AC-1:** Context-aware agent links functional
- ✅ Agent names in task list are clickable
- ✅ Clicking agent name opens correct agent profile
- ✅ Link opens in new tab
- ✅ Missing agent profiles show error message

**AC-2:** Help toolbar accessible
- ✅ Toolbar visible on all dashboard pages
- ✅ "Documentation" link opens docsite
- ✅ Dropdown shows at least 3 documentation shortcuts
- ✅ All links open in new tab

**AC-3:** ADR links detected and linked
- ✅ Pattern "ADR-XXX" detected in markdown content
- ✅ Links generated correctly with proper file path
- ✅ Clicking ADR link opens ADR document
- ✅ Non-existent ADRs fail gracefully

**AC-4:** Specification links visible
- ✅ Task detail modal shows specification link (if field present)
- ✅ Link opens specification file
- ✅ Missing specifications show user-friendly error

**AC-5:** Tooltip help functional
- ✅ Help icons placed on complex UI elements
- ✅ Hovering icon shows tooltip with explanation
- ✅ Tooltip includes "Learn more" link to docsite
- ✅ Keyboard navigation supported

### Non-Functional Acceptance

**AC-6:** Performance acceptable
- ✅ Link generation <10ms for typical task
- ✅ Dashboard loads without delay from link processing
- ✅ No additional HTTP requests for link resolution

**AC-7:** Security verified
- ✅ Generated links sanitized (no XSS vulnerabilities)
- ✅ Only safe URL schemes allowed
- ✅ External links include security attributes

**AC-8:** Accessibility compliant
- ✅ Links keyboard-navigable
- ✅ Tooltips accessible to screen readers
- ✅ WCAG 2.1 Level AA color contrast met

---

## Testing Strategy

### Unit Tests

1. **Link Pattern Detection**
   - Test regex matches ADR-XXX pattern correctly
   - Test agent name extraction from task data
   - Test specification path resolution

2. **Link Generation**
   - Test URL construction from templates
   - Test handling of special characters in filenames
   - Test relative vs. absolute URL resolution

3. **Security**
   - Test XSS prevention in generated links
   - Test URL scheme validation (allow http/https, block javascript:)
   - Test sanitization of user-provided docsite URLs

### Integration Tests

1. **End-to-End Link Navigation**
   - Open dashboard → click agent link → verify profile opens
   - Open task detail → click ADR link → verify ADR opens
   - Open task detail → click specification link → verify spec opens

2. **Tooltip Interaction**
   - Hover help icon → tooltip appears
   - Click "Learn more" → docsite page opens
   - Keyboard navigation → tooltip accessible via tab+focus

3. **Help Toolbar**
   - Click "Documentation" → docsite opens
   - Click help dropdown → menu appears with links
   - Click dropdown link → correct doc section opens

### Manual Exploration Tests

1. **Broken Link Handling**
   - Create task referencing non-existent ADR → verify graceful failure
   - Configure invalid docsite URL → verify dashboard still loads
   - Test with docsite server offline → verify fallback behavior

2. **Cross-Browser Compatibility**
   - Test link styling in Chrome, Firefox, Safari
   - Test tooltip positioning edge cases (near viewport edges)
   - Test keyboard navigation in different browsers

3. **Mobile Responsiveness**
   - Test tooltip display on touch devices
   - Test help toolbar on small screens
   - Test link tap targets (minimum 44x44px)

---

## Implementation Considerations

### Phase 1: Minimal Context-Aware Links (3-4 hours)
- Implement agent profile link detection in task views
- Add help toolbar with external docsite link
- Basic link generation and URL resolution

### Phase 2: Enhanced Link Detection (2-3 hours)
- Add ADR pattern detection in markdown rendering
- Add specification link in task detail modal
- Implement link sanitization and validation

### Phase 3: Tooltip Help System (2-3 hours)
- Design and implement tooltip component
- Place help icons on complex UI elements
- Wire tooltips to docsite documentation links

### Phase 4: Testing & Polish (2 hours)
- Unit tests for link detection and generation
- Integration tests for end-to-end link navigation
- Cross-browser testing and accessibility audit

**Total Estimated Effort:** 9-12 hours

---

## Open Questions

✅ **Resolved:**
- Q: Should links open in new tab or sidebar? **A:** New tab (simpler, less disruptive)
- Q: Which config files for link patterns? **A:** YAML config, environment variable for docsite URL
- Q: How to handle broken links? **A:** Graceful failure, log warning, show user-friendly error

⚠️ **Pending:**
- Q: Should dashboard detect local MkDocs server automatically? (probe http://localhost:8000)
- Q: Should tooltip help content be configurable or hardcoded?
- Q: Should link patterns support regex groups for more complex matching?

---

## Dependencies

- **Requires:** ADR-036 (Markdown Rendering) - ADR link detection happens during markdown parsing
- **Requires:** Dashboard MVP (ADR-032) - Foundation for UI integration
- **Enhances:** Portfolio View (ADR-037) - Initiative/feature links benefit from docsite integration

---

## Future Enhancements (Deferred)

1. **Embedded Docsite Viewer** (6-8 hours)
   - Iframe or webview displaying docsite within dashboard
   - Sidebar navigation for multi-page documentation

2. **Cross-Search Dashboard + Docsite** (8-10 hours)
   - Unified search bar querying both dashboard data and docsite markdown
   - Search result ranking and relevance scoring

3. **Smart Context Detection** (10-12 hours)
   - Detect directive references (e.g., "Directive 016") and link to directive docs
   - Detect specification IDs (e.g., "SPEC-DASH-001") and link to specs
   - Detect task IDs and create inter-task navigation

4. **Documentation Status Indicators** (4-6 hours)
   - Show badge if linked documentation is outdated (based on Git commit dates)
   - Highlight missing documentation (agent profiles not found, ADRs not created)

---

## References

- **Related ADRs:** ADR-032 (Dashboard), ADR-036 (Markdown Rendering)
- **Related Specs:** specifications/llm-dashboard/markdown-rendering.md
- **Docsite Structure:** docs-site/ (MkDocs)
- **Agent Profiles:** .github/agents/*.agent.md
- **ADRs:** docs/architecture/adrs/ADR-*.md
- **Specifications:** specifications/**/*.md

---

**Document Status:** Draft - Ready for technical design review  
**Next Steps:**
1. Architect Alphonso: Technical design for link resolution architecture
2. Backend-dev Benny: Implement backend link pattern configuration
3. Frontend Specialist: Implement UI components (help toolbar, tooltips, link styling)
