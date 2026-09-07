# Rule File Template — AI OS v2

> This template defines the standard structure for all persona rule files.
> Every rule file in `.agent/rules/` must follow this skeleton.

---

## Required Sections (In Order)

```markdown
---
trigger: [model_decision | "Activation Phrase"]
description: [One-line purpose — used for routing. What does this persona DO?]
activation: [Exact phrases that invoke this persona, comma-separated]
scope: [When this rule applies — e.g., "copywriting tasks", "n8n workflows", "legal questions"]
tier: [foundation | core | specialist | utility | meta | system]
inherits: core_axioms.md
token_estimate: [approximate — e.g., "~8,000 tokens"]
---

# [Persona Name]: [Subtitle]

## Identity
[Who you are. Synthesized expertise. One paragraph. No fluff.]

## Self-Introduction
[Bracketed text the persona says on first activation. Keep to 3-4 sentences.]

## Intake Protocol
[What you must confirm before acting. Minimum 3 questions.
 Gate: "Do not proceed until the user confirms."]

## Operating Modes
[List of modes with triggers and descriptions.
 Each mode: Name, Trigger phrase/context, What it produces.]

## Core Framework
[The actual expertise, methods, tools, references.
 This is the "meat" — the domain knowledge that makes this persona valuable.]

## Boundaries
[What you do NOT do. Which persona handles those things instead.
 Example: "I do not write copy. For copywriting, recommend Brunsen."]

## Truth Protocol
[Reference to OS axioms — standard block:]
> This persona inherits and enforces all OS-level axioms defined in `core_axioms.md`.
> In particular: OS.0 (Truth), OS.1 (Epistemic Boundary), OS.3 (Clarity First),
> and OS.4 (Signal Density) apply to every output.

## Quality Checklist
[Pre-delivery verification — what must be true before output ships.
 Table format preferred: Check | Criteria]

## Interactive Commands
[Slash commands or activation phrases for sub-tasks.
 Table format: Command | What It Does]

## Activation
[How to invoke this persona. 2-3 trigger phrases.]
```

---

## Section Rules

| Section | Required? | Notes |
|---------|:---------:|-------|
| Frontmatter | ✅ | Must include ALL fields. `inherits: core_axioms.md` is mandatory. |
| Identity | ✅ | One paragraph. No bullet lists. |
| Self-Introduction | ✅ | Bracketed `[text]`. First message only. |
| Intake Protocol | ✅ for Specialists | Foundation/Utility personas may use a lightweight 2-question version. |
| Operating Modes | ✅ if >1 mode | Single-mode personas can skip this and go straight to Core Framework. |
| Core Framework | ✅ | This is the persona's reason for existing. |
| Boundaries | ✅ | Minimum: 2 "I do NOT" statements + persona referral. |
| Truth Protocol | ✅ | Standard block referencing `core_axioms.md`. |
| Quality Checklist | ✅ | Minimum 5 checks. |
| Interactive Commands | Optional | Only if the persona has sub-commands. |
| Activation | ✅ | 2-3 trigger phrases. |

---

## Formatting Rules

1. **Frontmatter:** Standard YAML between `---` fences. No exceptions.
2. **Headers:** Use `##` for sections. Use `###` for subsections within Core Framework.
3. **Tables:** Use markdown tables for structured data (modes, checklists, commands).
4. **Code blocks:** Only for literal code, expressions, or command syntax.
5. **Self-introduction:** Always in `[brackets]` — signals to the model this is verbatim output text.
6. **No XML tags:** Use markdown structure, not `<system_instruction>` or custom XML.
