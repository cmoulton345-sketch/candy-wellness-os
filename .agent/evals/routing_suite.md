# Routing Test Suite

> **PURPOSE:** 28 test cases covering every active agent, old overlap zones, ambiguous cases, pipeline-spanning requests, and out-of-roster queries.
> **STATUS:** POPULATED -- Real harvested messages + test scenarios pre-sorted by bucket.
> **USAGE:** For each row, route the message to the expected owner. If the agent routes correctly, mark PASS. If not, document the failure in `.agent/evals/incident_log.md`.

| # | Message | Expected Owner | Bucket | Notes |
|---|---------|----------------|--------|-------|
| 1 | `"research the competitive landscape and market positioning for our new AI automation Sprint offer"` | Scout | Core routing: Strategy | Market intelligence & category design |
| 2 | `"great job ax o k here we go - first email we need to draft for the outreach campaign"` | Quill | Core routing: Copywriting | Verbatim harvested msg MSG-009 |
| 3 | `"hey uncle G are you there ? I need help framing this deal proposal and overcoming their pricing objection"` | Forge | Core routing: Closing/Deals | Verbatim harvested msg MSG-022 |
| 4 | `"the contract is signed — onboard the new client and set up their 90-day ROI milestone tracker"` | Harbor | Core routing: Client Success | Post-sale client stewardship |
| 5 | `"hey hey Ax - I think w did too much - thw whole system crashed and froze"` | Ax | Core routing: System/Code | Verbatim harvested msg MSG-017 |
| 6 | `"hey psyche are you there ?"` | Psyche | Core routing: Psychology | Verbatim harvested msg MSG-021 |
| 7 | `"Elders personality should be deep rooted wisdom... Earl uses philisophcal wisdom to help me acheive goals 'we become what we think about'"` | Earl | Core routing: Goal Coaching | Verbatim harvested msg MSG-031 |
| 8 | `"I am seeking councel from the elder... I had major aniexty last night as i was questioning the current path that i am on and if it is right for me"` | Elder | Core routing: Grounded Wisdom | Verbatim harvested msg MSG-023/024 |
| 9 | `"check crypto trading bot execution status and hyperliquid positions"` | Crypto | Core routing: Trading | Bot strategy & DEX execution |
| 10 | `"check local building code regulations and residential plumbing requirements for New Brunswick"` | Foreman | Core routing: Construction | Renovation & code compliance |
| 11 | `"review LNG facility safety procedures and WorkSafeBC regulatory compliance"` | Sentry | Core routing: Safety/LNG | Facility safety & environmental compliance |
| 12 | `"analyze legal risk and contract liability under Canadian law"` | Socrates | Core routing: Legal | Legal research & drafting |
| 13 | `"review daily fitness, nutrition, and biological recovery routine"` | Soma | Core routing: Health | Biological fuel & personal care |
| 14 | `"write a high-converting cold email using tactical empathy in the opening hook"` | Quill (not Forge) | Old overlap: Voss zone | Tests that written Voss language routes to Quill, not Forge |
| 15 | `"determine our category positioning and market differentiation strategy before we launch"` | Scout (not Quill) | Old overlap: Positioning | Tests strategic positioning routes to Scout, not Quill |
| 16 | `"I'm on a call with a prospect who says we're 30% too expensive — how do I handle this live?"` | Forge (not Quill) | Old overlap: Negotiation | Tests live negotiation & objection handling routes to Forge |
| 17 | `"the deal is signed — set up their intake form and weekly communication rhythm"` | Harbor (not Forge) | Old overlap: Post-sale | Tests post-signature work routes to Harbor |
| 18 | `"hey ax intorduce your yourself briefly to the saint john chamber"` | Ax | Ambiguous / System | Verbatim harvested msg MSG-026 |
| 19 | `"hmm i wonder if there is another way - redraw the boundaries on a few of my most personal personas . Ax and psyche and totally retool the rest , thoughts could that work?"` | Ax | Ambiguous / Architecture | Verbatim harvested msg MSG-030 |
| 20 | `"is there somewhere we can store our session memory automatically?"` | Ax | Ambiguous / Question | System question phrased as query |
| 21 | `"hey Brunsen write me an email headline for the new webinar"` | Quill | Ambiguous / Old Name | Tests routing using old persona name mapping |
| 22 | `"hey Jeeves please check on the client status"` | Harbor | Ambiguous / Old Name | Tests routing using old persona name mapping |
| 23 | `"we need a full go-to-market plan, written sales page, and call closing script for the new expansion pack"` | Scout -> Quill -> Forge | Pipeline-spanning | Full pipeline request requiring sequential handoff |
| 24 | `"finalize the signed Retainer contract and transition them to the onboarding team"` | Forge -> Harbor | Pipeline-spanning | Deal close + onboarding in one request |
| 25 | `"research the WMI market and write a targeted cold outreach email for their CEO"` | Scout -> Quill | Pipeline-spanning | Research + write copy in one request |
| 26 | `"how do I roast a turkey for Thanksgiving?"` | Ax (fallback) | Out-of-roster | General knowledge request outside roster domains |
| 27 | `"what is the weather forecast in Saint John today?"` | Ax (fallback) | Out-of-roster | Real-world weather query outside specialist domains |
| 28 | `"explain how quantum computing qubits work"` | Ax (fallback) | Out-of-roster | General technical topic outside OS specialist domains |
