# Automating-Emails-on-a-.csv-file
<hr>
Python program to automate an email personalized birthday message by reading details from a .csv file<br>
Also includes options to  add and remove details from said .csv file

# How To Use the birthday.csv File

1. The `birthday.csv` file contains the list of people with their details.
2. Each entry should have the following format:

```bash
first_name,last_name,email,dob
John,Doe,johndoe@example.com,1990-08-15
Jane,Smith,janesmith@example.com,1995-05-23
```

3. You can add or remove records while the script is running by choosing options in the interactive menu.

# How To Run

Put the script and the `birthday.csv` file in the same folder.
Update the script with your Gmail address and App Password:

```python
sender_address = "you@example.com"
sender_password = "your-app-password"
```

Run the following command from the terminal:

```bash
python birthday_manager.py
```

The script will:

* Load birthdays from `birthday.csv`
* Send birthday wishes to listed email addresses
* Allow you to add or remove birthdays interactively

# Benefits

**Automated:** Sends out personalized birthday wishes through Gmail.

**Interactive:** Add or remove entries without touching the CSV file manually.

**Secure:** Uses Gmail App Passwords instead of your real password.

**Extensible:** Can be enhanced to check today’s date, add scheduling, or support other email providers.

<!-- Updated README links and corrected typos -->
<!-- Updated README links and corrected typos -->