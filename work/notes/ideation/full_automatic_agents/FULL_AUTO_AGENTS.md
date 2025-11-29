# Full Auto Agents

With the recent work on various agentic MCP servers and SDKs, we can add a layer of automation into the existing file-based orchestration system we have set up.

The idea being to leverage the current python scripts, but add in:

- an API layer to allow users to interact with the agents through simplified prompting
- an agent interaction layer that can call LLM models directly
  - generating prompts
  - calling models/agents through SDKs or APIs ( e.g. OpenAI Agents SDK, LangChain, custom MCP providers, etc)
  - parsing responses and returning them to the user

The existing orchestration system can live in the middle layer, and the user can interact with the agents through the thin API layer. 
In it's simplest form, the API layer would be a simple python interface that delegates to the existing python scripts ( task creation, prompting, logging, etc).
The agent interaction layer would be a wrapper around the LLM model interactions, providing a consistent interface for interacting with different LLM providers and models.

This would allow us to build a fully automated system that can be used by anyone to interact with the agents.
It would also keep the current simplicity of the agents, while providing a more robust and flexible interface for interacting with the agents. (e.g. `call_alphonso(prompt: str)`, `create_task(...)`, `run_iteration()`, `activate_directive()`, `bootstrap()`, `execute_approach(name: str)`, ...).

A secondary CLI-proxy layer could be added to allow users to interact with the agent API through the CLI, providing a familiar and system-agnostic interface.

