# Dashboard Enhancements - Batch 2 Technical Design

**Status:** Proposed  
**Created:** 2026-02-06  
**Architect:** Alphonso  
**Related ADRs:** [ADR-038](../adrs/ADR-038-dashboard-docsite-integration.md), [ADR-039](../adrs/ADR-039-dashboard-repository-initialization.md), [ADR-040](../adrs/ADR-040-dashboard-configuration-management.md)  
**Related Specifications:**
- [SPEC-DASH-004: Docsite Integration](../../specifications/llm-dashboard/docsite-integration.md)
- [SPEC-DASH-005: Repository Initialization](../../specifications/llm-dashboard/repository-initialization.md)
- [SPEC-DASH-006: Configuration Management](../../specifications/llm-dashboard/configuration-management.md)

---

## Executive Summary

This document provides unified technical design for three dashboard enhancement features (Batch 2):

1. **Docsite Integration** (ADR-038) — Pattern-based documentation linking with help toolbar
2. **Repository Initialization** (ADR-039) — Bootstrap Bill integration with WebSocket streaming
3. **Configuration Management** (ADR-040) — Hybrid editing for agent configs with validation

**Combined Effort:** 48-63 hours (full implementation) or 37-48 hours (MVP variants)

**Key Architectural Decisions:**
- Client-side link resolution (no server-side doc validation)
- Subprocess execution with WebSocket streaming (or polling fallback)
- Direct file writes with schema validation (no config database)
- Optimistic locking for concurrent edit prevention

---

## Architecture Overview

### High-Level Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Dashboard Frontend                         │
│  ┌────────────────┐ ┌────────────────┐ ┌──────────────────┐   │
│  │ Doc Link       │ │ Init Form      │ │ Config Editor    │   │
│  │ Resolver       │ │ Modal          │ │ (Tabbed UI)      │   │
│  └────────┬───────┘ └────────┬───────┘ └────────┬─────────┘   │
│           │                  │                   │              │
│           │ WebSocket ←──────┼───────────────────┤              │
└───────────┼──────────────────┼───────────────────┼──────────────┘
            │                  │                   │
            ↓                  ↓                   ↓
┌─────────────────────────────────────────────────────────────────┐
│                     Dashboard Backend (Flask)                    │
│  ┌────────────────┐ ┌────────────────┐ ┌──────────────────┐   │
│  │ /api/config/   │ │ /api/init/     │ │ /api/config/     │   │
│  │ docsite        │ │ execute        │ │ llm-service      │   │
│  └────────────────┘ └────────┬───────┘ └────────┬─────────┘   │
│                               │                   │              │
│                    ┌──────────▼──────────┐       │              │
│                    │ Subprocess Manager  │       │              │
│                    │ (Bootstrap Bill)    │       │              │
│                    └──────────┬──────────┘       │              │
└───────────────────────────────┼──────────────────┼──────────────┘
                                │                   │
                     ┌──────────▼──────────┐  ┌────▼──────────┐
                     │ Bootstrap Bill      │  │ Config Files  │
                     │ Agent               │  │ (YAML/JSON/MD)│
                     └─────────────────────┘  └───────────────┘
```

### Component Integration

```
Feature Interaction Flow:

1. Docsite Integration (Static)
   Frontend → Link Resolver → Open in new tab
   (No backend involvement for link resolution)

2. Repository Initialization (Async)
   Frontend → /api/init/execute → Subprocess spawn
                                ↓
                        WebSocket progress events
                                ↓
                        Frontend log update

3. Configuration Management (CRUD)
   Frontend → /api/config/* → Schema validation
                            → File write (YAML/JSON)
                            → WebSocket broadcast update
```

---

## Data Models

### 1. Docsite Configuration

```json
{
  "docsite_base": "http://localhost:8000",
  "github_base": "https://github.com/sddevelopment-be/templates",
  "patterns": {
    "agent": "/agents/{agent-name}/",
    "adr": "/architecture/adrs/{adr-id}/",
    "guide": "/guides/{guide-name}/",
    "spec": "/specifications/{spec-path}/"
  },
  "auto_detect_local": true
}
```

### 2. Initialization Request

```json
{
  "vision": "Build a scalable microservices platform...",
  "constraints": "Must support Docker, Kubernetes...",
  "guidelines": "Follow 12-factor app principles...",
  "mtime": null
}
```

### 3. Initialization Progress Event

```json
{
  "job_id": "init-1738849200",
  "type": "stdout",
  "line": "Creating agent profiles...",
  "timestamp": "2026-02-06T12:15:30Z"
}
```

### 4. Configuration Update Request

```json
{
  "agent": "backend-dev-benny",
  "field": "model",
  "value": "gpt-5-mini",
  "mtime": 1738849100.5
}
```

### 5. Agent Profile Structure

```yaml
---
name: "backend-dev-benny"
description: "Service backends and integration surfaces"
tools: ["bash", "view", "edit", "create", "grep"]
model_override: "gpt-5-mini"
---

## Purpose

Backend Dev Benny specializes in...

## Directives

- Directive 016: ATDD
- Directive 017: TDD
```

---

## API Specifications

### Docsite Integration APIs

#### GET /api/config/docsite

**Purpose:** Return docsite URL configuration for link resolution

**Response:**
```json
{
  "docsite_base": "http://localhost:8000",
  "github_base": "https://github.com/sddevelopment-be/templates",
  "patterns": {...}
}
```

**Performance:** <50ms  
**Caching:** Client-side (1 hour TTL)

---

### Repository Initialization APIs

#### GET /api/init/check

**Purpose:** Check if repository is already initialized

**Response:**
```json
{
  "is_initialized": true,
  "indicators": {
    "agents_dir": true,
    "adr_dir": true,
    "roadmap": true,
    "agent_count": 12
  },
  "warning": "Repository appears initialized. Re-bootstrapping will overwrite files."
}
```

**Performance:** <100ms (file system check)

#### POST /api/init/execute

**Purpose:** Start Bootstrap Bill initialization

**Request Body:**
```json
{
  "vision": "Project vision (min 50 chars)",
  "constraints": "Optional constraints",
  "guidelines": "Optional guidelines"
}
```

**Response:**
```json
{
  "job_id": "init-1738849200",
  "status": "started"
}
```

**WebSocket Events:**
- `init_progress`: Real-time stdout lines
- `init_complete`: Final status with exit code

**Performance:**
- Startup: <500ms
- Duration: 2-5 minutes (Bootstrap Bill execution)
- Progress latency: <100ms per line

---

### Configuration Management APIs

#### GET /api/config/llm-service

**Purpose:** Load LLM service configuration

**Response:**
```json
{
  "config": {
    "default_model": "gpt-5",
    "available_models": [...],
    "agent_overrides": {...}
  },
  "mtime": 1738849100.5
}
```

#### PATCH /api/config/llm-service/agent-mapping

**Purpose:** Update agent-to-model mapping

**Request Body:**
```json
{
  "agent": "backend-dev-benny",
  "field": "model",
  "value": "gpt-5-mini",
  "mtime": 1738849100.5
}
```

**Response:**
```json
{
  "success": true,
  "config": {...}
}
```

**Error Response (Conflict):**
```json
{
  "error": "Configuration modified by another user",
  "conflict": true
}
```

**Performance:** <500ms (validation + write)

#### GET /api/config/agent-profile/:agent_name

**Purpose:** Load agent profile with frontmatter

**Response:**
```json
{
  "name": "backend-dev-benny",
  "frontmatter": {...},
  "content": "## Purpose\n\nBackend Dev Benny...",
  "mtime": 1738849000.0
}
```

#### PUT /api/config/agent-profile/:agent_name

**Purpose:** Update agent profile

**Request Body:**
```json
{
  "frontmatter": {...},
  "content": "Updated markdown content",
  "mtime": 1738849000.0
}
```

**Validation:**
- Required frontmatter fields: name, description, tools
- Path traversal prevention (agent_name whitelist)
- Optimistic locking (mtime check)

---

## Security Architecture

### Threat Model

| Threat                  | Vector                        | Mitigation                                           | Severity |
|-------------------------|-------------------------------|------------------------------------------------------|----------|
| XSS in doc links        | Malicious agent names         | Sanitize names before URL insertion                  | MEDIUM   |
| Path traversal          | Agent profile names           | Whitelist alphanumeric + hyphens                     | HIGH     |
| Command injection       | Bootstrap Bill inputs         | Escape shell characters, use subprocess args array   | HIGH     |
| YAML injection          | Config values                 | Use safe_load, validate against schema               | MEDIUM   |
| Concurrent edit conflict| Multiple users edit config    | Optimistic locking with mtime checks                 | LOW      |
| Subprocess hangs        | Bootstrap Bill never completes| 10-minute timeout, subprocess kill                   | MEDIUM   |

### Validation Rules

**Docsite Link Resolution:**
```javascript
function sanitizeAgentName(name) {
  // Allow: alphanumeric, hyphens, underscores
  return name.replace(/[^a-zA-Z0-9\-_]/g, '');
}
```

**Bootstrap Bill Input Validation:**
```python
def validate_vision(vision):
    if len(vision) < 50:
        raise ValueError("Vision must be at least 50 characters")
    if len(vision) > 5000:
        raise ValueError("Vision too long (max 5000 chars)")
    # Check for suspicious patterns
    if re.search(r'[;&|`$()]', vision):
        raise ValueError("Vision contains invalid characters")
```

**Agent Profile Path Validation:**
```python
def validate_agent_name(name):
    # Prevent path traversal
    if '/' in name or '\\' in name or '..' in name:
        raise ValueError("Invalid agent name")
    # Whitelist pattern
    if not re.match(r'^[a-z0-9\-]+$', name):
        raise ValueError("Agent name must be alphanumeric with hyphens")
```

**Configuration Schema Validation:**
```python
import jsonschema

with open('llm-service/config-schema.json') as f:
    schema = json.load(f)

try:
    jsonschema.validate(config, schema)
except jsonschema.ValidationError as e:
    return error_response(f"Validation failed: {e.message}")
```

---

## Performance Optimization

### Caching Strategy

**Docsite Configuration:**
- **Location:** Client-side (localStorage)
- **TTL:** 1 hour
- **Invalidation:** Manual refresh or server push

**Agent Profiles:**
- **Location:** In-memory backend cache (optional)
- **TTL:** 5 minutes
- **Invalidation:** File watcher or explicit cache clear

**Configuration Files:**
- **No caching:** Always read from disk (ensures consistency)
- **Optimization:** Use file watcher to detect changes

### Performance Targets

| Operation                  | Target P95 | Notes                                    |
|----------------------------|------------|------------------------------------------|
| Doc link resolution        | <1ms       | Synchronous, no I/O                      |
| Docsite config fetch       | <50ms      | Cached client-side after first load      |
| Init check                 | <100ms     | File system stat calls                   |
| Bootstrap Bill start       | <500ms     | Subprocess spawn overhead                |
| Progress event delivery    | <100ms     | WebSocket latency                        |
| Config load                | <200ms     | YAML parsing + schema validation         |
| Config update              | <500ms     | Validation + file write + broadcast      |
| Agent profile load         | <300ms     | Frontmatter parsing                      |
| Agent profile update       | <500ms     | Frontmatter write + validation           |

---

## Implementation Roadmap

### Batch 2 Features: 3-Week Timeline

**Week 1: Docsite Integration (9-12 hours)**
- Days 1-2: Link resolver + configuration endpoint (4h)
- Days 3-4: Auto-linkification (agent names, ADR refs) (4h)
- Day 5: Help toolbar UI (3h)
- Testing + docs (1h)

**Week 2: Repository Initialization (16-21 hours or 14-18h fallback)**
- Days 1-2: UI form + pre-check endpoint (5h)
- Days 3-4: Bootstrap Bill subprocess integration (7h)
- Days 5: WebSocket streaming (6h) OR polling fallback (4h)
- Testing + error handling (4h)

**Week 3: Configuration Management (23-30 hours or 14-18h MVP)**
- Days 1-2: Configuration viewer (tabbed UI) (8h)
- Days 3-4: Inline editing + validation (10h)
- Days 5-6: Agent profile editor (12h full OR 6h MVP)
- Testing + security audit (3h)

**Total Effort:**
- **Full Implementation:** 48-63 hours
- **MVP (polling + simple textarea):** 37-48 hours

---

## Testing Strategy

### Unit Tests (Backend)

**Docsite Integration:**
- Link pattern resolution (5 test cases)
- Configuration endpoint (2 test cases)

**Repository Initialization:**
- Input validation (10 test cases: vision length, special chars, optional fields)
- Subprocess command building (5 test cases)
- Re-bootstrap detection logic (3 test cases)

**Configuration Management:**
- Schema validation (15 test cases: valid/invalid configs)
- Optimistic locking (5 test cases: concurrent edits)
- Agent profile parsing (8 test cases: frontmatter + content)

**Total Unit Tests:** ~53 test cases

### Integration Tests

**Repository Initialization:**
- Full Bootstrap Bill execution (mock subprocess)
- WebSocket event delivery (3 scenarios: success, failure, timeout)

**Configuration Management:**
- File write + read consistency (YAML/JSON round-trip)
- Concurrent edit conflict detection

**Total Integration Tests:** ~8 scenarios

### Manual Testing

**Docsite Integration:**
- Click agent links (verify correct URL)
- Click ADR references (verify navigation)
- Toggle help toolbar (verify links work)
- Test with docsite down (verify graceful failure)

**Repository Initialization:**
- Initialize empty repository (full flow)
- Re-initialize existing repository (warning dialog)
- Test with invalid inputs (error handling)
- Test with Bootstrap Bill failure (error display)

**Configuration Management:**
- View all config tabs (LLM, Stack, Profiles)
- Edit agent mapping (inline)
- Edit agent profile (modal)
- Test concurrent edit conflict (two browser tabs)

---

## Rollout Plan

### Phase 1: Docsite Integration (Low Risk)
- **Deploy:** Immediately after testing
- **Rollback:** Remove link resolver JavaScript file
- **Monitoring:** Track broken link clicks (404 rate)

### Phase 2: Repository Initialization (Medium Risk)
- **Deploy:** After Phase 1 stable (1 week)
- **Rollback:** Hide "Initialize Repository" button
- **Monitoring:** Track subprocess execution time, error rate

### Phase 3: Configuration Management (High Risk)
- **Deploy:** After Phase 2 stable (2 weeks)
- **Rollback:** Restore config files from Git, disable config page
- **Monitoring:** Track config validation errors, file write failures

### Feature Flags (Optional)

```python
FEATURE_FLAGS = {
    'docsite_integration': True,
    'repo_initialization': False,  # Deploy gradually
    'config_management': False     # Deploy last
}
```

---

## Open Questions

1. **Docsite Integration:**
   - Should ADR links fallback to GitHub if local docsite unavailable?
   - Should help toolbar position be configurable (bottom-right vs top-right)?

2. **Repository Initialization:**
   - **CRITICAL:** WebSocket streaming (16-21h) vs polling fallback (14-18h)? 
     *(Recommendation: Start with polling, upgrade to WebSocket in Phase 2)*
   - Should dashboard support initializing external directories (not just current repo)?
   - Should re-bootstrap automatically backup existing files?

3. **Configuration Management:**
   - **CRITICAL:** Full markdown editor (23-30h) vs simple textarea (14-18h MVP)?
     *(Recommendation: MVP first, full editor in Phase 2 if needed)*
   - Should dashboard auto-commit configuration changes to Git?
   - Should validation be strict (block invalid) or permissive (warn but allow)?

---

## Success Metrics

### Usability Metrics
- Time to find agent profile documentation: <10 seconds
- Repository initialization completion rate: >90%
- Configuration edit error rate: <5%
- User satisfaction (survey): >4/5

### Technical Metrics
- Doc link resolution time: <1ms
- Bootstrap Bill execution time: 2-5 minutes (unchanged)
- Config update latency: <500ms P95
- Test coverage: >80%

### Adoption Metrics
- Documentation link clicks per session: >2
- Repositories initialized via dashboard: >50% of new repos
- Configuration edits via dashboard: >30% of total edits

---

## References

### Architectural Decision Records
- **ADR-038:** Dashboard-Docsite Content Integration
- **ADR-039:** Dashboard-Driven Repository Initialization
- **ADR-040:** Dashboard Configuration Management Interface

### Specifications
- **SPEC-DASH-004:** Dashboard-Docsite Content Integration
- **SPEC-DASH-005:** Dashboard-Driven Repository Initialization
- **SPEC-DASH-006:** Dashboard Configuration Management Interface

### Related Designs
- **Batch 1 Design:** `dashboard-enhancements-technical-design.md`
- **ADR-032:** Real-Time Execution Dashboard (foundation)
- **ADR-025:** LLM Service Layer (configuration structure)

### External Dependencies
- **python-frontmatter:** Agent profile parsing
- **ruamel.yaml:** Comment-preserving YAML writes
- **jsonschema:** Configuration validation
- **Bootstrap Bill Agent:** `.github/agents/bootstrap-bill.agent.md`

---

**Architect Approval:** Pending  
**Stakeholder Review:** Required for open questions  
**Implementation Start:** Upon approval + Petra task creation
