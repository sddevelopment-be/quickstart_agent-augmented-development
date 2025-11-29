#!/usr/bin/env python3
"""
Aggregate Iteration Metrics Script

Analyzes iteration summaries, task completions, and token usage to surface
trends in framework health, completion rates, and agent utilization.

Data Sources:
- work/collaboration/ITERATION_*_SUMMARY.md
- work/metrics/token-metrics-*.json
- work/done/**/*.yaml

Output Formats:
- Markdown report with ASCII charts
- JSON for programmatic consumption

Author: DevOps Danny (Build Automation)
Version: 1.0.0
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class IterationMetrics:
    """Metrics for a single iteration."""
    iteration_number: int
    date: str
    duration_minutes: int
    tasks_completed: int
    tasks_target: int
    agents_utilized: int
    artifacts_created: int
    work_logs_generated: int
    validation_success_rate: float
    errors: int
    framework_health_score: Optional[float] = None
    architectural_alignment: Optional[float] = None
    token_usage: Optional[int] = None
    agent_breakdown: Dict[str, int] = field(default_factory=dict)
    
    @property
    def completion_rate(self) -> float:
        """Calculate task completion rate."""
        if self.tasks_target == 0:
            return 0.0
        return (self.tasks_completed / self.tasks_target) * 100.0
    
    @property
    def avg_duration_per_task(self) -> float:
        """Calculate average duration per task in minutes."""
        if self.tasks_completed == 0:
            return 0.0
        return self.duration_minutes / self.tasks_completed


@dataclass
class AgentMetrics:
    """Metrics for agent utilization across iterations."""
    name: str
    total_tasks: int = 0
    total_duration_minutes: int = 0
    total_tokens: int = 0
    iterations_active: List[int] = field(default_factory=list)
    
    @property
    def avg_duration_per_task(self) -> float:
        """Average duration per task."""
        if self.total_tasks == 0:
            return 0.0
        return self.total_duration_minutes / self.total_tasks


class IterationMetricsAnalyzer:
    """Analyzes iteration summaries and surfaces trends."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.iterations: List[IterationMetrics] = []
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.token_data: Dict[str, dict] = {}
        
    def load_iteration_summaries(self) -> None:
        """Load and parse all ITERATION_*_SUMMARY.md files."""
        collab_dir = self.repo_root / "work" / "collaboration"
        summary_files = sorted(collab_dir.glob("ITERATION_*_SUMMARY.md"))
        
        for summary_file in summary_files:
            metrics = self._parse_iteration_summary(summary_file)
            if metrics:
                self.iterations.append(metrics)
                
        self.iterations.sort(key=lambda x: x.iteration_number)
    
    def _parse_iteration_summary(self, filepath: Path) -> Optional[IterationMetrics]:
        """Parse a single iteration summary file."""
        try:
            content = filepath.read_text()
            
            # Extract iteration number from filename
            match = re.search(r"ITERATION_(\d+)_SUMMARY", filepath.name)
            if not match:
                return None
            iteration_num = int(match.group(1))
            
            # Extract date
            date_match = re.search(r"\*\*Date:\*\* (\d{4}-\d{2}-\d{2})", content)
            date = date_match.group(1) if date_match else "unknown"
            
            # Extract metrics from table
            duration = self._extract_metric(content, r"\| Duration \| ([^|]+) \|")
            tasks_completed = self._extract_metric(content, r"\| Tasks Completed \| (\d+)/(\d+)")
            agents_utilized = self._extract_metric(content, r"\| Agents Utilized \| (\d+)")
            artifacts_created = self._extract_metric(content, r"\| Artifacts Created \| (\d+)")
            work_logs = self._extract_metric(content, r"\| Work Logs Generated \| (\d+)")
            validation = self._extract_metric(content, r"\| Validation Success \| (\d+)%")
            errors = self._extract_metric(content, r"\| Errors \| (\d+)")
            
            # Parse duration (can be in minutes or hours)
            duration_minutes = self._parse_duration(duration)
            
            # Parse tasks completed (format: "3/3" or "5/5")
            completed, target = 0, 0
            if isinstance(tasks_completed, tuple):
                completed = int(tasks_completed[0])
                target = int(tasks_completed[1])
            
            # Extract optional advanced metrics
            health_score = self._extract_optional_metric(content, r"\| Framework Health Score \| (\d+)/100")
            alignment = self._extract_optional_metric(content, r"\| Architectural Alignment \| ([\d.]+)%")
            
            # Extract agent breakdown
            agent_breakdown = self._extract_agent_breakdown(content)
            
            return IterationMetrics(
                iteration_number=iteration_num,
                date=date,
                duration_minutes=duration_minutes,
                tasks_completed=completed,
                tasks_target=target,
                agents_utilized=int(agents_utilized) if agents_utilized else 0,
                artifacts_created=int(artifacts_created) if artifacts_created else 0,
                work_logs_generated=int(work_logs) if work_logs else 0,
                validation_success_rate=float(validation) if validation else 100.0,
                errors=int(errors) if errors else 0,
                framework_health_score=float(health_score) if health_score else None,
                architectural_alignment=float(alignment) if alignment else None,
                agent_breakdown=agent_breakdown
            )
            
        except Exception as e:
            print(f"⚠️ Error parsing {filepath.name}: {e}", file=sys.stderr)
            return None
    
    def _extract_metric(self, content: str, pattern: str) -> Optional[str]:
        """Extract a metric using regex pattern."""
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.groups() if len(match.groups()) > 1 else match.group(1)
        return None
    
    def _extract_optional_metric(self, content: str, pattern: str) -> Optional[float]:
        """Extract optional metric, return None if not found."""
        match = re.search(pattern, content, re.IGNORECASE)
        return float(match.group(1)) if match else None
    
    def _parse_duration(self, duration_str: Optional[str]) -> int:
        """Parse duration string to minutes."""
        if not duration_str:
            return 0
        
        duration_str = duration_str.strip().lower()
        
        # Handle formats like "16 minutes", "~350 minutes (~5.8 hours)", "12 min"
        minutes_match = re.search(r"~?(\d+)\s*min", duration_str)
        if minutes_match:
            return int(minutes_match.group(1))
        
        hours_match = re.search(r"(\d+\.?\d*)\s*hour", duration_str)
        if hours_match:
            return int(float(hours_match.group(1)) * 60)
        
        return 0
    
    def _extract_agent_breakdown(self, content: str) -> Dict[str, int]:
        """Extract agent activity breakdown from summary."""
        agent_breakdown = {}
        
        # Look for agent activity summary sections (adjust boundary to next section or end)
        agent_section = re.search(
            r"## Agent Activity Summary\s*\n(.+?)(?:\n## |\Z)",
            content,
            re.DOTALL
        )
        
        if agent_section:
            section_text = agent_section.group(1)
            # Extract agent names and task counts
            # Pattern: ### AgentName (PersonName) \n - **Tasks Completed**: N (details)
            for match in re.finditer(
                r"### ([^\n]+)\n- \*\*Tasks Completed\*\*: (\d+)",
                section_text
            ):
                full_agent_name = match.group(1).strip()
                task_count = int(match.group(2))
                
                # Clean up agent name - extract just the role name before parenthesis
                agent_name = re.sub(r'\s*\([^)]*\)', '', full_agent_name).strip()
                
                # Skip non-agent sections like "Agent Performance Observations"
                if "observations" not in agent_name.lower() and "performance" not in agent_name.lower():
                    agent_breakdown[agent_name] = task_count
        
        return agent_breakdown
    
    def load_token_metrics(self) -> None:
        """Load token metrics from JSON files."""
        metrics_dir = self.repo_root / "work" / "metrics"
        json_files = sorted(metrics_dir.glob("token-metrics-*.json"))
        
        for json_file in json_files:
            try:
                data = json.loads(json_file.read_text())
                date = data.get("report_metadata", {}).get("report_date", "unknown")
                self.token_data[date] = data
            except Exception as e:
                print(f"⚠️ Error loading {json_file.name}: {e}", file=sys.stderr)
    
    def aggregate_agent_metrics(self) -> None:
        """Aggregate agent utilization across all iterations."""
        for iteration in self.iterations:
            for agent_name, task_count in iteration.agent_breakdown.items():
                if agent_name not in self.agent_metrics:
                    self.agent_metrics[agent_name] = AgentMetrics(name=agent_name)
                
                agent = self.agent_metrics[agent_name]
                agent.total_tasks += task_count
                agent.iterations_active.append(iteration.iteration_number)
        
        # Enrich with token data if available
        for date, token_data in self.token_data.items():
            per_agent = token_data.get("per_agent_metrics", {})
            for agent_name, metrics in per_agent.items():
                if agent_name in self.agent_metrics:
                    self.agent_metrics[agent_name].total_tokens += metrics.get("total_tokens", 0)
    
    def generate_report(self, output_format: str = "markdown") -> str:
        """Generate aggregated metrics report."""
        if output_format == "json":
            return self._generate_json_report()
        else:
            return self._generate_markdown_report()
    
    def _generate_json_report(self) -> str:
        """Generate JSON format report."""
        report = {
            "generated_at": datetime.now().isoformat() + "Z",
            "iterations": [
                {
                    "iteration": it.iteration_number,
                    "date": it.date,
                    "duration_minutes": it.duration_minutes,
                    "tasks_completed": it.tasks_completed,
                    "tasks_target": it.tasks_target,
                    "completion_rate": round(it.completion_rate, 2),
                    "agents_utilized": it.agents_utilized,
                    "artifacts_created": it.artifacts_created,
                    "work_logs_generated": it.work_logs_generated,
                    "validation_success_rate": it.validation_success_rate,
                    "errors": it.errors,
                    "framework_health_score": it.framework_health_score,
                    "architectural_alignment": it.architectural_alignment,
                    "avg_duration_per_task": round(it.avg_duration_per_task, 2),
                    "agent_breakdown": it.agent_breakdown
                }
                for it in self.iterations
            ],
            "agent_summary": {
                agent_name: {
                    "total_tasks": agent.total_tasks,
                    "total_tokens": agent.total_tokens,
                    "iterations_active": agent.iterations_active,
                    "avg_duration_per_task": round(agent.avg_duration_per_task, 2)
                }
                for agent_name, agent in self.agent_metrics.items()
            },
            "trends": self._calculate_trends()
        }
        return json.dumps(report, indent=2)
    
    def _generate_markdown_report(self) -> str:
        """Generate Markdown format report with ASCII charts."""
        lines = []
        lines.append("# Iteration Metrics Dashboard")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        lines.append(f"**Iterations Analyzed:** {len(self.iterations)}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Summary statistics
        lines.append("## Summary Statistics")
        lines.append("")
        if self.iterations:
            total_tasks = sum(it.tasks_completed for it in self.iterations)
            avg_completion_rate = sum(it.completion_rate for it in self.iterations) / len(self.iterations)
            total_artifacts = sum(it.artifacts_created for it in self.iterations)
            avg_duration = sum(it.duration_minutes for it in self.iterations) / len(self.iterations)
            
            lines.append(f"- **Total Tasks Completed:** {total_tasks}")
            lines.append(f"- **Average Completion Rate:** {avg_completion_rate:.1f}%")
            lines.append(f"- **Total Artifacts Created:** {total_artifacts}")
            lines.append(f"- **Average Iteration Duration:** {avg_duration:.1f} minutes")
            lines.append(f"- **Total Errors:** {sum(it.errors for it in self.iterations)}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Iteration-by-iteration metrics
        lines.append("## Iteration Details")
        lines.append("")
        lines.append("| Iter | Date | Duration | Tasks | Completion | Agents | Artifacts | Errors | Health |")
        lines.append("|------|------|----------|-------|------------|--------|-----------|--------|--------|")
        
        for it in self.iterations:
            health = f"{it.framework_health_score:.0f}/100" if it.framework_health_score else "N/A"
            lines.append(
                f"| {it.iteration_number} | {it.date} | {it.duration_minutes}m | "
                f"{it.tasks_completed}/{it.tasks_target} | {it.completion_rate:.0f}% | "
                f"{it.agents_utilized} | {it.artifacts_created} | {it.errors} | {health} |"
            )
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Completion rate trend
        lines.append("## Trends")
        lines.append("")
        lines.append("### Completion Rate Over Time")
        lines.append("")
        lines.append("```")
        lines.extend(self._ascii_chart(
            [it.completion_rate for it in self.iterations],
            [f"Iter {it.iteration_number}" for it in self.iterations],
            "Completion %",
            max_value=100
        ))
        lines.append("```")
        lines.append("")
        
        # Average duration trend
        lines.append("### Average Duration per Task (minutes)")
        lines.append("")
        lines.append("```")
        lines.extend(self._ascii_chart(
            [it.avg_duration_per_task for it in self.iterations],
            [f"Iter {it.iteration_number}" for it in self.iterations],
            "Minutes"
        ))
        lines.append("```")
        lines.append("")
        
        # Agent utilization
        lines.append("### Agent Utilization Summary")
        lines.append("")
        lines.append("| Agent | Total Tasks | Iterations Active | Avg Tokens/Task |")
        lines.append("|-------|-------------|-------------------|-----------------|")
        
        for agent_name in sorted(self.agent_metrics.keys()):
            agent = self.agent_metrics[agent_name]
            avg_tokens = agent.total_tokens / agent.total_tasks if agent.total_tasks > 0 else 0
            iterations_str = ", ".join(str(i) for i in agent.iterations_active)
            lines.append(
                f"| {agent_name} | {agent.total_tasks} | {iterations_str} | "
                f"{avg_tokens:,.0f} |"
            )
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Framework health trend (if available)
        health_scores = [it.framework_health_score for it in self.iterations if it.framework_health_score]
        if health_scores:
            lines.append("### Framework Health Score Over Time")
            lines.append("")
            lines.append("```")
            lines.extend(self._ascii_chart(
                health_scores,
                [f"Iter {it.iteration_number}" for it in self.iterations if it.framework_health_score],
                "Score",
                max_value=100
            ))
            lines.append("```")
            lines.append("")
        
        # Token usage trends
        if any(agent.total_tokens > 0 for agent in self.agent_metrics.values()):
            lines.append("### Token Usage by Agent")
            lines.append("")
            lines.append("```")
            token_counts = [(agent.name, agent.total_tokens) for agent in self.agent_metrics.values()]
            token_counts.sort(key=lambda x: x[1], reverse=True)
            
            max_tokens = max(t[1] for t in token_counts) if token_counts else 1
            for agent_name, tokens in token_counts[:10]:  # Top 10
                bar_length = int((tokens / max_tokens) * 40)
                bar = "█" * bar_length
                lines.append(f"{agent_name:20s} {bar} {tokens:,}")
            lines.append("```")
            lines.append("")
        
        # Common patterns section
        lines.append("---")
        lines.append("")
        lines.append("## Key Insights")
        lines.append("")
        trends = self._calculate_trends()
        
        for insight in trends.get("insights", []):
            lines.append(f"- {insight}")
        lines.append("")
        
        return "\n".join(lines)
    
    def _ascii_chart(self, values: List[float], labels: List[str], 
                     y_label: str, max_value: Optional[float] = None) -> List[str]:
        """Generate ASCII bar chart."""
        lines = []
        
        if not values:
            lines.append("No data available")
            return lines
        
        chart_width = 50
        max_val = max_value if max_value else max(values)
        
        if max_val == 0:
            max_val = 1
        
        for label, value in zip(labels, values):
            bar_length = int((value / max_val) * chart_width)
            bar = "█" * bar_length
            lines.append(f"{label:10s} │ {bar} {value:.1f}")
        
        return lines
    
    def _calculate_trends(self) -> dict:
        """Calculate trend insights."""
        insights = []
        
        if len(self.iterations) < 2:
            return {"insights": ["Not enough data for trend analysis (need at least 2 iterations)"]}
        
        # Completion rate trend
        completion_rates = [it.completion_rate for it in self.iterations]
        if completion_rates[-1] > completion_rates[0]:
            insights.append(f"✅ Completion rate improving: {completion_rates[0]:.0f}% → {completion_rates[-1]:.0f}%")
        elif completion_rates[-1] < completion_rates[0]:
            insights.append(f"⚠️ Completion rate declining: {completion_rates[0]:.0f}% → {completion_rates[-1]:.0f}%")
        else:
            insights.append(f"→ Completion rate stable at {completion_rates[-1]:.0f}%")
        
        # Duration trend
        durations = [it.avg_duration_per_task for it in self.iterations]
        if durations[-1] < durations[0]:
            insights.append(f"✅ Task duration decreasing: {durations[0]:.1f}m → {durations[-1]:.1f}m per task")
        elif durations[-1] > durations[0]:
            insights.append(f"⚠️ Task duration increasing: {durations[0]:.1f}m → {durations[-1]:.1f}m per task")
        
        # Error trend
        error_counts = [it.errors for it in self.iterations]
        total_errors = sum(error_counts)
        if total_errors == 0:
            insights.append("✅ Zero errors across all iterations")
        else:
            insights.append(f"⚠️ Total errors: {total_errors}")
        
        # Agent diversity
        total_agents = len(self.agent_metrics)
        insights.append(f"📊 {total_agents} unique agents utilized across iterations")
        
        # Most active agent
        if self.agent_metrics:
            most_active = max(self.agent_metrics.values(), key=lambda a: a.total_tasks)
            insights.append(f"🏆 Most active agent: {most_active.name} ({most_active.total_tasks} tasks)")
        
        return {"insights": insights}


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Aggregate iteration metrics and surface trends",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate markdown report
  ./aggregate-iteration-metrics.py
  
  # Generate JSON output
  ./aggregate-iteration-metrics.py --format json
  
  # Save to file
  ./aggregate-iteration-metrics.py --output work/metrics/iteration-trends.md
  
  # Specify custom repository root
  ./aggregate-iteration-metrics.py --repo-root /path/to/repo
        """
    )
    
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root directory (default: current directory)"
    )
    
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (default: stdout)"
    )
    
    args = parser.parse_args()
    
    # Validate repo root
    if not args.repo_root.exists():
        print(f"❗️ Error: Repository root does not exist: {args.repo_root}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize analyzer
    analyzer = IterationMetricsAnalyzer(args.repo_root)
    
    # Load data
    print("Loading iteration summaries...", file=sys.stderr)
    analyzer.load_iteration_summaries()
    
    if not analyzer.iterations:
        print("⚠️ No iteration summaries found", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found {len(analyzer.iterations)} iterations", file=sys.stderr)
    
    print("Loading token metrics...", file=sys.stderr)
    analyzer.load_token_metrics()
    
    print("Aggregating agent metrics...", file=sys.stderr)
    analyzer.aggregate_agent_metrics()
    
    # Generate report
    print("Generating report...", file=sys.stderr)
    report = analyzer.generate_report(args.format)
    
    # Output report
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report)
        print(f"✅ Report written to: {args.output}", file=sys.stderr)
    else:
        print(report)
    
    print("✅ Analysis complete", file=sys.stderr)


if __name__ == "__main__":
    main()
