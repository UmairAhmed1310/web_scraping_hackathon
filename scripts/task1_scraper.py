import requests
import pandas as pd
import time
import os

# TradingView screener endpoint for U.S. stocks
URL = "https://scanner.tradingview.com/america/scan"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

# Safe subset of working columns
COLUMNS = [
    "name",               # Symbol
    "description",        # Security Name
    "close",              # Price
    "change",             # Change %
    "volume",             # Volume
    "market_cap_basic",   # Market Cap
    "price_earnings_ttm"  # P/E
    #"relative_volume_10d_calc", # Relative Volume
    #"eps_ttm",                   # EPS (TTM)
    #"earnings_per_share_growth",# EPS Growth (YoY)
    #"dividends_yield",           # Dividend Yield %
    #"sector",                    # Sector
    #"recommendation"            # Analyst Rating
]

def get_stocks(start: int, end: int):
    payload = {
        "filter": [],
        "options": {"lang": "en"},
        "symbols": {"query": {"types": []}, "tickers": []},
        "columns": COLUMNS,
        "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"},
        "range": [start, end]
    }

    response = requests.post(URL, json=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()["data"]

def parse_data(data):
    parsed = []
    for stock in data:
        values = stock["d"]
        parsed.append(dict(zip(COLUMNS, values)))
    return parsed

def scrape_all():
    all_stocks = []
    total = 4576
    batch_size = 100

    for start in range(0, total + batch_size, batch_size):
        print(f"📦 Fetching stocks {start} to {start + batch_size}")
        try:
            data = get_stocks(start, start + batch_size)
            if not data:
                print(f"❌ No data returned at {start}")
                break
            parsed = parse_data(data)
            all_stocks.extend(parsed)
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Error at range {start}-{start + batch_size}: {e}")
            break

    if all_stocks:
        df = pd.DataFrame(all_stocks[:total])  # Trim extras if needed

        # Save the output file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, "..", "data", "task1_stocks.csv")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        df.to_csv(output_path, index=False)
        print(f"✅ Saved {len(df)} rows to {output_path}")
    else:
        print("⚠️ No data scraped. CSV not saved.")

if __name__ == "__main__":
    scrape_all()
