import requests

def shorten_url_with_tinyurl(long_url):
    url = f'http://tinyurl.com/api-create.php?url={long_url}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

long_url = r"INSERT YOUR LONG URL HERE"
short_url = shorten_url_with_tinyurl(long_url)

if short_url:
    print(f'Shortened URL: {short_url}')
else:
    print('Error shortening URL')