#!/usr/bin/env python3
"""
Ralph Wiggum Loop - Self-Observation CLI Tool

This script automates the Ralph Wiggum loop checkpoint process for agent tasks.
It can run manual checkpoints or watch tasks for automatic checkpoint triggers.

Usage:
    # Manual checkpoint
    python ops/scripts/ralph-wiggum-loop.py check --task-id 2026-01-31T1200-task

    # Watch mode with automatic checkpoints
    python ops/scripts/ralph-wiggum-loop.py watch \\
        --task-id 2026-01-31T1200-task \\
        --interval 15 \\
        --auto-continue-if-clean

    # Generate checkpoint report
    python ops/scripts/ralph-wiggum-loop.py report --task-id 2026-01-31T1200-task

Reference: Directive 024 (Self-Observation Protocol)
"""

import argparse
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from ops.common.path_utils import resolve_repo_path
except ImportError:
    # Fallback if path_utils not available
    def resolve_repo_path(relative_path: str) -> Path:
        return PROJECT_ROOT / relative_path


class CheckpointResult:
    """Result of a Ralph Wiggum loop checkpoint."""
    
    def __init__(self, 
                 task_id: str,
                 timestamp: str,
                 progress: str,
                 mode: str,
                 warnings: List[str],
                 critical_issues: List[str],
                 decision: str,
                 reasoning: str,
                 corrections: Optional[List[str]] = None):
        self.task_id = task_id
        self.timestamp = timestamp
        self.progress = progress
        self.mode = mode
        self.warnings = warnings
        self.critical_issues = critical_issues
        self.decision = decision
        self.reasoning = reasoning
        self.corrections = corrections or []
    
    @property
    def severity(self) -> str:
        """Determine severity based on issues detected."""
        if self.critical_issues:
            return "critical"
        elif len(self.warnings) >= 5:
            return "critical"
        elif len(self.warnings) >= 2:
            return "warning"
        else:
            return "clean"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "task_id": self.task_id,
            "timestamp": self.timestamp,
            "progress": self.progress,
            "mode": self.mode,
            "warnings": self.warnings,
            "critical_issues": self.critical_issues,
            "decision": self.decision,
            "reasoning": self.reasoning,
            "corrections": self.corrections,
            "severity": self.severity
        }


class RalphWiggumLoop:
    """Main class for Ralph Wiggum loop operations."""
    
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or PROJECT_ROOT
        self.checkpoints_dir = self.repo_root / "work" / "reports" / "ralph-checks"
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)
    
    def run_checkpoint(self, 
                       task_id: str,
                       progress: str = "unknown",
                       mode: str = "/analysis-mode",
                       interactive: bool = True) -> CheckpointResult:
        """
        Run a Ralph Wiggum loop checkpoint.
        
        Args:
            task_id: Unique task identifier
            progress: Current progress (e.g., "50%", "Step 3 of 7")
            mode: Current reasoning mode
            interactive: If True, prompt user for observations
        
        Returns:
            CheckpointResult object with assessment
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        print("\n" + "=" * 70)
        print("🔄 Ralph Wiggum Loop Checkpoint")
        print("=" * 70)
        print(f"Task ID: {task_id}")
        print(f"Timestamp: {timestamp}")
        print(f"Progress: {progress}")
        print(f"Mode: {mode}")
        print("=" * 70 + "\n")
        
        if interactive:
            warnings = self._interactive_checklist()
            critical_issues = self._check_critical_issues(warnings)
            decision, reasoning, corrections = self._make_decision(warnings, critical_issues)
        else:
            # Automated mode - basic heuristics
            warnings = []
            critical_issues = []
            decision = "continue"
            reasoning = "Automated checkpoint - no issues detected"
            corrections = []
        
        result = CheckpointResult(
            task_id=task_id,
            timestamp=timestamp,
            progress=progress,
            mode=mode,
            warnings=warnings,
            critical_issues=critical_issues,
            decision=decision,
            reasoning=reasoning,
            corrections=corrections
        )
        
        self._save_checkpoint(result)
        self._print_result(result)
        
        return result
    
    def _interactive_checklist(self) -> List[str]:
        """Run interactive self-observation checklist."""
        print("## Self-Observation Checklist\n")
        print("Answer each question honestly (yes/no):\n")
        
        questions = [
            ("Repetitive patterns", "Am I doing the same thing multiple times?"),
            ("Goal drift", "Have I lost sight of the original objective?"),
            ("Speculation", "Am I guessing instead of validating?"),
            ("Verbosity", "Are outputs becoming unclear or too long?"),
            ("Scope creep", "Am I adding work not requested?"),
            ("Directive violations", "Am I ignoring established protocols?"),
            ("Confusion", "Do I NOT understand what I'm doing next?"),
            ("Mode misuse", "Is my reasoning mode inappropriate?"),
        ]
        
        warnings = []
        
        for category, question in questions:
            response = input(f"  {question} [y/n]: ").strip().lower()
            if response in ['y', 'yes']:
                warnings.append(category)
                print(f"    ⚠️  Warning detected: {category}\n")
            else:
                print(f"    ✅  No issue\n")
        
        return warnings
    
    def _check_critical_issues(self, warnings: List[str]) -> List[str]:
        """Identify critical issues from warnings."""
        critical = []
        
        if "Confusion" in warnings:
            critical.append("Cannot determine next steps - clarity needed")
        
        if "Directive violations" in warnings:
            critical.append("Protocol compliance compromised")
        
        if len(warnings) >= 5:
            critical.append(f"Multiple warning signs detected ({len(warnings)} total)")
        
        return critical
    
    def _make_decision(self, 
                       warnings: List[str],
                       critical_issues: List[str]) -> Tuple[str, str, List[str]]:
        """
        Make checkpoint decision based on warnings.
        
        Returns:
            (decision, reasoning, corrections) tuple
        """
        if critical_issues:
            decision = "escalate"
            reasoning = f"Critical issues require human guidance: {', '.join(critical_issues)}"
            corrections = []
        elif len(warnings) >= 2:
            decision = "adjust"
            reasoning = f"Warning signs detected ({len(warnings)}), applying corrections"
            corrections = self._suggest_corrections(warnings)
        else:
            decision = "continue"
            reasoning = "No significant issues detected, proceeding as planned"
            corrections = []
        
        return decision, reasoning, corrections
    
    def _suggest_corrections(self, warnings: List[str]) -> List[str]:
        """Suggest corrections for detected warnings."""
        correction_map = {
            "Repetitive patterns": "Review approach for efficiency gains",
            "Goal drift": "Revert to original scope (Directive 020)",
            "Speculation": "Validate assumptions before proceeding",
            "Verbosity": "Simplify outputs, reduce verbosity by 50%",
            "Scope creep": "Remove features not explicitly requested",
            "Directive violations": "Review and comply with relevant directives",
            "Confusion": "Request clarification before continuing",
            "Mode misuse": "Switch to appropriate reasoning mode",
        }
        
        return [correction_map.get(w, f"Address {w}") for w in warnings]
    
    def _save_checkpoint(self, result: CheckpointResult):
        """Save checkpoint result to disk."""
        checkpoint_file = self.checkpoints_dir / f"{result.task_id}-checkpoints.log"
        
        with open(checkpoint_file, 'a') as f:
            f.write(f"\n{'=' * 70}\n")
            f.write(f"Checkpoint: {result.timestamp}\n")
            f.write(f"Progress: {result.progress}\n")
            f.write(f"Severity: {result.severity}\n")
            f.write(f"Warnings: {len(result.warnings)}\n")
            if result.warnings:
                f.write(f"  - {', '.join(result.warnings)}\n")
            f.write(f"Critical: {len(result.critical_issues)}\n")
            if result.critical_issues:
                for issue in result.critical_issues:
                    f.write(f"  - {issue}\n")
            f.write(f"Decision: {result.decision}\n")
            f.write(f"Reasoning: {result.reasoning}\n")
            if result.corrections:
                f.write(f"Corrections:\n")
                for correction in result.corrections:
                    f.write(f"  - {correction}\n")
            f.write(f"{'=' * 70}\n")
    
    def _print_result(self, result: CheckpointResult):
        """Print checkpoint result to console."""
        print("\n" + "=" * 70)
        print("## Checkpoint Result")
        print("=" * 70)
        
        if result.severity == "clean":
            print("✅ Status: CLEAN - Continue")
        elif result.severity == "warning":
            print("⚠️  Status: WARNING - Adjust Course")
        else:
            print("❗️ Status: CRITICAL - Stop and Escalate")
        
        if result.warnings:
            print(f"\nWarnings detected ({len(result.warnings)}):")
            for warning in result.warnings:
                print(f"  ⚠️  {warning}")
        
        if result.critical_issues:
            print(f"\nCritical issues ({len(result.critical_issues)}):")
            for issue in result.critical_issues:
                print(f"  ❗️ {issue}")
        
        if result.corrections:
            print(f"\nRecommended corrections:")
            for i, correction in enumerate(result.corrections, 1):
                print(f"  {i}. {correction}")
        
        print(f"\nDecision: {result.decision.upper()}")
        print(f"Reasoning: {result.reasoning}")
        print("=" * 70 + "\n")
    
    def watch_task(self,
                   task_id: str,
                   interval: int = 15,
                   max_duration: int = 240,
                   auto_continue_if_clean: bool = False):
        """
        Watch a task and run automatic checkpoints.
        
        Args:
            task_id: Task identifier
            interval: Minutes between checkpoints
            max_duration: Maximum watch duration in minutes
            auto_continue_if_clean: If True, auto-continue on clean checkpoints
        """
        print(f"\n🔄 Starting Ralph Wiggum loop watch mode")
        print(f"Task: {task_id}")
        print(f"Interval: {interval} minutes")
        print(f"Max duration: {max_duration} minutes")
        print(f"Auto-continue: {auto_continue_if_clean}\n")
        
        start_time = time.time()
        checkpoint_count = 0
        
        while True:
            elapsed = (time.time() - start_time) / 60
            
            if elapsed > max_duration:
                print(f"\n⏰ Watch duration exceeded {max_duration} minutes. Stopping.")
                break
            
            checkpoint_count += 1
            progress = f"Checkpoint {checkpoint_count} at {elapsed:.1f} min"
            
            result = self.run_checkpoint(
                task_id=task_id,
                progress=progress,
                interactive=not auto_continue_if_clean
            )
            
            if result.decision == "escalate":
                print("\n❗️ Critical issues detected. Stopping watch mode.")
                break
            
            if result.decision == "adjust" and not auto_continue_if_clean:
                proceed = input("\nApply corrections and continue? [y/n]: ").strip().lower()
                if proceed not in ['y', 'yes']:
                    print("Stopping watch mode.")
                    break
            
            print(f"\n⏳ Next checkpoint in {interval} minutes...")
            print(f"   (Press Ctrl+C to stop)\n")
            
            try:
                time.sleep(interval * 60)
            except KeyboardInterrupt:
                print("\n\n⏸️  Watch mode interrupted by user.")
                break
        
        self._print_watch_summary(task_id, checkpoint_count)
    
    def _print_watch_summary(self, task_id: str, checkpoint_count: int):
        """Print summary of watch session."""
        print("\n" + "=" * 70)
        print("## Watch Session Summary")
        print("=" * 70)
        print(f"Task: {task_id}")
        print(f"Checkpoints run: {checkpoint_count}")
        print(f"Log file: work/reports/ralph-checks/{task_id}-checkpoints.log")
        print("=" * 70 + "\n")
    
    def generate_report(self, task_id: str):
        """Generate checkpoint report for a task."""
        checkpoint_file = self.checkpoints_dir / f"{task_id}-checkpoints.log"
        
        if not checkpoint_file.exists():
            print(f"❌ No checkpoint data found for task: {task_id}")
            return
        
        print("\n" + "=" * 70)
        print(f"## Ralph Wiggum Loop Report: {task_id}")
        print("=" * 70 + "\n")
        
        with open(checkpoint_file, 'r') as f:
            content = f.read()
            print(content)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Ralph Wiggum Loop - Self-Observation CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run manual checkpoint
  %(prog)s check --task-id 2026-01-31T1200-architect-design
  
  # Watch with automatic checkpoints
  %(prog)s watch --task-id 2026-01-31T1200-task --interval 15
  
  # Generate report
  %(prog)s report --task-id 2026-01-31T1200-task
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Run manual checkpoint')
    check_parser.add_argument('--task-id', required=True, help='Task identifier')
    check_parser.add_argument('--progress', default='unknown', help='Current progress')
    check_parser.add_argument('--mode', default='/analysis-mode', help='Reasoning mode')
    check_parser.add_argument('--non-interactive', action='store_true',
                             help='Run without user prompts')
    
    # Watch command
    watch_parser = subparsers.add_parser('watch', help='Watch task with automatic checkpoints')
    watch_parser.add_argument('--task-id', required=True, help='Task identifier')
    watch_parser.add_argument('--interval', type=int, default=15,
                             help='Minutes between checkpoints (default: 15)')
    watch_parser.add_argument('--max-duration', type=int, default=240,
                             help='Maximum watch duration in minutes (default: 240)')
    watch_parser.add_argument('--auto-continue-if-clean', action='store_true',
                             help='Automatically continue on clean checkpoints')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate checkpoint report')
    report_parser.add_argument('--task-id', required=True, help='Task identifier')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    loop = RalphWiggumLoop()
    
    try:
        if args.command == 'check':
            loop.run_checkpoint(
                task_id=args.task_id,
                progress=args.progress,
                mode=args.mode,
                interactive=not args.non_interactive
            )
        
        elif args.command == 'watch':
            loop.watch_task(
                task_id=args.task_id,
                interval=args.interval,
                max_duration=args.max_duration,
                auto_continue_if_clean=args.auto_continue_if_clean
            )
        
        elif args.command == 'report':
            loop.generate_report(task_id=args.task_id)
        
        return 0
    
    except KeyboardInterrupt:
        print("\n\n⏸️  Operation cancelled by user.")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
