Currency Converter
==================

A simple Python CLI application that converts an amount from one currency to another
using live exchange rates fetched from an open API.

Modules:
--------

1. **api_handler.py**
   - Handles fetching exchange rate data from the online API.

2. **currencies.py**
   - Provides utility functions to list supported currencies and validate currency codes.

3. **converter.py**
   - Contains the core logic to convert between currencies using the exchange rates.

4. **main.py**
   - CLI interface where users input the currencies and amount to convert.

5. **test_*.py**
   - Unit tests for each module to ensure functionality.

Requirements:
-------------
- Python 3.7+
- `requests` library

Install dependencies:
---------------------
Run the following command to install dependencies:
- pip install -r requirements.txt

How to Use:
-----------
Run the main script from the terminal:

Follow the prompts to enter:
- Source currency code (e.g., USD)
- Target currency code (e.g., AUD)
- Amount to convert

The app will display the converted amount and allow you to repeat or exit.

Testing:
--------
To run tests:
- python -m unittest discover

Note:
-----
The conversion is based on live exchange rates retrieved from:
https://open.er-api.com/v6/latest

Make sure you are connected to the internet when running the app.

