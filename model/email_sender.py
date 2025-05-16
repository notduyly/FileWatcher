import base64
import os.path
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
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

def send_email(service, to, subject, body_text, attachment_path=None):
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
    print(f"✅ Message Id: {send_message['id']}")
    return send_message




# test
def send_email_with_csv(service, to: str, subject: str, body_text: str, csv_data: list, 
                       csv_filename: str = "export.csv") -> dict:
    """
    Send email with CSV file attachment generated from data
    
    Args:
        service: Gmail API service instance
        to: Recipient email address
        subject: Email subject
        body_text: Email body content
        csv_data: List of data to write to CSV
        csv_filename: Name of the CSV file (default: export.csv)
        
    Returns:
        dict: Message details from Gmail API
    """
    import csv
    import tempfile
    
    # Create temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        writer = csv.writer(temp_file)
        writer.writerows(csv_data)
        temp_path = temp_file.name
        
    try:
        # Send email with CSV attachment
        result = send_email(service, to, subject, body_text, temp_path)
        return result
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

# Usage example:
def test_csv_email():
    service = gmail_authenticate()
    
    # Sample CSV data
    csv_data = [
        ["Name", "Age", "City"],
        ["John Doe", "30", "New York"],
        ["Jane Smith", "25", "Los Angeles"]
    ]
    
    result = send_email_with_csv(
        service=service,
        to="recipient@email.com",
        subject="CSV Report",
        body_text="Please find the attached CSV report.",
        csv_data=csv_data,
        csv_filename="report.csv"
    )
    
    if result:
        print("Email with CSV sent successfully!")
    else:
        print("Failed to send email with CSV.")

if __name__ == "__main__":
    test_csv_email()