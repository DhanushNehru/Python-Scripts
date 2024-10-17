# Python program to convert the currency
# of one country to that of another country

# Import the modules needed
import requests
import json
import os

class Currency_convertor:
    # empty dict to store the conversion rates
    rates = {}

    def __init__(self, url):
        # Check if cache file exists (Offline Mode)
        if os.path.exists('currency_rates.json'):
            with open('currency_rates.json', 'r') as file:
                self.rates = json.load(file)
            print("Using cached rates.")
        else:
            # Fetch from API and handle potential errors
            try:
                data = requests.get(url).json()
                self.rates = data["rates"]

                # Cache rates to local file for offline usage
                with open('currency_rates.json', 'w') as file:
                    json.dump(self.rates, file)
                print("Fetched rates from API and cached them.")
            except requests.exceptions.RequestException as e:
                print("Error fetching data from API:", e)
                raise SystemExit("Failed to fetch rates.")

    # Function to do a simple cross multiplication between
    # the amount and the conversion rates
    def convert(self, from_currency, to_currency, amount):
        # Input validation for currency codes
        if from_currency not in self.rates or to_currency not in self.rates:
            print(f"Invalid currency code. Available currencies are: {', '.join(self.rates.keys())}")
            return

        # Validation for amount
        if not isinstance(amount, (int, float)) or amount <= 0:
            print("Amount must be a positive number.")
            return

        initial_amount = amount
        if from_currency != 'EUR':
            amount = amount / self.rates[from_currency]

        # Limiting the precision to 2 decimal places
        amount = round(amount * self.rates[to_currency], 2)
        print('{} {} = {} {}'.format(initial_amount, from_currency, amount, to_currency))

# Driver code
if __name__ == "__main__":

    # YOUR_ACCESS_KEY = 'GET YOUR ACCESS KEY FROM fixer.io'
    YOUR_ACCESS_KEY = 'your_api_key_here'  # For testing, add your API key here.
    url = f'http://data.fixer.io/api/latest?access_key={YOUR_ACCESS_KEY}'
    
    # Create an instance of the Currency_convertor class
    c = Currency_convertor(url)
    
    from_country = input("From Country (Currency Code): ").upper()
    to_country = input("To Country (Currency Code): ").upper()
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount entered. Please enter a numeric value.")
        exit()

    # Convert the currency
    c.convert(from_country, to_country, amount)
