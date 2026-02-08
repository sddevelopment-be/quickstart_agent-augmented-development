#!/usr/bin/env python3
"""
Path Reference Validator for GitHub Actions Workflows

This script validates that all path references in workflow files actually exist.
It checks:
- uses: references to local actions (e.g., ./.github/actions/*)
- run: references to scripts (e.g., python tools/*, bash scripts/*)
- path filters in workflow triggers
- working-directory references

Exit codes:
  0 - All path references are valid
  1 - Invalid path references found
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import List, Tuple, Set

# Root directory (repository root)
REPO_ROOT = Path(__file__).parent.parent.parent

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_success(msg: str):
    print(f"{GREEN}✅ {msg}{RESET}")


def print_error(msg: str):
    print(f"{RED}❌ {msg}{RESET}")


def print_warning(msg: str):
    print(f"{YELLOW}⚠️  {msg}{RESET}")


def print_info(msg: str):
    print(f"{BLUE}ℹ️  {msg}{RESET}")


def extract_local_action_paths(workflow_data: dict) -> Set[str]:
    """Extract local action paths from 'uses:' fields."""
    paths = set()
    
    def traverse(obj):
        if isinstance(obj, dict):
            if 'uses' in obj:
                uses = obj['uses']
                if isinstance(uses, str) and uses.startswith('./'):
                    # Remove any @ref suffix
                    path = uses.split('@')[0]
                    paths.add(path)
            for value in obj.values():
                traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)
    
    traverse(workflow_data)
    return paths


def extract_script_paths(workflow_data: dict) -> Set[str]:
    """Extract script paths from 'run:' commands."""
    paths = set()
    
    # Common patterns for script execution
    patterns = [
        r'python\s+([\w/.-]+\.py)',
        r'bash\s+([\w/.-]+\.sh)',
        r'sh\s+([\w/.-]+\.sh)',
        r'node\s+([\w/.-]+\.js)',
        r'\./([^\s]+\.(?:py|sh|js))',
        r'chmod\s+\+x\s+([\w/.-]+)',
    ]
    
    def extract_from_run(run_cmd: str):
        if not isinstance(run_cmd, str):
            return
        
        for pattern in patterns:
            matches = re.findall(pattern, run_cmd)
            for match in matches:
                # Clean up the path
                match = match.strip()
                if match and not match.startswith('/'):
                    paths.add(match)
    
    def traverse(obj):
        if isinstance(obj, dict):
            if 'run' in obj:
                extract_from_run(obj['run'])
            for value in obj.values():
                traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)
    
    traverse(workflow_data)
    return paths


def extract_working_directories(workflow_data: dict) -> Set[str]:
    """Extract working-directory paths."""
    paths = set()
    
    def traverse(obj):
        if isinstance(obj, dict):
            if 'working-directory' in obj:
                wd = obj['working-directory']
                if isinstance(wd, str) and not wd.startswith('$'):
                    paths.add(wd)
            for value in obj.values():
                traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)
    
    traverse(workflow_data)
    return paths


def extract_path_filters(workflow_data: dict) -> Set[str]:
    """Extract path filters from workflow triggers."""
    paths = set()
    
    # Look in 'on' section
    if 'on' in workflow_data:
        on_section = workflow_data['on']
        
        if isinstance(on_section, dict):
            for trigger_name, trigger_config in on_section.items():
                if isinstance(trigger_config, dict) and 'paths' in trigger_config:
                    path_list = trigger_config['paths']
                    if isinstance(path_list, list):
                        for path in path_list:
                            if isinstance(path, str):
                                # Remove wildcards and extract directory
                                clean_path = path.strip("'\"")
                                # For patterns like '.github/workflows/**', extract the base directory
                                base_path = clean_path.split('**')[0].rstrip('/')
                                if base_path and not base_path.startswith('!'):
                                    paths.add(base_path)
    
    return paths


def validate_path(path: str, is_action: bool = False) -> bool:
    """Check if a path exists relative to repository root."""
    # Remove leading './'
    clean_path = path
    if clean_path.startswith('./'):
        clean_path = clean_path[2:]
    
    # Skip paths with variables
    if '$' in clean_path or '{' in clean_path:
        return True
    
    # Skip wildcards - just check parent directory exists
    if '*' in clean_path:
        base_path = clean_path.split('*')[0].rstrip('/')
        if not base_path:
            return True
        full_path = REPO_ROOT / base_path
        return full_path.exists()
    
    full_path = REPO_ROOT / clean_path
    
    # For GitHub Actions, check if directory contains action.yml or action.yaml
    if is_action and full_path.is_dir():
        return (full_path / 'action.yml').exists() or (full_path / 'action.yaml').exists()
    
    return full_path.exists()


def validate_workflow_file(workflow_path: Path) -> Tuple[bool, List[str]]:
    """Validate a single workflow file."""
    print_info(f"Validating {workflow_path.relative_to(REPO_ROOT)}")
    
    try:
        with open(workflow_path, 'r') as f:
            workflow_data = yaml.safe_load(f)
    except Exception as e:
        print_error(f"Failed to parse {workflow_path}: {e}")
        return False, [f"Parse error: {e}"]
    
    if not workflow_data:
        print_warning(f"Empty workflow file: {workflow_path}")
        return True, []
    
    errors = []
    
    # Extract all path references
    action_paths = extract_local_action_paths(workflow_data)
    script_paths = extract_script_paths(workflow_data)
    working_dirs = extract_working_directories(workflow_data)
    path_filters = extract_path_filters(workflow_data)
    
    # Validate action paths
    for path in action_paths:
        if not validate_path(path, is_action=True):
            errors.append(f"Local action not found: {path}")
    
    # Validate script paths
    for path in script_paths:
        if not validate_path(path):
            errors.append(f"Script not found: {path}")
    
    # Validate working directories
    for path in working_dirs:
        if not validate_path(path):
            errors.append(f"Working directory not found: {path}")
    
    # Validate path filters (just check directories exist)
    for path in path_filters:
        if not validate_path(path):
            errors.append(f"Path filter directory not found: {path}")
    
    return len(errors) == 0, errors


def main():
    """Main validation logic."""
    print(f"{BLUE}=" * 60)
    print("GitHub Actions Path Reference Validator")
    print("=" * 60 + RESET)
    print()
    
    workflows_dir = REPO_ROOT / '.github' / 'workflows'
    
    if not workflows_dir.exists():
        print_error(f"Workflows directory not found: {workflows_dir}")
        return 1
    
    workflow_files = list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml'))
    
    if not workflow_files:
        print_warning("No workflow files found")
        return 0
    
    print_info(f"Found {len(workflow_files)} workflow files to validate")
    print()
    
    all_valid = True
    total_errors = 0
    
    for workflow_file in sorted(workflow_files):
        is_valid, errors = validate_workflow_file(workflow_file)
        
        if is_valid:
            print_success(f"{workflow_file.name}: All paths valid")
        else:
            all_valid = False
            print_error(f"{workflow_file.name}: {len(errors)} invalid path(s)")
            for error in errors:
                print(f"  - {error}")
            total_errors += len(errors)
        
        print()
    
    print(f"{BLUE}=" * 60 + RESET)
    
    if all_valid:
        print_success("All workflow path references are valid!")
        return 0
    else:
        print_error(f"Found {total_errors} invalid path reference(s)")
        print()
        print("Please ensure all referenced files and directories exist.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
