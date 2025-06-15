import requests

def get_exchange_data(api_url: str = "https://open.er-api.com/v6/latest") -> dict:
    """
    Retrieve the latest foreign exchange rates from the specified API.

    Args:
        api_url (str): Endpoint to fetch exchange data from. Defaults to the open.er-api URL.

    Returns:
        dict: A dictionary containing the base currency, timestamp, and exchange rates.

    Raises:
        Exception: If the API request fails or returns a non-200 status.
    """
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}")

    data = response.json()

    return data  # Includes 'base_code', 'time_last_update_utc', and 'rates'

# NOTE - for logging & debugging
if __name__ == "__main__":
    exchange_data = get_exchange_data()
    print("Base currency:", exchange_data["base_code"])
    print("Date:", exchange_data["time_last_update_utc"])
    print("Rates:", list(exchange_data["rates"].items())[:5])
