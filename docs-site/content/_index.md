---
title: "Quickstart Agent-Augmented Development Framework"
type: docs
---

# Welcome to the Quickstart Framework

**Transform your development workflow with AI-powered agents**

The Quickstart Agent-Augmented Development Framework provides a comprehensive, production-ready foundation for integrating AI agents into your software development process. Whether you're automating documentation, orchestrating multi-agent workflows, or building custom development tools, this framework gives you the structure and patterns you need to succeed.

---

## 🎯 What You Can Do

### For New Users

**🚀 Get Started Quickly**  
Go from zero to your first agent task in under 30 minutes. Our quickstart guide walks you through installation, configuration, and your first AI-augmented workflow.  
[Get Started →](/getting-started/)

**📚 Learn the Concepts**  
Understand agent profiles, task orchestration, file-based coordination, and the architectural patterns that make agent-augmented development scalable.  
[Core Concepts →](/getting-started/#concepts)

**🎓 Follow Tutorials**  
Hands-on tutorials guide you through common scenarios: documentation generation, code refactoring, CI/CD integration, and multi-agent orchestration.  
[Tutorials →](/guides/)

---

### For Active Users

**🔧 Integrate with Your Tools**  
Connect agents to your CI/CD pipelines, GitHub workflows, IDE extensions, and existing development tools. Comprehensive guides for GitHub Actions, Claude Code, and custom integrations.  
[Integration Guides →](/guides/)

**🤝 Orchestrate Multiple Agents**  
Coordinate specialized agents (architects, developers, testers, writers) to work together on complex tasks with file-based async coordination patterns.  
[Multi-Agent Orchestration →](/guides/multi-agent-orchestration/)

**🎨 Create Custom Agents**  
Build agent profiles tailored to your workflow. Learn how to define capabilities, responsibilities, decision frameworks, and collaboration contracts.  
[Agent Creation Guide →](/guides/creating-agents/)

---

### For Process Architects

**🏗️ Explore Architecture**  
Deep dive into architectural decisions, design patterns, and the philosophy behind agent-augmented development. Understand trade-offs and governance models.  
[Architecture Docs →](/architecture/)

**📋 Review ADRs**  
Architecture Decision Records document key design choices: modular directives, file-based coordination, token economy, versioning, and separated metadata.  
[ADRs →](/architecture/adrs/)

**📐 Apply Patterns**  
Reusable patterns for common scenarios: task decomposition, context management, validation workflows, and agent specialization.  
[Design Patterns →](/architecture/patterns/)

---

## ✨ Key Features

**🤖 Specialized Agent Profiles**  
Pre-built agent profiles for common roles: Architect, Developer, Tester, Writer, Curator, Build Automation. Each agent has clear responsibilities, capabilities, and collaboration patterns.

**📁 File-Based Coordination**  
Async, auditable coordination between agents using Git-tracked work files. No complex orchestration server required—just files, Git, and clear conventions.

**🔄 CI/CD Integration**  
Native GitHub Actions workflows, validation pipelines, and automated quality checks. Agents integrate seamlessly into your existing development workflow.

**📊 Traceable Decisions**  
Every architectural decision, design choice, and trade-off documented in ADRs. Full transparency and context for understanding why things are the way they are.

**🧩 Modular & Extensible**  
Add new agents, customize workflows, integrate with your tools. The framework provides structure without lock-in—adapt it to your needs.

**🎯 Token-Efficient Design**  
Optimized for AI agent context windows. Modular directives, separated metadata (optional), and clear documentation structure minimize token overhead.

---

## 🚦 Choose Your Path

### I'm New Here

**Start Here**: [Quickstart Guide](/getting-started/) (5 minutes)

1. **Install the framework** in your repository
2. **Run your first agent task** (documentation generation)
3. **Understand agent profiles** and how agents collaborate
4. **Explore next steps**: CI/CD integration, custom agents, advanced patterns

---

### I'm Exploring Options

**Evaluating the framework?** Here's what to review:

- **[Executive Summary](/about/#executive-summary)**: High-level overview, benefits, ROI
- **[Architecture Vision](/architecture/)**: Philosophy, design principles, trade-offs
- **[Use Cases](/guides/#use-cases)**: Real-world scenarios and success stories
- **[FAQ](/about/#faq)**: Common questions and answers

---

### I'm Implementing

**Ready to integrate?** Here's your roadmap:

1. **[Installation Guide](/getting-started/installation/)**: Set up in your repository
2. **[CI/CD Integration](/guides/ci-orchestration/)**: Automate with GitHub Actions
3. **[Agent Customization](/guides/creating-agents/)**: Tailor agents to your workflow
4. **[Multi-Agent Orchestration](/guides/multi-agent-orchestration/)**: Coordinate complex tasks
5. **[Best Practices](/guides/#best-practices)**: Patterns, anti-patterns, lessons learned

---

## 🎓 Learning Resources

### Documentation

- **[How-To Guides](/guides/)**: Task-oriented step-by-step instructions (19 guides)
- **[Troubleshooting](/guides/#troubleshooting)**: Common issues and solutions
- **[Reference](/reference/)**: Agent profiles, configuration options, glossary
- **[Architecture](/architecture/)**: Deep dives, ADRs, design patterns

### Community

- **GitHub Repository**: [sd-development/quickstart](https://github.com/sd-development/quickstart_agent-augmented-development)
- **Issues & Discussions**: Report bugs, request features, ask questions
- **Contributing**: [How to Contribute](/contributing/)

---

## 💡 Core Concepts (Quick Primer)

### Agent Profiles

**Specialized agents** with clear roles, capabilities, and responsibilities:

- **Architect Alphonso**: System design, architecture decisions, ADRs
- **Developer Dan**: Code implementation, testing, refactoring
- **Tester Tina**: Test strategy, test generation, mutation testing
- **Writer Wendy**: Documentation, user guides, content clarity
- **Curator Clara**: Repository organization, metadata management
- **Build Buddy**: CI/CD automation, deployment pipelines

Each agent has a **profile file** (`.github/agents/*.agent.md`) defining their behavior, collaboration contract, and decision-making framework.

### File-Based Coordination

Agents coordinate asynchronously using **work files** (`work/` directory):

- **Task Files**: Request work from other agents
- **Progress Logs**: Track task status and outcomes
- **Coordination Messages**: Async communication between agents
- **Handoff Documents**: Transfer context between agents

All coordination is **Git-tracked**, providing **full audit trail** and **reproducibility**.

### Modular Directives

**Directives** are reusable instructions for agents (`.github/agents/directives/`):

- **001 - CLI & Shell Tooling**: Repository discovery patterns
- **007 - Agent Declaration**: Authority confirmation
- **016 - ATDD**: Acceptance Test-Driven Development
- **017 - TDD**: Test-Driven Development
- **022 - Audience-Oriented Writing**: Persona-aware documentation

Agents load directives on demand with `/require-directive <code>` command.

---

## 🌟 Why Use This Framework?

### For Teams

- **Faster Onboarding**: New team members ramp up with agent-assisted learning
- **Consistent Quality**: Agents enforce standards, patterns, and best practices
- **Reduced Friction**: Automate documentation, testing, and repetitive tasks
- **Knowledge Preservation**: Decisions and context captured in ADRs and work logs

### For Organizations

- **Scalable Adoption**: Start small (1 agent), scale to multi-agent workflows
- **Governance-Ready**: ADRs, decision logs, and traceable changes satisfy audit requirements
- **Customizable**: Adapt agents and workflows to your organizational standards
- **Open Source**: No vendor lock-in; community-driven improvements

### For Individuals

- **Productivity Boost**: Offload tedious tasks to agents (docs, tests, refactoring)
- **Learning Accelerator**: Agents explain concepts, suggest patterns, guide decisions
- **Quality Improvement**: Agents catch mistakes, suggest improvements, enforce TDD
- **Experimentation**: Prototype with agent assistance; iterate faster

---

## 🚀 Next Steps

**[Get Started (5 min) →](/getting-started/)**  
**[Explore Guides →](/guides/)**  
**[Understand Architecture →](/architecture/)**

---

## 📰 Latest Updates

> **🎉 Documentation Site Launched!** (Batch 1 - 2026-01-31)
> 
> This is the initial release of the Quickstart documentation site. Content migration from `docs/HOW_TO_USE` is planned for Batch 2 (coming soon).
> 
> **Current Status**:
> - ✅ Site infrastructure and theme setup
> - ✅ Homepage and navigation structure
> - ⏳ Content migration (Batch 2)
> - ⏳ Tutorials and use cases (Batch 3)
> - ⏳ ADR migration and indexing (Batch 4)
> 
> Stay tuned for updates!

---

## 📞 Support & Contact

**Questions?** Open an issue on GitHub or check the [FAQ](/about/#faq).

**Found a bug?** Report it in [GitHub Issues](https://github.com/sd-development/quickstart/issues).

**Want to contribute?** See [Contributing Guide](/contributing/).

---

_Quickstart Agent-Augmented Development Framework · Version 1.0.0 · Licensed under MIT_
