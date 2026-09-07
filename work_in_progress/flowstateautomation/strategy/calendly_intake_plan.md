# Calendly Intake Automation Plan

## Goal Description
Build an automated intake system triggered when a prospect books a "Free Systems Audit" via Calendly. The system must send a premium, branded email to the prospect, notify the founder, and handle CRM routing.

## Proposed Changes

### N8N Workflow Construction
We will construct an `n8n` workflow that acts as the core intake engine.

**Trigger:**
*   **Calendly Trigger Node:** Listens for `invitee.created` events. This ensures it fires *only* when a meeting is actually booked.

**Logic & Actions:**
1.  **Founder Notification:**
    *   **Action:** Send an SMS (via Twilio/ClickSend if available, otherwise email) or a Slack/Discord message to Joe Moulton alerting him of the new booking, including the prospect's name, company, and answers to the Calendly questions.
2.  **Prospect Welcome Sequence:**
    *   **Action:** Send a beautifully formatted HTML email to the prospect.
    *   **Content:**
        *   Confirmation of the time/date.
        *   A "What to Expect" section to set the frame as a high-value consulting call.
        *   A link to the Pre-Audit Intake Questionnaire (to gather intel before the call).
        *   A professional headshot of Joe Moulton and FlowstateAI branding.
3.  **CRM Sync (Optional but Recommended):**
    *   **Action:** Add/Update the contact in the CRM (e.g., ActiveCampaign, HubSpot, or a Google Sheet fallback) and tag them as "Audit Booked".

## Verification Plan

### Manual Verification
1.  Create the n8n workflow JSON file.
2.  The user imports the JSON into their n8n instance.
3.  The user connects their Calendly API key and Email credentials to the nodes.
4.  The user books a test meeting on their own Calendly calendar.
5.  Verify the branded email arrives in the prospect's inbox.
6.  Verify the internal notification arrives.
