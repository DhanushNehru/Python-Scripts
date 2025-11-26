#!/usr/bin/env python3
"""
Example usage of the Google Custom Search Scraper
This demonstrates how to use the scraper programmatically
"""
import os
from google_web_scraper import GoogleSearchScraper


def example_basic_usage():
    """Example of basic usage"""
    # Initialize the scraper with API credentials
    # These can be set as environment variables: GOOGLE_API_KEY and SEARCH_ENGINE_ID
    api_key = os.getenv('GOOGLE_API_KEY')
    search_engine_id = os.getenv('SEARCH_ENGINE_ID')
    
    if not api_key or not search_engine_id:
        print("Please set GOOGLE_API_KEY and SEARCH_ENGINE_ID environment variables")
        return
    
    try:
        scraper = GoogleSearchScraper(api_key=api_key, search_engine_id=search_engine_id)
        
        # Search for Python tutorials
        results = scraper.search("Python tutorials", num_results=5)
        
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            link = result.get('link', 'No URL')
            snippet = result.get('snippet', 'No snippet')
            print(f"{i}. {title}")
            print(f"   URL: {link}")
            print(f"   Snippet: {snippet}")
            print()
    except Exception as e:
        print(f"Error during search: {e}")


def example_multiple_pages():
    """Example of searching multiple pages"""
    api_key = os.getenv('GOOGLE_API_KEY')
    search_engine_id = os.getenv('SEARCH_ENGINE_ID')
    
    if not api_key or not search_engine_id:
        print("Please set GOOGLE_API_KEY and SEARCH_ENGINE_ID environment variables")
        return
    
    try:
        scraper = GoogleSearchScraper(api_key=api_key, search_engine_id=search_engine_id)
        
        # Search for multiple pages of results
        results = scraper.search_multiple_pages("machine learning", total_results=15)
        
        print(f"Found {len(results)} results for 'machine learning':")
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            link = result.get('link', 'No URL')
            print(f"{i:2d}. {title}")
            print(f"    URL: {link}")
            print()
    except Exception as e:
        print(f"Error during search: {e}")


if __name__ == "__main__":
    print("=== Basic Usage Example ===")
    example_basic_usage()
    print("\n=== Multiple Pages Example ===") 
    example_multiple_pages()