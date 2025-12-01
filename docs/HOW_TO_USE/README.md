---
packaged: true
audiences: [user, software_engineer, devops_engineer, process_architect]
note: Practical guides for using the AI-augmented development framework and multi-agent orchestration system.
---

# How To Use Documentation

This directory contains practical guides for using the AI-augmented development framework and multi-agent orchestration system.

## Getting Started

**New to this repository?** Start here:

1. **[QUICKSTART.md](QUICKSTART.md)** - Initial setup and configuration guide
   - Customize project vision and guidelines
   - Configure agent specialists
   - Understand directory structure

## Core Guides

### Agent Development & Orchestration

- **[creating-agents.md](creating-agents.md)** - Agent development lifecycle
  - Creating new specialist agents
  - Agent profile structure
  - Capability definitions

- **[multi-agent-orchestration.md](multi-agent-orchestration.md)** - Multi-agent coordination system
  - File-based orchestration patterns
  - Task lifecycle management
  - Agent handoff protocols

### Testing & Quality

- **[testing-orchestration.md](testing-orchestration.md)** - Testing strategies for orchestrated workflows
  - E2E orchestration testing
  - Task validation
  - Quality metrics

### Automation & CI/CD

- **[ci-orchestration.md](ci-orchestration.md)** - CI/CD integration patterns
  - GitHub Actions workflows
  - Automated orchestration
  - Continuous validation

### Development Environment

- **[python-setup.md](python-setup.md)** - Python development environment setup
  - Virtual environment creation and management
  - Dependency installation
  - Testing and validation
  - Troubleshooting guide

- **[copilot-tooling-setup.md](copilot-tooling-setup.md)** - CLI tooling setup for GitHub Copilot
  - Installing ripgrep, fd, ast-grep
  - jq, yq, fzf configuration
  - Tool usage patterns

### GitHub Integration

- **[ISSUE_TEMPLATES_GUIDE.md](ISSUE_TEMPLATES_GUIDE.md)** - Using GitHub issue templates
  - Agent-specific issue templates
  - Task creation workflows
  - Issue label conventions

## User Journey

### For New Users

1. Read [QUICKSTART.md](QUICKSTART.md)
2. Set up Python environment with [python-setup.md](python-setup.md)
3. Review [creating-agents.md](creating-agents.md) to understand agent concepts
4. Explore [ISSUE_TEMPLATES_GUIDE.md](ISSUE_TEMPLATES_GUIDE.md) for task submission

### For Agent Developers

1. Set up development environment with [python-setup.md](python-setup.md)
2. Study [creating-agents.md](creating-agents.md)
3. Understand [multi-agent-orchestration.md](multi-agent-orchestration.md)
4. Implement testing per [testing-orchestration.md](testing-orchestration.md)

### For DevOps/Automation Engineers

1. Set up Python environment with [python-setup.md](python-setup.md)
2. Review [ci-orchestration.md](ci-orchestration.md)
3. Configure [copilot-tooling-setup.md](copilot-tooling-setup.md)
4. Understand orchestration patterns in [multi-agent-orchestration.md](multi-agent-orchestration.md)

## Related Documentation

- **Architecture:** [../architecture/README.md](../architecture/README.md)
- **Templates:** [../templates/README.md](../templates/README.md)
- **Vision & Guidelines:** [../VISION.md](../VISION.md), [../specific_guidelines.md](../specific_guidelines.md)
- **Repository Map:** [../../REPO_MAP.md](../../REPO_MAP.md)

## Contributing

When adding new guides to this directory:

1. Follow the existing document structure
2. Include practical examples
3. Link to related ADRs and architecture docs
4. Update this README index
5. Add cross-references from related documents

---

_This index ensures discoverability of practical guides for framework users_
