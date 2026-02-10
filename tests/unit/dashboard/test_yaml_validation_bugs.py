"""
Test for YAML validation bugs reported by dashboard.

Bug 1: YAML parsing error in task file (quoted strings in list)
Bug 2: Missing 'initiative' field in specification frontmatter

These tests capture the bugs before fixing them (TDD RED phase).
"""

import sys
from pathlib import Path
import yaml

# Add repository root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


def test_task_yaml_can_be_parsed():
    """
    Test that the problematic task YAML file can be parsed.
    
    Bug: Line 19 has quoted string that breaks YAML parser:
    - "Show Finished Work" toggle button added...
    
    This line is part of a list but the quote placement confuses parser.
    """
    task_file = Path("work/collaboration/done/frontend-freddy/2026-02-10T1105-frontend-freddy-kanban-restructure.yaml")
    
    if not task_file.exists():
        print(f"⚠️  SKIP: Task file not found: {task_file}")
        return True
    
    try:
        content = task_file.read_text()
        data = yaml.safe_load(content)
        
        # Verify acceptance_criteria parsed correctly
        assert 'acceptance_criteria' in data, "Missing acceptance_criteria field"
        assert isinstance(data['acceptance_criteria'], list), "acceptance_criteria should be a list"
        assert len(data['acceptance_criteria']) > 0, "acceptance_criteria list is empty"
        
        print(f"✅ PASS: Task YAML parsed successfully ({len(data['acceptance_criteria'])} criteria)")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ FAIL: YAML parsing error in {task_file}")
        print(f"   Error: {e}")
        print(f"   Fix: Properly quote or escape strings in list items")
        return False


def test_specification_has_initiative_field():
    """
    Test that specification files have required 'initiative' field.
    
    Bug: SPEC-DIST-001 and SPEC-DIST-002 missing 'initiative' field in frontmatter.
    
    Schema requires: id, title, status, initiative, priority
    """
    spec_files = [
        "specifications/initiatives/framework-distribution/SPEC-DIST-001-multi-tool-distribution.md",
        "specifications/initiatives/framework-distribution/SPEC-DIST-002-claude-code-optimization.md",
    ]
    
    results = []
    for spec_path in spec_files:
        spec_file = Path(spec_path)
        
        if not spec_file.exists():
            print(f"⚠️  SKIP: Spec file not found: {spec_file}")
            continue
        
        try:
            content = spec_file.read_text()
            
            # Extract frontmatter
            if not content.startswith('---'):
                print(f"❌ FAIL: {spec_file.name} - No frontmatter found")
                results.append(False)
                continue
            
            # Find end of frontmatter
            end_marker = content.find('\n---\n', 4)
            if end_marker == -1:
                print(f"❌ FAIL: {spec_file.name} - Malformed frontmatter")
                results.append(False)
                continue
            
            frontmatter_str = content[4:end_marker]
            frontmatter = yaml.safe_load(frontmatter_str)
            
            # Check for initiative field
            if 'initiative' not in frontmatter:
                print(f"❌ FAIL: {spec_file.name} - Missing 'initiative' field")
                print(f"   Has fields: {list(frontmatter.keys())}")
                print(f"   Fix: Add 'initiative: framework-distribution' to frontmatter")
                results.append(False)
            else:
                print(f"✅ PASS: {spec_file.name} - Has initiative field: {frontmatter['initiative']}")
                results.append(True)
                
        except Exception as e:
            print(f"❌ FAIL: {spec_file.name} - Error: {e}")
            results.append(False)
    
    return all(results) if results else True


def test_spec_parser_can_load_specifications():
    """
    Test that spec_parser can load the problematic specifications.
    
    This verifies the fix works end-to-end with the dashboard parser.
    """
    try:
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        parser = SpecificationParser("specifications")
        
        # Try to load specifications
        spec_dir = Path("specifications/initiatives/framework-distribution")
        if not spec_dir.exists():
            print("⚠️  SKIP: Specification directory not found")
            return True
        
        specs = parser.parse_all_specifications()
        
        # Check if our problematic specs are loaded
        spec_ids = [s.id for s in specs]
        
        if 'SPEC-DIST-001' in spec_ids:
            print("✅ PASS: SPEC-DIST-001 loaded successfully")
        else:
            print("❌ FAIL: SPEC-DIST-001 not loaded")
            return False
            
        if 'SPEC-DIST-002' in spec_ids:
            print("✅ PASS: SPEC-DIST-002 loaded successfully")
        else:
            print("❌ FAIL: SPEC-DIST-002 not loaded")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Spec parser error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("Testing YAML validation bugs (TDD RED phase)")
    print("=" * 70)
    print()
    
    results = []
    
    print("Test 1: Task YAML can be parsed")
    print("-" * 70)
    results.append(test_task_yaml_can_be_parsed())
    print()
    
    print("Test 2: Specifications have 'initiative' field")
    print("-" * 70)
    results.append(test_specification_has_initiative_field())
    print()
    
    print("Test 3: Spec parser can load specifications")
    print("-" * 70)
    results.append(test_spec_parser_can_load_specifications())
    print()
    
    print("=" * 70)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    if all(results):
        print("✅ ALL TESTS PASSED (GREEN)")
        sys.exit(0)
    else:
        print("❌ TESTS FAILED (RED) - Fix needed")
        sys.exit(1)
