import csv
import smtplib
import time
import random
import os
from email.message import EmailMessage

# ==========================================
# CONFIGURATION
# ==========================================
# Your Email Provider Settings (e.g. Gmail)
SMTP_SERVER = "smtp.gmail.com"  # Change if using Outlook (smtp.office365.com)
SMTP_PORT = 465                 # 465 for SSL, 587 for TLS
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "joe@flowstateaiautomation.ai")
# If your flowstate email is an alias on your personal Gmail, put your personal Gmail here:
LOGIN_EMAIL = "joemoulton2022@gmail.com"
# ⚠️ IMPORTANT: Use an App Password, not your real login password!
SENDER_APP_PASSWORD = os.environ.get("SENDER_APP_PASSWORD", "vhtp lbry ofce xfrf").replace(" ", "")

CSV_FILE = "sj_batch_1.csv"

# Set to True to send ONE test email to yourself before blasting 200+ people
TEST_MODE = True
TEST_EMAIL_ADDRESS = "joe@flowstateaiautomation.ai"

# ==========================================
# EMAIL TEMPLATE
# ==========================================
SUBJECT_TEMPLATE = "Local AI Support for {firm_name} / Complimentary Access to Socrates"

def get_email_body(first_name, firm_name):
    return f"""Hi {first_name},

I’m Joe Moulton, founder of FlowstateAI—an AI automation company based right here in Saint John. 

I know your inbox is probably flooded with generic software pitches from Silicon Valley, but I'm reaching out locally. We’re currently partnering with Maritime law firms to help them navigate the messy world of AI adoption securely, and I'd love to help {firm_name} stay ahead of the curve.

To help your team evaluate practical legal AI without the privacy risks, I want to give the fee-earners at {firm_name} complimentary access to Socrates Online—a web assistant we engineered specifically for Canadian case law, statutory analysis, and document drafting.

How your team can try it out:
1. Visit https://socrates-flowstate.pages.dev
2. Enter your work email for an instant access pass.
3. Enjoy 25 free research/drafting queries per fee-earner.

(Zero obligation, no credit card required, and absolutely no exposure or risk to your firm's data.)

Since we're both right here in the city, I would love to offer your firm a complimentary 30-minute internal Lunch & Learn on practical AI adoption and keeping client data safe.

Do you have 10 minutes next week for a brief introductory call, or perhaps a quick coffee?

Best regards,

Joe Moulton
Founder & CEO | FlowstateAI
joe@flowstateaiautomation.ai | (506) 607-1791
flowstateaiautomation.ai

***

Disclaimer: As with any public or cloud-based AI system (and in light of recent jurisprudence regarding AI and attorney-client privilege), we advise that no confidential Client Personally Identifiable Information (PII) or privileged un-redacted fact patterns be entered into the Socrates free-trial environment. Socrates is designed for statutory research, case law analysis, and template drafting using anonymized or redacted inputs.
"""

def send_emails():
    # Load contacts
    contacts = []
    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            contacts.append(row)
            
    if TEST_MODE:
        print("🧪 RUNNING IN TEST MODE - Only sending 1 email to test address.")
        # Override the first contact for testing
        contacts = [{
            'First Name': 'Joe',
            'Company': 'Test Law Firm',
            'Email': TEST_EMAIL_ADDRESS
        }]
    else:
        print(f"🚀 RUNNING IN PRODUCTION MODE - Sending to {len(contacts)} contacts.")
        print("Will pause for 2-5 minutes between emails to avoid spam filters.")
        
    # Connect to SMTP server
    try:
        print(f"Connecting to {SMTP_SERVER}...")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(LOGIN_EMAIL, SENDER_APP_PASSWORD)
        print("✅ Logged in successfully!")
    except Exception as e:
        print(f"❌ Failed to connect or login to SMTP server: {e}")
        return

    # Send emails
    for index, contact in enumerate(contacts):
        first_name = contact.get('First Name', 'Partner')
        firm_name = contact.get('Company', 'your firm')
        target_email = contact.get('Email')
        
        if not target_email or not '@' in target_email:
            print(f"⏭️ Skipping {first_name} at {firm_name} - Invalid email: {target_email}")
            continue

        subject = SUBJECT_TEMPLATE.format(firm_name=firm_name)
        body = get_email_body(first_name, firm_name)

        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = target_email

        try:
            server.send_message(msg)
            print(f"[{index+1}/{len(contacts)}] ✅ Sent to {first_name} at {firm_name} ({target_email})")
        except Exception as e:
            print(f"[{index+1}/{len(contacts)}] ❌ Failed to send to {target_email}: {e}")

        # Sleep between sends (Skip sleep if it's the last email or test mode)
        if not TEST_MODE and index < len(contacts) - 1:
            # Random delay between 120 and 300 seconds (2 to 5 minutes)
            delay = random.randint(120, 300)
            print(f"⏳ Sleeping for {delay} seconds to avoid spam filters...")
            time.sleep(delay)

    server.quit()
    print("🎉 All emails processed!")

if __name__ == "__main__":
    send_emails()
