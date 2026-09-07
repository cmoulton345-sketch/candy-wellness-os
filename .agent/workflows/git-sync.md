---
description: Automatic git sync — pull, commit, push, and conflict resolution handled by the AI
---
// turbo-all

# Git Auto-Sync Workflow

> **Who runs this?** The AI. Never the user. This workflow is triggered automatically per the rules in GEMINI.md `## Git Auto-Sync`.

---

## 1. Session Start — Pull Latest

Run at the **beginning of every session** to get the partner's latest changes.

```
Step 1: Stash any uncommitted local changes
$ git stash

Step 2: Pull with rebase to keep history clean
$ git pull --rebase origin master

Step 3: Re-apply any stashed local work
$ git stash pop
```

- If `git stash pop` has conflicts → resolve per Section 3 below.
- If `git pull --rebase` has conflicts → resolve per Section 3, then `git rebase --continue`.
- **Report to user:** "Synced — pulled X new commits from [partner]. Here's what changed: [brief summary]."
- If nothing changed: "Already up to date."

---

## 2. Save Point — Commit + Push

Run when:
- User says **"save"**, **"push"**, **"sync"**, **"commit"**, or **"we're done"**
- At the **end of any meaningful block of work** (file edits, new files, config changes)
- Before **switching tasks** or ending a session

```
Step 1: Stage everything
$ git add -A

Step 2: Commit with a descriptive auto-generated message
$ git commit -m "<type>: <what changed>"

Step 3: Pull any partner changes that arrived during the session
$ git pull --rebase origin master

Step 4: Push to remote
$ git push origin master
```

### Commit Message Format

Use this pattern:
```
<type>: <concise description of what changed>
```

Types:
- `content` — copy, marketing materials, axioms, research
- `config` — workspace config, agent rules, workflows, GEMINI.md
- `build` — HTML, CSS, JS, deployment files
- `docs` — documentation, README, architecture
- `feat` — new features or capabilities
- `fix` — bug fixes or corrections

Examples:
- `content: update WFOT landing page hero copy and OG tags`
- `config: add git-sync workflow and update GEMINI.md`
- `build: implement feedback engine admin page`

If multiple types of changes exist, use the dominant one and mention others in the description.

---

## 3. Conflict Resolution Strategy

> **Context:** Two collaborators working on different things. True conflicts are extremely rare. Any conflict is almost certainly a git artifact, not a real disagreement.

### Decision Tree

```
Is it a .md / .txt / content file?
  → YES: Keep both versions. Concatenate both sides, remove exact duplicates.
  → NO: Continue ↓

Is it a config file (.yaml, .json, GEMINI.md, agent rules)?
  → YES: Accept INCOMING (remote/partner's) version for structure.
         Merge in any LOCAL additions that don't conflict.
  → NO: Continue ↓

Is it an .html / .css / .js file?
  → YES: Accept INCOMING for structural/layout changes.
         Keep LOCAL content/copy changes.
         If both changed the same content → prefer the MORE RECENT change.
  → NO: Continue ↓

Fallback:
  → Accept INCOMING (partner's version). It's more likely to be intentional
    since they committed more recently.
```

### After Any Auto-Resolution

**Always report to the user:**
```
⚠️ Auto-resolved a merge conflict:
- File: [filename]
- What happened: [brief explanation]
- Resolution: [what was kept]
- Action needed: None (or: please review [filename])
```

### When to Escalate (Almost Never)

Only escalate to the user if:
- Both collaborators edited the **exact same lines** of a **code file**
- The conflict involves **deletion vs. modification** (one person deleted what the other edited)
- You genuinely can't determine the right resolution

Escalation format:
```
🔴 Git conflict needs your input:
- File: [filename]  
- Your version: [summary]
- Partner's version: [summary]
- My recommendation: [what you'd do]
- Say "go with mine", "go with theirs", or "show me both"
```

---

## 4. Quick Reference for the AI

| Trigger | Action |
|---------|--------|
| Session starts | Run Section 1 (Pull) |
| After editing any file(s) | Run Section 2 (Commit + Push). Don't ask. |
| After a successful deploy | Run Section 2 (Commit + Push) immediately. |
| After creating new files (plans, research, configs) | Run Section 2 (Commit + Push) |
| After verifying something works | Run Section 2 (Commit + Push) with verification note |
| User says "save/push/sync/commit/done" | Run Section 2 (Commit + Push) |
| Before switching tasks or topics | Run Section 2 (Commit + Push) outstanding changes |
| Merge conflict | Run Section 3 (Auto-resolve + report) |
| User asks "what did [partner] change?" | `git log --oneline -10` + `git diff HEAD~N` |
| User asks "is everything saved?" | `git status` + report |

### The Only Time NOT to Commit

- Temporary scratch files you're about to delete
- Mid-edit state where the code is broken and you know you're about to fix it in the next step
- That's it. Everything else gets committed.
