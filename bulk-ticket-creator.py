import os
import requests
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()

ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL")
ZENDESK_API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_SHEET_RANGE = os.getenv("GOOGLE_SHEET_RANGE")

# Load your service account key JSON file
SERVICE_ACCOUNT_FILE = 'path_to_your_service_account.json'

# Authenticate and build the Sheets API client
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)
service = build('sheets', 'v4', credentials=credentials)

def load_file_content(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

def get_emails_from_sheet():
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=GOOGLE_SHEET_ID,
                                range=GOOGLE_SHEET_RANGE).execute()
    values = result.get('values', [])
    
    email_map = {}
    for row in values:
        if row:
            email = row[0]
            domain = email.split('@')[1]
            if domain not in email_map:
                email_map[domain] = []
            email_map[domain].append(email)
    
    return email_map

def create_zendesk_ticket(requestor_email, cc_emails, subject, body):
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

def main():
    subject = load_file_content('subject.txt')
    body_template = load_file_content('body_template.txt')
    
    email_map = get_emails_from_sheet()
    
    for domain, emails in email_map.items():
        if emails:
            requestor_email = emails[0]
            cc_emails = emails[1:]
            create_zendesk_ticket(requestor_email, cc_emails, subject, body_template)

if __name__ == "__main__":
    main()
