# Tactic: Safe-to-Fail Experiment Design

**Invoked by:**
- Directive 021 (Locality of Change) — bounded exploration and premature optimization avoidance

**Related tactics:**
- `stopping-conditions.tactic.md` — explicit exit criteria for experiments
- `premortem-risk-identification.tactic.md` — failure scenario discovery before experimentation

**Complements:**
- Approach: Locality of Change

---

## Intent

Structure exploratory work as small, reversible experiments with explicit success/failure criteria to enable learning with minimal risk. Transforms uncertain situations from paralysis ("what if I'm wrong?") to progress ("what will I learn?").

Apply when:
- High uncertainty about best approach (no clear "right answer")
- Consequences of failure are acceptable and recoverable
- Learning is more valuable than immediate optimization
- Need to validate assumptions before committing significant resources
- Conventional risk mitigation (analysis, planning) provides diminishing returns

## Preconditions

**Required inputs:**
- Clear hypothesis to test (what you believe and why)
- Defined boundaries for the experiment (scope, duration, resources)
- Agreed-upon success/failure criteria (measurable outcomes)

**Assumed context:**
- Organization/team tolerates controlled failure for learning purposes
- Rollback mechanisms exist (version control, backups, feature flags)
- Time and resources available for experiment execution and analysis
- Stakeholders informed and aligned on experiment intent

**Exclusions (when NOT to use):**
- High-risk contexts where failure causes unacceptable harm (safety-critical systems)
- When proven best practices already exist (don't reinvent)
- Political environments that punish all failures regardless of learning
- Insufficient resources to properly execute and analyze experiment

## Execution Steps

1. **Define clear hypothesis**:
   - **Format**: "If [action], then [expected outcome] because [reasoning]"
   - **Example**: "If we cache API responses for 5 minutes, then response time will decrease by 40% because most requests are duplicates"
   - Make prediction specific and testable

2. **Set experiment boundaries** (contain blast radius):
   - **Scope**: What is included/excluded (single feature, user cohort, geographic region)
   - **Duration**: Time limit for experiment (hours, days, weeks)
   - **Resource limit**: Max budget, infrastructure, person-hours
   - **Audience**: Who is affected (internal team, beta users, 5% of traffic)

3. **Establish success/failure criteria** (before starting):
   - **Success**: Quantitative threshold (e.g., "response time < 200ms for 95th percentile")
   - **Failure**: Boundary conditions that trigger halt (e.g., "error rate > 1%")
   - **Learning**: What insights count as valuable even if hypothesis is wrong
   - **Decision rule**: How to interpret results ("proceed", "pivot", "abandon")

4. **Implement reversibility mechanism**:
   - **Version control**: Branch or tag for easy rollback
   - **Feature flags**: Toggle experiment on/off without deployment
   - **Database migrations**: Down-migration scripts prepared
   - **Infrastructure**: Parallel deployment or blue-green switching
   - **Verification**: Test rollback procedure before starting experiment

5. **Configure monitoring and instrumentation**:
   - Identify metrics to track (aligned with success/failure criteria)
   - Set up dashboards for real-time observation
   - Configure alerts for failure boundary conditions
   - Ensure logging captures diagnostic information for post-analysis

6. **Execute experiment**:
   - Activate experiment for defined scope/duration
   - Monitor metrics continuously (especially early hours/days)
   - Document observations in real-time (avoid hindsight bias)
   - **Halt immediately** if failure criteria met (don't wait for full duration)

7. **Analyze results** (structured reflection):
   - Compare actual outcomes vs. predicted outcomes
   - Categorize result: **Confirmed**, **Rejected**, **Inconclusive**, **Surprising**
   - Identify confounding factors (what else influenced outcome?)
   - Extract learnings independent of success/failure ("what did we discover?")

8. **Make explicit decision**:
   - **Adopt**: Hypothesis confirmed, make permanent
   - **Reject**: Hypothesis rejected, rollback and document why
   - **Iterate**: Partial success, refine hypothesis and re-experiment
   - **Escalate**: Inconclusive results, need broader context or resources
   - Document decision and rationale in project log or ADR

9. **Share learnings**:
   - Communicate results to stakeholders (success or failure)
   - Add to team knowledge base (what worked, what didn't, why)
   - Celebrate learning regardless of outcome (reinforce experimentation culture)

## Checks / Exit Criteria

- Hypothesis explicitly stated (If-Then-Because format)
- Experiment boundaries defined (scope, duration, resources, audience)
- Success/failure criteria established (quantitative thresholds, decision rules)
- Reversibility mechanism implemented and tested
- Monitoring configured (metrics, dashboards, alerts)
- Experiment executed within boundaries
- Results analyzed and documented
- Explicit decision made (adopt, reject, iterate, escalate)
- Learnings shared with team/organization

## Failure Modes

- **Scope creep:** Experiment expands beyond boundaries, increasing risk
- **Sunk cost fallacy:** Continuing failing experiment because of invested effort
- **Confirmation bias:** Interpreting ambiguous results as confirming hypothesis
- **No rollback plan:** Unable to reverse experiment when failure criteria met
- **Insufficient monitoring:** Missing critical signals, failing to detect issues
- **Premature conclusion:** Ending experiment too early without statistical significance
- **Political aftermath:** Punishing "failed" experiments, discouraging future learning
- **Lost knowledge:** Not documenting learnings, repeating same mistakes

## Outputs

- **Experiment Brief:**
  - Hypothesis (If-Then-Because)
  - Boundaries (scope, duration, resources, audience)
  - Success/failure criteria
  - Reversibility plan
  - Monitoring setup

- **Execution Log:**
  - Start/end timestamps
  - Real-time observations
  - Metric snapshots
  - Incidents or anomalies

- **Analysis Report:**
  - Result categorization (confirmed, rejected, inconclusive, surprising)
  - Actual vs. predicted outcomes (with data)
  - Confounding factors
  - Key learnings (bullet points)

- **Decision Record:**
  - Decision made (adopt, reject, iterate, escalate)
  - Rationale
  - Next actions
  - Reference to related ADR (if applicable)

## Notes

**Psychological safety requirement:** Safe-to-fail culture requires leadership support. Teams must trust that well-designed failures won't result in punishment.

**Cheap learning:** Small experiments cost less than large commitments. Fail fast on small scale to avoid catastrophic failure at large scale.

**Iterative refinement:** Most breakthroughs come from multiple experiments refining hypotheses progressively, not single "eureka" moments.

**Cynefin framework context:** Safe-to-fail experiments are especially valuable in "complex" domains where cause-effect relationships exist but are only obvious in retrospect.

**Not gambling:** Experiments are systematic (hypothesis, criteria, boundaries). Gambling is random. Disciplined experimentation accelerates learning; undisciplined risk-taking wastes resources.

**Feature flags are critical:** Deployment != release. Feature flags decouple code deployment from feature activation, enabling safe experimentation in production.

**Document failure equally:** Failed experiments that teach valuable lessons are as important to document as successes. Prevents organizational amnesia.

**Source:** Derived from "Safe-to-Fail Experiments" practice at https://patterns.sddevelopment.be/practices/safe_to_fail/
