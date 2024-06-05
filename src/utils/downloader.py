import base64
import os
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class EmailsExtractor:
    SCOPES = ['https://www.googleapis.com/auth/...']
    TOKEN_FILE = '/path/files/token.json'
    CREDENTIALS_FILE = '/path/files/client_secret_103211622544-38k6sa39ddk51sbman00n2akvnf12oqj.apps.googleusercontent.com.json'
    OUTPUT_DIR = '/path/files/'

    def __init__(self):
        self.service = self.get_service()

    def get_service(self):
        """Authenticate with Google API and return the credentials using refresh token if available."""
        creds = None
        if os.path.exists(self.TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_FILE, self.SCOPES, access_type='offline', prompt='consent')
                creds = flow.run_local_server(port=0)
            with open(self.TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        return build('gmail', 'v1', credentials=creds)

    def get_mime_message(self, user_id, msg_id):
        try:
            message = self.service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
            part = message['payload']['parts'][0]
            data = part['body']['data']
            return base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
        except Exception as error:
            print(f'Error: {error}')
            return None

    def save_emails_by_bank(self, user_id, messages):
        bank_keywords = {
            'BAC Credomatic': 'bac_credomatic_emails.json',
            'BCR': 'bcr_emails.json',
            'Banco Nacional': 'banco_nacional_emails.json'
        }
        emails_by_bank = {key: [] for key in bank_keywords}

        for message in messages:
            content = self.get_mime_message(user_id, message['id'])
            if content:
                for bank, filename in bank_keywords.items():
                    if bank in content:
                        email_dict = {
                            'subject': message.get('snippet', 'No Subject'),
                            'content': content
                        }
                        emails_by_bank[bank].append(email_dict)
                        break

        for bank, emails in emails_by_bank.items():
            if emails:
                file_path = os.path.join(self.OUTPUT_DIR, bank_keywords[bank])
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(emails, file, ensure_ascii=False, indent=4)
                print(f'Emails for {bank} saved in: {file_path}')

    def run(self):
        result = self.service.users().messages().list(userId='me', fields='messages(id,snippet)').execute()
        messages = result.get('messages', [])
        self.save_emails_by_bank('me', messages)

if __name__ == '__main__':
    extractor = EmailsExtractor()
    extractor.run()
