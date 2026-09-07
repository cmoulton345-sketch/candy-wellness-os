# Hybrid Autonomous Multi-Agent Architecture
### Flow State AI Automation — Internal Reference

> **Classification:** Internal Technical Reference  
> **Status:** Blueprint / Pre-Build  
> **Last Updated:** April 2026  
> **Author:** Joe / Flow State AI Automation

---

## Table of Contents

1. [Architecture Philosophy](#1-architecture-philosophy)
2. [System Overview](#2-system-overview)
3. [Deployment Model — Hybrid Stack](#3-deployment-model--hybrid-stack)
4. [Memory Architecture — Three Tiers](#4-memory-architecture--three-tiers)
5. [Agent Types and Roles](#5-agent-types-and-roles)
6. [Agent Spawning Protocol](#6-agent-spawning-protocol)
7. [Task, Rules & Outcome Model (TRO)](#7-task-rules--outcome-model-tro)
8. [Database Schemas](#8-database-schemas)
9. [Technology Stack](#9-technology-stack)
10. [n8n Integration Layer](#10-n8n-integration-layer)
11. [Visual Interface — Brain Metaphor](#11-visual-interface--brain-metaphor)
12. [Security & Compliance Considerations](#12-security--compliance-considerations)
13. [Scaling Path](#13-scaling-path)
14. [Build Phases](#14-build-phases)
15. [Known Risks & Mitigations](#15-known-risks--mitigations)
16. [Operational Cost Model](#16-operational-cost-model)

---

## 1. Architecture Philosophy

The system is built on three non-negotiable principles:

**1. The Right Layer for the Right Job**
No single storage or compute paradigm handles all agent needs. Filesystem = hot working memory. Vector DB = semantic recall. Relational DB = source of truth. Cloud = inference + scale. VPS self-hosted = orchestration + data control. Each layer does one job extremely well.

**2. Agents Are Ephemeral. Memory Is Not.**
Individual agent instances can be created, used, and destroyed. The memory system persists across sessions, agents, and time. The agent is a processor; the database is the brain.

**3. Spawn Lean, Share Selectively**
When a parent agent spawns a child, it does not hand over its full memory. It slices a minimal relevant subset. This prevents context explosion and keeps sub-agents focused. All agents write back to the shared database upon task completion.

---

## 1.5. Product Modes

This system serves two distinct purposes. They share infrastructure but have different build priorities, audiences, and success criteria. **Do not conflate them.**

### Mode A — Internal Engine (Build First)
**Audience:** FlowstateAI internal operations  
**Purpose:** Automate repetitive business workflows — lead research, content generation, client onboarding, competitive analysis  
**Interface:** CLI commands or n8n dashboard (no custom UI required)  
**Success Criteria:** A TRO completes accurately in < 5 minutes with zero human intervention  
**Build Priority:** This is the foundation. It must work flawlessly before anything client-facing is built.

### Mode B — Client Product (Build Second)
**Audience:** Clients, prospects, demo audiences  
**Purpose:** The Brain UI visualization layer, TRO input panel, and real-time agent monitoring — this is what you *sell or demo*  
**Interface:** The full Brain Metaphor UI (Section 11)  
**Success Criteria:** A prospect watches a live demo and says "I need this"  
**Build Priority:** Only after Mode A is stable. A beautiful UI on a broken engine is worse than no UI at all.

### Build Order Mandate
```
Mode A (Internal Engine) → Validate with 50+ real TROs → Mode B (Client UI)
```
Do not skip to Mode B. The engine earns the right to have a face.

---

## 2. System Overview

```
┌─────────────────────────────────────────────────────────┐
│                     USER INTERFACE                       │
│        Brain Visualization + Task Input Panel            │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              ORCHESTRATION LAYER (n8n VPS)               │
│   Task Router → Planner Agent → Builder Agent(s)         │
│   Spawns ephemeral Task Agents as needed                 │
└──────┬──────────────────┬──────────────────┬────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌────────────┐   ┌────────────────┐  ┌───────────────────┐
│  CLOUD LLM │   │  VECTOR DB     │  │   POSTGRES (VPS)  │
│  INFERENCE │   │  (Qdrant Cloud │  │   Source of Truth │
│  Anthropic │   │  or self-host) │  │   Task State      │
│  API       │   │  Semantic      │  │   Agent Memory    │
│            │   │  Memory        │  │   Conversation    │
└────────────┘   └────────────────┘  │   History         │
                                     └───────────────────┘
                                              │
                                     ┌────────────────────┐
                                     │   FILESYSTEM (VPS) │
                                     │   Hot Working Mem  │
                                     │   Scratchpads      │
                                     │   Plans / Artifacts│
                                     └────────────────────┘
```

---

## 3. Deployment Model — Hybrid Stack

### What Lives Where and Why

| Component | Location | Reason |
|---|---|---|
| n8n Orchestration | Self-hosted VPS (Hetzner/DO) | Full control, data stays off SaaS platforms |
| PostgreSQL | VPS (same or dedicated) | Source of truth, ACID compliance, persists agent state |
| Qdrant | VPS self-hosted OR Qdrant Cloud | Vector memory for semantic retrieval |
| Filesystem scratchpad | VPS local disk | Hot working memory, plan files, temp artifacts |
| LLM Inference (Claude) | Anthropic API (cloud) | Best-in-class reasoning, no GPU overhead |
| LLM Inference (local) | Ollama on VPS | Optional fallback, air-gapped client option |
| Object Storage | Cloudflare R2 or S3 | Long-term artifact archival, low cost |

### VPS Recommendation
- **Provider:** Hetzner Cloud (EU/Canada latency acceptable, best $/GB RAM)
- **Minimum Spec:** 4 vCPU / 16GB RAM / 160GB NVMe
- **Better Spec:** 8 vCPU / 32GB RAM for multi-agent concurrent workloads
- **Estimated Cost:** $30–60 CAD/month for a capable box

### When to Add True On-Prem
Only when a client contract specifically requires:
- PIPEDA data residency guarantees
- Healthcare/PHIPA compliance
- Legal firm air-gap requirements
- At that point, quote hardware provisioning into the project price.

---

## 4. Memory Architecture — Three Tiers

### Tier 1 — Working Memory (Filesystem)
**Purpose:** Hot context for the currently active agent  
**Location:** `/agent-workspace/{agent_id}/`  
**Contents:**
- `plan.md` — current task decomposition and step tracking
- `scratchpad.md` — intermediate reasoning, notes
- `tool_outputs/` — raw outputs from tool calls
- `context_slice.json` — the memory slice passed from parent agent

**Lifecycle:** Created at agent spawn. Archived to object storage at completion. Deleted from active disk after 24 hours.

**Why filesystem here:** The agent writes its plan to `plan.md` and references it constantly. This keeps the plan in the "recent" section of the context window where the LLM pays highest attention. It's cognitive architecture, not just storage.

### Tier 2 — Semantic Memory (Vector DB / Qdrant)
**Purpose:** "Find things related to this" — fuzzy, associative recall  
**Collections:**
- `agent_knowledge` — accumulated domain knowledge from past task completions
- `client_context` — client-specific information, preferences, history
- `tool_registry` — embeddings of available tools and their descriptions
- `task_outcomes` — embeddings of past task summaries for similar-task retrieval

**How agents use it:**
1. At task start → query for similar past tasks → inject into context
2. Mid-task → query for relevant domain knowledge
3. At task end → upsert new learnings back to collection

**Embedding Model:** `nomic-embed-text` (Ollama, local) or `text-embedding-3-small` (OpenAI API)

### Tier 3 — Relational Memory (PostgreSQL)
**Purpose:** Source of truth. Structured state. ACID guarantees.  
**Why this matters for multi-agent:** Concurrent filesystem writes corrupt. Concurrent DB writes with proper transactions do not.

See full schema in Section 8.

---

## 5. Agent Types and Roles

### Planner Agent (Persistent)
- Receives the TRO (Task, Rules, Outcome) object from the user
- Decomposes the task into a directed acyclic graph (DAG) of subtasks
- Determines which subtasks can run in parallel vs. sequential
- Maintains the master plan in `plan.md`
- Monitors child agent completions and re-plans if needed
- **Does NOT execute tasks directly**

### Builder / Execution Agent (Semi-Persistent)
- Receives a specific subtask from the Planner
- Has access to tools relevant to its subtask domain
- Can spawn Task Agents for atomic sub-routines
- Writes results back to PostgreSQL on completion
- Passes memory slice to any children it spawns

### Task Agent (Ephemeral)
- Spawned for a single, well-defined atomic operation
- Has the tightest possible context (memory slice only)
- No access to full system memory
- Terminates after writing its single output
- Lifecycle: seconds to minutes

### Arbiter Agent (On-demand)
- Invoked when conflicting memories or task results need reconciliation
- Analyzes contradictions and produces temporal reflection summaries
- Example: "Client preferred React until Q1 2026, has since moved to Vue"
- Prevents goal drift in long-running agents

**Implementation Notes (Versioned Vector Entries):**
- All Qdrant upserts MUST include a `created_at` timestamp and `source_agent_id` in the payload metadata
- Arbiter queries filter by date range to compare old knowledge vs. new knowledge on the same topic
- Conflict detection: When a new upsert has > 0.85 cosine similarity to an existing entry but contradictory content, flag for Arbiter review
- This is the most complex workflow in the system — budget 2x the estimated development time
- Requires custom SQL + vector hybrid queries (n8n Code nodes, not built-in memory nodes)

### Memory Manager Agent (Background)
- Runs on a scheduled trigger (heartbeat)
- Compresses old episodic memories into semantic summaries
- Prunes irrelevant vector embeddings
- Maintains database hygiene
- Think of this as the system's "sleep cycle"

---

## 6. Agent Spawning Protocol

### Spawn Decision Logic
The Planner or Builder agent evaluates three conditions before spawning:

1. **Complexity threshold** — Is this subtask too large for current context?
2. **Domain mismatch** — Does this subtask require different tools/expertise?
3. **Parallelization opportunity** — Can multiple subtasks run simultaneously?

### Memory Slicing Algorithm
When a parent spawns a child, it does NOT pass its full memory. It computes a slice:

```json
{
  "child_task": "Extract contact information from uploaded CSV",
  "memory_slice": {
    "episodic": [
      // Only recent conversation turns relevant to THIS subtask
    ],
    "semantic": [
      // Top-K vector search results relevant to subtask keywords
    ],
    "working": {
      // Subset of current plan context relevant to this child
      "parent_task_id": "uuid",
      "expected_output_schema": {},
      "rules": [],
      "deadline": "ISO timestamp"
    }
  }
}
```

### Spawn Registry (PostgreSQL)
Every spawn is logged. The visual layer queries this table to render sub-brain connections.

```sql
INSERT INTO agent_spawns (
  parent_agent_id,
  child_agent_id,
  spawned_at,
  subtask_description,
  memory_slice_hash,
  status
)
```

### Completion Handshake
Child writes output to `agent_task_results`. Parent polls or is notified via n8n webhook. Parent ingests child output, updates master plan, decides next step.

---

## 7. Task, Rules & Outcome Model (TRO)

The TRO is the atomic unit of work sent to the agent system. It is the user's intent contract.

### TRO Schema

```json
{
  "tro_id": "uuid",
  "created_at": "ISO timestamp",
  "task": {
    "description": "Research the top 5 medical aesthetics clinics in Moncton NB and compile a lead profile for each",
    "context": "Building outreach list for Flow State AI pitch campaign",
    "inputs": {
      "geography": "Moncton, NB",
      "industry": "Medical Aesthetics"
    }
  },
  "rules": [
    "Only use publicly available information",
    "Do not contact any business directly",
    "Flag any clinic already in our CRM",
    "Output must be structured JSON matching LeadProfile schema"
  ],
  "outcome": {
    "description": "A validated, structured list of 5 lead profiles ready for CRM import",
    "format": "JSON array matching LeadProfile schema",
    "quality_threshold": "Each profile must have: name, address, phone, website, estimated staff size, current tech stack if identifiable",
    "deadline": null
  },
  "constraints": {
    "max_agents": 5,
    "max_execution_minutes": 30,
    "escalate_to_human_on": ["ambiguous rules", "conflicting data", "missing required fields"]
  }
}
```

### TRO Lifecycle States
`RECEIVED → PLANNING → IN_PROGRESS → PENDING_REVIEW → COMPLETE | FAILED | ESCALATED`

---

## 8. Database Schemas

### Core Tables (PostgreSQL)

```sql
-- Master task tracking
CREATE TABLE tro_tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  status VARCHAR(50) DEFAULT 'RECEIVED',
  task_description TEXT NOT NULL,
  rules JSONB,
  outcome_spec JSONB,
  constraints JSONB,
  result JSONB,
  error TEXT,
  human_escalation_reason TEXT
);

-- Agent instance registry
CREATE TABLE agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tro_id UUID REFERENCES tro_tasks(id),
  agent_type VARCHAR(50), -- PLANNER | BUILDER | TASK | ARBITER | MEMORY_MANAGER
  status VARCHAR(50) DEFAULT 'SPAWNED',
  spawned_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  subtask_description TEXT,
  memory_slice JSONB,
  result JSONB,
  token_usage INTEGER,
  retry_count INTEGER DEFAULT 0,
  max_retries INTEGER DEFAULT 3,
  last_retry_at TIMESTAMPTZ,
  error TEXT
);

-- Agent spawn graph (for visual layer)
CREATE TABLE agent_spawns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  parent_agent_id UUID REFERENCES agents(id),
  child_agent_id UUID REFERENCES agents(id),
  spawned_at TIMESTAMPTZ DEFAULT NOW(),
  subtask_description TEXT,
  status VARCHAR(50) DEFAULT 'ACTIVE'
);

-- Long-term episodic memory
CREATE TABLE agent_memory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID REFERENCES agents(id),
  tro_id UUID REFERENCES tro_tasks(id),
  memory_type VARCHAR(50), -- EPISODIC | SEMANTIC | PROCEDURAL
  content TEXT NOT NULL,
  embedding_id VARCHAR(255), -- Reference to Qdrant point ID
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ,
  importance_score FLOAT DEFAULT 0.5
);

-- Conversation history (n8n chat memory)
CREATE TABLE conversation_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id VARCHAR(255) NOT NULL,
  agent_id UUID REFERENCES agents(id),
  role VARCHAR(20), -- user | assistant | system
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  token_count INTEGER
);

-- Tool call audit log
CREATE TABLE tool_calls (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID REFERENCES agents(id),
  tool_name VARCHAR(100) NOT NULL,
  input JSONB,
  output JSONB,
  latency_ms INTEGER,
  success BOOLEAN,
  error TEXT,
  called_at TIMESTAMPTZ DEFAULT NOW()
);

-- Learned knowledge (outputs of completed tasks)
CREATE TABLE knowledge_base (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_tro_id UUID REFERENCES tro_tasks(id),
  category VARCHAR(100),
  content TEXT NOT NULL,
  embedding_id VARCHAR(255),
  confidence_score FLOAT DEFAULT 1.0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_accessed_at TIMESTAMPTZ,
  access_count INTEGER DEFAULT 0
);

-- Temporal conflict resolutions (Arbiter outputs)
CREATE TABLE memory_reconciliations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  arbiter_agent_id UUID REFERENCES agents(id),
  conflict_description TEXT,
  old_memory_ids UUID[],
  resolution_summary TEXT,
  resolved_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 9. Technology Stack

### Core Infrastructure

| Layer | Technology | Version | Notes |
|---|---|---|---|
| Orchestration | n8n | Latest self-hosted | Docker Compose on VPS |
| Primary DB | PostgreSQL | 16+ | Via Docker on VPS |
| Vector DB | Qdrant | Latest | Self-hosted Docker OR Qdrant Cloud |
| LLM (primary) | Anthropic Claude | claude-sonnet-4-6 | API |
| LLM (local fallback) | Ollama + Llama 3.1 | 8B or 70B | On VPS for air-gapped clients |
| Embeddings | nomic-embed-text | via Ollama | Local embedding generation |
| Object Storage | Cloudflare R2 | - | Artifact archival, cheap egress |
| Reverse Proxy | Caddy or Nginx | Latest | TLS termination, routing |
| Container Runtime | Docker + Compose | Latest | All services containerized |

### Frontend / Visual Layer

| Layer | Technology | Notes |
|---|---|---|
| Brain UI | HTML/CSS/JS (Vanilla or React) | See Section 11 |
| Real-time Updates | WebSockets or SSE | Agent state polling |
| API Bridge | n8n Webhook + REST | Connects UI to orchestration |

### Optional Enhancements

| Purpose | Technology |
|---|---|
| Workflow observability | Prometheus + Grafana |
| Agent tracing | Langfuse (self-hosted) |
| Secrets management | Infisical or Doppler |
| CI/CD | GitHub Actions |

---

## 10. n8n Integration Layer

### Core Workflows to Build

**1. TRO Intake Workflow**
- Trigger: Webhook POST with TRO JSON
- Steps: Validate schema → Insert to `tro_tasks` → Trigger Planner Agent → Return task ID to UI

**2. Planner Agent Workflow**
- Trigger: New row in `tro_tasks` with status `RECEIVED`
- Steps: Pull TRO → Call Claude (system prompt: Planner role) → Parse DAG output → Insert subtasks to `agents` table → Trigger Builder(s)

**3. Builder Agent Workflow**
- Trigger: New row in `agents` with type `BUILDER`
- Steps: Load memory slice → Execute subtask (with tools) → Evaluate if spawn needed → Write result → Notify parent

**4. Task Agent Workflow**
- Trigger: Spawn event from Builder
- Steps: Receive minimal memory slice → Execute single atomic operation → Write to `agent_task_results` → Terminate

**5. Memory Heartbeat Workflow**
- Trigger: Scheduled (every 6 hours)
- Steps: Find stale episodic memories → Compress to summaries → Upsert to vector DB → Update importance scores

**6. Visual State Broadcaster**
- Trigger: Any status change in `agents` or `tro_tasks`
- Steps: Query spawn graph → Format as visual state JSON → Push to WebSocket endpoint → UI updates brain render

**7. Failure Recovery Workflow (Dead-Letter Queue)**
- Trigger: Any agent status changes to `FAILED`
- Steps:
  1. Log full error context (agent_id, TRO, memory_slice, error message) to `tool_calls` audit table
  2. Check `retry_count` against `max_retries` (default: 3)
  3. If retries remaining → increment `retry_count`, wait with exponential backoff (5s, 30s, 120s), re-trigger the agent workflow
  4. If max retries exhausted → escalate to human via notification (Telegram/email)
  5. Update TRO status to `ESCALATED` with `human_escalation_reason: "Agent failed after 3 retries"`
- **Backoff formula:** `delay_seconds = 5 * (4 ^ retry_count)` — 5s, 20s, 80s
- **Critical:** Never retry agents that failed due to PII detection or privilege violations — escalate immediately

### n8n Memory Nodes to Use
- **Postgres Chat Memory** — session-aware conversation history
- **Qdrant Vector Store** — semantic search within agent workflows
- **Window Buffer Memory** — short-term context within a single workflow execution

### Agent System Prompt Template (n8n Code Node)

```javascript
const systemPrompt = `
You are a ${agentType} agent in a multi-agent autonomous system.

YOUR ROLE: ${roleDescription}

YOUR TASK: ${taskDescription}

RULES YOU MUST FOLLOW:
${rules.map((r, i) => `${i+1}. ${r}`).join('\n')}

YOUR MEMORY CONTEXT:
${JSON.stringify(memorySlice, null, 2)}

TOOLS AVAILABLE TO YOU:
${tools.map(t => `- ${t.name}: ${t.description}`).join('\n')}

SPAWNING PROTOCOL:
- You MAY spawn a child agent if the subtask requires different domain expertise
- You MAY spawn child agents for parallelizable work
- When spawning, provide ONLY the relevant memory slice — do NOT pass your full context
- Always specify: child task description, expected output schema, deadline

OUTPUT FORMAT:
Always respond in valid JSON matching this schema:
{
  "reasoning": "your step by step thought process",
  "active_brain_regions": ["PLANNING", "MEMORY", "TOOL_USE"], // for visual layer
  "actions": [],
  "spawn_requests": [],
  "result": {},
  "status": "IN_PROGRESS | COMPLETE | BLOCKED | ESCALATE",
  "escalation_reason": null
}
`;
```

---

## 11. Visual Interface — Brain Metaphor

### Brain Region to Function Mapping

| Brain Region | Agent Function | Color When Active |
|---|---|---|
| Prefrontal Cortex | Planning, task decomposition, goal setting | `#00D4FF` cyan |
| Hippocampus | Memory retrieval, context loading | `#FFD700` gold |
| Temporal Lobe | Language processing, prompt construction | `#7C3AED` violet |
| Parietal Lobe | Tool use, action execution | `#F97316` orange |
| Occipital / Output | Result generation, writing output | `#10B981` emerald |
| Amygdala / Risk | Conflict detection, escalation trigger | `#EF4444` red |
| Cerebellum | Background processes, memory heartbeat | `#6B7280` grey pulse |
| Corpus Callosum | Inter-agent communication, spawn connections | `#F59E0B` amber |

### Visual Behavior Spec

**Idle State:** Brain outline in dark teal. Slow background pulse on all regions. Dim bioluminescent glow.

**Active Thinking:** Regions flash in sequence matching the agent's `active_brain_regions` array in its JSON output. Each flash is 200-400ms with a fade tail. Multiple regions can be active simultaneously.

**Sub-Brain Spawn:** A smaller brain SVG animates in from the edge of the canvas. A glowing line (Corpus Callosum color) connects parent brain to child brain. Child brain has its own region activation. On completion, child brain dims, connection line pulses gold once, then fades.

**Completion:** All active regions pulse white simultaneously, then fade to idle.

**Escalation/Error:** Amygdala region pulses red rapidly. Border of brain flashes red.

### UI Component Architecture

```
BrainInterface
├── TaskInputPanel
│   ├── TaskField (textarea)
│   ├── RulesBuilder (dynamic list)
│   ├── OutcomeField (textarea)
│   └── LaunchButton
├── BrainCanvas (main)
│   ├── SVG BrainOutline
│   ├── RegionLayer (interactive SVG regions)
│   ├── ActivityLayer (glow/pulse overlays)
│   └── ConnectionLayer (inter-agent lines)
├── SubBrainContainer
│   └── SubBrain[] (dynamically rendered)
├── ThoughtStream (sidebar)
│   └── ReasoningFeed (live text from agent.reasoning)
└── StatusBar
    ├── AgentCount
    ├── TaskStatus
    └── TokenUsage
```

### Real-Time State Protocol

The UI polls (or subscribes via WebSocket) to the n8n Visual State Broadcaster.

**State object pushed to UI:**
```json
{
  "tro_id": "uuid",
  "status": "IN_PROGRESS",
  "agents": [
    {
      "id": "uuid",
      "type": "PLANNER",
      "status": "ACTIVE",
      "active_regions": ["PREFRONTAL", "HIPPOCAMPUS"],
      "latest_reasoning": "Decomposing task into 3 parallel subtasks...",
      "children": ["uuid2", "uuid3"]
    },
    {
      "id": "uuid2",
      "type": "TASK",
      "status": "ACTIVE",
      "parent_id": "uuid",
      "active_regions": ["PARIETAL", "TEMPORAL"],
      "latest_reasoning": "Calling web search tool for clinic data..."
    }
  ],
  "spawn_connections": [
    { "from": "uuid", "to": "uuid2" },
    { "from": "uuid", "to": "uuid3" }
  ]
}
```

---

## 12. Security & Compliance Considerations

### Data Residency (Atlantic Canada SMBs)
- All client data processed and stored on Canadian-region VPS (Hetzner Ashburn or equivalent)
- LLM API calls to Anthropic transmit prompts — review client data sensitivity before including raw PII in prompts
- For PIPEDA-sensitive clients: redact PII before API call, re-inject into output post-processing

### API Key Management
- Never hardcode API keys in n8n workflows
- Use n8n's encrypted credential store for all keys
- Rotate Anthropic API keys quarterly minimum
- Use Infisical or Doppler for centralized secret management across services

### Agent Privilege Boundaries
- Each agent type has a defined tool permission set
- Task Agents: read-only tools only (web search, DB read)
- Builder Agents: read/write to scoped DB tables
- Planner Agent: orchestration privileges only, no direct tool execution
- No agent has direct shell access

### Audit Trail
- Every tool call logged to `tool_calls` table
- Every spawn logged to `agent_spawns` table
- Every TRO state transition logged with timestamp
- Retention: 90 days hot, archive to R2 indefinitely

### Human-in-the-Loop Triggers (Non-Negotiable)
Always escalate to human when:
1. Agent encounters ambiguous rules it cannot resolve
2. Agent confidence on a decision is below threshold
3. Task involves financial transactions or legal communications
4. Agent has been running > 2x the estimated time
5. Any agent detects PII it wasn't expecting

### Data Processing Agreements (DPA)
- **Anthropic:** A signed DPA must be on file before ANY client data flows through Claude API calls. Anthropic provides a standard DPA — execute it during onboarding.
- **Qdrant Cloud:** If using hosted Qdrant (not self-hosted), a DPA is required since client embeddings are stored on their infrastructure.
- **Tracking:** Maintain a `dpa_status` field per client in the CRM: `NOT_REQUIRED | PENDING | SIGNED`
- **Review cadence:** Quarterly audit of which clients have active DPAs and whether data flows match agreements.

### Air-Gap Clarification
The term "air-gapped" is used in this document to describe the **Ollama local fallback** option. To prevent contractual ambiguity with clients, use these precise definitions:

| Term | What It Actually Means | Use In Contracts |
|---|---|---|
| **LLM-Isolated** | LLM inference runs locally via Ollama on the VPS. No prompts or completions leave the server. However, the VPS itself has internet access for n8n webhooks, API integrations, and system updates. | ✅ Safe to promise |
| **Network-Isolated** | The VPS has no outbound internet access. All services run on a private network. Requires on-prem or dedicated VLAN. | ⚠️ Only promise with dedicated hardware |
| **True Air-Gap** | The system has zero internet connectivity. Physical hardware on client premises. No cloud services of any kind. | ❌ Do not promise unless quoting on-prem hardware |

> **Rule:** Never use the term "air-gapped" in client-facing materials. Use "LLM-Isolated" for the Ollama option. It's honest, it's accurate, and it won't create legal exposure.

---

## 13. Scaling Path

### Phase 1 — Single VPS (Current Build Target)
- 1 VPS: n8n + PostgreSQL + Qdrant + Ollama
- 1-3 concurrent TRO tasks
- Manual human review of all completed TROs
- Estimated capacity: 20-50 tasks/day

### Phase 2 — Separated Services
- Dedicated PostgreSQL instance (managed or separate VPS)
- Qdrant Cloud for vector DB (removes vector load from VPS)
- n8n scaled with queue mode + workers
- Estimated capacity: 200-500 tasks/day

### Phase 3 — Multi-Region / Client Isolation
- Per-client PostgreSQL schemas or databases
- Dedicated n8n environments per high-value client
- Qdrant namespaced collections per client
- Private cloud option for regulated industries

---

## 14. Build Phases

### Phase 1 — Foundation (Weeks 1-3)
- [ ] VPS provisioned (Hetzner recommended)
- [ ] Docker Compose stack: n8n + PostgreSQL + Qdrant
- [ ] Base database schema deployed
- [ ] n8n connected to Anthropic API
- [ ] Basic TRO intake webhook working
- [ ] Single Planner Agent workflow functional
- [ ] Manual test: Submit TRO → Planner decomposes → Output to DB

### Phase 2 — Multi-Agent Core (Weeks 4-6)
- [ ] Builder Agent workflow built
- [ ] Task Agent workflow built
- [ ] Spawn protocol functional (parent creates child DB record → triggers child workflow)
- [ ] Memory slicing implemented in Code nodes
- [ ] PostgreSQL Chat Memory connected
- [ ] Qdrant vector upsert/query working in n8n

### Phase 3 — Visual Layer (Weeks 7-9)
- [ ] Brain UI HTML/CSS/JS built (see Section 11)
- [ ] n8n Visual State Broadcaster workflow built
- [ ] Real-time WebSocket or polling connected to UI
- [ ] Sub-brain spawn animation functional
- [ ] TRO input panel connected to intake webhook

### Phase 4 — Hardening (Weeks 10-12)
- [ ] Arbiter Agent implemented
- [ ] Memory Heartbeat workflow running
- [ ] Human escalation flow built
- [ ] Audit logging verified end-to-end
- [ ] Basic observability (n8n execution logs + DB query dashboard)

### Phase 4.5 — Failure Recovery & Retry Logic (Week 11)
- [ ] Dead-letter queue workflow built (Section 10, Workflow 7)
- [ ] Exponential backoff retry tested end-to-end
- [ ] PII/privilege failure bypass verified (immediate escalation, no retry)
- [ ] Failure notification channel configured (Telegram or email)

---

## 14.5. Pilot Use Case

Before building the full system, validate the entire architecture with ONE end-to-end use case.

### The Pilot: Lead Research TRO

**Input TRO:**
```json
{
  "task": {
    "description": "Research the top 5 medical aesthetics clinics in Moncton NB and compile a lead profile for each",
    "context": "Building outreach list for Flow State AI pitch campaign"
  },
  "rules": [
    "Only use publicly available information",
    "Do not contact any business directly",
    "Output must be structured JSON matching LeadProfile schema"
  ],
  "outcome": {
    "format": "JSON array",
    "quality_threshold": "Each profile must have: name, address, phone, website, estimated staff size"
  },
  "constraints": {
    "max_agents": 5,
    "max_execution_minutes": 10
  }
}
```

**Expected Agent Behavior:**
1. Planner decomposes into 5 parallel Task Agents (one per clinic)
2. Each Task Agent searches the web, extracts structured data
3. Results written back to Postgres, Planner assembles final output
4. Total execution: < 5 minutes

**Success Criteria:**
- [ ] All 5 profiles returned with required fields populated
- [ ] Accuracy > 80% when manually verified against Google Maps
- [ ] Zero hallucinated businesses (every clinic must actually exist)
- [ ] Total token cost < $0.50 per TRO execution
- [ ] No human intervention required

**Why This Pilot:** It exercises every layer — spawning, memory slicing, tool use, parallel execution, result assembly, and quality validation — without touching sensitive client data.

---

## 14.6. Demo Playbook

When demonstrating the system to a prospect or partner, use this rehearsed script.

### Pre-Demo Setup
- [ ] Brain UI loaded and showing idle state (dark teal, slow pulse)
- [ ] TRO input panel visible and empty
- [ ] ThoughtStream sidebar visible (will show live reasoning)

### The Demo Script (Target: 90 seconds)

| Time | Action | What Audience Sees |
|---|---|---|
| 0:00 | Paste the Lead Research TRO into the input panel | The task description appears in clean UI |
| 0:05 | Click "Launch" | Prefrontal Cortex lights up cyan — Planner is thinking |
| 0:10 | Planner decomposes | ThoughtStream shows: "Decomposing into 5 parallel research tasks..." |
| 0:15 | Sub-brains spawn | 5 smaller brain SVGs animate in from edges, connected by amber lines |
| 0:15–0:60 | Task Agents execute | Parietal Lobe (orange) flashes on each sub-brain as tools are called. ThoughtStream shows live search queries. |
| 0:60 | Results return | Sub-brains dim one by one. Connection lines pulse gold. |
| 0:75 | Planner assembles | Main brain Occipital region (emerald) glows — writing output |
| 0:90 | Complete | All regions pulse white simultaneously. Result JSON appears in output panel. |

### The Closer
> "What you just watched was 5 AI agents working in parallel — researching, extracting, and assembling structured data — in 90 seconds. No templates. No manual entry. Just a plain-English request and a verified result. That's what we build for our clients."

### Demo Failure Protocol
If the demo fails mid-execution:
- Amygdala region will pulse red (this is built into the UI spec)
- Say: "This is actually a great example of our safety system. The AI detected an issue and escalated instead of guessing. In production, this triggers a human review. Let me show you what a completed run looks like..." → Switch to a pre-recorded successful run.

---

## 15. Known Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Agent spawns too many children (runaway) | Medium | High | Hard cap via `constraints.max_agents` in TRO |
| Memory conflicts between concurrent agents | Medium | Medium | All shared writes go through Postgres transactions |
| LLM output not valid JSON | High | Medium | n8n Code node with JSON repair + retry |
| Context window overflow | Medium | High | Memory slicing + strict token budgeting per agent |
| API rate limits hit during burst | Low | Medium | n8n retry with exponential backoff |
| VPS disk full (scratchpads accumulate) | Low | High | 24hr cleanup cron on `/agent-workspace/` |
| Sensitive client data in LLM prompt | Low | Very High | PII detection node before every API call |
| Agent loops indefinitely | Low | Medium | Max iteration counter per agent, auto-terminate |
| Failed agent with no retry path | Medium | Medium | Dead-letter queue + exponential backoff retry workflow (Section 10.7) |
| Redis failure kills n8n queue | Low | Very High | Docker healthcheck + auto-restart policy on Redis container |
| DPA not signed before client data flows | Low | Very High | Mandatory DPA checklist in client onboarding (Section 12) |
| "Air-gapped" overpromise to client | Low | High | Precise terminology matrix (LLM-Isolated vs True Air-Gap, Section 12) |

---

## 16. Operational Cost Model

Know your margins before you scale. This section tracks the real cost of running the agent system.

### Fixed Costs (Monthly)

| Item | Provider | Cost (CAD/mo) | Notes |
|---|---|---|---|
| VPS (Primary) | Hetzner Cloud | $30–60 | 4-8 vCPU, 16-32GB RAM |
| Domain + DNS | Cloudflare | $0 | Free tier |
| Object Storage (R2) | Cloudflare | $0–5 | Free tier covers first 10GB |
| Qdrant Cloud (optional) | Qdrant | $0–25 | Free tier covers 1M vectors |
| **Fixed Total** | | **$30–90** | |

### Variable Costs (Per TRO Execution)

| Component | Cost Estimate | Calculation |
|---|---|---|
| Planner Agent (Claude) | ~$0.05–0.10 | ~2K input + 1K output tokens |
| Builder Agent (Claude) | ~$0.10–0.20 | ~4K input + 2K output tokens |
| Task Agent (Claude) × N | ~$0.03–0.05 each | ~1K input + 500 output tokens |
| Embeddings (local Ollama) | $0.00 | Runs on VPS, no API cost |
| **Typical TRO (5 agents)** | **$0.25–0.50** | |

### Scaling Projections

| Daily TRO Volume | Monthly API Cost | Monthly Total (Fixed + Variable) |
|---|---|---|
| 10 TROs/day | ~$75–150 | ~$105–240 |
| 50 TROs/day | ~$375–750 | ~$405–840 |
| 200 TROs/day | ~$1,500–3,000 | ~$1,530–3,090 |
| 500 TROs/day | ~$3,750–7,500 | ~$3,780–7,590 |

### Token Budget Per Agent Type

To prevent runaway costs, enforce these hard limits in the system prompt or n8n Code node:

| Agent Type | Max Input Tokens | Max Output Tokens | Max Cost/Execution |
|---|---|---|---|
| Planner | 8,000 | 4,000 | $0.15 |
| Builder | 12,000 | 6,000 | $0.30 |
| Task | 4,000 | 2,000 | $0.08 |
| Arbiter | 16,000 | 4,000 | $0.25 |

### Break-Even Analysis
If FlowstateAI charges a client $500/month for automation services powered by this system:
- At 10 TROs/day → cost ~$150/month → **margin: 70%**
- At 50 TROs/day → cost ~$600/month → **margin: negative** (need to increase pricing or optimize token usage)
- **Sweet spot:** 15-30 TROs/day per client at $500-1,000/month retainer

> **Rule:** Track actual token spend per client per month. If a client's agent costs exceed 40% of their retainer, flag for pricing review.

---

## Appendix A — Quick Reference Commands

```bash
# Start the full stack
docker compose up -d

# Check n8n logs
docker compose logs -f n8n

# Connect to PostgreSQL
docker compose exec postgres psql -U agent_user -d agent_db

# Query active agents
SELECT id, agent_type, status, spawned_at FROM agents 
WHERE status = 'ACTIVE' ORDER BY spawned_at DESC;

# Check spawn graph for a TRO
SELECT p.id as parent, c.id as child, s.subtask_description, s.status
FROM agent_spawns s
JOIN agents p ON s.parent_agent_id = p.id
JOIN agents c ON s.child_agent_id = c.id
WHERE p.tro_id = '<your-tro-id>';

# View recent memory reconciliations
SELECT * FROM memory_reconciliations ORDER BY resolved_at DESC LIMIT 10;
```

## Appendix B — Docker Compose Skeleton

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - EXECUTIONS_MODE=queue
    volumes:
      - n8n_data:/home/node/.n8n
      - ./agent-workspace:/agent-workspace
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16
    restart: always
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=agent_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  qdrant:
    image: qdrant/qdrant:latest
    restart: always
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  redis:
    image: redis:7-alpine
    restart: always
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    volumes:
      - redis_data:/data

  ollama:
    image: ollama/ollama:latest
    restart: always
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

  caddy:
    image: caddy:2-alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - n8n

volumes:
  n8n_data:
  postgres_data:
  qdrant_data:
  redis_data:
  ollama_data:
  caddy_data:
  caddy_config:
```

---

*This document is a living blueprint. Update as the build evolves. Commit changes with date and context.*
