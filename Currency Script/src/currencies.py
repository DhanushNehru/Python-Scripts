# TODO REVIEW BELOW CODE TO ENSURE THAT WHAT IS IN THIS MODULE FOR FUNCTION RECALLING CURRENCY FROM API
# Importing necessary modules for currency formatting and HTTP requests
from locale import currency
import requests
import json

# Get the base currency input from the user and convert it to lowercase
currency = input("Enter the base currency (e.g., USD, EUR): ").lower()

# Initialize an empty cache to store exchange rates
cache = {}

# Infinite loop to process exchange requests until the user exits
while True:

    # Get the target currency input from the user and convert it to lowercase
    currency_exch = input("Enter the currency to exchange to (leave blank to exit): ").lower()

    # If the input is blank, break out of the loop (exit condition)
    if currency_exch == '':
        break

    # Get the amount to exchange from the user
    amount_to_exch = int(input("Enter the amount to exchange: "))

    # URL for getting exchange rates from floatrates.com
    URL = f'http://www.floatrates.com/daily/{currency}.json'

    # Fetch the exchange rates in JSON format
    exch = json.loads(requests.get(URL).text)

    # Update cache for USD and EUR based on the base currency
    if currency == 'usd':
        # If base currency is USD, cache EUR rate
        cache.update(eur=exch['eur']['rate'])
    elif currency == 'eur':
        # If base currency is EUR, cache USD rate
        cache.update(usd=exch['usd']['rate'])
    else:
        # For other base currencies, cache both USD and EUR rates
        cache.update(usd=exch['usd']['rate'], eur=exch['eur']['rate'])

    print("Checking the cache...")

    # Check if the target currency's rate is in the cache
    if currency_exch in cache:
        # If the rate is in the cache, calculate the exchanged amount
        rate = round(amount_to_exch * cache[currency_exch], 2)
        print("Oh! It is in the cache!")
        print(f"You received {rate} {currency_exch.upper()}.")
    else:
        # If the rate is not in the cache, fetch it from the exchange rates and store it in cache
        print("Sorry, but it is not in the cache!")
        cache[currency_exch] = exch[currency_exch]['rate']
        rate = round(amount_to_exch * cache[currency_exch], 2)
        print(f"You received {rate} {currency_exch.upper()}.")
