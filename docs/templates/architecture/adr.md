# Architecture Decision Records

> **ADR Numbering Guide:**
> - ADRs are numbered sequentially starting from 001
> - Check `docs/architecture/adrs/` for the highest existing number before creating a new ADR
> - Use `ls -1 docs/architecture/adrs/ADR-*.md | tail -1` to find the latest ADR
> - Reserve your number by creating the file immediately to prevent conflicts
> - In task specifications, use descriptive names instead of numbers until the ADR is created
> - Example: Use "follow-up-task-lookup-pattern" in planning, then assign next available number when creating the file

## ADR-NNN: Title

**status**: `Proposed` / `Accepted` / `Rejected`  
**date**: YYYY-MM-DD

### Context

> Why do we need to make this decision?   
> Briefly describe the context in which the decision is taken, and the forces at play.
> Try to describe the problem you are faced with, as well as the current state of the application and the development team.

### Decision

> What have we decided to do?
> Keep this section short and to the point, avoid going into too much technical detail.
> Refer to the rationale section for the trade-off breakdown, or to lower-level technical designs for implementation details.

### Rationale

> Why is this decision being made? What are the forces at play? What are the trade-offs? What are the implications of this decision?
> Refer to functional requirements and design vision for context.

### Envisioned Consequences

> What do we expect to happen as a result of this decision? Try and correlate these to your architectural vision and NFRs if possible.
> Make sure to outline both positive and negative consequences of the choice you made.
> The rationale sections should provide enough context to indicate why the trade-offs were accepted.
>
> **hint:** You can use a framework such as [AMMERSE](https://www.ammerse.org/) to make these impacts easier to write, and to ensure a
> consistent structure across your ADRs.

### Considered Alternatives

> What other options did you consider? Why did you decide against them?
> Do not go into too much detail, a bullet point list with a brief description of the alternative, and a single sentence as to why it was not chosen
> is sufficient.