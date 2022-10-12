import csv
import smtplib, ssl

message = """Hi {fname},
I wish you a very Happy Birthday.
I hope you had a great day."""

sender_address = "you@example.com"
sender_password = "examplePassword"

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_address, sender_password)

    with open(r"birthday.csv") as birthdays:
        reader = csv.reader(birthdays)
        next(reader)
        for fname, lname, email, dob in reader:
            server.sendmail(
                sender_address,
                email,
                message.format(fname=fname),
            )

choice = input(
    """Do you wish to add or remove names from the csv file?
    if you would like to add names type add
    otherwise if you would like to remove names type remove
    When you are finished, type exit
    """
)

if choice == "add":
    new_data = input("Enter data as first name,lastname,email,date of birth: ")
    new_data = new_data.split(",")
    with open(r"birthday.csv", "r ") as file:
        writer_object = csv.writer(file)
        next(file)
        writer_object.writerow(new_data)
elif choice == "remove":
    lines = []
    removal = input("Enter the first name of the person to be removed: ")
    with open(r"birthday.csv", "r") as file:
        reader = csv.reader(file)

        for row in reader:
            lines.append(row)

        for fields in row:
            if fields == removal:
                lines.remove(row)

    with open(r"birthday.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(lines)

