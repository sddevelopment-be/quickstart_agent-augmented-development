#!/usr/bin/env python3
"""
Import Migration Script for ADR-046 Domain Refactoring.

Updates imports from src.common.* to src.domain.{context}.* across the codebase.
Supports dry-run mode and per-context execution for incremental validation.

Usage:
    # Preview all changes
    python tools/migration/update_domain_imports.py --dry-run
    
    # Update specific context
    python tools/migration/update_domain_imports.py --context collaboration
    python tools/migration/update_domain_imports.py --context doctrine
    python tools/migration/update_domain_imports.py --context specifications
    python tools/migration/update_domain_imports.py --context common
    
    # Update all contexts
    python tools/migration/update_domain_imports.py --all

Directive 034: Spec-Driven Development
- Implementation validates against ADR-046 specifications
- Incremental execution per bounded context
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


# Import mappings per bounded context
# Maps old import paths to new domain-specific paths
IMPORT_MAPPINGS = {
    "collaboration": {
        "src.common.task_schema": "src.domain.collaboration.task_schema",
    },
    "doctrine": {
        "src.common.agent_loader": "src.domain.doctrine.agent_loader",
    },
    "specifications": {
        # No direct imports for specifications context yet
    },
    "common": {
        "src.common.path_utils": "src.domain.common.path_utils",
    },
    "types": {
        # Special context for handling src.common.types splitting
        # Uses TYPES_MAPPINGS dictionary instead
    },
}

# Special handling for src.common.types which splits across multiple domains
# These need custom logic to split imports correctly
TYPES_MAPPINGS = {
    "TaskStatus": "src.domain.collaboration.types",
    "TaskMode": "src.domain.collaboration.types",
    "TaskPriority": "src.domain.collaboration.types",
    "FeatureStatus": "src.domain.specifications.types",
    "AgentIdentity": "src.domain.doctrine.types",
    "validate_agent": "src.domain.doctrine.types",
    "get_all_agents": "src.domain.doctrine.types",
}


def get_python_files(root_dir: Path, exclude_dirs: Set[str] = None) -> List[Path]:
    """
    Find all Python files in the repository.
    
    Args:
        root_dir: Root directory to search
        exclude_dirs: Set of directory names to exclude
        
    Returns:
        List of Python file paths
    """
    if exclude_dirs is None:
        exclude_dirs = {
            "__pycache__", 
            ".git", 
            ".pytest_cache", 
            "venv", 
            "env", 
            ".egg-info",
            "node_modules",
        }
    
    python_files = []
    for path in root_dir.rglob("*.py"):
        # Check if any parent directory is in exclude list
        if any(excluded in path.parts for excluded in exclude_dirs):
            continue
        python_files.append(path)
    
    return python_files


def update_imports_in_file(
    file_path: Path, 
    mappings: Dict[str, str], 
    dry_run: bool = False,
    handle_types: bool = False
) -> Tuple[bool, List[str]]:
    """
    Update imports in a single file.
    
    Args:
        file_path: Path to Python file
        mappings: Dictionary of old_import -> new_import
        dry_run: If True, only report changes without modifying file
        handle_types: If True, also handle src.common.types split imports
        
    Returns:
        Tuple of (file_modified, list_of_changes)
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")
        return False, []
    
    original_content = content
    changes = []
    
    # Special handling for src.common.types imports (they split across domains)
    if handle_types and "from src.common.types import" in content:
        content, types_changes = update_types_imports(content)
        changes.extend(types_changes)
    
    # Pattern 1: from src.common.MODULE import ...
    # Pattern 2: import src.common.MODULE
    for old_import, new_import in mappings.items():
        # Handle both simple and complex imports
        patterns = [
            # from src.common.module import Something
            (
                rf"from {re.escape(old_import)}(\s+import)",
                rf"from {new_import}\1"
            ),
            # import src.common.module
            (
                rf"import {re.escape(old_import)}(\s|$)",
                rf"import {new_import}\1"
            ),
        ]
        
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                old_matches = list(re.finditer(f".*{pattern}.*", content))
                if old_matches:
                    old_line_text = old_matches[0].group(0).strip()
                    content = re.sub(pattern, replacement, content)
                    new_matches = list(re.finditer(f".*from {re.escape(new_import)}.*", content))
                    if new_matches:
                        new_line_text = new_matches[0].group(0).strip()
                        changes.append(f"  - {old_line_text}\n  + {new_line_text}")
    
    modified = content != original_content
    
    if modified and not dry_run:
        try:
            file_path.write_text(content, encoding="utf-8")
        except Exception as e:
            print(f"⚠️  Error writing {file_path}: {e}")
            return False, changes
    
    return modified, changes


def update_types_imports(content: str) -> Tuple[str, List[str]]:
    """
    Handle splitting src.common.types imports across domain contexts.
    
    This is complex because types from src.common.types are now split:
    - TaskStatus, TaskMode, TaskPriority → src.domain.collaboration.types
    - FeatureStatus → src.domain.specifications.types
    - AgentIdentity, validate_agent, get_all_agents → src.domain.doctrine.types
    
    Args:
        content: File content
        
    Returns:
        Tuple of (updated_content, list_of_changes)
    """
    changes = []
    
    # Pattern for multi-line imports: from src.common.types import (...)
    multiline_pattern = r"from src\.common\.types import \(([\s\S]*?)\)"
    multiline_match = re.search(multiline_pattern, content)
    
    if multiline_match:
        # Extract imported items
        imports_block = multiline_match.group(1)
        imported_items = [
            item.strip().rstrip(',')
            for item in imports_block.split('\n')
            if item.strip() and not item.strip().startswith('#')
        ]
        
        # Group by target domain
        collaboration_items = []
        doctrine_items = []
        specifications_items = []
        
        for item in imported_items:
            if item in TYPES_MAPPINGS:
                target_module = TYPES_MAPPINGS[item]
                if "collaboration" in target_module:
                    collaboration_items.append(item)
                elif "doctrine" in target_module:
                    doctrine_items.append(item)
                elif "specifications" in target_module:
                    specifications_items.append(item)
        
        # Build replacement imports
        replacement_lines = []
        if collaboration_items:
            if len(collaboration_items) == 1:
                replacement_lines.append(
                    f"from src.domain.collaboration.types import {collaboration_items[0]}"
                )
            else:
                items_str = ", ".join(collaboration_items)
                replacement_lines.append(
                    f"from src.domain.collaboration.types import {items_str}"
                )
        
        if doctrine_items:
            if len(doctrine_items) == 1:
                replacement_lines.append(
                    f"from src.domain.doctrine.types import {doctrine_items[0]}"
                )
            else:
                items_str = ", ".join(doctrine_items)
                replacement_lines.append(
                    f"from src.domain.doctrine.types import {items_str}"
                )
        
        if specifications_items:
            if len(specifications_items) == 1:
                replacement_lines.append(
                    f"from src.domain.specifications.types import {specifications_items[0]}"
                )
            else:
                items_str = ", ".join(specifications_items)
                replacement_lines.append(
                    f"from src.domain.specifications.types import {items_str}"
                )
        
        if replacement_lines:
            old_import = multiline_match.group(0)
            new_import = "\n".join(replacement_lines)
            content = content.replace(old_import, new_import)
            changes.append(f"  - {old_import[:60]}...\n  + {new_import[:60]}...")
    
    # Pattern for single-line imports: from src.common.types import Something
    single_pattern = r"from src\.common\.types import (.+)"
    single_match = re.search(single_pattern, content)
    
    if single_match:
        imports_str = single_match.group(1)
        # Handle single or comma-separated imports
        if ',' in imports_str:
            # Multiple items on one line
            imported_items = [item.strip() for item in imports_str.split(',')]
        else:
            imported_items = [imports_str.strip()]
        
        # Group by target domain
        collaboration_items = []
        doctrine_items = []
        specifications_items = []
        
        for item in imported_items:
            if item in TYPES_MAPPINGS:
                target_module = TYPES_MAPPINGS[item]
                if "collaboration" in target_module:
                    collaboration_items.append(item)
                elif "doctrine" in target_module:
                    doctrine_items.append(item)
                elif "specifications" in target_module:
                    specifications_items.append(item)
        
        # Build replacement imports
        replacement_lines = []
        if collaboration_items:
            items_str = ", ".join(collaboration_items)
            replacement_lines.append(
                f"from src.domain.collaboration.types import {items_str}"
            )
        
        if doctrine_items:
            items_str = ", ".join(doctrine_items)
            replacement_lines.append(
                f"from src.domain.doctrine.types import {items_str}"
            )
        
        if specifications_items:
            items_str = ", ".join(specifications_items)
            replacement_lines.append(
                f"from src.domain.specifications.types import {items_str}"
            )
        
        if replacement_lines:
            old_import = single_match.group(0)
            new_import = "\n".join(replacement_lines)
            content = content.replace(old_import, new_import)
            changes.append(f"  - {old_import}\n  + {new_import}")
    
    return content, changes


def update_context_imports(
    root_dir: Path,
    context: str,
    dry_run: bool = False
) -> Dict[str, List[str]]:
    """
    Update imports for a specific bounded context.
    
    Args:
        root_dir: Repository root directory
        context: Bounded context name (collaboration, doctrine, specifications, common)
        dry_run: If True, only report changes without modifying files
        
    Returns:
        Dictionary mapping file paths to list of changes
    """
    if context not in IMPORT_MAPPINGS:
        print(f"❌ Unknown context: {context}")
        print(f"   Available contexts: {', '.join(IMPORT_MAPPINGS.keys())}")
        sys.exit(1)
    
    mappings = IMPORT_MAPPINGS[context]
    if not mappings and context != "types":
        print(f"ℹ️  No import mappings defined for context: {context}")
        return {}
    
    python_files = get_python_files(root_dir)
    print(f"\n{'🔍 DRY RUN' if dry_run else '🔧 UPDATING'} imports for context: {context}")
    print(f"Found {len(python_files)} Python files to scan\n")
    
    results = {}
    modified_count = 0
    
    # Special handling: types context processes src.common.types splitting
    handle_types = context == "types"
    
    for file_path in python_files:
        modified, changes = update_imports_in_file(
            file_path, 
            mappings, 
            dry_run,
            handle_types=handle_types
        )
        if modified:
            modified_count += 1
            relative_path = file_path.relative_to(root_dir)
            results[str(relative_path)] = changes
            
            status = "Would modify" if dry_run else "Modified"
            print(f"✅ {status}: {relative_path}")
            for change in changes:
                print(f"   {change}")
    
    print(f"\n{'Would modify' if dry_run else 'Modified'} {modified_count} file(s)")
    return results


def update_all_contexts(root_dir: Path, dry_run: bool = False) -> None:
    """
    Update imports for all bounded contexts.
    
    Args:
        root_dir: Repository root directory
        dry_run: If True, only report changes without modifying files
    """
    total_files = 0
    
    # Process in order: collaboration, doctrine, specifications, common, then types
    for context in ["collaboration", "doctrine", "specifications", "common", "types"]:
        results = update_context_imports(root_dir, context, dry_run)
        total_files += len(results)
        print(f"\n{'─' * 70}\n")
    
    print(f"\n{'🔍 DRY RUN COMPLETE' if dry_run else '✅ UPDATE COMPLETE'}")
    print(f"Total files {'that would be ' if dry_run else ''}modified: {total_files}")


def main():
    """Main entry point for import migration script."""
    parser = argparse.ArgumentParser(
        description="Update imports from src.common.* to src.domain.{context}.*",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview all changes
  python tools/migration/update_domain_imports.py --dry-run

  # Update specific context
  python tools/migration/update_domain_imports.py --context collaboration

  # Update all contexts
  python tools/migration/update_domain_imports.py --all
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    
    parser.add_argument(
        "--context",
        choices=["collaboration", "doctrine", "specifications", "common", "types"],
        help="Update imports for specific bounded context (types=handle src.common.types splitting)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Update imports for all contexts"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.context and not args.all:
        parser.error("Must specify either --context or --all")
    
    # Find repository root
    script_path = Path(__file__).resolve()
    root_dir = script_path.parent.parent.parent
    
    if not (root_dir / "src").exists():
        print(f"❌ Error: Cannot find src/ directory in {root_dir}")
        sys.exit(1)
    
    print(f"📁 Repository root: {root_dir}")
    
    # Execute migration
    if args.all:
        update_all_contexts(root_dir, args.dry_run)
    else:
        update_context_imports(root_dir, args.context, args.dry_run)
    
    if args.dry_run:
        print("\n💡 To apply changes, run without --dry-run flag")


if __name__ == "__main__":
    main()
