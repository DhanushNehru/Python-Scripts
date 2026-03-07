import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from datetime import datetime

def get_all_links(url):
    print(f"Fetching page: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        for tag in soup.find_all("a", href=True):
            full_url = urljoin(url, tag["href"])
            if full_url.startswith("http"):
                links.add(full_url)
        print(f"Found {len(links)} links.")
        return links
    except Exception as e:
        print(f"Error fetching page: {e}")
        return set()


def check_link(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.head(url, timeout=10, allow_redirects=True, headers=headers)
        # Some servers don't support HEAD, fallback to GET
        if response.status_code in [405, 403]:
            response = requests.get(url, timeout=10, headers=headers)
        return response.status_code
    except requests.exceptions.ConnectionError:
        return "Connection Error"
    except requests.exceptions.Timeout:
        return "Timeout"
    except Exception as e:
        return f"Error: {e}"


def get_status_label(status):
    if isinstance(status, int):
        if status < 300:
            return " ✔ OK"
        elif status < 400:
            return "⚠️Redirect"
        elif status == 404:
            return "❌Not Found"
        elif status == 403:
            return "🔒Forbidden"
        elif status >= 500:
            return "Server Error"
    return str(status)


def export_to_csv(results, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["URL", "Status", "Result"])
        for url, status in results:
            label = "Working" if isinstance(status, int) and status < 400 else "Broken"
            writer.writerow([url, status, label])
    print(f"Results saved to: {filename}")


def check_all_links(website_url):
    links = get_all_links(website_url)

    if not links:
        print("No links found.")
        return

    broken = []
    working = []
    all_results = []

    print(f"{'STATUS':<15} URL")
    print("-" * 60)

    for i, link in enumerate(links, 1):
        status = check_link(link)
        label = get_status_label(status)
        all_results.append((link, status))

        print(f"{label:<15} {link}")

        if isinstance(status, int) and status < 400:
            working.append((link, status))
        else:
            broken.append((link, status))

    # Summary
    print("\nSUMMARY")
    print("-" * 20)
    print(f"Total Links: {len(links)}")
    print(f"Working:     {len(working)}")
    print(f"Broken:      {len(broken)}")

    # Broken links detail
    if broken:
        print("\nBROKEN LINKS:")
        for url, status in broken:
            print(f"[{status}] {url}")

    # Ask to export
    save = input("\nSave results to CSV? (y/n): ").strip().lower()
    if save == "y":
        filename = f"link_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        export_to_csv(all_results, filename)


if __name__ == "__main__":
    print("--- Link Checker Tool ---")
    website = input("Enter website URL: ").strip()
    if not website.startswith("http"):
        website = "https://" + website
    check_all_links(website)