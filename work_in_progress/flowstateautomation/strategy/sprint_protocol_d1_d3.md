# The FlowstateAI 5-Day Sprint: Client Delivery Protocol

This is the internal, step-by-step operating procedure for executing a 5-Day Sprint for a new client. The objective is to move from a signed contract to a fully functional, autonomous workflow with zero friction.

---

## Day 1: The "X-Ray" (Strategy & Specification)

**Objective:** Map the exact logic, boundaries, and expected outcomes of the workflow. The client signs off on a physical "Spec Sheet" by the end of the day. You do not touch n8n until the spec is approved.

### 1A. Pre-Call Checklist (Internal Prep)
- [ ] Review their Pre-Audit Intake Questionnaire.
- [ ] Review any SOPs, screenshots, or templates they provided.
- [ ] Draft a *hypothesis* workflow diagram (mental or rough sketch) to guide the conversation.
- [ ] Ensure the Zoom room is set to record automatically (you will need this for the build phase).

### 1B. The Strategy Session (60 Minutes with Client)
- **Phase 1: The Origin (15 mins):** What is the exact *trigger*? (e.g., "A new lead fills out a Facebook Lead Form.") Where does the data originate? What format is it in?
- **Phase 2: The Routing (20 mins):** What are the conditional logic paths? (e.g., "If they have a budget >$5k, send to HubSpot and flag high priority. If <$5k, send them the DIY guide via active campaign.")
- **Phase 3: The Destination & Edge Cases (15 mins):** Where must the data end up? What happens if an API fails? What happens if they input a fake phone number? (Define the error handling).
- **Phase 4: Missing Keys (10 mins):** Identify exactly what API credentials, logins, or access you need from them today.

### 1C. Post-Call Execution
- [ ] Process the Zoom recording transcript (via AI) to extract business logic.
- [ ] Draft the **Official Workflow Specification Document** (The Spec).
- [ ] **Deliverable to Client:** Send the Spec Document for approval via email: *"Reply YES to confirm this is the exact flow we are building. Once approved, the build begins and structural scope is locked."*
- [ ] Send credential request links (use a secure tool or ask them to generate API tokens referencing the `n8n_guide.md`).

---

## Day 2: Architecture & The "Plumbing" Phase

**Objective:** Connect the pipes. No complex logic is built today; the sole goal is to establish successful authentication and data movement between node A and node B in n8n.

### 2A. The Environment Setup
- [ ] Spin up the client's dedicated n8n canvas.
- [ ] Name the workflow according to convention: `[Client Name] - [Workflow Purpose] - V1`.
- [ ] Add "Sticky Notes" to the canvas outlining the 3-4 major phases of the approved Spec.

### 2B. The Credentials & Connections
- [ ] Securely input the API tokens/credentials received from the client into the n8n credential manager.
- [ ] Build the **Trigger Node** (e.g., Webhook URL, standard polling node, or specific app trigger).
- [ ] Test the Trigger node: Fire a test event from the source (e.g., submit a test Facebook Lead Form) and ensure n8n successfully catches the raw JSON payload.

### 2C. Destination Verification
- [ ] Build the final **Action Node(s)** (e.g., Create HubSpot Contact, Send Slack Message).
- [ ] Hardcode a dummy data payload and run the node manually to verify it successfully writes data to the client's destination platform.
- [ ] **Deliverable to Client:** End-of-Day 2 Update: *"Connections established. We have successfully authenticated with your [CRM] and [Trigger Source]. Building the routing logic tomorrow."*

---

## Day 3: The "Brain" (Logic & Routing Phase)

**Objective:** Connect the verified Trigger to the verified Destination using the transformative logic defined in the Day 1 Spec.

### 3A. Data Parsing & Transformation
- [ ] Add the necessary formatting nodes (e.g., changing date formats, splitting full names into First/Last).
- [ ] Ensure all incoming variables (email strings, phone numbers) are stripped of unwanted characters using standard regex or formatting nodes.

### 3B. The Routing & AI Layer (If Applicable)
- [ ] Build the **Switch/If Nodes** to handle the conditional paths defined in the Spec.
- [ ] If using AI (e.g., Gemini/OpenAI to draft a custom summary or email), insert the AI node.
- [ ] *Crucial Step:* Provide highly rigid System Prompts to the AI node to prevent hallucinations. Output should ideally be requested in strict JSON format.

### 3C. The "Happy Path" Dry Run
- [ ] Connect the Transform/Logic nodes to the Destination nodes.
- [ ] Execute a full end-to-end sandbox test using the "Happy Path" (perfect data input).
- [ ] Verify the output in the destination system matches the Spec perfectly.
- [ ] **Deliverable to Client:** End-of-Day 3 Update: *"Primary logic pathway is built and undergoing internal testing. Moving to edge-case handling and final QA tomorrow."*
