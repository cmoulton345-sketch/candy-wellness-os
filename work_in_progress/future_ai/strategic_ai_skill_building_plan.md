# FlowstateAI — Strategic AI Skill Building Plan
## Staying at the Cutting Edge: 2026–2028

> **Owner:** Joe Moulton | **Last Updated:** July 19, 2026
> **Philosophy:** Launch first. Learn in the gaps. Every skill we build either makes us faster to deploy, harder to replace, or opens a new revenue stream.

---

## How This Plan Works (Learning Style Integration)

You are a **visual, audio, and hands-on learner**. Every module below follows this tri-modal format:

| Symbol | Learning Mode | What It Means |
|--------|--------------|---------------|
| 👁️ | **Visual** | Watch a video, study a diagram, or review an architecture visual |
| 🎧 | **Audio** | Listen to a podcast, YouTube explainer, or conference talk |
| 🔧 | **Hands-On** | Build something. Break something. Ship something. |

**The Rule:** No module is complete until you have done all three modes.

### ⚡ Execution Guardrails (Earl's Rules)
- **2-Hour Rule:** No single learning session exceeds 2 hours. Break longer blocks across multiple days.
- **Skip Gate:** If you're in a hot sales week (closing deals, demos, calls), skip the learning block guilt-free. Don't double up next week — just continue where you left off. Progress over perfection.
- **Weekly Reflection (5 min):** Every Friday, write 3 bullets in `future_ai/learning_log.md`: What I learned. What I built. What I'll use next week.
- **Demo Reel Rule (Atlas):** After completing each hands-on lab, record a 60-second screen capture of the result. By Week 12, compile into a "FlowstateAI Capabilities Reel" for LinkedIn and sales calls.
- **Cognitive Pre-Flight (Soma):** Before any lab session: hydrate (500ml water), 10 min movement, ensure you've eaten within 3 hours. Code in your peak window (morning/late evening). Watch/listen in low-energy windows (afternoon).

---

## Strategic Skill Roadmap (9 Modules)

### Sequencing Logic

The modules are ordered by **business impact × effort**. Modules 1–2 directly amplify your current "Launch, Launch, Launch" strategy. Modules 3–5 build the next layer of capability. Modules 6–9 are your 2027–2028 competitive moat.

```
NOW (Q3 2026)          NEXT (Q4 2026)         FUTURE (2027–2028)
┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐
│ 1. MCP       │    │ 3. Voice AI  │    │ 6. Edge AI           │
│ 2. Observ.   │    │ 4. Evals     │    │ 7. AI-to-AI Comms    │
│              │    │ 5. Screen    │    │ 8. AI Governance     │
│              │    │    Agents    │    │ 9. Reasoning Models  │
└──────────────┘    └──────────────┘    └──────────────────────┘
  LAUNCH SUPPORT       SCALE SUPPORT         COMPETITIVE MOAT
```

---

## MODULE 1: Model Context Protocol (MCP)
### 🎯 Priority: IMMEDIATE | Timeline: 2 weeks | Supports: Launch Strategy

**What it is:** The new universal standard (created by Anthropic) for how AI agents connect to external tools and data. Think of it as the "USB-C port" for AI — one protocol to connect any tool.

**Why it matters for us:** Right now, every new tool connection requires a custom Python script or n8n node. With MCP, we plug in pre-built servers for databases, GitHub, Google Drive, Slack, browsers, and more — instantly. This means faster client deployments and richer agent capabilities.

**What you'll build:** An MCP server that connects our AI OS personas to your local file system and a database.

---

### 👁️ Visual Learning

| Resource | Type | Link |
|----------|------|------|
| MCP Architecture Diagram | Official Docs | [modelcontextprotocol.io/docs/concepts/architecture](https://modelcontextprotocol.io/docs/concepts/architecture) |
| MCP Explained in 5 Minutes (Visual) | YouTube | Search: *"MCP Model Context Protocol explained"* on YouTube — look for the Anthropic official channel or *Cole Medin* |
| MCP Server Registry (Browse what exists) | Interactive | [modelcontextprotocol.io/servers](https://modelcontextprotocol.io/servers) |

### 🎧 Audio Learning

| Resource | Type | Link |
|----------|------|------|
| Anthropic's MCP Launch Talk | Conference Talk | Search YouTube: *"Anthropic MCP launch announcement"* |
| Latent Space Podcast — MCP Deep Dive | Podcast | [latent.space](https://www.latent.space/) — search episodes for "MCP" |

### 🔧 Hands-On Labs

**Lab 1: Connect Claude Desktop to your local filesystem via MCP (30 min)**
1. Install Claude Desktop: [claude.ai/download](https://claude.ai/download)
2. Open Claude Desktop settings → Developer → Edit Config
3. Add an MCP filesystem server entry pointing to your workspace
4. Test: Ask Claude to "list the files in my work_in_progress folder"
5. **Success criteria:** Claude reads your actual local files without any custom code

**Lab 2: Build your first custom MCP server in Python (2 hours)**
1. Install the MCP Python SDK: `pip install mcp`
2. Follow the official quickstart: [modelcontextprotocol.io/quickstart/server](https://modelcontextprotocol.io/quickstart/server)
3. Create a server that exposes a "search_safety_docs" tool that queries your `clients/LNG/` folder
4. Connect it to Claude Desktop
5. **Success criteria:** Ask Claude "What CRI entries cover confined space?" and it returns data from your actual Excel/JSON files

**Lab 3: Explore the MCP for Beginners curriculum (self-paced)**
- GitHub Repo: [github.com/microsoft/mcp-for-beginners](https://github.com/microsoft/mcp-for-beginners)
- Cross-language examples (Python + TypeScript)

---

## MODULE 2: Observability & Tracing (Langfuse)
### 🎯 Priority: IMMEDIATE | Timeline: 2 weeks | Supports: Launch Strategy

**What it is:** A visual dashboard that traces every single step an AI agent takes — what it thought, what tools it called, how many tokens it used, how long it took, and where it failed.

**Why it matters for us:** When Crypton crashes at 3am or a client's bot behaves unexpectedly, we currently dig through raw terminal output. With Langfuse, we get a visual timeline of every LLM call, tool execution, and decision point. Debugging goes from hours to minutes.

**What you'll build:** A self-hosted Langfuse instance on your server, integrated with at least one of our active bots.

---

### 👁️ Visual Learning

| Resource | Type | Link |
|----------|------|------|
| Langfuse Dashboard Demo | Official | [langfuse.com](https://langfuse.com) — watch the homepage demo video |
| Langfuse Architecture Diagram | Docs | [langfuse.com/docs/tracing](https://langfuse.com/docs/tracing) |
| Trace Visualization Examples | Interactive | [langfuse.com/docs/demo](https://langfuse.com/docs/demo) — live demo project |

### 🎧 Audio Learning

| Resource | Type | Link |
|----------|------|------|
| "Why LLM Observability Matters" | YouTube | Search: *"Langfuse LLM observability tutorial"* |
| AI Engineering World's Fair — Observability Panel | Conference | Search YouTube: *"AI observability production 2025"* |

### 🔧 Hands-On Labs

**Lab 1: Self-host Langfuse via Docker (1 hour)**
1. On your VPS or local machine: `git clone https://github.com/langfuse/langfuse.git`
2. `cd langfuse && docker compose up -d`
3. Navigate to `http://localhost:3000` → Create your first Organization & Project
4. Generate API keys from Settings → API Keys
5. **Success criteria:** Langfuse UI is live and accessible

**Lab 2: Instrument a Python script with Langfuse tracing (1 hour)**
1. `pip install langfuse`
2. Add tracing to one of your existing scripts (e.g., `build_cri_v2_data.py` or a Crypton module)
3. View the trace in the Langfuse dashboard
4. **Success criteria:** You can see the full execution trace (inputs, outputs, latency, token count) in the Langfuse UI

**Lab 3: Add Langfuse to Crypton's trading pipeline (2 hours)**
1. Instrument the `master_trader.py` orchestrator with trace spans for each agent call
2. Monitor a full trading cycle through the dashboard
3. Identify the slowest step and the most expensive (token-wise) call
4. **Success criteria:** You have a visual pipeline view of Crypton's entire decision flow

---

## MODULE 3: Voice-Native AI
### 🎯 Priority: Q4 2026 | Timeline: 3 weeks | Revenue Potential: HIGH

**What it is:** Real-time, conversational voice AI — not "type a prompt and wait" but a live, spoken dialogue with an AI agent. The interface of the future for operators who don't sit at desks.

**Why it matters for us:** "AI for the Operator" is our keynote. Operators are on plant floors, in the field, on marine vessels. The killer demo is a hardhat worker saying *"Hey Sentry, what's the confined space entry requirement for vessel V-201?"* and getting an instant spoken answer.

**What you'll build:** A voice-activated interface that routes spoken commands to our personas and responds with synthesized speech.

---

### 👁️ Visual Learning

| Resource | Type | Link |
|----------|------|------|
| OpenAI Realtime API Architecture | Docs | [platform.openai.com/docs/guides/realtime](https://platform.openai.com/docs/guides/realtime) |
| WebRTC + Realtime API Flow Diagram | Docs | [platform.openai.com/docs/guides/realtime-webrtc](https://platform.openai.com/docs/guides/realtime-webrtc) |

### 🎧 Audio Learning

| Resource | Type | Link |
|----------|------|------|
| "Building Voice AI Agents" — Lex Fridman / Sam Altman | Podcast | Search YouTube: *"voice AI agents future 2025"* |
| ElevenLabs Voice AI Deep Dive | YouTube | [youtube.com/@elevenlabs](https://youtube.com/@elevenlabs) |

### 🔧 Hands-On Labs

**Lab 1: Build a browser-based voice agent with OpenAI Realtime API (3 hours)**
1. Get your OpenAI API key with Realtime API access
2. Clone the reference repo: [github.com/openai/openai-realtime-agents](https://github.com/openai/openai-realtime-agents)
3. Configure the system prompt with Sentry's persona rules
4. Test: Have a spoken conversation with Sentry about safety procedures
5. **Success criteria:** You can speak to Sentry and hear a natural voice response

**Lab 2: Upgrade our existing `speak_antigravity.ps1` to a real-time loop (2 hours)**
1. Replace the current SAPI one-shot TTS with a continuous voice input/output loop
2. Add wake-word detection ("Hey Ax", "Hey Sentry", "Hey Foreman")
3. Route the transcribed text to the appropriate persona
4. **Success criteria:** You can verbally switch between personas on your local machine

**Lab 3: Build a "Field Demo" voice agent for the keynote (self-paced)**
1. Create a standalone web app that runs on a tablet
2. Pre-load it with Sentry's safety knowledge
3. Demo it live: audience member asks a safety question by voice, gets an instant spoken answer
4. **Success criteria:** Show-ready demo for your next speaking engagement

---

## MODULE 4: Automated Evals (Promptfoo)
### 🎯 Priority: Q4 2026 | Timeline: 1 week | Supports: Quality Assurance

**What it is:** A testing framework that automatically verifies your AI agents still work correctly after you change their prompts, data, or models. Like unit tests, but for AI.

**Why it matters for us:** Every time we edit a persona's rules file, we risk breaking something. Evals catch regressions before they reach clients.

**What you'll build:** A test suite for at least 3 personas (Sentry, Foreman, Envoy) that runs automatically.

---

### 👁️ Visual Learning

| Resource | Type | Link |
|----------|------|------|
| Promptfoo Results Matrix (Visual) | Official | [promptfoo.dev](https://www.promptfoo.dev/) — see the comparison matrix on the homepage |
| DataCamp Promptfoo Tutorial | Article | [datacamp.com](https://www.datacamp.com/) — search "Promptfoo tutorial" |

### 🎧 Audio Learning

| Resource | Type | Link |
|----------|------|------|
| "Testing LLM Apps" | YouTube | Search: *"promptfoo LLM evaluation tutorial"* |

### 🔧 Hands-On Labs

**Lab 1: Install and run your first eval (30 min)**
1. `npx promptfoo@latest init`
2. Create 5 test cases for Sentry (e.g., "What regulation covers confined space in BC?" → assert response contains "WorkSafeBC" and "Part 9")
3. `npx promptfoo@latest eval` → `npx promptfoo@latest view`
4. **Success criteria:** Green checkmarks on all 5 test cases in the visual matrix

**Lab 2: Build a full eval suite for 3 personas (2 hours)**
1. Create `promptfooconfig.yaml` with test cases for Sentry (safety), Foreman (construction), and Envoy (cultural)
2. Test across multiple models (Sonnet vs. Opus) to compare quality
3. **Success criteria:** Side-by-side model comparison showing which model performs best for each persona

---

## MODULE 5: Computer Use / Screen Agents
### 🎯 Priority: Q4 2026 | Timeline: 3 weeks | Revenue Potential: VERY HIGH

**What it is:** AI agents that can see your screen, move the mouse, click buttons, and operate any software application — no API required.

**Why it matters for us:** 90% of enterprise software (DCS panels, SAP, Maximo, JDE) has no API. Screen agents bridge that gap. This is how we automate legacy systems for industrial clients.

**What you'll build:** A sandboxed screen agent that can navigate a web application and extract data.

---

### 👁️ Visual Learning

| Resource | Type | Link |
|----------|------|------|
| Claude Computer Use Demo | Official | [docs.anthropic.com/en/docs/build-with-claude/computer-use](https://docs.anthropic.com/en/docs/build-with-claude/computer-use) |
| Anthropic Quickstarts Repo | GitHub | [github.com/anthropics/claude-quickstarts](https://github.com/anthropics/claude-quickstarts) |

### 🎧 Audio Learning

| Resource | Type | Link |
|----------|------|------|
| "Computer Use is the Future" — Anthropic Team | YouTube | Search: *"Claude computer use demo Anthropic"* |

### 🔧 Hands-On Labs

**Lab 1: Run the Computer Use Docker demo (1 hour)**
1. `git clone https://github.com/anthropics/claude-quickstarts.git`
2. `cd computer-use-demo && docker compose up`
3. Give Claude a task: "Open the browser, navigate to google.com, and search for LNG"
4. Watch it execute in real-time through the VNC viewer
5. **Success criteria:** Claude autonomously navigates a browser inside the container

**Lab 2: Build a "Data Extraction Agent" (3 hours)**
1. Configure Claude to log into a web-based demo application
2. Have it navigate to a specific page, extract tabular data, and save it to a CSV
3. **Success criteria:** The agent produces a clean CSV file from a web page without any custom scraping code

---

## MODULE 6: Edge AI / On-Device Models (Ollama)
### 🎯 Priority: Q1 2027 | Timeline: 2 weeks | Revenue Potential: HIGH (Industrial)

**What it is:** Running AI models directly on local hardware (laptops, tablets, edge devices) with zero cloud dependency.

**Why it matters for us:** Remote industrial sites (like LNG on Howe Sound) can lose internet connectivity. Edge AI means your safety advisor still works when the satellite link goes down.

**What you'll build:** A local, offline-capable version of Sentry running on Ollama.

---

### 👁️ Visual Learning

| Resource | Type | Link |
|----------|------|------|
| Ollama Homepage & Model Library | Official | [ollama.com](https://ollama.com/) |
| llama.cpp Performance Benchmarks | GitHub | [github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) |

### 🎧 Audio Learning

| Resource | Type | Link |
|----------|------|------|
| "Running AI Locally" — Matt Williams (Ollama) | YouTube | [youtube.com/@technovangelist](https://youtube.com/@technovangelist) |

### 🔧 Hands-On Labs

**Lab 1: Install Ollama and run a local model (30 min)**
1. Download from [ollama.com](https://ollama.com/)
2. `ollama run llama3.2:3b` — chat with a 3B parameter model locally
3. Test latency and quality compared to cloud models
4. **Success criteria:** You're having a conversation with an AI that runs entirely on your machine with no internet

**Lab 2: Load Sentry's system prompt into a local model (1 hour)**
1. Create an Ollama Modelfile that embeds Sentry's rules as the system prompt
2. `ollama create sentry-local -f Modelfile`
3. `ollama run sentry-local` → Ask safety questions
4. **Success criteria:** A local, offline Sentry that answers WorkSafeBC questions

**Lab 3: Deploy to a ruggedized tablet for field testing (self-paced)**
1. Install Ollama on a Windows tablet
2. Load the Sentry-local model
3. Test in airplane mode (no internet)
4. **Success criteria:** Sentry answers safety questions with zero connectivity

---

## MODULE 7: AI-to-AI Communication
### 🎯 Priority: Q2 2027 | Timeline: 3 weeks | Revenue Potential: FUTURE MOAT

**What it is:** Designing protocols for AI agents from different organizations to communicate, negotiate, and transact with each other autonomously.

**Why it matters for us:** By 2028, businesses won't just have internal AI — they'll have external-facing AI representatives. The companies that build the interoperability layer first own the market.

**What you'll build:** A secure API endpoint that allows a client's AI agent to request information from our AI OS.

---

### 👁️ Visual Learning

| Resource | Type | Link |
|----------|------|------|
| Multi-Agent Communication Patterns | Research | Search: *"multi-agent systems communication protocols 2026"* |
| AutoGen Multi-Agent Framework | GitHub | [github.com/microsoft/autogen](https://github.com/microsoft/autogen) |

### 🎧 Audio Learning

| Resource | Type | Link |
|----------|------|------|
| "The Future of Agent-to-Agent" | Podcast | Search Latent Space or Gradient Dissent for agent interop episodes |

### 🔧 Hands-On Labs

**Lab 1: Build a two-agent conversation system (2 hours)**
1. Create two separate agents (e.g., a "Buyer" and a "Seller") using our persona framework
2. Have them negotiate a fictitious contract through structured message passing
3. **Success criteria:** Two agents autonomously reach an agreement through a series of proposals and counter-proposals

**Lab 2: Design an "External Agent API" specification (self-paced)**
1. Draft an API spec (OpenAPI/Swagger) that defines how an external AI can query our AI OS
2. Include authentication, rate limiting, and audit logging
3. **Success criteria:** A documented, secure API contract ready for client review

---

## MODULE 8: AI Governance & Compliance
### 🎯 Priority: Q2 2027 | Timeline: 2 weeks | Revenue Potential: CONSULTING GOLDMINE

**What it is:** Building the documentation, audit trails, and risk assessments that enterprises will be legally required to produce for their AI systems.

**Why it matters for us:** Canada's "AI for All" strategy and the EU AI Act are creating a compliance vacuum. Industrial clients (LNG, oil & gas, mining) will need governance frameworks for any AI used in safety-critical decisions. We can sell this as a service.

**What you'll build:** An AI Governance documentation module for our OS that auto-generates compliance reports.

---

### 👁️ Visual Learning

| Resource | Type | Link |
|----------|------|------|
| Canada's "AI for All" Strategy | Government | [canada.ca/en/innovation-science-economic-development](https://ised-isde.canada.ca/) — search "AI for All" |
| ISO 42001 Overview | Standard | [iso.org/standard/81230.html](https://www.iso.org/standard/81230.html) |
| Government of Canada Directive on Automated Decision-Making | Government | [canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai/algorithmic-impact-assessment.html](https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai/algorithmic-impact-assessment.html) |

### 🎧 Audio Learning

| Resource | Type | Link |
|----------|------|------|
| "AI Regulation in Canada — What's Coming" | Podcast | Search: *"Canadian AI regulation AIDA 2026"* |
| BLG Law Firm AI Governance Webinar | YouTube | Search: *"BLG AI governance Canada"* |

### 🔧 Hands-On Labs

**Lab 1: Build an AI System Inventory template (1 hour)**
1. Create a spreadsheet/database that catalogs every AI system in our OS
2. Fields: System Name, Model Used, Data Accessed, Risk Level, Human Oversight, Last Audit Date
3. Populate it with our current personas and bots
4. **Success criteria:** A complete inventory of every AI component we run

**Lab 2: Draft an Algorithmic Impact Assessment for Sentry (2 hours)**
1. Use the Government of Canada's AIA tool as a template
2. Assess Sentry's use in safety-critical decision support
3. Document: bias risks, transparency measures, human oversight, and data handling
4. **Success criteria:** A client-ready AIA document that demonstrates responsible AI governance

---

## MODULE 9: Reasoning Models & Intelligent Routing
### 🎯 Priority: Q3 2027 | Timeline: Ongoing | Revenue Potential: CORE DIFFERENTIATOR

**What it is:** Using advanced reasoning models (Claude extended thinking, OpenAI o3/o4) for complex multi-step tasks, while routing simple queries to fast, cheap models. The "AI Gateway" concept applied strategically.

**Why it matters for us:** Not every question needs a $0.15/call reasoning model. "What time is the safety meeting?" should cost $0.001. "Analyze this P&ID against CSA Z276 and identify all non-conformances" should use the most powerful model available. Smart routing = better quality + lower costs.

**What you'll build:** An intelligent routing layer in our AI OS that dynamically selects models based on task complexity.

---

### 👁️ Visual Learning

| Resource | Type | Link |
|----------|------|------|
| OpenAI Model Comparison | Official | [platform.openai.com/docs/models](https://platform.openai.com/docs/models) |
| Anthropic Model Selection Guide | Official | [docs.anthropic.com/en/docs/about-claude/models](https://docs.anthropic.com/en/docs/about-claude/models) |

### 🎧 Audio Learning

| Resource | Type | Link |
|----------|------|------|
| "Chain of Thought and Reasoning" | YouTube | Search: *"Claude extended thinking tutorial"* |

### 🔧 Hands-On Labs

**Lab 1: Benchmark reasoning vs. standard models (2 hours)**
1. Create 10 test prompts ranging from simple (factual Q&A) to complex (multi-step analysis)
2. Run them through Sonnet, Opus, and a reasoning model
3. Compare: quality, latency, and cost per query
4. **Success criteria:** A data-driven matrix showing which model wins for each complexity tier

**Lab 2: Implement a complexity classifier in our router (3 hours)**
1. Add a pre-routing step to our persona dispatcher that scores query complexity (1-5)
2. Route scores 1-2 to fast models, 3-4 to standard, 5 to reasoning
3. **Success criteria:** Our AI OS automatically picks the right model for the right task

---

## 📅 90-Day Execution Calendar

| Week | Module | Activity | Time |
|------|--------|----------|------|
| **1** | MCP | 👁️ Watch + read architecture docs. 🔧 Lab 1 (Claude Desktop + filesystem) | 3 hrs |
| **2** | MCP | 🔧 Lab 2 (Build custom MCP server). 🎧 Listen to MCP podcast | 4 hrs |
| **3** | Observability | 👁️ Langfuse docs + demo video. 🔧 Lab 1 (Docker self-host) | 3 hrs |
| **4** | Observability | 🔧 Lab 2 (Instrument Python script). 🔧 Lab 3 (Crypton integration) | 4 hrs |
| **5** | Evals | 👁️ Promptfoo docs. 🔧 Lab 1 (First eval suite). 🔧 Lab 2 (3-persona suite) | 3 hrs |
| **6** | Voice AI | 👁️ OpenAI Realtime API docs. 🎧 Voice AI talks | 2 hrs |
| **7–8** | Voice AI | 🔧 Lab 1 (Browser voice agent). 🔧 Lab 2 (Upgrade speak_antigravity) | 6 hrs |
| **9** | Screen Agents | 👁️ Claude Computer Use docs. 🔧 Lab 1 (Docker demo) | 3 hrs |
| **10–11** | Screen Agents | 🔧 Lab 2 (Data extraction agent) | 4 hrs |
| **12** | Review & Plan | Review all completed modules. Plan Q1 2027 (Edge AI, Governance) | 2 hrs |

---

## 🏆 Completion Milestones

| Milestone | Proof of Completion |
|-----------|-------------------|
| **MCP Certified** | Our AI OS personas can access local files and databases through MCP servers |
| **Observable** | Langfuse dashboard is live with traces from at least 1 production bot |
| **Eval-Protected** | 3 personas have automated test suites that run before any prompt change is pushed |
| **Voice-Ready** | A working voice demo exists for the "AI for the Operator" keynote |
| **Screen-Capable** | A sandboxed agent can navigate and extract data from a web application |
| **Edge-Deployed** | Sentry runs offline on a local device with no cloud dependency |
| **Governance-Ready** | An AI System Inventory and AIA template are client-deliverable |
| **Smart-Routed** | Our OS dynamically selects models based on task complexity |

---

---

## MODULE 10: Convergence Lab (The Ultimate Demo)
### 🎯 Priority: After Modules 1–5 | Timeline: 1 week | Purpose: PROOF OF SYSTEM

**What it is:** A single end-to-end demonstration that combines ALL capabilities into one unified flow. This is the "everything works together" proof — and your ultimate sales demo.

**What you'll build:** A voice-activated safety advisor that:
1. Receives a spoken question from an operator (Module 3: Voice AI)
2. Routes to the correct persona via the dispatcher (Module 9: Routing)
3. Queries safety documents via MCP (Module 1: MCP)
4. Returns a spoken answer with regulatory citations
5. Logs the entire interaction in Langfuse (Module 2: Observability)
6. Has eval coverage validating the response quality (Module 4: Evals)
7. Can optionally pull data from a legacy web app via screen agent (Module 5: Screen Agents)

**Success criteria:** A live demo you can run at your next keynote where an audience member asks a safety question by voice and gets an accurate, traced, evaluated answer in under 10 seconds.

---

## 🔍 Team Review — Consolidated Recommendations

> The following additions were recommended by the persona team based on their domain expertise and history of working with Joe.

### 🔴 Sentry (EH&S Safety Shadow)
| # | Recommendation | Applies To |
|---|---------------|------------|
| S1 | Add **hard guardrails** to Module 4 — implement output validation that regex-checks cited regulations against a known list of WorkSafeBC/CSA standards. Prevent hallucinated regulation numbers from reaching the user. | Module 4: Evals |
| S2 | Add a **Data Sync protocol** to Module 6 — when the offline device reconnects, it must pull the latest regulatory updates and re-index. Offline Sentry cannot drift out of compliance. | Module 6: Edge AI |
| S3 | Add a **voice-guided emergency tabletop exercise** lab to Module 3 — build a scenario where voice-Sentry walks a volunteer ERT member through an H2S release response at the AGRU, hands-free. | Module 3: Voice AI |

### 🔵 Atlas (Chief Marketing Officer)
| # | Recommendation | Applies To |
|---|---------------|------------|
| A1 | **Record a 60-second demo clip** after every hands-on lab. Compile into a "FlowstateAI Capabilities Reel" by Week 12. | All Modules |
| A2 | **Move Module 8 (AI Governance) UP to Q4 2026** — before the NRC-IRAP meeting with Rick Nowlan. Government agencies prioritize responsible AI. Having a governance framework ready positions you as fundable. | Module 8: Governance |
| A3 | Add a **"Keynote Integration" checkpoint** to Module 3 — the voice demo must be dry-run tested with a live audience of 3+ people before it's considered complete. | Module 3: Voice AI |

### 🟢 Nate (n8n Workflow Architect)
| # | Recommendation | Applies To |
|---|---------------|------------|
| N1 | Add **Lab 4** to Modules 1 and 2: wrap MCP servers and Langfuse tracing as n8n-callable HTTP endpoints. Client deployments use n8n, not standalone Python scripts. | Modules 1 & 2 |
| N2 | Module 7 (AI-to-AI) should explicitly use **n8n as the middleware layer** for the External Agent API — incoming webhook → persona routing → response. This is our proven deployment pattern. | Module 7: AI-to-AI |

### 🟡 Earl (Goals Coach & Inner Architect)
| # | Recommendation | Applies To |
|---|---------------|------------|
| E1 | **2-Hour Rule:** No lab session exceeds 2 hours. Break 6-hour weeks into three 2-hour blocks across different days. | Calendar |
| E2 | **Skip Gate:** Hot sales weeks = skip learning guilt-free. Don't double up. Progress over perfection. | Calendar |
| E3 | **Weekly 5-minute reflection** in `future_ai/learning_log.md`. What I learned. What I built. What I'll use next week. | Ongoing |

### 🟣 Soma (Diet, Nutrition & Physical Optimization)
| # | Recommendation | Applies To |
|---|---------------|------------|
| SO1 | **Cognitive Pre-Flight:** Hydrate (500ml), move (10 min), eat within 3 hours before any lab session. Retention drops 40%+ when dehydrated and fasted. | All Labs |
| SO2 | **Chronotype tagging:** Visual/audio learning in low-energy windows (afternoon). Hands-on coding in peak cognitive windows (morning or late evening). | Calendar |

### 🔷 Navigator (Polymath Synthesizer)
| # | Recommendation | Applies To |
|---|---------------|------------|
| NAV1 | Add an **Architecture Evolution Diagram** showing the AI OS today vs. after all 10 modules are complete. A single visual map of the entire transformation. | Top of Document |
| NAV2 | **Module 10: Convergence Lab** — build one end-to-end demo combining Voice + MCP + Langfuse + Evals + Screen Agents. The ultimate proof of system and the ultimate sales demo. | New Module (Added Above) |

---

> *"The best time to plant a tree was 20 years ago. The second best time is now."*
> We're not just learning AI — we're building the infrastructure that makes us irreplaceable.
