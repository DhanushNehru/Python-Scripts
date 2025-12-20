# IP Geolocator

A simple Python script that provides geolocation information for any IP address using the ip-api.com service.

## Features

- **IP Geolocation**: Get detailed location information for any IP address
- **Comprehensive Data**: Retrieves country, region, city, ZIP code, coordinates, timezone, and ISP information
- **Error Handling**: Gracefully handles API errors and invalid IP addresses
- **Simple Interface**: Easy-to-use command-line interface

## Requirements

- Python 3.x
- `requests` library

## Installation

1. Clone or download this repository
2. Install the required dependency:

```bash
pip install requests
```

## Usage

Run the script and enter an IP address when prompted:

```bash
python main.py
```

Example:
```
Enter IP Address To Geolocate: 8.8.8.8
Successfully Located : 8.8.8.8
Country:  United States
Region:  California
City:  Mountain View
ZIP:  94043
Latitude:  37.4056
Longitude:  -122.0775
Timezone:  America/Los_Angeles
ISP:  Google LLC
```

## API Information

This script uses the free ip-api.com service:
- **Endpoint**: `http://ip-api.com/json/`
- **Rate Limit**: 45 requests per minute for free tier
- **No API Key Required**: Works without registration

## Supported Information

The script retrieves the following information for each IP address:
- Country
- Region/State
- City
- ZIP/Postal Code
- Latitude and Longitude coordinates
- Timezone
- ISP (Internet Service Provider)

## Error Handling

If the API request fails or returns an error status, the script will display:
```
Error! Please try again.
```

## Limitations

- Free tier has rate limits (45 requests per minute)
- Some IP addresses may not return complete information
- Results depend on the accuracy of the ip-api.com database

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
