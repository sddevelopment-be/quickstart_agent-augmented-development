# Incremental Detail Design Diagramming (C4 Approach)

## Overview

The C4 model (Context, Container, Component, Code) is a lightweight hierarchical technique for structuring software architecture diagrams. It favors progressive disclosure of technical detail so stakeholders can consume exactly the level of abstraction they need without being overwhelmed.

## Core Levels

- **Context (Level 1):** Shows the system and its external actors (people, external systems). Answers: "What is this system and who uses it?"  
- **Container (Level 2):** Shows deployable/runtime units (services, databases, front-end apps, message brokers). Answers: "What are the major building blocks and how do they communicate?"  
- **Component (Level 3):** Breaks a container into internally collaborating components (modules, classes, adapters, routers). Answers: "How is responsibility divided inside a container?"  
- **Code (Level 4 – Optional):** Deep dive into implementation structure (class diagrams or call graphs). Used sparingly; only when needed for critical refactors, onboarding, or audits.

## Benefits

- **Audience Alignment:** Each level maps cleanly to stakeholder concerns (executives → context, architects → container, contributors → component/code).  
- **Change Isolation:** Updates typically occur in one level; reduces churn in higher-level diagrams when low-level implementation evolves.  
- **Cognitive Efficiency:** Prevents premature low-level detail exposure; improves clarity in design discussions.  
- **Traceability:** Facilitates linking decisions in ADRs (e.g., ADR-020 multi-tier runtime) to visual artifacts at the correct abstraction layer.  
- **Consistency:** Encourages uniform naming, boundaries, and depiction across systems.

## Recommended Practices

- Start at Context for new contributors; link downward rather than embedding all detail upfront.  
- Keep each diagram single-purpose: avoid mixing container and component views.  
- Use consistent naming between ADRs, diagrams, and implementation modules.  
- Prefer PlantUML C4 includes (`!include <C4/C4_Container>` etc.) for semantic clarity.  
- Only introduce Code-level diagrams for:
  - Security audits
  - Performance bottleneck analysis
  - Complex refactoring proposals
  - Teaching critical library internals
- Cross-link each diagram to its nearest ADR or technical design document.

## Anti-Patterns

- Skipping Context and diving directly into Component views → confuses non-technical stakeholders.
- Over-styling early diagrams → distracts from semantic alignment.
- Embedding runtime metrics or sequence logic in static structural diagrams → conflates concerns.
- Creating Code-level diagrams for stable, low-risk modules → maintenance burden without proportional value.

## Tooling Notes

- Use theme `common.puml` for Context and Container to maximize neutrality.  
- Use `puml-theme-bluegray_conversation.puml` for collaboration-heavy interaction or sequence overlays.  
- Use `puml-theme-stickies.puml` during ideation; replace with production theme before merging into architecture docs.

## How to Apply

1. Start by looking as the system you are developing as a whole. Define it's purpose, and main stakeholders. Specify main external interactions ( using `System_Ext` and optionally `Person_Ext` ).
2. Refine the diagram. Ensure you stick to a holistic view here. This diagram should show readers how the system fits in a larger ecosystem.
3. Based on the upper-level diagram, add the next layer of detail. You do this by decomposing the "blocks"/elements of the previous layer. Be mindfull not to add superfluous detail at this stage.
4. GO TO step 3. Repeat untill the desired level of specificity is reached, then proceed to step 5. **Important:** When defining lower-level granularity diagrams, consider splitting them up to detail specific designs / elements.
5. Review your diagrams, starting at the highest level of generality (most zoomed out). Step through the lower levels, and check that you are "zooming in" on a specific detail.

---

Prepared: 2025-12-01 by Diagram Daisy.
Status: Reviewed by maintainer.
