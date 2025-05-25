import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Source URL
URL = "https://sarmaaya.pk/mutual-funds/"

# Output directory setup
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "task2_mutual_funds.csv")

def scrape_mutual_funds():
    print("🌐 Requesting page...")
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    print("🔍 Parsing table...")
    table = soup.find("table")

    headers = [th.text.strip() for th in table.find("thead").find_all("th")]
    rows = []

    for tr in table.find("tbody").find_all("tr"):
        cols = [td.text.strip() for td in tr.find_all("td")]
        if cols:
            rows.append(cols)

    print(f"✅ Extracted {len(rows)} funds.")

    df = pd.DataFrame(rows, columns=headers)
    df.to_csv(output_path, index=False)
    print(f"💾 Saved to: {output_path}")

if __name__ == "__main__":
    scrape_mutual_funds()
