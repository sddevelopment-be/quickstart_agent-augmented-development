#!/usr/bin/env python3
"""
OpenCode Specification Validator

Validates JSON configuration files against the OpenCode agent specification.
Provides detailed error reporting for schema violations.

Usage:
    python3 opencode-spec-validator.py <config-file.json>

Exit Codes:
    0 - Valid configuration
    1 - Invalid configuration or validation error
    2 - File not found or cannot be read
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple


# OpenCode Schema Definition
# Based on common agent configuration patterns
# Update this when official specification is available
OPENCODE_SCHEMA = {
    "required_fields": ["agents", "version"],
    "optional_fields": ["metadata"],
    "agent_required_fields": ["name", "description", "instructions"],
    "agent_optional_fields": ["tools", "model", "capabilities"],
}


class ValidationError:
    """Represents a validation error with location and description."""
    
    def __init__(self, path: str, message: str, severity: str = "error"):
        self.path = path
        self.message = message
        self.severity = severity
    
    def __str__(self):
        icon = "❌" if self.severity == "error" else "⚠️"
        return f"{icon} [{self.path}] {self.message}"


class OpenCodeValidator:
    """Validates OpenCode configuration files."""
    
    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
    
    def validate(self, config: Dict[str, Any]) -> bool:
        """
        Validate the configuration against OpenCode schema.
        
        Args:
            config: Parsed JSON configuration
            
        Returns:
            True if valid, False otherwise
        """
        self.errors.clear()
        self.warnings.clear()
        
        # Check root-level required fields
        self._validate_required_fields(
            config, 
            OPENCODE_SCHEMA["required_fields"],
            "root"
        )
        
        # Validate version format
        if "version" in config:
            self._validate_version(config["version"])
        
        # Validate agents array
        if "agents" in config:
            if not isinstance(config["agents"], list):
                self.errors.append(
                    ValidationError("root.agents", "Must be an array")
                )
            else:
                self._validate_agents(config["agents"])
        
        # Validate metadata if present
        if "metadata" in config:
            self._validate_metadata(config["metadata"])
        
        # Check for unknown fields (warning only)
        known_fields = (
            OPENCODE_SCHEMA["required_fields"] + 
            OPENCODE_SCHEMA["optional_fields"]
        )
        for field in config.keys():
            if field not in known_fields:
                self.warnings.append(
                    ValidationError(
                        f"root.{field}",
                        f"Unknown field '{field}' in root configuration",
                        "warning"
                    )
                )
        
        return len(self.errors) == 0
    
    def _validate_required_fields(
        self, 
        obj: Dict[str, Any], 
        required: List[str],
        path: str
    ):
        """Check that all required fields are present."""
        for field in required:
            if field not in obj:
                self.errors.append(
                    ValidationError(
                        path,
                        f"Missing required field: '{field}'"
                    )
                )
    
    def _validate_version(self, version: Any):
        """Validate version field format."""
        if not isinstance(version, str):
            self.errors.append(
                ValidationError(
                    "root.version",
                    "Version must be a string"
                )
            )
        elif not version.strip():
            self.errors.append(
                ValidationError(
                    "root.version",
                    "Version cannot be empty"
                )
            )
    
    def _validate_agents(self, agents: List[Dict[str, Any]]):
        """Validate the agents array."""
        if len(agents) == 0:
            self.warnings.append(
                ValidationError(
                    "root.agents",
                    "Agents array is empty",
                    "warning"
                )
            )
        
        for idx, agent in enumerate(agents):
            self._validate_agent(agent, idx)
    
    def _validate_agent(self, agent: Dict[str, Any], idx: int):
        """Validate a single agent configuration."""
        path = f"agents[{idx}]"
        
        if not isinstance(agent, dict):
            self.errors.append(
                ValidationError(path, "Agent must be an object")
            )
            return
        
        # Check required fields
        self._validate_required_fields(
            agent,
            OPENCODE_SCHEMA["agent_required_fields"],
            path
        )
        
        # Validate name
        if "name" in agent:
            if not isinstance(agent["name"], str):
                self.errors.append(
                    ValidationError(f"{path}.name", "Must be a string")
                )
            elif not agent["name"].strip():
                self.errors.append(
                    ValidationError(f"{path}.name", "Cannot be empty")
                )
        
        # Validate description
        if "description" in agent:
            if not isinstance(agent["description"], str):
                self.errors.append(
                    ValidationError(f"{path}.description", "Must be a string")
                )
        
        # Validate instructions
        if "instructions" in agent:
            if not isinstance(agent["instructions"], str):
                self.errors.append(
                    ValidationError(f"{path}.instructions", "Must be a string")
                )
        
        # Validate tools if present
        if "tools" in agent:
            if not isinstance(agent["tools"], list):
                self.errors.append(
                    ValidationError(f"{path}.tools", "Must be an array")
                )
            else:
                for tool_idx, tool in enumerate(agent["tools"]):
                    if not isinstance(tool, str):
                        self.errors.append(
                            ValidationError(
                                f"{path}.tools[{tool_idx}]",
                                "Tool must be a string"
                            )
                        )
        
        # Check for unknown fields
        known_fields = (
            OPENCODE_SCHEMA["agent_required_fields"] +
            OPENCODE_SCHEMA["agent_optional_fields"]
        )
        for field in agent.keys():
            if field not in known_fields:
                self.warnings.append(
                    ValidationError(
                        f"{path}.{field}",
                        f"Unknown agent field '{field}'",
                        "warning"
                    )
                )
    
    def _validate_metadata(self, metadata: Any):
        """Validate metadata object."""
        if not isinstance(metadata, dict):
            self.errors.append(
                ValidationError(
                    "root.metadata",
                    "Metadata must be an object"
                )
            )
    
    def get_report(self) -> str:
        """Generate a human-readable validation report."""
        lines = []
        
        if self.errors:
            lines.append("\n❌ VALIDATION FAILED\n")
            lines.append(f"Found {len(self.errors)} error(s):\n")
            for error in self.errors:
                lines.append(f"  {error}")
        
        if self.warnings:
            lines.append(f"\n⚠️  Found {len(self.warnings)} warning(s):\n")
            for warning in self.warnings:
                lines.append(f"  {warning}")
        
        if not self.errors and not self.warnings:
            lines.append("\n✅ VALIDATION PASSED\n")
            lines.append("Configuration is valid according to OpenCode specification.")
        
        return "\n".join(lines)


def load_json_file(filepath: Path) -> Tuple[Dict[str, Any], str]:
    """
    Load and parse JSON file.
    
    Returns:
        Tuple of (parsed_data, error_message)
        If successful, error_message is empty string
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data, ""
    except FileNotFoundError:
        return {}, f"File not found: {filepath}"
    except json.JSONDecodeError as e:
        return {}, f"Invalid JSON: {e}"
    except Exception as e:
        return {}, f"Error reading file: {e}"


def main():
    """Main entry point for the validator."""
    parser = argparse.ArgumentParser(
        description="Validate OpenCode agent configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 opencode-spec-validator.py config.json
  python3 opencode-spec-validator.py --quiet opencode-config.json

Exit codes:
  0 - Valid configuration
  1 - Invalid configuration
  2 - File error (not found, invalid JSON, etc.)
        """
    )
    
    parser.add_argument(
        'config_file',
        type=Path,
        help='Path to OpenCode configuration JSON file'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress output, only use exit code'
    )
    
    parser.add_argument(
        '--warnings-as-errors',
        action='store_true',
        help='Treat warnings as errors'
    )
    
    args = parser.parse_args()
    
    # Load configuration file
    config, error = load_json_file(args.config_file)
    
    if error:
        if not args.quiet:
            print(f"❌ ERROR: {error}", file=sys.stderr)
        return 2
    
    # Validate configuration
    validator = OpenCodeValidator()
    is_valid = validator.validate(config)
    
    # Check if warnings should be treated as errors
    if args.warnings_as_errors and validator.warnings:
        is_valid = False
    
    # Print report
    if not args.quiet:
        print(validator.get_report())
    
    # Return appropriate exit code
    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
