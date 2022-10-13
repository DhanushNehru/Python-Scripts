from locale import currency
import requests
import json

currency = input().lower()
cache = {}

while True:

    currency_exch = input().lower()

    if currency_exch == '':
        break

    amount_to_exch = int(input())

    URL = f'http://www.floatrates.com/daily/{currency}.json'

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
        #print("Sorry, but it is not in the cache!")
        cache[currency_exch] = exch[currency_exch]['rate']
        rate = round(amount_to_exch * cache[currency_exch], 2)
        print(f"You received {rate} {currency_exch.upper()}.")
