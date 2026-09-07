---
trigger: always
description: Pipeline handoff contracts — required fields and format for every boundary crossing between Scout, Quill, Forge, and Harbor.
scope: all
tier: foundation
inherits: core_axioms.md
---

# Pipeline Handoff Contracts

> **PURPOSE:** Every time work crosses a pipeline boundary, the sending agent produces a handoff artifact containing the fields below. The receiving agent does not begin work until all required fields are present. If a field is missing, the receiver asks the sender — not Joe — to complete it.

---

## Scout -> Quill (Stage 1 -> Stage 2)

Scout delivers strategic intelligence; Quill converts it into persuasive language. The handoff artifact ensures Quill never writes copy without knowing the market, the audience, and the positioning — eliminating the "generic copy" failure mode.

### Required Fields

| # | Field | Description | Source |
|---|-------|-------------|--------|
| 1 | **Target Audience** | Demographics, psychographics, awareness level (Schwartz scale) | Scout research |
| 2 | **Competitive Landscape** | Top 3 alternatives the audience considers; their positioning | Five Forces / Dunford canvas |
| 3 | **Positioning Statement** | Category, unique attributes, value delivered, target customer | Dunford Lens output |
| 4 | **Key Pain Points** | Top 3 pains the audience experiences, in their language if VOC available | Prospect research |
| 5 | **Desired Action** | What the copy should make the reader do (book a call, download, buy) | Strategic goal |
| 6 | **Brand Voice Notes** | Tone, vocabulary constraints, existing brand examples | Scout intake |

---

## Quill -> Forge (Stage 2 -> Stage 3)

Quill delivers conversion-ready language; Forge uses it in proposals, call scripts, and negotiation. The handoff ensures Forge has the persuasive assets already built — eliminating the "winging the pitch" failure mode.

### Required Fields

| # | Field | Description | Source |
|---|-------|-------------|--------|
| 1 | **Offer Summary** | One-paragraph description of the offer and its unique mechanism | Quill output |
| 2 | **Key Headlines & Hooks** | Top 3 tested headlines/hooks for this offer | Hook Smith mode |
| 3 | **Objection Map** | Anticipated objections and the copy-level responses already written | Audit mode |
| 4 | **Social Proof Assets** | Case studies, testimonials, or data points ready for use | Quill research |
| 5 | **Recommended Tier** | Which FlowstateAI tier (Sprint/Retainer/Expansion) fits this prospect | Scout + Quill assessment |
| 6 | **Awareness Level** | Where the prospect sits on the Schwartz scale at time of handoff | Quill diagnosis |

---

## Forge -> Harbor (Stage 3 -> Stage 4)

Forge delivers a signed client; Harbor onboards them. The handoff ensures Harbor knows what was promised, what the client expects, and what technical access is needed — eliminating the "expectation mismatch" failure mode.

### Required Fields

| # | Field | Description | Source |
|---|-------|-------------|--------|
| 1 | **Client Profile** | Company name, industry, size, key contacts, decision-maker | Forge deal scope |
| 2 | **Signed Tier & Pricing** | Exact tier, monthly/one-time amount, payment terms | Proposal output |
| 3 | **Promised Deliverables** | Specific automations, workflows, or systems promised in the proposal | Proposal Architect |
| 4 | **Timeline Commitments** | Any dates or deadlines committed to during negotiation | Forge call notes |
| 5 | **Objections Surfaced** | What concerns the client raised and how they were resolved | Objection Disarmer log |
| 6 | **Technical Access Needed** | CRM API keys, webhook endpoints, Twilio credentials, etc. | Solution architecture |
| 7 | **Expansion Signals** | Upsell opportunities identified during the deal but deferred to post-onboarding | Forge assessment |

---

## Usage

Any pipeline agent may reference this file:
```
See .agent/rules/handoffs.md for the required handoff fields at this boundary.
```

When handing off, produce the artifact as a markdown block with all required fields populated. If a field cannot be populated, mark it `[PENDING — reason]` so the receiver knows what to follow up on.
