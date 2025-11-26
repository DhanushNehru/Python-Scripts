# 🌐 Python Web Surfing
This Python project allows you to scrape search results from the web using ```Google API``` and ```Google Custom Search Engine ID```, extract useful information, and perform basic data analysis using ```Gemini API```. It is designed to be reliable, modular, and easy to run from the command line.

---

## ✅ Functionalities Implemented

1. **Extracting Titles, URLs, and Snippets**  
   - Scrapes and saves the title, URL, and snippet/description from search results.

2. **Taking Dynamic Input (Query from Command Line)**  
   - Run the scraper with any search query directly from the command line:  
   ```bash
   python scraper.py <your query>
   ```
   For Example 
   ```bash
   python scraper.py "AI in healthcare"
   ```

3. **Saving Results to CSV File**
    - Results are saved in a seperate CSV file for each query.

4. **Running in Headless Mode (Browser in Background)**
    - The usage of the Custom Search Engine ID makes it totally headless.

5. **Crawling Multiple Pages**
    - The scraper can crawl multiple pages of search results (Free tier Google API only allows max 10 results at a time).

6. **Adding Logs**
    - Logs are stored in ```data/logs/```.

7. **Data Summarizer**
    - Summarizes the results all the results that were fetched and stores them in ```data_analysis``` folder.

## ⚡ How to Run
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Run Scraper
```bash
python scraper.py <your query>
```
## 💡 Notes
- Ensure you have ```Google API``` key, ```Google Custom Search Engine ID``` and ```Gemini API``` key set up in the script.
- Logs are automatically created for debugging and tracking scraping activity.