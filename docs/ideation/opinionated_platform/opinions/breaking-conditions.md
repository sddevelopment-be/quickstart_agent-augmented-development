+++
title = "Set stopping conditions"
author = "Stijn Dejongh"
problem="You tend to push too hard trying to reach a goal, or invest more than you can support."
description = "Put a hard limit on how much you are willing to invest into a certain endeavour."
summary= """
Setting stopping conditions helps maintain a healthy balance between effort and outcome, preventing overextension and resource depletion. 
This technique promotes sustainability, realistic goal-setting, and adaptability, especially when initial objectives need to be revised. 
While it has significant positive impacts on agility, maintainability, and reachability, it is crucial to apply it thoughtfully to avoid 
being overly cautious and missing out on valuable opportunities.
"""
categories = [
    "productivity",
]
tags = [
    "goals", "pivoting"
]
outputs = ['html', 'json']
uuid="49014706-77a2-4b8f-82de-75c16cac9c8c"
aliases=["49014706-77a2-4b8f-82de-75c16cac9c8c"]
ammerse = [
  {name = "agile", delta = "1", rationale="The analysis significantly supports agility by fostering adaptability and awareness of limitations."},
  {name = "minimal", delta = "0.25", rationale="The analysis promotes minimalism by encouraging clear and simple stopping criteria."},
  {name = "maintainable", delta = "0.75", rationale=" The analysis supports maintainability by ensuring resources are managed effectively and not over-extended."},
  {name = "environmental", delta = "0.15", rationale="The analysis promotes alignment with environmental and ethical standards, encouraging consideration of broader impacts."},
  {name = "reachable", delta = "-0.5", rationale="While the analysis promotes risk reflection, it can negatively impact the pursuit of reaching goals due to its emphasis on knowing when to quit."},
  {name = "solvable", delta = "0.35", rationale="The analysis supports effective problem-solving by ensuring goals are manageable and resources are not over-committed."},
  {name = "extensible", delta = "0", rationale=" The analysis supports extensibility by preventing over-commitment and allowing for reassessment but may introduce rigidity if stopping conditions are too strict."},
]
image="practices/stopping_conditions"
pubdate="2023-08-26"
related_concepts = [
  "b86230c6-49fb-4792-9008-a5241c5cdcb2",
  "3d5b775a-bd5d-40de-8ed3-d390dae16b7b"
]
related_practices = [
  "d8d2cbc3-1f28-4e6b-937f-2d8cf0bbaed1",
  "09986d9e-cd80-4016-8000-c62ed5064914",
  "1bdb4866-7c15-46b1-ad38-26111791eed5"
]
further_exploration=[
  {type="raw", author="Various Authors", year="2023", title="Game Theory", site="wikipedia.org", link="https://en.wikipedia.org/wiki/Game_theory"},
  {type="raw", author="Various Authors", year="2023", title="Pareto efficiency", site="wikipedia.org", link="https://en.wikipedia.org/wiki/Pareto_efficiency"},
  {type="raw", author="Various Authors", year="2023", title="Computer Optimization", site="wikipedia.org", link="https://en.wikipedia.org/wiki/Program_optimization"},
  {type="raw", author="McKay B.; McKay K.", year="2022", title="Podcast #840: When to Quit", site="artofmanliness.com", link="https://www.artofmanliness.com/character/behavior/podcast-840-when-to-quit/"},
  {type="raw", author="Greenberg, S.", year="2013", title="Why We Overvalue What We No Longer Have: The Psychology of Loss", site="spencergreenberg.com", link="https://www.spencergreenberg.com/2013/10/why-we-overvalue-the-things-we-lose-the-psychology-of-loss/"}
]
+++

## Problem statement

You tend to push too hard trying to reach a goal, or invest more than you can support.

## Intent

* Get a clear understanding of what is expected of you.
* Do not lose more than you are willing to lose in the pursuit of a goal.

## Solution

* Before starting a task clearly define what `positive evolution`/`success` means, also clearly define `negative impact`/`warning signals`.
* Set a hard limit on what you are willing to sacrifice in order to try and reach your goal.
  * make these as concrete as possible, similar to using SMART goals.
  * Focus on specifying your limits in various areas: financial, physical, mental, moral, time-bound, ...
* STOP IMMEDIATELY if you cross this threshold.
* When you are working on a commitment you made to someone else, be upfront about how far you are willing to go to achieve it.
  * People might still be disappointed you back out, but since you acted with honesty and integrity, no blame should be attributed to you.

Rather than only focussing on tracking progress, it is wise to also keep tabs on the cost it is inducing into your life or organization.
This is important if you want to evaluate the ROI of an approach. If you notice you are sacrificing too much of what is dear to you: stop striving to reach that particular goal.
To better cope with the disappointment of "needing to give up", it helps to see most endeavours as experiments rather than "do-or-die" type of deals.

In the end, reaching your goals at all costs is usually not really worth it.

## Contextual forces

### Enablers
The following factors support effective application of the practice:

* **Clear Boundaries:**  You have a clear idea of how far you can stretch, and what you are willing to invest in attempting to reach a goal.
* **Honest Communication:** When there is open and honest communication about the limits and conditions with stakeholders.
* **Supportive Environments:** In environments where stopping is respected and not seen as a failure.
* **Significant Investment:** When goals require significant investment and potential sacrifice, making it crucial to have predefined limits.

### Deterrents
The following factors prevent effective application of the practice:

* **Sunk-Cost Fallacy:** In cultures heavily influenced by the [sunk-cost fallacy](glossary/#sunk-cost-fallacy), where stopping is viewed 
  negatively. 
* **External Pressures:** When external pressures or expectations make it difficult to adhere to stopping conditions.
  * You feel sense of shame when stopping. Our culture has though us that __"quitters never win, and winners never quit"__.
  * You are unable to effectively adapt to the situation, as the goal is deemed to be a "do or die" situation.
  * Others are used to you going beyond your limit, they will be disappointed when you stop doing so.
* **Unpredictable Situations:** In highly unpredictable situations where flexibility is crucial, and setting stopping conditions upfront is 
  challenging.
* **Inflexibility:** When rigid stopping criteria hinder adaptability and responsiveness to changing circumstances.

## Rationale

* We are not purely rational beings: The feelings of _"loss"_ and _"failure"_ are not pleasant ones, as humans are hardwired to struggle
  for survival. We are also creatures of habit, favouring known situations over unknown ones.
* We are generally not great at knowing our limits.
* Goals are extremely motivating, but can push us well beyond our limits.
    * This is illustrated by marathon runners feeling severely unwell and [still continuing the race](https://en.wikipedia.org/wiki/List_of_marathon_fatalities), and people dying while [climbing mountains](https://en.wikipedia.org/wiki/List_of_people_who_died_climbing_Mount_Everest).
* We (generally) want to do what is good for ourselves, those close to us, and the people we care about
* There is a cost of choice while working with limited resources: choosing to invest your resources (time, energy, money, health) into an
  endeavour automatically makes it unavailable for investment elsewhere.
* We can [condition ourselves](https://en.wikipedia.org/wiki/Behaviorism) by stating declarations of intent in _"When X happens, then I will Y"_.
  This [priming](https://en.wikipedia.org/wiki/Response_priming) making it easier to act in the way we want to.
* The Theory Of Constraints teaches us that holding too much work-in-progress reduces our ability to be effective.
* Our mental capacity is limited. When we spend too much time fretting over the things we ought to do, there is little room to work on the things we are doing.

## Application

### Consequences

* **Short-Term Focus:** The pattern’s emphasis on current limits might neglect potential future opportunities, leading to a conservative approach.
* **External Pressures:** Individuals might still feel pressured by others to exceed their set limits, making adherence difficult.
* **Over-Cautiousness:** Risk of setting overly cautious stopping criteria that prevent necessary risk-taking and innovation.
* **Inflexibility:** Setting rigid stopping criteria might hinder adaptability in unpredictable environments, where flexibility is crucial.
* **Stagnation:** Lack of problem-solving skills and adaptability might lead to goals being abandoned prematurely, hindering growth and development.
* **Loss Aversion:** The fear of loss might prevent individuals from setting realistic stopping criteria, leading to overextension and resource depletion.
* **Not keeping commitments:** Setting stopping criteria too early might prevent individuals from reaching their full potential and achieving their 
  goals. When working on a commitment made to someone else, it is important to be upfront about how far you are willing to go to achieve it.

### Mitigation strategies

* **Regular Reassessment:** Regularly review and adjust stopping criteria based on new information and evolving contexts to maintain a balance
  between caution and opportunity.
* **Communication and Support:** Foster a supportive environment where individuals feel comfortable setting and respecting their limits. Open
  communication about the rationale behind stopping criteria can help mitigate external pressures. Provide support and training to help teams adapt
  to new goals and maintain focus on achievable objectives.
* **Balanced Approach:** Encourage a balanced approach where stopping criteria are set thoughtfully but flexibly, allowing for necessary
  adjustments without completely abandoning limits.
* **Improve Problem-Solving Skills:** Provide training and resources to enhance the ability to solve problems effectively. Foster a more agile
  environment where feedback is regularly incorporated, and strategies are adjusted as needed.
* **Risk Management:** Develop a risk management strategy that considers potential losses and gains, allowing for informed decision-making and
  realistic goal-setting.
* **Involvement and Accountability:** Involve team members in the decision-making process and hold them accountable for their commitments. Encourage
  open dialogue and feedback to ensure that stopping criteria are realistic and achievable. When the need arises, provide guidance and support 
  to be able to stop when necessary. Involve stakeholders in the decision-making process to ensure that stopping criteria, and the rationale 
  behind the decisions, are clearly communicated and understood.

## Examples

### Use Cases / Testimonials

#### Changing careers: starting a business

by: __Stijn Dejongh__

One of the concerns of leaving a comfortable employment situation, and trading it for a highly uncertain one, is that you could end up without an income.
While this is certainly a concern, most people have more leeway than they might realize. 

At one point, I was considering switching from a position of full-time employment to becoming a self-employed freelance software developer. 
For the duration of my entire life up until that point, I had tried to be financially sensible, not taking too large risks in order to avoid a reduction in luxury.
This had left me with quite a hefty sum of money in my bank account. For the next month or two, I kept close tabs on where my expenses went. Most of it was allocated to food, drink, technical books, and entertainment. With this data in hand, I calculated that it would take about 2 years before I completely ran out of money.

Obviously, this was not an acceptable future to me, so I rethought the situation to be more of an experiment.
Then I asked myself: "How much of my money am I willing to pay to know whether this is a viable way of life for me?". 
Turns out what I was willing to spend came down to about 4 months of living expenses. 
Considering I needed some margin if I were to go back to working as a full-time employee, I gave myself 3 months to start working as a freelancer.
This means I set myself a limit, a breaking condition, before I quit my job. The condition was: "If I do not have a signed multi-month freelance contract within the next three months, I will abandon the plan and focus on finding stable employment again".

I discussed my intent with my then-fiancee (now wife), as it also affected her. She was okay with delaying our long term plans with about one year in case I did not reach my intended goal.
This gave me two things. Foremost, it helped reassure me that I was not doing harm to the people I cared about. Secondly, it served as a 
sanity-check of my plans. If my goal was completely unrealistic, she would have undoubtedly told me at that point.

## Criticism & Clarifications

- Stopping conditions can be weaponised to mask fear of discomfort; pair them with courageous goals so they invite experimentation, not avoidance.
- In complex initiatives you rarely know the right threshold upfront—schedule reviews to adjust limits as new data emerges.
- Stakeholders may interpret quitting as lack of commitment. Communicate the rationale early and highlight how the practice protects long-term outcomes.
