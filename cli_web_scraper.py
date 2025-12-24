import requests
from bs4 import BeautifulSoup
import sys

def scrape_url(url: str) -> dict:
    """
    Scrape the given URL and return a dict with the title
    and a list of the first few text snippets.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")

    # get title
    title = soup.title.string if soup.title else "No title found"

    # get first few text snippets
    snippets = []
    for p in soup.find_all("p"):
        text = p.get_text().strip()
        if text:
            snippets.append(text)
        if len(snippets) >= 5:
            break

    return {"title": title, "snippets": snippets}


def main():
    if len(sys.argv) < 2:
        print("Usage: python cli_web_scraper.py <URL>")
        return

    url = sys.argv[1]
    result = scrape_url(url)

    if result:
        print(f"Title: {result['title']}")
        print("Snippets:")
        for snippet in result["snippets"]:
            print(f"- {snippet}")


if __name__ == "__main__":
    main()

