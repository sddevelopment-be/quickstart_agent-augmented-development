---
title: "Contributing"
weight: 6
bookCollapseSection: false
---

# Contributing to Quickstart Framework

Thank you for your interest in contributing to the Quickstart Agent-Augmented Development Framework!

## 🤝 How to Contribute

### Types of Contributions

We welcome contributions in several areas:

1. **Documentation** - Improve guides, fix typos, add examples
2. **Agent Profiles** - Create new agents or improve existing ones
3. **Directives** - Add new directives or refine existing ones
4. **Code** - Framework scripts, validation tools, automation
5. **Testing** - Test strategies, validation scripts, quality checks
6. **Examples** - Real-world use cases and patterns

---

## 📝 Documentation Contributions

### Docsite Content

This documentation site is built with Hugo and deployed via GitHub Pages.

**Contributing to Docsite**:

1. **Setup**: See [`docs-site/README.md`](/about/docsite-readme/) for local development setup
2. **Content Location**: Edit markdown files in `docs-site/content/`
3. **Preview**: Run `hugo server -D` to preview changes locally
4. **Submit**: Open a pull request with your changes

**Content Guidelines**:
- Use clear, concise language
- Include code examples where helpful
- Test all links before submitting
- Follow existing content structure

### Repository Documentation

**Contributing to `docs/` directory**:

1. **Setup**: Fork and clone the repository
2. **Content Location**: Edit markdown files in `docs/` (not `docs-site/`)
3. **Preview**: View in GitHub or your markdown editor
4. **Submit**: Open a pull request with your changes

---

## 🤖 Agent Profile Contributions

### Creating a New Agent

1. **Define Purpose**: What does this agent specialize in?
2. **Create Profile**: Copy template from `.github/agents/templates/agent-profile.md`
3. **Document Capabilities**: What can this agent do?
4. **Define Collaboration**: How does this agent work with others?
5. **Test**: Try the agent on real tasks
6. **Submit**: Open PR with agent profile in `.github/agents/`

**Example Structure**:
```markdown
# Agent Name

## Purpose
Clear description of agent specialization

## Capabilities
- Capability 1
- Capability 2

## Responsibilities
What the agent should focus on

## Collaboration Contract
How to work with other agents
```

---

## 🧩 Directive Contributions

### Creating a New Directive

1. **Identify Need**: What instruction is frequently repeated?
2. **Create Directive**: Follow template from `.github/agents/directives/template.md`
3. **Assign Code**: Get next available directive code (e.g., 025)
4. **Document Usage**: When and how to load this directive
5. **Test**: Verify directive clarity with multiple agents
6. **Submit**: Open PR with directive in `.github/agents/directives/`

---

## 💻 Code Contributions

### Development Workflow

1. **Fork Repository**: Create your own fork on GitHub
2. **Create Branch**: `git checkout -b feature/your-feature-name`
3. **Make Changes**: Implement your feature or fix
4. **Test**: Run tests, ensure nothing breaks
5. **Commit**: `git commit -m "feat: your feature description"`
6. **Push**: `git push origin feature/your-feature-name`
7. **Pull Request**: Open PR with clear description

### Commit Message Convention

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

**Examples**:
```
feat: add new directive for test automation
fix: correct agent profile typo in architect profile
docs: improve getting started guide clarity
```

---

## 🧪 Testing Contributions

### Test Strategy

- **Unit Tests**: Python tests in `tests/`
- **Validation Scripts**: Shell scripts in `validation/`
- **Agent Testing**: Manual agent workflow validation
- **Documentation Testing**: Link validation, markdown linting

### Running Tests

```bash
# Python tests
pytest

# Validation scripts
./validation/validate-all.sh

# Markdown linting (if configured)
markdownlint docs/
```

---

## 📋 Contribution Guidelines

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on improving the framework
- Help others learn and grow

### Pull Request Process

1. **Description**: Clearly explain what and why
2. **Testing**: Demonstrate that changes work
3. **Documentation**: Update docs if behavior changes
4. **Review**: Address feedback promptly and constructively
5. **Merge**: Maintainers will merge when ready

### Review Criteria

- **Quality**: Code/content meets framework standards
- **Clarity**: Changes are understandable and well-documented
- **Testing**: Changes are validated (manual or automated)
- **Consistency**: Aligns with existing patterns and style

---

## 🎯 Contribution Ideas

Not sure where to start? Here are some ideas:

### Documentation Improvements

- Fix typos or unclear wording
- Add missing code examples
- Improve navigation and cross-linking
- Create video tutorials or screencasts

### Agent Enhancements

- Improve existing agent profiles (clarity, examples)
- Add new specialized agents (e.g., Security Agent, Performance Agent)
- Document agent collaboration patterns

### Framework Features

- Add validation scripts
- Improve testing utilities
- Create IDE integrations
- Build CI/CD templates

### Community

- Answer questions in GitHub Discussions
- Share your use cases and patterns
- Write blog posts about your experience
- Present at meetups or conferences

---

## 📞 Getting Help

**Questions?**
- Open a [GitHub Discussion](https://github.com/sddevelopment-be/quickstart_agent-augmented-development/discussions)
- Check existing [Issues](https://github.com/sddevelopment-be/quickstart_agent-augmented-development/issues)
- Review [documentation](/guides/)

**Found a Bug?**
- Search [existing issues](https://github.com/sddevelopment-be/quickstart_agent-augmented-development/issues)
- Open a new issue with clear reproduction steps
- Include environment details (OS, tools, versions)

**Feature Request?**
- Open a [GitHub Issue](https://github.com/sddevelopment-be/quickstart_agent-augmented-development/issues/new) with `enhancement` label
- Describe use case and expected behavior
- Discuss with maintainers before implementing large features

---

## 🏆 Recognition

Contributors are recognized in:
- Repository contributors list (GitHub)
- Release notes for significant contributions
- `CONTRIBUTORS.md` file (coming soon)

---

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

---

_Thank you for helping make the Quickstart Agent-Augmented Development Framework better for everyone!_
