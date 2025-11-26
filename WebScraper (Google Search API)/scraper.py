import csv
import logging
import sys
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import textwrap

os.environ['GRPC_VERBOSITY'] = 'NONE'
import google.generativeai as genai


# Setup logging
os.makedirs("data/logs", exist_ok=True)
logging.basicConfig(
    filename=f"data/logs/scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("CUSTOM_SEARCH_ENGINE_ID")
gemini_api=os.getenv("GEMINI_API")

def scrape_google(query, num_results=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": API_KEY, "cx": CX, "q": query, "num": num_results}

    logging.info(f"Fetching results for query: {query}")
    try:
        req = requests.get(url, params=params)
        req.raise_for_status()
        data = req.json()
        results = []

        for item in data.get("items", []):
            results.append({
                "Title": item.get("title", ""),
                "URL": item.get("link", ""),
                "Snippet": item.get("snippet", "")
            })

        logging.info(f"Fetched {len(results)} results for query: {query}")
        return results

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return []

def save_results(results, filename):
    if not results:
        logging.warning("No results to save.")
        print("❌ No results to save.")
        return

    os.makedirs("data", exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "URL", "Snippet"])
        writer.writeheader()
        writer.writerows(results)
    logging.info(f"Saved results to {filename}")
    print(f"✅ Saved {len(results)} results to {filename}")
    
def summarize(query):
    filename=f"./data/{query}.csv"
    df=pd.read_csv(filename)
    texts_combined = "\n\n".join(df["Snippet"].astype(str).tolist())
    PROMPT=f'''
        You are an expert text summarizer. I will provide you with multiple short text excerpts. 
        Your task is to read all of them and produce a single, concise summary that captures the 
        key ideas, themes, and main points across all excerpts. 

        Make the summary clear, coherent, and around 3–5 sentences long.

        Texts:
        {texts_combined}
        
        Output only the final summary.
    '''
    genai.configure(api_key=gemini_api)
    model = genai.GenerativeModel('gemini-2.5-pro')
    response = model.generate_content(PROMPT)
    
    wrapped_text = textwrap.fill(response.text, width=95)
    
    folder_path = "data_analysis"
    os.makedirs(folder_path, exist_ok=True)
    summary_file_path = os.path.join(folder_path, f"{query}_summary.txt")
    
    with open(summary_file_path, "w", encoding="utf-8") as f:
        f.write(wrapped_text)

    print(f"✅ Summary saved to {summary_file_path}")
    
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <search query>")
        sys.exit(1)

    query = "".join(sys.argv[1])
    logging.info(f"Starting scrape for query: {query}")

    data = scrape_google(query)
    save_results(data,f"./data/{query}.csv")
    
    summarize(query)