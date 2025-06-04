import base64
import os.path
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def __gmail_authenticate():
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def __compose_email_message(service, to, subject, body_text, attachment_path=None):
    message = EmailMessage()
    message.set_content(body_text)
    message['To'] = to
    message['From'] = 'me'
    message['Subject'] = subject

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        message.add_attachment(file_data, maintype='application',
                            subtype='octet-stream', filename=file_name)

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {
        'raw': encoded_message
    }
    
    send_message = service.users().messages().send(userId="me", body=create_message).execute()
    print(f"Message Id: {send_message['id']}")
    return send_message

def send_email_with_attachment(recipient: str, file_path: str) -> bool:
    try:
        service = __gmail_authenticate()
        if not service:
            print("Failed to authenticate Gmail")
            return False
            
        subject = "File Watch Events Report"
        body_text = "Please find attached the file watch events report."
        
        if not os.path.exists(file_path):
            print(f"CSV file not found: {file_path}")
            return False
            
        __compose_email_message(
            service=service,
            to=recipient,
            subject=subject,
            body_text=body_text,
            attachment_path=file_path
        )
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def validate_email(email: str) -> bool:
    import re
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))