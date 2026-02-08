# Model Context Protocol (MCP) Server Setup Guide

**Version:** 1.0.0  
**Last Updated:** 2026-01-31  
**Reference:** [GitHub Docs - Enhance Agent Mode with MCP](https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/enhance-agent-mode-with-mcp)  
**Audience:** Repository maintainers and developers configuring GitHub Copilot with MCP servers

## Purpose

This guide explains how to configure Model Context Protocol (MCP) servers to enhance GitHub Copilot's capabilities with external tools, data sources, and integrations. MCP servers extend Copilot's context and enable it to interact with systems beyond the local repository.

## What is MCP?

The Model Context Protocol (MCP) is an open standard that enables AI assistants like GitHub Copilot to connect to external tools and data sources. MCP servers act as bridges between the AI and external systems, providing:

- **Extended Context**: Access to external documentation, APIs, databases
- **Tool Integration**: Execute commands, query systems, trigger workflows
- **Data Sources**: Fetch real-time information from various services
- **Custom Capabilities**: Implement domain-specific functionality

## Benefits for Agent-Augmented Development

### 1. Enhanced Context Awareness
- Access to external documentation and knowledge bases
- Real-time data from APIs and services
- Integration with project management tools (GitHub Issues, Projects)
- Connection to organizational wikis and documentation

### 2. Automated Workflow Integration
- Trigger CI/CD pipelines
- Create and update issues automatically
- Query build status and test results
- Access deployment information

### 3. Domain-Specific Extensions
- Custom tools for your technology stack
- Integration with internal systems
- Access to proprietary data sources
- Specialized code analysis tools

## Recommended MCP Servers

### Core MCP Servers for Agentic Development

#### 1. **GitHub MCP Server**
**Purpose:** Access GitHub repositories, issues, pull requests, and workflows

**Capabilities:**
- Read and search repository contents
- Query issues and pull requests
- Trigger GitHub Actions workflows
- Access commit history and diffs
- Manage labels and milestones

**Installation:**
```bash
npm install -g @modelcontextprotocol/server-github
```

**Configuration:**
```json
{
  "mcpServers": {
    "github": {
      "command": "mcp-server-github",
      "env": {
        "GITHUB_TOKEN": "YOUR_GITHUB_TOKEN"
      }
    }
  }
}
```

**Use Cases:**
- Cross-repository code search
- Automated issue tracking
- PR review automation
- Workflow orchestration

#### 2. **Filesystem MCP Server**
**Purpose:** Enhanced file system operations beyond basic read/write

**Capabilities:**
- Advanced file searching
- Batch file operations
- Directory structure analysis
- File metadata queries
- Pattern-based file manipulation

**Installation:**
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

**Configuration:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["--allowed-directories", "/path/to/repos"]
    }
  }
}
```

**Use Cases:**
- Large-scale refactoring
- Code migration tasks
- Repository structure analysis
- Batch documentation updates

#### 3. **Git MCP Server**
**Purpose:** Advanced Git operations and history analysis

**Capabilities:**
- Complex git log queries
- Branch comparison
- Commit history analysis
- Blame and authorship tracking
- Advanced merge operations

**Installation:**
```bash
npm install -g @modelcontextprotocol/server-git
```

**Configuration:**
```json
{
  "mcpServers": {
    "git": {
      "command": "mcp-server-git"
    }
  }
}
```

**Use Cases:**
- Tracing code changes
- Analyzing contribution patterns
- Identifying related changes
- Historical context for decisions

### Optional MCP Servers for Enhanced Capabilities

#### 4. **Postgres/Database MCP Server**
**Purpose:** Database query and schema analysis

**Use Cases:**
- Schema migration planning
- Query optimization
- Data analysis
- Database documentation

#### 5. **Slack MCP Server**
**Purpose:** Team communication integration

**Use Cases:**
- Notify team of task completion
- Query historical decisions from Slack
- Coordinate agent handoffs via Slack
- Status updates to channels

#### 6. **Web Search MCP Server**
**Purpose:** Access to web search results for current information

**Use Cases:**
- Research latest best practices
- Find relevant documentation
- Discover similar projects
- Stay current with technology trends

## Configuration for GitHub Copilot

### Step 1: Create MCP Configuration File

GitHub Copilot looks for MCP server configuration in `.github/copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "--allowed-directories",
        "${REPOSITORY_ROOT}"
      ]
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    }
  }
}
```

### Step 2: Set Up Environment Variables

For security, use environment variables for sensitive data:

```bash
# In your .env file (DO NOT COMMIT)
GITHUB_TOKEN=ghp_your_github_personal_access_token
```

### Step 3: Install MCP Server Dependencies

Update `.github/copilot/setup.sh` to install MCP server packages:

```bash
# Install Node.js if not present (required for npm-based MCP servers)
if ! command_exists node; then
    log_info "Installing Node.js..."
    if [[ "$OS_TYPE" == "linux" ]]; then
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
        sudo apt-get install -y nodejs
    elif [[ "$OS_TYPE" == "macos" ]]; then
        brew install node
    fi
fi

# Pre-install common MCP servers for faster startup
log_info "Installing MCP servers..."
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-git
```

### Step 4: Verify MCP Server Availability

Add verification to setup script:

```bash
# Verify MCP servers
log_info "Verifying MCP servers..."
if npm list -g @modelcontextprotocol/server-github >/dev/null 2>&1; then
    log_success "GitHub MCP server available"
else
    log_warning "GitHub MCP server not installed"
fi
```

## Security Considerations

### Token Management
- ⚠️ **NEVER commit tokens to Git**
- Use environment variables for all sensitive data
- Rotate tokens regularly (quarterly minimum)
- Use tokens with minimal required permissions
- Consider using GitHub Apps for better security

### Access Control
- Restrict filesystem access to repository directories only
- Use read-only tokens where possible
- Implement rate limiting for external API calls
- Monitor MCP server usage for anomalies

### Best Practices
- Document all MCP server configurations
- Review MCP server permissions regularly
- Test MCP servers in development before production
- Keep MCP server packages updated
- Log MCP server activity for audit trails

## Usage Examples

### Example 1: Cross-Repository Code Search

```
@copilot search for authentication patterns across all my repositories using the GitHub MCP server
```

The GitHub MCP server enables Copilot to:
1. List your accessible repositories
2. Search code across all repos
3. Identify common patterns
4. Suggest consolidation opportunities

### Example 2: Automated Issue Creation

```
@copilot analyze this code for TODO comments and create GitHub issues for each using the GitHub MCP server
```

The agent can:
1. Search for TODO patterns
2. Extract context around each TODO
3. Create issues with proper descriptions
4. Link issues to source code locations

### Example 3: Git History Analysis

```
@copilot using the Git MCP server, show me how the authentication module evolved over the last 6 months
```

The Git MCP server provides:
1. Filtered commit history
2. Code evolution analysis
3. Contributor patterns
4. Decision context from commit messages

## Integration with File-Based Orchestration

MCP servers enhance the file-based orchestration workflow:

### Task Assignment
- Agents can query GitHub Issues to create tasks
- Automatic task creation from project boards
- Pull metadata from external systems

### Context Enrichment
- Fetch related documentation automatically
- Pull historical decisions from wikis
- Access external knowledge bases

### Workflow Automation
- Trigger CI/CD on task completion
- Update issue status automatically
- Notify stakeholders via Slack

### Metrics Collection
- Track task execution times
- Monitor agent performance
- Analyze orchestration patterns

## Troubleshooting

### MCP Server Not Found
**Problem:** Copilot cannot locate MCP server
**Solution:**
1. Verify server is installed: `npm list -g @modelcontextprotocol/server-*`
2. Check PATH includes global npm bin directory
3. Try absolute path in configuration

### Authentication Failures
**Problem:** MCP server returns 401/403 errors
**Solution:**
1. Verify GITHUB_TOKEN is valid
2. Check token permissions/scopes
3. Regenerate token if expired
4. Ensure token is not rate-limited

### Performance Issues
**Problem:** MCP operations are slow
**Solution:**
1. Reduce scope of queries
2. Implement caching where possible
3. Use more specific search criteria
4. Consider local MCP server implementations

### Configuration Not Loaded
**Problem:** Changes to mcp-config.json not taking effect
**Solution:**
1. Verify file is at `.github/copilot/mcp-config.json`
2. Check JSON syntax is valid
3. Restart Copilot session
4. Clear Copilot cache if necessary

## Performance Optimization

### Caching Strategy
- Cache frequently accessed data locally
- Implement TTL for cached items
- Invalidate cache on relevant events
- Balance freshness vs. performance

### Request Batching
- Combine multiple queries when possible
- Use bulk operations for efficiency
- Implement request queuing
- Respect rate limits

### Lazy Loading
- Load MCP servers on-demand
- Initialize only required servers
- Defer expensive operations
- Progressive data fetching

## Maintenance

### Regular Reviews
- **Monthly**: Check for MCP server updates
- **Quarterly**: Review token permissions
- **Quarterly**: Audit usage patterns
- **Annually**: Reassess MCP server portfolio

### Update Strategy
1. Test updates in development environment
2. Review changelogs for breaking changes
3. Update one server at a time
4. Monitor for issues post-update
5. Keep rollback plan ready

## Advanced Configuration

### Custom MCP Server Development

For organization-specific needs, develop custom MCP servers:

```typescript
// Example: Custom documentation MCP server
import { MCPServer } from '@modelcontextprotocol/sdk';

const server = new MCPServer({
  name: 'company-docs',
  version: '1.0.0',
  capabilities: ['search', 'read']
});

server.registerTool('search-docs', async (query) => {
  // Implementation for searching company docs
  return await searchInternalDocs(query);
});
```

### Multi-Environment Configuration

Support different configurations per environment:

```json
// .github/copilot/mcp-config.development.json
{
  "mcpServers": {
    "github": {
      "env": {
        "GITHUB_TOKEN": "${DEV_GITHUB_TOKEN}",
        "GITHUB_API_URL": "https://github.company.dev"
      }
    }
  }
}
```

## Related Documentation

- [GitHub Copilot Custom Instructions](.github/copilot-instructions.md)
- [Copilot Tooling Setup Guide](copilot-tooling-setup.md)
- [ADR-010: GitHub Copilot Environment Tooling](../architecture/adrs/ADR-010-github-copilot-tooling-setup.md)
- [Directive 001: CLI & Shell Tooling](../.github/agents/directives/001_cli_shell_tooling.md)
- [GitHub Docs: MCP Tutorial](https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/enhance-agent-mode-with-mcp)

---

**Maintained by:** Architect Alphonso  
**Next Review:** 2026-04-30 (Quarterly)  
**Version:** 1.0.0
