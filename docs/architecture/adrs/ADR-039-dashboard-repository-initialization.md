# ADR-039: Dashboard-Driven Repository Initialization

**Status:** Proposed  
**Date:** 2026-02-06  
**Deciders:** Architect Alphonso, Human-in-Charge  
**Related Specs:** [Repository Initialization Specification](../../specifications/llm-dashboard/repository-initialization.md)  
**Related ADRs:** [ADR-032: Real-Time Execution Dashboard](ADR-032-real-time-execution-dashboard.md), [ADR-007: Agent Declaration](ADR-007-agent-declaration.md)

---

## Context

Repository initialization with the agent-augmented development framework currently requires CLI commands, manual file creation, and understanding of directory structure. This creates friction for non-technical stakeholders and slows project setup.

**Current Process:**
1. Create vision.md, constraints.md, guidelines files manually
2. Run Bootstrap Bill via CLI: `python -m framework.agents.bootstrap_bill --vision ...`
3. Monitor terminal output for completion (2-5 minutes)
4. Handle errors by reading terminal output

**Problem Statement:**  
Team leads need guided repository initialization through dashboard without CLI expertise or file system knowledge.

**Constraints:**
- MUST preserve Bootstrap Bill's scaffolding logic (no reimplementation)
- MUST initialize current repository only (no external directory support for MVP)
- MUST warn users before re-bootstrapping (prevents accidental overwrites)
- MUST provide feedback during 2-5 minute execution (avoid "black box" UX)
- SHOULD support live progress streaming (OPTIONAL: background job fallback acceptable)

**Key Requirements (from SPEC-DASH-005):**
- FR-M1: Web form for vision/constraints/guidelines input
- FR-M2: Bootstrap Bill invocation with validation
- FR-M3: Re-bootstrap warning dialog
- FR-S2: Live progress streaming via WebSocket (14-18h with fallback)

---

## Decision

Implement **guided repository initialization form** with Bootstrap Bill subprocess invocation and real-time progress streaming via WebSocket.

### Solution Components

**1. Initialization UI (Frontend)**

Modal form capturing Bootstrap Bill inputs:

```html
<!-- Initialization Modal -->
<div id="init-modal" class="modal">
  <div class="modal-content">
    <h2>Initialize Repository</h2>
    
    <form id="init-form">
      <div class="form-group required">
        <label for="vision">Project Vision *</label>
        <textarea id="vision" name="vision" rows="5" 
                  placeholder="Describe the project's purpose, goals, and strategic intent..."
                  minlength="50" required></textarea>
        <span class="char-count">0 / 50 minimum</span>
      </div>
      
      <div class="form-group">
        <label for="constraints">Constraints (Optional)</label>
        <textarea id="constraints" name="constraints" rows="4"
                  placeholder="Technical limitations, compliance requirements, platform constraints..."></textarea>
      </div>
      
      <div class="form-group">
        <label for="guidelines">Specific Guidelines (Optional)</label>
        <textarea id="guidelines" name="guidelines" rows="4"
                  placeholder="Coding standards, architectural patterns, tooling preferences..."></textarea>
      </div>
      
      <div class="form-actions">
        <button type="button" class="btn-secondary" onclick="closeInitModal()">Cancel</button>
        <button type="submit" class="btn-primary">Initialize Repository</button>
      </div>
    </form>
    
    <!-- Progress Display (hidden until initialization starts) -->
    <div id="init-progress" class="progress-panel hidden">
      <h3>Initializing Repository...</h3>
      <div class="progress-bar">
        <div class="progress-fill" id="init-progress-fill"></div>
      </div>
      <pre id="init-log" class="log-output"></pre>
    </div>
  </div>
</div>
```

**2. Re-Bootstrap Detection**

Check for existing initialization before proceeding:

```python
# app.py - Pre-initialization check endpoint
@app.route('/api/init/check', methods=['GET'])
def check_initialization():
    """Check if repository is already initialized."""
    indicators = {
        'agents_dir': os.path.exists('.github/agents'),
        'adr_dir': os.path.exists('docs/architecture/adrs'),
        'roadmap': os.path.exists('docs/planning/roadmap.md'),
        'agent_count': len(glob.glob('.github/agents/*.agent.md'))
    }
    
    is_initialized = (
        indicators['agents_dir'] and 
        indicators['agent_count'] >= 3
    )
    
    return jsonify({
        'is_initialized': is_initialized,
        'indicators': indicators,
        'warning': 'Repository appears initialized. Re-bootstrapping will overwrite existing files.' if is_initialized else None
    })
```

**3. Bootstrap Bill Subprocess Execution**

Invoke Bootstrap Bill as subprocess with streaming output:

```python
# app.py - Initialization endpoint
import subprocess
import threading
from queue import Queue

@app.route('/api/init/execute', methods=['POST'])
def execute_initialization():
    """Execute Bootstrap Bill initialization."""
    data = request.json
    vision = data.get('vision', '').strip()
    constraints = data.get('constraints', '').strip()
    guidelines = data.get('guidelines', '').strip()
    
    # Validation
    if len(vision) < 50:
        return jsonify({'error': 'Vision must be at least 50 characters'}), 400
    
    # Create temporary input files
    vision_file = '/tmp/bootstrap_vision.txt'
    with open(vision_file, 'w') as f:
        f.write(vision)
    
    # Build Bootstrap Bill command
    cmd = [
        'python', '-m', 'framework.agents.bootstrap_bill',
        '--vision-file', vision_file,
        '--repo-dir', os.getcwd()
    ]
    
    if constraints:
        constraints_file = '/tmp/bootstrap_constraints.txt'
        with open(constraints_file, 'w') as f:
            f.write(constraints)
        cmd.extend(['--constraints-file', constraints_file])
    
    if guidelines:
        guidelines_file = '/tmp/bootstrap_guidelines.txt'
        with open(guidelines_file, 'w') as f:
            f.write(guidelines)
        cmd.extend(['--guidelines-file', guidelines_file])
    
    # Start subprocess with output streaming
    job_id = f"init-{int(time.time())}"
    output_queue = Queue()
    
    def run_bootstrap():
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        for line in process.stdout:
            output_queue.put({'type': 'stdout', 'line': line.rstrip()})
            socketio.emit('init_progress', {
                'job_id': job_id,
                'line': line.rstrip()
            }, namespace='/dashboard')
        
        exit_code = process.wait()
        output_queue.put({'type': 'complete', 'exit_code': exit_code})
        socketio.emit('init_complete', {
            'job_id': job_id,
            'exit_code': exit_code,
            'success': exit_code == 0
        }, namespace='/dashboard')
    
    thread = threading.Thread(target=run_bootstrap, daemon=True)
    thread.start()
    
    return jsonify({'job_id': job_id, 'status': 'started'})
```

**4. WebSocket Progress Streaming**

Real-time output forwarding to dashboard:

```javascript
// dashboard.js - Progress streaming handler
socket.on('init_progress', function(data) {
  const logElement = document.getElementById('init-log');
  logElement.textContent += data.line + '\n';
  logElement.scrollTop = logElement.scrollHeight;  // Auto-scroll
  
  // Update progress bar based on output keywords
  if (data.line.includes('Creating agent profiles')) {
    updateProgressBar(40);
  } else if (data.line.includes('Creating ADR templates')) {
    updateProgressBar(70);
  } else if (data.line.includes('Initialization complete')) {
    updateProgressBar(100);
  }
});

socket.on('init_complete', function(data) {
  if (data.success) {
    showSuccess('Repository initialized successfully!');
    setTimeout(() => window.location.reload(), 2000);
  } else {
    showError('Initialization failed. Check logs for details.');
  }
});
```

**5. Fallback: Background Job**

Alternative to streaming for simplicity (reduces implementation from 16-21h to 14-18h):

```python
# Simplified version without streaming
@app.route('/api/init/execute', methods=['POST'])
def execute_initialization_simple():
    """Execute Bootstrap Bill as background job."""
    # ... validation code same as above ...
    
    # Start subprocess in background
    job_id = f"init-{int(time.time())}"
    
    def run_bootstrap():
        result = subprocess.run(cmd, capture_output=True, text=True)
        # Store result in session or database
        init_results[job_id] = {
            'exit_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    
    thread = threading.Thread(target=run_bootstrap, daemon=True)
    thread.start()
    
    return jsonify({'job_id': job_id, 'status': 'started'})

@app.route('/api/init/status/<job_id>', methods=['GET'])
def check_initialization_status(job_id):
    """Poll for initialization completion."""
    if job_id in init_results:
        return jsonify(init_results[job_id])
    return jsonify({'status': 'running'})
```

---

## Alternatives Considered

### Alternative 1: Direct Agent Invocation (No Subprocess)

**Description:** Import Bootstrap Bill as Python module and call directly.

**Pros:**
- Simpler integration (no subprocess management)
- Easier error handling (Python exceptions)

**Cons:**
- 🔴 **Blocking:** Ties up Flask worker thread for 2-5 minutes
- 🔴 **Fragile:** Assumes Bootstrap Bill is importable library
- 🟡 **Output Capture:** More complex to stream stdout/stderr

**Decision:** **REJECTED** — Blocking Flask thread unacceptable for multi-user dashboard.

---

### Alternative 2: External Directory Initialization

**Description:** Allow initializing arbitrary directories (not just current repo).

**Pros:**
- More flexible (initialize multiple projects from dashboard)
- Better for "project creation" workflow

**Cons:**
- 🔴 **Security Risk:** Path traversal vulnerabilities
- 🔴 **Complexity:** File browser UI, permission management
- 🟡 **Scope Creep:** Not required for MVP use case

**Decision:** **REJECTED for MVP** — Defer to future enhancement. Confirm with user (they specified "current dir only").

---

### Alternative 3: Polling-Based Progress (No WebSocket)

**Description:** Client polls `/api/init/status/<job_id>` every 2 seconds.

**Pros:**
- Simpler implementation (no WebSocket complexity)
- Works with any HTTP client (no socket.io dependency)

**Cons:**
- 🟡 **Latency:** 2-second delay before showing progress
- 🟡 **Server Load:** N users = N polling requests/sec
- 🟡 **User Experience:** Feels less responsive than streaming

**Decision:** **ACCEPTED AS FALLBACK** — Use polling if WebSocket streaming proves too complex. Spec indicates this is acceptable (14-18h vs 16-21h).

---

## Consequences

### Positive

✅ **Guided Workflow:** Form eliminates need for file structure knowledge  
✅ **Real-Time Feedback:** Users see progress (no "black box" waiting)  
✅ **Safety:** Re-bootstrap warning prevents accidental data loss  
✅ **Validation:** Input validation catches errors before execution  
✅ **Audit Trail:** Initialization logged via Git commits (Bootstrap Bill behavior)

### Negative

⚠️ **Single Repository:** Cannot initialize external directories (deferred to future)  
⚠️ **No Rollback:** Failed initialization requires manual cleanup  
⚠️ **WebSocket Complexity:** Streaming adds implementation complexity (fallback available)

### Neutral

ℹ️ **Current Dir Only:** Initializes repository where dashboard is running  
ℹ️ **2-5 Minute Duration:** Users must wait for completion (expected for setup task)

---

## Implementation Notes

### Phase 1: UI and Validation (4-5 hours)
1. Create initialization modal with form
2. Implement client-side validation (50-char minimum for vision)
3. Add re-bootstrap detection (/api/init/check endpoint)
4. Build warning dialog for re-bootstrap confirmation

### Phase 2: Bootstrap Bill Integration (6-8 hours)
1. Create subprocess execution endpoint (/api/init/execute)
2. Handle temporary file creation (vision, constraints, guidelines)
3. Test subprocess invocation with various input combinations
4. Implement error handling (subprocess failures, timeouts)

### Phase 3: Progress Streaming (6-8 hours for WebSocket, 4-5 hours for polling)
1. **WebSocket Option:** Implement real-time output forwarding
2. **Polling Option:** Implement status polling endpoint
3. Build progress UI (log output, progress bar)
4. Test completion detection and success/error states

### Testing Strategy
- **Unit Tests:** Input validation (vision length, optional fields)
- **Integration Tests:** Subprocess invocation with mock Bootstrap Bill
- **Manual Tests:** Full initialization flow on test repository
- **Error Scenarios:** Invalid inputs, Bootstrap Bill failures, timeout handling

### Performance Targets
- Form validation: <50ms
- Initialization start: <500ms (subprocess spawn)
- Progress updates: <100ms latency (WebSocket) or <2s (polling)
- Total duration: 2-5 minutes (Bootstrap Bill execution time)

### Security Considerations
- **Input Sanitization:** Escape shell characters in vision/constraints/guidelines
- **Path Validation:** Ensure Bootstrap Bill operates on current directory only
- **Timeout:** Kill subprocess after 10 minutes (prevent hangs)
- **Temp File Cleanup:** Delete input files after execution

---

## References

- **Specification:** `specifications/llm-dashboard/repository-initialization.md` (SPEC-DASH-005)
- **Related ADRs:** ADR-032 (Dashboard), ADR-007 (Agent Declaration)
- **Bootstrap Bill Profile:** `.github/agents/bootstrap-bill.agent.md`
- **Repository Structure:** `docs/architecture/repository-structure.md`

---

## Review Notes

**Architecture Review Status:** Pending stakeholder approval

**Key Questions for Stakeholders:**
1. **WebSocket vs Polling:** Should MVP use WebSocket streaming (16-21h) or polling fallback (14-18h)?
2. **External Directories:** Defer to future or include in initial implementation?
3. **Re-bootstrap Backup:** Should system auto-backup existing files before re-initialization?

**Risks:**
- 🟡 MEDIUM: Subprocess hangs could block dashboard (mitigated by timeout)
- 🟡 MEDIUM: Bootstrap Bill changes could break integration (mitigated by stable interface)
- 🟢 LOW: Users accidentally re-initialize (mitigated by warning dialog)

**Dependencies:**
- Requires Bootstrap Bill agent (already exists)
- Requires subprocess support (Python standard library)
- Optional: WebSocket infrastructure (already exists for dashboard)
