---
description: Secure any admin page with Cloudflare Access (Zero Trust). Covers DNS, IdP setup, application + policy creation, and API token for agent automation.
---

# /secure-admin-access

End-to-end workflow for protecting an admin route behind Cloudflare Access using Google as the identity provider. This is an edge authentication solution — the login wall runs at the CDN level, before the Worker ever executes.

## Prerequisites
- A Cloudflare account with the zone (domain) already active
- A Cloudflare Worker already deployed with routes for the admin page
- The admin emails list (who should have access)
- Google Cloud Console access (for OAuth client setup)

---

## Phase 1: DNS — Create the Admin Subdomain

> Skip this phase if the admin lives at a path (e.g. `/admin`) rather than a separate subdomain.

### Step 1.1 — Add DNS record for the admin subdomain

1. Go to **Cloudflare Dashboard** → select the domain → **DNS** → **Records**
2. Click **Add Record**
3. Configure:
   | Field | Value |
   |-------|-------|
   | Type | **CNAME** |
   | Name | `admin` |
   | Target | The same target as your main subdomain (e.g. `testimonials` CNAME target), or `{worker-name}.{account-subdomain}.workers.dev` |
   | Proxy status | **Proxied** (orange cloud ON) |
   | TTL | Auto |
4. Save

> [!IMPORTANT]
> The orange cloud (Proxied) MUST be enabled — Cloudflare Access only works on proxied records.

### Step 1.2 — Add the route to `wrangler.toml`

In the Worker's `wrangler.toml`, add the admin subdomain route:

```toml
routes = [
  { pattern = "testimonials.example.com/*", zone_name = "example.com" },
  { pattern = "admin.example.com/*", zone_name = "example.com" }
]
```

Then deploy: `npx wrangler deploy`

### Step 1.3 — Verify DNS resolution

Wait 1–2 minutes, then:
```bash
nslookup admin.example.com
```
Should resolve to a Cloudflare IP. If it returns NXDOMAIN, the record hasn't propagated yet.

---

## Phase 2: Google OAuth Client (Identity Provider Setup)

### Step 2.1 — Create a Google Cloud project (or use existing)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Name it something like `Cloudflare Access - {Company Name}`

### Step 2.2 — Configure the OAuth Consent Screen

1. Navigate to **APIs & Services** → **OAuth consent screen**
2. Select **External** user type → Create
3. Fill in:
   | Field | Value |
   |-------|-------|
   | App name | `{Company} Admin Access` |
   | User support email | Your email |
   | Developer contact email | Your email |
4. **Scopes**: Add `email`, `profile`, `openid`
5. **Test users**: Add all authorized email addresses
6. Save

> [!NOTE]
> While the app is in "Testing" mode, only listed test users can log in. This is fine — it acts as an extra layer of security. If you want to skip the test user list, you can publish the app (it won't need Google review since you're only requesting basic scopes).

### Step 2.3 — Create OAuth Client ID

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Configure:
   | Field | Value |
   |-------|-------|
   | Application type | **Web application** |
   | Name | `Cloudflare Access` |
   | Authorized redirect URIs | `https://{your-team-name}.cloudflareaccess.com/cdn-cgi/access/callback` |

4. Click **Create**
5. **Copy the Client ID and Client Secret** — you'll need both

> [!CAUTION]
> The redirect URI must match your Cloudflare Zero Trust team name exactly. Find your team name in Zero Trust dashboard → Settings → Custom Pages → Team domain.

---

## Phase 3: Cloudflare Zero Trust Configuration

### Step 3.1 — Find your Team Name

1. Go to [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/)
2. Navigate to **Settings** → **Custom Pages**
3. Note your **Team domain** (e.g. `your-company.cloudflareaccess.com`)
4. If you haven't set one up, you'll be prompted to create one

### Step 3.2 — Add Google as an Identity Provider

1. In Zero Trust dashboard → **Settings** → **Authentication** → **Login methods**
2. Click **Add new** → Select **Google**
3. Enter:
   | Field | Value |
   |-------|-------|
   | Client ID | From Step 2.3 |
   | Client Secret | From Step 2.3 |
4. Click **Save**
5. Click **Test** to verify the connection works

### Step 3.3 — Create an Access Application

1. Go to **Access** → **Applications** → **Add an application**
2. Select **Self-hosted**
3. Configure:
   | Field | Value |
   |-------|-------|
   | Application name | `{Project} Admin` (e.g. `FFC Admin`) |
   | Session duration | `24 hours` (or preference) |
   | Subdomain | `admin` |
   | Domain | `example.com` |
4. Click **Next**

### Step 3.4 — Create an Access Policy

1. On the policy configuration screen:
   | Field | Value |
   |-------|-------|
   | Policy name | `Allowed Admins` |
   | Action | **Allow** |
   | Session duration | Same as application |
2. Under **Configure rules** → **Include**:
   - Selector: **Emails**
   - Value: Add each authorized email, one per line
3. Click **Next** → **Add application**

### Step 3.5 — Verify

1. Open `https://admin.example.com` in an **incognito window**
2. You should see the Cloudflare Access login page with a "Sign in with Google" button
3. Sign in with an authorized email — you should reach the admin page
4. Try with an unauthorized email — you should be blocked

---

## Phase 4: API Token for Agent Automation (Future-Proofing)

> This enables the agent to configure Access programmatically for future clients.

### Step 4.1 — Create a Cloudflare API Token

1. Go to **Cloudflare Dashboard** → **My Profile** → **API Tokens**
2. Click **Create Token**
3. Select **Create Custom Token**
4. Configure permissions:

   | Resource | Permission |
   |----------|-----------|
   | Account > Access: Organizations, Identity Providers, and Groups | Edit |
   | Account > Access: Apps and Policies | Edit |
   | Zone > Zone | Read |
   | Zone > DNS | Edit |
   | Zone > Workers Routes | Edit |

5. Under **Account Resources**: Select your account
6. Under **Zone Resources**: Select "All zones" or specific zones
7. Click **Continue to summary** → **Create Token**
8. **Copy the token immediately** — it won't be shown again

### Step 4.2 — Store the Token as a Wrangler Secret

```bash
# Store securely (not in wrangler.toml, which is committed to git)
# Option A: Environment variable
set CLOUDFLARE_API_TOKEN={your-token}

# Option B: .env file (add to .gitignore!)
echo CLOUDFLARE_API_TOKEN={your-token} > .env
```

### Step 4.3 — Verify Token Works

```bash
curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" ^
  -H "Authorization: Bearer {your-token}"
```

Should return `"status": "active"`.

---

## Quick Reference: Cloudflare Access API Endpoints

Once you have the API token, the agent can automate everything:

```bash
# List identity providers
GET /accounts/{account_id}/access/identity_providers

# Create an Access application
POST /accounts/{account_id}/access/apps

# Create an Access policy
POST /accounts/{account_id}/access/apps/{app_id}/policies

# Create a DNS record
POST /zones/{zone_id}/dns_records
```

---

## Checklist

- [ ] DNS record created for admin subdomain (proxied)
- [ ] Worker route added to `wrangler.toml` and deployed
- [ ] Google OAuth Client ID + Secret created
- [ ] Redirect URI set to `https://{team}.cloudflareaccess.com/cdn-cgi/access/callback`
- [ ] Google added as IdP in Zero Trust dashboard
- [ ] Self-hosted Access application created
- [ ] Access policy with authorized emails configured
- [ ] Login tested in incognito window
- [ ] API token created with Access permissions (for agent automation)
- [ ] Token stored securely (env var or .env, NOT in git)
