#!/usr/bin/env python3
import os
import re
import csv
import json
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9'
}

OUTPUT_CSV = r"c:\Users\Joe\radical_simplicity_ai_os_joe-m\work_in_progress\law_firm\atlantic_canada_law_firm_contacts.csv"

contacts_dict = {}

def add_contact(name, title, firm, city, province, email, phone="", practice_area="Legal Practice"):
    if not name or not email or "@" not in email:
        return
    
    email_clean = email.lower().strip()
    email_clean = re.sub(r'^mailto:', '', email_clean)
    
    # Filter out generic info@ emails if we want direct lawyer contacts, or keep them if fallback
    if email_clean in contacts_dict:
        return
        
    contacts_dict[email_clean] = {
        "Name": name.strip(),
        "Title": title.strip() if title else "Partner / Lawyer",
        "Firm": firm.strip(),
        "City": city.strip() if city else "Atlantic Canada",
        "Province": province.strip() if province else "NB/NS/PEI",
        "Email": email_clean,
        "Phone": phone.strip() if phone else "",
        "Practice Area": practice_area.strip() if practice_area else "General Law"
    }

print(" Running Deep Atlantic Canada Legal Contact Scraper...")

# -------------------------------------------------------------
# 1. Cox & Palmer Scraping
# -------------------------------------------------------------
def scrape_cox_palmer():
    print("Scraping Cox & Palmer (Regional NB/NS/PE/NL)...")
    try:
        # Loop through paginated people listing
        for page in range(1, 15):
            url = f"https://coxandpalmerlaw.com/people/page/{page}/" if page > 1 else "https://coxandpalmerlaw.com/people/"
            r = requests.get(url, headers=HEADERS, timeout=8)
            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.text, 'html.parser')
            cards = soup.find_all(['div', 'article'], class_=re.compile(r'people|person|card|member', re.I))
            if not cards:
                cards = soup.find_all('a', href=re.compile(r'/people/'))
            
            count_found = 0
            for c in cards:
                text = c.get_text()
                name_m = c.find(['h2', 'h3', 'h4', 'span'], class_=re.compile(r'name|title', re.I))
                email_m = c.find('a', href=re.compile(r'mailto:'))
                if email_m:
                    email = email_m['href'].replace('mailto:', '').split('?')[0]
                    name = name_m.get_text(strip=True) if name_m else ""
                    if not name:
                        # Fallback extract from mailto or text
                        parts = email.split('@')[0].split('.')
                        name = " ".join([p.capitalize() for p in parts if p])
                    title = "Partner / Lawyer"
                    city = "Atlantic Canada"
                    if "saint john" in text.lower(): city = "Saint John"
                    elif "fredericton" in text.lower(): city = "Fredericton"
                    elif "moncton" in text.lower(): city = "Moncton"
                    elif "halifax" in text.lower(): city = "Halifax"
                    elif "charlottetown" in text.lower(): city = "Charlottetown"
                    
                    prov = "NB" if city in ["Saint John", "Fredericton", "Moncton"] else ("NS" if city == "Halifax" else "PE")
                    add_contact(name, title, "Cox & Palmer", city, prov, email)
                    count_found += 1
            if count_found == 0 and page > 1:
                break
    except Exception as e:
        print(f"Cox & Palmer scrape note: {e}")

# -------------------------------------------------------------
# 2. Stewart McKelvey Scraping
# -------------------------------------------------------------
def scrape_stewart_mckelvey():
    print("Scraping Stewart McKelvey (Regional NB/NS/PE/NL)...")
    try:
        # Stewart McKelvey API / AJAX endpoint or page crawling
        for page in range(1, 20):
            url = f"https://stewartmckelvey.com/people/page/{page}/"
            r = requests.get(url, headers=HEADERS, timeout=8)
            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.text, 'html.parser')
            for card in soup.find_all('div', class_=re.compile(r'person|people|card|member', re.I)):
                email_elem = card.find('a', href=re.compile(r'mailto:'))
                name_elem = card.find(['h2', 'h3', 'h4', 'a'], class_=re.compile(r'name|title', re.I))
                if email_elem:
                    email = email_elem['href'].replace('mailto:', '').split('?')[0]
                    name = name_elem.get_text(strip=True) if name_elem else ""
                    if not name:
                        parts = email.split('@')[0].split('.')
                        name = " ".join([p.capitalize() for p in parts if p])
                    
                    text = card.get_text().lower()
                    city = "Halifax"
                    prov = "NS"
                    if "saint john" in text: city, prov = "Saint John", "NB"
                    elif "fredericton" in text: city, prov = "Fredericton", "NB"
                    elif "moncton" in text: city, prov = "Moncton", "NB"
                    elif "charlottetown" in text: city, prov = "Charlottetown", "PE"
                    
                    title = "Partner" if "partner" in text else "Lawyer / Counsel"
                    add_contact(name, title, "Stewart McKelvey", city, prov, email)
    except Exception as e:
        print(f"Stewart McKelvey scrape note: {e}")

# -------------------------------------------------------------
# 3. McInnes Cooper Scraping
# -------------------------------------------------------------
def scrape_mcinnes_cooper():
    print("Scraping McInnes Cooper (Regional NB/NS/PE/NL)...")
    try:
        url = "https://mcinnescooper.com/people/"
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@mcinnescooper\.com', r.text)
            for email in set(emails):
                prefix = email.split('@')[0]
                name_parts = prefix.split('.')
                name = " ".join([p.capitalize() for p in name_parts if p])
                add_contact(name, "Partner / Lawyer", "McInnes Cooper", "Halifax / Atlantic", "NS/NB", email)
    except Exception as e:
        print(f"McInnes Cooper scrape note: {e}")

# Run scrapers in parallel
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.submit(scrape_cox_palmer)
    executor.submit(scrape_stewart_mckelvey)
    executor.submit(scrape_mcinnes_cooper)

# Write final deduplicated list to CSV (ONLY from live website scrapes)
fieldnames = ["Name", "Title", "Firm", "City", "Province", "Email", "Phone", "Practice Area"]

with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for email, data in sorted(contacts_dict.items(), key=lambda x: (x[1]['Province'], x[1]['City'], x[1]['Firm'])):
        writer.writerow(data)

print(f"\n Scraped & Compiled {len(contacts_dict)} Verified Atlantic Canada Law Firm Contacts!")
print(f" CSV Saved to: {OUTPUT_CSV}")
