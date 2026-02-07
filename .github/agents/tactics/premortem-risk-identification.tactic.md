# Tactic: Premortem Risk Identification

**Invoked by:**
- Directive 018 (Traceable Decisions) — ADR preparation and risk discovery

**Related tactics:**
- `adversarial-testing.tactic.md` — broader stress-testing for proposals/practices
- `stopping-conditions.tactic.md` — exit criteria based on identified risks
- `ammerse-analysis.tactic.md` — trade-off analysis after risk discovery

**Complements:**
- Approach: Decision-First Development

---

## Intent

Proactively identify critical failure modes for an idea, plan, or decision by deliberately attempting to "sabotage" it. Strengthens proposals by exposing blind spots and developing mitigation strategies before execution.

Apply when:
- Evaluating a new idea or approach with significant investment
- Need to strengthen a proposal against challenges
- Decision has high impact and limited reversibility
- Team tends toward optimism bias or groupthink

## Preconditions

**Required inputs:**
- Clearly defined idea, plan, or decision to evaluate
- Willingness to critically assess own ideas without defensiveness
- Access to knowledgeable individuals for feedback (optional but recommended)

**Assumed context:**
- Environment values thorough risk assessment
- Stakeholders appreciate transparent identification of weaknesses
- Time is available for structured analysis (not in crisis mode)

**Exclusions (when NOT to use):**
- Ultra-fast iterations where failure cost is negligible
- Situations requiring immediate action without analysis time
- Ideas so preliminary that detailed risk analysis is premature
- Contexts where excessive caution stifles necessary innovation

## Execution Steps

1. **Shift to destructive mindset**
   - Mentally distance yourself from emotional investment in the idea
   - Ask: "How can I ensure this fails spectacularly?"
   - Encourage creativity: explore beyond common/obvious issues
   - Set timer for 15-20 minutes of brainstorming

2. **Generate comprehensive failure list**
   - Write down every way the idea could fail (aim for 15-30 items)
   - Include technical, social, resource, timing, and external factors
   - Do not self-censor—capture wild/unlikely scenarios
   - Ask others to contribute failure scenarios

3. **Assign impact ratings** to each failure scenario:
   - **High impact:** Complete failure, major loss, unrecoverable damage
   - **Medium impact:** Significant setback, recoverable with effort
   - **Low impact:** Minor inconvenience, easily resolved

4. **Assign likelihood ratings** (optional but recommended):
   - **High likelihood:** Probable given current information
   - **Medium likelihood:** Possible but not certain
   - **Low likelihood:** Unlikely but not impossible

5. **Create 2x2 risk matrix** (optional):
   - Plot failure scenarios by impact (vertical) and likelihood (horizontal)
   - Quadrants: High Impact/High Likelihood, High Impact/Low Likelihood, Low Impact/High Likelihood, Low Impact/Low Likelihood

6. **Prioritize top failure scenarios**:
   - Identify the **5 highest-impact** failures regardless of likelihood
   - From these 5, select:
     - **3 most likely** high-impact scenarios
     - **2 least likely** high-impact scenarios (surprise/catastrophic risks)

7. **Develop mitigation strategies** for prioritized scenarios:
   - For each of the 5 prioritized failures, define:
     - **Prevention:** Actions to reduce likelihood
     - **Detection:** Early warning signals
     - **Response:** Actions if failure occurs despite prevention
   - Keep strategies concrete and actionable (not vague "be careful")

8. **Document risk tracking plan**:
   - Specify which failure modes will be monitored during execution
   - Define monitoring frequency (weekly, monthly, at milestones)
   - Assign responsibility for tracking

## Checks / Exit Criteria

- Failure list contains at least 10 distinct scenarios
- All scenarios assigned impact ratings
- Top 5 highest-impact scenarios identified
- Mitigation strategies defined for 3 most likely + 2 least likely high-impact scenarios
- Each mitigation strategy includes prevention, detection, and response components
- Risk tracking plan documented with monitoring frequency and ownership

## Failure Modes

- **Self-protection bias:** Avoiding harsh criticism to protect ego/investment
- **Surface-level analysis:** Only identifying obvious risks
- **Catastrophic thinking:** Spiraling into paralyzing negativity
- **Analysis paralysis:** Spending excessive time identifying risks instead of acting
- **Ignoring low-likelihood/high-impact:** Dismissing unlikely catastrophic risks as "won't happen"
- **Vague mitigations:** "Be more careful" instead of concrete prevention steps
- **No follow-through:** Creating risk analysis but never monitoring during execution

## Outputs

- **Failure Scenarios List:** 10-30 distinct ways the idea could fail
- **Risk Matrix** (if likelihood assessed): 2x2 grid showing impact vs. likelihood
- **Priority Risk Register:**
  - 3 most likely high-impact scenarios
  - 2 least likely high-impact scenarios
  - For each: description, impact, likelihood, prevention, detection, response
- **Risk Tracking Plan:** Monitoring frequency, assigned responsibility, trigger thresholds

## Notes

**Balance with optimism:** Pair premortem with "what would make this succeed?" exercise to maintain team morale. This tactic is diagnostic, not prescriptive.

**Timeboxing:** Limit initial brainstorming to 20 minutes and full analysis to 1-2 hours. Diminishing returns beyond this point.

**Psychological safety:** Anonymize or park sensitive risks (vendor issues, people concerns) to keep exercise safe and honest.

**Cognitive biases:** This tactic counteracts selection bias, effort justification, illusion of validity, and illusion of explanatory depth by forcing explicit confrontation with weaknesses.

**Surprise risks:** Low-likelihood/high-impact failures (e.g., "What if a hurricane destroys our data center?") are often what catches teams unprepared. Explicitly addressing 2 such scenarios improves resilience.

**Source:** Derived from "How Do We Make This Fail" practice at https://patterns.sddevelopment.be/practices/how_do_we_make_this_fail/
