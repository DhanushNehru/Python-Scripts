# TODO REVIEW AND ENSURE THE PURPOSE OF THIS MODULE IS TO CONVERT
# Python program to convert the currency
# of one country to that of another country

# Import the modules needed
import requests

class Currency_convertor:
    # empty dict to store the conversion rates
    rates = {}
    
    def __init__(self, url):
        data = requests.get(url).json()
        # Extracting only the rates from the json data
        self.rates = data["rates"]

    # function to do a simple cross multiplication between
    # the amount and the conversion rates
    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        if from_currency != 'EUR':
            amount = amount / self.rates[from_currency]

        # limiting the precision to 2 decimal places
        amount = round(amount * self.rates[to_currency], 2)
        print('{} {} = {} {}'.format(initial_amount, from_currency, amount, to_currency))

# Driver code
if __name__ == "__main__":

    YOUR_ACCESS_KEY = 'YOUR_ACCESS_KEY_HERE'  # Define your access key
    url = f'http://data.fixer.io/api/latest?access_key={YOUR_ACCESS_KEY}'  # Use f-string for cleaner concatenation
    c = Currency_convertor(url)
    
    from_country = input("From Country (currency code): ")
    to_country = input("To Country (currency code): ")
    amount = float(input("Amount: "))  # Use float for decimal support

    c.convert(from_country, to_country, amount)
