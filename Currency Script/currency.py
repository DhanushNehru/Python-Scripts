# Python program to convert the currency 
# of one country to that of another country

# Import the required module
import requests

# Currency converter class
class Currency_convertor:
    # Empty dictionary to store the conversion rates
    rates = {}
    
    # Constructor to initialize the conversion rates from an API
    def __init__(self, url):
        # Fetch the data from the provided URL and store it as a JSON object
        data = requests.get(url).json()
        
        # Extract only the 'rates' section from the JSON data
        self.rates = data["rates"]

    # Function to convert from one currency to another
    # using simple cross-multiplication based on the rates
    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount  # Store the initial amount before conversion
        
        # If the base currency is not EUR, first convert the amount to EUR
        if from_currency != 'EUR':
            amount = amount / self.rates[from_currency]
        
        # Convert the amount to the target currency and round it to 2 decimal places
        amount = round(amount * self.rates[to_currency], 2)
        
        # Display the result in a readable format
        print('{} {} = {} {}'.format(initial_amount, from_currency, amount, to_currency))

# Driver code to test the functionality
if __name__ == "__main__":
    
    # Replace 'YOUR_ACCESS_KEY' with your actual access key from fixer.io
    YOUR_ACCESS_KEY = 'GET_YOUR_ACCESS_KEY_FROM_fixer.io'
    
    # Construct the API URL with the access key
    url = str.__add__('http://data.fixer.io/api/latest?access_key=', YOUR_ACCESS_KEY)
    
    # Create an instance of the Currency_convertor class
    c = Currency_convertor(url)
    
    # Take inputs from the user: source country, target country, and amount to convert
    from_country = input("From Country (currency code): ")
    to_country = input("To Country (currency code): ")
    amount = int(input("Amount: "))
    
    # Call the convert function to get the conversion result
    c.convert(from_country, to_country, amount)
