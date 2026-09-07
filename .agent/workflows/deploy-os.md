---
description: Deploy the AI OS to a new client workspace. Creates a sibling directory with the full agent system.
---

# /deploy-os

Deploy the Radical Simplicity AI OS to a new client workspace.

## What It Does

Copies the core OS (agents, workflows, axioms, credentials, config) to a new directory beside this workspace. Optionally includes a specific `work_in_progress/` project. Registers the deployment for future update syncing.

## Usage

// turbo-all

### 1. Basic Deploy (empty workspace)

```powershell
.\deploy-os.ps1 -TargetName "clientname"
```

Creates: `...\radical_simplicity_ai_os_clientname\` with full OS and empty `work_in_progress/`.

### 2. Deploy with a WIP project

```powershell
.\deploy-os.ps1 -TargetName "dica" -IncludeWip "wfot" -Notes "Function First Coaching — DICA"
```

Creates: `...\radical_simplicity_ai_os_dica\` with the WFOT project included.

### 3. What Gets Copied

| Item | Included |
|------|----------|
| `.agent/` (rules, workflows, references) | ✅ |
| `.gemini/GEMINI.md` | ✅ |
| `.env` (real credentials) | ✅ |
| `content-system/` (axioms) | ✅ |
| `mission.md`, `README.md` | ✅ |
| `package.json`, `.gitignore` | ✅ |
| `.wrangler/` (excl. tokens file) | ✅ |
| `work_in_progress/{specified}` | ✅ (if `--IncludeWip`) |
| `file_clerk/`, `z_archive/`, `node_modules/` | ❌ |

### 4. After Deploy

The script will report the new workspace path. Then:
1. `cd` into the new workspace
2. Run `npm install`
3. Open in VS Code and start working
