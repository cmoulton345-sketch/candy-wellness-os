# AUDIT REPORT — MECE Agent OS Redesign

> **Phase:** 0 (Read-only)
> **Date:** 2026-08-17
> **Status:** AWAITING APPROVAL — no files will be modified until you sign off on proposed fixes.

---

## 1. OVERLAPS (MECE Violations)

### OV-1: Chris Voss claimed by both The Pen and The Closer

| File | Claim |
|------|-------|
| [pen.md:51](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/pen.md#L51) | "Chris Voss — Tactical empathy in language: labeling, mirroring, calibrated questions…" |
| [closer.md:36](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/closer.md#L36) | "Chris Voss — *Never Split the Difference.* FBI hostage negotiation weaponized for commerce…" |

**Diagnosis:** Voss techniques appear in both agents' synthesis stacks. The Pen uses Voss for *persuasive prose* (written language). The Closer uses Voss for *live negotiation* (objection handling, frame control). The techniques are the same; the application context differs. This is still an overlap because neither file constrains when Voss applies.

**Proposed fix:** Remove Voss from The Pen's synthesis stack entirely. The Pen already has 10 minds — Voss's labeling/mirroring techniques are a negotiation tool, not a copywriting tool. If The Pen needs empathy in copy, Cialdini's Unity principle and Hopkins's letter-form cover it.

---

### OV-2: "Positioning" claimed by both The Strategist and The Pen

| File | Claim |
|------|-------|
| [strategist.md:50](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/strategist.md#L50) | "Brand positioning and category design" |
| [pen.md:45](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/pen.md#L45) | "Dan Kennedy — Category positioning or vanish" |

**Diagnosis:** The Strategist owns *strategic* positioning (Dunford canvas, market category). The Pen invokes Kennedy's *positioning in copy* (movement-building, category framing in words). These are genuinely different — one is research/analysis, the other is language execution — but the word "positioning" in both files creates routing ambiguity.

**Proposed fix:** In The Pen, change Kennedy's framing from "category positioning" to "movement-building and tribal framing in copy" to eliminate the word overlap while keeping the function.

---

## 2. GAPS (Orphaned System Functions)

### GAP-1: Memory Protocol — file deleted, instructions remain

`memory.md` was archived. But **all 15 active agents** still contain:
```
At the start of every conversation, follow the memory system defined in memory.md (.agent/rules/memory.md).
```
This instruction now points to a file that does not exist in `.agent/rules/`. The memory directory (`memory/`) and its files still exist on disk, so the *data* is intact, but the *instructions for how to use it* are gone.

**Proposed fix:** Move the memory protocol into `core_axioms.md` as a new section (e.g., OS.13 — Memory Protocol). This way every agent inherits the instructions through the constitutional layer instead of referencing a standalone file. Then update each agent's memory protocol line to say "follow the memory system defined in core_axioms.md (OS.13)" or simply remove the line since `inherits: core_axioms.md` already loads it.

---

### GAP-2: Intent Clarification — no owner

The archived `clarity.md` owned "intent clarification" — when Joe's request is ambiguous, Clarity would ask clarifying questions before routing. No active agent currently has this responsibility.

**Proposed fix:** Add a fallback clause to `ax.md`: *"Any request that is ambiguous or maps to no agent's charter defaults to Ax, who either answers directly or routes with a one-line justification."* This makes Ax the fallback clarifier, which aligns with the conductor role.

---

### GAP-3: Proofreading — no owner

The archived `consistency.md` owned grammar, punctuation, spelling, and formatting audits. The `/proofread` workflow still exists but no active agent file owns the execution.

**Proposed fix:** Declare proofreading as silent infrastructure owned by the `/proofread` workflow. Add a one-line note in `core_axioms.md` under OS.3 (Clarity First): *"Proofreading is executed via the /proofread workflow and is not owned by any agent."*

---

### GAP-4: File Organization — no owner

The archived `information-architect.md` owned file structure, naming conventions, and workspace organization. No active agent claims this.

**Proposed fix:** Fold into Ax's scope. Ax already owns "ALL system architecture" — file organization is a natural extension. Add "workspace file organization and naming conventions" to Ax's YOU OWN list.

---

### GAP-5: Polymath Fallback — no owner

The archived `stephen_universal.md` was the "polymath fallback" — answering questions that no specialist covers. No agent currently has this role.

**Proposed fix:** This is the same gap as GAP-2. The fallback clause in Ax covers it: if no agent owns the question, Ax answers directly. No separate polymath agent needed.

---

## 3. CONTRADICTIONS (vs. core_axioms.md)

### C-1: Stale routing references to archived personas (6 active files)

These active files route to agents that no longer exist:

| File | Line | Stale Reference | Should Route To |
|------|------|-----------------|-----------------|
| [sentry.md:36](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/sentry.md#L36) | Chain of Custody | **Nate**, **Atlas** | **Ax**, **The Strategist** |
| [foreman.md:21](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/foreman.md#L21) | Chain of Custody | **Nate**, **Atlas** | **Ax**, **The Strategist** |
| [envoy.md:21](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/envoy.md#L21) | Chain of Custody | **Atlas**, **Nate** | **The Strategist**, **Ax** |
| [crypto.md:36](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/crypto.md#L36) | Chain of Custody | **Clarity** | **Ax** |
| [crypto.md:345-346](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/crypto.md#L345) | Boundaries | **Brunsen**, **Nate** | **The Pen**, **Ax** |
| [socrates.md:189-190](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/socrates.md#L189) | Boundaries | **Brunsen**, **Nate** | **The Pen**, **Ax** |
| [earl.md:380-382](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/earl.md#L380) | Boundaries | **Atlas**, **Brunsen**, **Nate** | **The Strategist**, **The Pen**, **Ax** |

**Proposed fix:** Find-and-replace all stale references in the 6 active files with their MECE replacements.

---

### C-2: Malformed YAML frontmatter (7 files)

Seven agent files have broken frontmatter — the `---` delimiters are misplaced or duplicated, causing the YAML block to not parse correctly. The content starts with `Session Behavior Rules` before the frontmatter, or has two separate `---` blocks:

| File | Issue |
|------|-------|
| [crypto.md](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/crypto.md#L1) | Starts with blank line + Session Behavior; frontmatter at line 16-24 |
| [distiller.md](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/distiller.md#L1) | Same pattern — Session Behavior first, frontmatter at line 17-25 |
| [earl.md](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/earl.md#L1) | Same — frontmatter at line 16-24 |
| [jarvis.md](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/jarvis.md#L1) | Same — frontmatter at line 18-26 |
| [sentry.md](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/sentry.md#L1) | Same — frontmatter at line 16-24 |
| [socrates.md](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/socrates.md#L1) | Same — frontmatter at line 16-23 |
| [wave.md](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/wave.md#L1) | Same — Memory Protocol first, frontmatter at line 7-10 |

**Root cause:** An earlier batch edit session prepended Session Behavior Rules and Memory Protocol blocks *before* the YAML frontmatter, breaking the expected file structure where `---` must be the very first line.

**Proposed fix:** Reorder each file so YAML frontmatter is lines 1–N, followed by the agent content. No content changes — structural fix only.

---

## 4. DRIFT RISKS (Nondeterministic Instructions)

### DR-1: Self-naming clauses in 4 pipeline agents

Each of the 4 new pipeline agents contains a nondeterministic instruction:

| File | Line | Text |
|------|------|------|
| [strategist.md:41](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/strategist.md#L41) | "Your name is yours to choose." |
| [pen.md:53](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/pen.md#L53) | "Your name is yours to choose." |
| [closer.md:46](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/closer.md#L46) | "Your name is yours to choose." |
| [steward.md:43](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/steward.md#L43) | "Your name is yours to choose." |

**Risk:** Every new session, each agent may pick a different name. Other agents that route to "The Pen" or "The Closer" will use the file-level name, but the agent itself might introduce itself as something else. This creates identity fragmentation — the roster table says one thing, the agent says another, and routing instructions become unreliable.

**Proposed fix:** Remove self-naming. Assign fixed names. Proposed names (for your approval):

| File | Current Label | Proposed Fixed Name | Rationale |
|------|--------------|---------------------|-----------|
| strategist.md | "The Strategist" | **Scout** | Short, active, parametrically sparse (avoids collision with generic "strategist" tokens), captures intelligence-gathering |
| pen.md | "The Pen" | **Quill** | Clean, distinctive, the instrument of persuasion — same metaphor but a proper name |
| closer.md | "The Closer" | **Forge** | Deals are forged, not closed — active, metallic, decisive |
| steward.md | "The Steward" | **Harbor** | Where clients dock and feel safe — warmth, refuge, long-term shelter |

*(You may override any of these.)*

---

### DR-2: Factory Protocol still contains "let the agent choose its own name"

[factory_protocol.md:44](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/factory_protocol.md#L44): *"For synthesis: name 3-5 minds and let the agent choose its own name."*

This propagates DR-1 to every future spawn.

**Proposed fix:** Change to: *"For synthesis: name 3-5 minds. The spawning agent assigns a fixed one-word name before deployment."*

---

### DR-3: No `incident_log.md` exists

`core_axioms.md` OS.12 references an "incident log" and factory_protocol.md references it for Birth Spec Option C inheritance. But no `incident_log.md` file exists anywhere in the repo.

**Proposed fix:** Create `.agent/evals/incident_log.md` (Phase 3 deliverable) and update OS.12 + factory_protocol.md to reference it at that specific path.

---

### DR-4: Handoff contracts between pipeline stages don't exist

The 4 pipeline agents reference each other's outputs (e.g., Strategist → Pen, Pen → Closer, Closer → Steward) but no file defines *what artifact is passed at each boundary*. Each agent can invent a different format every time.

**Proposed fix:** Create `.agent/rules/handoffs.md` (Phase 2 deliverable) with required-fields checklists for each boundary.

---

## 5. STRUCTURAL DAMAGE (From Previous Edit Session)

### SD-1: Duplicate Session Behavior blocks in earl.md

[earl.md](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/earl.md) has Session Behavior Rules at lines 2-8 (from the prepend bug) AND the original personality/operating rules starting at line 60+. There are also **two** Boundaries sections — the new MECE boundary (line 44-52) and the old boundary section (lines 378-382) that still routes to Atlas, Brunsen, and Nate.

**Proposed fix:** Remove the duplicate Session Behavior block (lines 1-13), remove the old stale Boundaries section (lines 378-382), keep only the MECE boundary.

---

### SD-2: Duplicate self-introduction instructions in several files

Multiple files have doubled self-introduction instructions like:
```
(ONLY when user uses your activation phrase or explicitly asks who you are — never repeat this unprompted) (ONLY when user uses your activation phrase or explicitly asks who you are — never repeat this unprompted)
```

Found in: [crypto.md:40](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/crypto.md#L40), [sentry.md:40](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/sentry.md#L40), [earl.md:57](file:///c:/Users/Admin/Agents/radical_simplicity_ai_os_v2/.agent/rules/earl.md#L57)

**Proposed fix:** Deduplicate during the frontmatter reordering pass.

---

## 6. PROPOSED FIX PLAN (Summary)

| ID | Fix | Phase |
|----|-----|-------|
| OV-1 | Remove Voss from Pen's synthesis | Phase 1 |
| OV-2 | Reword Kennedy in Pen to avoid "positioning" overlap | Phase 1 |
| GAP-1 | Move memory protocol into core_axioms.md as OS.13 | Phase 1 |
| GAP-2+5 | Add fallback clause to ax.md | Phase 1 |
| GAP-3 | Declare proofreading as /proofread workflow in core_axioms | Phase 1 |
| GAP-4 | Add file org to Ax's scope | Phase 1 |
| C-1 | Fix 6 files with stale routing references | Phase 1 |
| C-2 | Fix 7 files with malformed frontmatter | Phase 1 |
| DR-1 | Remove self-naming from 4 pipeline agents, assign fixed names | Phase 1 |
| DR-2 | Fix factory_protocol self-naming clause | Phase 1 |
| DR-3 | Create incident_log.md | Phase 3 |
| DR-4 | Create handoffs.md | Phase 2 |
| SD-1 | Remove duplicate blocks in earl.md | Phase 1 |
| SD-2 | Deduplicate self-intro instructions | Phase 1 |
| — | Restructure Pen's 11-mind synthesis into anchor + bench | Phase 1 |
| — | Same for Closer (5 minds) and Steward (5 minds) | Phase 1 |

---

> **IMPORTANT:** No files have been modified. Awaiting your approval on the proposed fixes above before proceeding to Phase 1.
> 
> Specific decisions I need from you:
> 1. **Pipeline agent names** — approve Scout/Quill/Forge/Harbor or suggest alternatives
> 2. **Voss removal from Pen** — confirm you're OK dropping Voss from The Pen (Closer keeps full Voss)
> 3. **Memory protocol location** — confirm moving it into core_axioms.md as OS.13
