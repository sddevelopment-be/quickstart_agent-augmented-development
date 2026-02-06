---
id: "SPEC-DASH-009"
title: "Dashboard Multi-Page Navigation"
status: "draft"
initiative: "Dashboard Enhancements"
priority: "CRITICAL"
epic: "Dashboard Core Features"
target_personas: ["software-engineer", "project-manager", "devops-danny"]
features:
  - id: "FEAT-DASH-009-01"
    title: "Navigation Bar Component"
    status: "draft"
    description: "Top-level navigation with 3 page tabs"
  - id: "FEAT-DASH-009-02"
    title: "Page Routing and State Management"
    status: "draft"
    description: "Client-side routing with URL hash navigation"
  - id: "FEAT-DASH-009-03"
    title: "Dashboard Page (Default)"
    status: "draft"
    description: "Recent Activity + Live Task Board (operational focus)"
  - id: "FEAT-DASH-009-04"
    title: "Initiatives & Milestones Page"
    status: "draft"
    description: "Portfolio Overview + Orphan Tasks (strategic focus)"
  - id: "FEAT-DASH-009-05"
    title: "Accounting Page"
    status: "draft"
    description: "Cost & Model Analytics (financial focus)"
completion: null
created: "2026-02-06"
updated: "2026-02-06"
author: "analyst-annie"
---

# Specification: Dashboard Multi-Page Navigation

**Status:** Draft  
**Created:** 2026-02-06  
**Last Updated:** 2026-02-06  
**Author:** Analyst Annie  
**Stakeholders:** Human-in-Charge, Software Engineers, Project Managers, DevOps Engineers

---

## User Story

**As a** user of the agent dashboard  
**I want** the dashboard content organized across multiple focused pages  
**So that** I can quickly access relevant information without overwhelming visual clutter and cognitive load

**Alternative: Acceptance Criterion Format**  
**Given** I open the dashboard  
**When** I view the interface  
**Then** I see a navigation bar with 3 tabs: "Dashboard", "Initiatives & Milestones", "Accounting"  
**And** clicking a tab displays the corresponding page content  
**And** the URL reflects the current page (for bookmarking)  
**And** the active tab is visually highlighted

**Target Personas:**
- Software Engineer (Primary) - Needs task-level operational view + strategic context
- Project Manager (Primary) - Needs portfolio visibility + cost tracking
- DevOps Danny (Secondary) - Monitors system health + cost efficiency
- Human-in-Charge (Secondary) - Executive overview across all dimensions

---

## Problem Statement

### Current Pain Points

**Single-Page Information Overload:**
The current dashboard displays 4 major sections on one page:
1. Recent Activity (operational)
2. Live Task Board / Kanban (operational)
3. Portfolio Overview (strategic)
4. Cost & Model Analytics (financial)

**User Impact:**
- 🔴 **CRITICAL:** Cognitive overload - too much information competing for attention
- 🔴 **CRITICAL:** Difficult to focus - switching mental contexts requires scrolling
- 🟡 **HIGH:** Slow load times - all data fetched simultaneously even if not viewed
- 🟡 **HIGH:** Poor mobile experience - vertical scroll becomes unwieldy
- 🟡 **HIGH:** No deep linking - can't bookmark specific dashboard views

**Quantified Problem:**
- Current page height: ~5000px (requires extensive scrolling)
- Metrics sidebar + 4 content sections = 5 visual regions competing for focus
- User spends 30% of time scrolling vs. reading (estimated)
- No way to share "Portfolio view" vs "Cost view" link with team

### Why Now?

**Trigger:** Dashboard feature accumulation has reached critical mass:
- ✅ Batch 1 complete: Markdown, Priority, Initiative Tracking
- 🚧 Batch 1.1 pending: Orphan Assignment
- 📋 Batch 2 queued: Docsite, Repo Init, Config Management

Without multi-page structure, Batch 2 features will exacerbate clutter.

---

## Overview

Multi-page navigation organizes dashboard content into **3 focused pages**, each addressing a distinct user mental model:

1. **"Dashboard" (Default)** - Operational focus: What's happening now?
   - Recent Activity feed
   - Live Task Board (Kanban columns)
   - Metrics sidebar (persistent across pages)

2. **"Initiatives & Milestones"** - Strategic focus: Where are we going?
   - Portfolio Overview (hierarchical accordion)
   - Orphan Tasks section
   - Initiative progress tracking

3. **"Accounting"** - Financial focus: What's the cost?
   - Cost & Model Analytics charts
   - Token usage trends
   - Model performance metrics

**Context:**
- **Problem Solved:** Information overload - users see only relevant content for current task
- **Why Needed:** Dashboard content has grown beyond single-page usability threshold
- **Constraints:**
  - MUST preserve all existing functionality (no feature loss)
  - MUST maintain real-time updates via WebSocket (no polling degradation)
  - MUST support browser back/forward navigation
  - MUST be responsive (mobile/tablet/desktop)
  - SHOULD have <200ms page transition time

**Related Documentation:**
- Related ADRs: ADR-032 (Real-Time Execution Dashboard - original architecture)
- Related Specifications: 
  - SPEC-DASH-003 (Initiative Tracking - portfolio view)
  - SPEC-DASH-002 (Markdown Rendering - affects all pages)
- Background:
  - Dashboard growth timeline: 2 weeks, 6 major features added
  - User feedback: "Too much scrolling, hard to find what I need"

---

## Functional Requirements (MoSCoW)

### MUST Have (Critical - Feature unusable without these)

**FR-M1:** System MUST provide a navigation bar with 3 page tabs
- **Rationale:** Core feature purpose - enable page switching
- **Personas Affected:** All users
- **Success Criteria:** Navigation bar visible at top of dashboard with tabs: "Dashboard", "Initiatives & Milestones", "Accounting"

**FR-M2:** System MUST display only the active page content (hide inactive pages)
- **Rationale:** Reduce cognitive load and improve performance
- **Personas Affected:** All users (cognitive load reduction)
- **Success Criteria:** Clicking "Accounting" hides task board and portfolio, shows only charts

**FR-M3:** System MUST visually highlight the active tab
- **Rationale:** User orientation - know current location
- **Personas Affected:** All users (usability)
- **Success Criteria:** Active tab has distinct background color, underline, or indicator

**FR-M4:** System MUST default to "Dashboard" page on first load
- **Rationale:** Operational focus is primary use case (80% of sessions)
- **Personas Affected:** Software Engineer, DevOps Danny
- **Success Criteria:** Opening http://localhost:8080 shows Recent Activity + Task Board

**FR-M5:** System MUST persist metrics sidebar across all pages
- **Rationale:** At-a-glance status indicators useful regardless of current page
- **Personas Affected:** All users (contextual awareness)
- **Success Criteria:** Left sidebar with metrics visible on all 3 pages

**FR-M6:** System MUST update URL hash when switching pages
- **Rationale:** Enable bookmarking and deep linking (e.g., share "Accounting" view with team)
- **Personas Affected:** Project Manager (reporting), DevOps Danny (monitoring)
- **Success Criteria:** URL changes to `#dashboard`, `#initiatives`, `#accounting` when tabs clicked

**FR-M7:** System MUST support browser back/forward buttons for page navigation
- **Rationale:** Standard browser behavior - user expectation
- **Personas Affected:** All users (usability)
- **Success Criteria:** Browser back button returns to previous page; URL hash drives page display

**FR-M8:** System MUST maintain WebSocket connection across page transitions
- **Rationale:** Real-time updates critical for all pages (task status, portfolio progress, cost tracking)
- **Personas Affected:** All users (data freshness)
- **Success Criteria:** Switching pages doesn't disconnect socket; updates continue to arrive

**FR-M9:** System MUST preserve data fetched on inactive pages (no re-fetch on tab switch)
- **Rationale:** Performance - data already loaded should remain cached
- **Personas Affected:** All users (speed)
- **Success Criteria:** Switching Dashboard → Accounting → Dashboard shows cached task board (no loading spinner)

### SHOULD Have (Important - Enhances usability significantly)

**FR-S1:** System SHOULD display page transition animation
- **Rationale:** Visual feedback improves perceived performance
- **Personas Affected:** All users (polish)
- **Success Criteria:** Fade-in or slide animation when switching pages (<200ms duration)

**FR-S2:** System SHOULD remember last active page in browser session
- **Rationale:** User workflow continuity - return to where you left off
- **Personas Affected:** All users (convenience)
- **Success Criteria:** Refresh browser on "Accounting" page → returns to "Accounting" (uses sessionStorage)

**FR-S3:** System SHOULD show badge indicators on tabs (e.g., orphan task count)
- **Rationale:** Contextual awareness - see important info without switching pages
- **Personas Affected:** Software Engineer (task triage), Project Manager (planning)
- **Success Criteria:** "Initiatives & Milestones" tab shows "(3)" badge if 3 orphan tasks exist

**FR-S4:** System SHOULD support keyboard shortcuts for page switching
- **Rationale:** Power user efficiency
- **Personas Affected:** Software Engineer (frequent users)
- **Success Criteria:** Alt+1/2/3 switches to Dashboard/Initiatives/Accounting pages

**FR-S5:** System SHOULD be responsive (mobile/tablet/desktop)
- **Rationale:** Dashboard used on various devices
- **Personas Affected:** All users (device flexibility)
- **Success Criteria:** Navigation bar collapses to hamburger menu on mobile (<768px)

**FR-S6:** System SHOULD lazy-load page content (fetch only when tab first clicked)
- **Rationale:** Performance - don't fetch Cost Analytics data if user never clicks "Accounting"
- **Personas Affected:** All users (initial load speed)
- **Success Criteria:** First load fetches only Dashboard page data; Accounting data fetched on first tab click

### COULD Have (Nice-to-have - Low priority enhancements)

**FR-C1:** System COULD support user-customizable page order
- **Rationale:** Personal workflow optimization
- **Personas Affected:** Power users
- **Success Criteria:** Drag-and-drop tab reordering; saved to localStorage

**FR-C2:** System COULD show loading skeletons during lazy-load
- **Rationale:** Visual feedback during first-time page loads
- **Personas Affected:** All users (polish)
- **Success Criteria:** Clicking "Accounting" first time shows chart placeholders, then actual charts

**FR-C3:** System COULD support page-level search/filter
- **Rationale:** Quick content location within large pages
- **Personas Affected:** Software Engineer, Project Manager
- **Success Criteria:** Search box in navigation bar filters current page content

**FR-C4:** System COULD display page-specific actions in navigation bar
- **Rationale:** Contextual actions (e.g., "Export CSV" on Accounting page)
- **Personas Affected:** Project Manager (reporting)
- **Success Criteria:** Navigation bar right side shows page-relevant action buttons

### WON'T Have (Explicitly excluded from this version)

**FR-W1:** System WON'T support user-defined custom pages
- **Rationale:** Complexity - custom layouts require page builder infrastructure
- **Alternative:** Future enhancement after core navigation stable

**FR-W2:** System WON'T support split-screen or multi-page view
- **Rationale:** Defeats purpose of focus - brings back information overload
- **Alternative:** Users can open multiple browser tabs if needed

**FR-W3:** System WON'T persist page preference across browser sessions (only within session)
- **Rationale:** User might want fresh start on next day (default to Dashboard)
- **Alternative:** FR-S2 uses sessionStorage, not localStorage

---

## Page Content Organization

### Page 1: "Dashboard" (Default)

**Focus:** Operational - What's happening right now?

**Content:**
- **Recent Activity** feed (top section)
  - Last 10 task updates
  - Real-time WebSocket updates
  - Timestamps + agent names
  - Click task → opens modal

- **Live Task Board** (main section)
  - Kanban columns: Inbox | Assigned | Done
  - Task cards with priority badges
  - Drag-and-drop (future enhancement)
  - Click task → opens modal

**Metrics Sidebar** (persistent):
- Total Tasks
- In Progress
- Done Today
- Active Agents

**User Mental Model:** "Show me what needs attention"

**Typical Usage:**
- Software Engineer: Check task status, pick next work item
- DevOps Danny: Monitor agent activity
- 80% of dashboard sessions start here

---

### Page 2: "Initiatives & Milestones"

**Focus:** Strategic - Where are we going?

**Content:**
- **Portfolio Overview** (top section)
  - Initiative hierarchy (expandable accordion)
  - Progress bars (feature-level and initiative-level)
  - Click feature → expands to show tasks
  - Click task → opens modal

- **Orphan Tasks** (bottom section)
  - Unlinked tasks (no specification: field)
  - "Assign to Specification" button (future: Batch 1.1)
  - Click task → opens modal

**Metrics Sidebar** (persistent):
- Same metrics as Dashboard page

**User Mental Model:** "Show me the big picture progress"

**Typical Usage:**
- Project Manager: Review initiative progress, triage orphans
- Software Engineer: Understand how task fits into strategy
- 15% of dashboard sessions (weekly reviews, planning)

---

### Page 3: "Accounting"

**Focus:** Financial - What's the cost?

**Content:**
- **Cost & Model Analytics** charts
  - Token usage over time (line chart)
  - Cost per model (bar chart)
  - Top 5 expensive tasks (table)
  - Monthly budget tracking (gauge)

**Metrics Sidebar** (persistent):
- Same metrics as Dashboard page

**User Mental Model:** "Show me resource consumption"

**Typical Usage:**
- Project Manager: Budget tracking, cost optimization
- DevOps Danny: Identify expensive operations
- Human-in-Charge: Executive cost overview
- 5% of dashboard sessions (monthly reviews, audits)

---

## Non-Functional Requirements

### Performance Requirements

**NFR-P1:** Page transition MUST complete in <200ms (P95)
- **Rationale:** Instant feel - no perceived delay
- **Measurement:** Time from tab click to content visible
- **Trade-offs:** CSS transitions kept minimal (<200ms); data pre-fetched

**NFR-P2:** Initial page load MUST complete in <1.5s (P95)
- **Rationale:** Dashboard is monitoring tool - needs fast startup
- **Measurement:** Time from URL entered to Dashboard page interactive
- **Trade-offs:** Lazy-load non-default pages (defer Accounting/Portfolio)

**NFR-P3:** Navigation bar MUST remain responsive during data loading
- **Rationale:** User shouldn't be blocked from switching pages
- **Measurement:** Tab clicks register <50ms even during WebSocket reconnect
- **Trade-offs:** Loading states shown per-page, not global blocking spinner

### Usability Requirements

**NFR-U1:** Navigation bar MUST be accessible (WCAG 2.1 AA)
- **Rationale:** Keyboard navigation, screen reader support required
- **Measurement:** 
  - Tab key navigates between tabs
  - Enter/Space activates tab
  - ARIA labels present: `role="tablist"`, `aria-selected`
- **Trade-offs:** Vanilla JS accessible patterns (no framework needed)

**NFR-U2:** Active tab MUST have 4.5:1 contrast ratio (WCAG AA)
- **Rationale:** Visual accessibility
- **Measurement:** Color contrast checker on active tab background
- **Trade-offs:** Use existing dashboard color variables

**NFR-U3:** Page transitions MUST not cause layout shift
- **Rationale:** Jarring visual jumps harm UX
- **Measurement:** Cumulative Layout Shift (CLS) <0.1
- **Trade-offs:** Reserve consistent heights for page containers

### Reliability Requirements

**NFR-R1:** System MUST handle invalid URL hash gracefully
- **Rationale:** User might manually edit URL or follow broken link
- **Measurement:** `http://localhost:8080#invalid` → redirects to `#dashboard`
- **Trade-offs:** Fallback to default page on any unrecognized hash

**NFR-R2:** System MUST preserve page state during WebSocket reconnect
- **Rationale:** Transient network issues shouldn't reset UI
- **Measurement:** Disconnect socket → active page remains visible → reconnect succeeds
- **Trade-offs:** State stored in JavaScript variables (not tied to socket connection)

---

## User Workflows

### Workflow 1: Basic Page Switching

**Actors:** Software Engineer

**Preconditions:**
- Dashboard loaded
- Default "Dashboard" page visible

**Main Flow:**
1. User clicks **"Initiatives & Milestones"** tab in navigation bar
2. System hides Dashboard page content (Recent Activity + Task Board)
3. System shows Initiatives page content (Portfolio + Orphans)
4. System updates URL hash to `#initiatives`
5. System highlights "Initiatives & Milestones" tab (active state)
6. User reviews portfolio progress
7. User clicks **"Dashboard"** tab to return
8. System hides Initiatives page content
9. System shows Dashboard page content (cached, no re-fetch)
10. System updates URL hash to `#dashboard`
11. System highlights "Dashboard" tab

**Postconditions:**
- User returned to Dashboard page
- URL reflects current page
- No data loss or re-fetching

**Alternative Flows:**

**A1: User Uses Browser Back Button**
- At step 7, instead of clicking "Dashboard" tab, user clicks browser back button
- System detects URL hash change from `#initiatives` to `#dashboard`
- System triggers page transition (same as clicking tab)
- Result: Dashboard page displayed, tab highlighted

**A2: User Refreshes Page on Non-Default Tab**
- User on "Accounting" page (`#accounting`)
- User presses F5 to refresh browser
- System reads URL hash on load
- System displays "Accounting" page (not default Dashboard)
- Result: User sees same page after refresh

---

### Workflow 2: Deep Linking to Specific Page

**Actors:** Project Manager

**Preconditions:**
- Dashboard running
- Project Manager wants to share Accounting view with team

**Main Flow:**
1. Project Manager navigates to "Accounting" page (URL: `http://localhost:8080#accounting`)
2. Project Manager copies URL from browser address bar
3. Project Manager shares URL in Slack: "Check this month's costs: http://localhost:8080#accounting"
4. Team member clicks link
5. Dashboard opens directly to "Accounting" page (skips Dashboard default)
6. Team member sees Cost & Model Analytics charts immediately
7. "Accounting" tab is highlighted (active state)

**Postconditions:**
- Deep link worked correctly
- User landed on intended page
- No manual navigation required

---

### Workflow 3: Keyboard Power User Navigation

**Actors:** Software Engineer (frequent user)

**Preconditions:**
- Dashboard loaded
- User familiar with keyboard shortcuts (FR-S4)

**Main Flow:**
1. User on "Dashboard" page, hands on keyboard
2. User presses **Alt+2** keyboard shortcut
3. System switches to "Initiatives & Milestones" page
4. User reviews portfolio (keyboard navigation with Tab)
5. User presses **Alt+3** keyboard shortcut
6. System switches to "Accounting" page
7. User reviews costs
8. User presses **Alt+1** keyboard shortcut
9. System returns to "Dashboard" page

**Postconditions:**
- User navigated 3 pages without touching mouse
- Keyboard shortcuts worked as expected

---

## Acceptance Criteria (Given/When/Then)

### AC1: Display Navigation Bar with 3 Tabs

**Given** I open the dashboard  
**When** the page loads  
**Then** I see a navigation bar at the top with 3 tabs:
- "Dashboard"
- "Initiatives & Milestones"
- "Accounting"  
**And** the "Dashboard" tab is highlighted (active state)  
**And** the Recent Activity and Task Board sections are visible

---

### AC2: Switch to Initiatives Page

**Given** I am on the "Dashboard" page  
**When** I click the "Initiatives & Milestones" tab  
**Then** the Dashboard page content (Recent Activity + Task Board) is hidden  
**And** the Initiatives page content (Portfolio + Orphans) is displayed  
**And** the "Initiatives & Milestones" tab is highlighted  
**And** the URL hash changes to `#initiatives`  
**And** the page transition completes in <200ms

---

### AC3: Switch to Accounting Page

**Given** I am on the "Dashboard" page  
**When** I click the "Accounting" tab  
**Then** the Dashboard page content is hidden  
**And** the Accounting page content (Cost & Model Analytics charts) is displayed  
**And** the "Accounting" tab is highlighted  
**And** the URL hash changes to `#accounting`

---

### AC4: Browser Back Button Navigation

**Given** I am on the "Accounting" page (`#accounting`)  
**And** I previously navigated from "Dashboard" → "Initiatives" → "Accounting"  
**When** I click the browser back button  
**Then** the system displays the "Initiatives & Milestones" page  
**And** the URL hash changes to `#initiatives`  
**And** the "Initiatives & Milestones" tab is highlighted  
**When** I click the browser back button again  
**Then** the system displays the "Dashboard" page  
**And** the URL hash changes to `#dashboard`

---

### AC5: Deep Link to Non-Default Page

**Given** the dashboard is not currently open  
**When** I navigate to `http://localhost:8080#initiatives` in my browser  
**Then** the dashboard loads and displays the "Initiatives & Milestones" page directly  
**And** the "Initiatives & Milestones" tab is highlighted  
**And** the Dashboard page is NOT shown (skip default)

---

### AC6: Refresh Page Preserves Active Tab

**Given** I am on the "Accounting" page (`#accounting`)  
**When** I press F5 to refresh the browser  
**Then** the dashboard reloads and displays the "Accounting" page  
**And** the "Accounting" tab remains highlighted  
**And** the URL hash remains `#accounting`

---

### AC7: Metrics Sidebar Persists Across Pages

**Given** I am on the "Dashboard" page  
**And** the metrics sidebar shows "Total Tasks: 143"  
**When** I switch to the "Initiatives & Milestones" page  
**Then** the metrics sidebar remains visible  
**And** the "Total Tasks: 143" metric is still displayed  
**When** I switch to the "Accounting" page  
**Then** the metrics sidebar remains visible  
**And** all metrics continue to display

---

### AC8: WebSocket Updates Continue Across Pages

**Given** I am on the "Accounting" page (not viewing task board)  
**And** a task status changes from "assigned" to "done" (WebSocket event received)  
**When** I switch back to the "Dashboard" page  
**Then** the task board reflects the updated status (done column)  
**And** no manual refresh was required  
**And** the WebSocket connection remained active throughout

---

### AC9: Invalid URL Hash Falls Back to Default

**Given** the dashboard is not currently open  
**When** I navigate to `http://localhost:8080#invalid-page`  
**Then** the dashboard loads and displays the "Dashboard" page (default)  
**And** the URL hash is corrected to `#dashboard`  
**And** no error is shown to the user

---

### AC10: Keyboard Shortcuts Work (SHOULD-have)

**Given** I am on the "Dashboard" page  
**And** keyboard shortcuts are enabled (FR-S4)  
**When** I press `Alt+2`  
**Then** the system switches to the "Initiatives & Milestones" page  
**When** I press `Alt+3`  
**Then** the system switches to the "Accounting" page  
**When** I press `Alt+1`  
**Then** the system returns to the "Dashboard" page

---

## Technical Architecture Notes

### Client-Side Routing (Hash-Based)

**Approach:** Use URL hash (`#dashboard`, `#initiatives`, `#accounting`) for routing

**Rationale:**
- ✅ No server-side changes needed (Flask routes unchanged)
- ✅ Browser back/forward works automatically (`hashchange` event)
- ✅ Bookmarking works (hash included in URL)
- ✅ No page reload (SPA behavior)

**Implementation:**
```javascript
// Hash to page mapping
const pages = {
  'dashboard': { content: '#dashboard-content', tab: '#tab-dashboard' },
  'initiatives': { content: '#initiatives-content', tab: '#tab-initiatives' },
  'accounting': { content: '#accounting-content', tab: '#tab-accounting' }
};

// Listen for hash changes
window.addEventListener('hashchange', function() {
  const page = window.location.hash.slice(1) || 'dashboard';
  showPage(page);
});

// Show page function
function showPage(pageName) {
  // Hide all pages
  document.querySelectorAll('.page-content').forEach(el => el.classList.add('hidden'));
  
  // Show active page
  const pageConfig = pages[pageName] || pages['dashboard'];
  document.querySelector(pageConfig.content).classList.remove('hidden');
  
  // Update tab highlighting
  document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
  document.querySelector(pageConfig.tab).classList.add('active');
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', function() {
  const initialPage = window.location.hash.slice(1) || 'dashboard';
  showPage(initialPage);
});
```

---

### HTML Structure Changes

**Current:**
```html
<div class="main-content">
  <section id="recent-activity">...</section>
  <section id="task-board">...</section>
  <section id="portfolio">...</section>
  <section id="charts">...</section>
</div>
```

**Proposed:**
```html
<nav class="page-navigation">
  <button id="tab-dashboard" class="nav-tab active">Dashboard</button>
  <button id="tab-initiatives" class="nav-tab">Initiatives & Milestones</button>
  <button id="tab-accounting" class="nav-tab">Accounting</button>
</nav>

<div class="main-content">
  <!-- Page 1: Dashboard (Default) -->
  <div id="dashboard-content" class="page-content">
    <section id="recent-activity">...</section>
    <section id="task-board">...</section>
  </div>
  
  <!-- Page 2: Initiatives & Milestones -->
  <div id="initiatives-content" class="page-content hidden">
    <section id="portfolio">...</section>
    <section id="orphan-tasks">...</section>
  </div>
  
  <!-- Page 3: Accounting -->
  <div id="accounting-content" class="page-content hidden">
    <section id="charts">...</section>
  </div>
</div>
```

---

### CSS Changes

**Navigation Bar Styling:**
```css
.page-navigation {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-bottom: 2px solid var(--border-color);
}

.nav-tab {
  padding: 0.75rem 1.5rem;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 4px 4px 0 0;
}

.nav-tab:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

.nav-tab.active {
  background: var(--bg-card);
  color: var(--primary-color);
  border-bottom: 2px solid var(--primary-color);
}

.page-content {
  display: block;
  animation: fadeIn 0.2s ease-in;
}

.page-content.hidden {
  display: none;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

---

### Lazy Loading Strategy (SHOULD-have FR-S6)

**Initial Load:**
- Fetch Dashboard page data only
- Defer Initiatives and Accounting data

**First Tab Click:**
- Fetch page data if not already loaded
- Show loading skeleton while fetching
- Cache data for subsequent visits

**Implementation:**
```javascript
const pageDataLoaded = {
  dashboard: true,   // Loaded by default
  initiatives: false,
  accounting: false
};

async function showPage(pageName) {
  // ... show page content ...
  
  // Lazy load data if needed
  if (!pageDataLoaded[pageName]) {
    showLoadingSkeleton(pageName);
    await loadPageData(pageName);
    pageDataLoaded[pageName] = true;
  }
}
```

---

## Security Considerations

**No New Attack Vectors:**
- Hash-based routing is client-side only (no server exposure)
- All existing XSS protections apply (DOMPurify, CSP headers)
- No new API endpoints (data fetching unchanged)

**Validation:**
- Sanitize page name from URL hash before using in querySelector
- Whitelist valid page names: `['dashboard', 'initiatives', 'accounting']`
- Reject any hash value not in whitelist

---

## Accessibility Considerations

**WCAG 2.1 AA Compliance:**

1. **Keyboard Navigation:**
   - Tab key moves between navigation tabs
   - Enter/Space activates tab
   - Focus visible (outline on focus)

2. **Screen Reader Support:**
   ```html
   <nav role="tablist" aria-label="Dashboard pages">
     <button role="tab" aria-selected="true" aria-controls="dashboard-content">
       Dashboard
     </button>
     <button role="tab" aria-selected="false" aria-controls="initiatives-content">
       Initiatives & Milestones
     </button>
     <button role="tab" aria-selected="false" aria-controls="accounting-content">
       Accounting
     </button>
   </nav>
   ```

3. **Color Contrast:**
   - Active tab: 4.5:1 contrast ratio minimum
   - Inactive tabs: 3:1 contrast ratio minimum

4. **Reduced Motion:**
   ```css
   @media (prefers-reduced-motion: reduce) {
     .page-content {
       animation: none;
     }
   }
   ```

---

## Migration Strategy

### Phase 1: Backend (No Changes Required)
- Flask routes unchanged
- API endpoints unchanged
- WebSocket events unchanged

### Phase 2: Frontend Structure
1. Add navigation bar HTML to `index.html`
2. Wrap existing sections in page containers
3. Add `.hidden` class to non-default pages

### Phase 3: Frontend Logic
1. Implement hash-based routing (`hashchange` listener)
2. Implement `showPage()` function
3. Wire up tab click handlers
4. Test browser back/forward

### Phase 4: Polish
1. Add CSS transitions
2. Implement keyboard shortcuts (optional)
3. Add badge indicators (optional)
4. Test accessibility

### Phase 5: Testing
1. Manual testing (all workflows)
2. Cross-browser testing (Chrome, Firefox, Safari)
3. Mobile responsive testing
4. Accessibility audit (keyboard, screen reader)

---

## Open Questions & Risks

### Open Questions

**Q1:** Should we implement lazy loading (FR-S6) in MVP or defer to v2?
- **Recommendation:** Defer - adds complexity, benefit unclear until user analytics available

**Q2:** Should keyboard shortcuts use Alt+1/2/3 or Ctrl+1/2/3?
- **Recommendation:** Alt+1/2/3 (Ctrl+1/2/3 often used by browsers for tab switching)

**Q3:** Should we show page title in browser tab?
- **Current:** "Agent Dashboard"
- **Proposed:** "Dashboard - Agent Dashboard" or "Initiatives - Agent Dashboard"
- **Recommendation:** Update document.title on page switch for better browser tab identification

### Risks & Mitigations

**R1: Breaking WebSocket Updates Across Pages**
- **Risk:** Page switching disrupts real-time updates
- **Impact:** Users see stale data
- **Mitigation:** Test WebSocket message handling during page transitions; ensure event listeners persist

**R2: Performance Degradation on Mobile**
- **Risk:** Page content too large for mobile rendering
- **Impact:** Slow page transitions, poor UX
- **Mitigation:** Test on actual mobile devices; consider further content reduction for mobile

**R3: User Confusion (Where Did My Content Go?)**
- **Risk:** Users don't understand pages are separated
- **Impact:** "Dashboard is broken, I can't see portfolio" support tickets
- **Mitigation:** 
  - Clear tab labels
  - Tooltips on tabs explaining content
  - User guide documentation update

**R4: Browser Compatibility Issues**
- **Risk:** Hash routing doesn't work on older browsers
- **Impact:** Navigation broken for some users
- **Mitigation:** Test on IE11, Safari 12+, Chrome 90+, Firefox 90+; document minimum browser requirements

---

## Success Metrics

### Quantitative Metrics (Track Post-Launch)

**M1:** Page Transition Time
- **Target:** <200ms P95
- **Measurement:** Performance API timing from tab click to content visible

**M2:** Initial Load Time
- **Target:** <1.5s P95 (no regression from current)
- **Measurement:** Time to interactive (TTI)

**M3:** Scroll Reduction
- **Target:** 80% reduction in vertical scrolling
- **Measurement:** Scroll depth analytics per page

**M4:** Deep Link Usage
- **Target:** 20% of sessions use non-default landing page
- **Measurement:** URL hash on session start (`#initiatives` or `#accounting`)

**M5:** Error Rate
- **Target:** <1% of page transitions result in JavaScript errors
- **Measurement:** Console error tracking

### Qualitative Metrics (User Feedback)

**M6:** User Satisfaction
- **Target:** 4.5/5 stars on "How easy is it to navigate the dashboard?" survey
- **Measurement:** In-app survey after 10 page transitions

**M7:** Feature Discoverability
- **Target:** 90% of users discover all 3 pages within first 3 sessions
- **Measurement:** Telemetry tracking unique pages visited

**M8:** Reduced Cognitive Load
- **Target:** Users report "less overwhelming" in feedback
- **Measurement:** User interviews; free-text feedback analysis

---

## Related Documentation

- **Directive 034:** Specification-Driven Development
- **Directive 035:** Specification Frontmatter Standards
- **ADR-032:** Real-Time Execution Dashboard (original architecture)
- **SPEC-DASH-003:** Initiative Tracking (Portfolio content)
- **SPEC-DASH-002:** Markdown Rendering (affects all pages)

---

## Appendix: Wireframes

### Page 1: Dashboard (Default)

```
┌─────────────────────────────────────────────────────────────┐
│ [Dashboard] [Initiatives & Milestones] [Accounting]         │ ← Navigation Bar
├─────────────────────────────────────────────────────────────┤
│ Sidebar │ Recent Activity                                   │
│ ┌─────┐ │ • Task X changed to done (2m ago)                 │
│ │ 143 │ │ • Task Y assigned to pedro (5m ago)               │
│ │Tasks│ │ • Task Z priority changed to HIGH (10m ago)       │
│ └─────┘ │                                                   │
│ ┌─────┐ │ Live Task Board                                   │
│ │  5  │ │ ┌────────┐ ┌────────┐ ┌────────┐                 │
│ │InPrg│ │ │ INBOX  │ │ASSIGNED│ │  DONE  │                 │
│ └─────┘ │ │        │ │        │ │        │                 │
│         │ │ Task A │ │ Task B │ │ Task C │                 │
│         │ │ Task D │ │ Task E │ │ Task F │                 │
│         │ └────────┘ └────────┘ └────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

### Page 2: Initiatives & Milestones

```
┌─────────────────────────────────────────────────────────────┐
│ [Dashboard] [Initiatives & Milestones] [Accounting]         │
├─────────────────────────────────────────────────────────────┤
│ Sidebar │ Portfolio Overview                                │
│ ┌─────┐ │ ▼ Dashboard Enhancements                  [100%] │
│ │ 143 │ │   ├─ Markdown Rendering (done)            [100%] │
│ │Tasks│ │   ├─ Priority Editing (done)              [100%] │
│ └─────┘ │   └─ Initiative Tracking (done)           [100%] │
│         │                                                   │
│         │ ⚠️ Orphan Tasks (3)                                │
│         │ • Implement caching layer [HIGH]                  │
│         │ • Add logging [MEDIUM]                            │
│         │ • Fix memory leak [CRITICAL]                      │
└─────────────────────────────────────────────────────────────┘
```

### Page 3: Accounting

```
┌─────────────────────────────────────────────────────────────┐
│ [Dashboard] [Initiatives & Milestones] [Accounting]         │
├─────────────────────────────────────────────────────────────┤
│ Sidebar │ Cost & Model Analytics                            │
│ ┌─────┐ │ ┌───────────────────────────────────────────┐   │
│ │ 143 │ │ │ Token Usage Over Time (Line Chart)        │   │
│ │Tasks│ │ │                                           │   │
│ └─────┘ │ │    /\     /\                              │   │
│         │ │   /  \   /  \    /\                       │   │
│         │ │  /    \ /    \  /  \                      │   │
│         │ └───────────────────────────────────────────┘   │
│         │                                                   │
│         │ ┌─────────────┐  ┌─────────────────────────┐    │
│         │ │ Cost/Model  │  │ Top 5 Expensive Tasks   │    │
│         │ │ (Bar Chart) │  │ (Table)                 │    │
│         │ └─────────────┘  └─────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

**End of Specification**
