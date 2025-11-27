# SD Development: AI-Augmented Workflow Starter Repo

This repository is a starter layout for AI-augmented / agentic workflows.

It gives you:
- A clear place for **agents** and their instructions.
- A space for **repo-specific vision and guidelines**.
- Separate areas for **work-in-progress** and **generated output**.

For further tips and tricks on using AI agents in your projects, take a look at:

- [Augmented Coding Patterns](https://lexler.github.io/augmented-coding-patterns//) by [@lexler](https://github.com/lexler)
- the [Agents.md](https://agents.md/) specification
- [Agent Framework Glossary](agents/GLOSSARY.md) for standardized terminology definitions

## Using this Repository with an AI Agent

When you attach an AI assistant to this repository, you can instruct it to:

1. Read `.github/agents/bootstrap.md` first.
2. Tell you when it's ready to start working.
3. Proceed with your instructions.

* Use `work/` for:
    - progress logs
    - design notes
    - coordination messages to other agents
* Write any generated artifacts (code, documents, reports) to `output/`.
* Never directly modify `docs/` without human approval.

This keeps intent (`docs/`), collaboration (`work/`), and artifacts (`output/`) clearly separated.

## Agent Workflows (example)

> **REPLACE THIS SECTION** with project-specific flows.

- **Design agent** writes initial plans to `work/design-notes.md`.
- **Builder agent** generates code into `output/`.
- **Human** reviews and promotes files from `output/` into tracked source directories.

You can use the specialist agents in `.github/agents/` as a starting point. On github, you can start tasks by using the 'agents panel' (top-right icon) or by assigning a GitHub issue to a specific agent.

![using_agents.png ](using_agents.png)

## Quickstart

1. **Define your intent**
   Edit:
    - [`docs/VISION.md`](docs/VISION.md)
    - [`docs/specific_guidelines.md`](docs/specific_guidelines.md)
2. **Adjust the agents**
    - Read [`.github/agents/QUICKSTART.md`](.github/agents/QUICKSTART.md).
    - Review the generic guidelines in [`.github/agents/general_guidelines.md`](.github/agents/general_guidelines.md).
    - Keep, rename, or remove specialist agents in [`.github/agents/*.agent.md`](agents).
3. **Use the shared spaces**
    - Use [`work/`](work) for notes, progress logs, and coordination between agents and humans.
    - Use [`output/`](output) for generated files that you review and copy into your actual code / content structure.

## Notes

- This repo is designed to be adapted. Feel free to modify the structure as needed.
- By default, everything in work/ is tracked.
  You can adjust [`.gitignore`](./.gitignore) if you want a more ephemeral scratch space.

---

> **REPLACE THIS README WHEN READY!**
> Use this README as a template to create your own project README.




