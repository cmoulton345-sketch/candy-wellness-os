# Learned Memory: Warden Live System Debugging Protocol

> **DATE:** 2026-08-28  
> **ORIGIN:** INC-001 (Hyperliquid Bot Auth Failure) & INC-002 (Warden Fire Drill)  
> **CATEGORY:** System Debugging / Architectural Control  

---

## Learned Behavior & Constraints

When any task touches live system failures, errors, bugs, or broken production services:

1. **Routing Intercept:** Route to **Warden FIRST** (Priority 0 gate in `dispatcher.md` and `router.yaml`) before Ax, Jarvis, Crypto, or any execution agent.
2. **Evidence Gate (4-Item Checklist):** No execution agent may act until all 4 items are provided verbatim:
   - Verbatim stack trace / raw error log line
   - Expected vs. actual behavior
   - Exact steps to reproduce / consistency pattern
   - Recent change delta (what changed before failure)
3. **Zero Speculation While Blocked:** While missing evidence, no agent may speculate or propose hedged theories ("it might be..."). Silence is mandatory until logs enter the gate.
4. **Acceptance Test:** No root cause may be stated as fact unless it passes: *"Does this root cause predict the exact error text/behavior observed?"* Otherwise, it must be labeled `Theory (unconfirmed): ...`.
5. **Two-Theory Limit & Knowledge Boundary:** If 2 proposed theories fail empirical testing, the execution agent MUST halt immediately, output a written knowledge-boundary statement detailing both theories and why each failed, and hand off to Warden for escalation.
6. **Commit Gate:** No code commit is permitted without explicit `WARDEN — PROCEED` logging.

---

## Key Enforcing Files
- [warden.md](file:///c:/Users/Joe/radical_simplicity_ai_os_joe-m/.agent/rules/warden.md)
- [ax.md](file:///c:/Users/Joe/radical_simplicity_ai_os_joe-m/.agent/rules/ax.md)
- [dispatcher.md](file:///c:/Users/Joe/radical_simplicity_ai_os_joe-m/.agent/dispatcher.md)
- [router.yaml](file:///c:/Users/Joe/radical_simplicity_ai_os_joe-m/.agent/router.yaml)
- [warden_log.md](file:///c:/Users/Joe/radical_simplicity_ai_os_joe-m/.agent/evals/warden_log.md)
- [incident_log.md](file:///c:/Users/Joe/radical_simplicity_ai_os_joe-m/.agent/evals/incident_log.md)
