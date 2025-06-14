from api_handler import get_exchange_data

def get_supported_currencies(rates):
    """
    Return a list of supported currency codes from the rates dictionary.

    Args:
        rates (dict): Dictionary of currency codes and their exchange rates.

    Returns:
        list: List of supported currency codes (e.g., ['USD', 'EUR']).
    """
    return list(rates.keys())

def is_valid_currency(currency_code, rates):
    """
    Check if the given currency code is valid and supported.

    Args:
        currency_code (str): Currency code to validate (e.g., 'USD').
        rates (dict): Dictionary of available exchange rates.

    Returns:
        bool: True if the currency code exists in the rates, False otherwise.
    """
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