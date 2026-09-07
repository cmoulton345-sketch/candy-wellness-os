# How to Run the Google Maps Lead Harvester

This guide will walk you through setting up and running the `google_maps_scraper.py` script to generate your lead lists for NB, NS, and PEI.

## Step 1: Get Your Free Google Places API Key
Google requires an API key to search Maps programmatically. You get a $200 free monthly credit, which is more than enough to scrape thousands of leads for free.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Sign in with your Google account.
3. Click the dropdown at the top left (next to the Google Cloud logo) and click **"New Project"**. Name it "FlowState Leads" and click Create.
4. Once the project is created, make sure it is selected in the top dropdown.
5. In the top search bar, search for **"Places API (New)"** and click on it.
6. Click the blue **"Enable"** button.
7. Note: Google will likely ask you to set up a Billing Account with a credit card if you haven't before. **You will not be charged** as long as you stay under the $200 free monthly tier (which equates to roughly 10,000 lead searches per month).
8. Once enabled, go to the left-hand menu -> **APIs & Services** -> **Credentials**.
9. Click **"+ Create Credentials"** at the top and select **"API Key"**.
10. Copy the long string of letters and numbers it generates.

## Step 2: Add the Key to the Script
1. Open the `google_maps_scraper.py` file in a text editor (like VS Code or Notepad).
2. Look for line 16: 
   `GOOGLE_PLACES_API_KEY = "YOUR_GOOGLE_API_KEY_HERE"`
3. Replace `"YOUR_GOOGLE_API_KEY_HERE"` with the key you just copied. Make sure to keep the key inside the quotation marks `" "`.
4. Save the file.

## Step 3: Customize Your Search Targets (Optional)
By default, I set up 4 initial searches in the script:
- "Medical Spa in Halifax, NS"
- "Laser Clinic in Moncton, NB"
- "RV Dealer in New Brunswick"
- "Real Estate Agency in Charlottetown, PEI"

If you want to search for different cities or different businesses, just change the text inside `SEARCH_QUERIES` on line 19 of the script.

## Step 4: Run the Script
1. Open PowerShell on your computer.
2. Navigate to the folder where the script is located:
   ```powershell
   cd C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\work_in_progress\flowstateautomation\flowstate_pitches
   ```
3. Run the script using Python:
   ```powershell
   python google_maps_scraper.py
   ```
4. The script will output its progress to the screen. You will see it searching Google, finding businesses, and then visiting their websites to attempt to scrape an email address.
5. Depending on how many queries you entered, it will take a few minutes to run so that it doesn't overwhelm the websites it visits.

## Step 5: View Your Leads
Once the script finishes, it will generate a new file in the exact same folder called **`flowstate_leads.csv`**.

You can open this file in Microsoft Excel, Google Sheets, or Apple Numbers. It will be perfectly formatted into columns covering:
- Search Query used
- Business Name
- Address
- Phone Number
- Website URL
- Scraped Email Address (if found)
- Google Map Rating (and total review count)

You can now use this list to import directly into your CRM or cold email outreach tool!
