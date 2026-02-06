# ADR-040: Dashboard Configuration Management Interface

**Status:** Proposed  
**Date:** 2026-02-06  
**Deciders:** Architect Alphonso, Human-in-Charge  
**Related Specs:** [Configuration Management Specification](../../specifications/llm-dashboard/configuration-management.md)  
**Related ADRs:** [ADR-032: Real-Time Execution Dashboard](ADR-032-real-time-execution-dashboard.md), [ADR-025: LLM Service Layer](ADR-025-llm-service-layer.md)

---

## Context

Agent-augmented development framework relies on multiple configuration files that control agent behavior, model routing, and cost optimization. Currently, modifying these requires manual text editing with risk of syntax errors breaking the system.

**Configuration Files:**
1. `llm-service/config.yaml` — Agent-to-model mappings, task-to-model routing, cost rules
2. `framework/agent_config.json` — Agent stack definitions, tool preferences, service URLs
3. `.github/agents/*.agent.md` — Individual agent profiles (YAML frontmatter + markdown content)

**Current Problems:**
- Configuration errors discovered at runtime (no validation)
- Non-technical stakeholders cannot adjust configurations
- No visibility into current configuration state
- Syntax errors cause hard-to-diagnose failures
- Manual Git commits required to track changes

**Problem Statement:**  
System architects need dashboard interface to view, validate, and edit agent configurations without risking syntax errors or breaking changes.

**Constraints:**
- MUST preserve file-based configuration (files remain source of truth, no database)
- MUST validate against schemas before saving
- MUST support both YAML and JSON formats
- MUST handle agent profile frontmatter + markdown content
- MUST maintain Git audit trail (files tracked in repo)
- SHOULD prevent concurrent edits (optimistic locking)

**Key Requirements (from SPEC-DASH-006):**
- FR-M1: View LLM service configuration (agent mappings, costs, models)
- FR-M2: Edit agent-to-model mappings with validation
- FR-M4: View agent profiles with frontmatter parsing
- FR-M5: Edit agent profile metadata (tools, descriptions)
- FR-S3: Full markdown editor for agent profile content (23-30h) or inline editing only (14-18h MVP)

---

## Decision

Implement **hybrid configuration management** with inline editing for structured fields and form-based editing for complex configurations, backed by schema validation and direct file writes.

### Solution Components

**1. Configuration Viewer (Frontend)**

Tabbed interface showing all configuration sources:

```html
<!-- Configuration Management Page -->
<div id="config-page" class="config-container">
  <nav class="config-tabs">
    <button data-tab="llm-service" class="active">LLM Service</button>
    <button data-tab="agent-stack">Agent Stack</button>
    <button data-tab="agent-profiles">Agent Profiles</button>
  </nav>
  
  <!-- Tab 1: LLM Service Config -->
  <div id="tab-llm-service" class="tab-content active">
    <h2>LLM Service Configuration</h2>
    
    <section class="config-section">
      <h3>Agent-to-Model Mappings</h3>
      <table class="config-table">
        <thead>
          <tr>
            <th>Agent</th>
            <th>Model</th>
            <th>Cost/1K Tokens</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody id="agent-model-mappings">
          <!-- Populated via API -->
        </tbody>
      </table>
      <button class="btn-primary" onclick="addAgentMapping()">+ Add Mapping</button>
    </section>
    
    <section class="config-section">
      <h3>Available Models</h3>
      <table class="config-table">
        <thead>
          <tr>
            <th>Model ID</th>
            <th>Display Name</th>
            <th>Cost (Input)</th>
            <th>Cost (Output)</th>
            <th>Max Tokens</th>
          </tr>
        </thead>
        <tbody id="available-models">
          <!-- Populated via API -->
        </tbody>
      </table>
    </section>
  </div>
  
  <!-- Tab 2: Agent Stack Config (similar structure) -->
  
  <!-- Tab 3: Agent Profiles -->
  <div id="tab-agent-profiles" class="tab-content">
    <h2>Agent Profiles</h2>
    
    <div class="agent-list">
      <div class="agent-card" data-agent="backend-dev-benny">
        <h3>Backend Dev Benny</h3>
        <p class="agent-description">Service backends and integration surfaces</p>
        <button onclick="editAgentProfile('backend-dev-benny')">Edit Profile</button>
      </div>
      <!-- More agent cards... -->
    </div>
  </div>
</div>
```

**2. Inline Editing (Simple Fields)**

Click-to-edit pattern for agent-to-model mappings:

```javascript
// Inline editing for agent-model mapping
function makeEditable(row, field) {
  const cell = row.querySelector(`[data-field="${field}"]`);
  const currentValue = cell.textContent.trim();
  
  if (field === 'model') {
    // Dropdown for model selection
    cell.innerHTML = `
      <select id="edit-${field}-${row.dataset.agent}">
        ${availableModels.map(m => 
          `<option value="${m.id}" ${m.id === currentValue ? 'selected' : ''}>${m.name}</option>`
        ).join('')}
      </select>
      <button onclick="saveEdit(this)">✓</button>
      <button onclick="cancelEdit(this)">✗</button>
    `;
  } else {
    // Text input for simple fields
    cell.innerHTML = `
      <input type="text" value="${currentValue}" />
      <button onclick="saveEdit(this)">✓</button>
      <button onclick="cancelEdit(this)">✗</button>
    `;
  }
}

function saveEdit(button) {
  const cell = button.closest('td');
  const row = button.closest('tr');
  const field = cell.dataset.field;
  const agent = row.dataset.agent;
  const newValue = cell.querySelector('input, select').value;
  
  // Send update to backend
  fetch('/api/config/llm-service/agent-mapping', {
    method: 'PATCH',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({agent, field, value: newValue})
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      cell.textContent = newValue;
      showSuccess('Configuration updated');
    } else {
      showError(data.error);
    }
  });
}
```

**3. Schema Validation (Backend)**

Validate configuration changes before writing to files:

```python
# app.py - Configuration update endpoint with validation
import jsonschema
import yaml

# Load schemas
with open('llm-service/config-schema.json') as f:
    LLM_CONFIG_SCHEMA = json.load(f)

@app.route('/api/config/llm-service/agent-mapping', methods=['PATCH'])
def update_agent_mapping():
    """Update agent-to-model mapping with validation."""
    data = request.json
    agent = data.get('agent')
    field = data.get('field')
    value = data.get('value')
    
    # Load current config
    config_path = 'llm-service/config.yaml'
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Apply change
    if 'agent_overrides' not in config:
        config['agent_overrides'] = {}
    
    if field == 'model':
        config['agent_overrides'][agent] = value
    
    # Validate against schema
    try:
        jsonschema.validate(config, LLM_CONFIG_SCHEMA)
    except jsonschema.ValidationError as e:
        return jsonify({'success': False, 'error': f'Validation failed: {e.message}'}), 400
    
    # Additional business logic validation
    if value not in [m['id'] for m in config.get('available_models', [])]:
        return jsonify({'success': False, 'error': f'Unknown model: {value}'}), 400
    
    # Write back to file (preserve comments with ruamel.yaml)
    from ruamel.yaml import YAML
    yaml_writer = YAML()
    yaml_writer.preserve_quotes = True
    with open(config_path, 'w') as f:
        yaml_writer.dump(config, f)
    
    return jsonify({'success': True, 'config': config})
```

**4. Agent Profile Editor**

Modal editor for agent profiles with frontmatter + markdown support:

```html
<!-- Agent Profile Editor Modal -->
<div id="profile-editor" class="modal">
  <div class="modal-content large">
    <h2>Edit Agent Profile: <span id="profile-agent-name"></span></h2>
    
    <div class="editor-layout">
      <!-- Left: Frontmatter Form -->
      <div class="frontmatter-form">
        <h3>Profile Metadata</h3>
        
        <div class="form-group">
          <label>Agent Name</label>
          <input type="text" id="profile-name" readonly />
        </div>
        
        <div class="form-group">
          <label>Description</label>
          <textarea id="profile-description" rows="3"></textarea>
        </div>
        
        <div class="form-group">
          <label>Tools (comma-separated)</label>
          <input type="text" id="profile-tools" placeholder="bash, view, edit, create" />
        </div>
        
        <div class="form-group">
          <label>Model Override</label>
          <select id="profile-model">
            <option value="">Use default</option>
            <!-- Populated from available models -->
          </select>
        </div>
      </div>
      
      <!-- Right: Markdown Content -->
      <div class="markdown-editor">
        <h3>Profile Content</h3>
        
        <!-- MVP: Simple textarea -->
        <textarea id="profile-content" rows="20" 
                  placeholder="## Purpose&#10;&#10;This agent..."></textarea>
        
        <!-- OPTIONAL (adds 9-12h): Rich markdown editor with preview -->
        <!-- 
        <div class="editor-toolbar">
          <button onclick="insertMarkdown('## ')">H2</button>
          <button onclick="insertMarkdown('**')">Bold</button>
          <button onclick="insertMarkdown('_')">Italic</button>
          <button onclick="insertMarkdown('- ')">List</button>
        </div>
        <div class="editor-panels">
          <textarea id="profile-content-advanced"></textarea>
          <div id="profile-preview" class="markdown-preview"></div>
        </div>
        -->
      </div>
    </div>
    
    <div class="form-actions">
      <button class="btn-secondary" onclick="closeProfileEditor()">Cancel</button>
      <button class="btn-primary" onclick="saveAgentProfile()">Save Changes</button>
    </div>
  </div>
</div>
```

**5. Agent Profile File Writer**

Parse, modify, and write agent profile files:

```python
# app.py - Agent profile update endpoint
import frontmatter

@app.route('/api/config/agent-profile/<agent_name>', methods=['GET'])
def get_agent_profile(agent_name):
    """Load agent profile with frontmatter parsing."""
    profile_path = f'.github/agents/{agent_name}.agent.md'
    
    if not os.path.exists(profile_path):
        return jsonify({'error': 'Agent profile not found'}), 404
    
    with open(profile_path, 'r') as f:
        post = frontmatter.load(f)
    
    return jsonify({
        'name': agent_name,
        'frontmatter': post.metadata,
        'content': post.content
    })

@app.route('/api/config/agent-profile/<agent_name>', methods=['PUT'])
def update_agent_profile(agent_name):
    """Update agent profile with validation."""
    data = request.json
    profile_path = f'.github/agents/{agent_name}.agent.md'
    
    # Validate frontmatter schema
    required_fields = ['name', 'description', 'tools']
    for field in required_fields:
        if field not in data.get('frontmatter', {}):
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Security: Validate agent_name prevents path traversal
    if '/' in agent_name or '\\' in agent_name or '..' in agent_name:
        return jsonify({'error': 'Invalid agent name'}), 400
    
    # Create frontmatter post
    post = frontmatter.Post(
        content=data.get('content', ''),
        **data.get('frontmatter', {})
    )
    
    # Write to file
    with open(profile_path, 'w') as f:
        f.write(frontmatter.dumps(post))
    
    return jsonify({'success': True})
```

**6. Optimistic Locking (Conflict Prevention)**

Prevent concurrent edits with file modification timestamps:

```python
@app.route('/api/config/llm-service', methods=['GET'])
def get_llm_config():
    """Return config with modification timestamp."""
    config_path = 'llm-service/config.yaml'
    mtime = os.path.getmtime(config_path)
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return jsonify({
        'config': config,
        'mtime': mtime  # Client stores this
    })

@app.route('/api/config/llm-service', methods=['PUT'])
def update_llm_config():
    """Update config with optimistic lock check."""
    data = request.json
    config_path = 'llm-service/config.yaml'
    
    # Check for concurrent modification
    current_mtime = os.path.getmtime(config_path)
    client_mtime = data.get('mtime')
    
    if client_mtime and current_mtime > client_mtime:
        return jsonify({
            'error': 'Configuration modified by another user. Please reload and retry.',
            'conflict': True
        }), 409
    
    # ... validation and write ...
```

---

## Alternatives Considered

### Alternative 1: Direct File Editing (Monaco Editor)

**Description:** Embed Monaco Editor (VS Code's editor) for raw YAML/JSON editing.

**Pros:**
- Full control over configuration syntax
- Syntax highlighting and IntelliSense
- Familiar for developers (VS Code-like)

**Cons:**
- 🔴 **No Validation:** Users can introduce syntax errors
- 🔴 **Complex Integration:** Monaco is 2MB+ JavaScript bundle
- 🟡 **Non-Technical Unfriendly:** Requires YAML/JSON knowledge

**Decision:** **REJECTED** — Violates "prevent syntax errors" requirement.

---

### Alternative 2: Configuration Database

**Description:** Store configurations in SQLite, generate files on demand.

**Pros:**
- Transaction support (atomic updates)
- Query capabilities (find all agents using model X)
- Version history built-in

**Cons:**
- 🔴 **Violates File-Based Architecture:** Configurations must be files for Git tracking
- 🔴 **Sync Complexity:** Database ↔ file synchronization error-prone
- 🔴 **Deployment Friction:** Database migrations on config changes

**Decision:** **REJECTED** — Files must remain source of truth (ADR-032, file-based orchestration).

---

### Alternative 3: Read-Only View (No Editing)

**Description:** Dashboard displays configurations but editing still requires text editor.

**Pros:**
- Simple implementation (no write logic)
- No risk of breaking configurations

**Cons:**
- 🔴 **Doesn't Solve Problem:** Users still edit files manually
- 🔴 **Low Value:** Dashboard provides minimal value over `cat config.yaml`

**Decision:** **REJECTED** — Core requirement is editing capability.

---

## Consequences

### Positive

✅ **Syntax Safety:** Schema validation prevents broken configurations  
✅ **Visibility:** Dashboard shows current configuration state clearly  
✅ **Accessibility:** Non-technical stakeholders can adjust mappings  
✅ **Git Integration:** File writes automatically tracked in version control  
✅ **Conflict Prevention:** Optimistic locking prevents concurrent edit issues  
✅ **Incremental Adoption:** MVP (inline editing) delivers value quickly, full editor deferred

### Negative

⚠️ **No Multi-User Real-Time Editing:** Last write wins (acceptable for infrequent config changes)  
⚠️ **File Write Latency:** Validation + write adds 100-500ms per edit  
⚠️ **Limited Markdown Editor (MVP):** Textarea only, no preview/toolbar (full editor adds 9-12h)

### Neutral

ℹ️ **Direct File Writes:** No caching layer, files updated immediately  
ℹ️ **Manual Git Commits:** Dashboard writes files, users commit changes separately

---

## Implementation Notes

### Phase 1: Configuration Viewer (6-8 hours)
1. Build tabbed interface (LLM Service, Agent Stack, Agent Profiles)
2. Create API endpoints to load configurations (`/api/config/*`)
3. Parse YAML/JSON and render as tables/cards
4. Test with existing configuration files

### Phase 2: Inline Editing + Validation (8-10 hours)
1. Implement click-to-edit for agent-model mappings
2. Add schema validation on backend (jsonschema library)
3. Implement file writers with ruamel.yaml (comment preservation)
4. Test validation error handling and user feedback

### Phase 3: Agent Profile Editor (9-12 hours)
1. Build profile editor modal (frontmatter form + markdown textarea)
2. Add frontmatter parsing (python-frontmatter library)
3. Implement profile update endpoint with validation
4. Test with various agent profiles

### Phase 4 (OPTIONAL): Rich Markdown Editor (9-12 hours)
1. Integrate markdown editor library (EasyMDE or SimpleMDE)
2. Add live preview panel
3. Implement toolbar shortcuts (headings, bold, lists)
4. Test markdown rendering consistency with ADR-036

### Testing Strategy
- **Unit Tests:** Schema validation logic (15 test cases)
- **Integration Tests:** Config file read/write with concurrency tests
- **Manual Tests:** Edit agent mappings, agent profiles, view updates
- **Security Tests:** Path traversal attempts, XSS in config values

### Performance Targets
- Config load: <200ms for all tabs
- Inline edit save: <500ms (validation + write)
- Agent profile load: <300ms (frontmatter parsing)
- Optimistic lock check: <50ms

### Security Considerations
- **Path Traversal:** Validate agent_name against whitelist (alphanumeric + hyphens)
- **YAML Injection:** Use safe_load (no arbitrary code execution)
- **XSS Prevention:** Sanitize configuration values before rendering
- **File Permissions:** Ensure dashboard process has write access to config files

---

## Implementation Recommendation

**MVP Approach (14-18 hours):**
- Phase 1: Configuration Viewer
- Phase 2: Inline Editing + Validation
- Phase 3: Agent Profile Editor (simple textarea for markdown)

**Full Implementation (23-30 hours):**
- MVP + Phase 4: Rich Markdown Editor with preview

**Stakeholder Decision Required:** Choose MVP vs Full based on priority of markdown editing UX.

---

## References

- **Specification:** `specifications/llm-dashboard/configuration-management.md` (SPEC-DASH-006)
- **Related ADRs:** ADR-032 (Dashboard), ADR-025 (LLM Service Layer)
- **Configuration Files:**
  - `llm-service/config.yaml` (LLM Service config)
  - `framework/agent_config.json` (Agent stack config)
  - `.github/agents/*.agent.md` (Agent profiles)
- **Schema Files:**
  - `llm-service/config-schema.json`
  - `framework/agent-config-schema.json`

---

## Review Notes

**Architecture Review Status:** Pending stakeholder approval

**Key Questions for Stakeholders:**
1. **MVP vs Full:** Should initial implementation include rich markdown editor (23-30h) or defer to Phase 2 (14-18h MVP)?
2. **Auto-Commit:** Should dashboard auto-commit configuration changes to Git, or leave commits to users?
3. **Validation Strictness:** Should invalid configurations be blocked (strict) or allowed with warnings (permissive)?

**Risks:**
- 🟡 MEDIUM: Concurrent edits could cause conflicts (mitigated by optimistic locking)
- 🟡 MEDIUM: Schema changes require updating validation logic (mitigated by schema-driven approach)
- 🟢 LOW: Configuration errors breaking system (mitigated by validation + rollback via Git)

**Dependencies:**
- Requires schema files (config-schema.json, agent-config-schema.json)
- Requires python-frontmatter library (agent profile parsing)
- Requires ruamel.yaml library (comment-preserving YAML writes)
- Optional: EasyMDE or SimpleMDE for rich markdown editor (Phase 4)
