# Import smtplib for our actual email sending function
import smtplib
 
# Helper email modules 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# sender email address
email_user = 'SENDER_EMAIL'
 
# sender email passowrd for login purposes
email_password = 'SENDER_EMAIL_PASSWORD'

# list of users to whom email is to be sent
email_send = ['LIST_OF_RECIPIENTS']
subject = 'EMAIL_SUBJECT'
msg = MIMEMultipart()
msg['From'] = email_user
# converting list of recipients into comma separated string
msg['To'] = ", ".join(email_send)
msg['Subject'] = subject
body = 'EMAIL_BODY'
msg.attach(MIMEText(body,'plain'))
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)
server.sendmail(email_user,email_send,text)
server.quit()