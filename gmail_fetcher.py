# gmail_fetcher.py

import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the OAuth 2.0 scopes for Gmail API (read-only access)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail():
    """Authenticate the user and return the Gmail API service client."""
    creds = None
    token_path = 'token.json'
    creds_path = 'credentials.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If no valid credentials, start OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def decode_base64_email(data):
    """Decode base64-encoded email content."""
    decoded_bytes = base64.urlsafe_b64decode(data.encode('UTF-8'))
    return decoded_bytes.decode('utf-8', errors='replace')


def fetch_promotional_emails(max_results=10):
    """Fetch recent promotional emails using Gmail API."""
    service = authenticate_gmail()
    results = service.users().messages().list(userId='me', labelIds=['CATEGORY_PROMOTIONS'], maxResults=max_results).execute()
    messages = results.get('messages', [])

    emails = []

    for msg in messages:
        full_msg = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = full_msg.get('payload', {})
        headers = payload.get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        from_email = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')

        body = ''
        parts = payload.get('parts', [])
        if parts:
            for part in parts:
                mime_type = part.get('mimeType')
                if mime_type == 'text/plain':
                    data = part.get('body', {}).get('data')
                    if data:
                        body = decode_base64_email(data)
                        break
        else:
            data = payload.get('body', {}).get('data')
            if data:
                body = decode_base64_email(data)

        emails.append({
            'id': msg['id'],
            'subject': subject,
            'from': from_email,
            'body': body,
        })

    return emails
