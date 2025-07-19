import yfinance as yf
import json
import os 
from datetime import datetime

tickers = ['TSLA', 'AAPL', 'INFY.NS', 'RELIANCE.NS', 'TCS.NS']
data = []

for symbol in tickers:
    stock = yf.Ticker(symbol)
    info = stock.info
    price_change = info.get("regularMarketChangePercent", 0)
    volume = info.get("volume")
    market_cap = info.get("marketCap")

    data.append({
        "ticker": symbol,
        "name": info.get("shortName", symbol),
        "sector": info.get("sector", "N/A"),
        "price_change": round(price_change, 2),
        "rsi": 50,  # Dummy for now
        "volume": f"{volume/1e6:.1f}M" if volume else "N/A",
        "market_cap": f"${market_cap/1e9:.1f}B" if market_cap else "N/A",
        "is_positive": price_change > 0
    })

with open("static/stocks.json", "w") as f:
    json.dump(data, f)

print("✅ Stock data updated")
from datetime import datetime
data.append({"_fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
from datetime import datetime

output = {
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "stocks": data
}

os.makedirs("static", exist_ok=True)
with open("static/stocks.json", "w") as f:
    json.dump(output, f, indent=2)
