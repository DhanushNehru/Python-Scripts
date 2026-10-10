import smtplib
import ssl
import os
from email.message import EmailMessage
from email.utils import formataddr
from mimetypes import guess_type

def send_email(sender_email: str,
               sender_name: str,
               password:str,
               receiver_emails: list,
               email_body: str,
               email_subject: str = "No subject",
               is_html: bool = False,
               attachments: list = None) -> None:
    
    msg = EmailMessage()
    msg["Subject"] = email_subject
    msg["From"] = formataddr((f"{sender_name}", f"{sender_email}"))
    msg["BCC"] = sender_email  # Can add CC or BCC here if needed
    
    # Support both plain text and HTML emails
    if is_html:
        msg.add_alternative(email_body, subtype='html')
    else:
        msg.set_content(email_body)

    # Add attachments if provided
    if attachments:
        for file_path in attachments:
            try:
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                    file_name = os.path.basename(file_path)
                    mime_type, _ = guess_type(file_path)
                    if mime_type:
                        mime_main, mime_subtype = mime_type.split('/')
                    else:
                        mime_main, mime_subtype = 'application', 'octet-stream'
                    
                    msg.add_attachment(file_data, maintype=mime_main, subtype=mime_subtype, filename=file_name)
                    print(f"Attached file: {file_name}")
            except Exception as e:
                print(f"Failed to attach {file_path}: {e}")

    smtp_port = 587
    smtp_server = "smtp.gmail.com"

    # Adding ssl layer of security
    ssl_context = ssl.create_default_context()

    try:
        # Creating smtp server
        print("Connecting to Server...")
        my_server = smtplib.SMTP(smtp_server, smtp_port)
        my_server.starttls(context=ssl_context)
        
        # Login to smtp server
        my_server.login(sender_email, password)
        print("Connected to server!")

        # Sending email
        print(f"Sending email from: {sender_email}")
        print("**************************************")
        for receiver in receiver_emails:
            msg["To"] = receiver
            print(f"Sending email to: {receiver}")
            my_server.sendmail(sender_email, receiver, msg.as_string())
            print(f"...\nSuccessfully sent to: {receiver}")
            print("**************************************")
            del msg["To"]
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        my_server.quit()

# Example usage
sender_email = "your-email@gmail.com"
sender_name = "your name"
password = os.environ.get("EMAIL_PASSWORD")

email_subject = "Good morning"
email_body = """
<h1>Good Morning!</h1>
<p>Hope you have a <strong>wonderful day</strong>.</p>
"""
receiver_emails = ["receiver1-email@gmail.com", "receiver2-email@gmail.com"]
attachments = ["path/to/attachment1.pdf", "path/to/attachment2.jpg"]

# Sending the email as HTML with attachments
send_email(sender_email, sender_name, password, receiver_emails, email_body, email_subject, is_html=True, attachments=attachments)
