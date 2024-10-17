import requests
import json
import os

currency = input("Enter base currency code: ").lower()
cache = {}

# Cache rates for offline mode
if os.path.exists(f'{currency}_rates.json'):
    with open(f'{currency}_rates.json', 'r') as file:
        cache = json.load(file)
    print(f"Using cached rates for {currency}.")
else:
    print("No cached rates found, fetching from the API.")

while True:
    currency_exch = input("Enter currency to exchange to (or press Enter to stop): ").lower()

    if currency_exch == '':
        break

    try:
        amount_to_exch = float(input("Enter amount to exchange: "))
        if amount_to_exch <= 0:
            print("Amount must be positive.")
            continue
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        continue

    URL = f'http://www.floatrates.com/daily/{currency}.json'

    try:
        exch = json.loads(requests.get(URL).text)

        if currency == 'usd':
            cache.update(eur=exch['eur']['rate'])
        elif currency == 'eur':
            cache.update(usd=exch['usd']['rate'])
        else:
            cache.update(usd=exch['usd']['rate'], eur=exch['eur']['rate'])

        print("Checking the cache...")
        if currency_exch in cache:
            rate = round(amount_to_exch * cache[currency_exch], 2)
            print("Oh! It is in the cache!")
            print(f"You received {rate} {currency_exch.upper()}.")
        else:
            # Store new rates in the cache
            cache[currency_exch] = exch[currency_exch]['rate']
            rate = round(amount_to_exch * cache[currency_exch], 2)
            print(f"You received {rate} {currency_exch.upper()}.")

            # Save new rates to file for offline mode
            with open(f'{currency}_rates.json', 'w') as file:
                json.dump(cache, file)
            print(f"Rates cached for future use.")

    except requests.exceptions.RequestException as e:
        print(f"API error or connection issue: {e}")
        break
