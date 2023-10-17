import csv
import os

CSV_FILE = "expenses.csv"

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Amount"])

def add_expense(date, description, amount):
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, description, amount])

def view_expenses():
    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(", ".join(row))

if __name__ == "__main__":
    initialize_csv()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            date = input("Enter the date (YYYY-MM-DD): ")
            description = input("Enter the description: ")
            amount = input("Enter the amount: ")

            add_expense(date, description, amount)
            print("Expense added successfully!")

        elif choice == "2":
            print("Expenses:")
            view_expenses()

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please try again.")
