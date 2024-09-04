# Step 1: Install Required Python Packages
First, install the necessary packages using pip:

```
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv requests
```

# Step 2: Create the .env File
Create a .env file in the same directory as your Python script with the following variables:

```
ZENDESK_SUBDOMAIN=your_zendesk_subdomain
ZENDESK_EMAIL=your_email@example.com
ZENDESK_API_TOKEN=your_api_token
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_SHEET_RANGE=Sheet1!A:A
```

Replace the values with your actual Zendesk and Google Sheets credentials.