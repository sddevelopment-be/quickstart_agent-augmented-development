# Tactic: Define Stopping Conditions

**Invoked by:**
- Directive 024 (Self-Observation Protocol) — checkpoint triggers for long-running tasks
- Directive 011 (Risk & Escalation) — timeout handling and boundary enforcement

**Related tactics:**
- [`premortem-risk-identification.tactic.md`](./premortem-risk-identification.tactic.md) — risk discovery before establishing stopping criteria
- [`safe-to-fail-experiment-design.tactic.md`](./safe-to-fail-experiment-design.tactic.md) — bounded exploration with explicit exit criteria

**Complements:**
- Approach: Locality of Change (premature optimization avoidance)

---

## Intent

Establish clear, measurable thresholds that define when to stop pursuing a goal or commitment. Protects against over-investment, burnout, and sunk-cost fallacy by defining acceptable loss limits before starting work.

Apply when:
- Starting a new initiative with uncertain outcomes (experiments, prototypes, career changes)
- Commitments require significant personal/organizational investment
- Risk of over-extension or mission creep is high
- Need to communicate boundaries to stakeholders upfront

## Preconditions

**Required inputs:**
- Clearly defined goal or commitment
- Understanding of personal/organizational limits (financial, time, energy, moral)
- Stakeholder awareness (if commitment affects others)

**Assumed context:**
- You have capacity to define boundaries before starting
- Environment respects stopping decisions (not heavily influenced by sunk-cost fallacy culture)
- Goal is framed as experiment or bounded commitment, not "do-or-die"

**Exclusions (when NOT to use):**
- Ultra-short tasks (<1 hour) with trivial investment
- Situations requiring immediate emergency response
- Contexts where rigid stopping criteria hinder necessary adaptability
- When external pressures make boundary enforcement impossible

## Execution Steps

1. **Define positive evolution/success criteria**
   - Write 3-5 concrete indicators of progress (measurable, observable)
   - Example: "Signed freelance contract", "Prototype validated by 10 users", "Revenue > $5K/month"

2. **Define negative impact/warning signals**
   - List 3-5 specific red flags indicating trouble (measurable, observable)
   - Example: "Savings < $10K", "Working >60 hrs/week for 3+ weeks", "No client meetings in 2 months"

3. **Set hard limits across resource categories**:
   - **Financial:** Maximum money willing to spend/lose
   - **Time:** Maximum duration before reassessment
   - **Physical:** Health indicators that trigger stop (sleep quality, stress symptoms)
   - **Mental:** Emotional well-being thresholds (anxiety levels, motivation loss)
   - **Moral:** Ethical boundaries that cannot be crossed
   - **Social:** Relationship impacts that are unacceptable

4. **Make limits concrete and SMART**:
   - Specific: "Savings < $8,000" not "Running out of money"
   - Measurable: "Zero contracts signed within 90 days" not "Not making progress"
   - Time-bound: "If X by date Y, stop immediately"

5. **Communicate boundaries to stakeholders**:
   - Share stopping conditions with affected parties (family, team, partners) before starting
   - Gain acknowledgment that stopping under defined conditions is acceptable
   - Document agreement explicitly

6. **Create trigger declaration**: Write "When X happens, then I will stop" statements
   - Example: "When my savings fall below $8,000, then I will pause freelancing and seek employment"
   - Prime yourself for action by stating intent clearly

7. **Schedule review checkpoints**:
   - Set calendar reminders to review progress vs. limits (weekly or monthly)
   - Define who will conduct reviews (self, accountability partner, team lead)

## Checks / Exit Criteria

- Positive success criteria defined (3-5 specific indicators)
- Warning signals identified (3-5 specific red flags)
- Hard limits set for at least 3 resource categories
- All limits are SMART (specific, measurable, time-bound)
- Stopping conditions communicated to key stakeholders
- Trigger declarations written in "When X, then I will Y" format
- Review checkpoints scheduled in calendar

## Failure Modes

- **Vague limits:** "I'll stop if it gets too hard" (not measurable, not triggerable)
- **Overoptimistic boundaries:** Setting limits far beyond actual capacity
- **Ignoring warnings:** Recognizing red flags but rationalizing continuation
- **Sunk-cost override:** "I've invested so much already, can't stop now"
- **External pressure compliance:** Allowing others to guilt you past your limits
- **No review mechanism:** Forgetting to check progress against limits
- **Skipping stakeholder communication:** Surprising others when you stop, creating conflict

## Outputs

- **Stopping Conditions Document:**
  - Success criteria (3-5 items)
  - Warning signals (3-5 items)
  - Hard limits table (financial, time, physical, mental, moral, social)
  - Trigger declarations ("When X, then I will Y")
  - Review schedule
  - Stakeholder acknowledgment (names, dates)

## Notes

**Cultural resistance:** Stopping is often viewed negatively ("quitters never win"). Reframe as experimentation and data-driven decision-making. Communicate that stopping protects long-term outcomes.

**Flexibility vs. rigidity:** Review and adjust limits as new information emerges, but do not move goalposts mid-execution without explicit justification and stakeholder agreement.

**Experiment framing:** Treat goals as experiments with defined parameters rather than all-or-nothing commitments. Reduces psychological cost of stopping.

**Loss aversion:** Humans overvalue things we lose (sunk-cost fallacy). Pre-commitment to stopping conditions counteracts this bias through behavioral conditioning.

**Source:** Derived from Breaking Conditions practice at https://patterns.sddevelopment.be/practices/breaking-conditions/
