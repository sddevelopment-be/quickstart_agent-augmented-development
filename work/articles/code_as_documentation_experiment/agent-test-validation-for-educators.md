# Understanding the Test Readability Check (Guide for Educators)

**Audience:** Non-technical educators and learning facilitators  
**Purpose:** Explain, in plain language, what “agents” are in this codebase, how our file-first framework works, and how we use a test readability check to make learning easier.  
**Pilot outcome:** Helpers could explain ~92% of the system from tests alone; the missing pieces were mostly “why we designed it this way” and “how it runs day to day.”

## I. What Are “Agents” Here?
- Think of agents as small assistants that read and write files. They don’t run big services; they simply pick up instructions from folders and leave their work in those same folders.  
- Tasks are YAML files that move through a clear path: `inbox → assigned → done → archive`. Because everything is in the repo, you can see progress without special tools.  
- This file-first, transparent setup (see the high-level design notes in `docs/architecture/design/async_multiagent_orchestration.md`) lets us add assistants for writing, reviewing, testing, and more—without extra infrastructure.

## II. Why Make Tests Readable?
- Tests can act like lesson plans. If someone can read them and explain the system, the tests are teaching effectively.  
- Clear tests speed up onboarding and reduce the need for meetings or long manuals.  
- When tests are unclear, learners and new team members struggle, and changes get riskier.

## III. The Test Readability Check (Side Note on the Experiment)
- **Learn from tests:** One helper reads only the tests and writes a plain-language summary of what the system does.  
- **Check and correct:** Another helper compares that summary to the real system and notes what the tests didn’t teach (design reasons, how it runs, security boundaries).  
- **Improve the lesson:** We add short notes or a small example so the tests teach those missing parts next time.

## A Simple Example
Our system moves task files through folders (`inbox → assigned → done → archive`). The tests showed that flow clearly—assignment, handoffs, timeouts, conflict detection. The helpers missed the “why”: we chose one coordinator and file-based storage for simplicity and transparency (documented in the architecture vision). Adding two sentences about that intent made the tests far more teachable.

## How Educators Can Use This
- Share the helper-written summary with new learners as a starter guide.  
- Pair it with a short note on design intent and operations to fill the gaps the helpers found.  
- Keep the gap list as a checklist when you update your teaching materials.

## Practical Notes
- The review takes about an hour; schedule it around major changes, not every edit.  
- Tests rarely explain “why” or operations—plan to add a sentence or two when helpers flag gaps.  
- Summaries age as code changes—rerun to keep them fresh.
