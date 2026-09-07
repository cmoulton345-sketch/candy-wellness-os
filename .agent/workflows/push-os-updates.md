---
description: Push OS-level agent updates to all deployed client workspaces. Reads deployments.yaml.
---

# /push-os-updates

Sync agent rules, workflows, axioms, and config from this source workspace to all deployed client workspaces.

## What It Does

Reads `deployments.yaml` and pushes OS-level changes to every registered deployment. Only syncs the agent system — never touches `.env`, `work_in_progress/`, or client-specific files.

## Usage

// turbo-all

### 1. Push to all deployments

```powershell
.\push-os-updates.ps1
```

### 2. Push to a specific deployment only

```powershell
.\push-os-updates.ps1 -TargetName "dica"
```

### 3. Dry run (see what WOULD be synced)

```powershell
.\push-os-updates.ps1 -DryRun
```

### 4. What Gets Synced

| Item | Synced |
|------|--------|
| `.agent/rules/` | ✅ |
| `.agent/workflows/` | ✅ |
| `.agent/references/` | ✅ |
| `.gemini/` | ✅ |
| `content-system/` | ✅ |
| `mission.md`, `README.md` | ✅ |
| `package.json`, `.gitignore` | ✅ |
| `.env` | ❌ (client-specific) |
| `work_in_progress/` | ❌ (client work) |
| `node_modules/`, `.git/` | ❌ |

## When to Use

After updating any agent persona, workflow, axiom, or OS-level config in this source workspace, run this to propagate changes to all client workspaces.
