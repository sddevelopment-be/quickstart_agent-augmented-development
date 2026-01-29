# Agent Specifications - Tooling-Specific Formats

This directory contains agent specifications converted into multiple tooling-specific optimized formats. These conversions enable different systems and platforms to consume agent specifications in their native format.

## Directory Structure

```
agent-specs/
├── json/          # JSON format for programmatic access and APIs
├── anthropic/     # Anthropic Claude system prompt format
├── openai/        # OpenAI GPT API format
├── yaml/          # YAML configuration for CI/CD pipelines
└── README.md      # This file
```

## Format Descriptions

### JSON Format (`json/`)

**Purpose:** Programmatic access, REST APIs, language-agnostic integration

**Structure:**
```json
{
  "name": "agent-name",
  "description": "Brief description",
  "tools": ["tool1", "tool2", ...],
  "purpose": "Agent purpose",
  "specialization": "Specialization details",
  "collaboration_contract": "Guidelines",
  "mode_defaults": "Operating modes",
  "context_sources": "Context references",
  "directive_references": "Directive table"
}
```

**Use Cases:**
- API endpoints serving agent specifications
- Dynamic agent configuration in applications
- Integration with monitoring/orchestration systems
- Cross-language agent specification consumption

### Anthropic Claude Format (`anthropic/`)

**Purpose:** Direct use with Anthropic's Claude models

**Format:** Plain text system prompt optimized for Claude's context window

**Structure:**
- Header with agent name and description
- Purpose section
- Specialization details
- Collaboration guidelines
- Available tools
- Operating modes

**Use Cases:**
- Direct Claude API integration
- Claude-based agent implementations
- Prompt engineering with Claude models
- Context-optimized Claude deployments

### OpenAI GPT Format (`openai/`)

**Purpose:** Direct use with OpenAI's GPT models

**Structure:**
```json
{
  "model": "gpt-4",
  "messages": [
    {
      "role": "system",
      "content": "Combined agent specification as system prompt"
    }
  ],
  "temperature": 0.7
}
```

**Use Cases:**
- Direct OpenAI API integration
- GPT-based agent implementations
- Chat completion API calls
- Model routing with OpenAI

### YAML Configuration Format (`yaml/`)

**Purpose:** CI/CD pipelines, configuration management, Infrastructure-as-Code

**Structure:**
```yaml
agent:
  name: agent-name
  description: Brief description
  tools: [tool1, tool2, ...]
configuration:
  purpose: Agent purpose
  specialization:
    primary_focus: Main focus area
    secondary_awareness: Secondary areas
    avoid: Things to avoid
context_sources: Context references
```

**Use Cases:**
- GitHub Actions workflow definitions
- Kubernetes ConfigMaps
- Helm chart configurations
- Ansible playbooks
- Docker Compose files

## Generating/Updating Specifications

The specifications are generated from the canonical `.agent.md` files in `.github/agents/` using the conversion script.

### Convert All Agents

```bash
python ops/scripts/convert_agent_specs.py
```

### Convert Specific Agent

```bash
python ops/scripts/convert_agent_specs.py --agent architect.agent.md
```

### Custom Output Directory

```bash
python ops/scripts/convert_agent_specs.py --output-dir /path/to/output
```

### Conversion Script Options

```bash
usage: convert_agent_specs.py [-h] [--input-dir INPUT_DIR] 
                              [--output-dir OUTPUT_DIR] [--agent AGENT]

options:
  --input-dir INPUT_DIR   Directory containing .agent.md files
                         (default: .github/agents)
  --output-dir OUTPUT_DIR Output directory for converted files
                         (default: docs/templates/schemas/agent-specs)
  --agent AGENT          Convert only specific agent
```

## Maintenance

### When to Regenerate

Regenerate specifications when:
- Agent definitions in `.github/agents/*.agent.md` are updated
- New agents are added
- Agent tools or capabilities change
- Directive references are modified

### Automation

Consider adding to CI/CD pipeline to automatically regenerate on agent file changes:

```yaml
name: Update Agent Specifications

on:
  push:
    paths:
      - '.github/agents/*.agent.md'

jobs:
  convert:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Convert specs
        run: python ops/scripts/convert_agent_specs.py
      - name: Commit changes
        run: |
          git config user.name "agent-bot"
          git add docs/templates/schemas/agent-specs/
          git commit -m "Update agent specifications" || true
          git push
```

## Integration Examples

### Python API Integration

```python
import json
from pathlib import Path

# Load agent specification
spec_file = Path("docs/templates/schemas/agent-specs/json/architect.agent.json")
spec = json.loads(spec_file.read_text())

# Use in application
print(f"Agent: {spec['name']}")
print(f"Tools: {', '.join(spec['tools'])}")
```

### Anthropic Claude Integration

```python
import anthropic
from pathlib import Path

# Load Claude-optimized prompt
prompt_file = Path("docs/templates/schemas/agent-specs/anthropic/architect.agent.txt")
system_prompt = prompt_file.read_text()

# Create Claude client
client = anthropic.Anthropic(api_key="your-key")

# Use in conversation
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    system=system_prompt,
    messages=[
        {"role": "user", "content": "Review this architecture..."}
    ]
)
```

### OpenAI GPT Integration

```python
import json
import openai
from pathlib import Path

# Load OpenAI-formatted spec
spec_file = Path("docs/templates/schemas/agent-specs/openai/architect.agent.json")
spec = json.loads(spec_file.read_text())

# Use directly with OpenAI API
client = openai.OpenAI(api_key="your-key")
response = client.chat.completions.create(**spec)
```

### GitHub Actions Integration

```yaml
name: Run Agent Task

on: workflow_dispatch

jobs:
  architect-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Load Agent Config
        id: agent
        run: |
          SPEC=$(cat docs/templates/schemas/agent-specs/yaml/architect.agent.yaml)
          echo "spec=$SPEC" >> $GITHUB_OUTPUT
      
      - name: Execute Task
        run: |
          # Use agent configuration in workflow
          echo "Running with agent: ${{ fromJSON(steps.agent.outputs.spec).agent.name }}"
```

## Source Files

All formats are generated from canonical agent specifications in:
- `.github/agents/*.agent.md` - Source agent definitions
- Conversion script: `ops/scripts/convert_agent_specs.py`

**Important:** Do not manually edit files in this directory. They are auto-generated. Make changes to the source `.agent.md` files and regenerate.

## Version Information

- **Format Version:** 1.0.0
- **Last Generated:** Auto-generated on conversion
- **Source:** `.github/agents/` markdown files

## Support and Questions

For questions about:
- **Agent definitions:** See `.github/agents/*.agent.md`
- **Conversion process:** See `ops/scripts/convert_agent_specs.py`
- **Format usage:** Refer to integration examples above
- **New formats:** Create an issue or PR to add new target formats

---

**Note:** These specifications are optimized for different platforms but maintain semantic equivalence with the source `.agent.md` files. When in doubt, refer to the canonical markdown source.
