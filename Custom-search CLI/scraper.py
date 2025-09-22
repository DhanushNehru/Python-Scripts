import requests
import json
import os
import csv
import argparse
from typing import List, Dict, Tuple, Any

SETTING_ROUTE = 'setting.json'
DEFAULT_CX = 'b0264518c3d104eda'


def load_settings(api_key: str | None = None) -> Dict[str, str]:
    """
    Load API settings from setting.json, or create it if missing.
    """
    if os.path.exists(SETTING_ROUTE):
        with open(SETTING_ROUTE, 'r', encoding="utf-8") as f:
            settings = json.load(f)

        if not settings.get("API_KEY"):
            if api_key:
                settings["API_KEY"] = api_key
                with open(SETTING_ROUTE, 'w', encoding="utf-8") as f:
                    json.dump(settings, f, indent=4)
            else:
                raise ValueError("API_KEY is missing in setting.json. Use --add_api_key to add one.")
    else:
        if not api_key:
            raise FileNotFoundError("No setting.json found. Please run with --add_api_key to create one.")
        settings = {"API_KEY": api_key, "CX": DEFAULT_CX}
        with open(SETTING_ROUTE, 'w', encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

    return settings


def scrape(search_query: str, api_key: str, cx: str, pages: int = 1) -> Tuple[List[Dict[str, Any]], float]:
    """
    Perform a Google Custom Search and return results.
    """
    results = []
    search_time = 0.0

    for page in range(pages):
        start = page * 10 + 1
        url = (
            f"https://www.googleapis.com/customsearch/v1"
            f"?key={api_key}&q={search_query}&cx={cx}&start={start}"
        )

        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError(f"API request failed: {response.status_code} {response.text}")

        data = response.json()

        if "items" not in data:
            print("No results found or error:", data)
            break

        results.extend(data["items"])
        search_time += float(data['searchInformation']['searchTime'])

    return results, search_time


def export_to_csv(results: List[Dict[str, Any]], filename: str = "output.csv") -> None:
    """
    Export search results to a CSV file.
    """
    rows = [[i + 1, item.get("title", ""), item.get("link", "")] for i, item in enumerate(results)]

    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["#", "Title", "Link"])
        writer.writerows(rows)

    print(f"Exported {len(results)} results to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Google Custom Search scraper")
    parser.add_argument("-sq", "--search_query", required=True, help="Search query to search for")
    parser.add_argument("--add_api_key", type=str, help="Your Google API key")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages of results to fetch")
    args = parser.parse_args()

    settings = load_settings(args.add_api_key)
    api_key = settings["API_KEY"]
    cx = settings["CX"]

    print(f"Using API key: {api_key}")

    results, elapsed_time = scrape(args.search_query, api_key, cx, args.pages)

    export_to_csv(results)
    print(f"Completed in {elapsed_time:.2f} seconds.")


if __name__ == "__main__":
    main()
