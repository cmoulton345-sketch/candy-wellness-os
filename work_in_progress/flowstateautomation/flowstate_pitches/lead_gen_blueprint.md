# FlowStateAI: Lead Generation Blueprint (NB, NS, PEI)

> **Objective:** Systematically identify and extract contact data for decision-makers in high-cash-flow verticals across the Maritimes.

## Core Strategy
We will not scrape the entire internet blindly. We will target the platforms where high-value businesses are forced to maintain accurate data: Google Maps (Google My Business), specialized association directories, and LinkedIn.

---

## 📍 Vertical 1: High-Volume Real Estate

### Target Profile
*   **Who:** Top-producing individual agents, boutique brokerage owners, and Team Leads. (Do not target brand-new agents; they have no budget and no volume to automate).
*   **Where:** NB (Moncton, Fredericton, Saint John), NS (Halifax, Dartmouth, Bedford), PEI (Charlottetown).

### Extraction Methods
1.  **The MLS / Realtor.ca Scrape:**
    *   *Search:* Go to Realtor.ca and search by city.
    *   *Filter:* Look for agents with 10+ active listings. These are the producers drowning in follow-ups.
    *   *Data:* Realtor.ca provides direct cell phone numbers and emails.
2.  **Google Maps Query:** `"Real Estate Agency [City, Province]"`
    *   *Target:* Look for boutique agencies (e.g., "Keller Williams [City]" or independent names) with 50+ reviews.
3.  **Provincial Associations:**
    *   Nova Scotia Association of Realtors (NSAR) member directory.
    *   New Brunswick Real Estate Association (NBREA).

---

## 💎 Vertical 2: High-End Med Spas & Private Clinics

### Target Profile
*   **Who:** Clinic Owners, Medical Directors, or Lead Coordinators at Botox clinics, laser centers, and private cosmetic dermatology practices.
*   **Where:** Urban centers and affluent suburbs in NB, NS, and PEI.

### Extraction Methods
1.  **Google Maps Deep Logic:**
    *   *Queries:* `"Medical Spa [City]"`, `"Laser Clinic [City]"`, `"Cosmetic Injectables [City]"`, `"Private Medical Clinic [City]"`.
    *   *Filter:* Must have a professional website and online booking system (this proves they are sophisticated enough to understand automation but likely using a clunky native system like Jane App).
2.  **Instagram Geotagging:**
    *   Search hashtags: `#HalifaxMedSpa`, `#MonctonBotox`, `#PEIAesthetics`.
    *   *Why:* Med spas live on Instagram. The link-in-bio usually goes straight to their booking page or the owner's direct contact.
3.  **The "Jane App" hack:**
    *   Search Google for: `site:janeapp.com "New Brunswick"` (or NS/PEI). This reveals exactly which clinics are using Jane App, allowing you to pitch specific integrations.

---

## 🛠️ Vertical 3: Automotive & RV Dealerships

### Target Profile
*   **Who:** Dealer Principals, General Managers (GMs), or Internet Sales Managers (ISMs).
*   **Where:** Across all three provinces, including rural areas for RV/Tractor dealers.

### Extraction Methods
1.  **Google Maps / AutoTrader:**
    *   *Queries:* `"RV Dealer [Province]"`, `"Used Car Dealership [City]"`, `"Powersports Dealer [Province]"`.
    *   *Filter:* Avoid massive corporate conglomerates (e.g., Steele Auto Group) initially. They have 2-year procurement cycles. Target independent dealerships with 50-200 cars on the lot. The owner is usually in the building.
2.  **Dealership Associations:**
    *   Nova Scotia Automobile Dealers Association.
    *   Recreational Vehicle Dealers Association (RVDA) of Canada (filter by Atlantic region).
3.  **LinkedIn Targeting:**
    *   *Search:* Job Title: `"General Manager" OR "Dealer Principal" OR "Internet Sales Manager" AND Location: "New Brunswick, Canada" (or NS/PEI).*

---

## 🚀 Execution: The Automated Scraping System
To avoid manual data entry, we can build an n8n workflow for you later that handles this automatically:

**The Proposed n8n "Lead Harvester" Workflow:**
1.  **Trigger:** A Google Sheets list of search queries (e.g., "Med Spa Halifax").
2.  **Action 1 (Scraping):** n8n hits the Google Places API (or a service like Phantombuster) to scrape the top 50 results for each query.
3.  **Action 2 (Enrichment):** n8n uses Hunter.io or Apollo.io API to find the owner's email address associated with the scraped website domain.
4.  **Action 3 (Storage):** n8n formats the data (Name, Business, Website, Email, Phone) and drops it perfectly into your CRM or Google Sheet, ready for your cold email sequences.
