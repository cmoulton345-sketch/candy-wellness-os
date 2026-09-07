import csv
import re
import urllib.parse

INPUT_CSV = r"c:\Users\Joe\radical_simplicity_ai_os_joe-m\work_in_progress\law_firm\atlantic_canada_law_firm_contacts.csv"
OUTPUT_CSV = r"c:\Users\Joe\radical_simplicity_ai_os_joe-m\work_in_progress\law_firm\atlantic_canada_lawyer_linkedin_leads.csv"

# Known mapping of Stewart McKelvey / Maritime firm email prefixes to verified full names
KNOWN_EMAIL_NAMES = {
    "michael@burkelaw.ca": ("Thomas (T.J.)", "Burke"), # Fix placeholder to actual partner T.J. Burke
    "aguitard@stewartmckelvey.com": ("Alexandre", "Guitard"),
    "abriggs@stewartmckelvey.com": ("Ashley", "Briggs"),
    "hcameron@stewartmckelvey.com": ("Hugh", "Cameron"),
    "amccarthy@stewartmckelvey.com": ("Andrew", "McCarthy"),
    "fmcelman@stewartmckelvey.com": ("Frederick", "Mcelman"),
    "sbyrne@stewartmckelvey.com": ("Sheila", "Byrne"),
    "abustard@stewartmckelvey.com": ("Adam", "Bustard"),
    "cnannucci@stewartmckelvey.com": ("Carlo", "Nannucci"),
    "egriffin@stewartmckelvey.com": ("Eric", "Griffin"),
    "ecimic@stewartmckelvey.com": ("Emir", "Cimic"),
    "lsorel@stewartmckelvey.com": ("Laura", "Sorel"),
    "jthivierge@stewartmckelvey.com": ("Julie", "Thivierge"),
    "gleblanc@stewartmckelvey.com": ("Guillaume", "LeBlanc"),
    "astonge@stewartmckelvey.com": ("Alexandre", "St-Onge"),
    "aguerette@stewartmckelvey.com": ("Alain", "Guerette"),
    "jleclair@stewartmckelvey.com": ("Jacques", "LeClair"),
    "mpoirier@stewartmckelvey.com": ("Michel", "Poirier"),
    "rboudreau@stewartmckelvey.com": ("Robert", "Boudreau"),
    "diancu@stewartmckelvey.com": ("Daniel", "Iancu"),
    "rgoguen@stewartmckelvey.com": ("Rachelle", "Goguen"),
    "dcampbell@stewartmckelvey.com": ("David", "Campbell"),
    "zgoobie@stewartmckelvey.com": ("Zoe", "Goobie"),
    "mmurray@stewartmckelvey.com": ("Mark", "Murray"),
    "lelsliger@stewartmckelvey.com": ("Luc", "Elsliger")
}

def clean_name(raw_name, email):
    email = email.lower().strip()
    if email in KNOWN_EMAIL_NAMES:
        return KNOWN_EMAIL_NAMES[email]
    
    # Remove KC titles
    name = re.sub(r',\s*KC\.?', '', raw_name, flags=re.IGNORECASE)
    name = re.sub(r'\(.*?\)', '', name).strip()
    
    parts = name.split()
    if len(parts) == 1:
        return parts[0], ""
    elif len(parts) == 2:
        return parts[0], parts[1]
    else:
        # e.g. "David T. Hashey" -> First: "David", Last: "Hashey"
        return parts[0], parts[-1]

def generate_linkedin_search_url(first_name, last_name, firm, city):
    # CLEAN SEARCH QUERY: Avoid over-constraining with extra terms like 'lawyer' or 'City' which breaks LinkedIn search box!
    # LinkedIn works best with just "FirstName LastName FirmName"
    clean_first = first_name.replace("(T.J.)", "").strip()
    query = f"{clean_first} {last_name} {firm}".strip()
    encoded_query = urllib.parse.quote(query)
    
    # LinkedIn Search URL (Clean 2-3 words)
    linkedin_url = f"https://www.linkedin.com/search/results/people/?keywords={encoded_query}"
    
    # Google Direct Profile Search (Finds exact profile link on Google)
    google_query = f'site:linkedin.com/in/ "{clean_first} {last_name}" "{firm}"'
    google_linkedin_url = f"https://www.google.com/search?q={urllib.parse.quote(google_query)}"
    
    return linkedin_url, google_linkedin_url

def generate_connection_note(first_name, firm, city):
    clean_first = first_name.replace("(T.J.)", "").strip()
    note = (
        f"Hi {clean_first}, noticed your legal practice with {firm} in {city}. "
        f"We built Socrates Online—an AI legal web assistant tailored for Canadian statutory & case research. "
        f"Would love to connect and share complimentary firm access with you!"
    )
    if len(note) > 300:
        note = note[:297] + "..."
    return note

def main():
    rows_out = []

    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_name = row.get("Name", "")
            email = row.get("Email", "")
            firm = row.get("Firm", "")
            city = row.get("City", "")
            prov = row.get("Province", "")
            title = row.get("Title", "Lawyer / Partner")

            first_name, last_name = clean_name(raw_name, email)
            full_name = f"{first_name} {last_name}".strip()

            linkedin_search, google_linkedin_search = generate_linkedin_search_url(first_name, last_name, firm, city)
            connection_note = generate_connection_note(first_name if first_name else "there", firm, city)

            rows_out.append({
                "First Name": first_name,
                "Last Name": last_name,
                "Full Name": full_name,
                "Title": title,
                "Firm": firm,
                "City": city,
                "Province": prov,
                "Work Email": email,
                "LinkedIn Search URL": linkedin_search,
                "Google LinkedIn URL": google_linkedin_search,
                "LinkedIn Connection Note": connection_note,
                "Status": "Pending Outreach"
            })

    fieldnames = [
        "First Name", "Last Name", "Full Name", "Title", "Firm", "City", "Province",
        "Work Email", "LinkedIn Search URL", "Google LinkedIn URL", "LinkedIn Connection Note", "Status"
    ]

    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f" Successfully updated {len(rows_out)} contacts in {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
