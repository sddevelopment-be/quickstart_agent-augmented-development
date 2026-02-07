# High-level architectural vision

This document describes the high-level architectural vision for the system. It is intended to provide an overview of the most important 
aspects of the system architecture. It aims to be understandable to all stakeholders, not just technical people.

## Business Goal Statement

> Describe the business goals that the system is intended to support. This should be a high-level description of the problem that the system
> is intended to solve, and the benefits that are expected to be gained from it. Stick to the overarching goals, and avoid going into too 
> much functional detail. This section explains the "why" of the system, not the "what". It should focus on the objectives of the stakeholders,
> and the expected benefits the system will give them. This section should contain a single, clear, and concise statement. It can then 
> elaborate on it by providing more context, or giving a rationale behind the business vision statement. This is a good place to list the 
> [key objectives and results (OKRs)](https://en.wikipedia.org/wiki/Objectives_and_key_results) that the system is intended to support.
> 
> As an example: when building a webshop, the business goal statement would be something like "In order to 
> compete with third-party vendors and suppliers, Hardware Company ABC wants to provide a platform to allow international customers 
> to purchase products online.".

For a more detailed breakdown of the business goals into functional requirements, 
refer to the [Functional Requirements Overview](./functional_requirements.md).

## Desired Quality Attributes

Within systems engineering, quality attributes are realized non-functional requirements used to evaluate the performance of a system. 
TThese are sometimes named architecture characteristics, or "ilities" after the suffix many of the words share. They are usually 
architecturally significant requirements that require architects' attention. This section will describe the quality attributes (QA) that 
were deemed most important for the system, and that will be used to guide the architectural decisions.

> Replace the placeholders with the actual quality attributes that are most important for the system.
> As QAs are not a fixed convention, you have a lot of wiggle room as an architect to define what you mean by them. 
> I advise you to search for an overview of quality attributes, select a few of them that speak to you, and select up to five of these 
> as important to your system. Describe the quality attribute in a very concise manner, and make sure that it is understandable to 
> non-technical readers. If you want to go into more detail, you can add a rationale section to explain why you selected these QAs.

* **quality attribute name**: short description of the quality attribute
* **quality attribute name**: short description of the quality attribute
* **quality attribute name**: short description of the quality attribute

For a more detailed breakdown of the architecturally significant decisions, taken to support the aforementioned Quality Attributes, refer to 
the [Architecture Decision Records](./adr.md).

## Organizational Context

> As an architect, you are not working in a vacuum. You are part of an organization, and your work is influenced by the organization's 
> structure, culture, and processes. This section describes the organizational context in which the system is being developed. It should
> describe the key stakeholders, their roles, and how they fit into the organization. It should also describe the development process that is 
> being used, how the developer teams are organized, and how the system fits into the overall IT landscape of the organization.
> Most importantly: it should describe relationships and dependencies between the development teams and other teams in the organization.
> Using the [Team Topologies](https://teamtopologies.com/) model can be a good way to describe the organizational context in a semiformal,  
> structured way.

## Solution Overview

This section describes the high-level solution to the problem. It will stick to describing the key components of the system, how they 
interact, and what the system as a whole is supposed to do. It will also describe the key technologies that will be used, and the envisioned 
interfaces used by the stakeholders. The breakdown of the functional requirements into technical components will be described in the 
[Functional Requirements Overview](./functional_requirements.md), and is not part of this document.

> Describe the high-level solution to the problem. This should be a non-technical description of the system, focusing on the key components.
> If you use the [C4-Model](https://c4model.com/), this would include the System Context and the Container diagrams.