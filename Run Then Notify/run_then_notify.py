import subprocess
import sys
import time
import socket
from getpass import getpass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


user_email = input("Enter your email: ")
user_password = getpass()
smtp_server = "smtp.gmail.com"
smtp_port = 587  # Port 587 for TLS


def send_text_email(subject, message, recipient_email, sender_email, sender_password, smtp_server, smtp_port):
    # Create a text/plain message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the text message
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
    except Exception as e:
        print(f"Email could not be sent: {str(e)}")


def run_then_notify(command):
    try:
        start_time = time.time()
        completed_process = subprocess.run(
            command,
            text=True,
            shell=True,
            stdout=sys.stdout,
            stderr=subprocess.STDOUT,
            stdin=sys.stdin
        )

        end_time = time.time()
        execution_time = end_time - start_time

        notif_subject = '[Run completed] Your command finished execution'
        notif_message = f"Command '{command}' completed\n\
            \twith exit code {completed_process.returncode}\n\
            \tin {execution_time:.2f} seconds\n\
            \n\
            This is an automated message sent from your device {socket.gethostname()}"

        send_text_email(
            subject=notif_subject,
            message=notif_message,
            recipient_email=user_email,
            sender_email=user_email,
            sender_password=user_password,
            smtp_server=smtp_server,
            smtp_port=smtp_port
        )

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_then_notify.py 'your_command_here'")
        sys.exit(1)

    command = sys.argv[1]
    run_then_notify(command)
