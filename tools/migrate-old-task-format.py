#!/usr/bin/env python3
"""
Migrate old task format to new format.

Old format: task_id, from_agent, to_agent, UPPERCASE status
New format: id, agent, lowercase status with proper frontmatter

Usage:
    python tools/migrate-old-task-format.py --dry-run  # Preview changes
    python tools/migrate-old-task-format.py            # Apply changes
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, Any

import yaml

# Add src/ to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from common.types import TaskStatus


def migrate_task(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Migrate old task format to new format.
    
    Migrations:
    - task_id → id
    - from_agent/to_agent → agent (use to_agent as primary)
    - UPPERCASE status → lowercase with enum validation
    - created_date → created (ISO8601 with Z)
    - Remove obsolete fields: from_agent, human_intervention_required, etc.
    """
    migrated = {}
    
    # 1. Migrate task_id → id
    if 'task_id' in task:
        migrated['id'] = task['task_id']
    elif 'id' in task:
        migrated['id'] = task['id']
    else:
        raise ValueError("Task missing both 'task_id' and 'id' fields")
    
    # 2. Migrate agent (use to_agent if present, else agent)
    if 'to_agent' in task:
        # Convert "Backend Benny" → "backend-dev"
        agent_name = task['to_agent'].lower().replace(' ', '-')
        # Simple mapping for common agents
        agent_map = {
            'backend-benny': 'backend-dev',
            'architect-alphonso': 'architect',
            'project-manager': 'manager',
            'build-automation': 'build-automation',
        }
        migrated['agent'] = agent_map.get(agent_name, agent_name)
    elif 'agent' in task:
        migrated['agent'] = task['agent']
    else:
        # Default to 'unknown' if not specified
        migrated['agent'] = 'unknown'
    
    # 3. Migrate status (lowercase + validate)
    if 'status' in task:
        status_str = task['status'].lower().replace('_', '_')
        # Map old status values to new enum
        status_map = {
            'todo': 'new',
            'complete': 'done',
            'completed': 'done',
            'in_progress': 'in_progress',
            'blocked': 'blocked',
            'error': 'error',
            'new': 'new',
            'inbox': 'inbox',
            'assigned': 'assigned',
            'done': 'done',
        }
        migrated['status'] = status_map.get(status_str, status_str)
        
        # Validate against TaskStatus enum
        try:
            TaskStatus(migrated['status'])
        except ValueError:
            print(f"  ⚠️  Warning: Invalid status '{migrated['status']}', defaulting to 'inbox'")
            migrated['status'] = 'inbox'
    else:
        migrated['status'] = 'inbox'
    
    # 4. Migrate priority (lowercase)
    if 'priority' in task:
        migrated['priority'] = task['priority'].lower()
    
    # 5. Copy title (required)
    if 'title' in task:
        migrated['title'] = task['title']
    elif 'description' in task and isinstance(task['description'], str):
        # Extract first line as title if missing
        first_line = task['description'].split('\n')[0].strip('# ').strip()
        migrated['title'] = first_line[:80]  # Max 80 chars
    else:
        migrated['title'] = f"Task {migrated['id']}"
    
    # 6. Migrate description (convert to multiline string if markdown)
    if 'description' in task:
        desc = task['description']
        if isinstance(desc, str) and ('\n' in desc or desc.startswith('#')):
            # Keep as multiline
            migrated['description'] = desc
        else:
            migrated['description'] = str(desc)
    
    # 7. Migrate timestamps (ISO8601 with Z suffix)
    timestamp_fields = ['created', 'assigned_at', 'started_at', 'completed_at']
    for field in timestamp_fields:
        # Try old format first (created_date)
        old_field = field + '_date' if field == 'created' else field
        if old_field in task:
            value = task[old_field]
            # Ensure Z suffix
            if isinstance(value, str) and not value.endswith('Z'):
                migrated[field] = value + 'T00:00:00Z'
            else:
                migrated[field] = value
        elif field in task:
            migrated[field] = task[field]
    
    # 8. Copy optional fields
    optional_fields = [
        'phase', 'batch', 'milestone', 'dependencies', 
        'estimated_effort_hours', 'actual_effort_hours',
        'tags', 'notes', 'result', 'error'
    ]
    for field in optional_fields:
        if field in task:
            migrated[field] = task[field]
    
    return migrated


def migrate_file(path: Path, dry_run: bool = False) -> bool:
    """
    Migrate a single task file.
    
    Returns True if migration needed, False if already new format.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse YAML
        task = yaml.safe_load(content)
        
        if not isinstance(task, dict):
            print(f"  ❌ Skipping {path.name}: Not a dictionary")
            return False
        
        # Check if migration needed
        needs_migration = 'task_id' in task or 'from_agent' in task or 'to_agent' in task
        
        if not needs_migration:
            print(f"  ✅ {path.name}: Already new format")
            return False
        
        # Migrate
        migrated = migrate_task(task)
        
        if dry_run:
            print(f"  🔍 {path.name}: Would migrate")
            print(f"     task_id={task.get('task_id')} → id={migrated['id']}")
            print(f"     status={task.get('status')} → {migrated['status']}")
            return True
        
        # Write migrated task
        with open(path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            yaml.safe_dump(migrated, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"  ✅ {path.name}: Migrated")
        return True
    
    except Exception as e:
        print(f"  ❌ {path.name}: Error - {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Migrate old task format to new format")
    parser.add_argument('--dry-run', action='store_true', help="Preview changes without applying")
    parser.add_argument('--path', type=Path, help="Specific file or directory to migrate")
    args = parser.parse_args()
    
    # Default to work/collaboration directory
    base_path = args.path or Path("work/collaboration")
    
    if not base_path.exists():
        print(f"❌ Path not found: {base_path}")
        return 1
    
    # Find all YAML files
    if base_path.is_file():
        files = [base_path]
    else:
        files = list(base_path.rglob("*.yaml"))
    
    print(f"🔍 Found {len(files)} YAML files")
    print(f"{'🔍 DRY RUN MODE' if args.dry_run else '✅ MIGRATION MODE'}\n")
    
    migrated_count = 0
    for file_path in files:
        if migrate_file(file_path, dry_run=args.dry_run):
            migrated_count += 1
    
    print(f"\n{'📊 Would migrate' if args.dry_run else '✅ Migrated'} {migrated_count}/{len(files)} files")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
