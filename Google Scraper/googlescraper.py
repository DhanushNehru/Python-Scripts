from bs4 import BeautifulSoup
import requests

response = requests.get("http://www.google.com")
soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all('a')

for link in links:
    print(link.get_text())
