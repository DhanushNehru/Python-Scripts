from datetime import date

def calculate_age(birth_year, birth_month, birth_day):
    today = date.today()
    age = today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))
    return age

if __name__ == "__main__":
    print("🎂 Welcome to the Age Calculator!")
    birth_year = int(input("Enter your birth year (YYYY): "))
    birth_month = int(input("Enter your birth month (MM): "))
    birth_day = int(input("Enter your birth day (DD): "))

    print(f"You are {calculate_age(birth_year, birth_month, birth_day)} years old.")
