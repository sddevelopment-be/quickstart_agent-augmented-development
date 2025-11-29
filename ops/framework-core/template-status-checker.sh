#!/usr/bin/env bash
#
# template-status-checker.sh
# 
# Purpose: Automate status reporting for run-iteration.md issue template
# Usage:
#   bash work/scripts/template-status-checker.sh [OPTIONS]
#
# Options:
#   --validate    Check success criteria and output validation report
#   --format=json Output in JSON format
#   --help        Show this help message
#
# Examples:
#   bash work/scripts/template-status-checker.sh
#   bash work/scripts/template-status-checker.sh --validate
#   bash work/scripts/template-status-checker.sh --format=json
#
# Version: 1.0.0
# Created: 2025-11-24
# Agent: DevOps Danny (build-automation)

set -eo pipefail

# === Script Implementation ===

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default options
VALIDATE_MODE=false
OUTPUT_FORMAT="text"

# Parse arguments
for arg in "$@"; do
  case $arg in
    --validate)
      VALIDATE_MODE=true
      shift
      ;;
    --format=json)
      OUTPUT_FORMAT="json"
      shift
      ;;
    --help)
      head -n 25 "$0" | grep '^#' | grep -v '#!/' | sed 's/^# //'
      exit 0
      ;;
    *)
      echo "Unknown option: $arg"
      echo "Use --help for usage information"
      exit 1
      ;;
  esac
done

# Function: Count tasks in a directory
count_tasks() {
  local dir=$1
  local pattern="${2:-*.yaml}"
  
  if [[ "$pattern" == "*.yaml" ]]; then
    count=$(ls "$dir"/$pattern 2>/dev/null | wc -l)
  else
    count=$(find "$dir" -name "$pattern" 2>/dev/null | wc -l)
  fi
  
  echo "$count"
}

# Function: Get task breakdown by agent
get_agent_breakdown() {
  local base_dir=$1
  local agents=()
  
  if [[ -d "$base_dir" ]]; then
    for agent_dir in "$base_dir"/*/; do
      if [[ -d "$agent_dir" ]]; then
        agent_name=$(basename "$agent_dir")
        task_count=$(count_tasks "$agent_dir" "*.yaml")
        if [[ $task_count -gt 0 ]]; then
          agents+=("$agent_name:$task_count")
        fi
      fi
    done
  fi
  
  echo "${agents[@]}"
}

# Function: Check if work logs exist for recent tasks
check_work_logs() {
  local done_count=$1
  local log_count
  
  # Count logs from last 7 days
  log_count=$(find work/logs -name "*.md" -mtime -7 2>/dev/null | wc -l)
  
  if [[ $done_count -gt 0 && $log_count -ge $done_count ]]; then
    echo "true"
  else
    echo "false"
  fi
}

# Function: Check AGENT_STATUS.md age
check_agent_status() {
  local status_file="work/collaboration/AGENT_STATUS.md"
  
  if [[ ! -f "$status_file" ]]; then
    echo "missing"
    return
  fi
  
  # Check if modified in last 24 hours
  local age_hours
  age_hours=$(( ($(date +%s) - $(stat -c %Y "$status_file" 2>/dev/null || stat -f %m "$status_file" 2>/dev/null)) / 3600 ))
  
  if [[ $age_hours -lt 24 ]]; then
    echo "current"
  else
    echo "stale"
  fi
}

# Function: Validate success criteria
validate_criteria() {
  local inbox_count=$1
  local assigned_count=$2
  local done_count=$3
  
  local criteria_met=0
  local criteria_total=8
  
  echo ""
  echo "=== Success Criteria Validation ==="
  echo ""
  
  # Criterion 1: At least 1 task completed
  if [[ $done_count -gt 0 ]]; then
    echo -e "${GREEN}✓${NC} At least 1 task completed"
    criteria_met=$((criteria_met + 1))
  else
    echo -e "${RED}✗${NC} At least 1 task completed"
  fi
  
  # Criterion 2: Work logs created
  local logs_valid=$(check_work_logs "$done_count")
  if [[ "$logs_valid" == "true" ]]; then
    echo -e "${GREEN}✓${NC} Work logs created per Directive 014"
    criteria_met=$((criteria_met + 1))
  else
    echo -e "${YELLOW}⚠${NC} Work logs may be incomplete (check recent logs)"
  fi
  
  # Criterion 3: AGENT_STATUS.md updated
  local status_state=$(check_agent_status)
  if [[ "$status_state" == "current" ]]; then
    echo -e "${GREEN}✓${NC} AGENT_STATUS.md updated recently"
    criteria_met=$((criteria_met + 1))
  elif [[ "$status_state" == "stale" ]]; then
    echo -e "${YELLOW}⚠${NC} AGENT_STATUS.md may be stale (>24h)"
  else
    echo -e "${RED}✗${NC} AGENT_STATUS.md missing"
  fi
  
  # Criterion 4-8: Generic checks (would need deeper inspection)
  echo -e "${BLUE}?${NC} Iteration summary created (manual verification required)"
  echo -e "${BLUE}?${NC} Metrics captured (check work logs)"
  echo -e "${BLUE}?${NC} Framework health assessed (check iteration summary)"
  echo -e "${BLUE}?${NC} Validation errors (run validation scripts)"
  echo -e "${BLUE}?${NC} Artifacts committed (check git status)"
  
  echo ""
  echo "Automated checks: $criteria_met/$criteria_total passed"
  echo ""
}

# Main execution
main() {
  # Get task counts
  inbox_count=$(ls work/inbox/*.yaml 2>/dev/null | wc -l)
  assigned_count=$(find work/assigned -name "*.yaml" 2>/dev/null | wc -l)
  done_count=$(ls work/done/*.yaml 2>/dev/null | wc -l)
  
  # Get agent breakdowns
  assigned_agents=($(get_agent_breakdown "work/assigned"))
  
  if [[ "$OUTPUT_FORMAT" == "json" ]]; then
    # JSON output
    cat <<EOF
{
  "inbox_tasks": $inbox_count,
  "assigned_tasks": $assigned_count,
  "done_tasks": $done_count,
  "assigned_by_agent": {
EOF
    
    first=true
    for agent_info in "${assigned_agents[@]}"; do
      IFS=':' read -r agent count <<< "$agent_info"
      if [[ "$first" == true ]]; then
        first=false
      else
        echo ","
      fi
      echo -n "    \"$agent\": $count"
    done
    
    echo ""
    echo "  },"
    echo "  \"agent_status\": \"$(check_agent_status)\","
    echo "  \"work_logs_valid\": $(check_work_logs "$done_count")"
    echo "}"
  else
    # Text output
    echo ""
    echo "=== Orchestration Queue Status ==="
    echo ""
    echo "Inbox:    $inbox_count tasks"
    echo "Assigned: $assigned_count tasks"
    echo "Done:     $done_count tasks"
    echo ""
    
    if [[ ${#assigned_agents[@]} -gt 0 ]]; then
      echo "Assigned tasks by agent:"
      for agent_info in "${assigned_agents[@]}"; do
        IFS=':' read -r agent count <<< "$agent_info"
        echo "  - $agent: $count"
      done
      echo ""
    fi
    
    # Validation mode
    if [[ "$VALIDATE_MODE" == true ]]; then
      validate_criteria "$inbox_count" "$assigned_count" "$done_count"
    fi
  fi
}

main
