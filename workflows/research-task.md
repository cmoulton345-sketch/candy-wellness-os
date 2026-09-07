---
description: Research the HOW for a single implementation task. Run once per task during planning, not all at once.
---

# /research-task

Research the specific **how** for one implementation plan task. This produces a How block that tells the executing agent exactly what to do — API calls, configurations, known gotchas, and code snippets.

> **When:** During PLANNING mode, after writing the implementation plan's WHAT checklist. Run this workflow once per task, sequentially.
> **Why:** Implementation plans that only say WHAT without HOW cause the executing agent to waste cycles doing research and implementation simultaneously.

## Input

A single unchecked task from the implementation plan. Example:

```
Wire n8n workflow to call RAG sidecar for context retrieval
```

## Steps

### 1. Identify the technologies involved

Read the task and list every technology, API, framework, or tool the task touches. Example: n8n, HTTP Request node, Docker networking, FastAPI, DuckDB.

### 2. Research each technology's specific interface

For each technology identified:

- **If it's an API:** Document the exact endpoint, method, headers, and request/response body. Use actual URLs, not placeholders.
- **If it's a framework feature:** Document the exact configuration, node type, or code pattern needed. Include version-specific details.
- **If it's infrastructure:** Document networking (Docker service names vs localhost), ports, volume mounts, environment variables.

Use web search, codebase search, and documentation review as needed. Do NOT guess — verify.

### 3. Identify gotchas

Search for known issues with the specific combination of technologies. Check:

- Project's own bug docs (e.g., `PROJECT_STATUS.md` "Bugs Found" section)
- Version-specific breaking changes
- Common pitfalls (e.g., n8n sandboxed Code nodes can't use `require()`)

### 4. Write the How block

Add a **How block** to the implementation plan under the relevant task. Format:

```markdown
### Task: [task description]

**How:**
1. [Exact step with specific details]
   - Config: `exact value or code snippet`
   - URL: `http://service:port/endpoint`
2. [Next step]
   ...

**Gotchas:**
- [Known issue and workaround]
- [Version-specific caveat]

**References:**
- [Link to relevant docs or files]
```

### 5. Verify completeness

Ask yourself: "Could an agent who has never seen this codebase execute this task using ONLY the How block?" If no, add more detail.

## Rules

- **One task at a time.** Do not batch-research multiple tasks. Research → write How → move to next task.
- **Be specific, not generic.** Write `http://rag:8100/search` not "call the search endpoint." Write `n8n HTTP Request node, Method: POST` not "make an API call."
- **Include real code/config.** If the task needs a JSON body, write the actual JSON. If it needs an n8n expression, write `{{$json.field}}`.
- **Document the negative.** If something WON'T work (like `require('fs')` in n8n), say so explicitly so the executing agent doesn't waste time trying it.
