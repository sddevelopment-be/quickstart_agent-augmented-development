#!/usr/bin/env python3
"""
Dashboard Generation Script

Generates markdown dashboard files from metrics data captured by capture-metrics.py.
Supports multiple dashboard types: summary, detail, and trends.

Usage:
    python3 generate-dashboard.py [options]

    # Generate all dashboard types
    python3 generate-dashboard.py --input metrics.json --output-dir work/reports/dashboards/

    # Generate specific dashboard type
    python3 generate-dashboard.py --input metrics.json --dashboard-type summary

    # Update existing dashboards
    python3 generate-dashboard.py --input metrics.json --update

Examples:
    # Generate all dashboards from latest metrics
    python3 ops/scripts/capture-metrics.py --output-file /tmp/metrics.json
    python3 ops/scripts/generate-dashboard.py --input /tmp/metrics.json

    # Generate only summary dashboard to stdout
    python3 ops/scripts/generate-dashboard.py --input metrics.json --dashboard-type summary --output-file -

Author: DevOps Danny (Build Automation)
Version: 1.0.0
License: MIT
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict


class DashboardGenerator:
    """Generate markdown dashboards from metrics data."""

    def __init__(self, metrics_data: Dict[str, Any]):
        """
        Initialize dashboard generator.

        Args:
            metrics_data: Parsed metrics data from capture-metrics.py
        """
        self.metrics_data = metrics_data
        self.metrics = metrics_data.get("metrics", [])
        self.summary = metrics_data.get("summary", {})
        self.extracted_at = metrics_data.get("extracted_at", "")

    def generate_summary_dashboard(self) -> str:
        """
        Generate a high-level summary dashboard.

        Returns:
            Markdown-formatted summary dashboard
        """
        lines = []
        lines.append("# Metrics Summary Dashboard")
        lines.append("")
        lines.append(f"_Generated: {datetime.now().isoformat()}Z_")
        lines.append(f"_Data extracted: {self.extracted_at}_")
        lines.append("")

        # Overall statistics
        lines.append("## Overall Statistics")
        lines.append("")
        lines.append(f"- **Total Tasks:** {len(self.metrics)}")
        
        agents = self.summary.get('agents', {})
        totals = self.summary.get('totals', {})
        
        lines.append(f"- **Unique Agents:** {len(agents)}")
        lines.append(f"- **Total Duration:** {totals.get('duration', 0):.1f} minutes")
        lines.append(f"- **Total Tokens:** {totals.get('tokens', 0):,}")
        lines.append("")

        # Top agents by task count
        lines.append("## Top Agents by Task Count")
        lines.append("")
        
        agents = self.summary.get('agents', {})
        agent_tasks = [
            (agent, data.get('count', 0))
            for agent, data in agents.items()
        ]
        agent_tasks.sort(key=lambda x: x[1], reverse=True)
        
        if agent_tasks:
            max_count = max(t[1] for t in agent_tasks)
            for agent, count in agent_tasks[:10]:
                bar = self._generate_bar(count, max_count, 30)
                lines.append(f"- **{agent}**: {count} tasks {bar}")
        else:
            lines.append("_No agent data available_")
        lines.append("")

        # Recent activity
        lines.append("## Recent Activity (Last 10 Tasks)")
        lines.append("")
        lines.append("| Timestamp | Agent | Task ID | Duration |")
        lines.append("|-----------|-------|---------|----------|")
        
        recent_metrics = sorted(
            [m for m in self.metrics if m.get('timestamp')],
            key=lambda x: x.get('timestamp', ''), 
            reverse=True
        )[:10]
        
        for metric in recent_metrics:
            timestamp = metric.get('timestamp', 'N/A')
            agent = metric.get('agent', 'N/A')
            task_id = metric.get('task_id', 'N/A')
            duration = metric.get('duration_minutes', 'N/A')
            duration_str = f"{duration}m" if isinstance(duration, (int, float)) else duration
            
            lines.append(f"| {timestamp} | {agent} | {task_id[:40]}... | {duration_str} |")
        
        if not recent_metrics:
            lines.append("| _No recent activity_ | | | |")
        
        lines.append("")
        return "\n".join(lines)

    def generate_detail_dashboard(self) -> str:
        """
        Generate a detailed metrics dashboard with per-agent breakdowns.

        Returns:
            Markdown-formatted detail dashboard
        """
        lines = []
        lines.append("# Metrics Detail Dashboard")
        lines.append("")
        lines.append(f"_Generated: {datetime.now().isoformat()}Z_")
        lines.append(f"_Data extracted: {self.extracted_at}_")
        lines.append("")

        # Per-agent detailed metrics
        lines.append("## Per-Agent Metrics")
        lines.append("")

        agents = self.summary.get('agents', {})
        
        for agent, data in sorted(agents.items()):
            lines.append(f"### {agent}")
            lines.append("")
            
            task_count = data.get('count', 0)
            total_duration = data.get('total_duration', 0)
            total_tokens = data.get('total_tokens', 0)
            
            lines.append(f"- **Tasks Completed:** {task_count}")
            lines.append(f"- **Total Duration:** {total_duration:.1f} minutes")
            if task_count > 0 and total_duration > 0:
                avg_duration = total_duration / task_count
                lines.append(f"- **Average Duration:** {avg_duration:.1f} minutes per task")
            lines.append(f"- **Total Tokens:** {total_tokens:,}")
            if task_count > 0 and total_tokens > 0:
                avg_tokens = total_tokens / task_count
                lines.append(f"- **Average Tokens:** {avg_tokens:,.0f} per task")
            
            lines.append("")
            
            # Recent tasks for this agent
            agent_metrics = [
                m for m in self.metrics 
                if m.get('agent') == agent and m.get('timestamp')
            ]
            recent_agent_metrics = sorted(
                agent_metrics,
                key=lambda x: x.get('timestamp', ''),
                reverse=True
            )[:5]
            
            if recent_agent_metrics:
                lines.append(f"**Recent Tasks:**")
                lines.append("")
                for metric in recent_agent_metrics:
                    timestamp = metric.get('timestamp', 'N/A')
                    task_id = metric.get('task_id', 'N/A')
                    duration = metric.get('duration_minutes', '')
                    duration_str = f" ({duration}m)" if duration else ""
                    lines.append(f"- `{timestamp}` - {task_id}{duration_str}")
                lines.append("")

        if not agents:
            lines.append("_No agent data available_")
            lines.append("")

        # Artifacts statistics
        lines.append("## Artifacts Summary")
        lines.append("")
        
        total_created = sum(
            m.get('artifacts_created', 0) 
            for m in self.metrics
        )
        total_modified = sum(
            m.get('artifacts_modified', 0) 
            for m in self.metrics
        )
        
        lines.append(f"- **Total Artifacts Created:** {total_created}")
        lines.append(f"- **Total Artifacts Modified:** {total_modified}")
        lines.append("")

        return "\n".join(lines)

    def generate_trends_dashboard(self) -> str:
        """
        Generate a trends dashboard showing metrics over time.

        Returns:
            Markdown-formatted trends dashboard
        """
        lines = []
        lines.append("# Metrics Trends Dashboard")
        lines.append("")
        lines.append(f"_Generated: {datetime.now().isoformat()}Z_")
        lines.append(f"_Data extracted: {self.extracted_at}_")
        lines.append("")

        # Group metrics by date
        metrics_by_date = defaultdict(list)
        for metric in self.metrics:
            timestamp = metric.get('timestamp', '')
            if timestamp:
                date = timestamp.split('T')[0] if 'T' in timestamp else timestamp[:10]
                metrics_by_date[date].append(metric)

        # Daily activity trend
        lines.append("## Daily Activity Trend")
        lines.append("")
        
        if metrics_by_date:
            dates = sorted(metrics_by_date.keys())
            lines.append("| Date | Tasks | Avg Duration | Total Tokens |")
            lines.append("|------|-------|--------------|--------------|")
            
            for date in dates:
                day_metrics = metrics_by_date[date]
                task_count = len(day_metrics)
                
                durations = [
                    m.get('duration_minutes', 0) 
                    for m in day_metrics 
                    if m.get('duration_minutes')
                ]
                avg_duration = sum(durations) / len(durations) if durations else 0
                
                tokens = [
                    m.get('token_total', 0) 
                    for m in day_metrics 
                    if m.get('token_total')
                ]
                total_tokens = sum(tokens)
                
                lines.append(
                    f"| {date} | {task_count} | {avg_duration:.1f}m | {total_tokens:,} |"
                )
            lines.append("")
        else:
            lines.append("_No trend data available_")
            lines.append("")

        # Agent activity over time
        lines.append("## Agent Activity Timeline")
        lines.append("")
        
        # Group by agent and date
        agent_timeline = defaultdict(lambda: defaultdict(int))
        for metric in self.metrics:
            timestamp = metric.get('timestamp', '')
            agent = metric.get('agent', 'unknown')
            if timestamp:
                date = timestamp.split('T')[0] if 'T' in timestamp else timestamp[:10]
                agent_timeline[agent][date] += 1

        if agent_timeline:
            # Show most active agents
            active_agents = sorted(
                agent_timeline.items(),
                key=lambda x: sum(x[1].values()),
                reverse=True
            )[:5]
            
            for agent, dates in active_agents:
                total_tasks = sum(dates.values())
                lines.append(f"### {agent} ({total_tasks} tasks)")
                lines.append("")
                
                sorted_dates = sorted(dates.items())
                max_tasks = max(dates.values())
                
                for date, count in sorted_dates:
                    bar = self._generate_bar(count, max_tasks, 20)
                    lines.append(f"- **{date}**: {count} tasks {bar}")
                lines.append("")
        else:
            lines.append("_No timeline data available_")
            lines.append("")

        # Token usage trends
        lines.append("## Token Usage Trends")
        lines.append("")
        
        token_by_date = defaultdict(int)
        for metric in self.metrics:
            timestamp = metric.get('timestamp', '')
            tokens = metric.get('token_total', 0)
            if timestamp and tokens:
                date = timestamp.split('T')[0] if 'T' in timestamp else timestamp[:10]
                token_by_date[date] += tokens

        if token_by_date:
            sorted_dates = sorted(token_by_date.items())
            max_tokens = max(token_by_date.values())
            
            for date, tokens in sorted_dates:
                bar = self._generate_bar(tokens, max_tokens, 30)
                lines.append(f"- **{date}**: {tokens:,} tokens {bar}")
            lines.append("")
        else:
            lines.append("_No token usage data available_")
            lines.append("")

        return "\n".join(lines)

    def _generate_bar(self, value: float, max_value: float, width: int = 20) -> str:
        """
        Generate an ASCII bar chart.

        Args:
            value: Current value
            max_value: Maximum value for scaling
            width: Width of the bar in characters

        Returns:
            ASCII bar string
        """
        if max_value == 0:
            return ""
        
        filled = int((value / max_value) * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"`{bar}`"


def load_metrics(input_path: Path) -> Dict[str, Any]:
    """
    Load metrics data from JSON file.

    Args:
        input_path: Path to metrics JSON file

    Returns:
        Parsed metrics data

    Raises:
        FileNotFoundError: If input file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Metrics file not found: {input_path}")
    
    with input_path.open('r') as f:
        return json.load(f)


def save_dashboard(content: str, output_path: Optional[Path] = None) -> None:
    """
    Save dashboard content to file or stdout.

    Args:
        content: Dashboard markdown content
        output_path: Output file path (None or '-' for stdout)
    """
    if output_path is None or str(output_path) == '-':
        print(content)
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open('w') as f:
            f.write(content)
        print(f"✅ Dashboard saved to {output_path}", file=sys.stderr)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate markdown dashboards from metrics data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all dashboard types
  %(prog)s --input metrics.json --output-dir dashboards/

  # Generate specific dashboard type
  %(prog)s --input metrics.json --dashboard-type summary

  # Generate to stdout
  %(prog)s --input metrics.json --dashboard-type summary --output-file -

  # Update existing dashboards
  %(prog)s --input metrics.json --update
        """
    )
    
    parser.add_argument(
        '--input',
        type=Path,
        default=Path('work/reports/metrics/metrics.json'),
        help='Input metrics JSON file (default: work/reports/metrics/metrics.json)'
    )
    
    parser.add_argument(
        '--dashboard-type',
        choices=['summary', 'detail', 'trends', 'all'],
        default='all',
        help='Dashboard type to generate (default: all)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('work/reports/dashboards'),
        help='Output directory for dashboards (default: work/reports/dashboards)'
    )
    
    parser.add_argument(
        '--output-file',
        type=str,
        help='Output file path (use "-" for stdout, overrides --output-dir)'
    )
    
    parser.add_argument(
        '--update',
        action='store_true',
        help='Update existing dashboard files'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    try:
        # Load metrics data
        if args.verbose:
            print(f"[INFO] Loading metrics from {args.input}", file=sys.stderr)
        
        metrics_data = load_metrics(args.input)
        
        if args.verbose:
            print(
                f"[INFO] Loaded {metrics_data.get('metrics_count', 0)} metrics",
                file=sys.stderr
            )

        # Initialize generator
        generator = DashboardGenerator(metrics_data)

        # Determine output file path
        if args.output_file:
            output_path = None if args.output_file == '-' else Path(args.output_file)
        else:
            output_path = None

        # Generate dashboards
        dashboards = {
            'summary': ('summary-dashboard.md', generator.generate_summary_dashboard),
            'detail': ('detail-dashboard.md', generator.generate_detail_dashboard),
            'trends': ('trends-dashboard.md', generator.generate_trends_dashboard),
        }

        if args.dashboard_type == 'all':
            types_to_generate = dashboards.keys()
        else:
            types_to_generate = [args.dashboard_type]

        for dash_type in types_to_generate:
            filename, generator_func = dashboards[dash_type]
            
            if args.verbose:
                print(f"[INFO] Generating {dash_type} dashboard", file=sys.stderr)
            
            content = generator_func()
            
            if args.output_file:
                # Use specified output file
                save_dashboard(content, output_path)
            else:
                # Use default output directory
                final_path = args.output_dir / filename
                save_dashboard(content, final_path)

        if args.verbose:
            print("[INFO] Dashboard generation complete", file=sys.stderr)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in metrics file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
