import requests

def get_exchange_data(api_url: str = "https://open.er-api.com/v6/latest") -> dict:
    """Fetch latest exchange data from the API."""
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}")

    data = response.json()
    # Ensure response was successful
    if data.get("result") != "success":
        raise Exception(f"API returned error: {data.get('error-type', 'Unknown error')}")

    return data  # Includes 'base_code', 'time_last_update_utc', and 'rates'

# NOTE - for logging & debugging
if __name__ == "__main__":
    exchange_data = get_exchange_data()
    print("Base currency:", exchange_data["base_code"])
    print("Date:", exchange_data["time_last_update_utc"])
    print("Rates:", list(exchange_data["rates"].items())[:5])
