import ssl
import smtplib
import csv
from abc import ABC, abstractmethod


class EmailSender(ABC):
    @abstractmethod
    def send_email(self, recipient, message):
        pass


class GmailEmailSender(EmailSender):
    def __init__(self, sender_address, sender_password):
        self.sender_address = sender_address
        self.sender_password = sender_password

    def send_email(self, recipient, message):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_address, self.sender_password)
            server.sendmail(self.sender_address, recipient, message)


class BirthdayMessage:
    @staticmethod
    def create_message(fname):
        return f"""Hi {fname},

I wish you a very Happy Birthday.

I hope you had a great day."""


class BirthdayListManager:
    def __init__(self, filename):
        self.filename = filename

    def load_birthdays(self):
        with open(self.filename) as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            return list(reader)

    def add_birthday(self, new_data):
        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(new_data)

    def remove_birthday(self, first_name):
        updated_lines = []
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] != first_name:
                    updated_lines.append(row)

        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_lines)


class BirthdayNotifier:
    def __init__(self, email_sender, birthday_list_manager):
        self.email_sender = email_sender
        self.birthday_list_manager = birthday_list_manager

    def notify_birthdays(self):
        birthdays = self.birthday_list_manager.load_birthdays()
        for fname, lname, email, dob in birthdays:
            message = BirthdayMessage.create_message(fname)
            self.email_sender.send_email(email, message)


def main():
    sender_address = "you@example.com"
    sender_password = "examplePassword"
    birthday_file = "birthday.csv"

    email_sender = GmailEmailSender(sender_address, sender_password)
    birthday_list_manager = BirthdayListManager(birthday_file)
    notifier = BirthdayNotifier(email_sender, birthday_list_manager)

    notifier.notify_birthdays()

    while True:
        choice = input(
            """Do you wish to add or remove names from the csv file?
            If you would like to add names type 'add'
            Otherwise if you would like to remove names type 'remove'
            When you are finished, type 'exit': """
        ).strip().lower()

        if choice == "exit":
            break
        elif choice == "add":
            new_data = input("Enter data as first name,lastname,email,date of birth: ")
            new_data = new_data.split(",")
            birthday_list_manager.add_birthday(new_data)
        elif choice == "remove":
            removal = input("Enter the first name of the person to be removed: ")
            birthday_list_manager.remove_birthday(removal)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
