# Old Script #

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_key_statistics(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    tables = soup.find_all("table")
    data = {}
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 2:
                label = cells[0].text.strip()
                value = cells[1].text.strip()
                data[label] = value
    data["Ticker"] = ticker.upper()
    return data

tickers = ['AAPL', 'CCL', 'MSFT', 'TSLA', 'PYPL', 'SNOW', 'TEAM', 'HOOD', 'BABA', 'TM', 'META','BA', 'MAR', 'RCL']
all_data = []

for ticker in tickers:
    stats = get_key_statistics(ticker)
    all_data.append(stats)

df = pd.DataFrame(all_data)

cols = ['Ticker'] + [col for col in df.columns if col != 'Ticker']
df = df[cols]

df.to_csv("stocks.csv", index=False)

print("Saved key statistics for 'stocks.csv'")
