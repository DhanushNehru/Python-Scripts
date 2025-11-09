#!/usr/bin/env python3
"""
CLI Web Scraper using Google Custom Search API
This script allows users to search for websites and extract titles, URLs, and snippets
using Google Custom Search API, making it more robust than traditional web scraping.
"""
import os
import sys
import json
import argparse
import requests


class GoogleSearchScraper:
    """
    A web scraper that uses Google Custom Search API to extract URLs, titles, and snippets.
    """

    def __init__(self, api_key=None, search_engine_id=None):
        """
        Initialize the scraper with API credentials.

        :param api_key: Google API Key
        :param search_engine_id: Google Custom Search Engine ID
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.search_engine_id = search_engine_id or os.getenv('SEARCH_ENGINE_ID')

        if not self.api_key:
            raise ValueError(
                "Google API Key is required. "
                "Set GOOGLE_API_KEY environment variable or pass as parameter."
            )
        if not self.search_engine_id:
            raise ValueError(
                "Search Engine ID is required. "
                "Set SEARCH_ENGINE_ID environment variable or pass as parameter."
            )

        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search(self, query, num_results=10, start_index=1):
        """
        Search using Google Custom Search API and extract results.

        :param query: Search query
        :param num_results: Number of results to return (max 10 per request)
        :param start_index: Starting index for results (1-based)
        :return: List of dictionaries containing title, URL, and snippet
        """
        # The API allows maximum 10 results per request
        if num_results > 10:
            num_results = 10

        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'num': num_results,
            'start': start_index
        }

        response = requests.get(self.base_url, params=params, timeout=10)

        if response.status_code != 200:
            raise Exception(f"Error from Google API: {response.status_code} - {response.text}")

        data = response.json()

        results = []
        if 'items' in data:
            for item in data['items']:
                result = {
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', '')
                }
                results.append(result)

        return results

    def search_multiple_pages(self, query, total_results=10):
        """
        Search and retrieve multiple pages of results.

        :param query: Search query
        :param total_results: Total number of results desired
        :return: List of all results
        """
        all_results = []
        start_index = 1

        while len(all_results) < total_results:
            num_to_fetch = min(10, total_results - len(all_results))
            results = self.search(query, num_to_fetch, start_index)

            if not results:
                break

            all_results.extend(results)
            start_index += 10

            # Break if we have reached the desired number of results
            if len(all_results) >= total_results:
                break

        return all_results[:total_results]


def save_results_to_file(results, filename, format_type='txt'):
    """
    Save search results to a file in the specified format.

    :param results: List of search results
    :param filename: Name of the file to save to
    :param format_type: Format to save ('txt' or 'json')
    """
    if format_type.lower() == 'json':
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    else:  # default to txt format
        with open(filename, 'w', encoding='utf-8') as f:
            for i, result in enumerate(results, 1):
                f.write(f"Result {i}:\n")
                f.write(f"Title: {result['title']}\n")
                f.write(f"URL: {result['link']}\n")
                f.write(f"Snippet: {result['snippet']}\n")
                f.write("-" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='CLI Web Scraper using Google Custom Search API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --query "Python tutorials" --results 10
  %(prog)s --query "machine learning blogs" --results 20 --format json
  %(prog)s --query "web development news" --output my_search.txt
        """
    )

    parser.add_argument(
        '--query',
        '-q',
        required=True,
        help='Search query to use for web scraping'
    )

    parser.add_argument(
        '--results',
        '-r',
        type=int,
        default=10,
        help='Number of search results to retrieve (default: 10)'
    )

    parser.add_argument(
        '--output',
        '-o',
        default='search_results.txt',
        help='Output file name (default: search_results.txt)'
    )

    parser.add_argument(
        '--format',
        '-f',
        choices=['txt', 'json'],
        default='txt',
        help='Output format: txt or json (default: txt)'
    )

    parser.add_argument(
        '--api-key',
        '-k',
        help='Google API Key (optional, will use GOOGLE_API_KEY env var if not provided)'
    )

    parser.add_argument(
        '--engine-id',
        '-e',
        help='Google Custom Search Engine ID (optional, will use SEARCH_ENGINE_ID env var if not provided)'
    )

    args = parser.parse_args()

    try:
        scraper = GoogleSearchScraper(api_key=args.api_key, search_engine_id=args.engine_id)
        results = scraper.search_multiple_pages(args.query, args.results)

        if not results:
            print("No results found for the query.")
            return

        print(f"Found {len(results)} results for query '{args.query}':\n")

        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   URL: {result['link']}")
            print(f"   Snippet: {result['snippet']}")
            print()

        save_results_to_file(results, args.output, args.format)
        print(f"Results saved to '{args.output}' in {args.format.upper()} format.")

    except ValueError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        print("\nTo use this script, you need to provide Google API credentials:")
        print("1. Get a Google API key from: https://console.cloud.google.com/apis/credentials")
        print("2. Create a Custom Search Engine from: https://programmablesearchengine.google.com/")
        print("3. Set environment variables or use command-line parameters:")
        print("   export GOOGLE_API_KEY='your_api_key'")
        print("   export SEARCH_ENGINE_ID='your_search_engine_id'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
