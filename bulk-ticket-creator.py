import os
import csv
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL")
ZENDESK_API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")
DRY_RUN = os.getenv("DRY_RUN", "false").lower() in ["true", "1", "t"]

# Load content from a text file
def load_file_content(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

# Retrieve emails from the specified CSV file
def get_emails_from_csv():
    email_map = {}
    with open(CSV_FILE_PATH, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                email = row[0].strip()
                domain = email.split('@')[1]
                if domain not in email_map:
                    email_map[domain] = []
                email_map[domain].append(email)
    return email_map

# Create or simulate creating a Zendesk ticket
def create_zendesk_ticket(requestor_email, cc_emails, subject, body):
    if DRY_RUN:
        print(f"Dry Run: Ticket would be created for {requestor_email} (CC'd: {cc_emails})")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
    else:
        url = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/tickets.json"
        
        ticket_data = {
            "ticket": {
                "subject": subject,
                "comment": {"body": body},
                "requester": {"email": requestor_email},
                "ccs": [{"email": email} for email in cc_emails]
            }
        }
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            url,
            json=ticket_data,
            auth=(f"{ZENDESK_EMAIL}/token", ZENDESK_API_TOKEN),
            headers=headers
        )
        
        if response.status_code == 201:
            print(f"Ticket created successfully for {requestor_email} (CC'd: {cc_emails})")
        else:
            print(f"Failed to create ticket for {requestor_email}: {response.text}")

# Main function to execute the ticket creation process
def main():
    subject = load_file_content('subject.txt')
    body_template = load_file_content('body_template.txt')
    
    email_map = get_emails_from_csv()
    
    for domain, emails in email_map.items():
        if emails:
            requestor_email = emails[0]
            cc_emails = emails[1:]
            create_zendesk_ticket(requestor_email, cc_emails, subject, body_template)

if __name__ == "__main__":
    main()
