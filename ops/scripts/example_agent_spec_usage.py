#!/usr/bin/env python3
"""
Example: Loading and using agent specifications in different formats.

This script demonstrates how to load and use agent specifications
from the various converted formats.
"""

import json
import yaml
from pathlib import Path


def example_json_usage():
    """Example: Using JSON format for API integration."""
    print("=" * 60)
    print("Example 1: JSON Format (API Integration)")
    print("=" * 60)
    
    # Load JSON specification
    spec_path = Path("docs/templates/schemas/agent-specs/json/architect.agent.json")
    spec = json.loads(spec_path.read_text())
    
    # Access agent properties
    print(f"\nAgent Name: {spec['name']}")
    print(f"Description: {spec['description']}")
    print(f"\nAvailable Tools:")
    for tool in spec['tools']:
        print(f"  - {tool}")
    
    print(f"\nPurpose:")
    print(f"  {spec['purpose']}")
    
    # Example: Filter agents by tool availability
    print("\n" + "-" * 60)
    print("Finding all agents with 'bash' tool:")
    print("-" * 60)
    
    json_dir = Path("docs/templates/schemas/agent-specs/json")
    agents_with_bash = []
    
    for agent_file in json_dir.glob("*.json"):
        agent_spec = json.loads(agent_file.read_text())
        if 'bash' in agent_spec.get('tools', []):
            agents_with_bash.append(agent_spec['name'])
    
    for agent_name in sorted(agents_with_bash):
        print(f"  ✓ {agent_name}")
    
    print()


def example_yaml_usage():
    """Example: Using YAML format for configuration."""
    print("=" * 60)
    print("Example 2: YAML Format (Configuration)")
    print("=" * 60)
    
    # Load YAML configuration
    spec_path = Path("docs/templates/schemas/agent-specs/yaml/synthesizer.agent.yaml")
    config = yaml.safe_load(spec_path.read_text())
    
    # Access configuration
    print(f"\nAgent: {config['agent']['name']}")
    print(f"Description: {config['agent']['description']}")
    
    if 'specialization' in config.get('configuration', {}):
        spec = config['configuration']['specialization']
        print(f"\nPrimary Focus:")
        print(f"  {spec.get('primary_focus', 'N/A')}")
    
    print()


def example_anthropic_usage():
    """Example: Using Anthropic format for Claude integration."""
    print("=" * 60)
    print("Example 3: Anthropic Format (Claude Integration)")
    print("=" * 60)
    
    # Load Anthropic prompt
    prompt_path = Path("docs/templates/schemas/agent-specs/anthropic/researcher.agent.txt")
    system_prompt = prompt_path.read_text()
    
    print(f"\nSystem Prompt Length: {len(system_prompt)} characters")
    print(f"\nFirst 200 characters:")
    print("-" * 60)
    print(system_prompt[:200] + "...")
    
    print(f"\n\nThis prompt can be used directly with Anthropic Claude API:")
    print("  client.messages.create(")
    print("      model='claude-3-opus-20240229',")
    print("      system=system_prompt,")
    print("      messages=[...]")
    print("  )")
    print()


def example_openai_usage():
    """Example: Using OpenAI format for GPT integration."""
    print("=" * 60)
    print("Example 4: OpenAI Format (GPT Integration)")
    print("=" * 60)
    
    # Load OpenAI specification
    spec_path = Path("docs/templates/schemas/agent-specs/openai/backend-dev.agent.json")
    openai_spec = json.loads(spec_path.read_text())
    
    print(f"\nModel: {openai_spec.get('model', 'N/A')}")
    print(f"Temperature: {openai_spec.get('temperature', 'N/A')}")
    print(f"Messages: {len(openai_spec.get('messages', []))} message(s)")
    
    if openai_spec.get('messages'):
        first_msg = openai_spec['messages'][0]
        print(f"\nFirst Message:")
        print(f"  Role: {first_msg.get('role', 'N/A')}")
        print(f"  Content Length: {len(first_msg.get('content', ''))} characters")
    
    print(f"\n\nThis specification can be used directly with OpenAI API:")
    print("  client.chat.completions.create(**openai_spec)")
    print()


def example_multi_format_comparison():
    """Example: Comparing the same agent across formats."""
    print("=" * 60)
    print("Example 5: Multi-Format Comparison")
    print("=" * 60)
    
    agent_name = "manager"
    
    # Load from different formats
    json_spec = json.loads(
        Path(f"docs/templates/schemas/agent-specs/json/{agent_name}.agent.json").read_text()
    )
    yaml_spec = yaml.safe_load(
        Path(f"docs/templates/schemas/agent-specs/yaml/{agent_name}.agent.yaml").read_text()
    )
    anthropic_prompt = Path(
        f"docs/templates/schemas/agent-specs/anthropic/{agent_name}.agent.txt"
    ).read_text()
    openai_spec = json.loads(
        Path(f"docs/templates/schemas/agent-specs/openai/{agent_name}.agent.json").read_text()
    )
    
    print(f"\nAgent: {agent_name}")
    print(f"\nFormat Comparison:")
    print(f"  JSON:")
    print(f"    - Name: {json_spec.get('name', 'N/A')}")
    print(f"    - Tools: {len(json_spec.get('tools', []))} tools")
    print(f"    - Size: {len(json.dumps(json_spec))} bytes")
    
    print(f"\n  YAML:")
    print(f"    - Name: {yaml_spec.get('agent', {}).get('name', 'N/A')}")
    print(f"    - Tools: {len(yaml_spec.get('agent', {}).get('tools', []))} tools")
    print(f"    - Size: {len(yaml.dump(yaml_spec))} bytes")
    
    print(f"\n  Anthropic:")
    print(f"    - Format: Plain text prompt")
    print(f"    - Size: {len(anthropic_prompt)} bytes")
    
    print(f"\n  OpenAI:")
    print(f"    - Model: {openai_spec.get('model', 'N/A')}")
    print(f"    - Messages: {len(openai_spec.get('messages', []))}")
    print(f"    - Size: {len(json.dumps(openai_spec))} bytes")
    
    print()


def main():
    """Run all examples."""
    print("\n")
    print("*" * 60)
    print("Agent Specification Format Examples")
    print("*" * 60)
    print()
    
    try:
        example_json_usage()
        example_yaml_usage()
        example_anthropic_usage()
        example_openai_usage()
        example_multi_format_comparison()
        
        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        print()
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure agent specifications have been generated:")
        print("  python ops/scripts/convert_agent_specs.py")
        print()


if __name__ == '__main__':
    main()
