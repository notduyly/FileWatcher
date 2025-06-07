import base64
import os.path
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def __gmail_authenticate():
    """
    Authenticate with Gmail API using OAuth2 credentials.
    
    Returns:
        googleapiclient.discovery.Resource: Gmail service object for API calls.
    """
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
    """
    Compose and send an email message with optional attachment via Gmail API.
    
    Args:
        service: Authenticated Gmail service object.
        to: Recipient email address.
        subject: Email subject line.
        body_text: Email body content.
        attachment_path: Path to file to attach. Defaults to None.
        
    Returns:
        dict: Gmail API response containing message details and message ID.
        
    Raises:
        Exception: If file attachment cannot be read or email sending fails.
    """
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
    """
    Send an email with a CSV attachment containing file watch events.
    
    Args:
        recipient: Email address of the recipient.
        file_path: Path to the CSV file to attach to the email.
        
    Returns:
        bool: True if email was sent successfully, False if any error occurred.
        
    Raises:
        Exception: Catches and handles all exceptions, returning False on failure.
    """
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
    """
    Validate an email address format using regular expression pattern matching.
    
    Args:
        email: Email address string to validate.
        
    Returns:
        bool: True if email format is valid, False otherwise.
    """
    import re
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))