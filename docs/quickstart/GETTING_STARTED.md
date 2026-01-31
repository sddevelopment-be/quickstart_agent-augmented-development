# Getting Started with the Quickstart Framework

**5-minute setup for the impatient developer**

Welcome! This guide will have you running your first agent-augmented development task in about 5 minutes. If you want more detail, we've got comprehensive guides waiting for you afterward.

## What You're Getting

The Quickstart Agent-Augmented Development Framework gives you:

- **Pre-configured AI agent profiles** for different development tasks
- **Structured workflows** that agents can follow
- **Reusable templates** for documentation, architecture decisions, and work items
- **Quality validation** to keep your work consistent

Think of it as training wheels for working with AI coding assistants—except these training wheels actually make you go faster.

## Prerequisites

Before we begin, make sure you have:

- A POSIX-compliant shell (bash, sh, zsh—you're covered on Linux/macOS/WSL)
- Basic command-line familiarity
- A project repository (or create a new one—we're not picky)
- 5 minutes and a sense of adventure

## Quick Install

### Step 1: Get the Framework

Download the latest release from GitHub:

```bash
# Download the release (replace X.Y.Z with current version)
wget https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/download/vX.Y.Z/quickstart-framework-X.Y.Z.zip

# Or use curl if you prefer
curl -L -O https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/download/vX.Y.Z/quickstart-framework-X.Y.Z.zip
```

### Step 2: Extract and Install

```bash
# Unzip the release
unzip quickstart-framework-*.zip

# Navigate into it
cd quickstart-framework-*

# Install into your project (replace /path/to/your/project)
./scripts/framework_install.sh . /path/to/your/project
```

You'll see something like:

```
ℹ Validating release artifact structure...
ℹ Installing framework files...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework Installation Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Results:
  NEW:      287 files
  SKIPPED:  0 files (already exist)

✓ Installation completed successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 3: Verify It Worked

```bash
cd /path/to/your/project
cat .framework_meta.yml
```

If you see version information, you're good to go! 🎉

## Your First Task

Now that the framework is installed, let's create your first structured work item.

### Create a Task

```bash
cd work
cp templates/TASK_TEMPLATE.md collaboration/my-first-task.md
```

Edit `my-first-task.md` and fill in:

```markdown
---
id: my-first-task
title: Add README badges
status: ACTIVE
priority: MEDIUM
agent: editor-eddy
---

## Context
We need to add status badges to our README to show build status and test coverage.

## Objective
Add CI/CD and coverage badges to README.md

## Success Criteria
- [ ] Build status badge visible
- [ ] Coverage badge visible
- [ ] Badges link to appropriate pages
```

### Work With an Agent

Now when you work with your AI assistant (Claude, Copilot, etc.), reference the agent profile:

```
I have a task in work/collaboration/my-first-task.md. 
Please act as Editor Eddy (see .github/agents/editor-eddy.agent.md) 
and help me complete this task.
```

The agent will:
1. Read the task context
2. Understand its role and constraints
3. Follow the framework's workflows
4. Produce consistent output

### Track Your Progress

As you work, update the task file:

```markdown
## Progress Log

**2026-01-31 10:30** - Located README.md, identified badge services
**2026-01-31 10:45** - Added GitHub Actions badge
**2026-01-31 11:00** - Added Codecov badge, verified links
```

### Complete the Task

When done, update the status:

```markdown
status: COMPLETED
```

## What Just Happened?

You just:

1. ✅ Installed the framework
2. ✅ Created a structured task from a template
3. ✅ Worked with an agent profile
4. ✅ Tracked your work in a standardized way

This pattern scales from small tasks to complex multi-week projects.

## What's in Your Project Now?

After installation, you have:

```
your-project/
├── .github/
│   └── agents/              # AI agent profiles and directives
├── docs/
│   ├── templates/           # Document templates
│   └── architecture/        # ADRs and design docs
├── work/
│   ├── templates/           # Task and analysis templates
│   └── collaboration/       # Your active work (gitignored)
├── framework/               # Python framework modules
├── validation/              # Quality validation scripts
├── AGENTS.md                # Agent coordination protocol
└── .framework_meta.yml      # Installation metadata
```

The framework lives alongside your project code without getting in the way.

## Next Steps

### Learn the Profiles

Explore the agent profiles in `.github/agents/`:

- **devops-danny.agent.md** - CI/CD, infrastructure, deployments
- **editor-eddy.agent.md** - Documentation, writing, clarity
- **architect-anna.agent.md** - System design, ADRs, technical decisions
- **researcher-rachel.agent.md** - Analysis, investigation, research
- And more...

Each profile defines:
- What the agent specializes in
- How it makes decisions
- What it should and shouldn't do

### Try Different Templates

Check out `work/templates/` and `docs/templates/`:

```bash
ls work/templates/
# TASK_TEMPLATE.md
# ANALYSIS_TEMPLATE.md
# MEETING_NOTES_TEMPLATE.md
# ...

ls docs/templates/
# ADR_TEMPLATE.md
# API_DOCUMENTATION_TEMPLATE.md
# ...
```

Each template provides structure for a specific type of work.

### Read the Deep Docs

When you're ready for more detail:

- **[Distribution Guide](../USER_GUIDE_distribution.md)** - What's distributed, profiles, building releases
- **[Installation Guide](../USER_GUIDE_installation.md)** - Deep dive on installation
- **[Upgrade Guide](../USER_GUIDE_upgrade.md)** - Upgrading, conflicts, rollbacks
- **[AGENTS.md](../../AGENTS.md)** - The full agent coordination protocol
- **[Architecture Docs](../architecture/)** - ADRs and technical design

### Customize Your Setup

The framework is designed to be customized:

1. **Add your own agent profiles** in `.github/agents/`
2. **Create custom templates** in `work/templates/` or `docs/templates/`
3. **Put project-specific overrides** in `local/` (never overwritten by upgrades)
4. **Modify workflows** to match your team's process

### Join the Community

- Report issues and request features on GitHub
- Share your custom profiles and templates
- Contribute improvements back to the framework

## Common Questions

### Can I use this with [my favorite AI assistant]?

Yes! The framework is AI-agnostic. It works with:
- Claude (Anthropic)
- GitHub Copilot
- ChatGPT
- Any LLM-based coding assistant

The key is referencing the agent profiles when you start a conversation.

### Will this change my existing project structure?

No. The framework installs alongside your code without modifying it. You're always in control of what files get created and where.

### What if I don't like something?

Customize it! The framework is a starting point, not a straitjacket. Modify profiles, create your own templates, and adapt workflows to your needs.

### Can I uninstall it?

Yes. The framework tracks what it installs in `.framework_meta.yml`. You can remove those files and you're back to where you started.

### Does this work for solo developers?

Absolutely. Even solo developers benefit from structured thinking, consistent documentation, and the ability to "switch hats" between different roles (coding, architecture, DevOps, etc.).

## Tips for Success

**Start small.** Don't try to adopt everything at once. Pick one agent profile and one template type. Get comfortable with those before expanding.

**Reference the agents.** Make it a habit to start conversations with: "Acting as [Agent Name], help me with..."

**Update task files.** Keeping your `work/collaboration/` files current makes it easy to resume work or hand off to others.

**Read the profiles.** The agent profiles contain important context about how to work effectively. Skim them before diving in.

**Experiment!** The framework is designed to be forgiving. Try things. Break things. Learn what works for your style.

## You're Ready!

That's it. You've got the framework installed, you've created your first task, and you know where to go next.

The beauty of structured development is that it scales—from quick 5-minute tasks to multi-month initiatives, from solo work to team collaboration.

Now go build something great. 🚀

---

**Questions?** Check the [comprehensive documentation](../USER_GUIDE_installation.md) or file an issue on GitHub.

**Want to go deeper?** Start with the [Distribution Guide](../USER_GUIDE_distribution.md) to understand what you just installed.
