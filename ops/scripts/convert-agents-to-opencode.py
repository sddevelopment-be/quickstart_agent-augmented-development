#!/usr/bin/env python3
"""
Agent to OpenCode Configuration Converter

Converts agent markdown files from .github/agents to OpenCode JSON format.
Parses YAML frontmatter and markdown content to generate standardized config.

Usage:
    python3 convert-agents-to-opencode.py [options]

Options:
    -i, --input-dir PATH     Agent files directory (default: .github/agents)
    -o, --output PATH        Output JSON file (default: opencode-config.json)
    -v, --verbose            Enable verbose logging
    --validate               Validate output using opencode-spec-validator.py

Exit Codes:
    0 - Successful conversion
    1 - Conversion errors occurred
    2 - Validation failed (when --validate is used)
"""

import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple


class AgentParser:
    """Parse agent markdown files with YAML frontmatter."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors: List[str] = []
    
    def log(self, message: str):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(f"ℹ️  {message}")
    
    def parse_file(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """
        Parse an agent markdown file.
        
        Args:
            filepath: Path to the agent file
            
        Returns:
            Dictionary with agent data or None if parsing fails
        """
        try:
            content = filepath.read_text(encoding='utf-8')
            
            # Extract YAML frontmatter
            frontmatter_match = re.match(
                r'^---\s*\n(.*?)\n---\s*\n(.*)$',
                content,
                re.DOTALL
            )
            
            if not frontmatter_match:
                self.log(f"Skipping {filepath.name}: No YAML frontmatter found")
                return None
            
            frontmatter_text = frontmatter_match.group(1)
            markdown_body = frontmatter_match.group(2).strip()
            
            # Parse frontmatter manually (simple YAML subset)
            frontmatter = self._parse_simple_yaml(frontmatter_text)
            
            if not frontmatter:
                self.errors.append(f"Failed to parse frontmatter in {filepath.name}")
                return None
            
            # Build agent configuration
            agent = {
                "name": frontmatter.get("name", ""),
                "description": frontmatter.get("description", ""),
                "instructions": markdown_body
            }
            
            # Add optional fields if present
            if "tools" in frontmatter:
                agent["tools"] = frontmatter["tools"]
            
            # Validate required fields
            if not agent["name"]:
                self.errors.append(f"Missing 'name' in {filepath.name}")
                return None
            
            if not agent["description"]:
                self.errors.append(f"Missing 'description' in {filepath.name}")
                return None
            
            self.log(f"Parsed agent: {agent['name']}")
            return agent
            
        except Exception as e:
            self.errors.append(f"Error parsing {filepath.name}: {e}")
            return None
    
    def _parse_simple_yaml(self, yaml_text: str) -> Dict[str, Any]:
        """
        Parse a simple subset of YAML (key: value and key: [list]).
        
        This is a minimal parser for the frontmatter format used in agent files.
        Does not support full YAML spec.
        """
        result = {}
        
        for line in yaml_text.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Match key: value pattern
            match = re.match(r'^(\w+):\s*(.+)$', line)
            if not match:
                continue
            
            key = match.group(1)
            value = match.group(2).strip()
            
            # Parse array format: ["item1", "item2", ...]
            if value.startswith('[') and value.endswith(']'):
                # Remove brackets and split by comma
                items_text = value[1:-1]
                items = []
                for item in items_text.split(','):
                    item = item.strip()
                    # Remove quotes
                    if (item.startswith('"') and item.endswith('"')) or \
                       (item.startswith("'") and item.endswith("'")):
                        item = item[1:-1]
                    if item:
                        items.append(item)
                result[key] = items
            else:
                # Remove surrounding quotes if present
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                result[key] = value
        
        return result


class AgentConverter:
    """Convert agent files to OpenCode configuration."""
    
    def __init__(self, input_dir: Path, verbose: bool = False):
        self.input_dir = input_dir
        self.parser = AgentParser(verbose=verbose)
        self.verbose = verbose
    
    def log(self, message: str):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(f"ℹ️  {message}")
    
    def convert(self) -> Tuple[Dict[str, Any], List[str]]:
        """
        Convert all agent files to OpenCode configuration.
        
        Returns:
            Tuple of (config_dict, list_of_errors)
        """
        if not self.input_dir.exists():
            return {}, [f"Input directory not found: {self.input_dir}"]
        
        # Find all .agent.md files
        agent_files = sorted(self.input_dir.glob("*.agent.md"))
        
        if not agent_files:
            self.log("No .agent.md files found")
            return {}, ["No agent files found to convert"]
        
        self.log(f"Found {len(agent_files)} agent file(s)")
        
        # Parse each agent file
        agents = []
        for filepath in agent_files:
            agent = self.parser.parse_file(filepath)
            if agent:
                agents.append(agent)
        
        if not agents and self.parser.errors:
            return {}, self.parser.errors
        
        # Build OpenCode configuration
        try:
            source_path = str(self.input_dir.relative_to(Path.cwd()))
        except ValueError:
            source_path = str(self.input_dir)
        
        config = {
            "version": "1.0.0",
            "agents": agents,
            "metadata": {
                "source": source_path,
                "generated": datetime.now(timezone.utc).isoformat(),
                "generator": "convert-agents-to-opencode.py",
                "agent_count": len(agents)
            }
        }
        
        return config, self.parser.errors
    
    def save_config(self, config: Dict[str, Any], output_path: Path) -> bool:
        """
        Save configuration to JSON file.
        
        Args:
            config: OpenCode configuration
            output_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write with pretty formatting
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                f.write('\n')  # Add final newline
            
            self.log(f"Saved configuration to {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving configuration: {e}", file=sys.stderr)
            return False


def validate_output(output_path: Path, validator_script: Path) -> bool:
    """
    Validate the generated configuration using the validator script.
    
    Args:
        output_path: Path to generated config file
        validator_script: Path to validator script
        
    Returns:
        True if validation passes, False otherwise
    """
    import subprocess
    
    if not validator_script.exists():
        print(f"⚠️  Validator not found: {validator_script}", file=sys.stderr)
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(validator_script), str(output_path)],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running validator: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point for the converter."""
    parser = argparse.ArgumentParser(
        description="Convert agent markdown files to OpenCode JSON configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert agents from default location
  python3 convert-agents-to-opencode.py
  
  # Specify custom paths
  python3 convert-agents-to-opencode.py -i .github/agents -o config.json
  
  # Convert and validate
  python3 convert-agents-to-opencode.py --validate --verbose
        """
    )
    
    parser.add_argument(
        '-i', '--input-dir',
        type=Path,
        default=Path('.github/agents'),
        help='Directory containing agent markdown files (default: .github/agents)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path('opencode-config.json'),
        help='Output JSON file path (default: opencode-config.json)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate output using opencode-spec-validator.py'
    )
    
    args = parser.parse_args()
    
    # Convert agents
    print(f"🔄 Converting agents from {args.input_dir}...")
    
    converter = AgentConverter(args.input_dir, verbose=args.verbose)
    config, errors = converter.convert()
    
    # Report errors
    if errors:
        print(f"\n⚠️  Encountered {len(errors)} issue(s) during conversion:")
        for error in errors:
            print(f"  • {error}")
    
    # Check if we got any agents
    if not config or not config.get("agents"):
        print("\n❌ No agents were successfully converted", file=sys.stderr)
        return 1
    
    # Save configuration
    print(f"\n💾 Saving configuration to {args.output}...")
    if not converter.save_config(config, args.output):
        return 1
    
    print(f"\n✅ Successfully converted {len(config['agents'])} agent(s)")
    
    # Validate if requested
    if args.validate:
        print("\n🔍 Validating output...")
        validator_path = args.output.parent / 'ops' / 'scripts' / 'opencode-spec-validator.py'
        if not validator_path.exists():
            # Try relative to current script
            validator_path = Path(__file__).parent / 'opencode-spec-validator.py'
        
        if validate_output(args.output, validator_path):
            print("\n✅ Validation successful")
        else:
            print("\n❌ Validation failed", file=sys.stderr)
            return 2
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
