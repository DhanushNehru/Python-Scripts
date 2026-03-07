

# Weather Checker

A Python script to fetch weather data for Santa Barbara (ZIP code 93001) using the Open-Meteo API.

## Requirements

- No API key is needed for this script.

## Usage

1. Install the required dependency:
   ```sh
   pip install requests
   ```

2. Run the script:
   ```sh
   python weather_checker.py
   ```

3. The script will output weather details like temperature, conditions, humidity, and wind speed for Santa Barbara.

## Example Output

```
Weather in Santa Barbara:
Temperature: 25°C (Feels like 28°C)
Conditions: 0 (Clear)
Humidity: 64%
Wind Speed: 5 km/h
```

## Notes

- The script is hardcoded to fetch weather for Santa Barbara (`34.42, -119.70`). If you want to check a different location, modify the `latitude` and `longitude` values in the `get_weather` function.
- Open-Meteo provides data in metric units by default (Celsius). No need for additional parameters unless you prefer imperial units.
- Ensure your internet connection is stable when running the script, as it relies on an external API.