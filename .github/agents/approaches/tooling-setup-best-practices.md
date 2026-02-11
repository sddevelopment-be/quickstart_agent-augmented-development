# Tooling Setup Best Practices

**Approach Type:** Development Environment Configuration  
**Version:** 1.0.0  
**Last Updated:** 2025-11-27  
**Status:** Active

## Overview

This approach describes best practices for setting up, configuring, and maintaining development tooling to support agent-augmented development. It provides a framework for tool selection, configuration patterns, and maintenance strategies that ensure consistent, secure, and performant development environments.

**Related Resources:**

- **Directive 013:** [Tooling Setup & Fallbacks](./../directives/013_tooling_setup.md) — Installation commands and fallback strategies
- **Directive 001:** [CLI & Shell Tooling](./../directives/001_cli_shell_tooling.md) — Tool usage patterns
- **Source Assessment:** [Copilot Tooling Value Assessment](../../../work/reports/logs/architect/2025-11-24-copilot-tooling-value-assessment.md)

## Core Principles

### 1. Tool Selection Rigor

Choose tools based on measurable criteria: usage frequency, performance improvement, maintenance activity, and security posture.

### 2. Configuration Consistency

Establish reproducible environments through version pinning, platform-aware setup scripts, and documented configuration patterns.

### 3. Proactive Maintenance

Schedule regular reviews to update versions, audit security, assess performance, and align with evolving agent needs.

### 4. Graceful Degradation

Provide fallback strategies for every tool to ensure agents can operate even when preferred tools are unavailable.

### 5. Documentation Discipline

Keep setup instructions, troubleshooting guides, and version tables synchronized with actual tooling state.

## When to Use This Approach

**Use tooling setup best practices when:**

- Establishing a new development environment for agent-augmented work
- Evaluating tools for addition to the standard toolkit
- Configuring CI/CD environments for consistent agent execution
- Troubleshooting tool availability or performance issues
- Planning quarterly or annual tooling maintenance reviews
- Creating derivative repositories from templates

**Do NOT use this approach when:**

- Working with experimental or one-off tools not intended for standardization
- Setting up tools outside the agent execution context
- Making temporary workarounds that shouldn't become precedents

## Tool Selection Guidelines

### Decision Framework

Use this four-step evaluation process for any tool under consideration:

#### 1. Necessity Check

Answer these questions to determine if a tool justifies inclusion:

- **Frequency:** Is this tool used by agents in >50% of tasks?
- **Fallback Quality:** Does a generic fallback exist (e.g., `grep` for `rg`)?
- **ROI Threshold:** Does installation overhead + maintenance cost < cumulative time saved?

**Example Evaluation:**

```markdown
Tool: ripgrep (rg)
- Frequency: ~80% of agent tasks involve code search
- Fallback: grep (universal availability)
- Performance gain: 10-100x faster than grep
- Verdict: INCLUDE
```

#### 2. Quality Assessment

Evaluate tool maturity and community health:

- **Active Maintenance:** Commits or releases in the last 6 months
- **Community Support:** >1,000 GitHub stars for niche tools, >5,000 for widely-adopted tools
- **Package Manager Support:** Available in apt, brew, or other official channels
- **Versioning Clarity:** Follows semantic versioning with clear changelogs

**Red Flags:**

- No commits in >12 months
- Multiple unresolved critical issues
- Frequent API breaking changes
- Abandoned or forked without active maintainer

#### 3. Security Evaluation

Assess supply chain and runtime security:

- **Distribution Channels:** Official repositories or verified binaries only
- **Verification Mechanisms:** GPG signatures or SHA256 checksums available
- **Vulnerability Status:** No unresolved critical CVEs in security databases
- **Dependency Tree:** Minimal external dependencies (reduces attack surface)

**Security Checklist:**

```markdown
- [ ] Tool distributed through official channels (apt, brew, GitHub releases)
- [ ] Download URLs use HTTPS exclusively
- [ ] Checksums or signatures available for binary downloads
- [ ] CVE database checked (no critical unresolved issues)
- [ ] Dependencies reviewed (if applicable)
- [ ] Tool doesn't require elevated privileges for normal operation
```

#### 4. Performance Validation

Benchmark against alternatives and measure overhead:

- **Performance Ratio:** >2x improvement over fallback for primary use cases
- **Installation Time:** <30 seconds preferred, <60 seconds acceptable
- **Disk Space:** <20MB per tool, <50MB for comprehensive toolchains
- **Startup Overhead:** Negligible impact on agent cold-start time

**Benchmark Template:**

```bash
# Measure tool performance
time rg "pattern" .  # Test tool
time grep -r "pattern" .  # Compare fallback

# Measure installation overhead
time install_tool.sh  # Record setup duration
du -sh /usr/local/bin/tool  # Check disk usage
```

### Tool Selection Checklist

Use this checklist for consistent evaluation:

```markdown
## Tool Evaluation: [Tool Name]

### Necessity
- [ ] Used by agents frequently (>5 invocations/week projected)
- [ ] Provides >2x performance improvement over fallback
- [ ] Fallback strategy documented and tested

### Quality
- [ ] Available in apt/brew repositories OR verifiable binary
- [ ] Actively maintained (last commit <6 months ago)
- [ ] Semantic versioning with clear changelogs
- [ ] Community size appropriate for tool type

### Security
- [ ] Official distribution channel verified
- [ ] GPG signature or SHA256 checksum available
- [ ] No unresolved critical CVEs
- [ ] Minimal dependency tree

### Performance
- [ ] Installation time <30 seconds
- [ ] Disk space <20MB
- [ ] Benchmarked against fallback (>2x faster)
- [ ] Cold start impact measured (<5s)

### Documentation
- [ ] Usage examples in Directive 001
- [ ] Installation instructions in Directive 013
- [ ] Troubleshooting guidance documented
- [ ] Version requirements specified

**Decision:** [INCLUDE / EXCLUDE / DEFER]  
**Rationale:** [Brief explanation]
```

## Configuration Best Practices

### Version Pinning Strategy

Balance stability with updates using a tiered approach:

#### Tier 1: Pinned Versions (Stability-Critical Tools)

Pin specific versions for tools where API changes or behavioral differences impact agent reliability:

```bash
# Pin tools with stability requirements
YQ_VERSION="v4.40.5"  # Stable API, rare breaking changes
AST_GREP_VERSION="0.15.1"  # AST structure compatibility matters

# Download and verify
wget "https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_amd64"
echo "${YQ_SHA256} yq_linux_amd64" | sha256sum --check
```

**When to Pin:**

- AST-based tools where syntax changes affect parsing
- YAML/JSON processors with query language variations
- Tools with breaking changes in minor versions

#### Tier 2: Package Manager Versions (Auto-Update)

Let package managers handle updates for stable, backward-compatible tools:

```bash
# Auto-update via package manager
sudo apt install -y ripgrep fd-find jq

# These tools maintain backward compatibility and benefit from
# security patches without manual intervention
```

**When to Auto-Update:**

- Search tools with stable CLI interfaces (rg, fd)
- Standard utilities with POSIX compatibility (jq)
- Tools with strong backward compatibility commitments

#### Tier 3: Latest Stable (Cutting Edge)

Use latest versions for rapidly evolving tools where new features outweigh stability:

```bash
# Install latest stable release
LATEST=$(curl -s https://api.github.com/repos/tool/releases/latest | jq -r .tag_name)
wget "https://github.com/tool/releases/download/${LATEST}/tool-binary"
```

**When to Track Latest:**

- Experimental tools in early adoption phase
- Tools where new features directly impact agent capabilities
- Development tools not used in production scripts

### Error Handling Patterns

Implement resilient installation with appropriate failure modes:

#### Critical Tools (Fail Fast)

For tools essential to agent operation, fail immediately with clear diagnostics:

```bash
install_critical_tool() {
    local tool_name="$1"
    local install_cmd="$2"
    
    if ! eval "$install_cmd"; then
        log_error "Critical tool ${tool_name} failed to install"
        log_error "Agent execution requires this tool. Aborting setup."
        exit 1
    fi
    
    log_success "Installed ${tool_name}"
}

# Usage
install_critical_tool "ripgrep" "sudo apt install -y ripgrep"
install_critical_tool "fd" "sudo apt install -y fd-find"
```

#### Optional Tools (Warn and Continue)

For tools that enhance but don't block agent functionality, log warnings and continue:

```bash
install_optional_tool() {
    local tool_name="$1"
    local install_cmd="$2"
    local fallback="$3"
    
    if ! eval "$install_cmd"; then
        log_warning "Optional tool ${tool_name} not available"
        log_warning "Agents will use fallback: ${fallback}"
        return 1
    fi
    
    log_success "Installed ${tool_name}"
    return 0
}

# Usage
install_optional_tool "ast-grep" "install_ast_grep.sh" "grep/sed patterns"
install_optional_tool "fzf" "install_fzf.sh" "manual selection"
```

#### Verification Steps

After installation, verify tool availability and basic functionality:

```bash
verify_installation() {
    local tool_name="$1"
    local version_cmd="$2"
    local min_version="$3"
    
    if ! command -v "$tool_name" &>/dev/null; then
        log_error "${tool_name} not found in PATH"
        return 1
    fi
    
    local actual_version
    actual_version=$(eval "$version_cmd" 2>/dev/null | grep -oP '\d+\.\d+\.\d+' | head -1)
    
    log_success "${tool_name} installed: version ${actual_version}"
    
    if [[ -n "$min_version" ]]; then
        if version_compare "$actual_version" "$min_version"; then
            log_success "Version meets minimum requirement (${min_version})"
        else
            log_warning "Version below minimum (${min_version}), may cause issues"
        fi
    fi
}

# Usage
verify_installation "rg" "rg --version" "13.0.0"
verify_installation "fd" "fd --version" "8.0.0"
verify_installation "jq" "jq --version" "1.6"
```

### Platform Compatibility

Handle platform-specific quirks gracefully:

#### Linux (Debian/Ubuntu)

Address package naming and path issues:

```bash
handle_linux_quirks() {
    # fd-find vs fd naming issue on Debian/Ubuntu
    if command -v fdfind &>/dev/null && ! command -v fd &>/dev/null; then
        log_info "Creating fd symlink for Debian/Ubuntu compatibility"
        sudo ln -sf "$(which fdfind)" /usr/local/bin/fd
    fi
    
    # Ensure /usr/local/bin is in PATH
    if [[ ":$PATH:" != *":/usr/local/bin:"* ]]; then
        log_warning "/usr/local/bin not in PATH, adding temporarily"
        export PATH="/usr/local/bin:$PATH"
    fi
}
```

#### macOS (Homebrew)

Handle Homebrew path variations:

```bash
handle_macos_quirks() {
    # Initialize Homebrew environment
    if [[ -f /opt/homebrew/bin/brew ]]; then
        # Apple Silicon
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [[ -f /usr/local/bin/brew ]]; then
        # Intel
        eval "$(/usr/local/bin/brew shellenv)"
    else
        log_warning "Homebrew not found, some tools may be unavailable"
    fi
    
    # fzf shell integration
    if [[ -d "$(brew --prefix)/opt/fzf/shell" ]]; then
        source "$(brew --prefix)/opt/fzf/shell/completion.bash"
        source "$(brew --prefix)/opt/fzf/shell/key-bindings.bash"
    fi
}
```

#### Cross-Platform Detection

Detect platform early and route accordingly:

```bash
detect_platform() {
    case "$(uname -s)" in
        Linux*)
            if [[ -f /etc/debian_version ]]; then
                echo "debian"
            elif [[ -f /etc/redhat-release ]]; then
                echo "redhat"
            else
                echo "linux-generic"
            fi
            ;;
        Darwin*)
            echo "macos"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            echo "windows"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Usage
PLATFORM=$(detect_platform)
case "$PLATFORM" in
    debian)
        handle_linux_quirks
        install_via_apt
        ;;
    macos)
        handle_macos_quirks
        install_via_brew
        ;;
    *)
        log_error "Unsupported platform: $PLATFORM"
        exit 1
        ;;
esac
```

## Maintenance Guidelines

### Quarterly Review Process

Schedule and execute these reviews every 3 months:

#### Version Update Workflow

```markdown
## Q[X] YYYY Tooling Review

**Date:** [Review Date]  
**Reviewer:** [Agent or Human]  
**Duration:** [Est. 30-45 minutes]

### 1. Version Updates

**For each pinned tool:**

- [ ] Check GitHub releases for new stable versions
  ```bash
  # Example for yq
  curl -s https://api.github.com/repos/mikefarah/yq/releases/latest | jq -r .tag_name
  ```

- [ ] Review changelog for breaking changes
    - API modifications affecting agent scripts
    - CLI flag deprecations or changes
    - Performance regressions noted

- [ ] Test new version in staging environment
  ```bash
  # Install candidate version
  YQ_VERSION="v4.41.0"
  ./install_tool.sh yq "$YQ_VERSION"
  
  # Run test suite
  ./tests/tool_compatibility_tests.sh
  ```

- [ ] Update version constants if validated
  ```bash
  # In setup.sh or config file
  YQ_VERSION="v4.41.0"  # Updated from v4.40.5
  ```

**Update Log:**
| Tool | Old Version | New Version | Breaking Changes | Status |
|------|-------------|-------------|------------------|--------|
| yq | v4.40.5 | v4.41.0 | None | ✅ Updated |
| ast-grep | 0.15.1 | 0.16.0 | Query syntax change | ⚠️ Deferred |

### 2. Security Audit

- [ ] Scan for known CVEs
  ```bash
  # Check CVE databases for each tool
  curl -s "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=ripgrep"
  ```

- [ ] Verify checksums still valid
  ```bash
  # Re-download checksum files and compare
  wget https://github.com/tool/releases/download/v1.0/checksums.txt
  sha256sum -c checksums.txt
  ```

- [ ] Review supply chain security advisories
    - GitHub Security Advisories
    - Tool-specific security mailing lists
    - Dependency vulnerabilities (if applicable)

- [ ] Update security documentation
    - Document new vulnerabilities (if any)
    - Update mitigation strategies
    - Refresh security checklist in Directive 013

**Security Status:**
| Tool | CVE Check | Checksum | Advisories | Status |
|------|-----------|----------|------------|--------|
| ripgrep | ✅ Clean | ✅ Valid | ✅ None | Safe |
| yq | ✅ Clean | ✅ Valid | ✅ None | Safe |

### 3. Performance Assessment

- [ ] Measure setup duration
  ```bash
  # Should remain <120 seconds total
  time ./setup.sh
  ```

- [ ] Check disk space usage
  ```bash
  # Should remain <500MB total
  du -sh /usr/local/bin/{rg,fd,jq,yq,ast-grep,fzf}
  ```

- [ ] Review tool usage logs
    - Identify frequently-used tools (keep)
    - Identify rarely-used tools (candidates for removal)
    - Look for missing tools agents request repeatedly

- [ ] Benchmark against baseline metrics
  ```bash
  # Compare search performance
  time rg "pattern" .  # Should remain <2s on repo
  time fd -t f -e md  # Should remain <1s on repo
  ```

**Performance Metrics:**
| Metric | Baseline | Current | Delta | Status |
|--------|----------|---------|-------|--------|
| Setup time | 95s | 102s | +7s | ✅ Acceptable |
| Disk usage | 380MB | 395MB | +15MB | ✅ Acceptable |
| Search (rg) | 1.2s | 1.1s | -0.1s | ✅ Improved |

### 4. Documentation Sync

- [ ] Update version table in Directive 013
- [ ] Refresh troubleshooting guide with new issues encountered
- [ ] Validate all links and references (no 404s)
- [ ] Update platform support matrix if platforms added/removed
- [ ] Sync README with any new tools or removed tools

**Documentation Updates:**

- [x] Updated yq version in Directive 013
- [x] Added Windows WSL2 troubleshooting note
- [x] Fixed broken link to assessment document
- [ ] Pending: Add ast-grep advanced patterns guide

```

#### Quarterly Review Checklist Summary

Use this condensed checklist for quick reference:

```markdown
## Quick Quarterly Review Checklist

- [ ] Check for new stable versions of pinned tools
- [ ] Review changelogs for breaking changes
- [ ] Test updates in staging before production
- [ ] Scan for CVEs and security advisories
- [ ] Verify download checksums remain valid
- [ ] Measure setup time and disk usage
- [ ] Review tool usage patterns
- [ ] Update version constants and documentation
- [ ] Complete review log in work/reports/maintenance/
```

### Annual Strategic Review

Conduct a comprehensive assessment once per year:

```markdown
## YYYY Annual Tooling Review

**Date:** [Annual Review Date]  
**Participants:** [Agent(s) and/or Human Stakeholders]  
**Duration:** [Est. 2-3 hours]

### 1. Strategic Assessment

**Tool Portfolio Alignment:**

- [ ] Evaluate current tool set against agent task patterns
  - Are all tools still necessary?
  - Are agents requesting tools not in the portfolio?
  - Do tool capabilities match agent needs?

- [ ] Survey team for tool usage feedback
  ```markdown
  Survey Questions:
  1. Which tools do you use most frequently?
  2. Which tools have you never used?
  3. What tools do you wish were available?
  4. Which tools have caused the most issues?
  ```

- [ ] Assess new tools in ecosystem
    - Research emerging alternatives to current tools
    - Evaluate tools gaining popularity in agent community
    - Consider tools that address current pain points

- [ ] Identify deprecated or unused tools
  ```bash
  # Analyze usage logs (if available)
  grep "command not found" logs/*.log | sort | uniq -c
  
  # Survey agent profiles for tool references
  rg "rg|fd|jq|yq|ast-grep|fzf" agents/*.agent.md
  ```

**Strategic Decisions:**
| Decision | Rationale | Impact |
|----------|-----------|--------|
| Remove fzf | <5% usage, interactive mode rarely used | -15MB disk |
| Add sd (find/replace) | Agents frequently use sed, sd is safer | +8MB disk |
| Keep ast-grep | 40% task usage, no good alternative | No change |

### 2. Ecosystem Analysis

**Derivative Repository Adoption:**

- [ ] Calculate adoption rate across derivative repos
  ```bash
  # Count repos using tooling setup
  # (Requires access to derivative repositories)
  TOTAL_REPOS=20
  ADOPTING_REPOS=12
  ADOPTION_RATE=$((ADOPTING_REPOS * 100 / TOTAL_REPOS))
  echo "Adoption rate: ${ADOPTION_RATE}%"
  ```

- [ ] Analyze cross-repository tool usage patterns
    - Which tools are universally adopted?
    - Which tools are customized per repository?
    - Are there repository-type patterns? (e.g., backend vs. frontend)

- [ ] Identify common customizations
    - Tool version differences
    - Platform-specific additions
    - Optional tool variations

  **Insight:** If >50% of derivatives customize the same aspect, consider standardizing

- [ ] Calculate actual ROI vs. projected
  ```markdown
  ## ROI Calculation
  
  **Projected (1 year ago):**
  - Time saved per repo: 20 hours/year
  - Repos using setup: 15
  - Total savings: 300 hours/year
  
  **Actual:**
  - Time saved per repo: 24 hours/year (measured)
  - Repos using setup: 12
  - Total savings: 288 hours/year
  
  **Assessment:** On target (96% of projection)
  ```

**Ecosystem Insights:**

- Adoption lower than projected (12 vs. 15 repos)
- Time savings higher than projected (+20%)
- Backend repos benefit most (30 hrs/year)
- Frontend repos benefit less (12 hrs/year) - different tooling needs

### 3. Improvement Planning

**Optimization Opportunities:**

- [ ] Prioritize improvements based on usage data
    1. Add Windows WSL support (requested by 4 derivative repos)
    2. Improve ast-grep performance (bottleneck in 30% of tasks)
    3. Add tool version validation pre-flight checks

- [ ] Plan platform expansion
    - Windows native support? (WSL sufficient for now)
    - Container-based environments? (Docker/Podman support)
    - Cloud shell environments? (GCP/AWS CloudShell compatibility)

- [ ] Design next-generation features
    - **Intelligent tool selection:** Auto-detect repository type, install relevant subset
    - **Usage analytics:** Track tool invocation frequency, optimize installations
    - **On-demand installation:** Lazy-load tools only when needed by specific agents

- [ ] Update roadmap
  ```markdown
  ## Tooling Roadmap 2026
  
  **Q1:** Windows WSL2 native support
  **Q2:** Intelligent tool selection based on repo analysis
  **Q3:** Usage analytics dashboard for maintenance insights
  **Q4:** Container-optimized setup for CI/CD environments
  ```

**Investment Priorities:**
| Priority | Item | Effort | Impact | Decision |
|----------|------|--------|--------|----------|
| P0 | Windows WSL support | Medium | High | ✅ Approved |
| P1 | Version validation | Low | Medium | ✅ Approved |
| P2 | Intelligent selection | High | Medium | 🔄 Research phase |
| P3 | Usage analytics | Medium | Low | ⏸️ Deferred |

```

## Integration with Orchestration Framework

The tooling setup integrates with file-based orchestration to eliminate installation overhead and ensure consistent agent execution environments.

### Pre-Task Setup Hook

Configure the orchestration system to verify tooling before task assignment:

```python
# In ${WORKSPACE_ROOT}/scripts/agent_orchestrator.py

def verify_tooling_setup(agent_profile):
    """Verify required tools are available before task assignment."""
    required_tools = agent_profile.get('required_tools', ['rg', 'fd', 'jq'])
    
    missing_tools = []
    for tool in required_tools:
        if not shutil.which(tool):
            missing_tools.append(tool)
    
    if missing_tools:
        log_warning(f"Missing tools for {agent_profile['name']}: {missing_tools}")
        log_info("Run .github/copilot/setup.sh to install required tooling")
        return False
    
    return True

# Before task assignment
if not verify_tooling_setup(agent):
    # Queue task for retry after setup, or escalate
    return TaskStatus.PENDING_SETUP
```

### Task Metadata Enhancement

Record tool availability and versions in task results:

```yaml
# Task result file
result:
  status: completed
  duration_minutes: 18
  tooling_environment:
    rg_version: "13.0.0"
    fd_version: "8.7.0"
    jq_version: "1.6"
    setup_verified: true
    setup_timestamp: "2025-11-27T10:15:00Z"
```

### Performance Tracking

Measure and compare task duration with/without tooling setup:

```markdown
## Orchestration Performance Impact

**Before Tooling Setup:**
- Average task duration: 25 minutes
- Tool installation overhead: 3-5 minutes per task
- Task failures due to tool issues: 8%

**After Tooling Setup:**
- Average task duration: 20 minutes
- Tool installation overhead: 0 minutes (pre-installed)
- Task failures due to tool issues: <1%

**Improvement:**
- 20% faster task execution
- 87% reduction in tool-related failures
- More predictable task duration (reduced variance)
```

### Batch Task Optimization

For orchestrated batch operations, tooling setup provides compounding benefits:

```bash
# Without setup: Each agent installs tools independently
# 10 parallel agents × 3 minutes setup = 30 CPU-minutes wasted

# With setup: Tools installed once, shared by all agents
# 1 × 2 minutes setup = 2 CPU-minutes total
# Savings: 28 CPU-minutes per batch (93% reduction)
```

## Troubleshooting Common Issues

### Tool Not Found in PATH

**Symptom:** `command not found: fd` after installation

**Diagnosis:**

```bash
# Check if tool is installed
which fd
# or
command -v fd

# Check PATH
echo $PATH
```

**Solutions:**

1. Add tool location to PATH:
   ```bash
   export PATH="/usr/local/bin:$PATH"
   # Make persistent by adding to ~/.bashrc or ~/.zshrc
   ```

2. Create symlink in PATH directory:
   ```bash
   sudo ln -s /path/to/tool /usr/local/bin/tool
   ```

3. Reload shell configuration:
   ```bash
   source ~/.bashrc  # or ~/.zshrc for zsh
   ```

### Version Conflicts

**Symptom:** Tool behavior differs from expected (API changes, broken scripts)

**Diagnosis:**

```bash
# Check installed version
tool --version

# Compare with documented minimum version
# See Directive 013 for version requirements
```

**Solutions:**

1. Update to compatible version:
   ```bash
   # Remove old version
   sudo apt remove tool  # or brew uninstall tool
   
   # Install pinned version
   # Follow Directive 013 installation instructions
   ```

2. Use fallback tool temporarily:
   ```bash
   # If rg unavailable, use grep
   if ! command -v rg &>/dev/null; then
       alias rg='grep -r'
   fi
   ```

### Platform-Specific Installation Failures

**Symptom:** Installation script fails with platform-specific errors

**Diagnosis:**

```bash
# Identify platform
uname -s
lsb_release -a  # Linux
sw_vers  # macOS

# Check error logs
tail -n 50 /var/log/setup-errors.log
```

**Solutions:**

For **Debian/Ubuntu fd-find issue:**

```bash
# fdfind binary, not fd
sudo apt install fd-find
sudo ln -s $(which fdfind) /usr/local/bin/fd
```

For **macOS Homebrew path issue:**

```bash
# Initialize Homebrew environment
if [[ -f /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi
```

For **Permission denied errors:**

```bash
# Ensure correct ownership
sudo chown -R $USER:$USER /usr/local/bin

# Or install to user directory
mkdir -p ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"
# Install tools to ~/.local/bin instead
```

### Checksum Verification Failures

**Symptom:** SHA256 checksum mismatch during binary download

**Diagnosis:**

```bash
# Download failed or file corrupted
sha256sum downloaded_file
# Compare with published checksum
```

**Solutions:**

1. Re-download from official source:
   ```bash
   rm downloaded_file
   wget https://official-source/tool-binary
   sha256sum tool-binary  # Verify again
   ```

2. Check for updated checksums:
   ```bash
   # Visit release page
   # https://github.com/tool/releases/tag/vX.Y.Z
   # Copy correct SHA256 value
   ```

3. If persistent, escalate security concern:
   ```markdown
   ⚠️ Unable to verify binary authenticity for [tool]
   - Source: [URL]
   - Expected SHA256: [checksum]
   - Actual SHA256: [checksum]
   - Recommend manual investigation before proceeding
   ```

## Best Practices Summary

### Quick Reference Checklist

Use this for rapid validation of tooling setup decisions:

```markdown
## Tooling Setup Validation

**Tool Selection:**
- [ ] Tool usage frequency justifies inclusion (>50% of tasks)
- [ ] Performance improvement >2x over fallback
- [ ] Active maintenance (commits in last 6 months)
- [ ] Security verified (checksums, no CVEs)

**Configuration:**
- [ ] Version pinning strategy documented
- [ ] Error handling appropriate (critical vs. optional)
- [ ] Platform quirks addressed
- [ ] Verification steps included

**Maintenance:**
- [ ] Quarterly review scheduled
- [ ] Annual strategic review scheduled
- [ ] Documentation sync process defined
- [ ] Troubleshooting guide available

**Integration:**
- [ ] Orchestration framework awareness
- [ ] Pre-task verification hook
- [ ] Performance metrics tracked
- [ ] Task metadata enhanced

**Documentation:**
- [ ] Installation in Directive 013
- [ ] Usage patterns in Directive 001
- [ ] Approach documented here
- [ ] Cross-references validated
```

### Key Success Factors

1. **Measurable Criteria:** Base all decisions on data (usage frequency, performance gains, security posture)
2. **Graceful Degradation:** Always provide fallback strategies; tools enhance but don't block agent operation
3. **Proactive Maintenance:** Schedule regular reviews; don't wait for tools to break
4. **Clear Documentation:** Keep Directive 013, Directive 001, and this approach synchronized
5. **Platform Awareness:** Handle quirks explicitly; test on all target platforms
6. **Security First:** Verify checksums, audit CVEs, use official channels exclusively

## Related Resources

- **Directive 001:** [CLI & Shell Tooling](./../directives/001_cli_shell_tooling.md) — Detailed tool usage patterns
- **Directive 013:** [Tooling Setup & Fallbacks](./../directives/013_tooling_setup.md) — Installation instructions
- **Directive 011:** [Risk & Escalation](./../directives/011_risk_escalation.md) — How to escalate tool unavailability
- **Directive 017 (TDD):** Testing Requirements (Directive 016, 017)
- **Assessment:
  ** [Copilot Tooling Value Assessment](../../../work/reports/logs/architect/2025-11-24-copilot-tooling-value-assessment.md) — Data-driven analysis supporting these practices

---

_Version: 1.0.0_  
_Author: Editor Eddy (via Copilot)_  
_Last Updated: 2025-11-27_  
_Status: Active_
