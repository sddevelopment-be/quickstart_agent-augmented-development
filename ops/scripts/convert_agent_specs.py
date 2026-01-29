#!/usr/bin/env python3
"""
Convert agent specifications from .agent.md format to multiple tooling-specific formats.

This script reads agent specifications in Markdown format with YAML frontmatter
and converts them into various optimized formats for different platforms:
- JSON (for programmatic access and APIs)
- Anthropic Claude system prompt format
- OpenAI GPT system prompt format
- YAML (for CI/CD pipelines and configuration)
"""

import argparse
import json
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional


class AgentSpecConverter:
    """Converts agent specifications to different formats."""
    
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir
        
    def parse_agent_file(self, filepath: Path) -> Dict[str, Any]:
        """Parse an agent .md file with YAML frontmatter."""
        content = filepath.read_text()
        
        # Extract YAML frontmatter
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)'
        match = re.match(frontmatter_pattern, content, re.DOTALL)
        
        if not match:
            raise ValueError(f"No YAML frontmatter found in {filepath}")
        
        frontmatter_text = match.group(1)
        markdown_content = match.group(2)
        
        # Parse frontmatter
        frontmatter = yaml.safe_load(frontmatter_text)
        
        # Extract sections from markdown
        sections = self._extract_sections(markdown_content)
        
        return {
            'name': frontmatter.get('name', ''),
            'description': frontmatter.get('description', ''),
            'tools': frontmatter.get('tools', []),
            'content': markdown_content,
            'sections': sections,
            'frontmatter': frontmatter
        }
    
    def _extract_sections(self, markdown: str) -> Dict[str, str]:
        """Extract markdown sections by header.
        
        Supports both numbered (## 1. Purpose) and unnumbered (## Purpose) headers.
        The space after the period in numbered headers is optional.
        """
        sections = {}
        current_section = None
        current_content = []
        
        for line in markdown.split('\n'):
            # Match headers like "## 1. Purpose", "## 1.Purpose", or "## Purpose"
            # The (?:\d+\.\s*)? pattern allows optional numbering with optional space after period
            header_match = re.match(r'^##\s+(?:\d+\.\s*)?(.+)$', line)
            if header_match:
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = header_match.group(1).strip()
                current_content = []
            elif current_section:
                current_content.append(line)
        
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def to_json(self, agent_data: Dict[str, Any]) -> str:
        """Convert agent specification to JSON format."""
        output = {
            'name': agent_data['name'],
            'description': agent_data['description'],
            'tools': agent_data['tools'],
            'purpose': agent_data['sections'].get('Purpose', ''),
            'specialization': agent_data['sections'].get('Specialization', ''),
            'collaboration_contract': agent_data['sections'].get('Collaboration Contract', ''),
            'mode_defaults': agent_data['sections'].get('Mode Defaults', ''),
            'context_sources': agent_data['sections'].get('Context Sources', ''),
            'directive_references': agent_data['sections'].get('Directive References (Externalized)', ''),
        }
        return json.dumps(output, indent=2)
    
    def to_anthropic_prompt(self, agent_data: Dict[str, Any]) -> str:
        """Convert agent specification to Anthropic Claude system prompt format."""
        prompt_parts = [
            f"# {agent_data['name']}",
            "",
            agent_data['description'],
            "",
            "## Purpose",
            agent_data['sections'].get('Purpose', ''),
            "",
            "## Specialization",
            agent_data['sections'].get('Specialization', ''),
            "",
            "## Collaboration Guidelines",
            agent_data['sections'].get('Collaboration Contract', ''),
            "",
            "## Available Tools",
            ", ".join(agent_data['tools']),
            "",
            "## Operating Modes",
            agent_data['sections'].get('Mode Defaults', ''),
        ]
        
        return '\n'.join(prompt_parts)
    
    def to_openai_prompt(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert agent specification to OpenAI GPT format."""
        system_prompt = f"""{agent_data['description']}

## Purpose
{agent_data['sections'].get('Purpose', '')}

## Specialization
{agent_data['sections'].get('Specialization', '')}

## Collaboration Guidelines
{agent_data['sections'].get('Collaboration Contract', '')}

## Available Tools
{', '.join(agent_data['tools'])}
"""
        
        return {
            'model': 'gpt-4',
            'messages': [
                {
                    'role': 'system',
                    'content': system_prompt.strip()
                }
            ],
            'temperature': 0.7
        }
    
    def to_yaml_config(self, agent_data: Dict[str, Any]) -> str:
        """Convert agent specification to YAML configuration format."""
        config = {
            'agent': {
                'name': agent_data['name'],
                'description': agent_data['description'],
                'tools': agent_data['tools'],
            },
            'configuration': {
                'purpose': agent_data['sections'].get('Purpose', ''),
                'specialization': {
                    'primary_focus': self._extract_focus(agent_data['sections'].get('Specialization', ''), 'Primary focus:'),
                    'secondary_awareness': self._extract_focus(agent_data['sections'].get('Specialization', ''), 'Secondary awareness:'),
                    'avoid': self._extract_focus(agent_data['sections'].get('Specialization', ''), 'Avoid:'),
                },
            },
            'context_sources': agent_data['sections'].get('Context Sources', ''),
        }
        return yaml.dump(config, default_flow_style=False, sort_keys=False)
    
    def _extract_focus(self, specialization_text: str, marker: str) -> str:
        """Extract specific focus areas from specialization section.
        
        Extracts content from the marker line and strips markdown formatting.
        This is a simplified extraction that captures inline content.
        For complete multi-line specialization content, use the full
        specialization field available in other format outputs.
        
        Note: This method extracts only the first line after the marker.
        Full specialization text with all details is preserved in the
        'specialization' field of JSON and other formats.
        """
        lines = specialization_text.split('\n')
        for i, line in enumerate(lines):
            if marker in line:
                # Extract content after the marker (same line only)
                content = line.split(marker, 1)[1].strip()
                # Strip markdown formatting (e.g., **text** -> text)
                content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
                content = content.lstrip('*').strip()
                return content
        return ''
    
    def convert_agent(self, agent_file: Path) -> bool:
        """Convert a single agent file to all formats.
        
        Returns:
            True if conversion succeeded, False otherwise.
        """
        print(f"Converting {agent_file.name}...")
        
        try:
            agent_data = self.parse_agent_file(agent_file)
            agent_slug = agent_file.stem  # e.g., 'architect.agent'
            
            # Create output directories
            formats = ['json', 'anthropic', 'openai', 'yaml']
            for fmt in formats:
                (self.output_dir / fmt).mkdir(parents=True, exist_ok=True)
            
            # Convert to JSON
            json_output = self.to_json(agent_data)
            (self.output_dir / 'json' / f'{agent_slug}.json').write_text(json_output)
            
            # Convert to Anthropic format
            anthropic_output = self.to_anthropic_prompt(agent_data)
            (self.output_dir / 'anthropic' / f'{agent_slug}.txt').write_text(anthropic_output)
            
            # Convert to OpenAI format
            openai_output = self.to_openai_prompt(agent_data)
            (self.output_dir / 'openai' / f'{agent_slug}.json').write_text(
                json.dumps(openai_output, indent=2)
            )
            
            # Convert to YAML
            yaml_output = self.to_yaml_config(agent_data)
            (self.output_dir / 'yaml' / f'{agent_slug}.yaml').write_text(yaml_output)
            
            print(f"  ✓ Converted to all formats")
            return True
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def convert_all(self) -> int:
        """Convert all agent files in the input directory.
        
        Returns:
            Number of agents that failed to convert (0 means all succeeded).
        """
        agent_files = sorted(self.input_dir.glob('*.agent.md'))
        
        if not agent_files:
            print(f"No agent files found in {self.input_dir}")
            return 0
        
        print(f"Found {len(agent_files)} agent files\n")
        
        failed_agents = []
        for agent_file in agent_files:
            if not self.convert_agent(agent_file):
                failed_agents.append(agent_file.name)
        
        print(f"\nConversion complete! Output in {self.output_dir}")
        print(f"  - JSON: {self.output_dir / 'json'}")
        print(f"  - Anthropic: {self.output_dir / 'anthropic'}")
        print(f"  - OpenAI: {self.output_dir / 'openai'}")
        print(f"  - YAML: {self.output_dir / 'yaml'}")
        
        if failed_agents:
            print(f"\n⚠️  {len(failed_agents)} agent(s) failed to convert:")
            for agent in failed_agents:
                print(f"  - {agent}")
        
        return len(failed_agents)


def main():
    parser = argparse.ArgumentParser(
        description='Convert agent specifications to multiple formats'
    )
    parser.add_argument(
        '--input-dir',
        type=Path,
        default=Path('.github/agents'),
        help='Directory containing .agent.md files (default: .github/agents)'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('docs/templates/schemas/agent-specs'),
        help='Output directory for converted files (default: docs/templates/schemas/agent-specs)'
    )
    parser.add_argument(
        '--agent',
        type=str,
        help='Convert only specific agent (e.g., architect.agent.md)'
    )
    
    args = parser.parse_args()
    
    # Validate input directory
    if not args.input_dir.exists():
        print(f"Error: Input directory {args.input_dir} does not exist")
        sys.exit(1)
    
    # Create converter
    converter = AgentSpecConverter(args.input_dir, args.output_dir)
    
    # Convert
    if args.agent:
        agent_file = args.input_dir / args.agent
        if not agent_file.exists():
            print(f"Error: Agent file {agent_file} does not exist")
            sys.exit(1)
        success = converter.convert_agent(agent_file)
        sys.exit(0 if success else 1)
    else:
        failed_count = converter.convert_all()
        sys.exit(failed_count)


if __name__ == '__main__':
    main()
