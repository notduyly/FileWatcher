import smtplib
import ssl
from email.message import EmailMessage
import os
from typing import Optional

class EmailSender:
    def __init__(self, sender_email: str, password: str):
        self.sender_email = sender_email
        self.password = password
        self.smtp_server = "smtp.office365.com"
        self.smtp_port = 587
        
    def send_email_with_attachment(self, recipient_email: str, subject: str, body: str, attachment_path: str) -> bool:
        """Send email with attachment using Office365 SMTP server.
        
        Args:
            recipient_email: Recipient's email address
            subject: Email subject
            body: Email body text
            attachment_path: Path to attachment file
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not os.path.exists(attachment_path):
            print(f"Error: Attachment file not found - {attachment_path}")
            return False
            
        try:
            message = EmailMessage()
            message["From"] = self.sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.set_content(body)
            
            with open(attachment_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(attachment_path)
            message.add_attachment(file_data, maintype="application", 
                                    subtype="octet-stream", filename=file_name)
            
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.password)
                server.send_message(message)
                print("📨 Email sent successfully!")
                return True
                
        except FileNotFoundError as e:
            print(f"Error reading attachment: {e}")
        except smtplib.SMTPAuthenticationError:
            print("SMTP authentication failed. Check your email and password.")
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        return False