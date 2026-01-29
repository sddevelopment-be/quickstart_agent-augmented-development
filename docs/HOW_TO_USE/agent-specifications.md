# Agent Specifications and Format Conversion

**Version:** 1.0.0  
**Last Updated:** 2026-01-29  
**Audience:** Developers integrating agents with external platforms

## Overview

Agent specifications in this repository are maintained in a canonical `.agent.md` format with YAML frontmatter. These specifications can be converted into multiple tooling-specific optimized formats to enable integration with different platforms and systems.

## Canonical Format

Agent specifications are defined in `.github/agents/*.agent.md` files with the following structure:

```markdown
---
name: agent-name
description: Brief agent description
tools: [ "tool1", "tool2", "tool3" ]
---

# Agent Profile: Agent Name

## 1. Context Sources
- Reference documentation locations

## 2. Purpose
Agent's primary purpose and mission

## 3. Specialization
- **Primary focus:** Main areas of expertise
- **Secondary awareness:** Supporting knowledge areas
- **Avoid:** Things outside scope
- **Success means:** Definition of success

## 4. Collaboration Contract
Guidelines for working with this agent

## 5. Mode Defaults
Operating modes and their use cases

## 6. Initialization Declaration
Status confirmation template
```

## Available Formats

The repository provides automated conversion to four optimized formats:

### 1. JSON Format

**Location:** `docs/templates/schemas/agent-specs/json/`

**Purpose:** API integration, programmatic access, language-agnostic consumption

**Example:**
```json
{
  "name": "architect-alphonso",
  "description": "Clarify complex systems with contextual trade-offs.",
  "tools": ["read", "write", "search", "edit", "bash", "plantuml"],
  "purpose": "Clarify and decompose complex socio-technical systems...",
  "specialization": "...",
  "collaboration_contract": "..."
}
```

**Use Cases:**
- REST API endpoints
- Microservices configuration
- Cross-language integration
- Monitoring and orchestration systems

### 2. Anthropic Claude Format

**Location:** `docs/templates/schemas/agent-specs/anthropic/`

**Purpose:** Direct integration with Anthropic's Claude models

**Format:** Plain text system prompt optimized for Claude's context window

**Example:**
```
# architect-alphonso

Clarify complex systems with contextual trade-offs.

## Purpose
Clarify and decompose complex socio-technical systems...

## Specialization
...

## Available Tools
read, write, search, edit, bash, plantuml
```

**Use Cases:**
- Claude API integration
- Claude-based agent implementations
- Prompt engineering with Claude

### 3. OpenAI GPT Format

**Location:** `docs/templates/schemas/agent-specs/openai/`

**Purpose:** Direct integration with OpenAI's GPT models

**Example:**
```json
{
  "model": "gpt-4",
  "messages": [
    {
      "role": "system",
      "content": "Agent specification as system prompt..."
    }
  ],
  "temperature": 0.7
}
```

**Use Cases:**
- OpenAI API integration
- GPT-based agent implementations
- Chat completion workflows

### 4. YAML Configuration Format

**Location:** `docs/templates/schemas/agent-specs/yaml/`

**Purpose:** CI/CD pipelines, Infrastructure-as-Code, configuration management

**Example:**
```yaml
agent:
  name: architect-alphonso
  description: Clarify complex systems with contextual trade-offs.
  tools:
    - read
    - write
    - search
configuration:
  purpose: "..."
  specialization:
    primary_focus: "..."
    secondary_awareness: "..."
```

**Use Cases:**
- GitHub Actions workflows
- Kubernetes ConfigMaps
- Docker Compose configurations
- Ansible playbooks

## Converting Specifications

### Convert All Agents

```bash
python ops/scripts/convert_agent_specs.py
```

This generates specifications for all 15 agents in all 4 formats (60 files total).

### Convert Specific Agent

```bash
python ops/scripts/convert_agent_specs.py --agent architect.agent.md
```

### Custom Directories

```bash
python ops/scripts/convert_agent_specs.py \
  --input-dir .github/agents \
  --output-dir custom/output/path
```

### Validation

Validate all converted specifications:

```bash
python ops/scripts/validate_agent_specs.py
```

This checks:
- JSON/YAML syntax validity
- Required fields presence
- Format-specific structure
- Consistency across formats

## Integration Examples

### Python with JSON

```python
import json
from pathlib import Path

# Load agent specification
spec_path = Path("docs/templates/schemas/agent-specs/json/architect.agent.json")
spec = json.loads(spec_path.read_text())

# Access agent properties
print(f"Agent: {spec['name']}")
print(f"Purpose: {spec['purpose']}")
print(f"Tools: {', '.join(spec['tools'])}")
```

### Python with Anthropic Claude

```python
import anthropic
from pathlib import Path

# Load Claude-optimized prompt
prompt_path = Path("docs/templates/schemas/agent-specs/anthropic/architect.agent.txt")
system_prompt = prompt_path.read_text()

# Create Claude client
client = anthropic.Anthropic(api_key="your-api-key")

# Use in conversation
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    system=system_prompt,
    messages=[{"role": "user", "content": "Review this architecture..."}]
)
```

### Python with OpenAI GPT

```python
import json
import openai
from pathlib import Path

# Load OpenAI-formatted spec
spec_path = Path("docs/templates/schemas/agent-specs/openai/architect.agent.json")
spec = json.loads(spec_path.read_text())

# Use directly with OpenAI API
client = openai.OpenAI(api_key="your-api-key")

# Add user message
spec['messages'].append({
    'role': 'user',
    'content': 'Design an architecture for...'
})

# Make API call
response = client.chat.completions.create(**spec)
print(response.choices[0].message.content)
```

### GitHub Actions with YAML

```yaml
name: Run Architecture Review

on: workflow_dispatch

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Load Agent Config
        id: agent
        run: |
          # Load YAML configuration
          cat docs/templates/schemas/agent-specs/yaml/architect.agent.yaml > agent.yaml
          
          # Extract agent name
          AGENT_NAME=$(yq .agent.name agent.yaml)
          echo "name=$AGENT_NAME" >> $GITHUB_OUTPUT
      
      - name: Run Review
        run: |
          echo "Running review with agent: ${{ steps.agent.outputs.name }}"
          # Use agent configuration in workflow
```

## Maintaining Specifications

### When to Regenerate

Regenerate converted formats when:
- Agent definitions in `.github/agents/*.agent.md` are updated
- New agents are added
- Agent tools or capabilities change
- Directive references are modified

### Automated Regeneration

Add to CI/CD pipeline:

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
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install pyyaml
      
      - name: Convert specifications
        run: python ops/scripts/convert_agent_specs.py
      
      - name: Validate specifications
        run: python ops/scripts/validate_agent_specs.py
      
      - name: Commit changes
        run: |
          git config user.name "agent-bot"
          git add docs/templates/schemas/agent-specs/
          git diff --staged --quiet || git commit -m "Update agent specifications"
          git push
```

## Best Practices

### For Agent Creators

1. **Edit source files only:** Always edit `.github/agents/*.agent.md` files, never the converted formats
2. **Regenerate after changes:** Run conversion script after updating agent definitions
3. **Validate conversions:** Always run validation script before committing
4. **Document tools:** Keep the `tools` list in frontmatter up to date

### For Integration Developers

1. **Use appropriate format:** Choose the format that best matches your platform
2. **Don't modify generated files:** These are auto-generated from source
3. **Handle missing fields:** Not all sections may be present in all agents
4. **Version awareness:** Check format version in documentation

### For Maintainers

1. **Keep formats in sync:** Regenerate all formats when updating conversion logic
2. **Add new formats carefully:** Consider maintenance burden of additional formats
3. **Document format changes:** Update this guide when adding/changing formats
4. **Test integrations:** Validate that real-world integrations work after changes

## Directory Structure

```
docs/templates/schemas/agent-specs/
├── json/              # JSON format (15 files)
│   ├── architect.agent.json
│   ├── backend-dev.agent.json
│   └── ...
├── anthropic/         # Anthropic Claude format (15 files)
│   ├── architect.agent.txt
│   ├── backend-dev.agent.txt
│   └── ...
├── openai/            # OpenAI GPT format (15 files)
│   ├── architect.agent.json
│   ├── backend-dev.agent.json
│   └── ...
├── yaml/              # YAML configuration format (15 files)
│   ├── architect.agent.yaml
│   ├── backend-dev.agent.yaml
│   └── ...
└── README.md          # Format documentation
```

## Troubleshooting

### Conversion Errors

**Problem:** Script fails to parse agent file

**Solution:**
- Verify YAML frontmatter is properly formatted
- Check markdown section headers match expected format
- Ensure file encoding is UTF-8

### Validation Failures

**Problem:** Validation script reports errors

**Solution:**
- Check error message for specific field
- Regenerate specifications from source
- Verify source `.agent.md` files are valid

### Missing Fields

**Problem:** Converted format missing expected data

**Solution:**
- Check source markdown has all required sections
- Verify section headers match expected format
- Update conversion script if new sections added

## Related Documentation

- **Agent Profiles:** `.github/agents/*.agent.md` - Canonical agent definitions
- **Conversion Script:** `ops/scripts/convert_agent_specs.py` - Implementation
- **Validation Script:** `ops/scripts/validate_agent_specs.py` - Quality checks
- **Format README:** `docs/templates/schemas/agent-specs/README.md` - Detailed format docs
- **Creating Agents:** `docs/HOW_TO_USE/creating-agents.md` - Agent development guide

## Support

For questions or issues:
1. Check this documentation and format README
2. Review conversion script source code
3. Validate your specifications
4. Create an issue with error details and agent file content

---

_Document Version: 1.0.0_  
_Last Updated: 2026-01-29_  
_Maintained by: Framework Team_
