# Next Batch Options - Post M4 Batch 4.1

**Decision Point:** 2026-02-05 19:30:00 UTC  
**Previous Batch:** M4 Batch 4.1 - Rich CLI + Template Generation (✅ COMPLETE)  
**Decision Maker:** Human-in-Charge  
**Planning Context:** Two strong options with different strategic value

---

## Executive Summary

M4 Batch 4.1 delivered exceptional results (⭐⭐⭐⭐⭐ architect-approved). We now have two high-value paths forward:

1. **Option A: M4 Batch 4.2 (Dashboard MVP)** - Continue UX momentum
2. **Option B: M3 Batch 3.2 (Policy Engine)** - Prioritize cost optimization

Both are Human-Priority ⭐⭐⭐⭐⭐ items. Choice depends on current business priorities.

---

## Option A: M4 Batch 4.2 - Dashboard MVP

**Batch:** M4 Batch 4.2 - Real-Time Execution Dashboard  
**Milestone:** Milestone 4 - User Experience Enhancements  
**Status:** 🟡 READY TO START  
**Estimated Duration:** 12-16 hours  
**Priority:** ⭐⭐⭐⭐⭐ HUMAN PRIORITY (Dashboard)

### Strategic Value

**Pros:**
- 🎯 Maintains M4 momentum (capitalize on fresh UX foundation)
- 🎯 Real-time visibility into agent operations (high stakeholder value)
- 🎯 File-based task tracking (aligns with audit trail requirements)
- 🎯 Immediate user feedback on progress/costs
- 🎯 Builds on completed Rich CLI infrastructure

**Cons:**
- ⚠️ Requires 12-16 hours (larger batch)
- ⚠️ Adds Flask/SocketIO dependencies
- ⚠️ Cost optimization delayed until after dashboard

### Description

Implement real-time web dashboard for monitoring agent execution, costs, and task status using file-based tracking (no database for tasks).

### Key Deliverables

1. **Backend Infrastructure** (6-8 hours)
   - Flask + Flask-SocketIO server
   - File watcher for YAML task files
   - WebSocket event system
   - SQLite telemetry integration
   
2. **Frontend Dashboard** (6-8 hours)
   - Single-page web interface
   - Live execution view
   - Cost tracking dashboard
   - Task Kanban board (inbox → assigned → done)
   - Real-time metrics visualization

### Acceptance Criteria

- ✅ Dashboard displays active operations in real-time
- ✅ Cost metrics update live (tokens, costs, model usage)
- ✅ Task board reflects file system state (YAML watching)
- ✅ WebSocket connections handle disconnects gracefully
- ✅ No database for tasks (file-based only)
- ✅ Works with existing telemetry infrastructure
- ✅ Test coverage >80%

### Dependencies

- ✅ M4 Batch 4.1 (Rich CLI) - COMPLETE
- ✅ M2 Telemetry (SQLite cost tracking) - COMPLETE
- ✅ File-based orchestration - ESTABLISHED

### References

- [ADR-032: Real-Time Execution Dashboard](../architecture/adrs/ADR-032-real-time-execution-dashboard.md)
- [M4 Batch 4.1 Review](../../work/reports/architecture/2026-02-05-M4-batch-4.1-executive-summary.md)

---

## Option B: M3 Batch 3.2 - Policy Engine Implementation

**Batch:** M3 Batch 3.2 - Policy Engine + Cost Optimization  
**Milestone:** Milestone 3 - Telemetry & Cost Optimization  
**Status:** 🟡 READY TO START  
**Estimated Duration:** 8-12 hours  
**Priority:** ⭐⭐⭐⭐⭐ HUMAN PRIORITY (Cost Optimization)

### Strategic Value

**Pros:**
- 💰 Unlocks 30-56% cost reduction (core value proposition)
- 💰 $3,000-$6,000 annual savings per team
- 💰 Smart model selection based on task complexity
- 💰 Budget enforcement (soft/hard limits)
- 💰 Completes M3 milestone (cost optimization)

**Cons:**
- ⚠️ Requires policy configuration complexity
- ⚠️ Breaks M4 UX momentum
- ⚠️ Dashboard visibility delayed

### Description

Implement intelligent routing policies for cost optimization, budget enforcement, and smart model selection based on task characteristics.

### Key Deliverables

1. **Policy Engine Core** (4-6 hours)
   - Policy evaluation engine
   - Rule-based routing decisions
   - Budget tracking and enforcement
   - Cost threshold triggers
   
2. **Policy Configuration** (2-3 hours)
   - YAML policy schema
   - Policy validation
   - Default policy templates
   - Policy testing framework
   
3. **Integration & Testing** (2-3 hours)
   - Integrate with routing engine
   - Add telemetry hooks
   - Cost optimization tests
   - End-to-end validation

### Acceptance Criteria

- ✅ Policies route requests based on cost thresholds
- ✅ Budget enforcement (soft/hard limits) works
- ✅ Smart model selection (task complexity → model tier)
- ✅ Policy configuration validates correctly
- ✅ Measurable cost reduction in test scenarios
- ✅ Test coverage >90%
- ✅ Zero performance degradation

### Dependencies

- ✅ M2 Routing Engine - COMPLETE
- ✅ M2 Telemetry (cost tracking) - COMPLETE
- 📋 M3 Batch 3.1 - Token usage tracking (if not complete)

### References

- [ADR-026: Routing Engine](../architecture/adrs/ADR-026-routing-engine-design.md)
- [Cost Optimization Prestudy](../architecture/design/llm-service-layer-prestudy.md)

---

## Recommendation Matrix

| Factor | Option A (Dashboard) | Option B (Policy Engine) |
|--------|---------------------|------------------------|
| **Business Value** | High (visibility) | Very High (cost savings) |
| **User Impact** | Immediate (dashboard) | Delayed (needs dashboard to see) |
| **ROI Timeline** | Long (visibility benefit) | Short (immediate cost reduction) |
| **Technical Risk** | Medium (new dependencies) | Low (extends existing systems) |
| **Complexity** | High (frontend + backend) | Medium (backend only) |
| **Time Investment** | 12-16 hours | 8-12 hours |
| **Strategic Fit** | UX enhancement path | Core value proposition |

---

## Decision Factors

### Choose Option A (Dashboard) if:

✅ Real-time visibility is top priority  
✅ Stakeholder demos are imminent  
✅ UX momentum is strategically valuable  
✅ Team capacity is available (12-16 hours)  
✅ Cost optimization can wait 1-2 weeks

### Choose Option B (Policy Engine) if:

✅ Cost reduction is immediate business need  
✅ ROI justification is priority  
✅ Want to complete M3 milestone  
✅ Prefer smaller batch (8-12 hours)  
✅ Can live without dashboard for now

---

## Planning Petra's Recommendation

**Primary Recommendation:** **Option B (Policy Engine)** for the following reasons:

1. **Core Value Proposition**: Cost optimization is the primary business driver ($3-6K annual savings)
2. **Faster ROI**: Delivers measurable cost reduction immediately
3. **Smaller Batch**: 8-12 hours vs 12-16 hours (lower risk)
4. **Completes Milestone**: Closes out M3 (telemetry + cost optimization)
5. **Dashboard Enhancement**: Dashboard will be MORE valuable with cost data to display

**Secondary Option:** **Option A (Dashboard)** if immediate visibility is critical for stakeholder engagement.

---

## Next Steps

**Human-in-Charge Decision Required:**

1. Select Option A or Option B based on business priorities
2. Confirm timeline and resource allocation
3. Planning Petra will update `NEXT_BATCH.md` accordingly
4. Relevant agents will receive task assignments

**Questions for Human-in-Charge:**

- What is current priority: visibility or cost reduction?
- Are there upcoming demos/reviews that need dashboard?
- Is there budget pressure that needs immediate optimization?
- What is team capacity over next 2 weeks?

---

**Document Owner:** Planning Petra  
**Created:** 2026-02-05 19:30:00 UTC  
**Status:** 🟡 AWAITING DECISION
