+++
title = "Connascence"
subtitle = "Interdependence of software components"
author = "Nicholas Ocket, Stijn Dejongh"
description = "Connascence describes how strongly software components depend on each other and what kinds of changes create ripple effects across a system."
summary = """
Connascence is a powerful concept for understanding the hidden dependencies between software components. Unlike generic discussions of coupling, it breaks interdependence down into specific, measurable types --- such as name, timing, or meaning. This helps developers reason about change impact more effectively and communicate design concerns with precision.
"""
categories = [
    "software development",
]
tags = [
    "Architecture", "Design", "Programming", "Trade-off"
]
uuid="c8c57ad1-c7f0-49ff-8aa1-f37166f8f65d"
aliases=["c8c57ad1-c7f0-49ff-8aa1-f37166f8f65d", "orthogonality"]
pubdate="2025-04-05"
image = "concepts/connascence"
related_concepts = [
    "c57288e3-b102-4212-adb7-a4339a3a9e87",
    "3683719c-d1ff-4693-a5c5-d9eefb07e409"
]
related_practices = [
    "04c6129d-11f7-4aa0-a809-1b972a0d7ef9"
]
further_exploration = [
    {type="biblio", id="9d8ff83e-f49a-4c7c-8e40-e34ac63e2792"},
    {type="biblio", id="8572443d-2c27-462a-b9d7-839dd6e4d58b"},
    {type="raw", author="Mozingo, D.; Richards, T.", year="2019", title="What is Connascence?", link="https://connascence.io/", site="Connascence.io"},
    {type="raw", author="Weirich, J", year="2012", title="Talk: Connascence Examined", link="https://www.youtube.com/watch?v=HQXVKHoUQxY", site="YouTube"},
    {type="raw", author="Brown, G.", year="2011", title="Connascence as a Software Design Metric", link="https://practicingruby.com/articles/connascence", site="practicingruby.com"},
    {type="raw", author="Page-Jones, M.", year="1992", title="Comparing techniques by means of encapsulation and connascence", link="https://dl.acm.org/doi/abs/10.1145/130994.131004", publication="Communications of the ACM", volume="35", issue="9"},
	{type="raw", author="Raymond, E. S.", year="2023", title="The art of Unix Programming", link="http://www.catb.org/~esr/writings/taoup/html/index.html", publication="Cathedral and the Bazaar"},
	{type="raw", author="Various authors", site="wikipedia.org", title="Orthogonality", link="https://en.wikipedia.org/wiki/Orthogonality_(programming)"}
]

+++

## Definition

Originating from the Latin word _'connascere'_, meaning _'born together'_, connascence is a term used in software development to describe the interdependence of software components --- a property often referred to as _'coupling'_. It is a measure of how much two or more software components are dependent on each other, with respect to a particular reason for change. Excessive connascence in our software means that the system is hard to change and hard to maintain.

{{< quote text=`Two elements are connascent if a change to one element would also force a change to the other in order for the program to be correct.` author="Meilir Page-Jones" >}}

One of the most important benefits of connascence is that it gives developers a vocabulary to talk about different types of coupling. Connascence codifies what many experienced engineers have learned by trial and error: Having a common set of nouns to refer to different types of coupling allows us to share that experience more easily.

## Key Components

Reasoning about the amount of interdependence between software components is tricky, as it is not a binary property. Components can be interdependent in various ways, and to various degrees. To make reasoning about coupling of components more manageable, the connascence metric has been broken down into several different facets. Software components can be evaluated for their connascence based on the following criteria:

- **Strength**: The strength of connascence is a measure of how much a change in one component would necessitate a change in another component. The higher the strength, the more tightly coupled the components are.
- **Degree**: The degree of connascence is a measure of how many components are dependent on each other. The higher the degree, the more components are affected by a change in one component.
- **Locality**: The locality of connascence is a measure of how close the dependent components are to each other. The closer the components, the more localized the connascence.

### Types of Connascence

There are many different types of connascence, each with its own particularities. Broadly speaking, we can distinguish between two categories of connascence: **Static** and **Dynamic** connascence. The distinction between these two categories is based on the time at which the connascence is established. Static connascence is established at compile time, while dynamic connascence is established at runtime. While both types of connascence can be problematic, certain forms of static connascence are considered more problematic because they introduce tighter coupling at compile time, reducing flexibility.

{{< warning text=`The different types of connascence are not mutually exclusive, i.e. a single piece of code can exhibit multiple types of connascence at the same time. Reading through these different types of connascence, you might find them overly detailed or even redundant. The main goal is to offer an overview and general understanding of the different ways elements in a system can become interdependent. `>}}


#### Static Connascence

Static connascence is established at compile time, meaning that the dependencies between components are determined before the program is run. This type of connascence is often associated with strong coupling, as it can lead to a more rigid and inflexible system. Static connascence can be further divided into several subtypes:

* **Connascence of Name**: This type of connascence occurs when two components refer to each other by name. For example: if one class uses a method from another class, and that method is renamed, all calls to that method must also be changed. This is often seen in object-oriented programming languages, where classes and methods are defined by name.
* **Connascence of Type**: This type of connascence occurs when two components are dependent on each other based on their data types. For example: if a function expects a certain data type as an argument, and that data type changes, all calls to that function must also change.
* **Connascence of Meaning**: This type of connascence occurs when two components need to agree on the meaning of a certain value or property in the system. For example: if the `user_role` with value `admin` is used to indicate administrative privileges, the code that checks for this value must change if the meaning of the `admin` value changes. Other examples include the use of specific identifiers to denote test versions, the meaning of column names in a database, or the meaning of currency codes in a financial system.
* **Connascence of Position**: This type of connascence occurs when two components are dependent on each other based on their position in a data structure. For example: if the parameter order in a function signature changes, all calls to that function must also change. 
* **Connascence of Algorithm**: Connascence of algorithm frequently occurs when two entities must manipulate data in the same way. For example, if data is being transmitted from one service to another, some sort of checksum algorithm is commonly used. The sender and receiver must agree on which algorithm is to be used. If the sender changes the algorithm used, the receiver must change as well. Another example is the use of certain validation rules in a system to ensure an email is valid ( the same rules need to apply to the data layer, the logic in the code, and any UI components).

#### Dynamic Connascence

Dynamic connascence is established at runtime, meaning that the dependencies between components are determined while the program is running. This type of connascence is often associated with weak coupling, as it can lead to a more flexible and adaptable system. Dynamic connascence can be further divided into several subtypes:

* **Connascence of Execution**: When two components must be executed in a specific order to function correctly. Example: A service that must initialise a connection before sending data.
* **Connascence of Timing**: When components depend on each other completing tasks within a certain time window. Example: A consumer process that fails if the producer is delayed.
* **Connascence of Values**: When one component must use values produced or modified by another. Example: A downstream module relying on dynamically calculated thresholds from an upstream module.
* **Connascence of Identity**: When two components must refer to the exact same instance or object. Example: Passing a shared object between modules where identity equality (not just value equality) matters.
* **Connascence of Convention**: When components rely on shared, informal agreements about behaviour or usage. Example: Multiple modules that interpret a log level string like `WARN` in a hardcoded, implicit way.

These dynamic types of connascence are typically challenging to detect and manage, as they do not show themselves until the system is running. They can be mitigated through careful design and testing practices. Using shared interfaces, common libraries, and well-defined APIs can help make these dependencies more explicit --- and therefore easier to manage.  

## Background

### Origin

The term **connascence** comes from the Latin _connascentia_, derived from _con-_ (“together”) and _nasci_ (“to be born”), meaning “born together” or “originating together.” In general English usage, the word is rare and mostly used in literary or biological contexts to describe things that grow or emerge together from a common origin.

In software design, the term was popularised by **Meilir Page-Jones** in the early 1990s as a way to describe the **interdependence between software components**. Unlike the broader and sometimes ambiguous term *coupling*, connascence breaks down these relationships into concrete types and levels, giving developers a more precise vocabulary for reasoning about change impact and design quality. The concept provides a structured way to discuss not only **whether** components are coupled, but also **how**, **how strongly**, and **how many** components are involved.


### Application

Connascence helps experienced developers and technical leads reason more effectively about design quality and system maintenance. It is particularly useful when:

* **You need language for design trade-offs**: Connascence provides a structured vocabulary to describe different kinds of coupling, helping you move beyond vague concerns like “this feels brittle.”
* **You're reviewing code or evolving APIs**: It highlights what kinds of changes will ripple through a system, making review feedback more concrete and easier to act on.
* **You’re managing systems with shared ownership**: When multiple teams depend on the same components, connascence makes hidden dependencies easier to detect and discuss.
* **You want to reduce long-term maintenance risks**: Understanding strength, degree, and locality of dependencies helps prioritise what to decouple and when.
* **You're working in complex, layered systems**: Whether it’s microservices, shared schemas, or asynchronous flows, connascence clarifies where coordination is fragile and why.
* **You care about growing design literacy in your team**: It gives your team a shared language to talk about interdependence clearly and consistently.

{{<tip text=`Use connascence to explain **why** a refactor or rewrite is needed, not just that it is required. For example, instead of saying __"we need to decouple this module"__, you can say __"this module has high connascence of name and type with several other modules, which makes it hard to change without breaking things. We should refactor it to reduce that coupling."__` >}}

### Comparisons

#### Relationship to Orthogonality

At first glance, **connascence** and **orthogonality** may appear similar—they both deal with how parts of a system relate to each other, but they differ in **focus**, **granularity**, and **intent**. The table below summarizes the key differences:

| Aspect          | **Orthogonality**                                          | **Connascence**                                                       |
|-----------------|------------------------------------------------------------|-----------------------------------------------------------------------|
| **Focus**       | Design independence—how isolated responsibilities are.     | Degree and nature of coupling—how changes in one part affect another. |
| **Perspective** | Encourages *separation of concerns* and *minimal overlap*. | Classifies the *strength and type of dependencies*.                   |
| **Granularity** | Typically applied at the module or system design level.    | Often applied at the code level: functions, arguments, naming.        |
| **Intent**      | Promote composability, clarity, and modifiability.         | Evaluate and reduce harmful coupling to improve maintainability.      |

In simple terms:

- **Orthogonality** asks:  
  _“Can I understand, use, or change this component without needing to understand or touch others?”_
- **Connascence** asks:  
  _“If I change this, how many other things do I need to change? and why?”_

While both concepts aim to reduce unnecessary entanglement, **orthogonality is a design principle**, whereas **connascence is a diagnostic lens**. Orthogonality helps you **prevent entanglement**, connascence helps you **detect and classify it**.

## Examples


{{<tip text=`Connascence is not a silver bullet. It is a tool for reasoning about design quality, but it does not replace the need for good design principles, testing practices, and team communication. Use it as part of a broader toolkit for building maintainable systems.` >}}

### Micro-Services, Macro Problems 

A team deploys a new version of a microservice that exposes an internal API to several downstream services. The deployment passes CI/CD checks, and all services start up correctly in staging and production — everything seems fine. However, within minutes, logs begin to show erratic failures in related services.

The problem? The development team made what seemed like a harmless change: they reordered the parameters of a JSON payload in a request object (static connascence of position), renamed a status field (connascence of name), and refined a timeout behaviour that slightly delays a response under certain conditions (dynamic connascence of timing).

Although the schema wasn’t formally versioned, other services were implicitly relying on field names, order, and response timing. These dependencies weren’t enforced by any compiler or test suite — they only showed up when the system was live. The result was a cascade of subtle failures, including retries, dropped messages, and incorrect status reporting. Fixing the issue required careful rollback and a clearer contract definition between services.

### Database Schema Changes

An engineering team updates a backend service that reads from a shared customer database. As part of a schema cleanup, they remove a legacy `status_code` field that was deemed unused, and refactor the `created_at` field from a `string` to a proper `timestamp` format in the database.

The application’s unit tests pass, and the deployment succeeds --- but hours later, support tickets start rolling in. A different internal tool, maintained by another team, had been silently depending on the `status_code` field to filter active accounts. Worse, a nightly reporting job fails because it attempts to parse the `created_at` field as a string, causing the entire pipeline to break.

In this case, the system exhibited:

* **Connascence of Meaning**: Different applications implicitly shared an understanding of what `status_code` meant.
* **Connascence of Type**: The reporting job expected a `string` where a `timestamp` was now stored.
* **Connascence of Values**: The removed `status_code` values (e.g. "active", "pending") were hardcoded elsewhere.

These kinds of issues are difficult to detect ahead of time because the coupling is **not visible at the API level**. It hides in the database schema and in informal agreements between teams. The lack of an explicit contract or shared data ownership policy made it easy for one change to have far-reaching, unintended effects.
