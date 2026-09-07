> ⚠️ **DEPRECATED** — This document has been superseded by the comprehensive [3-Tier Scalability SOP](00_business_model/three_tier_scalability_sop.md). This file is kept for reference only.

# SOP: Client "OS Tier" Deployment

**Purpose:** To quickly and efficiently stamp out a customized AI Operating System instance for a new client who has purchased the "OS Tier" (Done-For-You/System Deployment Tier) of the 3-tiered business model.

---

## 1. Initial Deployment (The "Franchise Clone")

The very first step is to stamp out a clean copy of your core AI OS for the client. This ensures they have all the base workflows, personas, and system files without polluting your main instance.

1. Open a terminal in your core workspace (`radical_simplicity_ai_os_joe-m`).
2. Run the deployment script with the client's name:
   ```powershell
   .\deploy-os.ps1 -TargetName "ClientName"
   ```
   *(Optional)* If you already know their first project name, you can include it:
   ```powershell
   .\deploy-os.ps1 -TargetName "ClientName" -IncludeWip "ProjectName"
   ```
3. The script will automatically create a sibling directory called `radical_simplicity_ai_os_ClientName`.
4. Close your current VS Code window (or open a new one) and open the newly created client directory:
   - `File > Open Folder... > \radical_simplicity_ai_os_ClientName\`

## 2. Environment & Dependency Setup

Now that you are in the client's isolated OS environment, you need to install the dependencies and verify the environment.

1. In the VS Code terminal for the new client directory, install any necessary Node packages:
   ```powershell
   npm install
   ```
2. Open the `.env` file and review it. Update any API keys if the client provided their own, or ensure your agency keys are properly seated if you are managing the usage for them.

## 3. Client Context Injection (The "Brainwash")

The OS now needs to know *who* it works for. You must update its base context.

1. **Update `mission.md`:** Open `mission.md` and rewrite the primary directives, goals, and tone to match the client's specific business and brand.
2. **Update Axioms:** Navigate to `content-system/axioms/`.
   - Remove any of your personal/agency axioms that don't apply to the client.
   - Inject the client's specific business rules, brand voice guidelines, and operational procedures as new `.md` files in this folder.

## 4. Persona & Workflow Tuning

Depending on what the client purchased or needs, they might need different "employees" (personas) and workflows.

1. **Prune Unnecessary Personas:** Look in the `.agent/personas/` (or wherever personas are stored). If they are an e-commerce brand, you might not need B2B lead-gen personas. Delete what isn't needed to keep their system lean.
2. **Add Custom Workflows:** If they have a specific process (e.g., a custom n8n webhook pipeline), add that specific workflow markdown to their `.agent/workflows/` directory so Antigravity knows how to execute it.

## 5. Initiating the First Task

The OS is now fully customized for the client. It's time to put it to work.

1. Open a new chat with Antigravity inside the client's VS Code instance.
2. Prompt it to read the new `mission.md` and their `content-system/axioms/` to acknowledge its new identity.
3. Start their first project inside the `work_in_progress` folder and ask Antigravity to begin executing tasks.

## 6. Future Updates

When you make a massive improvement to your *Core OS* (like adding a new universal tool or a better system prompt), you don't need to do this manually for every client. 
- You simply use the `/push-os-updates` workflow from your main workspace to blast those core improvements down to all deployed client instances via the `deployments.yaml` tracker.

---
**Estimated Setup Time:** 5-10 minutes per client.
