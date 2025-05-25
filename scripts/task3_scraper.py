import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Load all stock symbols from Task 1
task1_path = os.path.join(os.path.dirname(__file__), "..", "data", "task1_stocks.csv")
df = pd.read_csv(task1_path)
symbols = df["name"].dropna().unique()

BASE_URL = "https://www.tradingview.com/symbols/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

results = []

def get_stock_overview(symbol):
    url = BASE_URL + symbol + "/"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Example: Try to extract title and meta description
        title = soup.find("meta", property="og:title")
        desc = soup.find("meta", property="og:description")

        return {
            "symbol": symbol,
            "title": title["content"] if title else "",
            "description": desc["content"] if desc else ""
        }

    except Exception as e:
        print(f"⚠️ Failed for {symbol}: {e}")
        return {
            "symbol": symbol,
            "title": "",
            "description": ""
        }

def scrape_all_overviews():
    print(f"🚀 Scraping overviews for {len(symbols)} stocks...")
    for i, sym in enumerate(symbols):
        print(f"[{i+1}/{len(symbols)}] 🔍 {sym}")
        data = get_stock_overview(sym)
        results.append(data)
        time.sleep(0.25)  # avoid rate limiting

    df_out = pd.DataFrame(results)

    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "task3_overviews.csv")
    df_out.to_csv(output_path, index=False)
    print(f"✅ Done. Saved to {output_path}")

if __name__ == "__main__":
    scrape_all_overviews()
