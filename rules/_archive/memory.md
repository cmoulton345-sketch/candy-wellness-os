---
trigger: always
description: Three-tier persistent memory system. Loads active context at session start, updates at session end, self-heals through staleness detection.
scope: all
tier: system
inherits: core_axioms.md
---

# Memory System Rule (v2.0)

## Architecture

```
memory/
├── active/                    # TIER 1: Always loaded at session start
│   ├── identity.md            # WHO — verified facts about Joe and the company
│   ├── current_state.md       # WHAT — active projects, pipeline, next actions
│   └── session_memory.md      # LAST SESSION — what just happened
│
├── long_term/                 # TIER 2: Loaded on demand based on task
│   ├── session_log.md         # Chronological session history
│   ├── decisions.md           # Key decisions and rationale
│   ├── preferences.md         # Working style, tools, brand standards
│   ├── joe_profile.md         # Joe's voice, story, beliefs (for copy)
│   └── psyche/                # PRIVATE — see Privacy Rules below
│       ├── joe_sessions.md
│       ├── candy_sessions.md
│       ├── candy_context.md
│       └── shared_patterns.md
│
├── long_term/                 # TIER 2 (continued)
│
└── _maintenance/              # TIER 3: System health (never loaded into context)
    └── memory_manifest.md     # Master index with staleness tracking
```

## At Session Start

### Always Load (Tier 1)
1. `memory/active/identity.md` — know who we are
2. `memory/active/current_state.md` — know what's in progress
3. `memory/active/session_memory.md` — know what just happened

### Load on Demand (Tier 2)
- **Writing copy or content:** `long_term/joe_profile.md` + `long_term/preferences.md`
- **Making strategic decisions:** `long_term/decisions.md`
- **Discussing past sessions:** `long_term/session_log.md`
- **Psyche persona active (Joe is user):** `long_term/psyche/joe_sessions.md` + `long_term/psyche/shared_patterns.md`
- **Psyche persona active (Candy is user):** `long_term/psyche/candy_sessions.md` + `long_term/psyche/candy_context.md` + `long_term/psyche/shared_patterns.md`

### Staleness Check
After loading Tier 1 files, check the `Last Updated` date on `current_state.md`. If older than 14 days:
- Flag: *"⚠️ `current_state.md` hasn't been updated in X days. Want me to refresh it?"*

## At Session End

1. **Always update** `active/session_memory.md` — replace with current session summary
2. **Always update** `long_term/session_log.md` — append entry for today's session
3. **Update if changed:** `active/current_state.md` — mark completed items, add new ones
4. **Update if new info:** `long_term/decisions.md` — log significant decisions
5. **Update if Psyche session:** the appropriate `psyche/*.md` journal
6. **Update `_maintenance/memory_manifest.md`** — refresh "Last Updated" dates for any modified files

## Privacy Rules (CONSTITUTIONAL — NO EXCEPTIONS)

1. `psyche/joe_sessions.md` — **Psyche reads when Joe is the active user.** Never surface to Candy.
2. `psyche/candy_sessions.md` — **Psyche reads when Candy is the active user.** Never surface to Joe.
3. `psyche/candy_context.md` — **Psyche-only.** Candy does not know this file exists. Approach as if meeting her fresh.
4. `psyche/shared_patterns.md` — **Psyche-only.** Neither party sees raw cross-references.
5. When the Psyche persona is active, identify the user before loading any private files.

## File Locations

All memory files live in `memory/` at the workspace root:
```
c:\Users\Admin\Agents\radical_simplicity_ai_os_v2\memory\
```

## Reference Pointers (Not Memory)

These files are NOT loaded at session start. They are referenced when needed:
- `sops/crypto_trading_system.md` — Trading system details (shelved)
- `work_in_progress/flowstateautomation/client_pipeline.md` — Active leads & outreach
- `knowledge/` — Reference documents (Toronto targets, Vancouver materials, WCB report, etc.)
