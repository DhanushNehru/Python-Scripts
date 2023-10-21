import smtplib
import ssl
import os
from email.message import EmailMessage
from email.utils import formataddr

def send_email(sender_email: str,
               sender_name: str,
               password:str,
               receiver_emails: str ,
               email_body: str,
               email_subject: str="No subject",)-> None:
    
    msg = EmailMessage()
    msg["Subject"] = email_subject
    msg["From"] = formataddr((f"{sender_name}", f"{sender_email}"))
    msg["BCC"] = sender_email
    msg.set_content(email_body)
    
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

# change these variables to suite your requirements
sender_email = "your-email@gmail.com"
sender_name = "your name"
password = os.environ.get("EMAIL_PASSWORD")

email_subject = "good morning"
email_body = "good morning, hope you have a wonderful day"

receiver_emails = ["receiver1-email@gmail.com", "receiver2-email@gmail.com", "receiver3-email@gmail.com"]

send_email(sender_email, sender_name, password, receiver_emails, email_body,email_subject)