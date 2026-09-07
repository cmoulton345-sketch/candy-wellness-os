import csv
import html
import json
import os

CSV_FILE = r"c:\Users\Joe\radical_simplicity_ai_os_joe-m\work_in_progress\law_firm\atlantic_canada_lawyer_linkedin_leads.csv"
HTML_OUTPUT = r"c:\Users\Joe\radical_simplicity_ai_os_joe-m\work_in_progress\law_firm\linkedin_outreach_dashboard.html"
MD_OUTPUT = r"c:\Users\Joe\radical_simplicity_ai_os_joe-m\work_in_progress\law_firm\linkedin_outreach_guide.md"

def main():
    leads = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            leads.append(r)

    # -------------------------------------------------------------
    # 1. GENERATE HTML DASHBOARD FOR DUAL-SCREEN WORKSPACE
    # -------------------------------------------------------------
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkedIn Legal Outreach Command Center — FlowstateAI</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
            --card-border: #334155;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-blue: #38bdf8;
            --accent-indigo: #818cf8;
            --accent-green: #34d399;
            --accent-gold: #fbbf24;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            line-height: 1.5;
            padding-bottom: 60px;
        }}
        
        /* STICKY HEADER & SCRIPTS */
        header {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--card-border);
            padding: 16px 24px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5);
        }}
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        .brand-title {{
            font-size: 1.25rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-indigo));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .badge {{
            background: #0369a1;
            color: #e0f2fe;
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 600;
        }}
        
        /* QUICK SCRIPT CARDS */
        .scripts-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 10px;
        }}
        .script-box {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 12px;
            position: relative;
        }}
        .script-title {{
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--accent-blue);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
            display: flex;
            justify-content: space-between;
        }}
        .script-text {{
            font-size: 0.85rem;
            color: #cbd5e1;
            font-family: 'Inter', sans-serif;
            white-space: pre-wrap;
        }}
        .copy-btn {{
            background: #334155;
            color: #f8fafc;
            border: 1px solid #475569;
            border-radius: 4px;
            padding: 3px 8px;
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .copy-btn:hover {{
            background: var(--accent-blue);
            color: #0f172a;
            font-weight: 600;
        }}
        
        /* CONTROLS & FILTERS */
        .controls {{
            max-width: 1400px;
            margin: 20px auto 10px auto;
            padding: 0 24px;
            display: flex;
            gap: 12px;
            align-items: center;
            flex-wrap: wrap;
        }}
        .search-input {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            color: #fff;
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 0.9rem;
            width: 280px;
        }}
        .filter-btn {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            color: var(--text-muted);
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 0.85rem;
            cursor: pointer;
            font-weight: 500;
        }}
        .filter-btn.active {{
            background: #0284c7;
            color: #fff;
            border-color: #0369a1;
        }}
        .stats-counter {{
            margin-left: auto;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}

        /* LEADS CONTAINER */
        .leads-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 10px 24px;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            gap: 16px;
        }}
        
        .lead-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 10px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }}
        .lead-card:hover {{
            border-color: var(--accent-blue);
            transform: translateY(-2px);
        }}
        .lead-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 8px;
        }}
        .lead-name {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #f8fafc;
        }}
        .lead-firm {{
            font-size: 0.85rem;
            color: var(--accent-indigo);
            font-weight: 600;
        }}
        .lead-meta {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 12px;
        }}
        .lead-note-box {{
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 10px;
            font-size: 0.82rem;
            color: #e2e8f0;
            margin-bottom: 12px;
            position: relative;
        }}
        .actions-row {{
            display: flex;
            gap: 8px;
            align-items: center;
            margin-top: auto;
        }}
        .btn-linkedin {{
            background: #0077b5;
            color: white;
            text-decoration: none;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: background 0.2s;
        }}
        .btn-linkedin:hover {{
            background: #005582;
        }}
        .btn-google {{
            background: #334155;
            color: #cbd5e1;
            text-decoration: none;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 0.78rem;
        }}
        .btn-google:hover {{
            background: #475569;
            color: white;
        }}
        .status-toggle {{
            margin-left: auto;
            background: #1e293b;
            border: 1px solid #475569;
            color: #94a3b8;
            font-size: 0.75rem;
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
        }}
        .status-toggle.sent {{
            background: #166534;
            color: #86efac;
            border-color: #22c55e;
        }}
        
        .toast {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--accent-green);
            color: #0f172a;
            font-weight: 700;
            padding: 10px 18px;
            border-radius: 8px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            display: none;
            z-index: 1000;
        }}
    </style>
</head>
<body>

    <header>
        <div class="header-top">
            <div class="brand-title">
                ⚖️ FlowstateAI — Legal LinkedIn Outreach Command Center
                <span class="badge">{len(leads)} Enriched Maritime Leads</span>
            </div>
            <div style="font-size: 0.85rem; color: var(--text-muted);">
                Dual-Screen Workflow: Keep this on Screen 2 while sending on LinkedIn (Screen 1)
            </div>
        </div>

        <div class="scripts-grid">
            <div class="script-box">
                <div class="script-title">
                    1️⃣ Default Connection Note (&lt; 300 Chars)
                    <button class="copy-btn" onclick="copyText('script1')">Copy Master Note</button>
                </div>
                <div class="script-text" id="script1">Hi [First Name], noticed your legal practice with [Firm] in [City]. We built Socrates Online—an AI legal web assistant tailored for Canadian statutory & case research. Would love to connect and share complimentary firm access with you!</div>
            </div>

            <div class="script-box">
                <div class="script-title">
                    2️⃣ Post-Acceptance Follow-Up Message
                    <button class="copy-btn" onclick="copyText('script2')">Copy Follow-Up</button>
                </div>
                <div class="script-text" id="script2">Thanks for connecting, [First Name]! As mentioned, we gave local Maritime fee-earners 25 complimentary research/drafting queries on Socrates. You can try it instantly with your work email here: https://socrates-flowstate.pages.dev (zero credit card or setup needed). Would love your feedback!</div>
            </div>
        </div>
    </header>

    <div class="controls">
        <input type="text" id="searchInput" class="search-input" placeholder="Search lawyer name, firm, city..." onkeyup="filterLeads()">
        <button class="filter-btn active" onclick="setCityFilter('ALL', this)">All ({len(leads)})</button>
        <button class="filter-btn" onclick="setCityFilter('Fredericton', this)">Fredericton</button>
        <button class="filter-btn" onclick="setCityFilter('Moncton', this)">Moncton</button>
        <button class="filter-btn" onclick="setCityFilter('Saint John', this)">Saint John</button>
        <button class="filter-btn" onclick="setCityFilter('Halifax', this)">Halifax</button>

        <div class="stats-counter" id="statsDisplay">
            Showing {len(leads)} leads | 0 Invites Sent
        </div>
    </div>

    <div class="leads-container" id="leadsContainer">
"""

    for idx, lead in enumerate(leads):
        fname = html.escape(lead.get('First Name', ''))
        lname = html.escape(lead.get('Last Name', ''))
        fullname = html.escape(lead.get('Full Name', ''))
        title = html.escape(lead.get('Title', 'Lawyer'))
        firm = html.escape(lead.get('Firm', ''))
        city = html.escape(lead.get('City', ''))
        email = html.escape(lead.get('Work Email', ''))
        note = html.escape(lead.get('LinkedIn Connection Note', ''))
        linkedin_url = lead.get('LinkedIn Search URL', '#')
        google_url = lead.get('Google LinkedIn URL', '#')

        html_content += f"""
        <div class="lead-card" data-city="{city}" data-search="{fullname.lower()} {firm.lower()} {city.lower()}">
            <div>
                <div class="lead-header">
                    <div>
                        <div class="lead-name">{fullname}</div>
                        <div class="lead-firm">{firm}</div>
                    </div>
                    <span class="badge" style="background:#334155;">{city}</span>
                </div>
                <div class="lead-meta">👔 {title} {f'• 📧 {email}' if email else ''}</div>
                <div class="lead-note-box">
                    <div style="font-size:0.7rem; color:var(--accent-blue); font-weight:600; margin-bottom:4px; display:flex; justify-content:space-between;">
                        <span>CUSTOMIZED CONNECTION NOTE</span>
                        <a href="javascript:void(0)" onclick="copyText('note_{idx}')" style="color:var(--accent-blue); text-decoration:none;">📋 Copy</a>
                    </div>
                    <span id="note_{idx}">{note}</span>
                </div>
            </div>
            <div class="actions-row">
                <a href="{linkedin_url}" target="_blank" class="btn-linkedin">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
                    LinkedIn Search
                </a>
                <a href="{google_url}" target="_blank" class="btn-google">🔍 Google Profile</a>
                <button class="status-toggle" onclick="toggleStatus(this)">[ ] Sent Invite</button>
            </div>
        </div>
        """

    html_content += """
    </div>

    <div class="toast" id="toast">Copied to clipboard!</div>

    <script>
        let currentCity = 'ALL';
        let sentCount = 0;

        function copyText(elementId) {
            const text = document.getElementById(elementId).innerText;
            navigator.clipboard.writeText(text).then(() => {
                showToast("Copied script to clipboard!");
            });
        }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            toast.innerText = msg;
            toast.style.display = 'block';
            setTimeout(() => { toast.style.display = 'none'; }, 2000);
        }

        function toggleStatus(btn) {
            if (btn.classList.contains('sent')) {
                btn.classList.remove('sent');
                btn.innerText = '[ ] Sent Invite';
                sentCount--;
            } else {
                btn.classList.add('sent');
                btn.innerText = '✅ Sent Invite';
                sentCount++;
            }
            updateStats();
        }

        function setCityFilter(city, btn) {
            currentCity = city;
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterLeads();
        }

        function filterLeads() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.lead-card');
            let visibleCount = 0;

            cards.forEach(card => {
                const cardCity = card.getAttribute('data-city');
                const cardSearch = card.getAttribute('data-search');
                
                const matchesCity = (currentCity === 'ALL' || cardCity.toLowerCase().includes(currentCity.toLowerCase()));
                const matchesSearch = (!query || cardSearch.includes(query));

                if (matchesCity && matchesSearch) {
                    card.style.display = 'flex';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            updateStats(visibleCount);
        }

        function updateStats(visibleCount) {
            const container = document.querySelectorAll('.lead-card');
            const totalVisible = visibleCount !== undefined ? visibleCount : container.length;
            document.getElementById('statsDisplay').innerText = `Showing ${totalVisible} leads | ${sentCount} Invites Sent`;
        }
    </script>
</body>
</html>
"""

    with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f" Created Dual-Screen HTML Dashboard: {HTML_OUTPUT}")

    # -------------------------------------------------------------
    # 2. GENERATE MARKDOWN GUIDE FOR IDE ARTIFACT / SIDEBAR
    # -------------------------------------------------------------
    md_content = f"""# ⚖️ Atlantic Canada Legal LinkedIn Outreach Guide

> **Purpose:** Side-by-side reference guide for LinkedIn outreach. Keep this open on one monitor while executing outreach on your main display.

---

## 📜 Master Outreach Scripts

### 1️⃣ Connection Request Note (< 300 Characters)
```text
Hi [First Name], noticed your legal practice with [Firm] in [City]. We built Socrates Online—an AI legal web assistant tailored for Canadian statutory & case research. Would love to connect and share complimentary firm access with you!
```

### 2️⃣ Post-Acceptance Follow-Up Message
```text
Thanks for connecting, [First Name]! As mentioned, we gave local Maritime fee-earners 25 complimentary research/drafting queries on Socrates. You can try it instantly with your work email here: https://socrates-flowstate.pages.dev (zero credit card or setup needed). Would love your feedback!
```

---

## 📋 Master Lead Directory ({len(leads)} Contacts)

"""

    # Group by City
    cities = {}
    for lead in leads:
        c = lead.get('City', 'Other Atlantic Canada')
        if c not in cities:
            cities[c] = []
        cities[c].append(lead)

    for city_name, city_leads in sorted(cities.items()):
        md_content += f"### 📍 {city_name} ({len(city_leads)} Leads)\n\n"
        for l in city_leads:
            fn = l.get('First Name', '')
            ln = l.get('Last Name', '')
            firm = l.get('Firm', '')
            title = l.get('Title', 'Lawyer')
            email = l.get('Work Email', '')
            note = l.get('LinkedIn Connection Note', '')
            li_url = l.get('LinkedIn Search URL', '#')
            g_url = l.get('Google LinkedIn URL', '#')

            md_content += f"#### **{fn} {ln}** — {title} at **{firm}**\n"
            md_content += f"- **City:** {city_name} | **Email:** `{email}`\n"
            md_content += f"- **Search Links:** [🔗 LinkedIn Search]({li_url}) | [🔍 Google Profile Search]({g_url})\n"
            md_content += f"- **Custom Note:**\n```text\n{note}\n```\n"
            md_content += f"- **Status:** `[ ] Pending Invite`\n\n"
            md_content += "---\n\n"

    with open(MD_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f" Created Markdown Guide: {MD_OUTPUT}")

if __name__ == "__main__":
    main()
