# Custom-search CLI
A simple Python script that uses the **Google Custom Search API** to fetch search results and export them into a CSV file.


## Requirements
- Python 3.8+
- A Google API key
- A Google Custom Search Engine (CX) ID
- Install dependencies:
  ```bash
  pip install requests
  pip install beautifulsoup4
  pip install python-csv
  pip install argparse
  ```
  
## Setup
1. Get a Google API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Create a Custom Search Engine (CX) at [Google CSE](https://cse.google.com/cse/all)
3. Run the script with your API key to create setting.json:

    python main.py -sq [SEARCH_QUERY] --add_api_key [YOUR_API_KEY]

## Usage
Search with query:
```bash
python scraper.py -sq "github"
```
Fetch multiple pages (10 results per page):
```bash
python scraper.py -sq "github" --pages 3
```
## Output
- Results are saved in output.csv in the following columns:

\# , Title , Link 

> [!NOTE] </br>
> Free quota: 100 queries/day (10 results per query). </br>
> If `setting.json` is missing or doesn’t have an API key, use `--add_api_key`.
---