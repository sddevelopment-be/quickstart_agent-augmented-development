#!/usr/bin/env python3
"""
Validate converted agent specifications.

This script validates that converted agent specifications:
1. Are valid JSON/YAML
2. Contain required fields
3. Match the source agent names
"""

import json
import sys
import yaml
from pathlib import Path


def validate_json_specs(specs_dir: Path) -> bool:
    """Validate JSON specifications."""
    json_dir = specs_dir / 'json'
    if not json_dir.exists():
        print(f"✗ JSON directory not found: {json_dir}")
        return False
    
    json_files = list(json_dir.glob('*.json'))
    if not json_files:
        print(f"✗ No JSON files found in {json_dir}")
        return False
    
    print(f"\nValidating {len(json_files)} JSON files...")
    errors = []
    
    for json_file in json_files:
        try:
            data = json.loads(json_file.read_text())
            
            # Check required fields
            required_fields = ['name', 'description', 'tools']
            missing_fields = [f for f in required_fields if f not in data]
            
            if missing_fields:
                errors.append(f"{json_file.name}: Missing fields: {missing_fields}")
            
            # Check tools is a list
            if 'tools' in data and not isinstance(data['tools'], list):
                errors.append(f"{json_file.name}: 'tools' must be a list")
                
        except json.JSONDecodeError as e:
            errors.append(f"{json_file.name}: Invalid JSON - {e}")
    
    if errors:
        print("✗ JSON validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print(f"✓ All {len(json_files)} JSON files valid")
    return True


def validate_yaml_specs(specs_dir: Path) -> bool:
    """Validate YAML specifications."""
    yaml_dir = specs_dir / 'yaml'
    if not yaml_dir.exists():
        print(f"✗ YAML directory not found: {yaml_dir}")
        return False
    
    yaml_files = list(yaml_dir.glob('*.yaml'))
    if not yaml_files:
        print(f"✗ No YAML files found in {yaml_dir}")
        return False
    
    print(f"\nValidating {len(yaml_files)} YAML files...")
    errors = []
    
    for yaml_file in yaml_files:
        try:
            data = yaml.safe_load(yaml_file.read_text())
            
            # Check required top-level keys
            if 'agent' not in data:
                errors.append(f"{yaml_file.name}: Missing 'agent' key")
                continue
            
            # Check agent fields
            if 'name' not in data['agent']:
                errors.append(f"{yaml_file.name}: Missing 'agent.name' field")
            
            if 'tools' not in data['agent']:
                errors.append(f"{yaml_file.name}: Missing 'agent.tools' field")
            elif not isinstance(data['agent']['tools'], list):
                errors.append(f"{yaml_file.name}: 'agent.tools' must be a list")
                
        except yaml.YAMLError as e:
            errors.append(f"{yaml_file.name}: Invalid YAML - {e}")
    
    if errors:
        print("✗ YAML validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print(f"✓ All {len(yaml_files)} YAML files valid")
    return True


def validate_openai_specs(specs_dir: Path) -> bool:
    """Validate OpenAI format specifications."""
    openai_dir = specs_dir / 'openai'
    if not openai_dir.exists():
        print(f"✗ OpenAI directory not found: {openai_dir}")
        return False
    
    openai_files = list(openai_dir.glob('*.json'))
    if not openai_files:
        print(f"✗ No OpenAI files found in {openai_dir}")
        return False
    
    print(f"\nValidating {len(openai_files)} OpenAI format files...")
    errors = []
    
    for openai_file in openai_files:
        try:
            data = json.loads(openai_file.read_text())
            
            # Check OpenAI API structure
            if 'messages' not in data:
                errors.append(f"{openai_file.name}: Missing 'messages' field")
                continue
            
            if not isinstance(data['messages'], list):
                errors.append(f"{openai_file.name}: 'messages' must be a list")
                continue
            
            # Check first message is system message
            if data['messages']:
                first_msg = data['messages'][0]
                if 'role' not in first_msg or first_msg['role'] != 'system':
                    errors.append(f"{openai_file.name}: First message must have role='system'")
                
                if 'content' not in first_msg:
                    errors.append(f"{openai_file.name}: Message missing 'content' field")
                    
        except json.JSONDecodeError as e:
            errors.append(f"{openai_file.name}: Invalid JSON - {e}")
    
    if errors:
        print("✗ OpenAI format validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print(f"✓ All {len(openai_files)} OpenAI format files valid")
    return True


def validate_anthropic_specs(specs_dir: Path) -> bool:
    """Validate Anthropic format specifications."""
    anthropic_dir = specs_dir / 'anthropic'
    if not anthropic_dir.exists():
        print(f"✗ Anthropic directory not found: {anthropic_dir}")
        return False
    
    anthropic_files = list(anthropic_dir.glob('*.txt'))
    if not anthropic_files:
        print(f"✗ No Anthropic files found in {anthropic_dir}")
        return False
    
    print(f"\nValidating {len(anthropic_files)} Anthropic format files...")
    errors = []
    
    for anthropic_file in anthropic_files:
        content = anthropic_file.read_text()
        
        # Check it's not empty
        if not content.strip():
            errors.append(f"{anthropic_file.name}: File is empty")
            continue
        
        # Check for key sections
        if '## Purpose' not in content:
            errors.append(f"{anthropic_file.name}: Missing '## Purpose' section")
        
        if '## Specialization' not in content:
            errors.append(f"{anthropic_file.name}: Missing '## Specialization' section")
    
    if errors:
        print("✗ Anthropic format validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print(f"✓ All {len(anthropic_files)} Anthropic format files valid")
    return True


def validate_consistency(specs_dir: Path) -> bool:
    """Validate that all formats have the same agents."""
    json_files = {f.stem for f in (specs_dir / 'json').glob('*.json')}
    yaml_files = {f.stem for f in (specs_dir / 'yaml').glob('*.yaml')}
    openai_files = {f.stem for f in (specs_dir / 'openai').glob('*.json')}
    anthropic_files = {f.stem for f in (specs_dir / 'anthropic').glob('*.txt')}
    
    print(f"\nValidating consistency across formats...")
    print(f"  JSON: {len(json_files)} agents")
    print(f"  YAML: {len(yaml_files)} agents")
    print(f"  OpenAI: {len(openai_files)} agents")
    print(f"  Anthropic: {len(anthropic_files)} agents")
    
    # Check all have same agents
    if not (json_files == yaml_files == openai_files == anthropic_files):
        print("✗ Agent sets differ across formats")
        
        all_agents = json_files | yaml_files | openai_files | anthropic_files
        for agent in sorted(all_agents):
            formats_present = []
            if agent in json_files:
                formats_present.append('JSON')
            if agent in yaml_files:
                formats_present.append('YAML')
            if agent in openai_files:
                formats_present.append('OpenAI')
            if agent in anthropic_files:
                formats_present.append('Anthropic')
            
            if len(formats_present) != 4:
                print(f"  {agent}: {', '.join(formats_present)}")
        
        return False
    
    print(f"✓ All formats have consistent agent set ({len(json_files)} agents)")
    return True


def main():
    specs_dir = Path('docs/templates/schemas/agent-specs')
    
    if not specs_dir.exists():
        print(f"✗ Specs directory not found: {specs_dir}")
        sys.exit(1)
    
    print("=" * 60)
    print("Agent Specification Validation")
    print("=" * 60)
    
    results = []
    
    results.append(validate_json_specs(specs_dir))
    results.append(validate_yaml_specs(specs_dir))
    results.append(validate_openai_specs(specs_dir))
    results.append(validate_anthropic_specs(specs_dir))
    results.append(validate_consistency(specs_dir))
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ All validations passed!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("✗ Some validations failed")
        print("=" * 60)
        sys.exit(1)


if __name__ == '__main__':
    main()
