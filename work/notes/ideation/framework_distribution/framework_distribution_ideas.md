# Framework Distribution Ideas

**Packaging note:** Exclude this directory from packaged releases. It contains ideation and planning notes, not runtime or user-facing assets.

> Minimal, but complete, framework distribution. Apply it to a real-world project without dragging in too many unfocused dependencies or unnecessary files.

## User Experience

- Ensure that the framework is easy to install, configure, and use
  - High-level documentation + specific guides and instructions
  - auto-install scripts, preferably for linux/windows systems
  - step-by-step installation and upgrade guides
- Ensure local changes are preserved across upgrades
- Ensure that the framework is easy to extend
- After installation: no framework specific documentation is kept ( e.g. no internal wiki, no ADRs about the framework, no work-in-progress files, no ideation notes, ...)
- What is released should be the minimum required to run the framework, and the internal consistency tests.

## Technical considerations

- A packaging / release workflow that is easy to maintain and extend
  - Automated testing of releases
  - Automated publishing of releases
  - Use configurable repository map, to indicate which parts are to be packaged

## Framework Implications

- Clear split between framework content and scaffolding
- Make it easy to extend and adapt the framework, for example: 
  - moving directives to domain-specific subdirectories
  - moving templates to domain-specific subdirectories
  - create an "offloading" mechanism, moving files in or out of the active listings
- Ensure that the framework can be used in different contexts (e.g. different programming languages, different project types, different interaction modes)
- Ensure that the framework can be used in different environments (e.g. different operating systems, different CI/CD systems)
