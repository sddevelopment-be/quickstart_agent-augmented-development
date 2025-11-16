#!/usr/bin/env python3
"""
OpenCode Specification Validator

Validates JSON configuration files against the OpenCode agent specification.
Uses the official JSON Schema from docs/opencode_config.json.

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
from typing import Dict, Any, Tuple

try:
    import jsonschema
    from jsonschema import validate, ValidationError as JsonSchemaValidationError, SchemaError
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False


def load_schema(schema_path: Path) -> Tuple[Dict[str, Any], str]:
    """
    Load the OpenCode JSON Schema.
    
    Args:
        schema_path: Path to the schema file
        
    Returns:
        Tuple of (schema_dict, error_message)
    """
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
            return schema, ""
    except FileNotFoundError:
        return {}, f"Schema file not found: {schema_path}"
    except json.JSONDecodeError as e:
        return {}, f"Invalid JSON in schema: {e}"
    except Exception as e:
        return {}, f"Error loading schema: {e}"


def validate_with_jsonschema(config: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate configuration using jsonschema library.
    
    Args:
        config: Configuration to validate
        schema: JSON Schema to validate against
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not JSONSCHEMA_AVAILABLE:
        return False, "jsonschema library not available"
    
    try:
        validate(instance=config, schema=schema)
        return True, ""
    except JsonSchemaValidationError as e:
        # Format the validation error nicely
        error_path = " -> ".join(str(p) for p in e.path) if e.path else "root"
        error_msg = f"Validation error at {error_path}:\n  {e.message}"
        
        # Add context if available
        if e.context:
            error_msg += "\n\nContext:"
            for ctx_error in e.context:
                ctx_path = " -> ".join(str(p) for p in ctx_error.path) if ctx_error.path else "root"
                error_msg += f"\n  • {ctx_path}: {ctx_error.message}"
        
        return False, error_msg
    except SchemaError as e:
        return False, f"Invalid schema: {e.message}"
    except Exception as e:
        return False, f"Validation error: {e}"


def simple_validation(config: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Simple validation without jsonschema library.
    Checks basic structure only.
    
    Args:
        config: Configuration to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    errors = []
    
    # Check if it's a dict
    if not isinstance(config, dict):
        return False, "Configuration must be a JSON object"
    
    # Check for agent property (optional but common)
    if "agent" in config:
        if not isinstance(config["agent"], dict):
            errors.append("'agent' must be an object")
        else:
            # Check each agent configuration
            for agent_name, agent_config in config["agent"].items():
                if not isinstance(agent_config, dict):
                    errors.append(f"Agent '{agent_name}' must be an object")
                    continue
                
                # Check for prompt (common field)
                if "prompt" in agent_config:
                    if not isinstance(agent_config["prompt"], str):
                        errors.append(f"Agent '{agent_name}': 'prompt' must be a string")
                
                # Check for mode (common field)
                if "mode" in agent_config:
                    if not isinstance(agent_config["mode"], str):
                        errors.append(f"Agent '{agent_name}': 'mode' must be a string")
    
    if errors:
        return False, "\n".join(f"  • {e}" for e in errors)
    
    return True, ""


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
    
    def __init__(self, schema_path: Path = None):
        self.schema_path = schema_path
        self.schema = None
        self.use_jsonschema = JSONSCHEMA_AVAILABLE
        
        # Try to load schema if provided
        if schema_path and schema_path.exists():
            self.schema, error = load_schema(schema_path)
            if error:
                print(f"⚠️  Warning: {error}", file=sys.stderr)
                self.schema = None
    
    def validate(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate the configuration.
        
        Args:
            config: Parsed JSON configuration
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # If we have jsonschema and a schema, use it
        if self.use_jsonschema and self.schema:
            return validate_with_jsonschema(config, self.schema)
        
        # Otherwise fall back to simple validation
        return simple_validation(config)
    
    def get_report(self, is_valid: bool, error_msg: str = "") -> str:
        """Generate a human-readable validation report."""
        lines = []
        
        if is_valid:
            lines.append("\n✅ VALIDATION PASSED\n")
            if self.schema:
                lines.append("Configuration is valid according to OpenCode specification.")
            else:
                lines.append("Configuration passed basic structure validation.")
                lines.append("(Full schema validation unavailable)")
        else:
            lines.append("\n❌ VALIDATION FAILED\n")
            if error_msg:
                lines.append(error_msg)
        
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


def find_schema_file() -> Path:
    """Find the OpenCode schema file in the repository."""
    # Try common locations
    candidates = [
        Path('docs/opencode_config.json'),
        Path('../docs/opencode_config.json'),
        Path('../../docs/opencode_config.json'),
    ]
    
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    
    return None


def main():
    """Main entry point for the validator."""
    parser = argparse.ArgumentParser(
        description="Validate OpenCode agent configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 opencode-spec-validator.py config.json
  python3 opencode-spec-validator.py --quiet opencode-config.json
  python3 opencode-spec-validator.py --schema docs/opencode_config.json config.json

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
        '-s', '--schema',
        type=Path,
        help='Path to OpenCode JSON Schema file (default: auto-detect)'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress output, only use exit code'
    )
    
    parser.add_argument(
        '--no-schema',
        action='store_true',
        help='Skip schema validation, only do basic checks'
    )
    
    args = parser.parse_args()
    
    # Load configuration file
    config, error = load_json_file(args.config_file)
    
    if error:
        if not args.quiet:
            print(f"❌ ERROR: {error}", file=sys.stderr)
        return 2
    
    # Find schema file if not provided
    schema_path = None
    if not args.no_schema:
        if args.schema:
            schema_path = args.schema
        else:
            schema_path = find_schema_file()
        
        if schema_path and not schema_path.exists():
            if not args.quiet:
                print(f"⚠️  Schema file not found: {schema_path}", file=sys.stderr)
                print(f"⚠️  Falling back to basic validation", file=sys.stderr)
            schema_path = None
    
    # Validate configuration
    validator = OpenCodeValidator(schema_path=schema_path)
    is_valid, error_msg = validator.validate(config)
    
    # Print report
    if not args.quiet:
        print(validator.get_report(is_valid, error_msg))
    
    # Return appropriate exit code
    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
