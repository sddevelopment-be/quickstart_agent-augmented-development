# ADR-041: Dashboard Multi-Page Navigation Architecture

**Status:** Proposed  
**Date:** 2026-02-06  
**Author:** Architect Alphonso  
**Specification:** SPEC-DASH-009  
**Priority:** CRITICAL

---

## Context

The dashboard has accumulated 4 major content sections (Recent Activity, Task Board, Portfolio, Cost Analytics) causing information overload. Current single-page layout requires 5000px vertical scroll, forcing users to spend ~30% of time scrolling vs. consuming information.

**Technical Constraints:**
- WebSocket real-time updates MUST continue across page transitions
- No server-side routing changes allowed (Flask routes unchanged)
- Browser back/forward MUST work (standard navigation expectation)
- Deep linking MUST be supported (URL bookmarking)
- Performance regression NOT acceptable (<1.5s initial load maintained)

**Related ADRs:**
- ADR-032: Real-Time Execution Dashboard (original architecture)
- ADR-037: Dashboard Initiative Tracking (portfolio view)

---

## Decision

Implement **hash-based client-side routing** using vanilla JavaScript with 3 distinct pages organized by user mental model:

1. **Dashboard (Default)** - Operational focus: Recent Activity + Task Board
2. **Initiatives & Milestones** - Strategic focus: Portfolio + Orphans
3. **Accounting** - Financial focus: Cost Analytics

**Key Architectural Choices:**

### 1. Hash-Based URL Routing (Client-Side)

**Selected Approach:**  
Use URL hash fragments (`#dashboard`, `#initiatives`, `#accounting`) for navigation state.

**Rationale:** Hash-based routing satisfies all technical constraints with minimal complexity. Flask routes remain unchanged, browser navigation works automatically, and WebSocket connections persist.

---

### 2. Page Content Organization

**Selected Approach:**  
Wrap existing sections in page containers, use CSS `.hidden` class for visibility toggling.

**Rationale:** CSS class toggling provides instant page transitions (<50ms) while preserving DOM state (scroll position, form inputs). WebSocket event listeners remain attached regardless of page visibility.

---

### 3. Performance Characteristics

**Estimated Time to Interactive:** ~1.3s (+0.1s acceptable)  
**Page Transition Time:** ~215ms (within target with margin)  
**Memory Impact:** +3MB (~7% increase, negligible)

---

## Migration Plan

**Total Estimated Effort:** 7 hours

1. **HTML Structure** (1h): Add navigation bar, wrap sections in page containers
2. **JavaScript Routing** (2h): Implement hash-based routing, page switching logic
3. **CSS Styling** (1h): Navigation bar styles, page transitions
4. **Testing** (2h): Manual, cross-browser, mobile, accessibility
5. **Documentation** (0.5h): Update README with navigation instructions

---

## Security & Accessibility

- **XSS Protection:** Whitelist validation of hash values (no unsanitized DOM insertion)
- **CSP Compliance:** All navigation logic in served JavaScript (no inline handlers)
- **WCAG 2.1 AA:** Keyboard navigation, ARIA roles, 4.5:1 contrast ratio

---

## Success Criteria

- ✅ All 9 MUST-have requirements implemented
- ✅ Page transition time <250ms (P95)
- ✅ Initial load time <1.5s (no regression)
- ✅ Accessibility audit passes
- ✅ Cross-browser testing passes

---

**Next Steps:**
1. Human-in-Charge approval
2. Planning Petra: Create implementation tasks
3. Frontend Freddy: Implement navigation
4. Frontend Freddy: Write tests

---

**End of ADR-041**
