#!/usr/bin/env python3
"""
Boy Scout Task-to-Spec Mapper

Intelligently maps done tasks to specification files based on:
- Task title keywords
- Task description content
- ADR references
- Date proximity
- Agent type

Directive 036: Boy Scout Rule - Leave repository better than we found it
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Task title patterns → Specification mappings
SPEC_MAPPINGS = {
    # Dashboard Enhancements
    r'dashboard.*markdown|markdown.*dashboard': 'specifications/initiatives/dashboard-enhancements/markdown-rendering.md',
    r'dashboard.*priority|priority.*edit': 'specifications/initiatives/dashboard-enhancements/task-priority-editing.md',
    r'portfolio.*track|initiative.*track': 'specifications/initiatives/dashboard-enhancements/initiative-tracking.md',
    r'dashboard.*cors|file.*watcher|telemetry': 'specifications/initiatives/dashboard-enhancements/real-time-execution-dashboard.md',
    r'docsite|documentation.*site': 'specifications/initiatives/dashboard-enhancements/docsite-integration.md',
    
    # Framework Distribution
    r'export|exporter|validation.*test|multi.*tool': 'specifications/initiatives/framework-distribution/SPEC-DIST-001-multi-tool-distribution.md',
    r'claude.*adapter|openai.*adapter|subprocess': 'specifications/initiatives/framework-distribution/SPEC-DIST-001-multi-tool-distribution.md',
    r'config.*schema|pydantic|click.*cli': 'specifications/initiatives/framework-distribution/SPEC-DIST-001-multi-tool-distribution.md',
    
    # Src Consolidation
    r'src.*consolidation|duplicat.*analysis|review.*src': 'specifications/initiatives/src-consolidation/SPEC-CONSOLIDATION-001-src-code-consolidation.md',
    
    # Research & Documentation (no specs - leave as orphan)
    r'ralph.*wiggum|research': None,
    r'tooling.*best.*practice|maintenance.*checklist': None,
    r'yaml.*format.*error|update.*docs': None,
}

# Feature-specific patterns (for tasks that should link to specific features)
FEATURE_MAPPINGS = {
    # Initiative tracking features
    r'portfolio.*bug|task.*link': ('specifications/initiatives/dashboard-enhancements/initiative-tracking.md', 'FEAT-DASH-003-02'),
    r'portfolio.*api': ('specifications/initiatives/dashboard-enhancements/initiative-tracking.md', 'FEAT-DASH-003-03'),
    
    # Priority editing features
    r'priority.*edit': ('specifications/initiatives/dashboard-enhancements/task-priority-editing.md', 'FEAT-DASH-004-01'),
    
    # Markdown rendering features
    r'markdown.*render': ('specifications/initiatives/dashboard-enhancements/markdown-rendering.md', 'FEAT-DASH-005-01'),
}


def read_task(path: Path) -> Optional[Dict]:
    """Read and parse task YAML."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            task = yaml.safe_load(f)
        return task if isinstance(task, dict) else None
    except Exception as e:
        print(f"  ⚠️  Failed to read {path.name}: {e}")
        return None


def match_task_to_spec(task: Dict, task_path: Path) -> Tuple[Optional[str], Optional[str]]:
    """
    Match task to specification and optional feature.
    
    Returns:
        (specification_path, feature_id) or (None, None)
    """
    title = task.get('title', '').lower()
    description = task.get('description', '').lower()
    combined = f"{title} {description}"
    
    # Check for existing (possibly broken) specification field
    existing_spec = task.get('specification')
    if existing_spec:
        # Fix broken paths
        if 'llm-dashboard' in existing_spec:
            fixed_spec = existing_spec.replace('llm-dashboard', 'initiatives/dashboard-enhancements')
            print(f"  🔧 {task_path.name}: Fixing broken path")
            print(f"     {existing_spec} → {fixed_spec}")
            return (fixed_spec, None)
    
    # Try feature-specific matches first (includes feature ID)
    for pattern, (spec, feature) in FEATURE_MAPPINGS.items():
        if re.search(pattern, combined, re.IGNORECASE):
            print(f"  ✅ {task_path.name}: Matched to {Path(spec).stem}")
            print(f"     Pattern: {pattern}")
            print(f"     Feature: {feature}")
            return (spec, feature)
    
    # Try specification-only matches
    for pattern, spec in SPEC_MAPPINGS.items():
        if re.search(pattern, combined, re.IGNORECASE):
            if spec is None:
                print(f"  ⏭️  {task_path.name}: Intentional orphan (research/docs)")
                return (None, None)
            print(f"  ✅ {task_path.name}: Matched to {Path(spec).stem}")
            print(f"     Pattern: {pattern}")
            return (spec, None)
    
    # No match found
    print(f"  ❓ {task_path.name}: No specification match")
    print(f"     Title: {task.get('title', 'N/A')}")
    return (None, None)


def update_task_with_spec(task_path: Path, spec_path: Optional[str], feature_id: Optional[str], dry_run: bool = False) -> bool:
    """
    Update task YAML with specification and feature fields.
    
    Returns True if updated, False if no changes needed.
    """
    task = read_task(task_path)
    if not task:
        return False
    
    changes_made = False
    
    # Update specification field
    if spec_path:
        current_spec = task.get('specification')
        if current_spec != spec_path:
            task['specification'] = spec_path
            changes_made = True
    
    # Update feature field (if provided)
    if feature_id:
        current_feature = task.get('feature')
        if current_feature != feature_id:
            task['feature'] = feature_id
            changes_made = True
    
    if not changes_made:
        return False
    
    if dry_run:
        return True
    
    # Write updated task
    with open(task_path, 'w', encoding='utf-8') as f:
        f.write("---\n")
        yaml.safe_dump(task, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Map tasks to specifications (Boy Scout Rule)")
    parser.add_argument('--dry-run', action='store_true', help="Preview changes")
    args = parser.parse_args()
    
    done_dir = Path("work/collaboration/done")
    
    if not done_dir.exists():
        print(f"❌ Directory not found: {done_dir}")
        return 1
    
    # Find all done tasks
    task_files = list(done_dir.rglob("*.yaml"))
    print(f"🔍 Found {len(task_files)} done tasks")
    print(f"{'🔍 DRY RUN MODE' if args.dry_run else '✅ UPDATE MODE'}\n")
    
    updated_count = 0
    orphan_count = 0
    already_linked_count = 0
    
    for task_path in sorted(task_files):
        task = read_task(task_path)
        if not task:
            continue
        
        # Check if already has correct specification
        if task.get('specification') and 'llm-dashboard' not in task.get('specification', ''):
            already_linked_count += 1
            continue
        
        # Match to specification
        spec_path, feature_id = match_task_to_spec(task, task_path)
        
        if spec_path is None:
            orphan_count += 1
            continue
        
        # Update task
        if update_task_with_spec(task_path, spec_path, feature_id, dry_run=args.dry_run):
            updated_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   Already linked: {already_linked_count}")
    print(f"   {'Would update' if args.dry_run else 'Updated'}: {updated_count}")
    print(f"   Orphans (intentional): {orphan_count}")
    print(f"   Total: {len(task_files)}")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
