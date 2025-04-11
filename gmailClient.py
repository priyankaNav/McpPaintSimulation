import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import asyncio

class GmailClient:
    # Gmail API scope for sending emails
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.creds = None
        self.service = None

    @classmethod
    async def create(cls, credentials_path='credentials.json', token_path='token.json'):
        self = cls(credentials_path, token_path)
        await self.authenticate()
        return self

    async def authenticate(self):
        # Load token if available (offload the blocking file I/O and parsing)
        if os.path.exists(self.token_path):
            self.creds = await asyncio.to_thread(
                Credentials.from_authorized_user_file, self.token_path, self.SCOPES
            )
        # If there are no valid credentials, initiate OAuth flow
        if not self.creds or not self.creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
            # Run the OAuth flow in a separate thread so it doesn't block the event loop.
            self.creds = await asyncio.to_thread(flow.run_local_server, port=0)
            # Save the newly obtained credentials to token file.
            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())
        # Build the Gmail service off the main thread
        self.service = await asyncio.to_thread(build, 'gmail', 'v1', credentials=self.creds)
        # (Optional) Print a debug statement
        print("Gmail service built successfully.")

    def _send_email(self, to, subject, message_text):
        """Internal synchronous method to send email."""
        # Create the email message
        message = MIMEText(message_text)
        message['to'] = to
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw}
        try:
            sent_message = self.service.users().messages().send(userId="me", body=body).execute()
            return {"status": "success", "message_id": sent_message.get("id")}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def send_email(self, to, subject, message_text):
        # Wrap the blocking _send_email call in a thread.
        return await asyncio.to_thread(self._send_email, to, subject, message_text)

    async def gmail_send(self, params: dict):
        # Validate incoming parameters
        required = ["to", "subject", "message"]
        if not all(param in params for param in required):
            return {"status": "error", "error": "Missing required parameters: 'to', 'subject', 'message'"}
        # Call the Gmail client to send the email
        return await self.send_email(params["to"], params["subject"], params["message"])

# Testing the GmailClient module directly.
if __name__ == "__main__":
    async def main():
        # Create an instance (this will trigger OAuth and build the service)
        gmail_client = await GmailClient.create()
        # Now send an email using the client.
        result = await gmail_client.gmail_send({
            "to": "priyanka.navgire11@gmail.com",
            "subject": "Test Email",
            "message": "This is a test email sent from the Gmail MCP tool."
        })
        print(result)
    
    asyncio.run(main())