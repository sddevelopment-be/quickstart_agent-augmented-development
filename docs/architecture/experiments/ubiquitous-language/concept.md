Agentic Ubiquitous Language

A dialectic exploration on language, DDD, and agentic systems


---


## Context


This document captures an exploratory conversation around an agentic concept: using large language model–based agents to observe, extract, and govern organizational language as a first-class architectural concern.

The focus is explicitly not on automating architecture decisions, but on leveraging linguistic analysis to:

- surface semantic drift,

- make bounded contexts visible,

- and inform architectural review through evidence grounded in real usage.


This text is intentionally reflective and dialectic. It is meant as raw material for an architectural proposal or future essay, not as a polished prescription.


---


## Initial Thesis


The core observation:

> The real strength of Domain-Driven Design in corporate environments is not architectural patterns, but linguistic alignment — people using the same words to mean the same things.



- From this follows a proposal:

- Feed an agent stack with organizational artifacts:

- books,

- codebases,

- documentation,

- anonymized meeting transcripts.


- Ask it to extract domain concepts and terminology.

- Detect and log cases where:

- the same word is used with multiple meanings,

- different words are used for the same concept.



- The output becomes:

- a structured glossary (possibly split per domain / bounded context),

- formalized via tools like Contextive,

- usable as an input to DDD-oriented design and implementation.


At its heart: agent-assisted ubiquitous language capture.


---


## Expansion: Linguistics as an Architectural Signal


- A key reinforcement emerged quickly:

- LLMs are especially strong at linguistic pattern detection.

They are not authorities on correctness, but they are sensitive to inconsistency, drift, and ambiguity.


This reframes the system as:

> A semantic drift detector, not a glossary oracle.



- Language conflicts often precede architectural problems:

- hidden or overlapping bounded contexts,

- leaky abstractions,

- shared primitives with divergent meanings,

- data models acting as accidental sources of truth.


- Surfacing linguistic conflict therefore becomes a way to:

- review architecture indirectly,

- detect cross-domain clashes,

and expose organizational dysjoints that would otherwise remain implicit.



---


## Escalation: From Glossary to PR-Level Review


- Once a glossary exists, a further step suggests itself:

- Introduce a domain review agent that runs on pull requests in a "DDD-compliant repository".

- The agent uses:

- bounded context structure in the repo,

- glossary definitions and decisions,

- and the PR diff itself.



- Its role is not to approve architecture, but to:

- flag ambiguous or deprecated terminology,

- detect boundary leaks (foreign domain language used without translation),

- propose new glossary candidates when new terms appear.


- Crucially, enforcement is tiered:

- comment-only by default,

- acknowledgement-based checks where appropriate,

- hard failures only for explicitly banned or high-confidence violations.


The intent is to create linguistic feedback at the point of change, not centralized control.


---


## Terminology Principle


A key clarification was explicitly stated and preserved:

> The system must operate with a human in charge, not “human in the loop.”



Language decisions are accountable, contextual, and owned. The agent observes, suggests, and evidences — it does not decide.


---


## Red Team: Why This Is a Terrible Idea


- Before capturing the concept, a deliberate red-team critique was applied.


### 1. Linguistic Policing


- The system risks turning language into a compliance regime:

- developers writing to appease bots,

- performative adherence instead of shared understanding,

- increased anxiety around terminology.



### 2. Early Noise and False Positives


- Transcripts are messy.

- Legacy code distorts meaning.

- Casual shorthand may be misread as semantic conflict.


- Early low-quality output could permanently damage trust.


### 3. Glossary as Power Instrument


- A CI-enforced glossary can become a political tool:

- whose language becomes canonical?

- who blocks whom?


- Semantic authority is real authority in organizations.


### 4. Incentive Conflicts Masquerading as Semantic Conflicts


Some terms diverge because incentives diverge, not because of misunderstanding. A glossary can document this — but cannot resolve it.


### 5. Privacy and Compliance Risks


Meeting transcripts contain sensitive information. Anonymization is brittle. Centralizing semantic extraction creates an attractive compliance target.


### 6. Sociolinguistic Reality


- Different registers exist across:

- roles,

- seniority,

- teams,

- regions,

- written vs spoken language.


- Normal variation may be misclassified as drift.


### 7. PR-Level Harm


- Running this on every PR risks:

- review fatigue,

- defensive reactions,

- blocking small refactors due to legacy language.



### 8. Canonizing the Wrong Model


- The system may standardize what is common rather than what is correct or useful.


### 9. Maintenance Burden


- Glossaries need ownership, cadence, revision, and deprecation strategies. Without this, they rot.


### 10. False Sense of Progress


- Aligning words can distract from deeper structural issues:

- ownership,

- coupling,

- incentives,

delivery mechanics.



---


## Rebuttal


- Several counterpoints were articulated clearly.

- Contexts Already Address This

DDD’s bounded contexts explicitly accept semantic divergence. The problem historically has not been theory, but lack of observability.

- The agent does not invent contexts — it reveals where they already exist or are violated.

- Agentic Flows Change Feasibility

- What was previously infeasible is now tractable:

- continuous capture,

- multi-source analysis,

- incremental maintenance,

- selective human review.


- This is an economic shift, not just a tooling upgrade.

- Companies Are Semantic Battlegrounds

- Semantic conflict is not introduced by the system. It already exists:

- in meetings,

- in code reviews,

- in APIs,

- in data definitions.


The real question is whether these conflicts remain implicit and corrosive, or explicit and governable.


---


## Synthesis


The emerging synthesis can be stated plainly:

> This system does not attempt to eliminate semantic conflict. It makes semantic conflict explicit, contextual, and governable — with a human in charge.



Or, more sharply:

> Domain-Driven Design provides a theory of semantic boundaries. Agentic tooling makes those boundaries observable at the point of change.



The system’s value lies in surfacing reality, not enforcing purity.


---


## Irreducible Risk


One risk remains unavoidable:

> In some organizations, this will be used as a control mechanism rather than a learning mechanism.



This cannot be fully designed away. At best, misuse can be made visible, enforcement can be constrained, and evidence can be favored over authority.


---


## Closing Note


- This exploration treats language as infrastructure:

- fragile,

- political,

- and deeply architectural.


- Agentic systems do not solve this. They merely make it harder to pretend it isn’t happening.

That alone may be enough to justify the experiment.