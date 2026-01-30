---
name: "Approach: Trunk-Based Development for Agent-First Workflows"
description: "Trunk-based development (TBD) is a branching strategy where all developers (agents and humans) commit frequently to a single shared branch (`main`), with short-lived feature branches (<24 hours) us..."
version: "1.0.0"
type: "approach"
category: "operational-pattern"
---

# Approach: Trunk-Based Development for Agent-First Workflows

Trunk-based development (TBD) is a branching strategy where all developers (agents and humans) commit frequently to a single shared branch (`main`), with short-lived feature branches (<24 hours) us...

## Instructions

Trunk-based development (TBD) is a branching strategy where all developers (agents and humans) commit frequently to a single shared branch (`main`), with short-lived feature branches (<24 hours) used only for coordinated changes. This approach minimizes merge conflicts, accelerates feedback, and aligns naturally with agent task completion patterns.

**Key principles:**

1. **Single source of truth:** `main` branch is always deployable
2. **Small, frequent commits:** Multiple commits per day
3. **Short-lived branches:** Maximum 24 hours, prefer <4 hours
4. **Continuous validation:** Every commit runs tests and checks
5. **Feature flags:** Hide incomplete work, don't hold it in branches
6. **Rapid revert:** Fix or rollback within 15 minutes of failure

**When to use trunk-based development:**

- ✅ Async multi-agent orchestration (this repository)
- ✅ Rapid iteration with frequent small changes
- ✅ Strong test coverage and automated validation
- ✅ Team comfortable with continuous integration discipline

**When to avoid:**

- ❌ Large, risky changes without adequate test coverage
- ❌ Teams without automated validation infrastructure
- ❌ Work requiring extended isolation (>24h)

---

