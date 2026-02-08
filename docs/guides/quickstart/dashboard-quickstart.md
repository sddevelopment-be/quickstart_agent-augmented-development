# Dashboard Quick Start Guide

## 🚀 Launch the Dashboard

```bash
# Activate virtual environment
source /home/stijn/Documents/_code/.venv_shared/bin/activate

# Run dashboard
python run_dashboard.py
```

The dashboard will start at: **http://localhost:8080**

## 📊 What You'll See

- **Task Kanban Board**: Real-time view of tasks in inbox/assigned/done
- **Agent Status**: Current state of all agents
- **Cost Tracking**: Token usage and costs (requires telemetry data)
- **Live Updates**: WebSocket-based real-time updates (<100ms)

## 🎛️ Options

```bash
# Custom port
python run_dashboard.py --port 5000

# Debug mode (auto-reload on code changes)
python run_dashboard.py --debug

# Different watch directory
python run_dashboard.py --watch-dir /path/to/tasks

# All options
python run_dashboard.py --help
```

## 🔍 Health Check

Visit: http://localhost:8080/health

Expected response:
```json
{
  "status": "healthy",
  "service": "llm-service-dashboard",
  "timestamp": "2026-02-06T11:20:00.000Z"
}
```

## 📋 Current Features

✅ **Working Now:**
- Task file monitoring (watches `work/collaboration/` YAML files)
- Real-time WebSocket updates
- Agent status display
- Professional dark-themed UI

⚠️ **Requires M3.1 (Telemetry):**
- Cost tracking ($0.00 until telemetry implemented)
- Token usage statistics
- Model usage trends

## 🛑 Stopping the Dashboard

Press **CTRL+C** in the terminal where it's running.

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Ensure dependencies are installed
pip install -e .
```

### Can't connect to WebSocket
- Check that firewall allows localhost:8080
- Verify browser supports WebSocket (Chrome/Firefox/Edge)

### Tasks not updating
- Verify `work/collaboration/` directory exists
- Check YAML files are valid
- Look for errors in terminal output

## 📖 Documentation

Full documentation: `src/llm_service/dashboard/README.md`
Architecture: `docs/architecture/adrs/ADR-032-real-time-execution-dashboard.md`
