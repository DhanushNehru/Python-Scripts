# Guidebook: Email Automation Script with Advanced Features

# Overview

This Python script automates the process of sending emails to multiple recipients with enhanced features such as support for attachments and HTML-formatted emails. The script uses Python's built-in libraries (smtplib, ssl, and email) to send emails securely through Gmail's SMTP server. It also allows the user to customize the email's content, subject, recipients, and more via environment variables or in-script configuration.

# Features Added

1. Support for Attachments: You can now attach files to the email, making it more versatile for different use cases like sending reports, documents, or images.
2. HTML Email Support: You can send emails in HTML format, giving you more flexibility with rich text formatting, embedded links, and other styling options.

# Prerequisites

1. Python 3.x
2. A Gmail account (with less secure apps access enabled or an app-specific password if using 2FA)
3. Required libraries: smtplib, ssl, os, email (all built-in Python libraries)

# Environment Setup
To ensure security, it's recommended to store sensitive information like email credentials in environment variables. For this guide, we will store the Gmail password as an environment variable:

export EMAIL_PASSWORD='your_gmail_password'

# Code Breakdown
1. Import Required Modules 

import smtplib
import ssl
import os
from email.message import EmailMessage
from email.utils import formataddr
-------------------------------------------------------------------------------------
smtplib: Used to create the connection to the Gmail SMTP server.
ssl: Provides a layer of security for the email communication.
os: Used to access environment variables (like the email password).
email.message: Allows crafting email messages, including text, HTML, and attachments.

**send_email Function**

This is the main function that sends the email.

Function Parameters:
sender_email (str): The email address sending the email.
sender_name (str): The sender's name that will appear in the email.
password (str): The sender's email password, pulled from environment variables.
receiver_emails (list): A list of email addresses to send the email to.
email_body (str): The body of the email, which can be in plain text or HTML.
email_subject (str): The subject line of the email. Default is "No subject."

**Example Function**

send_email(
    sender_email="youremail@gmail.com",
    sender_name="Your Name",
    password=os.environ.get("EMAIL_PASSWORD"),
    receiver_emails=["recipient1@gmail.com", "recipient2@gmail.com"],
    email_body="Hello, this is a test email!",
    email_subject="Test Email"
)

-------------------------------------------------------------------------------------

**Setting Up Email Headers**
The email headers include the subject, sender, recipient, and format:

msg["Subject"] = email_subject
msg["From"] = formataddr((f"{sender_name}", f"{sender_email}"))
msg["BCC"] = sender_email
msg.set_content(email_body)  # This can also be an HTML body

-------------------------------------------------------------------------------------

**SMTP Server Connection**
Here we establish a connection to Gmail's SMTP server and use TLS (Transport Layer Security) to ensure a secure connection.

smtp_port = 587
smtp_server = "smtp.gmail.com"
ssl_context = ssl.create_default_context()

-------------------------------------------------------------------------------------

**Login and Sending the Email**
After logging in, the script loops through each recipient in the receiver_emails list and sends the email.

my_server = smtplib.SMTP(smtp_server, smtp_port)
my_server.starttls(context=ssl_context)
my_server.login(sender_email, password)

-------------------------------------------------------------------------------------

**Adding Attachments**
If you want to send attachments, use the following modification:

if attachments:
    for file in attachments:
        with open(file, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(file)
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

-------------------------------------------------------------------------------------

**Sending HTML Emails**
To send HTML emails, modify the email body to contain HTML:

msg.add_alternative("""\
    <html>
        <body>
            <p>Hello, <br>
            This is an <b>HTML email</b>!</p>
        </body>
    </html>
    """, subtype='html')

 -------------------------------------------------------------------------------------

**Error Handling**
The script includes basic error handling to notify you if the connection or email-sending process fails:

except Exception as e:
    print(f"ERROR: {e}")

--------------------------------------------------------------------------------------

**Full Example with Attachment and HTML Support**

send_email(
    sender_email="youremail@gmail.com",
    sender_name="Your Name",
    password=os.environ.get("EMAIL_PASSWORD"),
    receiver_emails=["recipient1@gmail.com", "recipient2@gmail.com"],
    email_body="<h1>This is a Test Email with HTML</h1>",
    email_subject="Test Email with HTML and Attachment",
    attachments=["path/to/attachment1", "path/to/attachment2"]
)


--------------------------------------------------------------------------------------

# How to run the script

Ensure the required environment variable (EMAIL_PASSWORD) is set.
Customize the sender email, receiver emails, email body, and subject in the script.
Run the script from the command line:

python email_automation.py or main.py

You can also schedule the script to run daily using cron jobs or Task Scheduler (Windows).


# Thank You  for reading this tutorial. I hope you found it helpful. If you have any questions or need further

