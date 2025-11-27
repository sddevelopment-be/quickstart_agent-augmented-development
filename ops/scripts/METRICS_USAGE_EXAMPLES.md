# ADR-009 Metrics Capture - Usage Examples

This document provides practical examples for using the `capture-metrics.py` script to extract and analyze orchestration metrics.

## Basic Usage

### Extract All Metrics (JSON)

```bash
# Output to stdout
python3 ops/scripts/capture-metrics.py

# Save to file
python3 ops/scripts/capture-metrics.py --output-file metrics.json
```

### Extract All Metrics (CSV)

```bash
# For spreadsheet analysis
python3 ops/scripts/capture-metrics.py \
  --output-format csv \
  --output-file metrics.csv
```

### Verbose Mode

```bash
# See processing details
python3 ops/scripts/capture-metrics.py --verbose
```

## Advanced Usage

### Time-Based Analysis

Extract metrics and filter by date using `jq`:

```bash
# Extract metrics for November 2025
python3 ops/scripts/capture-metrics.py | \
  jq '.metrics[] | select(.timestamp | startswith("2025-11"))'

# Extract metrics from last 7 days
python3 ops/scripts/capture-metrics.py | \
  jq --arg date "$(date -d '7 days ago' '+%Y-%m-%d')" \
  '.metrics[] | select(.timestamp >= $date)'
```

### Agent-Specific Analysis

```bash
# Extract metrics for specific agent
python3 ops/scripts/capture-metrics.py | \
  jq '.metrics[] | select(.agent == "synthesizer")'

# Summary for each agent
python3 ops/scripts/capture-metrics.py | \
  jq '.summary.agents'
```

### Performance Analysis

```bash
# Find longest running tasks
python3 ops/scripts/capture-metrics.py | \
  jq '.metrics | sort_by(.duration_minutes) | reverse | .[0:10] | 
      .[] | {task_id, agent, duration_minutes}'

# Calculate average duration per agent
python3 ops/scripts/capture-metrics.py | \
  jq '.summary.agents | to_entries[] | 
      {agent: .key, avg_duration: (.value.total_duration / .value.count)}'
```

### Token Usage Analysis

```bash
# Total token usage by agent
python3 ops/scripts/capture-metrics.py | \
  jq '.summary.agents | to_entries[] | 
      {agent: .key, total_tokens: .value.total_tokens}'

# Tasks with highest token usage
python3 ops/scripts/capture-metrics.py | \
  jq '.metrics | sort_by(.token_total) | reverse | .[0:10] | 
      .[] | {task_id, agent, token_total}'

# Average tokens per task
python3 ops/scripts/capture-metrics.py | \
  jq '[.metrics[] | select(.token_total != null)] | 
      length as $count | 
      (map(.token_total) | add) as $total | 
      {total_tasks: $count, average_tokens: ($total / $count)}'
```

### Artifact Productivity

```bash
# Total artifacts created per agent
python3 ops/scripts/capture-metrics.py | \
  jq '.summary.agents | to_entries[] | 
      {agent: .key, tasks: .value.count}'

# Tasks that created the most artifacts
python3 ops/scripts/capture-metrics.py | \
  jq '.metrics | sort_by(.artifacts_created) | reverse | .[0:10] | 
      .[] | {task_id, agent, artifacts_created}'
```

### Handoff Analysis

```bash
# List all handoffs
python3 ops/scripts/capture-metrics.py | \
  jq '.metrics[] | select(.next_agent != null) | 
      {task_id, from_agent: .agent, to_agent: .next_agent}'

# Total handoff count
python3 ops/scripts/capture-metrics.py | \
  jq '.summary.totals.handoffs'
```

## Integration Examples

### Generate Daily Report

```bash
#!/bin/bash
# daily-metrics-report.sh

DATE=$(date +%Y-%m-%d)
OUTPUT_DIR="work/reports/metrics/daily"
mkdir -p "$OUTPUT_DIR"

echo "Generating metrics report for $DATE..."

# Extract metrics
python3 ops/scripts/capture-metrics.py \
  --output-file "$OUTPUT_DIR/metrics-$DATE.json"

# Generate summary
python3 ops/scripts/capture-metrics.py | \
  jq '.summary' > "$OUTPUT_DIR/summary-$DATE.json"

echo "Report saved to $OUTPUT_DIR/"
```

### CSV Import to Spreadsheet

```bash
# Generate CSV for Excel/Google Sheets
python3 ops/scripts/capture-metrics.py \
  --output-format csv \
  --output-file metrics-$(date +%Y%m%d).csv

# Open with default spreadsheet app (macOS)
open metrics-*.csv

# Or upload to Google Sheets using gsheet-cli
# gsheet upload metrics-*.csv
```

### Trend Analysis

```bash
#!/bin/bash
# weekly-trend-analysis.sh

# Extract metrics for each of the last 4 weeks
for week in {0..3}; do
  START_DATE=$(date -d "$((week * 7)) days ago" +%Y-%m-%d)
  END_DATE=$(date -d "$(((week - 1) * 7)) days ago" +%Y-%m-%d)
  
  echo "Week ending $END_DATE:"
  
  python3 ops/scripts/capture-metrics.py | \
    jq --arg start "$START_DATE" --arg end "$END_DATE" '
      .metrics[] | 
      select(.timestamp >= $start and .timestamp < $end)
    ' | \
    jq -s '{
      total_tasks: length,
      total_duration: (map(.duration_minutes // 0) | add),
      total_tokens: (map(.token_total // 0) | add)
    }'
  
  echo ""
done
```

### CI/CD Integration

```bash
# In GitHub Actions workflow
- name: Extract Metrics
  run: |
    python3 ops/scripts/capture-metrics.py \
      --output-file metrics.json
    
    # Fail if no metrics found
    METRICS_COUNT=$(jq '.metrics_count' metrics.json)
    if [ "$METRICS_COUNT" -eq 0 ]; then
      echo "ERROR: No metrics extracted"
      exit 1
    fi
    
    echo "Extracted $METRICS_COUNT metrics"

- name: Upload Metrics Artifact
  uses: actions/upload-artifact@v3
  with:
    name: orchestration-metrics
    path: metrics.json
```

## Data Export Examples

### Export to SQLite

```bash
# Install sqlite3 if needed: apt-get install sqlite3

# Create database schema
sqlite3 metrics.db <<EOF
CREATE TABLE IF NOT EXISTS metrics (
  task_id TEXT PRIMARY KEY,
  agent TEXT,
  duration_minutes INTEGER,
  token_total INTEGER,
  artifacts_created INTEGER,
  artifacts_modified INTEGER,
  timestamp TEXT,
  source_type TEXT
);
EOF

# Import CSV data
python3 ops/scripts/capture-metrics.py --output-format csv --output-file /tmp/metrics.csv
sqlite3 metrics.db <<EOF
.mode csv
.import /tmp/metrics.csv metrics_temp
INSERT OR REPLACE INTO metrics SELECT * FROM metrics_temp;
DROP TABLE metrics_temp;
EOF

# Query the database
sqlite3 metrics.db "SELECT agent, COUNT(*), SUM(duration_minutes) 
                     FROM metrics 
                     GROUP BY agent;"
```

### Export to Prometheus Format

```bash
# Generate Prometheus metrics
python3 ops/scripts/capture-metrics.py | \
  jq -r '.summary.agents | to_entries[] | 
    "orchestration_tasks_total{agent=\"\(.key)\"} \(.value.count)\n" +
    "orchestration_duration_minutes_total{agent=\"\(.key)\"} \(.value.total_duration)\n" +
    "orchestration_tokens_total{agent=\"\(.key)\"} \(.value.total_tokens)"'
```

## Troubleshooting

### No Metrics Found

```bash
# Check if work logs exist
ls -la work/reports/logs/*/

# Check if task files exist
ls -la work/collaboration/done/*/

# Run with verbose mode to see what's being processed
python3 ops/scripts/capture-metrics.py --verbose
```

### Incomplete Metrics

Some work logs may not have all ADR-009 metrics. The script handles this gracefully:

```bash
# See which metrics are most commonly available
python3 ops/scripts/capture-metrics.py | \
  jq '.metrics | 
      [.[] | keys] | 
      flatten | 
      group_by(.) | 
      map({field: .[0], count: length}) | 
      sort_by(.count) | 
      reverse'
```

## Related Documentation

- [ADR-009: Orchestration Metrics and Quality Standards](../../docs/architecture/adrs/ADR-009-orchestration-metrics-standard.md)
- [Operations Scripts README](../README.md)
- [Directive 014: Work Log Creation](../../.github/agents/directives/014_worklog_creation.md)
