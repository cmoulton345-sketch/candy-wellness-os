import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import time
import csv
import json
import urllib.parse
import urllib.request
import re

# ==========================================
# FLOWSTATE AI - GOOGLE PLACES LEAD HARVESTER
# ==========================================
# Scrapes Google Maps for Real Estate, Medical, and Auto/RV businesses
# across New Brunswick, Nova Scotia, and PEI.
# Exports to CSV and optionally to Google Sheets.

# ==========================================
# CONFIGURATION - FILL THESE IN
# ==========================================

# 1. Google Places API Key
#    Get one: console.cloud.google.com -> Enable "Places API (New)" -> Credentials -> Create API Key
GOOGLE_PLACES_API_KEY = "AIzaSyDT8sdRT2LYCRroqQGjmxE4tnOzMenyv64"

# 2. Google Sheets Export (optional but recommended)
#    To use: create a Google Sheet, share it with your service account email,
#    install gspread: pip install gspread google-auth
#    Then paste your service account JSON key file path below.
GOOGLE_SHEETS_ENABLED = False
GOOGLE_SHEETS_KEY_FILE = "service_account.json"   # Path to your service account JSON
GOOGLE_SHEET_NAME = "FlowState AI Leads"           # Must match the exact sheet name in Google Drive

# 3. Output CSV file
OUTPUT_CSV = "flowstate_leads.csv"

# ==========================================
# SEARCH QUERIES - Atlantic Canada
# ==========================================
SEARCH_QUERIES = [

    # --- REAL ESTATE ---
    "Real Estate Agency in Moncton, New Brunswick",
    "Real Estate Agency in Fredericton, New Brunswick",
    "Real Estate Agency in Saint John, New Brunswick",
    "Real Estate Agency in Halifax, Nova Scotia",
    "Real Estate Agency in Dartmouth, Nova Scotia",
    "Real Estate Agency in Sydney, Nova Scotia",
    "Real Estate Agency in Charlottetown, PEI",
    "Real Estate Agency in Summerside, PEI",
    "Realtor in Moncton, NB",
    "Realtor in Halifax, NS",

    # --- HIGH-END MEDICAL / CLINICS ---
    "Medical Spa in Moncton, New Brunswick",
    "Medical Spa in Fredericton, New Brunswick",
    "Medical Spa in Halifax, Nova Scotia",
    "Medical Spa in Dartmouth, Nova Scotia",
    "Medical Spa in Charlottetown, PEI",
    "Laser Clinic in Moncton, NB",
    "Laser Clinic in Halifax, NS",
    "Aesthetic Clinic in New Brunswick",
    "Cosmetic Clinic in Nova Scotia",
    "Chiropractic Clinic in Moncton, NB",
    "Private Health Clinic in Halifax, NS",
    "Dental Clinic in Moncton, NB",
    "Dental Clinic in Halifax, NS",

    # --- AUTOMOTIVE / RECREATIONAL VEHICLES ---
    "Car Dealership in Moncton, New Brunswick",
    "Car Dealership in Fredericton, New Brunswick",
    "Car Dealership in Saint John, New Brunswick",
    "Car Dealership in Halifax, Nova Scotia",
    "Car Dealership in Charlottetown, PEI",
    "Used Car Dealership in Moncton, NB",
    "Used Car Dealership in Halifax, NS",
    "RV Dealer in New Brunswick",
    "RV Dealer in Nova Scotia",
    "RV Dealer in Prince Edward Island",
    "Recreational Vehicle Dealer in Moncton, NB",
    "ATV Dealer in New Brunswick",
    "Motorcycle Dealership in Halifax, NS",
    "Truck Dealership in Moncton, NB",
    "Auto Group in Atlantic Canada",
]


# ==========================================
# GOOGLE PLACES API
# ==========================================

def search_google_places(query):
    """Hits the Google Places API text search endpoint."""
    print(f"\n🔍 Searching: '{query}'...")

    url = "https://places.googleapis.com/v1/places:searchText"

    payload = json.dumps({
        "textQuery": query,
        "languageCode": "en"
    }).encode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': GOOGLE_PLACES_API_KEY,
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.websiteUri,places.nationalPhoneNumber,places.rating,places.userRatingCount'
    }

    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get('places', [])
    except urllib.error.HTTPError as e:
        print(f"❌ Google API Error: {e.code} - {e.reason}")
        error_body = e.read().decode()
        print(error_body)
        if e.code == 403:
            print("   -> Tip: Check your API key and that 'Places API (New)' is enabled.")
        return []
    except Exception as e:
        print(f"❌ Failed to reach Google API: {e}")
        return []


# ==========================================
# EMAIL SCRAPER
# ==========================================

def scrape_email_from_website(website_url):
    """Scans a business homepage for contact email addresses."""
    if not website_url:
        return ""

    print(f"   🌐 Scanning {website_url} for emails...")
    try:
        req = urllib.request.Request(
            website_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=6) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            emails = re.findall(r'[a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+\.[a-zA-Z]{2,}', html_content)
            valid_emails = [e for e in emails if not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'))]
            if valid_emails:
                found = list(set(valid_emails))[0]
                print(f"   ✉️  Found: {found}")
                return found
    except Exception:
        pass

    return ""


# ==========================================
# GOOGLE SHEETS EXPORT
# ==========================================

def push_to_google_sheets(leads):
    """Pushes all collected leads to a Google Sheet."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        print("\n⚠️  gspread not installed. Run: pip install gspread google-auth")
        print("   Skipping Google Sheets export.\n")
        return

    print("\n📊 Pushing leads to Google Sheets...")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    try:
        creds = Credentials.from_service_account_file(GOOGLE_SHEETS_KEY_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open(GOOGLE_SHEET_NAME).sheet1

        # Write header row if sheet is empty
        if sheet.row_count == 0 or sheet.cell(1, 1).value is None:
            sheet.append_row(["Search Query", "Business Name", "Address", "Phone", "Website", "Scraped Email", "Google Rating"])

        # Write all leads
        rows = []
        for lead in leads:
            rows.append([
                lead["Search Query"],
                lead["Business Name"],
                lead["Address"],
                lead["Phone"],
                lead["Website"],
                lead["Scraped Email"],
                lead["Google Rating"]
            ])

        sheet.append_rows(rows)
        print(f"   ✅ {len(rows)} leads pushed to Google Sheet: '{GOOGLE_SHEET_NAME}'")

    except FileNotFoundError:
        print(f"   ❌ Service account key file not found: {GOOGLE_SHEETS_KEY_FILE}")
        print("   Download it from Google Cloud -> IAM -> Service Accounts -> Keys -> Add Key -> JSON")
    except Exception as e:
        print(f"   ❌ Google Sheets error: {e}")


# ==========================================
# MAIN
# ==========================================

def main():
    if GOOGLE_PLACES_API_KEY == "YOUR_GOOGLE_API_KEY_HERE":
        print("\n🛑 ERROR: Insert your Google Places API Key at the top of the script.")
        print("Get one at: console.cloud.google.com -> Places API (New) -> Credentials")
        return

    print("=" * 50)
    print("🚀 FLOWSTATE AI LEAD HARVESTER - ATLANTIC CANADA")
    print("=" * 50)
    print(f"   Industries: Real Estate | Medical | Auto & RV")
    print(f"   Regions:    NB | NS | PEI")
    print(f"   Queries:    {len(SEARCH_QUERIES)}")
    print("=" * 50)

    all_leads = []
    seen = set()  # Deduplicate by business name + address

    for query in SEARCH_QUERIES:
        places = search_google_places(query)
        print(f"   ✅ {len(places)} results.")

        for place in places:
            name = place.get('displayName', {}).get('text', 'N/A')
            address = place.get('formattedAddress', 'N/A')
            dedup_key = f"{name}|{address}"

            if dedup_key in seen:
                continue
            seen.add(dedup_key)

            phone = place.get('nationalPhoneNumber', 'N/A')
            website = place.get('websiteUri', '')
            rating = f"{place.get('rating', 'N/A')} ({place.get('userRatingCount', 0)} reviews)"
            email = scrape_email_from_website(website)

            # Detect industry from query
            q_lower = query.lower()
            if any(x in q_lower for x in ['real estate', 'realtor']):
                industry = "Real Estate"
            elif any(x in q_lower for x in ['rv', 'recreational', 'car dealer', 'used car', 'atv', 'motorcycle', 'truck', 'auto']):
                industry = "Automotive / RV"
            else:
                industry = "Medical / Clinic"

            lead = {
                "Industry": industry,
                "Search Query": query,
                "Business Name": name,
                "Address": address,
                "Phone": phone,
                "Website": website,
                "Scraped Email": email,
                "Google Rating": rating
            }
            all_leads.append(lead)
            time.sleep(0.5)

    if not all_leads:
        print("\n⚠️  No leads found. Check your API key and queries.")
        return

    # --- CSV Export ---
    print(f"\n💾 Saving {len(all_leads)} leads to {OUTPUT_CSV}...")
    fieldnames = ["Industry", "Search Query", "Business Name", "Address", "Phone", "Website", "Scraped Email", "Google Rating"]

    with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_leads)

    print(f"   ✅ CSV saved: {OUTPUT_CSV}")

    # --- Google Sheets Export ---
    if GOOGLE_SHEETS_ENABLED:
        push_to_google_sheets(all_leads)

    print(f"\n🎯 DONE. {len(all_leads)} unique leads collected across {len(SEARCH_QUERIES)} searches.")
    print(f"   Breakdown by industry:")
    for ind in ["Real Estate", "Medical / Clinic", "Automotive / RV"]:
        count = sum(1 for l in all_leads if l["Industry"] == ind)
        print(f"   - {ind}: {count} leads")


if __name__ == "__main__":
    main()
