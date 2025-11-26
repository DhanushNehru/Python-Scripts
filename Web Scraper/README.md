# Web Scraper

This repository contains two web scraping scripts:

## 1. Traditional Web Scraper (`Web_Scraper.py`)

This script uses the `requests` library to send a GET request to the Python.org blogs page. It then uses the `BeautifulSoup` library to parse the HTML content of the page.

It finds all the blog titles on the page by searching for `h2` elements with the class `blog-title`. It then prints each title found and saves them to a file named `blog_titles.txt`.

### Usage
To run this script, first install the required libraries:

```bash
pip install requests beautifulsoup4
```

Then run:

```bash
python Web_Scraper.py
```

## 2. Google Custom Search Scraper (`google_web_scraper.py`)

This enhanced CLI web scraper uses the Google Custom Search API to extract URLs, titles, and snippets from search results. This approach is more robust than traditional web scraping methods as it:

- Bypasses CAPTCHA challenges that may occur during direct web scraping
- Retrieves structured data (title, URL, and snippet/description) 
- Handles dynamic websites more reliably
- Is less prone to breaking when website structures change
- Allows searching by keyword to retrieve multiple metadata fields

### Prerequisites
Before using this script, you need:
1. A Google API Key from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. A Custom Search Engine ID from [Google Programmable Search Engine](https://programmablesearchengine.google.com/)

### Installation
```bash
pip install -r requirements.txt
```

### Setup
Set your API credentials as environment variables:
```bash
export GOOGLE_API_KEY='your_google_api_key'
export SEARCH_ENGINE_ID='your_search_engine_id'
```

Alternatively, you can pass them directly as command-line arguments.

### Usage
Basic usage:
```bash
python google_web_scraper.py --query "Python tutorials" --results 10
```

Save results in JSON format:
```bash
python google_web_scraper.py --query "machine learning blogs" --results 20 --format json
```

Specify output file:
```bash
python google_web_scraper.py --query "web development news" --output my_search.json --format json
```

With API credentials as arguments:
```bash
python google_web_scraper.py --query "Python tutorials" --api-key YOUR_API_KEY --engine-id YOUR_ENGINE_ID
```

### Options
- `--query, -q`: Search query to use for web scraping (required)
- `--results, -r`: Number of search results to retrieve (default: 10)
- `--output, -o`: Output file name (default: search_results.txt)
- `--format, -f`: Output format: txt or json (default: txt)
- `--api-key, -k`: Google API Key (optional)
- `--engine-id, -e`: Google Custom Search Engine ID (optional)

### Features
- Command-line interface with configurable options
- Support for both TXT and JSON output formats
- Environment variable support for credentials
- Error handling and user-friendly messages
- Ability to retrieve multiple pages of results