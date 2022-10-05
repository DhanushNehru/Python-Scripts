# import necessary libraries
from bs4 import BeautifulSoup
import requests


# function to extract html document from given url
def getHTMLdocument(url):

    # request for HTML document of given url
    response = requests.get(url)
    
    if(response.status_code == 200):
        # return HTML document
        return response.text
    else:
        # return None
        raise Exception("Invalid URL or Check your internet connection")


# assign required credentials
# assign URL
url_to_scrape = input("Enter the URL to be Scraped: ")

# create document
html_document = getHTMLdocument(url_to_scrape)

# create soap object
soup = BeautifulSoup(html_document, 'html.parser')

def getHash(link):
    s = ''
    i = 0
    n = len(link)
    while(i < n):
        if(link[i] == '#'):
            s += link[i:i+7]
        i += 1
    return s

# find all the anchor tags with "href"
# attribute starting with "https://"

l = set()

for link in soup.find_all('td'):
    s = getHash(str(link))
    if s != '':
        l.add(s.lower())
file = open('colors.txt', 'a')
file.write('[')
for i in l:
    file.write("'"+i+"',")
file.write(']')
file.close()
