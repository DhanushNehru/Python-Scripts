import requests
import json

def get_exchange_data(api_url: str = "https://theratesapi.com/api/latest/") -> dict:
    """Fetch latest exchange data from the API."""
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}")

    data = response.json()
    return data  # This includes 'base', 'date', and 'rates'

# NOTE - for logging & debugging
if __name__ == "__main__":
    exchange_data = get_exchange_data()
    print("Base currency:", exchange_data["base"])
    print("Date:", exchange_data["date"])
    print("Rates:", list(exchange_data["rates"].items())[:5])
