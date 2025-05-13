import smtplib
import ssl
from email.message import EmailMessage
import os

class EmailSender:
    def __init__(self, sender_email: str, password: str):
        self.sender_email = sender_email
        self.password = password
        self.smtp_server = "smtp.office365.com"
        self.smtp_port = 587
        
    def send_email_with_attachment(self, recipient_email: str, subject: str, body: str, attachment_path: str):
      
        message = EmailMessage()
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.set_content(body)
        
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        message.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
        
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.password)
                server.send_message(message)
                print("📨 Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
            