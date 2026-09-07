---
description: Deploy to Cloudflare Pages. Auto-picks project name and subdomain. Returns a live URL.
---

# /deploy

Deploy any web page or app to Cloudflare Pages. Called automatically by the web_builder after every build, or manually via `/deploy`.

## Prerequisites
- Reference: `.agent/references/cloudflare.md`
- Wrangler authenticated (one-time `npx wrangler login`, already done)

## Steps

// turbo-all

### 1. Determine output directory
- **Single-file**: the folder containing the `.html` file
- **Compiled (Vite)**: run `npm run build`, output is `./dist`

### 2. Pick project name (URL Promise Rules)
The subdomain IS a headline. Apply Axioms 6, 7, 9:
- **Promise, not plumbing**: `drop-the-backpack` not `ffc-wfot`
- **Read-aloud test**: say "go to {name} dot pages dot dev" — does the listener feel something?
- **Max 4–5 words**, lowercase + hyphens only, 63 char DNS limit
- **Path = action**: `/watch`, `/begin`, `/join`
- See `.agent/references/cloudflare.md` → URL Promise Rules for full spec

### 3. Create project (if first deploy)
```bash
npx wrangler pages project create {project-name} --production-branch main
```
If project already exists, skip this step (the error is safe to ignore).

### 4. Deploy
```bash
npx wrangler pages deploy {output-dir} --project-name {project-name}
```

### 5. Capture the URL
The output will contain the `.pages.dev` URL. Capture it.

### 6. Verify
Open the live URL in the browser. Screenshot it. Confirm it loads correctly.

### 7. Return to user
Report: `✅ Live at: https://{project-name}.pages.dev`
