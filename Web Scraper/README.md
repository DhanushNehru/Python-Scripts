In this script, we use the `requests` library to send a GET request to the Python.org blogs page. We then use the `BeautifulSoup` library to parse the HTML content of the page.

We find all the blog titles on the page by searching for `h2` elements with the class `blog-title`. We then print each title found and save them to a file named `blog_titles.txt`.

To run this script, first install the required libraries:

```bash
pip install requests beautifulsoup4
