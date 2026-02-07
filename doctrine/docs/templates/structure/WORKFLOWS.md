# WORKFLOWS — Build, Test, Release, CI

_Last updated: {{DATE}}_

## Build
- Tooling: {{build tool}}
- Commands:
    - `{{cmd}}` — {{desc}}

## Test
- Unit: {{framework}} (`{{cmd}}`)
- Integration: {{framework}} (`{{cmd}}`)
- Coverage: {{tool}} → threshold {{%}}

## Release
- Versioning: semver / calendar / other
- Changelog: {{path or tool}}
- Publishing: {{registry}} (`{{cmd}}`)

## CI/CD
| Pipeline | Trigger   | Stages     | Artifacts       | Status  |
|----------|-----------|------------|-----------------|---------|
| {{...}}  | push/main | build,test | dist/, coverage | passing |

## Environments
- Dev: {{notes}}
- Staging: {{notes}}
- Prod: {{notes}}