---
description: Sequential axiom-by-axiom copy refinement with full audit trail. Default behavior for all Brunsen copy output unless user says "without audit" or "skip audit."
---

# /execute-recursive-axiom-audit

> **Default behavior for Brunsen.** All copy output runs through this pipeline unless the user explicitly opts out (e.g., "answer without audit", "skip audit", "quick draft").

---

## Prerequisites

Before starting, you MUST have:
1. **A defined copy unit** — headline, section, hook, page, email, ad, or any deliverable text
2. **Context** — who the audience is, what the product is, the awareness level
3. **The Axiom Stack** — loaded from `content-system/axioms/` (all files)

---

## Phase 1: The Sequential Forge (Axioms 0–9)

Process the copy through EACH axiom, one at a time, in order. For each pass:

### Pass Structure (repeat for Axioms 0 through 9)

```
AXIOM [#]: [Name]
VERDICT: PASS | FAIL | N/A
BEFORE: [copy as it entered this pass]
AFTER: [copy as it exits this pass — unchanged if PASS/N/A]
DELTA: [what changed and why, or "No change — [reason]"]
```

### The 10 Passes

| Pass | Axiom | Core Question |
|:-----|:------|:-------------|
| 0 | Truth | Is every word verifiably true? Would it survive scrutiny? |
| 1 | Projection Rule | Am I claiming to know something I haven't earned? Any unearned assumptions? |
| 2 | Absolutes Are Lies | Any absolutes? (always, never, everyone, nothing, everything) |
| 3 | Clarity Over Cleverness | Can the reader answer: What is this? Who for? What outcome? How to get it? |
| 4 | Mirrors, Not Projectors | Am I reflecting reality or dictating experience? |
| 5 | Research-to-Impact | Are claims backed by verifiable research merged with product truth? |
| 6 | Destination, Not Vehicle | Am I selling the transformation or describing the airplane? |
| 7 | Read-Aloud Test | Can every line be spoken aloud as a complete, natural sentence? |
| 8 | Hell Yes Architecture | Does it evoke felt need? Pre-loaded pain, proximity, asymmetric value, immediate gratification, invisible structure? |
| 9 | Somatic Compression | Does any phrase command a physical response? Triple-duty words? (N/A for body copy — applies primarily to hooks/headlines) |

### Rules for Each Pass

1. **Apply ONLY the current axiom.** Do not pre-optimize for later axioms.
2. **If the axiom doesn't apply** to this copy unit (e.g., Somatic Compression on an FAQ), log `N/A` with the reason. Do not force applicability.
3. **Log the delta honestly.** If nothing changed, say so. If the copy got worse, say that too.
4. **Preserve prior improvements.** A later axiom pass must not undo a valid change from an earlier pass unless there is a direct conflict — in which case, log the conflict and resolve in favor of the higher-priority axiom (lower number wins for 0-5; for 6-9, use judgment and log rationale).

---

## Phase 2: Gate Evaluation

After all 10 passes, re-evaluate the ENTIRE output against the full stack simultaneously.

```
## Gate Evaluation

### Final Copy
> [the copy after all 10 passes]

### Full-Stack Check
| Axiom | Status | Notes |
|:------|:-------|:------|
| 0 Truth | ✅/❌ | |
| 1 Projection | ✅/❌ | |
| 2 Absolutes | ✅/❌ | |
| 3 Clarity | ✅/❌ | |
| 4 Mirrors | ✅/❌ | |
| 5 Research | ✅/❌ | |
| 6 Destination | ✅/❌ | |
| 7 Read-Aloud | ✅/❌ | |
| 8 Hell Yes | ✅/❌ | |
| 9 Somatic | ✅/❌/N/A | |

### Verdict: SHIP | RE-FORGE
### Failure Reasons: [if re-forging — which axioms failed and why]
```

**Why a separate gate?** Sequential passes can introduce conflicts. A change that satisfies Axiom 6 (Destination) might violate Axiom 0 (Truth). The gate catches cross-axiom regressions.

---

## Phase 3: Re-Forge Loop (If Needed)

If the gate verdict is **RE-FORGE**:

1. Log the failure reasons
2. Use the failed output as the new input
3. Repeat Phase 1 (all 10 passes) — this is **Loop 2**
4. Re-evaluate at the gate
5. Maximum **3 loops** before escalating to the user with a summary of what's failing and why

```
## Loop [N] — Re-Forge
**Reason for re-forge:** [from previous gate failure]
**Starting input:** [output from previous loop]

[Repeat Pass 0-9 structure]
[Repeat Gate Evaluation]
```

---

## Phase 4: Save the Forge Log

After shipping (or after max loops + user decision), save the complete audit trail:

**Location:** `work_in_progress/forge_logs/`
**Filename:** `forge_[copy-unit-name]_[YYYY-MM-DD].md`

The file contains the COMPLETE audit trail from Phase 1 through final gate, including all loops.

### Forge Log Template

```markdown
# Forge Log: [Copy Unit Name]

**Date:** [YYYY-MM-DD]
**Input Type:** [headline / section / page / hook / email / ad]
**Persona:** [active Brunsen sub-persona]
**Loops Completed:** [1-3]
**Final Verdict:** SHIP | ESCALATED

---

## Raw Input
> [original copy before any axiom processing]

---

## Loop 1

### Pass 0: Truth
- **Verdict:** [PASS/FAIL/N/A]
- **Before:** [copy entering this pass]
- **After:** [copy exiting this pass]
- **Delta:** [what changed and why]

### Pass 1: Projection Rule
[same structure]

...through Pass 9...

### Gate Evaluation
[full-stack table]
**Verdict:** [SHIP/RE-FORGE]

---

## Loop 2 (if applicable)
[same structure as Loop 1]

---

## Final Output
> [the shipped copy]

## Audit Summary
| Axiom | Passes Applied | Key Changes |
|:------|:--------------|:------------|
| 0 | [count] | [summary] |
| ... | ... | ... |
```

---

## Opt-Out Triggers

The user can bypass this workflow with any of the following:
- "Without audit"
- "Skip audit"
- "Quick draft"
- "Just brainstorm"
- "Rough ideas"

When opted out, Brunsen still applies axiom principles but does NOT produce the sequential forge log.

---

## Integration Notes

- This workflow is **referenced in brunsen.md** as default copy behavior
- Forge logs are living artifacts — if the user asks to revise shipped copy, start a new forge log referencing the previous one
- The workflow applies to ALL Brunsen sub-personas (Master Copywriter, Headline Writer, Email, FB Ads, Google Ads, Landing Page)
