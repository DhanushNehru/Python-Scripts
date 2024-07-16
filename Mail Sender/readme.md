Email Sender Script Documentation

This Python script sends an email with an attachment using the smtplib library. It is designed to send a sales report email with a specific body and a file attachment. Below are the details and usage of the script:

Email Content:

    The email's body contains a simple message with a sales report for the year.
    The sender's email address and password should be specified in the script.
    The recipient's email address should also be provided in the script.


Code Explanation:

    The script uses the smtplib library to send emails.
    It constructs the email message with a subject, sender, recipient, and body text.
    It attaches the 'temp.txt' file to the email.
    It connects to the Gmail SMTP server, enables a secure connection, and logs in using the sender's credentials.
    The email message is converted to a string, sent, and the connection to the SMTP server is closed.
    A message, "Mail Sent," is printed to indicate that the email has been sent.

Please note that this script is set up for Gmail's SMTP server by default. If you are using a different email service, you may need to adjust the SMTP server details accordingly.

Ensure that you have allowed less secure apps to access your Gmail account or use an application-specific password for sending emails via Gmail

<!-- Updated README links and corrected typos -->
<!-- Updated README links and corrected typos -->