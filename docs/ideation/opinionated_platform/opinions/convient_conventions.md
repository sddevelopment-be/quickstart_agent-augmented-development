+++
title = "Synced Style"
author = "Stijn Dejongh"
problem="Developers struggle to maintain code consistency, negatively affecting code maintainability and reliability."
description = "Maintaining a consistent coding style within a team, using automation and documentation to enforce it."
summary="""
Establish and maintain a consistent coding style within a team or project. By enforcing a uniform style, the pattern aims to improve code 
maintainability, readability, and reliability, ultimately reducing mental load and enhancing the ease of collaboration.
"""
categories = [
    "software development",
]
tags = [
    "programming", "complexity", "readability"
]
uuid="1848f4a6-3acb-4dc8-aa49-e57a1b87cf3b"
aliases=["1848f4a6-3acb-4dc8-aa49-e57a1b87cf3b"]
outputs = ['html', 'json']
ammerse = [
  {name = "agile", delta = "-0.45", rationale="Potential for lengthy discussions and meetings on coding standards, which can detract from agility and speed."},
  {name = "minimal", delta = "-0.3", rationale="Initial overhead and potential for over-discussion, making the process less minimal."},
  {name = "maintainable", delta = "1", rationale="Long-term benefits of consistent code readability and maintainability"},
  {name = "environmental", delta = "0.5", rationale="Improved resource efficiency from consistent coding practices."},
  {name = "reachable", delta = "0.3", rationale="Long-term benefits of reliable project outcomes outweigh initial delays."},
  {name = "solvable", delta = "0.9", rationale="Improved problem-solving efficiency from reduction in cognitive load."},
  {name = "extensible", delta = "0", rationale="No significant impact on extensibility, as long as conventions are well-documented and flexible."}
]
pubdate="2023-08-26"
image="practices/conventions_cover"
related_concepts = [
  "1f3849c8-28bc-4934-95bf-66d9dcee6858",
]
related_practices = [
  "94a558cd-4e86-4814-a5e9-d6ecafcb0d6b",
  "336b0448-e78b-4428-83a5-d4d473afda63"
]
further_exploration = [
  {type="biblio", id="d22ee68e-2f19-4677-9123-2994cb111c0c"},
  {type="biblio", id="9d8ff83e-f49a-4c7c-8e40-e34ac63e2792"},
  {type="biblio", id="8572443d-2c27-462a-b9d7-839dd6e4d58b"},
  {type="biblio", id="2930d42d-e7cf-4ea5-a6f3-eceb5b9a5fc1"},
  {type="raw", author="Various authors", year="2023", title="Programming Style", site="wikipedia.org", link="https://en.wikipedia.org/wiki/Programming_style"},  
  {type="tool", id="7c28156d-be10-4b0d-a97a-bed2836bc9a4"},  
  {type="raw", author="Gravley, L.", year="2020", title="Introducing GitHub Super Linter", site="GitHub.blog", link="https://github.blog/2020-06-18-introducing-github-super-linter-one-linter-to-rule-them-all/"},  
]
+++

{{<image
src="/images/practices/outlier_consistency"
alt="A field of blue circles and a single orange square"
caption="Find the orange square! Illustrating that finding an outlier is easier in a mostly uniform environment." >}}

## Problem Statement

Developers struggle to maintain code consistency, negatively affecting code maintainability and reliability.

## Intent

We wish to maintain a higher level of code discipline, increasing the reliability of the code.

## Solution

Define a consistent coding style for your team, document it, use it, and enforce it.
If possible, add automation to your build process to point out any irregularities.
<br /><br />
Even if code is not fully up to spec, it is better to be consistent with the rest of the surrounding code than to introduce yet another style to
an existing project. If you are going to change conventions midway through the life-cycle of a codebase, be sure to change all of it.
Do not let inconsistent styles creep into your repositories.  

{{<info text=`
Being consistent within a codebase does not mean your need to apply the same style to all repositories within your project.
It can be a viable option to apply a certain style within one repository, and a different one in another.
As long as the code is consistent with it's surrounding, you will get the benefit of pattern recognition.
` >}}

## Contextual forces

Well-suited for teams working on projects where code maintainability and readability are paramount, such as large-scale enterprise applications
or long-term software projects. It is particularly beneficial in environments where multiple developers collaborate on the same codebase,
ensuring consistency and reducing cognitive load. This pattern is also effective in organizations that prioritize code quality and
have the resources to invest in defining, documenting, and enforcing coding standards.

### Enablers
The following factors support effective application of the practice:

* **Team Dynamics:** The team is cohesive and willing to align on a preferred coding style. 
* **Existing Guidelines:** The language, team, or organization has a recommended style guide for the programming language(s) in use.
* **Tooling Support:** The development environment supports the sharing and importing of code styles. Automated tools for code analysis and linting
  are available and integrated into the development process.

### Deterrents
The following factors prevent effective application of the practice:

* **Individual Expression:** Developers highly value their coding individuality and resist standardization.
* **Inconsistent Structure:** The team works with multiple distinct codebases or programming languages, making it difficult to enforce a single
  style.
* **Lack of Tooling:** Manually reviewing code for consistency is tedious and often avoided.
* **Bless this Mess:** The development culture is heavily influenced by the normalization of deviance, where exceptions become the norm.

## Rationale

* Code is write-once, read-often.
* Working with consistent representations lowers mental load.
* Humans are excellent at recognizing deviations from the norm.


## Application

### Consequences

* **Developer Resistance:** Enforcing a uniform style might face pushback from developers who value their coding individuality.
* **Initial Overhead:** The process of defining, documenting, and implementing consistent coding standards can be time-consuming and
  resource-intensive.
* **Tool Dependence:** Reliance on automated tools for enforcement might lead to over-dependence, reducing manual oversight and potentially missing
  nuanced issues.
* **Stifled Innovation:** Strict adherence to coding conventions might stifle creative problem-solving and innovative coding techniques. It is
  essential to strike a balance between consistency and flexibility to encourage creativity while maintaining readability and maintainability.
  Avoid the "Not Invented Here" syndrome, and be mindful not to spend significant amounts of time on discussing the "best" way to formulate things.
* **Initial Overhead:** The process of defining, documenting, and implementing consistent coding standards can be time-consuming and
  resource-intensive.
* **Team Dynamics:** The process of defining and enforcing coding standards can cause friction within the team, especially when consensus is
  required. Senior or vocal team members might dominate the creation and enforcement of rules, creating an oppressive atmosphere for
  others, particularly new or timid team members. It is essential to manage this process carefully to avoid negatively impacting team dynamics.
* **Onboarding Challenges:** While having a set of conventions aims to reduce variation and cognitive load, overly strict enforcement of coding
  conventions might overwhelm new team members, making it difficult for them to integrate smoothly.

### Mitigation Strategies

* **Inclusive Decision-Making:** Involve the entire team in the process of defining the coding standards to ensure buy-in and reduce resistance.
* **Incremental Implementation:** Introduce the standards gradually, starting with the most critical rules, and expand over time to allow for
  adaptation.
* **Flexible Enforcement:** Allow for exceptions where necessary and encourage developers to suggest improvements to the conventions.
* **Comprehensive Training:** Provide training sessions and resources to help developers understand and adopt the new standards effectively.
* **Regular Reviews:** Conduct regular code reviews and discussions to address any issues with the conventions and make adjustments as needed.
* **Mentorship Programs:** Pair new team members with mentors who can help them understand and adapt to coding standards without feeling
  intimidated.

## Examples

### Nuke 'em, duke!

A great example of this is the use of brackets to identify code blocks in Java. While not strictly necessary to make your code compile or work, 
many teams explicitly ask their developers to include brackets, even on conditionals that could be written as one-liners. This particular 
convention tends to irk newer developers who like their code to be as concise as possible. 
While brevity is a usually good, at times it can confuse your readers. 

Let's have   a quick look at the code below, which checks whether we are under attack, and whether to launch a retaliatory nuclear strike.

```java
public void failSafe(boolean thePresidentIsDead){
    if(thePresidentIsDead)
        launchNukes();

    businessAsUsual();
}
```
   
Now imagine someone in the team is tasked to add logging statements to the entire codebase. 
They do as they are told, resulting in the code below.
At first glance, everything looks fine. Can you spot the cataclysmic mistake?

```java
public void failSafe(boolean thePresidentIsDead){
    LOG.info("Checking to see if everything is still okay...");

    if(thePresidentIsDead)
        LOG.warn("OMG! You killed him. You bastards!");
        launchNukes();

    LOG.info("Carry on, carrying on");
    businessAsUsual();
}
```

The nukes will be launched, regardless of the president being alive or not.
A simple log statement, combined with misleading indentation has set forth a thermonuclear apocalypse.

### Use Case: Enforce coding standards automatically

Most (semi-mature) languages have a preferred style. It is usually wise to stick to it, even if you do not personally like it.
As a few examples: Java is written mostly in camelCase, C# uses PascalCase for everything but variables, Python and JavaScript developers tend to 
put expected variable types in the names. The list on small and large differences between different language default writing styles is long. 

Even on your project, you might decide to use a particular spacing/indentation convention, method ordering, or you might enforce a certain level 
of test coverage for parts of your project. Basically: there are a lot of custom conventions that exist within a project. On most projects, the 
biggest part of review comments are related to people not following the preferred style correctly.

In order to avoid mostly useless back-and-forth on stylistic differences, delegate these things to an automated system.
There are plenty of good linters and static code analysis tools out there that let your automatically find and highlight issues with the style of 
code that is being written. Additionally: most modern IDE's allow developers to import a stylesheet into their tooling, and reformat the code 
prior to committing it to the source control system. 

{{<tip text=`
Let a machine handle the easily spotted and corrected "issues" in your code base, enforcing consistency.
Spend your time on digging into the important things, such as functionality or the architecture of the code.
` >}}

## Criticism & Clarifications

- Standardisation can drift into bureaucracy—review the rule set periodically and delete guidance that no longer adds value.
- People may treat linters as antagonists; frame automation as a time saver so humans focus on design and behaviour, not whitespace.
- Global mandates are risky: allow teams to diverge deliberately when domain constraints (embedded, data science, etc.) require alternate conventions.
