---
title: "Getting Started"
weight: 1
bookCollapseSection: false
---

# Getting Started with Quickstart Framework

Welcome! This section will help you get up and running with the Quickstart Agent-Augmented Development Framework in under 30 minutes.

## Quick Navigation

**⚡ Quickstart (5 min)**  
Get your first agent task running immediately. Perfect if you want to see the framework in action before diving deeper.  
[Start Now →](#quickstart)

**📦 Installation**  
Complete installation instructions for various platforms and environments. Includes prerequisites, setup scripts, and verification steps.  
[Installation Guide →](#installation)

**🧠 Core Concepts**  
Understand the key concepts: agent profiles, file-based coordination, directives, and task orchestration.  
[Learn Concepts →](#concepts)

---

## Quickstart (5 minutes)

**Goal**: Run your first AI-augmented task using the framework.

### Prerequisites

- Git installed
- GitHub account
- AI assistant (Claude, GitHub Copilot, etc.)

### Steps

**1. Clone or Fork the Repository**

```bash
# Clone the quickstart template
git clone https://github.com/sddevelopment-be/quickstart_agent-augmented-development.git
cd quickstart_agent-augmented-development

# Or fork on GitHub and clone your fork
```

**2. Explore the Structure**

```bash
# View agent profiles
ls .github/agents/

# View documentation
ls docs/

# View work directory (agent coordination)
ls work/
```

**3. Attach Your AI Assistant**

- **Claude Desktop / Claude Code**: Open the repository
- **GitHub Copilot**: Open in VS Code with Copilot Chat
- **Cursor**: Open repository in Cursor IDE

**4. Give Your First Agent Task**

Instruct your AI assistant:

> "Read `.github/agents/bootstrap.md` first, then tell me when you're ready. After that, I want you to act as Writer Wendy and create a brief summary of this repository's purpose in `work/summaries/repo-overview.md`."

**5. Review the Output**

Check `work/summaries/repo-overview.md` for the agent-generated summary.

**✅ Success!** You've completed your first agent-augmented task.

---

## Installation

### Option 1: Download Latest Release (Recommended)

**For downstream projects:** Download the packaged framework from GitHub Releases.

```bash
# Download and install the latest release
curl -fsSL https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/latest/download/deploy_framework.sh | bash

# Or install a specific version
curl -fsSL https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/latest/download/deploy_framework.sh | bash -s -- --version 1.0.0
```

**Manual download:**
1. Visit [GitHub Releases](https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/latest)
2. Download `quickstart-framework-X.Y.Z.zip`
3. Extract to your project root
4. Run the included installation script

### Option 2: Clone Repository (For Development)

**For contributing or customizing:** Clone the full repository.

```bash
# Clone the repository
git clone https://github.com/sddevelopment-be/quickstart_agent-augmented-development.git
cd quickstart_agent-augmented-development

# Initialize submodules (if any)
git submodule update --init --recursive
```

### Post-Installation Steps

1. **Customize for your project:**
   - Edit `docs/VISION.md` with your project goals
   - Review agent profiles in `.github/agents/`
   - Adjust workflows in `.github/workflows/`

2. **Verify installation:**
   ```bash
   # Check framework files are present
   ls .github/agents/
   ls docs/
   ```

3. **(Optional) Deploy to AI assistants:**
   ```bash
   npm install
   npm run deploy:claude:prompts  # Deploy to Claude Code
   npm run deploy:copilot         # Deploy to GitHub Copilot
   ```

For complete installation instructions, see [`docs/HOW_TO_USE/framework_install.md`](https://github.com/sddevelopment-be/quickstart_agent-augmented-development/blob/main/docs/HOW_TO_USE/framework_install.md).

---

## Core Concepts

_Comprehensive concepts guide coming in Batch 2._

**Preview**: Key concepts to understand:

### Agent Profiles

Each agent has a profile defining:
- **Purpose**: What the agent specializes in
- **Capabilities**: What the agent can do
- **Responsibilities**: What the agent should focus on
- **Collaboration Contract**: How the agent works with others

### File-Based Coordination

Agents communicate via files:
- `work/tasks/`: Task requests
- `work/progress/`: Status updates
- `work/analysis/`: Research and analysis outputs
- `output/`: Final artifacts

### Directives

Modular instructions loaded on demand:
- Stored in `.github/agents/directives/`
- Referenced by code (e.g., `007_agent_declaration.md`)
- Loaded with `/require-directive <code>`

### Workflows

Common workflows:
1. **Single Agent**: Simple task with one agent
2. **Sequential Handoff**: Agent A completes task, hands off to Agent B
3. **Parallel Work**: Multiple agents work independently, merge results
4. **Collaborative**: Multiple agents refine work iteratively

---

## What's Next?

**After Quickstart**:
- [Explore How-To Guides]({{< relref "/guides" >}}) (19 comprehensive guides)
- [Understand Architecture]({{< relref "/architecture" >}}) (design decisions and patterns)
- [Create Custom Agents](guides/creating-agents/) (tailor to your workflow)
- [Integrate with CI/CD](guides/ci-orchestration/) (automate with GitHub Actions)

---

_This section is under active development. Content from `docs/HOW_TO_USE/QUICKSTART.md` will be migrated in Batch 2._
