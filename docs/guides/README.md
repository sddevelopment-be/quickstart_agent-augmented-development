# Guides

**Purpose:** User-facing guides for using the agent-augmented development framework  
**Audience:** All users - from first-time setup to advanced optimization

---

## Directory Structure

This directory contains all operational guides organized by user experience level:

```
docs/guides/
├── quickstart/     # Getting started guides for new users
├── technical/      # Setup, deployment, and integration guides
├── advanced/       # Optimization, orchestration, and deep topics
└── README.md       # This file
```

---

## Quick Navigation

### 🚀 Quickstart (New Users Start Here)

First-time setup and basic workflows:

- **[QUICKSTART.md](quickstart/QUICKSTART.md)** - 5-minute getting started guide
- **[User Guide: Installation](quickstart/user-guide-installation.md)** - Step-by-step first install
- **[User Guide: Upgrade](quickstart/user-guide-upgrade.md)** - Upgrading existing installations
- **[User Guide: Distribution](quickstart/user-guide-distribution.md)** - Distributing the framework
- **[Dashboard Quickstart](quickstart/dashboard-quickstart.md)** - Real-time monitoring setup
- **[Mutation Testing Quickstart](quickstart/mutation-testing-quickstart.md)** - Test quality validation
- **[Creating Agents](quickstart/creating-agents.md)** - Build custom specialist agents
- **[Template-Based Configuration](quickstart/template-based-configuration.md)** - Config generation
- **[Issue Templates Guide](quickstart/ISSUE_TEMPLATES_GUIDE.md)** - GitHub issue automation

### 🔧 Technical (Setup & Integration)

Infrastructure, deployment, and tool setup:

- **[Framework Installation](technical/framework_install.md)** - Technical installation details
- **[Python Setup](technical/python-setup.md)** - Python environment configuration
- **[Copilot Tooling Setup](technical/copilot-tooling-setup.md)** - GitHub Copilot integration
- **[Claude Deployment](technical/claude-deployment-guide.md)** - Claude Desktop integration
- **[MCP Server Setup](technical/mcp-server-setup.md)** - Model Context Protocol servers
- **[CI Validation Guide](technical/ci-validation-guide.md)** - Continuous integration setup
- **[GitHub Workflows](technical/github_workflows.md)** - GitHub Actions configuration

### ⚡ Advanced (Optimization & Orchestration)

Performance, coordination, and advanced workflows:

- **[Multi-Agent Orchestration](advanced/multi-agent-orchestration.md)** - Coordinating agent workflows
- **[Context Optimization](advanced/context-optimization-guide.md)** - Token efficiency strategies
- **[Prompt Optimization](advanced/prompt-optimization-quick-reference.md)** - Effective prompting
- **[Prompt Validation](advanced/prompt-validation-guide.md)** - Quality assurance for prompts
- **[Release & Upgrade](advanced/release_and_upgrade.md)** - Production deployment workflows
- **[Testing Orchestration](advanced/testing-orchestration.md)** - Automated testing coordination
- **[CI Orchestration](advanced/ci-orchestration.md)** - Advanced CI/CD patterns

---

## Additional Resources

**Framework Core:**
- [Architecture Documentation](../architecture/) - ADRs, diagrams, reviews
- [Templates](../templates/) - Reusable artifact templates
- [Audience Personas](../audience/) - Target user profiles

**Reference:**
- [Doctrine](../../doctrine/) - Agent guidelines and directives
- [Specifications](../../specifications/) - Feature specifications
- [Work Directory](../../work/) - Active collaboration artifacts

---

## Contributing to Guides

**Guidelines:**
- **Quickstart:** Beginner-friendly, step-by-step, assumes no prior knowledge
- **Technical:** Assumes familiarity with development tools, focuses on integration
- **Advanced:** Assumes deep framework knowledge, focuses on optimization

**Naming Convention:** kebab-case (e.g., `my-guide-name.md`)

**Template:** See [Guide Template](../templates/documentation/guide-template.md) (if exists)

---

**Maintained by:** Writer-Editor, Curator Claire  
**Last Updated:** 2026-02-08  
**Version:** 2.0.0 (Consolidated from docs/guides/ + docs/HOW_TO_USE/)
