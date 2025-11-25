+++
title = "Avoid Gold Plating"
author = "Stijn Dejongh"
problem = "You are spending much more time and mental effort on a piece of software than is needed or valuable."
description = "Write readable code that is as well-designed as it needs to be at this point in time."
summary="""
The practice of "Avoid Over-Engineering" involves writing code that is as well-designed as it needs to be at the current point in time, 
adhering to the basic principles of clean code and design. The aim is to improve speed, stability, readability, and maintainability by avoiding 
unnecessary complexity and functionality that may never be used. Developers should take note of more generic solutions that come to mind and revisit them later, 
iteratively enhancing the codebase when necessary.
"""
categories = [
    "software development",
]
tags = [
    "elegance", "KISS", "YAGNI", "complexity"
]
uuid="94a558cd-4e86-4814-a5e9-d6ecafcb0d6b"
aliases=["94a558cd-4e86-4814-a5e9-d6ecafcb0d6b"]
outputs = ['html', 'json']
ammerse = [
  {name = "agile", delta = "0.35", rationale="The analysis supports agility by reducing unnecessary work and focusing on immediate needs. However, it may limit future adaptability if initial designs do not consider potential changes."},
  {name = "minimal", delta = "0.8", rationale="The analysis promotes minimalism by encouraging simplicity and avoiding unnecessary complexity."},
  {name = "maintainable", delta = "-0.25", rationale="While the practice improves initial readability, it may lead to significant rework and technical debt due to lack of future-proofing."},
  {name = "environmental", delta = "0.15", rationale="The practice indirectly supports environmental values by promoting efficient use of resources."},
  {name = "reachable", delta = "0.2", rationale="The practice makes immediate goals more attainable but may hinder long-term goal achievement due to lack of future-proofing."},
  {name = "solvable", delta = "0.75", rationale="The practice supports effective problem-solving by reducing complexity."},
  {name = "extensible", delta = "-0.7", rationale="The practice may initially limit extensibility and require significant rework if future requirements are not considered."}
]
pubdate="2023-09-16"
image="practices/keep_it_simple_cover"
related_concepts = [
  "b86230c6-49fb-4792-9008-a5241c5cdcb2",
  "1f3849c8-28bc-4934-95bf-66d9dcee6858"
]
related_practices = [
  "d8d2cbc3-1f28-4e6b-937f-2d8cf0bbaed1"
]
further_exploration = [
  { type="raw", author="Nauerby, E. M.; Kragbæk, M.; et al.", year="2019", title="FizzBuzz: Enterprise Edition", site="GitHub.com", link="https://github.com/EnterpriseQualityCoding/FizzBuzzEnterpriseEdition" },
  { type="tool", id="d81319c3-355c-43e0-bbd5-0eb3dfe71c76" },
  { type="biblio", id="e15a25a0-6c08-4b78-b593-ca54eea8cce2"},
  { type="biblio", id="93c3d298-690e-48b5-8140-b34ce90c2083"},
  { type="biblio", id="8572443d-2c27-462a-b9d7-839dd6e4d58b"}
]
+++

## Problem statement

Programmers tend to over-design simple things to make them more capable, clever, or beautiful than needed. They often spend far more time and mental effort than necessary—or worse, build functionality that will never be used.

## Intent

* Speed: Lower throughput time of changes
* Stability: Less regression or bugs introduced during tasks
* Lower function point count of changes
* Reduced cyclic complexity
* Improved readability

## Solution

* write code that is as well-designed as it needs to be at this point in time.
* make sure the code you write at this point in time adheres to the basic principles of clean code and design
* when an idea for a more generic solution comes to mind during your implementation, take note of it and revisit it afterwards
* iteratively enhance the codebase when it makes sense to do so: when tackling a new code challenge, look for reusable components or
  structural improvements.

In order to avoid over-complicating your code, ask yourself:
* _"Is this code likely to be changed/expanded in the future?"_
* _"Is my design solving an issue that is here NOW, or am I solving an issue that might never happen?"_
* _"If this expected issue occurs in the future, can it be easily fixed at that time?"_

## Contextual forces
This practice can be applied in software development projects, particularly in contexts where efficiency, readability, and maintainability are
critical. It is suited for projects with well-defined short-term goals and limited lifespans, where over-engineering could lead to wasted time and
effort.

### Enablers
The following factors support effective application of the practice:

* **Clear Immediate Requirements:** When the problem at hand is well-defined and unlikely to change drastically in the short term.
* **Cost-Sensitive Projects:** In projects where development time is expensive and efficiency is critical.
* **Readability and Maintainability:** When maintaining clear, understandable code is a priority.
* **Limited lifespan:** The code in its current form expected to be decommissioned in the short- to midterm. Due to it solving a 
  specific -temporary- problem or due to the unpredictability of future requirements causing a complete rewrite.

### Deterrents
The following factors prevent effective application of the practice:

* **Long-Term Projects:** When long-term scalability and extensibility are major concerns.
* **Future-Proofing Needed:** When anticipating significant future requirements is crucial.
* **High-Complexity Systems:** In systems where thinking ahead can prevent larger issues down the line.
* **Unclear Requirements:** When the requirements (or the problem to solve) are vaguely described or likely to change significantly in the short 
  term.

## Rationale

* The level of refinement of a codebase should match the problem scope and expected lifespan.
* Over-engineering introduces unnecessary complexity, making code harder to understand and maintain.
* Premature optimization often targets problems that never materialize, wasting valuable development time.

## Application

### Consequences

* **Short-Term Focus:** The pattern’s emphasis on the present might neglect potential future needs, leading to frequent refactoring.
* **Cleverness and Ego:** Developers might still over-complicate to showcase their skills, defeating the pattern’s purpose.
* **Technical Debt:** The pattern might lead to accumulating technical debt, as developers might not consider future requirements. Consistent
  under-designing is likely to take place, making the codebase fragile when new requirements emerge.
* **Team Dynamics:** Developers may feel demotivated if their ideas for better designs are consistently postponed.

### Mitigation strategies

* **Regular Reviews:** Implement regular code reviews to ensure adherence to simplicity principles while considering future requirements.
* **Refactoring:** Encourage refactoring to address technical debt and ensure the codebase remains maintainable.
* **Flexible Design Principles:** Encourage the use of design patterns that balance simplicity with flexibility, allowing for future enhancements
  without major overhauls.
* **Developer Education:** Train developers on the importance of simplicity and the risks of over-engineering. Highlight successful case studies
  where avoiding gold plating led to project success.
* **Future-Proofing Guidelines:** Develop guidelines that help developers make informed decisions about when to anticipate future needs and when to
  focus strictly on current requirements.

By focusing on these strategies, the potential drawbacks of the pattern can be mitigated, ensuring that the code remains both simple and robust enough to handle evolving requirements.

## Examples

{{<image
  src="/images/practices/overdesign"
  size="35%"
  alt="An image of a bicycle with a robotic rear wheel, looking highly complicated and over-engineered" >}}

### How not to do it: Enterprise Quality Fizz Buzz

"Fizz Buzz" is a children's game well known to software developers, as it is commonly used as a training exercise or interview question. 
The aim is to write a program that counts to a given number. When the current count is divisible by 3, the program should print out `Fizz` rather 
than the current count. When the current count is divisible by 5, it should print out `Buzz`. If the number divisible by both, we expect `FizzBuzz`.
The Fizz Buzz exercise aims to gauge basic programming aptitude, such as the use of loops and accumulators.

Usually, one can write a program to do this in a dozen lines of code. As satire to the tendency of programmers in big corporations to 
overcomplicate their code, people have co-created a version of this program that counts upwards of 10'000 lines of code.
This marvel of over-engineering is available online on [github.com/EnterpriseQualityCoding/FizzBuzzEnterpriseEdition](https://github.
com/EnterpriseQualityCoding/FizzBuzzEnterpriseEdition)

To give you an idea of how far the authors took it: the Enterprise FizzBuzz system uses Spring, and implements nearly all Go4 patterns.  
The class below shows a strategy-injection visitor to determine which output formatter to use for a given number. 

```java
/**
 * Context for FizzBuzzOutputGeneration
 */
 public final class FizzBuzzOutputGenerationContext implements OutputGenerationContext {

	private final DataPrinter printer;
	private final IsEvenlyDivisibleStrategy strategy;

	/**
	 * @param strategy IsEvenlyDivisibleStrategy
	 * @param printer DataPrinter
	 */
	public FizzBuzzOutputGenerationContext(final IsEvenlyDivisibleStrategy strategy,
			final DataPrinter printer) {
		super();
		this.strategy = strategy;
		this.printer = printer;
	}

	/**
	 * @return
	 */
	@Override
	public DataPrinter getPrinter() {
		return this.printer;
	}

	/**
	 * @return
	 */
	@Override
	public IsEvenlyDivisibleStrategy getStrategy() {
		return this.strategy;
	}

}
```

## Criticism & Clarifications

- Avoiding gold plating is not a license to ignore architecture; revisit decisions regularly so short-term hacks do not calcify into core systems.
- Critics sometimes equate this practice with complacency. Clarify that the goal is sequencing improvements, not abandoning quality altogether.
- Teams in safety-critical or highly regulated domains may need more upfront investment—adapt the heuristic to match compliance or risk thresholds.
