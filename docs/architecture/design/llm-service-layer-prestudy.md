# Technical Design: LLM Service Layer for Agent-Tool Orchestration

**Version:** 0.2.0 (Approved Prestudy)  
**Status:** Approved - Ready for Implementation  
**Author:** Architect Alphonso  
**Date:** 2026-02-04  
**Approved By:** Human-in-Charge (2026-02-04)  
**Target Audience:** Process Architects, Software Engineers, AI Power Users

---

## Context

The current agent-augmented development framework provides agent profiles, directives, and orchestration patterns that enable structured multi-agent workflows. However, agent-to-LLM-stack mapping and model selection are currently implicit and manual. Each agent interaction requires the human operator to:

1. Select the appropriate LLM tool (Claude, Cursor, Codex, Gemini CLI, etc.)
2. Choose the right model tier for the task complexity
3. Manually invoke CLI commands with correct parameters
4. Context-switch between different tools and interfaces

This creates friction in the workflow, increases cognitive load, and prevents optimization of token costs through automatic model-task matching.

### Problem Statement

**Goal:** Enhance user experience, discoverability, and overall system capability by adding a service layer that delegates execution to user-defined LLM stacks via CLI calls.

**Key Requirements:**

- Agent-to-tool mapping (e.g., "planner uses Codex+GPT-5.2, backend-dev uses Claude-code+Haiku")
- Task-to-model mapping (simple requests → cheaper models, complex tasks → premium models)
- Local machine usage only with CLI-based interaction
- Cross-OS portability via Linux layers (WSL2 on Windows, native on Linux/macOS)
- Minimal implementation focus (KISS principle)
- Future-ready but not designed for remote API service deployment

### Current State

The framework provides:

- Agent profiles defining specializations (`.github/agents/*.agent.md`)
- Task orchestration via file-based YAML workflow (`work/collaboration/`)
- Directive system for agent behavior and guidelines
- Multiple human personas (AI Power User, Software Engineer, Process Architect)

What is missing:

- Unified interface for agent-LLM interaction
- Configuration-driven tool/model selection
- Token cost tracking and optimization
- Task complexity classification
- Swarm-mode coordination (multi-agent, multi-model task execution)

---

## Acceptance Criteria

This is an **architectural prestudy**, not an implementation specification. The document must:

- ✅ Define generic components and their interactions (not implementation details)
- ✅ Provide at least 3 usage scenarios using known personas
- ✅ Analyze impact on usability and token cost
- ✅ Recommend minimal tech stack options
- ✅ Assume cross-OS portability via Linux layers
- ✅ Focus on local CLI-based usage (no remote service design)
- ✅ Delegate diagram creation to diagrammer specialist
- ✅ Provide suggested acceptance tests in pseudo-code (ATDD adherence per Directive 016)
- ❌ Make final architectural decisions (human approval required)

---

## Suggested Acceptance Tests (Directive 016 Compliance)

The following acceptance tests define externally observable behavior that validates the service layer design. These are written in pseudo-code/BDD format and should be implemented as executable tests during Phase 1.

### AT-1: Agent-to-Tool Routing

**Scenario:** Route agent request to configured tool

```gherkin
Feature: Agent-to-Tool Routing
  As a user
  I want the service to automatically select the correct LLM tool for each agent
  So that I don't need to manually choose tools

  Scenario: Architect agent routes to Cursor
    Given the configuration file "config/agents.yaml" contains:
      """
      agents:
        architect:
          preferred_tool: cursor
          preferred_model: gpt-4-turbo
      """
    And the tool "cursor" is installed and available in PATH
    When I execute "llm-service exec --agent=architect --prompt=test.md"
    Then the service should invoke "cursor --prompt-file test.md --model gpt-4-turbo"
    And the response should be returned to stdout
    And the exit code should be 0

  Scenario: Backend-dev agent routes to Claude
    Given the configuration file "config/agents.yaml" contains:
      """
      agents:
        backend-dev:
          preferred_tool: claude
          preferred_model: claude-sonnet-20240229
      """
    And the tool "claude" is installed and available
    When I execute "llm-service exec --agent=backend-dev --prompt=code.md"
    Then the service should invoke "claude /code-review code.md --model claude-sonnet-20240229"
    And the response should be returned to stdout
    And the exit code should be 0
```

### AT-2: Task-Based Model Selection

**Scenario:** Select cheaper model for simple tasks

```gherkin
Feature: Task-Based Model Selection
  As a cost-conscious user
  I want simple tasks to use cheaper models automatically
  So that I minimize token costs

  Scenario: Simple task uses cheaper model
    Given the configuration file "config/policies.yaml" contains:
      """
      policies:
        cost_optimization:
          simple_task_threshold_tokens: 1500
          simple_task_models: [claude-haiku-20240307]
      """
    And the prompt file "simple.md" contains 800 tokens
    And agent "backend-dev" prefers "claude-sonnet-20240229"
    When I execute "llm-service exec --agent=backend-dev --prompt=simple.md"
    Then the service should detect prompt is under 1500 tokens
    And the service should override to use "claude-haiku-20240307"
    And the telemetry log should record model="claude-haiku-20240307"
    And the telemetry log should record reason="cost_optimization"

  Scenario: Complex task uses premium model
    Given the same configuration as above
    And the prompt file "complex.md" contains 3000 tokens
    When I execute "llm-service exec --agent=backend-dev --prompt=complex.md"
    Then the service should use preferred model "claude-sonnet-20240229"
    And the telemetry log should record reason="above_threshold"
```

### AT-3: Fallback Chain Activation

**Scenario:** Use fallback when primary tool unavailable

```gherkin
Feature: Fallback Chain
  As a user
  I want the service to try alternative tools when the primary tool fails
  So that I can continue working despite tool unavailability

  Scenario: Primary tool unavailable, fallback succeeds
    Given the configuration file "config/agents.yaml" contains:
      """
      agents:
        architect:
          preferred_tool: cursor
          fallback_chain:
            - cursor:gpt-4-turbo
            - claude:claude-opus-20240229
            - gemini:gemini-pro-vision
      """
    And the tool "cursor" is not available in PATH
    And the tool "claude" is available
    When I execute "llm-service exec --agent=architect --prompt=design.md"
    Then the service should attempt "cursor" and fail
    And the service should warn "Primary tool cursor unavailable, trying fallback"
    And the service should invoke "claude" with "claude-opus-20240229"
    And the response should be returned to stdout
    And the exit code should be 0
    And the telemetry log should record tool="claude", reason="fallback"

  Scenario: All tools in fallback chain unavailable
    Given the same configuration as above
    And no tools in the fallback chain are available
    When I execute "llm-service exec --agent=architect --prompt=design.md"
    Then the service should attempt all tools in fallback chain
    And the service should return error "No available tools in fallback chain"
    And the exit code should be 1
```

### AT-4: Configuration Validation

**Scenario:** Validate configuration on startup

```gherkin
Feature: Configuration Validation
  As a user
  I want the service to validate configuration files on startup
  So that I catch errors before executing tasks

  Scenario: Valid configuration passes validation
    Given valid configuration files exist in "~/.config/llm-service/"
    When I execute "llm-service config validate"
    Then the service should parse all YAML files successfully
    And the service should check for required fields
    And the service should verify tool references are consistent
    And the output should be "✅ Configuration valid"
    And the exit code should be 0

  Scenario: Invalid agent configuration detected
    Given "config/agents.yaml" references unknown tool "nonexistent-tool"
    When I execute "llm-service config validate"
    Then the service should detect the invalid tool reference
    And the output should contain "❌ Error in config/agents.yaml: Unknown tool 'nonexistent-tool'"
    And the output should suggest valid tools from "config/tools.yaml"
    And the exit code should be 1

  Scenario: Missing required configuration file
    Given "config/agents.yaml" does not exist
    When I execute "llm-service config validate"
    Then the service should detect missing file
    And the output should contain "❌ Missing required file: config/agents.yaml"
    And the output should suggest "Run 'llm-service init' to create default configuration"
    And the exit code should be 1
```

### AT-5: Telemetry and Cost Tracking

**Scenario:** Track token usage and costs

```gherkin
Feature: Telemetry and Cost Tracking
  As a user
  I want to track token usage and costs over time
  So that I can optimize my LLM spending

  Scenario: Invocation logged to telemetry database
    Given the service is configured with telemetry enabled
    When I execute "llm-service exec --agent=architect --prompt=design.md"
    And the LLM tool returns response with 1500 input tokens and 800 output tokens
    Then the service should insert a record into telemetry database with:
      | field          | value                  |
      | timestamp      | 2026-02-04T07:30:00Z   |
      | agent          | architect              |
      | tool           | cursor                 |
      | model          | gpt-4-turbo            |
      | input_tokens   | 1500                   |
      | output_tokens  | 800                    |
      | total_tokens   | 2300                   |
      | cost_usd       | 0.039                  |
      | latency_ms     | 2340                   |
      | status         | success                |

  Scenario: Daily cost report
    Given the telemetry database contains 50 invocations from today
    And the total cost for today is $3.45
    When I execute "llm-service stats --daily"
    Then the output should contain:
      """
      Daily Usage Report (2026-02-04):
      - Total invocations: 50
      - Total tokens: 125,000
      - Total cost: $3.45
      - Average cost per invocation: $0.069
      
      By Agent:
      - architect: 20 invocations, $1.80
      - backend-dev: 25 invocations, $1.20
      - scribe: 5 invocations, $0.45
      
      By Model:
      - gpt-4-turbo: $2.00 (58%)
      - claude-sonnet: $1.00 (29%)
      - claude-haiku: $0.45 (13%)
      """
    And the exit code should be 0
```

### AT-6: Budget Enforcement

**Scenario:** Warn when approaching budget limit

```gherkin
Feature: Budget Enforcement
  As a process architect
  I want the service to warn when approaching budget limits
  So that I can prevent unexpected costs

  Scenario: Warn at 80% of daily budget
    Given the configuration file "config/policies.yaml" contains:
      """
      policies:
        default:
          daily_budget_usd: 10.00
          alert_threshold_percent: 80
      """
    And the current daily spending is $8.10 (81% of budget)
    When I execute "llm-service exec --agent=architect --prompt=design.md"
    Then the service should display warning before execution:
      """
      ⚠️  Budget Warning: Daily spending at 81% of limit ($8.10 / $10.00)
      Estimated cost for this request: ~$0.50
      Proceed? [y/N]
      """
    And the service should wait for user confirmation
    When the user enters "y"
    Then the service should proceed with execution

  Scenario: Optional hard limit enforcement
    Given the policy contains "block_over_budget: true"
    And the current daily spending is $9.80
    And the estimated cost for the request is $0.50 (would exceed $10.00)
    When I execute "llm-service exec --agent=architect --prompt=design.md"
    Then the service should block execution with error:
      """
      ❌ Budget Exceeded: Request would exceed daily budget ($10.30 / $10.00)
      Options:
      1. Increase daily_budget_usd in config/policies.yaml
      2. Use --force flag to override (requires justification)
      3. Wait until tomorrow (budget resets at midnight UTC)
      """
    And the exit code should be 1
```

### AT-7: Cross-Platform Compatibility

**Scenario:** Service works on multiple operating systems

```gherkin
Feature: Cross-Platform Compatibility
  As a user on different operating systems
  I want the service to work consistently
  So that I can use the same configuration across machines

  Scenario Outline: Service executes on different platforms
    Given I am running on <platform>
    And the service is installed in <install_path>
    And configuration files are in <config_path>
    When I execute "llm-service exec --agent=architect --prompt=test.md"
    Then the service should detect platform as <platform>
    And the service should use configuration from <config_path>
    And the service should locate tools using platform-specific paths
    And the response should be returned successfully

    Examples:
      | platform     | install_path                    | config_path                          |
      | Linux        | /usr/local/bin/llm-service      | ~/.config/llm-service/               |
      | macOS        | /usr/local/bin/llm-service      | ~/.config/llm-service/               |
      | Windows/WSL2 | /usr/local/bin/llm-service      | ~/.config/llm-service/               |

  Scenario: Tool path detection on Windows
    Given I am running on Windows with WSL2
    And the tool "cursor" is installed at "C:\Users\user\AppData\Local\Programs\cursor\cursor.exe"
    And "config/tools.yaml" contains Windows-specific path
    When I execute "llm-service exec --agent=architect --prompt=test.md"
    Then the service should translate WSL2 path to Windows path
    And the service should invoke tool successfully
```

### AT-8: Context Chaining for Multi-Agent Workflows

**Scenario:** Chain outputs between agents

```gherkin
Feature: Context Chaining
  As a software engineer
  I want to chain outputs from one agent to the next
  So that I can automate multi-step workflows

  Scenario: Three-agent pipeline with context passing
    Given I have a workflow script "orchestrate.sh":
      """
      llm-service exec --agent=architect --prompt=analyze.md --output=analysis.txt
      llm-service exec --agent=backend-dev --prompt=implement.md --context=analysis.txt --output=code.py
      llm-service exec --agent=scribe --prompt=document.md --context=code.py --output=README.md
      """
    When I execute "bash orchestrate.sh"
    Then the service should:
      1. Execute architect task, save output to "analysis.txt"
      2. Execute backend-dev task, include "analysis.txt" as context
      3. Execute scribe task, include "code.py" as context
    And all three files should exist: "analysis.txt", "code.py", "README.md"
    And the telemetry should record 3 linked invocations
    And the exit code should be 0
```

### Test Execution Strategy

**Phase 1 (MVP):**
- Implement AT-1 (Agent-to-Tool Routing) - Core functionality
- Implement AT-4 (Configuration Validation) - Fail-fast on setup errors

**Phase 2 (Cost Optimization):**
- Implement AT-2 (Task-Based Model Selection) - Cost savings
- Implement AT-5 (Telemetry and Cost Tracking) - Observability

**Phase 3 (Robustness):**
- Implement AT-3 (Fallback Chain Activation) - Reliability
- Implement AT-6 (Budget Enforcement) - Cost control
- Implement AT-7 (Cross-Platform Compatibility) - Portability

**Phase 4 (Advanced Features):**
- Implement AT-8 (Context Chaining) - Multi-agent orchestration

**Testing Tools:**
- **BDD Framework:** Use behave (Python) or godog (Go) for Gherkin execution
- **Mocking:** Mock LLM tool CLIs using test doubles (avoid real API calls in CI)
- **CI/CD:** GitHub Actions matrix testing (Linux, macOS, Windows/WSL2)
- **Coverage Target:** 80%+ for core routing and configuration logic

---

## Design

### Overview

The **LLM Service Layer** acts as an intelligent routing and orchestration middleware between agents and LLM stacks. It interprets agent requests, selects appropriate tools and models based on configuration and task characteristics, executes CLI commands, and returns results.

**Core Responsibilities:**

1. **Configuration Management:** Load and validate agent-tool mappings, model preferences, and cost policies
2. **Request Routing:** Match agent identity and task type to appropriate LLM stack
3. **CLI Execution:** Invoke external tools (cursor, claude, codex, gemini-cli) with correct parameters
4. **Response Handling:** Normalize outputs across different CLI tools
5. **Telemetry:** Track token usage, cost, and performance metrics
6. **Error Recovery:** Fallback strategies when preferred tools are unavailable

**Key Design Principles:**

- **Simplicity First:** Start with configuration files and shell invocation, not complex RPC
- **Declarative Configuration:** YAML/TOML for agent-tool mappings, avoid hardcoded logic
- **Tool Agnostic:** Plugin architecture allows adding new LLM CLIs without core changes
- **Observable:** Every invocation logged for cost tracking and debugging
- **Fail-Safe:** Graceful degradation when tools are unavailable or rate-limited

### Architecture Components

#### 1. Configuration Layer

**Purpose:** Define agent-tool mappings, model selection policies, and cost constraints.

**Components:**

- **Agent Registry (`config/agents.yaml`):** Maps agent names to tool preferences and model tiers
- **Tool Definitions (`config/tools.yaml`):** Defines available LLM CLIs, invocation patterns, and capabilities
- **Model Catalog (`config/models.yaml`):** Lists models, token costs, rate limits, and task suitability
- **Policy Rules (`config/policies.yaml`):** Cost budgets, fallback chains, and usage quotas

**Key Decisions:**

- Use YAML for human-readability and Git-friendliness (track configuration changes over time)
- Separate concerns: agent preferences vs tool capabilities vs cost policies
- Support environment variable overrides for local customization (e.g., `AGENT_TOOL_OVERRIDE`)

#### 2. Service Core

**Purpose:** Route requests and orchestrate LLM invocations based on configuration.

**Components:**

- **Request Parser:** Extracts agent identity, task type, and prompt content from input
- **Routing Engine:** Applies configuration policies to select tool and model
- **Execution Manager:** Builds CLI commands, invokes subprocesses, captures output
- **Response Normalizer:** Transforms tool-specific outputs into common format

**Key Decisions:**

- Keep core logic in a single-process Python/Node.js/Go application (no microservices yet)
- Use adapter pattern for tool-specific CLI invocations (easy to add new tools)
- Implement synchronous execution initially (async/parallel invocation in future enhancement)

#### 3. CLI Interface

**Purpose:** Provide human-friendly command-line interface for invoking the service.

**Components:**

- **Interactive Mode:** Prompt-based interface for ad-hoc queries (e.g., `llm-service chat`)
- **Direct Invocation:** Pass prompt files and agent context (e.g., `llm-service exec --agent=architect --prompt=file.md`)
- **Configuration Commands:** Inspect and validate configuration (e.g., `llm-service config validate`)
- **Telemetry Query:** View cost and usage reports (e.g., `llm-service stats --agent=backend-dev`)

**Key Decisions:**

- CLI-first design aligns with current workflow (agents invoke shell commands)
- Support both stdin and file-based prompt input (flexibility for different workflows)
- Colorized output with structured logging (JSON mode for machine parsing)

#### 4. Tool Adapters

**Purpose:** Abstract differences between LLM CLI tools into common interface.

**Components:**

- **Cursor Adapter:** Invokes `cursor` CLI with project context and prompt
- **Claude Adapter:** Invokes `claude` CLI (or API wrapper) with system/user messages
- **Codex Adapter:** Invokes OpenAI Codex CLI with code-specific context
- **Gemini Adapter:** Invokes `gemini-cli` with structured input

**Key Decisions:**

- Each adapter implements common interface: `execute(prompt, context, model, options) -> response`
- Adapters responsible for tool-specific error handling and retry logic
- Adapters emit telemetry (tokens, cost, latency) in standardized format

#### 5. Telemetry & Logging

**Purpose:** Track usage, cost, and performance for optimization and debugging.

**Components:**

- **Invocation Log:** Record every LLM request with agent, task type, model, and prompt hash
- **Cost Tracker:** Accumulate token usage and estimated costs per agent/project/day
- **Performance Monitor:** Track latency and error rates per tool/model
- **Audit Trail:** Compliance-friendly log of all AI-assisted decisions (optional)

**Key Decisions:**

- Store telemetry in local SQLite database (simple, portable, queryable)
- Support CSV/JSON export for analysis in external tools (Excel, notebooks)
- Privacy-aware: log metadata and prompt hashes, not full prompt content (configurable)

---

### Implementation Considerations

#### Technology Stack Recommendations

**Option A: Python-based Service** (Recommended for rapid prototyping)

- **Core:** Python 3.10+ with Click for CLI, PyYAML for configuration
- **Execution:** `subprocess.run()` for tool invocation
- **Telemetry:** SQLite via `sqlite3` standard library
- **Testing:** pytest with fixtures for tool mocking
- **Distribution:** Single-file executable via PyInstaller or Nuitka

**Rationale:** Python is ubiquitous, agent-friendly, and fast to iterate. Rich ecosystem for CLI tools.

**Option B: Go-based Service** (Recommended for production hardening)

- **Core:** Go 1.21+ with Cobra for CLI, Viper for configuration
- **Execution:** `os/exec` package for subprocesses
- **Telemetry:** SQLite via `mattn/go-sqlite3`
- **Testing:** `testing` package with mocks
- **Distribution:** Single static binary (no runtime dependencies)

**Rationale:** Go binaries are portable, fast, and easy to distribute. Strong concurrency primitives for future enhancements.

**Option C: Node.js-based Service** (Alternative for JavaScript-centric teams)

- **Core:** Node.js 18+ with Commander.js, YAML parser
- **Execution:** `child_process.spawn()` for tools
- **Telemetry:** SQLite via `better-sqlite3`
- **Testing:** Jest with mocks
- **Distribution:** `pkg` or Bun for standalone executable

**Rationale:** Familiar for web developers, good ecosystem, but less suited for system-level tooling.

**Recommended Choice:** **Python** for initial prototype, **Go** for hardened v1.0 release.

---

#### Cross-OS Portability Strategy

**Target Environments:**

- **Linux:** Native support (Ubuntu 20.04+, Fedora 38+, Arch)
- **macOS:** Native support (macOS 12+ Monterey)
- **Windows:** WSL2 required (Ubuntu 20.04+ image)

**Portability Tactics:**

1. **Path Handling:** Use `pathlib` (Python) or `filepath` (Go) for cross-platform paths
2. **Shell Invocation:** Prefer direct binary execution over shell scripts (avoid bash-isms)
3. **Environment Detection:** Auto-detect OS and adjust tool paths (e.g., `cursor.exe` vs `cursor`)
4. **Configuration Paths:** Use XDG Base Directory spec on Linux/macOS, AppData on Windows
5. **Testing Matrix:** CI/CD runs on Linux, macOS, WSL2 (GitHub Actions matrix)

**Assumptions:**

- Linux layer available on Windows (WSL2 installed and configured)
- LLM CLI tools installed in PATH or configured in `config/tools.yaml`
- Standard POSIX utilities available (sh, cat, grep for scripting)

---

#### Configuration Schema Design

**Agent Registry Example (`config/agents.yaml`):**

```yaml
agents:
  architect:
    preferred_tool: cursor
    preferred_model: gpt-4-turbo
    fallback_chain:
      - cursor:gpt-4-turbo
      - claude:claude-opus-20240229
      - gemini:gemini-pro-vision
    task_types:
      analysis: gpt-4-turbo
      synthesis: claude-opus-20240229
      diagramming: gemini-pro-vision

  backend-dev:
    preferred_tool: claude
    preferred_model: claude-sonnet-20240229
    fallback_chain:
      - claude:claude-sonnet-20240229
      - cursor:gpt-4
      - codex:code-davinci-002
    task_types:
      coding: claude-sonnet-20240229
      debugging: gpt-4
      refactoring: claude-haiku-20240307

  planner:
    preferred_tool: codex
    preferred_model: gpt-5.2-preview
    fallback_chain:
      - codex:gpt-5.2-preview
      - cursor:gpt-4-turbo
      - claude:claude-opus-20240229
```

**Tool Definitions Example (`config/tools.yaml`):**

```yaml
tools:
  cursor:
    binary: cursor
    platforms:
      linux: /usr/local/bin/cursor
      macos: /Applications/Cursor.app/Contents/MacOS/cursor
      windows: C:\Users\{USER}\AppData\Local\Programs\cursor\cursor.exe
    invoke_pattern: "{binary} --prompt-file {prompt_file} --model {model}"
    models:
      - gpt-4-turbo
      - gpt-4
      - gpt-3.5-turbo
    capabilities:
      - code_generation
      - code_editing
      - project_context

  claude:
    binary: claude
    invoke_pattern: "{binary} /code-review {prompt_file} --model {model}"
    models:
      - claude-opus-20240229
      - claude-sonnet-20240229
      - claude-haiku-20240307
    capabilities:
      - long_context
      - function_calling
      - vision
```

**Model Catalog Example (`config/models.yaml`):**

```yaml
models:
  gpt-4-turbo:
    provider: openai
    cost_per_1k_tokens:
      input: 0.01
      output: 0.03
    context_window: 128000
    task_suitability:
      - architecture
      - complex_reasoning
      - code_review

  claude-sonnet-20240229:
    provider: anthropic
    cost_per_1k_tokens:
      input: 0.003
      output: 0.015
    context_window: 200000
    task_suitability:
      - coding
      - long_documents
      - editing

  claude-haiku-20240307:
    provider: anthropic
    cost_per_1k_tokens:
      input: 0.00025
      output: 0.00125
    context_window: 200000
    task_suitability:
      - simple_queries
      - fast_responses
      - high_volume
```

**Policy Rules Example (`config/policies.yaml`):**

```yaml
policies:
  default:
    daily_budget_usd: 10.00
    prefer_cheaper_models_under_tokens: 2000
    auto_fallback_on_rate_limit: true
    log_prompts: false
    log_metadata: true

  cost_optimization:
    simple_task_threshold_tokens: 1000
    simple_task_models:
      - claude-haiku-20240307
      - gpt-3.5-turbo
    complex_task_models:
      - gpt-4-turbo
      - claude-opus-20240229

  rate_limiting:
    max_requests_per_minute:
      cursor: 20
      claude: 50
      codex: 10
      gemini: 30
```

---

#### Request Flow Sequence

1. **Agent Invocation:** Agent (or human) invokes `llm-service exec --agent=architect --task=analysis --prompt=design.md`
2. **Request Parsing:** Service reads agent identity, task type, and prompt content
3. **Configuration Lookup:** Load `config/agents.yaml` to find preferred tool/model for architect+analysis
4. **Policy Application:** Check `config/policies.yaml` to determine if cheaper model can be used (token count < threshold)
5. **Tool Selection:** Choose tool from fallback chain (check availability and rate limits)
6. **CLI Invocation:** Build command string, execute subprocess, capture stdout/stderr
7. **Response Normalization:** Parse tool output, extract relevant data, format consistently
8. **Telemetry Recording:** Log invocation metadata to SQLite (timestamp, agent, task, model, tokens, cost, latency)
9. **Result Return:** Output response to stdout (or file if `--output` specified)

---

### Cross-cutting Concerns

#### Security

**Threat Model:**

- **Prompt Injection:** Malicious input in prompt files could execute arbitrary commands if not sanitized
- **Credential Leakage:** API keys for LLM tools must be secured (not in Git)
- **Output Integrity:** LLM responses could contain malicious code/scripts

**Mitigations:**

- **Input Sanitization:** Validate prompt file paths, reject absolute paths outside allowed directories
- **Credential Management:** Use environment variables or OS keychain (not config files)
- **Subprocess Isolation:** Use `subprocess` with `shell=False` to prevent shell injection
- **Output Filtering:** Optional sandboxing of generated code (future enhancement)
- **Audit Logging:** Track all invocations for compliance and security review

#### Performance

**Latency Requirements:**

- **Interactive Mode:** < 500ms overhead (tool invocation time dominates)
- **Batch Mode:** Support parallel invocation of multiple prompts (future)
- **Configuration Loading:** < 100ms startup time (cache parsed YAML in memory)

**Scalability Considerations:**

- **Single Process:** Sufficient for local usage (1-10 concurrent requests)
- **SQLite Database:** Handles 100k+ invocation records without performance issues
- **Future Enhancements:** Consider worker pool for parallel tool invocation

#### Deployment

**Installation Steps:**

1. Download single binary (`llm-service` executable) from GitHub Releases
2. Place in PATH (e.g., `/usr/local/bin` on Linux/macOS, `C:\Tools` on Windows)
3. Run `llm-service init` to create default configuration in `~/.config/llm-service/`
4. Edit `config/agents.yaml` to map agents to preferred tools
5. Edit `config/tools.yaml` to set correct binary paths for installed LLM CLIs
6. Run `llm-service config validate` to check configuration
7. Test with `llm-service exec --agent=test --prompt=hello.md`

**Configuration Management:**

- **User Config:** `~/.config/llm-service/` (XDG standard)
- **Project Config:** `.llm-service/` in repository root (overrides user config)
- **Environment Overrides:** `LLM_SERVICE_CONFIG_DIR` for custom paths

**Updates:**

- **Binary Replacement:** Download new version, replace executable
- **Configuration Migration:** `llm-service config migrate` for schema changes
- **Backward Compatibility:** Support old config formats for 2 major versions

#### Auditing and Logging

**Log Levels:**

- **ERROR:** Tool invocation failures, configuration errors
- **WARN:** Fallback activations, rate limit warnings, cost threshold exceeded
- **INFO:** Successful invocations, configuration changes
- **DEBUG:** Full CLI commands, subprocess output, timing details

**Log Destinations:**

- **Console:** Colorized output for interactive use
- **File:** Structured JSON logs in `~/.local/share/llm-service/logs/`
- **Telemetry DB:** SQLite database for queryable history

**Privacy Controls:**

- **Minimal Logging (default):** Log metadata only (agent, task, model, tokens, cost)
- **Full Logging (opt-in):** Include prompt hashes for debugging
- **Audit Mode (compliance):** Log full prompts and responses (encrypted at rest)

---

## Usage Scenarios

### Scenario 1: AI Power User - Consistent Agent Experience

**Persona:** AI Power User (Consistency-Seeking)  
**Goal:** Maintain reliable, cost-effective LLM interactions across all agent profiles without manual tool switching.

**Current Workflow (Without Service Layer):**

1. Open Cursor for coding tasks with backend-dev agent
2. Switch to Claude web UI for architectural analysis (architect agent)
3. Manually copy/paste prompts between tools
4. Lose context when switching tools
5. No visibility into token costs across sessions
6. Frustration with inconsistent tool behavior

**New Workflow (With Service Layer):**

1. Configure preferred tools once in `~/.config/llm-service/agents.yaml`:
   ```yaml
   agents:
     architect: { preferred_tool: cursor, preferred_model: gpt-4-turbo }
     backend-dev: { preferred_tool: claude, preferred_model: claude-sonnet-20240229 }
   ```
2. Invoke any agent consistently: `llm-service exec --agent=architect --prompt=design.md`
3. Service automatically routes to correct tool (Cursor for architect, Claude for backend-dev)
4. View cost summary anytime: `llm-service stats --daily`
5. Adjust model preferences based on budget: Edit config to use cheaper models for simple tasks

**Benefits:**

- ✅ **Consistency:** Same CLI interface for all agents/tools
- ✅ **Context Preservation:** Service tracks conversation history per agent
- ✅ **Cost Awareness:** Real-time visibility into token usage
- ✅ **Workflow Efficiency:** No manual tool switching or copy/paste
- ⚠️ **Learning Curve:** Initial configuration setup required

**Token Cost Impact:**

- **Before:** ~50k tokens/day across mixed tools (no tracking, frequent GPT-4 usage)
- **After:** ~30k tokens/day (smart model selection, 40% cheaper models for simple tasks)
- **Monthly Savings:** Estimated $50-75 (assuming $0.01/1k tokens for premium models)

---

### Scenario 2: Software Engineer - Efficient Multi-Agent Collaboration

**Persona:** Software Engineer / Platform Engineer  
**Goal:** Orchestrate multiple agents on complex tasks with automatic tool/model selection.

**Current Workflow (Without Service Layer):**

1. Start architectural analysis: Manually open Cursor, load architect agent profile
2. Generate code: Switch to Claude Code, load backend-dev agent profile
3. Review documentation: Open GPT-4 web UI, manually format prompt
4. Context lost between tool switches (re-explain project every time)
5. Manual cost estimation (guessing token usage)
6. Sequential processing (wait for each tool to finish before next)

**New Workflow (With Service Layer):**

1. Create orchestration script (`orchestrate.sh`):
   ```bash
   llm-service exec --agent=architect --prompt=analyze.md --output=analysis.txt
   llm-service exec --agent=backend-dev --prompt=implement.md --context=analysis.txt --output=code.py
   llm-service exec --agent=scribe --prompt=document.md --context=code.py --output=README.md
   ```
2. Run script: `bash orchestrate.sh`
3. Service automatically:
   - Routes architect task to Cursor+GPT-4-turbo
   - Routes backend-dev task to Claude+Sonnet (with analysis.txt context)
   - Routes scribe task to Gemini+Pro (cheapest model for documentation)
4. Review aggregated costs: `llm-service stats --script=orchestrate.sh`

**Benefits:**

- ✅ **Automation:** Multi-agent workflow scripted and repeatable
- ✅ **Context Chaining:** Outputs from one agent feed into next automatically
- ✅ **Cost Optimization:** Service chooses cheaper models for documentation (30% savings)
- ✅ **Performance Tracking:** Compare execution time and cost across iterations
- ⚠️ **Sequential Execution:** Initial version processes agents one-by-one (parallel mode in future)

**Token Cost Impact:**

- **Before:** ~100k tokens/day (all tasks routed to GPT-4 manually, no optimization)
- **After:** ~70k tokens/day (30% cheaper models for simple tasks, better task-model matching)
- **Monthly Savings:** Estimated $100-150 (assuming $0.01/1k tokens average)

**Usability Improvement:**

- **Before:** 30 minutes manual orchestration (tool switching, copy/paste, context re-entry)
- **After:** 5 minutes setup + automated execution (5-6x faster)

---

### Scenario 3: Process Architect - Strategic Cost Management

**Persona:** Process Architect / Software Architect  
**Goal:** Define team-wide policies for LLM usage, enforce cost budgets, track usage patterns.

**Current Workflow (Without Service Layer):**

1. Team members use LLM tools ad-hoc (no central tracking)
2. Unexpected monthly bills ($500+ surprise costs)
3. No visibility into which agents/tasks consume most tokens
4. No enforcement of cost-effective model selection
5. Manual auditing of LLM usage (spreadsheets, API logs)

**New Workflow (With Service Layer):**

1. Define team policy in `config/policies.yaml`:
   ```yaml
   policies:
     team_budget:
       daily_budget_usd: 50.00
       monthly_budget_usd: 1000.00
       alert_threshold_percent: 80
     
     model_selection:
       simple_task_threshold_tokens: 1500
       simple_task_models: [claude-haiku-20240307, gpt-3.5-turbo]
       complex_task_models: [gpt-4-turbo, claude-opus-20240229]
       
     enforcement:
       block_over_budget: false
       require_justification_over_usd: 10.00
   ```
2. Distribute team configuration: Commit `config/` to repository, team members pull updates
3. Service automatically enforces policies:
   - Warns when approaching daily budget (80% threshold)
   - Auto-selects cheaper models for simple tasks
   - Logs justifications for expensive tasks
4. Review weekly usage report: `llm-service stats --team --week`
5. Identify optimization opportunities:
   - Which agents consume most tokens?
   - Which tasks are over-using expensive models?
   - Are fallback chains configured optimally?

**Benefits:**

- ✅ **Cost Control:** Proactive budget enforcement prevents surprise bills
- ✅ **Policy Automation:** Model selection rules applied consistently
- ✅ **Usage Transparency:** Detailed reports for strategic planning
- ✅ **Team Alignment:** Shared configuration in Git ensures consistency
- ⚠️ **Governance Overhead:** Requires initial policy design and periodic review

**Token Cost Impact:**

- **Before:** ~$1000/month (uncontrolled usage, mostly premium models)
- **After:** ~$500/month (50% reduction through smart model selection and budget alerts)
- **Annual Savings:** ~$6,000 (ROI for service layer development)

**Compliance Benefits:**

- Audit trail of all LLM invocations (who, what, when, cost)
- Privacy controls (no prompt logging in default mode)
- Compliance-ready reports for finance/legal review

---

## Impact Analysis

### Usability Improvements

**Positive Impacts:**

1. **Unified Interface:** Single CLI command for all agent-LLM interactions (reduces cognitive load)
2. **Automatic Tool Selection:** No need to remember which tool works best for which agent
3. **Context Preservation:** Service tracks conversation history and project context across invocations
4. **Cost Transparency:** Real-time visibility into token usage and estimated costs
5. **Configuration-Driven:** Preferences stored in Git-tracked YAML files (versioned, shareable)
6. **Fail-Safe Operation:** Automatic fallback to alternative tools when primary is unavailable

**Potential Usability Challenges:**

1. **Initial Configuration:** Requires upfront setup of `config/agents.yaml` and `config/tools.yaml`
2. **Learning Curve:** New CLI syntax to learn (vs. familiar tool-specific interfaces)
3. **Tool Installation:** Users must still install individual LLM CLI tools (service doesn't bundle them)
4. **Error Debugging:** Failures could originate from service layer OR underlying tools (adds indirection)

**Net Usability Score:** **+8/10** (significant improvement for regular users, minor overhead for setup)

---

### Token Cost Optimization

**Cost Reduction Mechanisms:**

1. **Smart Model Selection:**
   - Route simple tasks (< 1500 tokens) to cheaper models (Haiku, GPT-3.5-turbo)
   - Reserve premium models (GPT-4, Opus) for complex reasoning/architecture tasks
   - **Estimated Savings:** 30-40% reduction in average token cost

2. **Task-Model Matching:**
   - Coding tasks → Claude Sonnet (better code quality, 70% cheaper than GPT-4)
   - Architecture analysis → GPT-4 Turbo (better reasoning, worth premium)
   - Documentation → Gemini Pro or Haiku (cheapest option, sufficient quality)
   - **Estimated Savings:** 20-25% by avoiding over-provisioning

3. **Budget Enforcement:**
   - Daily/monthly spend limits prevent runaway costs
   - Warnings at 80% threshold allow course correction
   - **Risk Reduction:** Eliminate surprise $1000+ monthly bills

4. **Usage Analytics:**
   - Identify inefficient prompt patterns (e.g., repetitive context re-entry)
   - Optimize fallback chains based on actual tool availability
   - Track cost-per-task trends over time
   - **Continuous Improvement:** 5-10% ongoing optimization

**Cost Estimation Examples:**

| Agent          | Task Type      | Before (Model)     | Before (Cost/1k) | After (Model)       | After (Cost/1k) | Savings |
|----------------|----------------|--------------------|------------------|---------------------|-----------------|---------|
| Architect      | Analysis       | GPT-4              | $0.03            | GPT-4-turbo         | $0.01           | 67%     |
| Backend-Dev    | Simple Coding  | GPT-4              | $0.03            | Claude Sonnet       | $0.003          | 90%     |
| Backend-Dev    | Complex Debug  | Claude Opus        | $0.015           | Claude Opus         | $0.015          | 0%      |
| Scribe         | Documentation  | GPT-4              | $0.03            | Claude Haiku        | $0.00025        | 99%     |
| Planner        | Roadmap        | GPT-4              | $0.03            | GPT-4-turbo         | $0.01           | 67%     |

**Aggregate Cost Impact (Monthly Estimates):**

- **Low-Volume User (10k tokens/day):** $9/month → $4/month (56% savings, ~$60/year saved)
- **Medium-Volume User (50k tokens/day):** $45/month → $20/month (56% savings, ~$300/year saved)
- **High-Volume Team (500k tokens/day):** $450/month → $200/month (56% savings, ~$3000/year saved)

**ROI Calculation:**

- **Development Cost:** ~40 hours @ $100/hr = $4,000 (one-time)
- **Break-Even Point:** Medium-volume user saves $300/year → 13 users OR high-volume team (instant ROI)
- **5-Year Value:** $15,000 - $30,000 savings for a typical engineering team (10-20 developers)

---

## Tech Stack Recommendations (Detailed)

### Approved Options: Python or Node.js

The human-in-charge has approved **both Python and Node.js** as viable options for the initial implementation. The choice depends on team expertise and organizational context.

---

### Option A: Python-based Implementation (Recommended for ML/AI Teams)

**Rationale:**

- **Ubiquity:** Python installed on all target platforms (Linux, macOS, WSL2)
- **Agent Familiarity:** Most AI/ML practitioners comfortable with Python
- **Rapid Prototyping:** Fast iteration on configuration schemas and routing logic
- **Rich Ecosystem:** Libraries for CLI (Click/Typer), config (PyYAML), database (sqlite3), testing (pytest)
- **Distribution:** PyInstaller or Nuitka create standalone executables

**Core Dependencies:**

```python
# requirements.txt
click>=8.1.0           # CLI framework
pyyaml>=6.0            # Configuration parsing
pydantic>=2.0          # Configuration validation
rich>=13.0             # Terminal output formatting
```

**Project Structure:**

```
llm-service/
├── src/
│   ├── __init__.py
│   ├── cli.py              # Click-based CLI interface
│   ├── config.py           # Configuration loading and validation
│   ├── router.py           # Agent-to-tool routing logic
│   ├── executor.py         # Subprocess execution manager
│   ├── adapters/           # Tool-specific adapters
│   │   ├── claude_code.py  # Claude-Code adapter (MVP)
│   │   ├── codex.py        # Codex adapter (MVP)
│   │   └── base.py         # Base adapter interface
│   ├── telemetry.py        # Usage tracking and cost calculation
│   └── utils.py            # Shared utilities
├── config/
│   ├── agents.yaml
│   ├── tools.yaml
│   ├── models.yaml
│   └── policies.yaml
├── tests/
│   ├── test_router.py
│   ├── test_adapters.py
│   └── fixtures/
├── pyproject.toml
└── README.md
```

**Key Implementation Details:**

```python
# Example: router.py (simplified)
from pydantic import BaseModel
import yaml

class AgentConfig(BaseModel):
    preferred_tool: str
    preferred_model: str
    fallback_chain: list[str]

class Router:
    def __init__(self, config_path: str):
        self.agents = self._load_config(config_path)
    
    def route(self, agent: str, task_type: str) -> tuple[str, str]:
        """Returns (tool, model) for given agent and task."""
        agent_cfg = self.agents.get(agent)
        if not agent_cfg:
            raise ValueError(f"Unknown agent: {agent}")
        
        # Check task-specific overrides
        if task_type in agent_cfg.task_types:
            model = agent_cfg.task_types[task_type]
            tool = self._model_to_tool(model)
            return (tool, model)
        
        # Use preferred defaults
        return (agent_cfg.preferred_tool, agent_cfg.preferred_model)
```

**Testing Strategy:**

- **Unit Tests:** Mock subprocess calls, test routing logic with fixture configs
- **Integration Tests:** Real tool invocation with test prompts (requires tool installation)
- **CI/CD:** GitHub Actions with matrix strategy (Linux, macOS, Windows/WSL2)

---

### Option B: Node.js-based Implementation (Recommended for JavaScript-Centric Teams)

**Rationale:**

- **Familiarity:** Web developers and DevOps teams comfortable with Node.js
- **Async Excellence:** Native async/await for concurrent tool invocations (future enhancement)
- **Rich Ecosystem:** Libraries for CLI (Commander, Yargs), config (js-yaml), database (better-sqlite3)
- **Distribution:** `pkg` or Bun create standalone executables
- **Cross-Platform:** Node.js runtime available on all target platforms

**Core Dependencies:**

```json
{
  "dependencies": {
    "commander": "^11.0.0",
    "js-yaml": "^4.1.0",
    "better-sqlite3": "^9.0.0",
    "chalk": "^5.3.0"
  }
}
```

**Project Structure:**

```
llm-service/
├── src/
│   ├── cli.js              # Commander-based CLI interface
│   ├── config.js           # Configuration loading and validation
│   ├── router.js           # Agent-to-tool routing logic
│   ├── executor.js         # Child process execution manager
│   ├── adapters/           # Tool-specific adapters
│   │   ├── claudeCode.js   # Claude-Code adapter (MVP)
│   │   ├── codex.js        # Codex adapter (MVP)
│   │   └── base.js         # Base adapter interface
│   ├── telemetry.js        # Usage tracking and cost calculation
│   └── utils.js            # Shared utilities
├── config/
│   ├── agents.yaml
│   ├── tools.yaml
│   ├── models.yaml
│   └── policies.yaml
├── tests/
│   ├── router.test.js
│   ├── adapters.test.js
│   └── fixtures/
├── package.json
└── README.md
```

**Key Implementation Details:**

```javascript
// Example: router.js (simplified)
import yaml from 'js-yaml';
import { readFileSync } from 'fs';

class Router {
  constructor(configPath) {
    this.agents = this._loadConfig(configPath);
  }
  
  route(agent, taskType) {
    const agentCfg = this.agents[agent];
    if (!agentCfg) {
      throw new Error(`Unknown agent: ${agent}`);
    }
    
    // Check task-specific overrides
    if (agentCfg.task_types?.[taskType]) {
      const model = agentCfg.task_types[taskType];
      const tool = this._modelToTool(model);
      return { tool, model };
    }
    
    // Use preferred defaults
    return {
      tool: agentCfg.preferred_tool,
      model: agentCfg.preferred_model
    };
  }
}
```

**Testing Strategy:**

- **Unit Tests:** Jest with mocks for child processes
- **Integration Tests:** Real tool invocation with test prompts
- **CI/CD:** GitHub Actions with matrix strategy (Linux, macOS, Windows/WSL2)

---

### Comparison Matrix

| Criteria | Python | Node.js |
|----------|--------|---------|
| **Team Familiarity** | AI/ML practitioners, data scientists | Web developers, DevOps engineers |
| **Async Support** | Good (asyncio) | Excellent (native async/await) |
| **CLI Libraries** | Click, Typer | Commander, Yargs |
| **Distribution** | PyInstaller, Nuitka | pkg, Bun |
| **Startup Time** | ~100-200ms | ~50-100ms (faster) |
| **Memory Footprint** | ~30-50MB | ~20-40MB (lighter) |
| **Ecosystem Maturity** | Excellent for data/ML tools | Excellent for web/infra tools |
| **Cross-Platform** | Native (via Python runtime) | Native (via Node.js runtime) |
| **Learning Curve** | Low for ML teams | Low for web teams |

---

### Recommended Decision Process

**Choose Python if:**
- Team has ML/AI background (Python-native workflows)
- Existing tooling/scripts are Python-based
- Need rich data analysis capabilities (future enhancements)
- Prioritize rapid prototyping with mature ML ecosystem

**Choose Node.js if:**
- Team has web development background (JavaScript-native workflows)
- Need best-in-class async performance (future parallel invocations)
- Existing infrastructure is Node.js-based (CI/CD, deployment tools)
- Prioritize fast startup time and lightweight distribution

**Both are viable:** The architecture is language-agnostic. Configuration files (YAML) and tool adapters (subprocess-based) work identically in both implementations.
## Next Steps for Implementation

This prestudy provides the architectural foundation. The following steps are recommended:

### Phase 1: Minimal Viable Implementation (1-2 weeks)

1. **Configuration Schema:** Define and validate YAML structures for agents, tools, models, policies
2. **Router Logic:** Implement basic agent-to-tool mapping (no cost optimization yet)
3. **Tool Adapters:** Create Cursor and Claude adapters (cover 80% of use cases)
4. **CLI Interface:** Implement `llm-service exec` command with prompt file input
5. **Testing:** Unit tests for router, integration tests with mocked tools

**Deliverables:**

- Functional prototype with 2 tool adapters (Cursor, Claude)
- Basic configuration files (`config/agents.yaml`, `config/tools.yaml`)
- CLI that can route architect/backend-dev agents to appropriate tools
- Test suite covering core routing logic

### Phase 2: Cost Optimization & Telemetry (1 week)

1. **Model Catalog:** Add `config/models.yaml` with token costs
2. **Policy Engine:** Implement simple task threshold (< 1500 tokens → cheap model)
3. **Telemetry:** SQLite database for invocation logging
4. **Stats Command:** Implement `llm-service stats` for cost reporting

**Deliverables:**

- Smart model selection based on token count
- Local telemetry database with cost tracking
- Daily/monthly cost reports via CLI

### Phase 3: Robustness & Distribution (1 week)

1. **Fallback Logic:** Implement retry and fallback chain traversal
2. **Error Handling:** Graceful degradation when tools unavailable
3. **Distribution:** Create standalone executables (PyInstaller)
4. **Documentation:** User guide, configuration reference, troubleshooting

**Deliverables:**

- Production-ready service with error handling and fallbacks
- Standalone binaries for Linux, macOS, Windows/WSL2
- Comprehensive documentation and quickstart guide

### Phase 4: Advanced Features (Future Enhancements)

- **Parallel Execution:** Support concurrent tool invocation for multi-agent workflows
- **Context Management:** Automatic conversation history tracking per agent/project
- **Web UI:** Optional local dashboard for configuration and monitoring
- **Plugin System:** User-defined tool adapters without core code changes
- **Cloud Sync:** (Optional) Sync telemetry and configuration across machines

---

## Human Decisions (Approved 2026-02-04)

The following architectural decisions have been approved by the human-in-charge:

1. **Tech Stack Selection:** ✅ **Python or Node.js** for initial implementation
   - Both options approved; choose based on team expertise
   - Python: Better for ML/AI practitioners, rich ecosystem for CLI tools
   - Node.js: Familiar for JavaScript-centric teams, excellent async capabilities
   - **Recommendation:** Start with Python for prototype, consider Node.js if performance issues arise

2. **Configuration Format:** ✅ **YAML** confirmed
   - Human-readable and Git-friendly
   - Widely adopted in DevOps/infrastructure tooling
   - Strong library support in both Python (PyYAML) and Node.js (js-yaml)

3. **Budget Enforcement:** ✅ **Both hard and soft limits** (configurable)
   - Implement `limit.type` configuration setting: `soft` (warn only) or `hard` (block execution)
   - Default to `soft` for user-friendliness
   - Allow per-agent or per-project override via configuration

4. **Tool Coverage:** ✅ **Start with Claude-Code and Codex**
   - MVP focuses on `claude-code` and `codex` as primary tools
   - **Extensible design:** Allow adding new tool invocations via YAML configuration
   - Tool definition includes command template for easy integration (no code changes required)

### Configuration Examples (Approved Design)

**Policy Rules with Configurable Budget Enforcement (`config/policies.yaml`):**

```yaml
policies:
  default:
    daily_budget_usd: 10.00
    limit:
      type: soft              # Options: "soft" (warn), "hard" (block)
      threshold_percent: 80    # Warn/block at 80% of budget
    prefer_cheaper_models_under_tokens: 2000
    auto_fallback_on_rate_limit: true
    log_prompts: false
    log_metadata: true

  production:
    daily_budget_usd: 50.00
    limit:
      type: hard              # Block requests over budget
      threshold_percent: 90
    require_justification_over_usd: 10.00
```

**Tool Definitions with Command Templates (`config/tools.yaml`):**

```yaml
tools:
  claude-code:
    binary: claude
    command_template: "{binary} {prompt_file} --model {model} --output {output_file}"
    platforms:
      linux: /usr/local/bin/claude
      macos: /usr/local/bin/claude
      windows: /usr/bin/claude  # Via WSL2
    models:
      - claude-opus-20240229
      - claude-sonnet-20240229
      - claude-haiku-20240307
    capabilities:
      - code_generation
      - code_review
      - long_context

  codex:
    binary: codex
    command_template: "{binary} generate --prompt={prompt_file} --model={model}"
    platforms:
      linux: /usr/local/bin/codex
      macos: /usr/local/bin/codex
      windows: /usr/bin/codex  # Via WSL2
    models:
      - code-davinci-002
      - gpt-4-turbo
      - gpt-5.2-preview
    capabilities:
      - code_generation
      - code_completion
      - technical_documentation

  # Example: Adding new tool via YAML (no code changes)
  gemini-cli:
    binary: gemini
    command_template: "{binary} --input {prompt_file} --model {model} --format json"
    platforms:
      linux: /usr/local/bin/gemini
      macos: /usr/local/bin/gemini
      windows: /usr/bin/gemini  # Via WSL2
    models:
      - gemini-pro
      - gemini-pro-vision
    capabilities:
      - multimodal
      - data_analysis
      - vision
```

### Implications of Approved Decisions

**1. Python/Node.js Flexibility:**
- Implementation team can choose based on expertise
- Both have mature CLI frameworks (Python: Click/Typer, Node.js: Commander/Yargs)
- Both support YAML parsing, subprocess execution, and SQLite integration
- **Action:** Document dual-path implementation guide in Phase 1

**2. YAML-Based Tool Extensibility:**
- Users can add new LLM tools without modifying service code
- Command template pattern enables flexible CLI invocation syntax
- Platform-specific binary paths support cross-OS deployments
- **Action:** Create tool adapter plugin architecture that reads command templates

**3. Configurable Budget Enforcement:**
- `soft` mode: Warn users, log overage, allow override (default for development)
- `hard` mode: Block execution, require explicit budget increase (recommended for production)
- Per-agent budget overrides possible (e.g., architect gets higher budget for complex analysis)
- **Action:** Implement budget policy engine with warning/blocking logic

**4. MVP Tool Focus:**
- `claude-code` for code generation and review (Anthropic)
- `codex` for code completion and technical docs (OpenAI)
- Clear path to add Gemini, Cursor, or custom tools via YAML
- **Action:** Build two reference adapters (claude-code, codex), document template for community contributions

---

## Diagrams

The following architecture diagrams have been created in PlantUML format by Diagram Daisy:

### 1. Component Architecture Diagram (C4 Container Level)

**Location:** `docs/architecture/diagrams/llm-service-layer-component-architecture.puml`

Shows the service core, CLI interface, tool adapters, configuration layer, and telemetry database. Illustrates data flow from agent invocation through routing, policy enforcement, tool execution, and response delivery.

**Key Components:**
- CLI Interface (user interaction)
- Routing Engine (agent-to-tool mapping)
- Configuration Manager (YAML loading)
- Policy Engine (budget enforcement, cost optimization)
- Execution Manager (subprocess orchestration)
- Tool Adapters (Claude-Code, Codex, Generic)
- Telemetry Database (SQLite)

### 2. Request Flow Sequence Diagram

**Location:** `docs/architecture/diagrams/llm-service-layer-request-flow-sequence.puml`

Details the step-by-step interaction from `llm-service exec` command through configuration lookup, policy application, tool invocation, telemetry logging, and response return.

**Sequence Steps:**
1. User invokes CLI command
2. Configuration loading (agents, tools, models, policies)
3. Routing decision (agent → tool+model)
4. Policy enforcement (budget check, cost optimization)
5. Tool adapter invocation (subprocess execution)
6. Telemetry logging (tokens, cost, latency)
7. Response delivery to user

### 3. Configuration Relationships Diagram

**Location:** `docs/architecture/diagrams/llm-service-layer-configuration-relationships.puml`

Shows relationships between `agents.yaml`, `tools.yaml`, `models.yaml`, and `policies.yaml`. Illustrates how configuration files compose to determine routing decisions.

**Configuration Flow:**
1. `agents.yaml` → preferred_tool (references `tools.yaml`)
2. `agents.yaml` → preferred_model (references `models.yaml`)
3. `tools.yaml` → command_template + available models
4. `models.yaml` → cost data + capabilities
5. `policies.yaml` → budget rules + optimization thresholds
6. Composition → final CLI invocation command

### 4. Deployment Architecture Diagram

**Location:** `docs/architecture/diagrams/llm-service-layer-deployment-architecture.puml`

Depicts local machine setup across Linux, macOS, and Windows/WSL2 environments. Shows LLM Service installation, configuration file locations, telemetry database, and installed LLM CLI tools.

**Platform-Specific Details:**
- **Linux:** Native deployment with XDG paths
- **macOS:** Native deployment with Homebrew support
- **Windows:** WSL2-based deployment with path translation

**Configuration Paths:**
- Config: `~/.config/llm-service/`
- Telemetry: `~/.local/share/llm-service/`
- Tools: Platform-specific (defined in `tools.yaml`)

---

## References

- **Agent Profiles:** `.github/agents/*.agent.md`
- **Personas:** `docs/audience/*.md`
- **Directives:** `.github/agents/directives/`
- **Templates:** `docs/templates/architecture/`
- **Related ADRs:** (To be created upon human approval of this prestudy)

---

## Metadata

- **Version:** 0.2.0 (Approved Prestudy)
- **Status:** Approved - Ready for Implementation
- **Approval Date:** 2026-02-04
- **Approved Decisions:** Python/Node.js tech stack, YAML configuration, configurable budget limits, claude-code+codex MVP tools
- **Next Steps:** Implementation planning (milestones and task assignment) → Diagram creation → Phase 1 kickoff
- **Estimated Implementation Effort:** 3-4 weeks for Phases 1-3 (MVP)
- **Estimated Value:** $3,000 - $6,000 annual cost savings for typical engineering team
