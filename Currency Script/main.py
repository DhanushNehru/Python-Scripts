"""
main.py - Simple CLI interface for Currency Converter

Prompts user for input currencies and amount, and displays the converted value.
"""

from converter import CurrencyConverter

def main():
    """
    Run the interactive currency converter CLI loop.
    Prompts user for source and target currencies and amount to convert.
    Continues until the user types 'no' to exit.
    """
    print("Welcome to the Currency Converter\n")

    converter = CurrencyConverter()

    while True:
        try:
            from_currency = input("Enter source currency code (e.g., AUD): ").strip().upper()
            to_currency = input("Enter target currency code (e.g., USD): ").strip().upper()
            amount = float(input(f"Enter amount in {from_currency}: "))

            converted = converter.convert(from_currency, to_currency, amount)
            print(f"\n✅ {amount} {from_currency} = {converted} {to_currency}\n")

        except ValueError as e:
            print(f"❌ Error: {e}\n")

        # Ask to convert another or exit
        again = input("Do you want to convert another amount? (yes/no): ").strip().lower()
        if again != "yes":
            print("Thank you for using the Currency Converter. Goodbye!")
            break

if __name__ == "__main__":
    main()
