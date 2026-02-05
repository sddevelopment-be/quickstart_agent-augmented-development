-- SQLite Schema for LLM Service Telemetry
-- Version: 1.0.0
-- Purpose: Track LLM invocations, costs, and performance metrics

-- ============================================================================
-- Invocations Table
-- ============================================================================
-- Records every LLM invocation with full metadata for cost tracking,
-- performance analysis, and debugging.

CREATE TABLE IF NOT EXISTS invocations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invocation_id TEXT UNIQUE NOT NULL,      -- UUID for this specific invocation
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    agent_name TEXT,                         -- Which agent made the request (nullable)
    tool_name TEXT NOT NULL,                 -- Tool used (claude-code, cursor, etc.)
    model_name TEXT NOT NULL,                -- Model used (claude-3.5-sonnet, gpt-4, etc.)
    prompt_tokens INTEGER DEFAULT 0,         -- Input token count
    completion_tokens INTEGER DEFAULT 0,     -- Output token count
    total_tokens INTEGER DEFAULT 0,          -- Sum of input + output tokens
    cost_usd REAL DEFAULT 0.0,              -- Cost in USD
    latency_ms INTEGER DEFAULT 0,           -- Execution time in milliseconds
    status TEXT NOT NULL,                    -- success, error, timeout
    error_message TEXT,                      -- Error details if status = error
    privacy_level TEXT DEFAULT 'metadata'    -- metadata, full, none
);

-- ============================================================================
-- Daily Cost Aggregation Table
-- ============================================================================
-- Pre-aggregated daily statistics for fast dashboard queries.
-- Updated automatically via triggers or application logic.

CREATE TABLE IF NOT EXISTS daily_costs (
    date DATE NOT NULL,
    agent_name TEXT,
    tool_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    invocations INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    total_cost_usd REAL DEFAULT 0.0,
    PRIMARY KEY (date, agent_name, tool_name, model_name)
);

-- ============================================================================
-- Indexes for Query Performance
-- ============================================================================
-- Optimized for common query patterns:
-- 1. Time-series analysis (timestamp)
-- 2. Agent-specific reports (agent_name)
-- 3. Tool/model analysis (tool_name, model_name)
-- 4. Error tracking (status)
-- 5. Cost analysis by date

CREATE INDEX IF NOT EXISTS idx_invocations_timestamp 
    ON invocations(timestamp);

CREATE INDEX IF NOT EXISTS idx_invocations_agent 
    ON invocations(agent_name);

CREATE INDEX IF NOT EXISTS idx_invocations_tool 
    ON invocations(tool_name);

CREATE INDEX IF NOT EXISTS idx_invocations_model 
    ON invocations(model_name);

CREATE INDEX IF NOT EXISTS idx_invocations_status 
    ON invocations(status);

CREATE INDEX IF NOT EXISTS idx_daily_costs_date 
    ON daily_costs(date);

-- ============================================================================
-- Schema Version Tracking
-- ============================================================================
-- Track schema version for migrations

CREATE TABLE IF NOT EXISTS schema_version (
    version TEXT PRIMARY KEY,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

INSERT OR IGNORE INTO schema_version (version, description)
VALUES ('1.0.0', 'Initial telemetry schema with invocations and daily_costs tables');
