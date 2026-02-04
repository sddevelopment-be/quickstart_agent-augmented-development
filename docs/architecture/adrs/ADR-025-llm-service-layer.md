# Architecture Decision Records

## ADR-025: LLM Service Layer for Agent-Tool Orchestration

**status**: `Accepted`  
**date**: 2026-02-04  
**decision-makers**: Human-in-Charge, Architect Alphonso  
**consulted**: AI Power Users, Software Engineers, Process Architects

### Context

The current agent-augmented development framework provides agent profiles, directives, and file-based orchestration patterns for structured multi-agent workflows. However, agent-to-LLM-stack interaction remains manual and unoptimized:

**Current State Problems:**
1. **Manual Tool Selection:** Each agent interaction requires developers to manually choose between LLM tools (Claude, Cursor, Codex, Gemini CLI)
2. **No Cost Optimization:** Developers have no guidance on model selection, leading to over-provisioning (always using expensive models like GPT-4)
3. **No Usage Tracking:** Token consumption and costs are invisible, resulting in surprise bills and inability to optimize
4. **Context Switching Overhead:** Switching between tools requires re-entering context, copying prompts, and learning different CLI syntaxes
5. **No Policy Enforcement:** Teams lack centralized budget controls or cost-effective model selection rules

**Business Impact:**
- Estimated $1,000+/month uncontrolled LLM spending per team
- 30-40 minutes/day wasted on tool switching and manual invocation
- No data-driven insights for cost optimization

**Forces at Play:**
- **User Experience:** Need unified interface for all agent-LLM interactions
- **Cost Control:** Budget limits and smart model selection essential for sustainability
- **Extensibility:** New LLM tools emerge frequently (Gemini, Cursor); need adaptable architecture
- **Cross-Platform:** Teams use Linux, macOS, Windows/WSL2; must support all
- **Simplicity:** MVP must be implementable in 4 weeks with 1-2 developers

### Decision

**We will build a configuration-driven LLM Service Layer** that routes agent requests to appropriate LLM CLI tools based on agent identity, task complexity, and cost policies.

**Core Components:**
1. **Configuration Layer:** YAML-based files defining agent-to-tool mappings, model catalogs, and budget policies
2. **CLI Interface:** Single command (`llm-service exec --agent=X --prompt=file.md`) for all interactions
3. **Routing Engine:** Selects tool and model based on agent preferences, task complexity, and fallback chains
4. **Tool Adapters:** Abstraction layer for LLM CLI invocation with common interface and YAML-configurable command templates
5. **Policy Engine:** Enforces budget limits (configurable soft warnings vs. hard blocks) and optimizes model selection
6. **Telemetry System:** SQLite database tracking token usage, costs, and performance metrics

**Technology Decisions:**
- **Implementation Language:** Python OR Node.js (both approved; team chooses based on expertise)
- **Configuration Format:** YAML (human-readable, Git-friendly, widely adopted)
- **Budget Enforcement:** Configurable via `limit.type: soft|hard` (soft = warn, hard = block)
- **MVP Tools:** claude-code + codex (extensible via YAML command templates)
- **Cross-Platform:** Native on Linux/macOS, WSL2 on Windows

**Key Design Principles:**
1. **Configuration-Driven:** All routing decisions in YAML, not hardcoded
2. **KISS (Keep It Simple):** Single-process service, no microservices or remote APIs
3. **Extensibility:** New tools added via YAML config without code changes
4. **Cost-Aware:** Smart model selection (simple tasks → cheap models)
5. **Observable:** Every invocation logged for cost tracking and debugging

### Rationale

**Why Configuration-Driven Architecture?**
- **Flexibility:** Users customize agent-tool mappings without code changes
- **Maintainability:** Configuration versioned in Git alongside code
- **Testability:** Configuration validation catches errors before execution
- **Collaboration:** Teams share configurations via repository commits

**Why YAML Over JSON/TOML?**
- **Readability:** Comments and multi-line strings improve documentation
- **Adoption:** Widely used in DevOps/infrastructure tooling (Kubernetes, Docker Compose, Ansible)
- **Ecosystem:** Mature libraries in Python (PyYAML) and Node.js (js-yaml)

**Why Python/Node.js Over Go?**
- **Rapid Prototyping:** Python/Node.js enable faster MVP iteration (4-week constraint)
- **Agent Familiarity:** Most AI/ML practitioners know Python; web teams know Node.js
- **Rich Ecosystem:** Abundant libraries for CLI, subprocess execution, YAML parsing
- **Trade-off:** Go offers better performance and simpler distribution, but longer development time

**Why Configurable Budget Enforcement (soft/hard)?**
- **Flexibility:** Soft limits (warnings) good for development/experimentation
- **Safety:** Hard limits (blocks) required for production cost control
- **User Adoption:** Soft defaults reduce friction, hard limits optional for governance

**Why SQLite Over PostgreSQL/MySQL?**
- **Simplicity:** No external database server required (single-file storage)
- **Portability:** Database travels with configuration (easy backup/restore)
- **Sufficient:** Handles 100k+ invocation records without performance issues
- **Local-First:** Aligns with local machine usage requirement

**Why Tool Adapters With Command Templates?**
- **Extensibility:** Users add new tools via YAML without code changes
- **Maintainability:** Command template changes don't require recompilation
- **Community:** Users can contribute tool definitions via pull requests
- **Future-Proof:** Adapts to evolving LLM CLI interfaces

### Envisioned Consequences

**Positive Consequences:**

**Agility:**
- ✅ **Unified Interface:** Single CLI command for all agent-LLM interactions (reduced cognitive load)
- ✅ **Faster Iteration:** Configuration changes take effect immediately (no recompilation)
- ✅ **Multi-Agent Orchestration:** Context chaining enables automated workflows (5-6x speedup per prestudy estimates)

**Maintainability:**
- ✅ **YAML Configuration:** Human-readable, Git-tracked, easily reviewed in pull requests
- ✅ **Tool Extensibility:** New LLM tools added without core code changes (community contributions welcome)
- ✅ **Testability:** Configuration validation catches errors early; mocks simplify testing

**Modifiability:**
- ✅ **Agent Preferences:** Teams customize tool/model mappings per agent without code changes
- ✅ **Policy Flexibility:** Budget limits and optimization rules adjust to organizational needs
- ✅ **Platform Adaptation:** Command templates handle platform-specific binary paths

**Ergonomics:**
- ✅ **Consistent UX:** Same CLI syntax across all tools (learning curve reduced)
- ✅ **Cost Transparency:** Stats command provides real-time spending visibility
- ✅ **Fail-Safe:** Automatic fallback to alternative tools when primary unavailable

**Repeatability:**
- ✅ **Configuration Versioning:** Teams share standard configurations via Git
- ✅ **Telemetry Data:** Historical logs enable data-driven optimization
- ✅ **Reproducible Builds:** Configuration + code = deterministic behavior

**Security:**
- ✅ **Audit Trail:** Every invocation logged (compliance-ready)
- ✅ **Budget Controls:** Prevent runaway costs through configurable limits
- ✅ **Privacy Controls:** Metadata-only logging default (no prompt content stored)

**Negative Consequences:**

**Agility:**
- ⚠️ **Initial Configuration Overhead:** Users must set up YAML files before first use (mitigated by `llm-service init` wizard and examples)
- ⚠️ **Learning Curve:** New CLI syntax to learn (mitigated by comprehensive documentation and examples)

**Maintainability:**
- ⚠️ **Configuration Complexity:** Multiple YAML files (agents, tools, models, policies) could become unwieldy (mitigated by validation and clear documentation)
- ⚠️ **Cross-Platform Testing:** Requires CI/CD matrix for Linux, macOS, WSL2 (added testing burden)

**Modifiability:**
- ⚠️ **Tech Stack Lock-In:** Python or Node.js choice limits contributor pool to specific language community (mitigated by choosing popular languages)

**Ergonomics:**
- ⚠️ **Indirection Layer:** Errors could originate from service OR underlying tools (mitigated by clear error messages and logging)
- ⚠️ **Tool Installation Requirement:** Users must still install individual LLM CLIs (service doesn't bundle them)

**Repeatability:**
- ⚠️ **Configuration Drift:** Teams may diverge in configurations over time (mitigated by shared configuration repo patterns)

**Security:**
- ⚠️ **Credential Management:** API keys for LLM tools must be secured (mitigated by environment variable + keychain guidance)
- ⚠️ **Prompt Injection Risks:** Malicious prompt files could exploit subprocess execution (mitigated by input sanitization and subprocess security)

**Cost Impact:**
- **Development:** ~160 hours (4 weeks × 1-2 developers) = $16,000-$32,000 one-time cost
- **Savings:** $3,000-$6,000/year per team (30-56% token cost reduction per prestudy analysis)
- **ROI:** Break-even at 3-5 teams or 1 year for single high-volume team

### Considered Alternatives

**Alternative 1: API-Based Remote Service**
- **Description:** Deploy LLM routing service as remote API (e.g., REST/gRPC server)
- **Rejected Because:** Requirements explicitly state "local machine usage only, with CLI-based interaction." Remote service adds complexity (authentication, network latency, deployment infrastructure) without solving current problem. Future enhancement possible if remote collaboration needed.

**Alternative 2: Simple Shell Script Wrapper**
- **Description:** Bash/Python script that wraps LLM CLI tools without configuration system
- **Rejected Because:** Insufficient for complex routing logic, cost tracking, and policy enforcement. Would become brittle as requirements evolve. Configuration-driven approach provides better maintainability and extensibility.

**Alternative 3: Embedded DSL for Agent Configuration**
- **Description:** Custom domain-specific language for expressing agent-tool mappings (e.g., Ruby DSL, Python decorators)
- **Rejected Because:** YAML provides better balance of readability and power. Custom DSL increases learning curve without clear benefit. YAML is widely understood and has strong tooling support (linters, validators, editors).

**Alternative 4: Go Implementation for Performance**
- **Description:** Implement service in Go for faster execution and simpler distribution (single static binary)
- **Rejected Because:** Python/Node.js enable faster MVP development (4-week constraint). Performance unlikely to be bottleneck for local CLI usage (subprocess execution dominates latency). Go could be migration target if performance issues arise, but not justified for MVP.

**Alternative 5: Direct LLM API Integration (No CLI Tools)**
- **Description:** Service calls LLM APIs directly (OpenAI API, Anthropic API) instead of invoking CLI tools
- **Rejected Because:** Requires managing multiple API clients, authentication, rate limiting, and error handling. CLI tools already solve these problems. Adapter pattern allows mixing API and CLI approaches in future if needed.

**Alternative 6: Monolithic Tool Support (Cursor or Claude Only)**
- **Description:** Build service for single tool (e.g., Cursor) with tight integration
- **Rejected Because:** Violates extensibility goal. Teams use diverse LLM tools; single-tool approach forces vendor lock-in. Generic adapter pattern enables multi-tool support without significant complexity increase.

### Implementation Plan

**Milestone 1: Foundation (Weeks 1-2)**
- Configuration schema (YAML) with validation
- CLI interface (exec, config validate, init, version)
- Routing engine (agent-to-tool mapping, fallback chains)

**Milestone 2: Tool Integration (Weeks 2-3)**
- Adapter base interface
- Claude-Code adapter (MVP tool #1)
- Codex adapter (MVP tool #2)
- Generic YAML-configured adapter

**Milestone 3: Cost Optimization & Telemetry (Weeks 3-4)**
- SQLite telemetry database
- Policy engine (budget enforcement, cost optimization)
- Stats command (daily/monthly reports)

**Milestone 4: Integration & Distribution (Week 4)**
- Acceptance tests (8 Gherkin scenarios)
- Cross-platform testing (Linux, macOS, WSL2)
- Documentation (user guide, configuration reference, persona workflows)
- Packaging (PyInstaller/pkg standalone executables)

**Human Gates:**
- Approval before Milestone 3 (cost implications for users)
- Final approval before public release

### Related Documents

- **Prestudy:** `docs/architecture/design/llm-service-layer-prestudy.md` (detailed architecture)
- **Diagrams:** `docs/architecture/diagrams/llm-service-layer-*.puml` (4 PlantUML diagrams)
- **Implementation Plan:** `docs/planning/llm-service-layer-implementation-plan.md` (milestones, tasks, batches)
- **Roadmap:** `docs/architecture/roadmap-llm-service-layer.md` (timeline, metrics, risks)
- **Task Files:** `work/collaboration/inbox/2026-02-04T17*-*.yaml` (file-based orchestration)

### Acceptance Criteria

This ADR is considered accepted when:
- ✅ Human-in-charge approved architectural decisions (completed 2026-02-04)
- ✅ Prestudy document finalized with approved design (completed)
- ✅ Architecture diagrams created (4 PlantUML diagrams completed)
- ✅ Implementation plan with task breakdown created (completed)
- ✅ ADR published and linked from prestudy/roadmap (this document)
- ⏳ Phase 1 implementation begins (pending tech stack decision)

### Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-02-04 | 1.0.0 | Initial ADR creation based on approved prestudy | Architect Alphonso |

---

**Status:** ✅ **Accepted** (2026-02-04)  
**Next Action:** Begin Phase 1 implementation after tech stack decision (Python vs. Node.js)
