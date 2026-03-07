# Import required libraries
import requests

def get_weather():
    """
    Fetches weather data for Santa Barbara (hardcoded coordinates) using Open-Meteo API.

    Returns:
        dict: Weather data if successful, None otherwise.
    """
    base_url = "https://api.open-meteo.com/v1/weather"
    params = {
        'latitude': 34.42,
        'longitude': -119.70,
        'current_weather': True,
        'hourly': {'temperature_2m': {'time': ['2023-08-25T00']}}  # Example date
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching weather data: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    # Example usage (no ZIP code input, hardcoded for Santa Barbara)
    weather_data = get_weather()

    if weather_data:
        print(f"Weather in {weather_data['current']['location']['name']}:")
        print(f"Temperature: {weather_data['current']['temperature']}°C (Feels like {weather_data['current']['apparent_temperature']}°C)")
        print(f"Conditions: {weather_data['current']['weathercode']}")  # Weather code
        print(f"Humidity: {weather_data['hourly']['relativehumidity_2m'][0]}%")
        print(f"Wind Speed: {weather_data['current']['windspeed']} km/h")
    else:
        print("Failed to fetch weather data.")

if __name__ == "__main__":
    main()