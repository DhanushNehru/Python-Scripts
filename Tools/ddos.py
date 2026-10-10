import requests
from concurrent.futures import ThreadPoolExecutor
import time

def make_request(url, method='GET', headers=None, cookies=None, data=None, params=None):
    try:

        response = requests.request(method, url, headers=headers, cookies=cookies, data=data, params=params)
        print(f"Response code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

def start_requests(url, method='GET', headers=None, cookies=None, data=None, params=None, num_threads=5, duration=10):
    executor = ThreadPoolExecutor(max_workers=num_threads)
    end_time = time.time() + duration  # Time to stop the requests

    while time.time() < end_time:
        for _ in range(num_threads):
            executor.submit(make_request, url, method, headers, cookies, data, params)

    executor.shutdown(wait=True)
    print("Requests completed.")

# Usage example
url = "Sample URL"
start_requests(url, num_threads=5, duration=15) #time in seconds
#change methods as required