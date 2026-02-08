#!/usr/bin/env python3
"""
Task Path Migration Script
==========================

Purpose: Update task YAML files to reflect post-refactor directory structure.

Context: PR #135 refactored:
  - ops/ → tools/ and src/
  - validation/ → tools/validators/
  - examples/ → fixtures/

This script:
1. Scans all .yaml files in work/collaboration/assigned/
2. Finds artifact paths containing obsolete directories
3. Updates them to new paths
4. Creates backup before modifying
5. Generates detailed migration report

Author: Planning Petra
Date: 2026-02-08
"""

import os
import sys
import re
import shutil
from pathlib import Path
from datetime import datetime
import yaml


# Path mappings: old → new
PATH_MAPPINGS = {
    'ops/exporters/': 'tools/exporters/',
    'ops/portability/': 'tools/exporters/portability/',
    'ops/scripts/': 'tools/scripts/',
    'ops/orchestration/': 'src/framework/orchestration/',
    'ops/': 'tools/',  # Catch-all for remaining ops/ paths
    'validation/': 'tools/validators/',
    'examples/': 'fixtures/',
}


class TaskPathMigrator:
    """Migrates task artifact paths from old to new structure."""
    
    def __init__(self, assigned_dir: Path, backup_dir: Path = None):
        self.assigned_dir = assigned_dir
        self.backup_dir = backup_dir or assigned_dir.parent / "backups" / datetime.now().strftime("%Y-%m-%dT%H%M%S")
        self.changes = []
        self.errors = []
        
    def backup_tasks(self):
        """Create backup of all task files before modification."""
        print(f"📦 Creating backup at: {self.backup_dir}")
        if self.backup_dir.exists():
            print(f"⚠️  Backup directory already exists, skipping backup creation")
            return False
        
        shutil.copytree(self.assigned_dir, self.backup_dir)
        print(f"✅ Backup created: {len(list(self.backup_dir.glob('*/*.yaml')))} files")
        return True
        
    def migrate_path(self, old_path: str) -> tuple[str, bool]:
        """
        Migrate a single path string using PATH_MAPPINGS.
        
        Returns:
            (new_path, changed): Tuple of new path and whether it changed
        """
        new_path = old_path
        changed = False
        
        # Apply mappings in order (most specific first)
        for old_prefix, new_prefix in PATH_MAPPINGS.items():
            if old_prefix in new_path:
                new_path = new_path.replace(old_prefix, new_prefix)
                changed = True
                # Only apply first matching rule
                break
                
        return new_path, changed
        
    def process_yaml_content(self, content: str, file_path: Path) -> tuple[str, list]:
        """
        Process YAML content and update paths.
        
        Returns:
            (new_content, changes): Tuple of modified content and list of changes
        """
        file_changes = []
        lines = content.split('\n')
        new_lines = []
        
        for line_num, line in enumerate(lines, 1):
            new_line = line
            
            # Check if line contains artifact path (typically under 'artifact:' or in paths)
            if any(old_prefix in line for old_prefix in PATH_MAPPINGS.keys()):
                # Migrate the path
                migrated_line = line
                for old_prefix, new_prefix in PATH_MAPPINGS.items():
                    if old_prefix in migrated_line:
                        migrated_line = migrated_line.replace(old_prefix, new_prefix)
                        file_changes.append({
                            'line': line_num,
                            'old': line.strip(),
                            'new': migrated_line.strip(),
                            'mapping': f"{old_prefix} → {new_prefix}"
                        })
                        break
                        
                new_line = migrated_line
                
            new_lines.append(new_line)
            
        return '\n'.join(new_lines), file_changes
        
    def validate_yaml(self, content: str, file_path: Path) -> bool:
        """Validate YAML syntax."""
        try:
            yaml.safe_load(content)
            return True
        except yaml.YAMLError as e:
            self.errors.append({
                'file': str(file_path),
                'error': f"YAML validation failed: {e}"
            })
            return False
            
    def process_file(self, file_path: Path):
        """Process a single task file."""
        try:
            # Read original content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
                
            # Validate original YAML
            if not self.validate_yaml(original_content, file_path):
                return
                
            # Process content
            new_content, file_changes = self.process_yaml_content(original_content, file_path)
            
            # Only write if changes were made
            if file_changes:
                # Validate new YAML
                if not self.validate_yaml(new_content, file_path):
                    self.errors.append({
                        'file': str(file_path),
                        'error': "New content failed YAML validation - skipping"
                    })
                    return
                    
                # Write updated content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    
                self.changes.append({
                    'file': file_path.relative_to(self.assigned_dir),
                    'changes': file_changes
                })
                
        except Exception as e:
            self.errors.append({
                'file': str(file_path),
                'error': str(e)
            })
            
    def migrate_all(self):
        """Migrate all task files in assigned directory."""
        print(f"\n🔍 Scanning: {self.assigned_dir}")
        
        task_files = list(self.assigned_dir.glob('*/*.yaml'))
        print(f"📋 Found {len(task_files)} task files")
        
        if not task_files:
            print("⚠️  No task files found")
            return
            
        # Create backup
        backup_created = self.backup_tasks()
        if not backup_created and self.backup_dir.exists():
            user_input = input("Backup exists. Continue without new backup? (y/n): ")
            if user_input.lower() != 'y':
                print("❌ Migration cancelled")
                return
        
        print(f"\n🔄 Processing {len(task_files)} files...")
        
        for file_path in task_files:
            self.process_file(file_path)
            
        self.generate_report()
        
    def generate_report(self):
        """Generate migration report."""
        print("\n" + "=" * 80)
        print("📊 MIGRATION REPORT")
        print("=" * 80)
        
        print(f"\n✅ Files processed: {len(list(self.assigned_dir.glob('*/*.yaml')))}")
        print(f"📝 Files modified: {len(self.changes)}")
        print(f"❌ Errors: {len(self.errors)}")
        
        if self.changes:
            print("\n" + "-" * 80)
            print("MODIFIED FILES:")
            print("-" * 80)
            
            for change_record in self.changes:
                print(f"\n📄 {change_record['file']}")
                for change in change_record['changes']:
                    print(f"  Line {change['line']}: {change['mapping']}")
                    print(f"    - OLD: {change['old']}")
                    print(f"    + NEW: {change['new']}")
                    
        if self.errors:
            print("\n" + "-" * 80)
            print("⚠️  ERRORS:")
            print("-" * 80)
            for error in self.errors:
                print(f"\n❌ {error['file']}")
                print(f"   {error['error']}")
                
        # Generate summary statistics
        print("\n" + "-" * 80)
        print("STATISTICS:")
        print("-" * 80)
        
        total_changes = sum(len(record['changes']) for record in self.changes)
        print(f"Total path changes: {total_changes}")
        
        # Count by mapping type
        mapping_counts = {}
        for record in self.changes:
            for change in record['changes']:
                mapping = change['mapping']
                mapping_counts[mapping] = mapping_counts.get(mapping, 0) + 1
                
        print("\nChanges by path mapping:")
        for mapping, count in sorted(mapping_counts.items(), key=lambda x: -x[1]):
            print(f"  {mapping}: {count} changes")
            
        print("\n" + "=" * 80)
        
        # Save report to file
        report_path = Path('work/reports/task-path-migration-report.txt')
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write(f"Task Path Migration Report\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"{'=' * 80}\n\n")
            f.write(f"Files processed: {len(list(self.assigned_dir.glob('*/*.yaml')))}\n")
            f.write(f"Files modified: {len(self.changes)}\n")
            f.write(f"Total changes: {total_changes}\n")
            f.write(f"Errors: {len(self.errors)}\n\n")
            
            if self.changes:
                f.write("MODIFIED FILES:\n")
                f.write("-" * 80 + "\n")
                for record in self.changes:
                    f.write(f"\n{record['file']}\n")
                    for change in record['changes']:
                        f.write(f"  Line {change['line']}: {change['mapping']}\n")
                        
            if self.errors:
                f.write("\nERRORS:\n")
                f.write("-" * 80 + "\n")
                for error in self.errors:
                    f.write(f"\n{error['file']}\n  {error['error']}\n")
                    
        print(f"\n💾 Detailed report saved to: {report_path}")


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent.parent
    assigned_dir = repo_root / 'work' / 'collaboration' / 'assigned'
    
    if not assigned_dir.exists():
        print(f"❌ Error: Directory not found: {assigned_dir}")
        sys.exit(1)
        
    print("=" * 80)
    print("TASK PATH MIGRATION UTILITY")
    print("=" * 80)
    print(f"\nTarget directory: {assigned_dir}")
    print("\nPath mappings:")
    for old, new in PATH_MAPPINGS.items():
        print(f"  {old:30} → {new}")
        
    print("\n⚠️  This will modify task files in place (backup will be created)")
    user_input = input("\nProceed with migration? (y/n): ")
    
    if user_input.lower() != 'y':
        print("❌ Migration cancelled")
        sys.exit(0)
        
    migrator = TaskPathMigrator(assigned_dir)
    migrator.migrate_all()
    
    if migrator.errors:
        sys.exit(1)
    else:
        print("\n✅ Migration completed successfully!")
        sys.exit(0)


if __name__ == '__main__':
    main()
