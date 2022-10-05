import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
body = '''
Hello, Admin
I am attaching The Sales Files With This Email.
This Year We Got a Wooping 200% Profit One Our Sales.

Regards,
Team Sales
xyz.com
'''
# Sender Email addresses and password
senders_email = ''
sender_password = ''
reveiver_email = ''

message = MIMEMultipart()
message['From'] = senders_email
message['To'] = reveiver_email
message['Subject'] = 'Sales Report 2021-- Team Sales'
message.attach(MIMEText(body, 'plain'))

attach_file_name = 'temp.txt'
attach_file = open(attach_file_name, 'rb')
payload = MIMEBase('application', 'octate-stream')
payload.set_payload((attach_file).read())
encoders.encode_base64(payload)
payload.add_header('Content-Decomposition', 'attachment',
                   filename=attach_file_name)
message.attach(payload)

session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
session.starttls()  # enable security
# login with mail_id and password
session.login(senders_email, sender_password)
text = message.as_string()
session.sendmail(senders_email, reveiver_email, text)
session.quit()
print('Mail Sent')
