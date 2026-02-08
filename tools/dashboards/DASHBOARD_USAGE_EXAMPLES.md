# Dashboard Generation Usage Examples

This document provides practical examples for using `generate-dashboard.py` to create visualization dashboards from metrics data.

## Prerequisites

First, capture metrics using `capture-metrics.py`:

```bash
python3 ops/dashboards/capture-metrics.py --output-file work/reports/metrics/metrics.json
```

## Basic Usage

### Generate All Dashboard Types

Generate all three dashboard types (summary, detail, trends) to default location:

```bash
python3 ops/dashboards/generate-dashboard.py --input work/reports/metrics/metrics.json
```

Output files:
- `work/reports/dashboards/summary-dashboard.md`
- `work/reports/dashboards/detail-dashboard.md`
- `work/reports/dashboards/trends-dashboard.md`

### Generate Single Dashboard Type

Generate only the summary dashboard:

```bash
python3 ops/dashboards/generate-dashboard.py \
  --input work/reports/metrics/metrics.json \
  --dashboard-type summary
```

Available types:
- `summary` - High-level overview with top agents and recent activity
- `detail` - Per-agent detailed metrics and recent tasks
- `trends` - Historical trends and activity timelines
- `all` - Generate all three types (default)

### Output to Standard Output

View dashboard content directly without creating files:

```bash
python3 ops/dashboards/generate-dashboard.py \
  --input work/reports/metrics/metrics.json \
  --dashboard-type summary \
  --output-file -
```

## Advanced Usage

### Custom Output Directory

Save dashboards to a custom location:

```bash
python3 ops/dashboards/generate-dashboard.py \
  --input work/reports/metrics/metrics.json \
  --output-dir docs/metrics/
```

### Update Existing Dashboards

Refresh dashboards with latest data:

```bash
python3 ops/dashboards/generate-dashboard.py \
  --input work/reports/metrics/metrics.json \
  --update
```

### Verbose Mode

Enable detailed logging for troubleshooting:

```bash
python3 ops/dashboards/generate-dashboard.py \
  --input work/reports/metrics/metrics.json \
  --verbose
```

### Custom Output File

Save a specific dashboard type to a custom filename:

```bash
python3 ops/dashboards/generate-dashboard.py \
  --input work/reports/metrics/metrics.json \
  --dashboard-type trends \
  --output-file reports/weekly-trends.md
```

## Integration Workflows

### Complete Metrics Pipeline

Capture metrics and generate dashboards in one workflow:

```bash
# Capture current metrics
python3 ops/dashboards/capture-metrics.py \
  --work-dir work/ \
  --output-file work/reports/metrics/metrics.json \
  --verbose

# Generate all dashboards
python3 ops/dashboards/generate-dashboard.py \
  --input work/reports/metrics/metrics.json \
  --output-dir work/reports/dashboards/ \
  --verbose
```

### Automated Dashboard Updates

Create a script to regularly update dashboards:

```bash
#!/bin/bash
# update-dashboards.sh

# Capture latest metrics
python3 ops/dashboards/capture-metrics.py \
  --output-file /tmp/latest-metrics.json

# Update dashboards
python3 ops/dashboards/generate-dashboard.py \
  --input /tmp/latest-metrics.json \
  --update \
  --verbose

echo "Dashboards updated at $(date)"
```

### CI/CD Integration

Add to your CI/CD pipeline:

```yaml
- name: Generate Metrics Dashboards
  run: |
    python3 ops/dashboards/capture-metrics.py --output-file metrics.json
    python3 ops/dashboards/generate-dashboard.py --input metrics.json
```

## Dashboard Types Explained

### Summary Dashboard

**Purpose:** Quick overview of overall system health and activity.

**Contains:**
- Total tasks, agents, duration, and token usage
- Top 10 most active agents with bar charts
- Last 10 tasks completed

**Use Case:** Daily standup, quick status checks

**Example:**
```bash
python3 ops/dashboards/generate-dashboard.py \
  --dashboard-type summary \
  --output-file - | less
```

### Detail Dashboard

**Purpose:** Deep dive into per-agent performance and activity.

**Contains:**
- Detailed metrics for each agent
- Task completion counts and averages
- Duration and token usage per agent
- Recent tasks for each agent
- Overall artifacts summary

**Use Case:** Performance analysis, capacity planning

**Example:**
```bash
python3 ops/dashboards/generate-dashboard.py \
  --dashboard-type detail \
  --output-file reports/detail-$(date +%Y%m%d).md
```

### Trends Dashboard

**Purpose:** Historical analysis and trend identification.

**Contains:**
- Daily activity trends with metrics table
- Agent activity timeline with visual charts
- Token usage trends over time
- ASCII visualizations for patterns

**Use Case:** Sprint reviews, long-term planning, identifying patterns

**Example:**
```bash
python3 ops/dashboards/generate-dashboard.py \
  --dashboard-type trends \
  --output-dir docs/retrospectives/
```

## Troubleshooting

### No Data in Dashboard

**Problem:** Dashboard shows "No agent data available"

**Solution:** Ensure metrics file contains summary data:
```bash
python3 -c "import json; print(json.load(open('metrics.json')).get('summary'))"
```

### Missing Charts

**Problem:** ASCII bar charts not appearing

**Solution:** Verify terminal supports Unicode:
```bash
echo "█░"  # Should show filled and empty blocks
```

### File Not Found Error

**Problem:** `Metrics file not found: ...`

**Solution:** Check the input file path:
```bash
ls -l work/reports/metrics/metrics.json
```

If missing, capture metrics first:
```bash
python3 ops/dashboards/capture-metrics.py --output-file work/reports/metrics/metrics.json
```

## Sample Output

### Summary Dashboard Preview

```markdown
# Metrics Summary Dashboard

_Generated: 2025-11-27T20:30:00Z_

## Overall Statistics

- **Total Tasks:** 99
- **Unique Agents:** 9
- **Total Duration:** 700.0 minutes
- **Total Tokens:** 476,227

## Top Agents by Task Count

- **build-automation**: 27 tasks `██████████████████████████████`
- **curator**: 18 tasks `████████████████████░░░░░░░░░░`
- **architect**: 17 tasks `██████████████████░░░░░░░░░░░░`
```

## Related Documentation

- **Metrics Capture:** `ops/dashboards/capture-metrics.py` and `METRICS_USAGE_EXAMPLES.md`
- **Testing:** `ops/scripts/test-generate-dashboard.sh`
- **ADR-009:** Orchestration Metrics and Quality Standards
- **Main Documentation:** `ops/README.md`

## Support

For issues or questions:
1. Run with `--verbose` flag for detailed logging
2. Check metrics file structure: `python3 -m json.tool metrics.json | head -50`
3. Run test suite: `bash ops/scripts/test-generate-dashboard.sh`
