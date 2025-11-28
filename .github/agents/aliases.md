# **Command Aliases Reference**

*Last updated: 2025-11-15*
*Format: Markdown checklist (human-readable + agent-parsable)*
*Version: v1.1.0*

---

### **Execution Header Block**

> **Purpose:**
> Establish default behavior and mode selection logic when interpreting shorthand commands or ambiguous requests.
> Ensures consistent execution across writing, reasoning, and image-generation workflows.

---

#### **Default Interpretation Rules**

* [ ] If the command starts with `/`, treat it as a **structured operation**, not a conversational request.
* [ ] Always cross-reference this file with the **Operational Reference** for tone, and the **Strategic Reference** for intent.
* [ ] If command intent conflicts with either reference, **pause and flag ❗️ before execution**.
* [ ] When a command is missing but contextually implied, infer the closest alias from behavior patterns (e.g., “draft a new pattern” →
  `/draft-pattern`).
* [ ] Always confirm uncertain inferences before major action.

---

#### **Mode Selection**

* [ ] Default to **/analysis-mode** when requests involve reasoning, patterns, trade-offs, or system design.
* [ ] Use **/creative-mode** for narrative, metaphorical, or fictional explorations.
* [ ] Use **/meta-mode** for reflection about process, style, or collaboration patterns.
* [ ] Combine `/analysis-mode` + `/creative-mode` when bridging abstract reasoning with illustrative storytelling.
* [ ] If tone ambiguity arises, confirm which mode dominates before output.

---

#### **Priority Rules**

* [ ] Writing commands (e.g., `/draft-pattern`, `/refine-tone`, `/draft-episode`) take precedence over reasoning modes if explicitly invoked.
* [ ] When image generation and writing commands coexist, **run text generation first**, then derive images based on confirmed textual context.
* [ ] When multiple modes are invoked together, follow order of specificity:
    1. Explicit writing/image command
    2. Mode (analysis, creative, meta)
    3. Operational tone rules
* [ ] Never execute multiple conflicting content-generation commands without confirmation.

---

#### **Output Discipline**

* [ ] Label first outputs as **“FIRST PASS”** if exploratory.
* [ ] Use `✅` confirmation when aligned and stable.
* [ ] Use ❗️ for detected misalignment or unclear instruction.
* [ ] Use ⚠️ for partial confidence or assumption-based execution.
* [ ] For sequential commands, maintain state continuity — do not reset reasoning between dependent actions unless explicitly told.

---

### **Command Summary**

> **Read this first.**
> These shorthand commands encapsulate common behaviors and generation patterns. Each alias expands into a structured, context-aware workflow aligned with Operational and Strategic references.

---

## **1. Image Generation & Visual Modes**

### `/child-colouring`

* [ ] Generate **children’s colouring book–style line art**.
* [ ] Base the output on a provided **reference image**.
* [ ] Output must be **clean black-and-white outlines**, suitable for colouring.
* [ ] Remove unnecessary detail, maintain recognizability.
* [ ] Never infer likenesses of individuals without explicit photo input.
* [ ] Output: single image, A4 portrait preferred.

### `/mandala`

* [ ] Generate **mandala-inspired** interpretation of an image or concept.
* [ ] Use **symmetrical, radial balance**; avoid religious iconography.
* [ ] Output aesthetic: contemplative, geometric, printable.
* [ ] Maintain colour harmony and symmetry; allow mild abstraction.
* [ ] Output: single image, square aspect preferred.

### `/thumbnail`

* [ ] Create a **cover or thumbnail image** for blog posts, podcast episodes, or pattern entries.
* [ ] Composition: clean, minimalist, high contrast, typographically neutral.
* [ ] Style variants allowed: *flat-illustration*, *conceptual metaphor*, or *subtle symbolic*.
* [ ] Include optional overlay title text when requested.
* [ ] Prioritize visual consistency across series.
* [ ] Output: 16:9 ratio, web-optimized resolution.

---

## **2. Writing & Pattern Creation**

### `/draft-pattern`

* [ ] Start a new **Pattern Library entry** using the standard markdown template.
* [ ] Include sections: Problem / Intent / Solution / Contextual Forces / Rationale / Application / Examples / Criticism.
* [ ] Tone: structured, analytical, dry, context-sensitive.
* [ ] Populate scaffold placeholders if concept not yet fully known.

### `/refine-pattern`

* [ ] Improve an existing pattern draft.
* [ ] Ensure consistency in section order, heading syntax, and voice.
* [ ] Focus on **clarity, trade-off articulation, contextual accuracy**.
* [ ] Preserve authorial tone; avoid over-editing texture.

### `/summarize-pattern`

* [ ] Create a concise summary of a pattern.
* [ ] Output 2–3 paragraphs highlighting **intent, use cases, trade-offs**.
* [ ] Tone: balanced, professional, neutral.

### `/draft-blurb`

* [ ] Produce a short **“blurb” insert** for course or publication material.
* [ ] Tone: informal, classroom-like, conversational recommendation.
* [ ] Contrast with formal prose — lighter but still insightful.

### `/refine-tone`

* [ ] Rework a draft to match a specified tone (Pattern, Podcast, LinkedIn, Essay).
* [ ] Reference Operational Section 4 for tonal profiles.
* [ ] Confirm intent before large tonal shifts.

---

## **3. Social & Public Communication**

### `/summarize-for-linkedin`

* [ ] Convert reflective or technical piece into **LinkedIn-post** format.
* [ ] Short paragraphs, personal warmth, final reflective invitation.
* [ ] Strip meta commentary; retain one core takeaway.
* [ ] Avoid hashtags and performative hooks.
* [ ] Output: ~150–300 words.
* [ ] Tone: professional yet approachable.
* [ ] Avoid jargon, en/em dashes, and formulaic openings.

### `/summarize-for-medium`

* [ ] Adapt a piece for **Medium or cross-platform publishing**.
* [ ] Hybrid tone: engaging intro + layered depth.
* [ ] Maintain authentic voice; optimize layout for readability.
* [ ] Avoid formulaic openings and excessive formatting.

### `/extract-quote`

* [ ] Identify **quotable fragments** from longer texts.
* [ ] Prioritize clarity, resonance, standalone meaning.
* [ ] Output: `"Quote text" — Source reference`.

---

## **5. Reflection & Meta Analysis**

### `/compare-style`

* [ ] Compare drafts for tone and stylistic alignment.
* [ ] Evaluate: voice consistency, pacing, readability, authenticity.
* [ ] Output table or structured commentary with recommendations.

### `/evaluate-fit`

* [ ] Assess alignment with target medium (Pattern, Podcast, LinkedIn, Essay).
* [ ] Provide scorecard or qualitative judgment + adjustments.

### `/summarize-notes`

* [ ] Condense raw notes or meeting logs into clean outline.
* [ ] Highlight decision points, themes, uncertainties.

---

## **6. Image-Integrated Workflows**

### `/generate-diagram`

* [ ] Produce **diagram-as-code** snippets (PlantUML or Mermaid).
* [ ] Follow visual conventions (e.g., color categories) if defined.
* [ ] Maintain semantic relationships and clear labels.

### `/generate-thumbnail`

* [ ] Alias of `/thumbnail`; included for pipeline consistency.

---

## **7. Interaction Mode Shifts**

### `/analysis-mode`

* [ ] Switch to **systemic reasoning mode**.
* [ ] Provide structured breakdowns: Problem → Forces → Trade-offs → Patterns → Implications.

### `/creative-mode`

* [ ] Enter **imaginative narrative mode** for fiction, dialogue, metaphor.
* [ ] Maintain emotional authenticity and symbolic consistency.

### `/meta-mode`

* [ ] Reflect on process or collaboration patterns.
* [ ] Output concise insights on reasoning or alignment.

### `/fast-draft`

* [ ] Generate **quick ideation draft** without polish.
* [ ] Emphasize structure over phrasing; mark output “FIRST PASS”.

### `/precision-pass`

* [ ] Perform **line-level clarity revision**.
* [ ] Preserve meaning; tighten rhythm and phrasing.

---

## **8. Safety & Integrity Checks**

### `/validate-alignment`

* [ ] Compare output against Operational & Strategic references.
* [ ] Flag deviations with ❗️ (violation) or ⚠️ (partial confidence).
* [ ] Provide summary table: Alignment ✓ / Deviation ⚠️ / Violation ❗️.

### `/risk-scan`

* [ ] Review drafts for ambiguity or prompt-injection risk.
* [ ] Identify potential context leak points; propose neutral rewrites.

---

**End of Command Aliases Reference v1.1.1**
*Defines shorthand commands and execution protocols for consistent collaboration while preserving voice integrity and judgment standards.*
