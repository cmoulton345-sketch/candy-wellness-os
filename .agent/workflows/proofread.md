---
description: Activate the Consistency persona to mechanically proofread a file for grammar, punctuation, capitalization, spelling, trademark compliance, and formatting errors. Never touches voice, strategy, or conversion architecture.
---

# /proofread — Mechanical Copy Editing Pass

## Usage
```
/proofread [target file]
```
If no file is specified, proofread the user's currently active document.

## Steps

1. **Activate Persona**
   ```
   ADOPT: Consistency
   ```
   Load `.agent/personas/consistency.md` and operate under its rules exclusively.

2. **Load Brand Standards**
   Read the FFC SKILL file (`.agent/skills/function-first-coaching-brand-standards-bloom-aota/SKILL.md`) and the style guide (`style_guide.md` in user memory) to populate the brand compliance checklist.

3. **Read Target File**
   Read the entire target file. If HTML, parse the visible text content and alt attributes. If Markdown, parse all text content.

4. **Execute Mechanical Scan**
   Scan the file against all six Consistency checklist categories:
   - [ ] Punctuation
   - [ ] Capitalization
   - [ ] Spelling & Typos
   - [ ] Trademark & Brand Compliance
   - [ ] Consistency & Parallel Structure
   - [ ] HTML-Specific (if applicable)

5. **Report Findings**
   Present all issues using the Consistency output format:
   ```
   [LINE/LOCATION] ISSUE → FIX
   "[original text]" → "[corrected text]"
   Reason: [one-line mechanical justification]
   ```
   Group by severity: 🔴 Errors first, then 🟡 Inconsistencies, then 🔵 Suggestions.

6. **Apply Fixes (on user approval)**
   After user reviews the list and approves (all or selectively), apply the approved fixes to the file. Never auto-apply without explicit approval.

## Rules
- **NEVER** alter voice, tone, hooks, strategy, or conversion architecture
- **NEVER** rewrite for "clarity" — fix mechanics only
- **NEVER** make subjective calls — if debatable, skip it
- If zero issues found, report "Clean copy. No mechanical issues detected."
