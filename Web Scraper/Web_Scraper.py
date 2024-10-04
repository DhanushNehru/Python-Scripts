import requests
from bs4 import BeautifulSoup

# URL to scrape data from
URL = "https://www.python.org/blogs/"

# Send a GET request to the URL
response = requests.get(URL)

# Parse the webpage content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the blog titles on the page
titles = soup.find_all('h2', class_='blog-title')

# Print each title found
print("Python.org Blog Titles:\n")
for i, title in enumerate(titles, start=1):
    print(f"{i}. {title.get_text(strip=True)}")

# Save the titles to a file
with open("blog_titles.txt", "w") as file:
    for title in titles:
        file.write(title.get_text(strip=True) + "\n")

print("\nBlog titles saved to 'blog_titles.txt'.")
     
   
     
     