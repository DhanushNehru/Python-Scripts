def get_user_input():
    try:
        years = int(input("🔢 How many years will you be saving? "))
        principal = float(input("💰 Enter current amount in your account: ₹"))
        monthly_invest = float(input("📥 Enter your monthly investment amount: ₹"))
        interest = float(input("📈 Enter the expected yearly interest rate (e.g., 10% as 0.1): "))
        return years, principal, monthly_invest, interest
    except ValueError:
        print("⚠️ Please enter valid numeric values.")
        return get_user_input()


def calculate_future_value(years, principal, monthly_invest, annual_interest):
    yearly_contribution = monthly_invest * 12
    amount = principal

    for _ in range(years):
        amount = (amount + yearly_contribution) * (1 + annual_interest)

    return amount


def main():
    print("💼 Welcome to the Investment Growth Calculator 💼\n")

    years, principal, monthly_invest, interest = get_user_input()
    print("\n⏳ Calculating investment growth...\n")

    future_value = calculate_future_value(years, principal, monthly_invest, interest)

    print("📊 After {} years, your total account balance will be: ₹{:.2f}".format(years, future_value))
    print("\n✅ Thank you for using the Investment Calculator!")


if __name__ == "__main__":
    main()
