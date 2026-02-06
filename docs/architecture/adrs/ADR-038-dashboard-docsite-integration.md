# ADR-038: Dashboard-Docsite Content Integration

**Status:** Proposed  
**Date:** 2026-02-06  
**Deciders:** Architect Alphonso, Human-in-Charge  
**Related Specs:** [Dashboard-Docsite Integration Specification](../../specifications/llm-dashboard/docsite-integration.md)  
**Related ADRs:** [ADR-032: Real-Time Execution Dashboard](ADR-032-real-time-execution-dashboard.md), [ADR-036: Dashboard Markdown Rendering](ADR-036-dashboard-markdown-rendering.md)

---

## Context

The dashboard operates as a standalone monitoring tool with no connection to the project's documentation site. Users must context-switch to GitHub or local docsite to reference agent profiles, ADRs, guides, or architectural documentation. This friction slows decision-making during active development sessions.

**Problem Statement:**  
Engineers monitoring dashboard need quick access to relevant documentation without leaving their monitoring session or losing situational awareness.

**Constraints:**
- MUST NOT duplicate documentation content in dashboard (single source of truth)
- MUST work with local docsite (http://localhost:8000) and GitHub Pages
- MUST handle missing documentation gracefully (broken links acceptable)
- SHOULD NOT require complex parsing of documentation structure
- MUST remain lightweight (<20KB JavaScript overhead)

**Key Requirements (from SPEC-DASH-004):**
- FR-M1: Context-aware agent profile links (agent names → profiles)
- FR-M2: Help toolbar with documentation shortcuts
- FR-M3: External docsite link (configurable URL)
- FR-S1: Context-aware ADR links (ADR-XXX → documents)

---

## Decision

Implement **minimal documentation linking** using pattern-based URL resolution with a help toolbar for persistent documentation access.

### Solution Components

**1. Link Resolution Engine (Client-Side)**

JavaScript resolver that converts dashboard entities to documentation URLs:

```javascript
// Link resolver (dashboard-doc-links.js)
const DOC_CONFIG = {
  docsiteBase: 'http://localhost:8000',  // Configurable
  githubBase: 'https://github.com/sddevelopment-be/templates',
  patterns: {
    agent: '/agents/{agent-name}/',
    adr: '/architecture/adrs/{adr-id}/',
    guide: '/guides/{guide-name}/',
    spec: '/specifications/{spec-path}/'
  }
};

function resolveAgentLink(agentName) {
  // "backend-dev-benny" → "http://localhost:8000/agents/backend-dev-benny/"
  return DOC_CONFIG.docsiteBase + DOC_CONFIG.patterns.agent
    .replace('{agent-name}', slugify(agentName));
}

function resolveADRLink(adrId) {
  // "ADR-035" → "http://localhost:8000/architecture/adrs/ADR-035/"
  return DOC_CONFIG.docsiteBase + DOC_CONFIG.patterns.adr
    .replace('{adr-id}', adrId);
}
```

**2. Context-Aware Link Injection**

Automatic linkification of recognized patterns in dashboard:

```javascript
// Auto-linkify agent names in task cards
function linkifyAgentNames(taskCard) {
  const agentSpan = taskCard.querySelector('.task-agent');
  if (agentSpan) {
    const agentName = agentSpan.textContent;
    agentSpan.innerHTML = `
      <a href="${resolveAgentLink(agentName)}" 
         target="_blank" 
         class="agent-link"
         title="View ${agentName} profile">
        ${agentName} <span class="external-icon">↗</span>
      </a>
    `;
  }
}

// Auto-linkify ADR references in descriptions
function linkifyADRReferences(textContent) {
  return textContent.replace(
    /\b(ADR-\d{3})\b/g,
    '<a href="' + resolveADRLink('$1') + '" target="_blank" class="adr-link">$1 ↗</a>'
  );
}
```

**3. Help Toolbar**

Persistent toolbar providing access to key documentation sections:

```html
<!-- Help toolbar (fixed position, bottom-right) -->
<div id="help-toolbar" class="help-toolbar">
  <button class="help-toggle" aria-label="Documentation help">
    <span class="icon">📚</span>
  </button>
  
  <div class="help-menu hidden">
    <h3>Documentation</h3>
    <ul class="help-links">
      <li><a href="{docsite}/agents/" target="_blank">Agent Profiles</a></li>
      <li><a href="{docsite}/architecture/adrs/" target="_blank">ADRs</a></li>
      <li><a href="{docsite}/guides/" target="_blank">Guides</a></li>
      <li><a href="{docsite}/specifications/" target="_blank">Specifications</a></li>
      <li class="divider"></li>
      <li><a href="{github}/docs-site/" target="_blank">Full Documentation ↗</a></li>
    </ul>
  </div>
</div>
```

**4. Configuration Management**

Dashboard backend provides docsite URL configuration:

```python
# app.py - Configuration endpoint
@app.route('/api/config/docsite', methods=['GET'])
def get_docsite_config():
    """Return docsite URL configuration."""
    config = {
        'docsite_base': os.getenv('DOCSITE_URL', 'http://localhost:8000'),
        'github_base': 'https://github.com/sddevelopment-be/templates',
        'auto_detect_local': True  # Try localhost:8000 first
    }
    return jsonify(config)
```

**5. Graceful Degradation**

Handle missing documentation without breaking dashboard:

- Broken links open in new tab (users see 404, can navigate back)
- No server-side validation of documentation existence
- Help toolbar always visible (even if links fail)
- Console warnings for failed link resolutions (debugging)

---

## Alternatives Considered

### Alternative 1: Embedded Documentation Viewer

**Description:** Embed iframe or fetch documentation content directly into dashboard sidebar.

**Pros:**
- No context switching (docs visible in dashboard)
- Could cache frequently accessed docs

**Cons:**
- 🔴 **Complexity:** Requires markdown parsing, styling, navigation in dashboard
- 🔴 **Maintenance:** Duplicates docsite rendering logic
- 🔴 **Performance:** Fetching and rendering docs adds latency
- 🔴 **UX:** Splits screen real estate, reduces dashboard visibility

**Decision:** **REJECTED** — Violates "single source of truth" and adds significant complexity.

---

### Alternative 2: Server-Side Link Validation

**Description:** Backend validates documentation existence before generating links.

**Pros:**
- Prevents broken links (better UX)
- Could provide "missing docs" warnings

**Cons:**
- 🔴 **Latency:** File system checks add 10-50ms per link
- 🔴 **Complexity:** Requires docsite structure knowledge in backend
- 🔴 **Fragility:** Breaks if docsite structure changes
- 🟡 **Overkill:** Users can handle 404 pages gracefully

**Decision:** **REJECTED** — Optimization not worth complexity trade-off.

---

### Alternative 3: GraphQL Documentation API

**Description:** Build API to query documentation structure and content.

**Pros:**
- Powerful querying (find all ADRs, agents, etc.)
- Could support search and filtering

**Cons:**
- 🔴 **Massive Complexity:** Requires building entire API layer
- 🔴 **Maintenance:** Documentation API must stay synchronized with docs
- 🔴 **Overkill:** Dashboard only needs simple link resolution

**Decision:** **REJECTED** — Complexity vastly exceeds requirements.

---

## Consequences

### Positive

✅ **Minimal Complexity:** Pattern-based resolution requires <20KB JavaScript  
✅ **Fast Implementation:** 9-12 hours estimated (simple URL templates)  
✅ **Maintainable:** No tight coupling to docsite structure  
✅ **Discoverable:** Help toolbar makes documentation access obvious  
✅ **Flexible:** Docsite URL configurable (localhost, GitHub Pages, custom)  
✅ **Graceful:** Broken links don't break dashboard functionality

### Negative

⚠️ **No Link Validation:** Broken links possible if docs move or missing  
⚠️ **Manual Configuration:** Users must set docsite URL if not using defaults  
⚠️ **Limited Intelligence:** Cannot detect renamed agents or ADRs automatically

### Neutral

ℹ️ **Opens in New Tab:** All doc links open externally (preserves dashboard state)  
ℹ️ **Local Docsite Assumed:** Defaults to http://localhost:8000 (requires MkDocs running)

---

## Implementation Notes

### Phase 1: Link Resolution Engine (3-4 hours)
1. Create `dashboard-doc-links.js` with pattern-based resolver
2. Add configuration endpoint `/api/config/docsite`
3. Test link generation for agents, ADRs, guides

### Phase 2: Auto-Linkification (3-4 hours)
1. Inject agent links into task cards
2. Auto-linkify ADR references (regex: `ADR-\d{3}`)
3. Add CSS styling for doc links (icon, hover states)

### Phase 3: Help Toolbar (3-4 hours)
1. Build toolbar UI component (fixed bottom-right)
2. Populate with standard documentation links
3. Add toggle interaction (show/hide menu)
4. Test accessibility (keyboard navigation, ARIA labels)

### Testing Strategy
- **Unit Tests:** Link resolver functions (10 test cases)
- **Integration Tests:** API endpoint returns valid config
- **Manual Tests:** Click agent names, ADR refs, toolbar links
- **Accessibility:** Keyboard navigation, screen reader compatibility

### Performance Targets
- Link resolution: <1ms (synchronous, no I/O)
- Configuration fetch: <50ms
- Toolbar toggle: <16ms (60fps interaction)

### Security Considerations
- **XSS Prevention:** Sanitize agent names before URL insertion
- **URL Validation:** Whitelist allowed URL schemes (http, https)
- **No Sensitive Data:** Configuration endpoint exposes no secrets

---

## References

- **Specification:** `specifications/llm-dashboard/docsite-integration.md` (SPEC-DASH-004)
- **Related ADRs:** ADR-032 (Dashboard), ADR-036 (Markdown Rendering)
- **MkDocs Structure:** `docs-site/` directory
- **Agent Profiles:** `.github/agents/*.agent.md`
- **ADR Location:** `docs/architecture/adrs/`

---

## Review Notes

**Architecture Review Status:** Pending stakeholder approval

**Key Questions for Stakeholders:**
1. Should docsite URL auto-detection try multiple ports (8000, 8001)?
2. Should ADR links fallback to GitHub if local docsite unavailable?
3. Is help toolbar positioned correctly (bottom-right vs top-right)?

**Risks:**
- 🟡 LOW: Users may not discover help toolbar (mitigated by icon + tooltip)
- 🟡 LOW: Docsite structure changes break links (acceptable, easy to fix)

**Dependencies:**
- Requires MkDocs docsite running locally (existing setup)
- Works with ADR-036 (markdown rendering) for linkified task descriptions
