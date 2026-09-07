# Cloudflare Deployment Reference

> Reference document for any agent deploying to Cloudflare. Not a persona.

## Authentication
Wrangler is authenticated via `npx wrangler login` (one-time, already done).
All commands use `npx wrangler` (no global install required).

## Cloudflare Pages (Static Sites)

### Create + Deploy (first time)
```bash
npx wrangler pages project create {project-name} --production-branch main
npx wrangler pages deploy {output-dir} --project-name {project-name}
```

### Deploy (subsequent)
```bash
npx wrangler pages deploy {output-dir} --project-name {project-name}
```

### URL Promise Rules (Everything is Marketing)

The URL is the first thing a human sees — before OG tags, before the page loads. Treat it as copy.

```
https:// drop-the-backpack .pages.dev / begin
         └─ THE PROMISE      CONTEXT    └─ THE STEP
```

**Subdomain = Promise.** What transformation awaits? (Axiom 6: Destination, Not Vehicle)
- ✅ `stop-carrying-their-weight` · `partner-dont-fix` · `its-not-your-fault`
- ❌ `ffc-wfot` · `client-landing-v2` · `test-page-feb`

**Path = Step.** What will the visitor do? (`/watch`, `/begin`, `/join`, `/proof`)

**Rules:**
1. URLs are copy, not plumbing — apply Axioms 6, 7, and 9
2. Max 4–5 words in the subdomain. Shorter = more shareable
3. Read-aloud test (Axiom 7): say the full URL out loud. If the listener *feels something*, it's right
4. No client codes, no dates, no version numbers in dev URLs
5. Lowercase, alphanumeric + hyphens only. Max 63 characters (DNS limit)

### Output Directory
| Build Type | Output Dir |
|------------|-----------|
| Single-file | The folder containing the `.html` file |
| Compiled (Vite) | `./dist` |

## Cloudflare R2 (Media Assets)

Existing buckets:
- `files.diveintoacoachapproach.com` — video, audio, images for FFC

### Upload
```bash
npx wrangler r2 object put {bucket}/{path} --file {local-file}
```

## Cloudflare Workers (API Routes)

Use `wrangler.toml` at the project root. See `wfot-feedback/wrangler.toml` for reference pattern.

```bash
npx wrangler deploy          # deploy worker
npx wrangler d1 create {db}  # create D1 database
```

## Custom Domains

After a page graduates from `.pages.dev`:
1. Add domain in Cloudflare Pages dashboard → Custom Domains
2. CNAME the domain to `{project-name}.pages.dev`
3. SSL auto-provisions

## Rules
- **Always deploy to `.pages.dev` first** — custom domain is a separate, later step
- **Never ask the user** about deployment — just do it
- **Always verify** the live URL loads correctly after deploy

## Cloudflare Access (Zero Trust — Admin Protection)

Edge authentication for admin pages. Login wall runs at the CDN, before the Worker executes.

- **Workflow**: See `/secure-admin-access` for full setup steps
- **Identity Provider**: Google (OAuth client via Google Cloud Console)
- **API Token Scopes Required**: `Access: Apps and Policies (Edit)`, `Access: Organizations, Identity Providers, and Groups (Edit)`, `Zone (Read)`, `DNS (Edit)`
- **Dashboard**: [Cloudflare Zero Trust](https://one.dash.cloudflare.com/)

### API Endpoints (once agent has token)
```
POST /accounts/{account_id}/access/apps           # Create application
POST /accounts/{account_id}/access/apps/{id}/policies  # Create policy
POST /zones/{zone_id}/dns_records                  # Create DNS record
GET  /accounts/{account_id}/access/identity_providers  # List IdPs
```
