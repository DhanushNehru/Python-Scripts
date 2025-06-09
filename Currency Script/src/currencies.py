from api_handler import get_exchange_data

# Returns a list of all supported currency codes.
def get_supported_currencies(rates):
    return list(rates.keys())

# Checks if a currency code is supported.
def is_valid_currency(currency_code, rates):
    return currency_code.upper() in rates

# --- DEBUG / MANUAL TEST SECTION ---
# This section runs only when you run this file directly (not when imported elsewhere)
if __name__ == "__main__":
    # Fetch live exchange data from the API
    exchange_data = get_exchange_data()

    # Print the first 5 currencies for quick inspection
    print("Sample of live rates from API:")
    print(list(exchange_data["rates"].items())[:5])

    # Sample rates dictionary for local testing
    rates_example = {"USD": 1.12, "EUR": 1.0, "GBP": 0.87}

    # Print supported currencies
    print("\nSupported currencies:", get_supported_currencies(rates_example))

    # Check a few currency codes
    print("Is 'usd' valid?", is_valid_currency("usd", rates_example))   # True
    print("Is 'AUD' valid?", is_valid_currency("AUD", rates_example))  # False