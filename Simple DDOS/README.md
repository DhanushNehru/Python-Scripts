# Multithreaded HTTP Requests with Python

This script performs multithreaded HTTP requests using Python's `requests` library and `ThreadPoolExecutor`. The code allows you to send multiple HTTP requests concurrently for a specified duration.

## Features
- Sends concurrent HTTP requests to a specified URL.
- Supports multiple request methods (GET, POST, etc.).
- Allows customizing headers, cookies, data, and URL parameters.
- The number of threads and the duration of the requests can be controlled.
- Uses ThreadPoolExecutor to handle multithreading efficiently.

## Requirements
- Python 3.x
- `requests` library

To install the `requests` library, run:
```bash
pip install requests
```

## Usage

### Function: `make_request`
This function sends a single HTTP request to a given URL with the specified parameters.
- **Arguments**:
  - `url` (str): The URL to send the request to.
  - `method` (str): The HTTP method to use (default: GET).
  - `headers` (dict): Optional HTTP headers to include.
  - `cookies` (dict): Optional cookies to include.
  - `data` (dict): Optional data for POST requests.
  - `params` (dict): Optional URL parameters.

- **Example**:
make_request("https://example.com", method='POST', data={"key": "value"})

### Function: `start_requests`
This function sends multiple HTTP requests concurrently for a specified duration.
- **Arguments**:
  - `url` (str): The URL to send the requests to.
  - `method` (str): The HTTP method to use (default: GET).
  - `headers` (dict): Optional HTTP headers to include.
  - `cookies` (dict): Optional cookies to include.
  - `data` (dict): Optional data for POST requests.
  - `params` (dict): Optional URL parameters.
  - `num_threads` (int): The number of threads to use (default: 5).
  - `duration` (int): The duration in seconds to send requests (default: 10 seconds).

- **Example**:
url = "https://example.com/api"
start_requests(url, method='GET', num_threads=5, duration=15)

## How It Works
1. The `start_requests` function uses `ThreadPoolExecutor` to manage the specified number of threads.
2. Each thread sends an HTTP request to the given URL.
3. The process continues until the specified duration ends.
4. The `make_request` function handles sending the requests and printing the response status codes.

## Example Usage
url = "https://example.com/api"
start_requests(url, num_threads=5, duration=15)  # Sends requests for 15 seconds using 5 threads.

## Customization
- You can modify the method, headers, cookies, data, or params in the function calls to fit your use case.
- For POST requests, pass data through the `data` argument.

start_requests("https://example.com/post", method='POST', data={'key': 'value'}, num_threads=10, duration=20)

## License
This project is licensed under the MIT License.
