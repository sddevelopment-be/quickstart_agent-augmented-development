# Learning Refactoring Plan

## Goal
Introduce preferred refactoring techniques into the doctrine stack as reusable tactics so generated code quality aligns with desired style and engineering preferences.

## Way of Working

1. Ralph researches and compares candidate refactoring techniques, as well as software design/architectural motifs (patterns).
- Produce a short evidence-based comparison note and content capture in `work/research`.
- For each technique/motif capture:
  - what problem it solves
  - when to apply it
  - risk profile and failure modes
  - Optional: compatibility with existing directives (`017`, `021`, `028`, `036`)

2.a Claire converts selected techniques into tactic files.
- Create one tactic file per selected technique in `doctrine/tactics/`.
- Use `doctrine/templates/tactic.md` as the structural contract.
- Keep tactics procedural and testable (no broad advisory prose).
- Optional: Reorganize tactics for discoverability/navigational ease ( ensure references are updated ).

2.b Claire converts selected patterns into reference files ( `doctrine/docs/references`)
- Research will include design patterns / software architecture motifs, identify them
- 

3. Link tactics from the appropriate refactoring directive(s).
- Directives should invoke tactics, not embed full procedures.
- Keep directive language focused on constraints and invocation conditions.

4. Register and discoverability updates.
- Add entries to `doctrine/tactics/README.md`.
- Update relevant agent profiles if specific roles should load these tactics by default.

5. Validation and consistency pass.
- Validate cross-links and path references.
- Ensure no tactic references unstable/non-core paths.
- Ensure local extensions do not conflict with General/Operational guidelines.
- Confirm no contradiction with doctrine stack precedence.

## Existing Baseline
- Reuse `doctrine/tactics/refactoring-strangler-fig.tactic.md` as a normalization reference for naming, granularity, and output quality.

## Deliverables
- Research comparison note (Ralph)
- New/refined tactic files (Claire)
- Updated directive links
- Updated tactics index
- Validation summary

## References
Fetch your information from the following sources:

- **Low level techniques:** https://refactoring.guru/refactoring/techniques
  - Composition
    - https://refactoring.guru/extract-variable
    - https://refactoring.guru/inline-temp
    - https://refactoring.guru/replace-temp-with-query
    - https://refactoring.guru/remove-assignments-to-parameters
    - https://refactoring.guru/replace-method-with-method-object
    - https://refactoring.guru/substitute-algorithm
  - Moving Features between Objects
    - https://refactoring.guru/move-method
    - https://refactoring.guru/move-field
    - https://refactoring.guru/extract-class
    - https://refactoring.guru/inline-class
    - https://refactoring.guru/hide-delegate
    - https://refactoring.guru/remove-middle-man
    - https://refactoring.guru/introduce-foreign-method
    - https://refactoring.guru/introduce-local-extension
  - Organizing Data
    - https://refactoring.guru/self-encapsulate-field
    - https://refactoring.guru/replace-data-value-with-object
    - https://refactoring.guru/change-value-to-reference
    - https://refactoring.guru/change-reference-to-value
    - https://refactoring.guru/replace-array-with-object
    - https://refactoring.guru/duplicate-observed-data
    - https://refactoring.guru/change-unidirectional-association-to-bidirectional
    - https://refactoring.guru/replace-magic-number-with-symbolic-constant
    - https://refactoring.guru/encapsulate-field
    - https://refactoring.guru/encapsulate-collection
    - https://refactoring.guru/replace-type-code-with-class
    - https://refactoring.guru/replace-type-code-with-subclasses
    - https://refactoring.guru/replace-type-code-with-state-strategy
    - https://refactoring.guru/replace-subclass-with-fields
  - Simplifying Conditional Expressions
    - https://refactoring.guru/decompose-conditional
    - https://refactoring.guru/consolidate-conditional-expression
    - https://refactoring.guru/consolidate-duplicate-conditional-fragments
    - https://refactoring.guru/remove-control-flag
    - https://refactoring.guru/replace-nested-conditional-with-guard-clauses
    - https://refactoring.guru/replace-conditional-with-polymorphism
    - https://refactoring.guru/introduce-null-object
    - https://refactoring.guru/introduce-assertion
  - Simplifying Method Calls
    - https://refactoring.guru/rename-method
    - https://refactoring.guru/add-parameter
    - https://refactoring.guru/remove-parameter
    - https://refactoring.guru/separate-query-from-modifier
    - https://refactoring.guru/parameterize-method
    - https://refactoring.guru/replace-parameter-with-explicit-methods
    - https://refactoring.guru/preserve-whole-object
    - https://refactoring.guru/replace-parameter-with-method-call
    - https://refactoring.guru/introduce-parameter-object
    - https://refactoring.guru/remove-setting-method
    - https://refactoring.guru/hide-method
    - https://refactoring.guru/replace-constructor-with-factory-method
    - https://refactoring.guru/replace-error-code-with-exception
    - https://refactoring.guru/replace-exception-with-test
  - Dealing with Generalization
    - https://refactoring.guru/pull-up-field
    - https://refactoring.guru/pull-up-method
    - https://refactoring.guru/pull-up-constructor-body
    - https://refactoring.guru/push-down-method
    - https://refactoring.guru/push-down-field
    - https://refactoring.guru/extract-subclass
    - https://refactoring.guru/extract-superclass
    - https://refactoring.guru/extract-interface
    - https://refactoring.guru/collapse-hierarchy
    - https://refactoring.guru/form-template-method
    - https://refactoring.guru/replace-inheritance-with-delegation
    - https://refactoring.guru/replace-delegation-with-inheritance
    
-  **Refactor To Patterns Overview:** https://www.industriallogic.com/refactoring-to-patterns/
  - **Chain Constructors:** https://www.industriallogic.com/refactoring-to-patterns/catalog/chainConstructors.html
  - **Compose Method:** https://www.industriallogic.com/refactoring-to-patterns/catalog/composeMethod.html
  - **Encapsulate With Factory:** https://www.industriallogic.com/refactoring-to-patterns/catalog/classesWithFactory.html
  - **Encapsulate with Builder:** https://www.industriallogic.com/refactoring-to-patterns/catalog/compositeWithBulder.html
  - **Extract Adapter:** https://www.industriallogic.com/refactoring-to-patterns/catalog/extractAdapter.html
  - **Extract Composite:** https://www.industriallogic.com/refactoring-to-patterns/catalog/extractComposite.html
  - **Extract Parameter:** https://www.industriallogic.com/refactoring-to-patterns/catalog/extractParameter.html
  - **Form Template Method:** https://www.industriallogic.com/refactoring-to-patterns/catalog/formTemplateMethod.html
  - **Inline Singleton:** https://www.industriallogic.com/refactoring-to-patterns/catalog/inlineSingleton.html
  - **Null Object:** https://www.industriallogic.com/refactoring-to-patterns/catalog/nullObject.html
  - **Polymorphic create w/ Factory Method:** https://www.industriallogic.com/refactoring-to-patterns/catalog/polymorphicCreationFactory.html
  - **Limit instantiation w/ Singleton:** https://www.industriallogic.com/refactoring-to-patterns/catalog/instantiationWithSingleton.html
  - **Accumulation to Collecting Param:** https://www.industriallogic.com/refactoring-to-patterns/catalog/accumulationToCollection.html
  - **Creation Knowledge to Factory:** https://www.industriallogic.com/refactoring-to-patterns/catalog/creationWithFactory.html

- **Design Patterns:** Target state / known solutions to architectural/design challenges:
  - https://refactoring.guru/design-patterns/facade
  - https://refactoring.guru/design-patterns/decorator
  - https://refactoring.guru/design-patterns/proxy
  - https://refactoring.guru/design-patterns/chain-of-responsibility
  - https://refactoring.guru/design-patterns/command
  - https://refactoring.guru/design-patterns/iterator
  - https://refactoring.guru/design-patterns/mediator
  - https://refactoring.guru/design-patterns/observer
  - https://refactoring.guru/design-patterns/state
  - https://refactoring.guru/design-patterns/strategy
  - https://refactoring.guru/design-patterns/template-method
  - https://refactoring.guru/design-patterns/visitor
  - https://refactoring.guru/design-patterns/abstract-factory
  - https://refactoring.guru/design-patterns/factory-method
  - https://refactoring.guru/design-patterns/prototype
  - https://refactoring.guru/design-patterns/singleton
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/backends-for-frontends
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/pipes-and-filters
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/publisher-subscriber
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/priority-queue
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/index-table
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/retry
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/async-request-reply
  - https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven
  - https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/n-tier
  - https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/web-queue-worker
  - https://martinfowler.com/eaaDev/EventNarrative.html
  - https://martinfowler.com/bliki/CQRS.html
  - https://martinfowler.com/articles/201701-event-driven.html

