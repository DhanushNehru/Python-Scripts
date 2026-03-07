# Link Checker

A Python script that scans a website and detects broken links.

The tool extracts all links from a webpage, checks their HTTP status code, and reports whether they are working or broken. Results can also be exported to a CSV file.

## Features

- Extracts all links from a webpage
- Detects broken and working links
- Shows HTTP status codes
- Displays a summary report
- Optional CSV export of results

## Requirements

- Python 3.8+

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python link_checker.py
```

Enter a website URL when prompted:

```
Enter website URL: https://example.com
```

## Example Output

```
--- Link Checker Tool ---

Fetching page: https://example.com
Found 25 links.

STATUS           URL
------------------------------------------------------------
✔ OK             https://example.com/about
⚠️ Redirect       https://example.com/docs
❌ Not Found      https://example.com/old-page

SUMMARY
--------------------
Total Links: 25
Working:     23
Broken:      2
```

## CSV Export

After scanning, you can save results to a CSV file:

```
Save results to CSV? (y/n):
```

A report like this will be generated:

```
link_report_20260307_143210.csv
```

## License

MIT License