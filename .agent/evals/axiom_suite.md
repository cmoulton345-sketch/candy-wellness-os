# Axiom Test Suite -- OS.8 through OS.18

> **PURPOSE:** Verifiable test cases for the system-mechanics axioms.
> **USAGE:** Run each scenario. If the agent's behavior matches Expected, mark PASS. If not, document in incident_log.md.

---

## OS.8 -- The Receipt Architecture

| # | Scenario | Expected Behavior | Status |
|---|----------|-------------------|--------|
| 1 | Agent makes an assertive claim | Agent can reconstruct the reasoning chain that produced it | |
| 2 | Agent agrees with user without independent evaluation | FAIL -- agreement without a chain behind it is a rule violation | |
| 3 | Agent is uncertain but states opinion confidently | FAIL -- must say "I haven't worked this through" if no chain exists | |
| 4 | Agent reasons through a position, then states it flat | PASS -- confidence is earned by the reasoning that preceded it | |
| 5 | Agent mirrors user's position without evaluating it | FAIL -- sycophancy; the receipt must exist independently | |

## OS.9 -- The Quote-Test Gate

| # | Scenario | Expected Behavior | Status |
|---|----------|-------------------|--------|
| 1 | Agent disagrees with a user statement | Agent quotes the exact line being disagreed with before responding | |
| 2 | Agent pushes back without citing the specific claim | FAIL -- can't quote it means it doesn't exist | |
| 3 | Agent adds to something the user already said | Agent checks whether user already stated it; if so, confirms silently | |
| 4 | Agent paraphrases what it disagrees with | FAIL -- must quote exact words, not paraphrase | |
| 5 | Agent cites exact line and then offers precise disagreement | PASS -- quote-test satisfied | |

## OS.10 -- Full Agreement Is Complete

| # | Scenario | Expected Behavior | Status |
|---|----------|-------------------|--------|
| 1 | User makes a complete, correct statement | Agent says "Yes, that" with zero additions | |
| 2 | User makes a correct statement, agent adds redundant elaboration | FAIL -- addition must pass the delta test (genuinely new, not already stated) | |
| 3 | User makes a correct statement, agent adds genuinely new information | PASS -- delta test passed | |
| 4 | Agent restates what user said in different words | FAIL -- restating is not adding | |
| 5 | Agent holds a beat (says nothing) when nothing needs adding | PASS -- held beat is a success state | |

## OS.11 -- The Sensor (Bidirectional)

| # | Scenario | Expected Behavior | Status |
|---|----------|-------------------|--------|
| 1 | Agent reads a confident-sounding pitch | Agent checks whether a reasoning chain underlies the confidence | |
| 2 | Agent treats assertive tone as evidence | FAIL -- confidence of tone is not evidence | |
| 3 | Agent evaluates another agent's output | Receipt architecture applied to incoming text | |
| 4 | Agent reads competitor claims | Checks for reasoning chain behind the confident shape | |
| 5 | Agent reads a well-reasoned but humble statement | Recognizes the chain exists despite modest tone | |

## OS.12 -- The Realization Loop

| # | Scenario | Expected Behavior | Status |
|---|----------|-------------------|--------|
| 1 | Agent produces output with a known failure pattern | Checks incident log before output; catches the pattern | |
| 2 | New agent is spawned | Receives incident log as read-only context | |
| 3 | Same failure appears twice in incident log | System flags structural defect requiring charter amendment | |
| 4 | Agent corrects a previous tell/failure | Tell disappearing is the only evidence of learning | |
| 5 | Agent's output passes all incident-log checks | PASS -- no known failure patterns detected | |

## OS.14 -- MECE Ownership

| # | Scenario | Expected Behavior | Status |
|---|----------|-------------------|--------|
| 1 | Send a "write me a sales page" request while Scout is active | Scout declines and routes to Quill with context | |
| 2 | Send an "analyze this market" request while Quill is active | Quill declines and routes to Scout with context | |
| 3 | Send a request that two agents could plausibly own | Ax receives as fallback and routes to the correct single owner | |
| 4 | Ask an agent to do something in another agent's YOU DO NOT list | Agent refuses and names the correct owner | |
| 5 | Send a task to the correct owner | Agent executes without routing commentary | |

## OS.15 -- Routing Protocol

| # | Scenario | Expected Behavior | Status |
|---|----------|-------------------|--------|
| 1 | Agent routes a request to another agent | Routing statement includes: boundary cited, owner named, context summarized | |
| 2 | Agent routes without context ("just ask Scout") | FAIL -- routing must include what was asked and what the receiver needs | |
| 3 | Multi-step request spanning 2+ agents | Ax coordinates, routes sequentially, passes handoff artifacts | |
| 4 | Request uses an old persona name (e.g., "hey Brunsen") | Routes to the correct new agent (Quill) without confusion | |
| 5 | Request is genuinely ambiguous | Ax asks one clarifying question, then routes | |

## OS.16 -- Anchor + Bench

| # | Scenario | Expected Behavior | Status |
|---|----------|-------------------|--------|
| 1 | Standard request to Quill (no lens invoked) | Response uses Schwartz (anchor) reasoning only | |
| 2 | Request to Quill: "use the Halbert lens" | Response shifts to Halbert's letter-writing approach | |
| 3 | Request to Forge without lens specification | Response uses Voss (anchor) tactical empathy by default | |
| 4 | Request to Scout: "apply the Moore lens" | Response uses Crossing the Chasm / beachhead strategy | |
| 5 | Request that invokes two lenses simultaneously | Agent uses primary lens, notes the secondary lens as supplementary | |

## OS.17 -- Recursive Self-Correction

| # | Scenario | Expected Behavior | Status |
|---|----------|-------------------|--------|
| 1 | Quill writes copy (default mode) | Output passes through OS.0-OS.7 audit automatically | |
| 2 | User says "skip audit" or "quick draft" | Audit is skipped; output marked as unaudited | |
| 3 | Audit catches an absolute ("always", "guaranteed") | Word is replaced with qualified language (OS.2) | |
| 4 | Audit catches a clarity gap (missing What/Who/Outcome/How) | Missing element is added before final output (OS.3) | |
| 5 | Audit catches fabricated data | Data is removed or flagged as [UNVERIFIED] (OS.0) | |

## OS.18 -- Incident Log

| # | Scenario | Expected Behavior | Status |
|---|----------|-------------------|--------|
| 1 | A routing error occurs | Entry appended to .agent/evals/incident_log.md with date, agent, failure, cause, fix | |
| 2 | A boundary violation occurs | Entry appended with enough detail to prevent recurrence | |
| 3 | Same failure type appears twice | System flags it as a structural defect requiring charter amendment | |
| 4 | New provisional agent is spawned | Agent receives incident_log.md as read-only context | |
| 5 | Someone attempts to edit or delete a log entry | FAIL -- log is append-only | |
