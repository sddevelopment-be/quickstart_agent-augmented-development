# ADR-034: MCP Server Integration Strategy

**status**: Accepted  
**date**: 2026-02-05  
**author**: Architect Alphonso  
**approved-by**: Human-in-Charge

## Context

The [kitty-cli comparative analysis](../../design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md) and subsequent [architecture impact analysis](../../../work/reports/architecture/2026-02-05-kitty-cli-architecture-impact-analysis.md) revealed that **Model Context Protocol (MCP) servers** represent a critical integration pattern for modern LLM-augmented development workflows.

### What is MCP?

**Model Context Protocol (MCP)** is an open standard protocol for LLM tools to access external capabilities through server processes. MCP servers provide:

- **File System Operations** - Read/write/search files (`@modelcontextprotocol/server-filesystem`)
- **Git Operations** - Commit/diff/log (`@modelcontextprotocol/server-git`)
- **Web Search** - External knowledge retrieval
- **Code Search** - Semantic code navigation
- **Database Access** - Query structured data
- **API Integration** - External service calls

MCP servers run as independent processes and expose capabilities via standardized JSON-RPC protocol over stdio or HTTP.

### Current State Problems

1. **No MCP Support**
   - Our LLM Service Layer routes to CLI tools (claude-code, codex) but doesn't declare or manage MCP server requirements
   - Users must manually configure MCP servers for each tool
   - No validation that required servers are available before execution

2. **Tool Capability Opacity**
   - Configuration doesn't document what MCP tools are required/recommended for each LLM tool
   - Users don't know which MCP servers to install for their workflows
   - No guidance on optional vs. essential capabilities

3. **No Lifecycle Management**
   - Users manually start MCP servers before using LLM tools
   - No health checks or connection validation
   - Server failures only discovered during LLM execution

4. **No Discovery Mechanism**
   - Users can't enumerate available MCP tools at runtime
   - No way to detect server capabilities programmatically
   - Manual configuration required for every tool addition

### kitty-cli Learnings

**What kitty-cli Does (Passive Declarations):**
```yaml
# missions/software-dev/mission.yaml
mcp_tools:
  required: [filesystem, git]
  recommended: [code-search, test-runner]
  optional: [github, gitlab]
```

**What kitty-cli Does NOT Do:**
- ❌ Start/stop MCP servers automatically
- ❌ Validate server availability before execution
- ❌ Configure server connections
- ❌ Health check servers during execution
- ❌ Discover tools dynamically

**Our Opportunity:** Implement active MCP server management to exceed kitty-cli's capabilities.

## Decision

**We will implement a two-phase MCP integration strategy:**

### Phase 1 (Milestone 3): Passive Declarations

**Adopt kitty-cli's declarative pattern without lifecycle management.**

**Configuration Schema:**
```yaml
# config/tools.yaml
tools:
  claude-code:
    binary: claude
    command_template: "{binary} {prompt_file} --model {model}"
    models: [claude-3.5-sonnet, claude-3-opus]
    
    # NEW: MCP tool requirements (documentation-only in M3)
    mcp_tools:
      required: [filesystem, git]        # Must be available
      recommended: [code-search]         # Enhances capabilities
      optional: [github, gitlab]         # Nice-to-have
    
    # NEW: Role-based tool restrictions
    role_restrictions:
      implementation:
        allowed_tools: [filesystem.write, git.commit, bash]
      review:
        allowed_tools: [filesystem.read, git.log, grep]
```

**Validation (M3):**
- Check that declared MCP tools are referenced consistently
- Warn if required tools not documented in tool-specific configs
- NO runtime server validation (users manage servers)

---

### Phase 2 (Milestone 4): Active Lifecycle Management

**Implement automatic MCP server startup, health checks, and discovery.**

**Configuration Schema:**
```yaml
# config/mcp_servers.yaml (NEW file)
mcp_servers:
  filesystem:
    package: "@modelcontextprotocol/server-filesystem"
    command: "npx -y @modelcontextprotocol/server-filesystem /allowed/path"
    auto_start: true                    # Start automatically when needed
    health_check:
      method: "tool_call"
      tool: "filesystem.list_directory"
      args: {path: "/tmp"}
      timeout_seconds: 5
    
  git:
    package: "@modelcontextprotocol/server-git"
    command: "npx -y @modelcontextprotocol/server-git"
    auto_start: true
    health_check:
      method: "tool_call"
      tool: "git.status"
      timeout_seconds: 3
  
  code-search:
    package: "@modelcontextprotocol/server-code-search"
    command: "npx -y @modelcontextprotocol/server-code-search --index-path .code-index"
    auto_start: false                   # User manages lifecycle
    health_check:
      method: "ping"
      timeout_seconds: 2

# Global MCP settings
mcp_settings:
  auto_start_default: false             # Opt-in per server
  health_check_interval_seconds: 30
  startup_timeout_seconds: 10
  shutdown_timeout_seconds: 5
  log_directory: "logs/mcp_servers"
```

**Lifecycle Management (M4):**
```python
# Server lifecycle operations
mcp_manager.start_server("filesystem")       # Start if not running
mcp_manager.stop_server("filesystem")        # Graceful shutdown
mcp_manager.health_check("filesystem")       # Verify availability
mcp_manager.restart_server("filesystem")     # Stop + start

# Discovery operations
tools = mcp_manager.discover_tools("filesystem")
# → Returns: ["filesystem.read", "filesystem.write", "filesystem.search", ...]

capabilities = mcp_manager.get_capabilities("git")
# → Returns: {"tools": [...], "resources": [...], "prompts": [...]}
```

**Dashboard Integration (M4):**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ MCP Server Status                           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ filesystem    ✅ Running    5 tools          │
│ git           ✅ Running    8 tools          │
│ code-search   ⚠️  Manual     12 tools        │
│ github        ❌ Stopped    -                │
└─────────────────────────────────────────────┘
```

## Rationale

### Why Two-Phase Approach?

**Phase 1 Benefits:**
- ✅ **Quick Implementation** - Documentation-only (2-3 hours)
- ✅ **Low Risk** - No operational complexity added
- ✅ **Foundation** - Sets schema for M4 active management
- ✅ **User Guidance** - Documents tool requirements clearly

**Phase 2 Benefits:**
- ✅ **Automation** - Eliminates manual server startup
- ✅ **Reliability** - Health checks detect failures early
- ✅ **Discovery** - Runtime tool enumeration
- ✅ **Competitive Advantage** - Exceeds kitty-cli capabilities

**Why NOT Combine?**
- ⚠️ M3 timeline constrained (CLI UX improvements prioritized)
- ⚠️ Active management requires subprocess management complexity
- ⚠️ Health checks need careful design for reliability
- ✅ Phased approach reduces risk, allows iteration based on M3 feedback

---

### Why MCP Over Direct API Integration?

**MCP Advantages:**
- ✅ **Standardized Protocol** - Industry-wide adoption by Anthropic, Google, others
- ✅ **Extensibility** - Community can create new servers without code changes
- ✅ **Process Isolation** - Servers run in separate processes (security boundary)
- ✅ **Language Agnostic** - Servers in any language (Python, Node.js, Go, Rust)
- ✅ **Reusable** - Same server works with multiple LLM tools

**Trade-offs Accepted:**
- ⚠️ **Subprocess Overhead** - Starting servers adds latency (~100-500ms)
- ⚠️ **Node.js Dependency** - Most MCP servers require Node.js runtime
- ⚠️ **Configuration Complexity** - Server configs + tool configs = more YAML

---

### Why Optional Auto-Start?

**Flexibility:**
- ✅ **Development** - Auto-start ON for fast iteration
- ✅ **Production** - Auto-start OFF for controlled environments
- ✅ **CI/CD** - Pre-started servers for deterministic builds
- ✅ **Debugging** - Manual start allows log inspection

**Default:** `auto_start: false` (opt-in for safety)

---

### Why 3-Tier Tool Classification?

**Alignment with kitty-cli Pattern:**
- **Required** - Execution fails without these tools (hard dependency)
- **Recommended** - Capabilities significantly enhanced (soft dependency)
- **Optional** - Nice-to-have features (zero pressure)

**Benefits:**
- ✅ **Clear Expectations** - Users know what to install
- ✅ **Progressive Enhancement** - System works without optional tools
- ✅ **Graceful Degradation** - Warns if recommended tools missing
- ✅ **Onboarding Simplicity** - Start with required tools only

---

### Why Role-Based Tool Restrictions?

**Security Pattern from kitty-cli:**
```python
# Claude invoker restricts tools by role
if role == "implementation":
    allowed = ["Read", "Write", "Edit", "Bash", "Grep"]
elif role == "review":
    allowed = ["Read", "Grep"]  # Read-only
```

**Benefits:**
- ✅ **Security** - Review agents can't modify code
- ✅ **Intent Clarity** - Permissions match workflow phase
- ✅ **Error Prevention** - Restricts accidental destructive operations
- ✅ **Compliance** - Audit trail shows restricted operations

**Application to MCP:**
```yaml
role_restrictions:
  implementation:
    allowed_tools: [filesystem.write, filesystem.delete, git.commit]
  review:
    allowed_tools: [filesystem.read, git.log, git.diff]
```

## Envisioned Consequences

### Positive Consequences

**Phase 1 (Passive Declarations):**

1. ✅ **Documentation Improvement**
   - Users know which MCP servers to install
   - Tool requirements clearly documented
   - Onboarding friction reduced

2. ✅ **Configuration Foundation**
   - Schema ready for M4 active management
   - Validation patterns established
   - Migration path clear

3. ✅ **Competitive Parity**
   - Matches kitty-cli's declarative approach
   - Establishes MCP as first-class concern
   - Signals future enhancements

**Phase 2 (Active Management):**

4. ✅ **Automation**
   - Users don't manually start servers
   - Health checks detect failures early
   - Graceful restarts on errors

5. ✅ **Reliability**
   - Pre-flight validation before execution
   - Real-time health monitoring
   - Dashboard visibility into server status

6. ✅ **Competitive Advantage**
   - Exceeds kitty-cli's passive declarations
   - Only LLM service with active MCP management
   - Unique selling point for marketing

7. ✅ **Developer Experience**
   - Runtime tool discovery
   - Automatic capability detection
   - Reduced configuration burden

### Negative Consequences

**Phase 1:**

1. ⚠️ **Documentation Overhead**
   - Every tool needs MCP tool declarations
   - *Mitigation:* Template-based config generation (ADR-031)

2. ⚠️ **No Runtime Enforcement**
   - Users can still run tools without required MCP servers
   - *Mitigation:* Clear warnings in CLI output, validation in M4

**Phase 2:**

3. ⚠️ **Subprocess Management Complexity**
   - Starting/stopping servers adds code complexity
   - *Mitigation:* Use proven subprocess patterns, extensive testing

4. ⚠️ **Node.js Dependency**
   - Most MCP servers require Node.js runtime
   - *Mitigation:* Document requirement, check availability, support pre-started servers

5. ⚠️ **Resource Consumption**
   - Multiple MCP servers consume memory (~50-100MB each)
   - *Mitigation:* Lazy start (only when needed), automatic shutdown on idle

6. ⚠️ **Configuration Complexity**
   - mcp_servers.yaml + tools.yaml = more files to manage
   - *Mitigation:* Sensible defaults, template generation, clear documentation

### Risk Mitigation Strategies

**Subprocess Reliability:**
```python
# Graceful error handling
try:
    server = mcp_manager.start_server("filesystem")
except ServerStartupError as e:
    logger.warning(f"Failed to start filesystem server: {e}")
    logger.info("Continuing without filesystem MCP tools")
    # Execution continues with degraded capabilities
```

**Health Check Failures:**
```python
# Automatic recovery
if not mcp_manager.health_check("git"):
    logger.warning("Git server unhealthy, attempting restart")
    mcp_manager.restart_server("git")
    if mcp_manager.health_check("git"):
        logger.info("Git server recovered")
    else:
        logger.error("Git server restart failed, disabling git tools")
```

**Node.js Availability:**
```python
# Pre-flight checks
if not shutil.which("node") and not shutil.which("npx"):
    logger.warning("Node.js not found, MCP server auto-start disabled")
    mcp_settings.auto_start_default = False
```

## Implementation Guidance

### Phase 1 (M3): Passive Declarations - 2-3 hours

**Step 1: Extend Pydantic Schema (30 minutes)**
```python
# src/llm_service/config/schemas.py

class MCPTools(BaseModel):
    """MCP tool requirements for a tool."""
    required: list[str] = Field(default_factory=list, description="Must be available")
    recommended: list[str] = Field(default_factory=list, description="Enhances capabilities")
    optional: list[str] = Field(default_factory=list, description="Nice-to-have")

class RoleRestrictions(BaseModel):
    """Tool access restrictions by workflow role."""
    allowed_tools: list[str] = Field(description="Tools allowed for this role")

class ToolConfig(BaseModel):
    """Enhanced tool configuration with MCP support."""
    # ... existing fields ...
    mcp_tools: Optional[MCPTools] = None
    role_restrictions: Optional[dict[str, RoleRestrictions]] = None
```

**Step 2: Update Configuration Files (1 hour)**
```yaml
# config/tools.yaml
tools:
  claude-code:
    binary: claude
    command_template: "{binary} {prompt_file} --model {model}"
    models: [claude-3.5-sonnet, claude-3-opus]
    mcp_tools:
      required: [filesystem, git]
      recommended: [code-search]
      optional: [github]
    role_restrictions:
      implementation:
        allowed_tools: [filesystem.write, git.commit]
      review:
        allowed_tools: [filesystem.read, git.log]
```

**Step 3: Add Validation (1 hour)**
```python
# src/llm_service/config/validator.py

def validate_mcp_tool_references(config: ServiceConfig) -> list[ValidationError]:
    """Ensure MCP tools referenced consistently across configs."""
    errors = []
    
    all_mcp_tools = set()
    for tool in config.tools.values():
        if tool.mcp_tools:
            all_mcp_tools.update(tool.mcp_tools.required)
            all_mcp_tools.update(tool.mcp_tools.recommended)
            all_mcp_tools.update(tool.mcp_tools.optional)
    
    # Check role restrictions reference valid MCP tools
    for tool_name, tool in config.tools.items():
        if tool.role_restrictions:
            for role, restrictions in tool.role_restrictions.items():
                for allowed_tool in restrictions.allowed_tools:
                    if "." in allowed_tool:  # MCP tool format: "server.method"
                        server_name = allowed_tool.split(".")[0]
                        if server_name not in all_mcp_tools:
                            errors.append(ValidationError(
                                field=f"tools.{tool_name}.role_restrictions.{role}",
                                message=f"References unknown MCP server: {server_name}"
                            ))
    
    return errors
```

**Step 4: Documentation (30 minutes)**
```markdown
# docs/user-guide/mcp-integration.md

## MCP Server Requirements

Each LLM tool declares its MCP server requirements in three tiers:

- **Required:** Execution fails without these servers
- **Recommended:** Capabilities significantly enhanced
- **Optional:** Nice-to-have features

Check your tool's configuration:
```bash
$ llm-service config validate --show-mcp-requirements
```

Example output:
```
claude-code requires MCP servers:
  ✅ Required: filesystem, git
  ⚠️  Recommended: code-search (install: npm install -g @modelcontextprotocol/server-code-search)
  ℹ️  Optional: github, gitlab
```
```

---

### Phase 2 (M4): Active Management - 10-12 hours

**Step 1: MCP Server Configuration Schema (2 hours)**
```python
# src/llm_service/config/schemas.py

class MCPHealthCheck(BaseModel):
    """Health check configuration for MCP server."""
    method: Literal["ping", "tool_call"] = "ping"
    tool: Optional[str] = None  # Required if method="tool_call"
    args: Optional[dict] = None
    timeout_seconds: int = Field(default=5, ge=1, le=30)

class MCPServerConfig(BaseModel):
    """Configuration for a single MCP server."""
    package: str = Field(description="NPM package name")
    command: str = Field(description="Command to start server")
    auto_start: bool = Field(default=False, description="Start automatically when needed")
    health_check: MCPHealthCheck
    restart_on_failure: bool = Field(default=True)
    max_restart_attempts: int = Field(default=3, ge=1, le=10)

class MCPSettings(BaseModel):
    """Global MCP server settings."""
    auto_start_default: bool = False
    health_check_interval_seconds: int = Field(default=30, ge=10, le=300)
    startup_timeout_seconds: int = Field(default=10, ge=1, le=60)
    shutdown_timeout_seconds: int = Field(default=5, ge=1, le=30)
    log_directory: Path = Field(default=Path("logs/mcp_servers"))

class MCPConfiguration(BaseModel):
    """MCP server configuration file schema."""
    mcp_servers: dict[str, MCPServerConfig]
    mcp_settings: MCPSettings = Field(default_factory=MCPSettings)
```

**Step 2: Server Lifecycle Manager (4 hours)**
```python
# src/llm_service/mcp/server_manager.py

import subprocess
import signal
import psutil
from typing import Optional
from dataclasses import dataclass

@dataclass
class ServerProcess:
    """Running MCP server process."""
    name: str
    process: subprocess.Popen
    pid: int
    started_at: datetime
    last_health_check: Optional[datetime] = None
    health_status: str = "unknown"  # "healthy", "unhealthy", "starting"

class MCPServerManager:
    """Manages MCP server lifecycle."""
    
    def __init__(self, config: MCPConfiguration):
        self.config = config
        self.processes: dict[str, ServerProcess] = {}
        self._health_check_thread = None
    
    def start_server(self, server_name: str) -> ServerProcess:
        """Start an MCP server."""
        if server_name in self.processes:
            logger.info(f"Server {server_name} already running")
            return self.processes[server_name]
        
        server_config = self.config.mcp_servers[server_name]
        logger.info(f"Starting MCP server: {server_name}")
        
        # Parse command (support shell expansion)
        cmd_parts = shlex.split(server_config.command)
        
        # Start subprocess
        process = subprocess.Popen(
            cmd_parts,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line-buffered
        )
        
        server_process = ServerProcess(
            name=server_name,
            process=process,
            pid=process.pid,
            started_at=datetime.now(),
            health_status="starting",
        )
        
        self.processes[server_name] = server_process
        
        # Wait for startup with timeout
        if not self._wait_for_startup(server_process, server_config):
            raise ServerStartupError(f"Server {server_name} failed to start")
        
        logger.info(f"Server {server_name} started successfully (PID {process.pid})")
        return server_process
    
    def stop_server(self, server_name: str, graceful: bool = True) -> None:
        """Stop an MCP server."""
        if server_name not in self.processes:
            logger.warning(f"Server {server_name} not running")
            return
        
        server_process = self.processes[server_name]
        logger.info(f"Stopping MCP server: {server_name} (PID {server_process.pid})")
        
        if graceful:
            # Send SIGTERM, wait for graceful shutdown
            server_process.process.terminate()
            try:
                server_process.process.wait(timeout=self.config.mcp_settings.shutdown_timeout_seconds)
            except subprocess.TimeoutExpired:
                logger.warning(f"Server {server_name} did not stop gracefully, forcing")
                server_process.process.kill()
        else:
            # Force kill
            server_process.process.kill()
        
        del self.processes[server_name]
        logger.info(f"Server {server_name} stopped")
    
    def health_check(self, server_name: str) -> bool:
        """Check if MCP server is healthy."""
        if server_name not in self.processes:
            return False
        
        server_process = self.processes[server_name]
        server_config = self.config.mcp_servers[server_name]
        
        # Check if process still running
        if server_process.process.poll() is not None:
            logger.error(f"Server {server_name} process terminated unexpectedly")
            server_process.health_status = "unhealthy"
            return False
        
        # Execute health check based on method
        health_check = server_config.health_check
        
        if health_check.method == "ping":
            # Simple alive check (process running = healthy)
            server_process.health_status = "healthy"
            server_process.last_health_check = datetime.now()
            return True
        
        elif health_check.method == "tool_call":
            # Call MCP tool and check response
            try:
                result = self._call_mcp_tool(
                    server_process,
                    health_check.tool,
                    health_check.args or {},
                    timeout=health_check.timeout_seconds,
                )
                is_healthy = result.get("status") == "success"
                server_process.health_status = "healthy" if is_healthy else "unhealthy"
                server_process.last_health_check = datetime.now()
                return is_healthy
            except Exception as e:
                logger.error(f"Health check failed for {server_name}: {e}")
                server_process.health_status = "unhealthy"
                return False
        
        return False
    
    def restart_server(self, server_name: str) -> ServerProcess:
        """Restart an MCP server."""
        logger.info(f"Restarting MCP server: {server_name}")
        self.stop_server(server_name, graceful=True)
        return self.start_server(server_name)
    
    def discover_tools(self, server_name: str) -> list[str]:
        """Discover available tools from MCP server."""
        if server_name not in self.processes:
            raise ValueError(f"Server {server_name} not running")
        
        server_process = self.processes[server_name]
        
        # Call MCP list_tools method
        result = self._call_mcp_tool(server_process, "list_tools", {})
        
        tools = result.get("tools", [])
        return [tool["name"] for tool in tools]
    
    def get_capabilities(self, server_name: str) -> dict:
        """Get server capabilities (tools, resources, prompts)."""
        if server_name not in self.processes:
            raise ValueError(f"Server {server_name} not running")
        
        server_process = self.processes[server_name]
        
        # Call MCP capabilities method
        capabilities = self._call_mcp_tool(server_process, "get_capabilities", {})
        
        return capabilities
    
    def _wait_for_startup(self, server_process: ServerProcess, server_config: MCPServerConfig) -> bool:
        """Wait for server to be ready."""
        timeout = self.config.mcp_settings.startup_timeout_seconds
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if server_process.process.poll() is not None:
                # Process terminated during startup
                return False
            
            # Try health check
            try:
                if self.health_check(server_process.name):
                    return True
            except Exception:
                pass
            
            time.sleep(0.5)
        
        return False
    
    def _call_mcp_tool(self, server_process: ServerProcess, tool: str, args: dict, timeout: int = 5) -> dict:
        """Call an MCP tool via JSON-RPC."""
        # Construct JSON-RPC request
        request = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": tool,
            "params": args,
        }
        
        # Send to server stdin
        server_process.process.stdin.write(json.dumps(request) + "\n")
        server_process.process.stdin.flush()
        
        # Read response from stdout (with timeout)
        response_line = self._read_line_with_timeout(server_process.process.stdout, timeout)
        response = json.loads(response_line)
        
        if "error" in response:
            raise MCPToolError(response["error"])
        
        return response.get("result", {})
    
    def _read_line_with_timeout(self, stream, timeout: int) -> str:
        """Read a line from stream with timeout."""
        import select
        ready, _, _ = select.select([stream], [], [], timeout)
        if ready:
            return stream.readline()
        else:
            raise TimeoutError("MCP tool call timed out")
```

**Step 3: Dashboard Integration (2-3 hours)**
```python
# src/llm_service/dashboard/mcp_status.py

class MCPStatusView:
    """Dashboard view for MCP server status."""
    
    def render(self, mcp_manager: MCPServerManager) -> dict:
        """Render MCP server status for dashboard."""
        servers = []
        
        for server_name, config in mcp_manager.config.mcp_servers.items():
            if server_name in mcp_manager.processes:
                process = mcp_manager.processes[server_name]
                status = {
                    "name": server_name,
                    "state": "running",
                    "health": process.health_status,
                    "pid": process.pid,
                    "uptime_seconds": (datetime.now() - process.started_at).total_seconds(),
                    "tools_count": len(mcp_manager.discover_tools(server_name)),
                }
            else:
                status = {
                    "name": server_name,
                    "state": "stopped",
                    "health": "n/a",
                    "auto_start": config.auto_start,
                }
            
            servers.append(status)
        
        return {
            "servers": servers,
            "total_running": sum(1 for s in servers if s["state"] == "running"),
            "total_healthy": sum(1 for s in servers if s.get("health") == "healthy"),
        }
```

**Step 4: CLI Commands (2 hours)**
```python
# src/llm_service/cli/mcp.py

@click.group()
def mcp():
    """Manage MCP servers."""
    pass

@mcp.command()
def status():
    """Show MCP server status."""
    manager = get_mcp_manager()
    
    table = Table(title="MCP Server Status")
    table.add_column("Server", style="cyan")
    table.add_column("State", style="magenta")
    table.add_column("Health", style="green")
    table.add_column("Tools", style="yellow")
    
    for server_name, config in manager.config.mcp_servers.items():
        if server_name in manager.processes:
            process = manager.processes[server_name]
            state = "🟢 Running"
            health = "✅" if process.health_status == "healthy" else "❌"
            tools = str(len(manager.discover_tools(server_name)))
        else:
            state = "⚫ Stopped"
            health = "-"
            tools = "-"
        
        table.add_row(server_name, state, health, tools)
    
    console.print(table)

@mcp.command()
@click.argument("server_name")
def start(server_name: str):
    """Start an MCP server."""
    manager = get_mcp_manager()
    
    with StepTracker(f"Starting {server_name}") as tracker:
        tracker.step("Validating configuration")
        if server_name not in manager.config.mcp_servers:
            tracker.error("validate", f"Server {server_name} not configured")
            raise click.ClickException(f"Unknown server: {server_name}")
        tracker.complete()
        
        tracker.step("Starting server process")
        try:
            process = manager.start_server(server_name)
            tracker.complete(f"PID {process.pid}")
        except ServerStartupError as e:
            tracker.error("start", str(e))
            raise
        
        tracker.step("Health check")
        if manager.health_check(server_name):
            tracker.complete("Server healthy")
        else:
            tracker.error("health", "Health check failed")

@mcp.command()
@click.argument("server_name")
def stop(server_name: str):
    """Stop an MCP server."""
    manager = get_mcp_manager()
    manager.stop_server(server_name)
    console.print(f"[green]✓[/green] Server {server_name} stopped")

@mcp.command()
@click.argument("server_name")
def discover(server_name: str):
    """Discover tools from MCP server."""
    manager = get_mcp_manager()
    
    if server_name not in manager.processes:
        console.print(f"[red]✗[/red] Server {server_name} not running")
        console.print(f"Start with: llm-service mcp start {server_name}")
        return
    
    tools = manager.discover_tools(server_name)
    
    console.print(Panel.fit(
        f"[bold cyan]{len(tools)} tools[/bold cyan] discovered from {server_name}",
        border_style="cyan"
    ))
    
    for tool in sorted(tools):
        console.print(f"  • {tool}")
```

**Step 5: Integration Tests (2 hours)**
```python
# tests/integration/test_mcp_integration.py

def test_mcp_server_lifecycle():
    """Test MCP server start/stop/health lifecycle."""
    config = MCPConfiguration(
        mcp_servers={
            "test-server": MCPServerConfig(
                package="@test/server",
                command="node test-server.js",
                auto_start=False,
                health_check=MCPHealthCheck(method="ping"),
            )
        }
    )
    
    manager = MCPServerManager(config)
    
    # Start server
    process = manager.start_server("test-server")
    assert process.name == "test-server"
    assert process.pid > 0
    
    # Health check
    assert manager.health_check("test-server") is True
    
    # Discover tools
    tools = manager.discover_tools("test-server")
    assert len(tools) > 0
    
    # Stop server
    manager.stop_server("test-server")
    assert "test-server" not in manager.processes

def test_mcp_server_restart_on_failure():
    """Test automatic restart on health check failure."""
    # ... test implementation ...

def test_mcp_tool_restrictions_by_role():
    """Test role-based tool access restrictions."""
    # ... test implementation ...
```

## Considered Alternatives

### Alternative 1: Direct MCP API Integration (No Subprocess)

**Description:** Integrate MCP protocol directly into LLM Service Layer using Python MCP client library.

**Pros:**
- ✅ No subprocess management complexity
- ✅ Tighter integration
- ✅ Better error handling

**Cons:**
- ❌ Couples LLM Service to MCP protocol version
- ❌ Limits language choice for MCP servers
- ❌ Harder to integrate pre-existing MCP servers
- ❌ Less flexible for future protocol changes

**Rejected Because:** Subprocess isolation provides better flexibility and aligns with industry patterns (kitty-cli, Claude Code, etc.).

---

### Alternative 2: Single-Phase Implementation (All M3)

**Description:** Implement passive declarations AND active management in M3.

**Pros:**
- ✅ Faster time to full feature set
- ✅ No need for two-phase migration

**Cons:**
- ❌ M3 timeline already constrained
- ❌ High risk of delaying M3 milestone
- ❌ No iteration opportunity based on M3 feedback
- ❌ Combines low-risk (passive) with high-risk (active) features

**Rejected Because:** Phased approach reduces risk and allows iteration. M3 timeline constrained by CLI UX priorities.

---

### Alternative 3: Database-Backed Server Registry

**Description:** Store MCP server configurations and state in SQLite database instead of YAML files.

**Pros:**
- ✅ Structured queries for server state
- ✅ Historical tracking of server health
- ✅ Better concurrency support

**Cons:**
- ❌ Adds database complexity
- ❌ YAML config files still needed for declarations
- ❌ Migration complexity for schema changes
- ❌ Harder to debug (no human-readable config)

**Rejected Because:** YAML files align with our file-based orchestration philosophy (ADR-008). SQLite adds unnecessary complexity for server management.

---

### Alternative 4: No Role-Based Restrictions

**Description:** Allow all MCP tools for all workflow phases without restrictions.

**Pros:**
- ✅ Simpler configuration
- ✅ More flexible for users

**Cons:**
- ❌ Security risk (review agents could modify code)
- ❌ No safety guardrails for destructive operations
- ❌ Doesn't align with kitty-cli best practices

**Rejected Because:** Role-based restrictions provide important security boundaries and intent clarity.

## References

**Related ADRs:**
- [ADR-025: LLM Service Layer](ADR-025-llm-service-layer.md) - Strategic vision
- [ADR-029: Adapter Interface Design](ADR-029-adapter-interface-design.md) - Tool adapters
- [ADR-030: Rich Terminal UI](ADR-030-rich-terminal-ui-cli-feedback.md) - CLI feedback
- [ADR-032: Real-Time Dashboard](ADR-032-real-time-execution-dashboard.md) - Dashboard UI
- [ADR-033: Step Tracker Pattern](ADR-033-step-tracker-pattern.md) - Progress tracking

**Related Documents:**
- [Architecture Impact Analysis](../../../work/reports/architecture/2026-02-05-kitty-cli-architecture-impact-analysis.md)
- [kitty-cli Research Findings](../../../work/reports/research/RESEARCH_SUMMARY.md)
- [MCP Integration Technical Design](../../design/mcp-integration-technical-design.md) (to be created)

**External References:**
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Anthropic MCP Documentation](https://docs.anthropic.com/model-context-protocol)
- [kitty-cli MCP Implementation](https://github.com/Priivacy-ai/spec-kitty) - Reference implementation

---

**Status:** ✅ Accepted  
**Implementation Target:** M3 (Passive - 2-3 hours), M4 (Active - 10-12 hours)  
**Dependencies:** ADR-030 (Rich UI), ADR-033 (Step Tracker), ADR-032 (Dashboard)
