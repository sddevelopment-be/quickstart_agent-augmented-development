# Diagramming Templates

This directory provides diagram-as-code assets to keep visuals consistent, maintainable, and easy to reproduce across the project. It contains PlantUML themes and example diagrams that illustrate common structures and flows.

## Contents

### Themes

- `common.puml`: Minimal shared conventions (fonts, spacing, colors). Use this to keep diagrams readable without imposing a strong visual style.
- `puml-theme-bluegray_conversation.puml`: Blue-gray conversational tone. Good for interaction flows, stakeholder discussions, and sequence/collaboration diagrams where clarity of dialogue matters.
- `puml-theme-stickies.puml`: Sticky-note workshop style. Useful for brainstorming, ideation sessions, Kanban-like visuals, and lightweight planning boards.

### Examples

- `causal-map.puml`: Cause–effect relationships between concepts. Shows how to model causal links without relying on a theme.
- `content-map.puml`: Content inventory and relationships. Useful for mapping documentation artifacts and their dependencies.
- `frontend-architecture.puml`: Component-level front-end overview. Highlights boundaries and responsibilities in UI projects.
- `repo-content-graph.puml`: Repository structure graph. Baseline example that intentionally avoids theming to teach raw composition.
- `request-lifecycle.puml`: Request flow through system components. Helps clarify ingress/egress points and processing stages.
- `system-map.puml`: High-level system context map. Good for orienting stakeholders before deeper component views.

Note: Several items in `examples/` intentionally avoid theme includes. They serve as “how to create these without theming” guidelines to help you learn the fundamentals of PlantUML composition before applying project themes.

## How to Use Themes

Include a theme at the top of your PlantUML file. Adjust the path based on where your diagram lives.

```plantuml
@startuml
!include docs/templates/diagramming/themes/common.puml

' Your diagram content here

@enduml
```

For a stronger visual style, swap `common.puml` with one of the themed files:

```plantuml
@startuml
!include docs/templates/diagramming/themes/puml-theme-bluegray_conversation.puml

' Your diagram content here

@enduml
```

## When to Skip Theming

- You’re teaching or exploring PlantUML basics.
- You need a neutral baseline for documentation or ADRs.
- You want maximum portability across contexts where custom colors/fonts may not render consistently.

## Tips

- Prefer diagram-as-code over screenshots to keep artifacts diffable and reviewable.
- Link diagrams from architecture docs (e.g., `docs/architecture/`) for discoverability.
- Keep diagrams semantically focused: structure over decoration, clarity over complexity.

### Theme Cross-Links

Direct links to theme sources for quick inclusion:

- [common.puml](themes/common.puml): Baseline primitives; minimal visual opinion; ideal for ADRs and neutral technical designs.
- [puml-theme-bluegray_conversation.puml](themes/puml-theme-bluegray_conversation.puml): Conversation-focused styling; use for interaction, request lifecycle, or orchestration flow diagrams.
- [puml-theme-stickies.puml](themes/puml-theme-stickies.puml): Ideation/workshop aesthetic; use for brainstorming causal maps, planning boards, or exploratory architecture sketches.

Recommended pairing examples:

- System context (e.g., `docs/architecture/diagrams/framework/framework-context.puml`) → `common.puml` for clarity.
- Component breakdown (e.g., `framework-component.puml`) → `bluegray_conversation` for emphasis on collaboration.
- Workflow ideation (e.g., early orchestration flow drafts) → `stickies` to signal provisional state.

Include via relative path from architecture diagrams:

```plantuml
@startuml
!include ../../templates/diagramming/themes/common.puml
...
@enduml
```

Or from deeper nested folders adjust `../` segments accordingly. Keep includes stable to avoid breaking cross-repo portability.

