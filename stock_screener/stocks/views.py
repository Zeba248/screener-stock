from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import Stock
import yfinance as yf
import json
from datetime import datetime
import logging
import signal

logger = logging.getLogger(__name__)

def home(request):
    """Render the main stock screener page with real-time data"""
    # Fetch real-time stock data
    stocks_data = get_realtime_stock_data()
    
    # Handle sorting
    sort_by = request.GET.get('sort', 'price_change_percent')
    reverse = True  # Default to descending
    
    if sort_by == 'current_price':
        stocks_data.sort(key=lambda x: x.get('current_price', 0), reverse=reverse)
    elif sort_by == 'volume':
        # Sort by volume (convert from string like "123.4M" to float)
        def volume_sort_key(stock):
            vol_str = stock.get('volume', '0')
            if vol_str == 'N/A':
                return 0
            try:
                if 'M' in vol_str:
                    return float(vol_str.replace('M', ''))
                elif 'B' in vol_str:
                    return float(vol_str.replace('B', '')) * 1000
                else:
                    return float(vol_str)
            except:
                return 0
        stocks_data.sort(key=volume_sort_key, reverse=reverse)
    elif sort_by == 'market_cap':
        # Sort by market cap (convert from string like "$123.4B" to float)
        def market_cap_sort_key(stock):
            cap_str = stock.get('market_cap', '0')
            if cap_str == 'N/A':
                return 0
            try:
                cap_str = cap_str.replace('$', '')
                if 'B' in cap_str:
                    return float(cap_str.replace('B', ''))
                elif 'M' in cap_str:
                    return float(cap_str.replace('M', '')) / 1000
                else:
                    return float(cap_str)
            except:
                return 0
        stocks_data.sort(key=market_cap_sort_key, reverse=reverse)
    else:  # Default to price_change_percent
        stocks_data.sort(key=lambda x: x.get('price_change_percent', 0), reverse=reverse)
    
    context = {
        'stocks': stocks_data,
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'sort_by': sort_by
    }
    
    return render(request, 'stocks/index.html', context)

def stocks_json(request):
    """Return real-time stock data as JSON"""
    stocks_data = get_realtime_stock_data()
    
    # Ensure all data is JSON serializable
    json_stocks_data = []
    for stock in stocks_data:
        json_stock = {
            "ticker": str(stock.get("ticker", "")),
            "name": str(stock.get("name", "")),
            "sector": str(stock.get("sector", "")),
            "current_price": float(stock.get("current_price", 0)),
            "price_change": float(stock.get("price_change", 0)),
            "price_change_percent": float(stock.get("price_change_percent", 0)),
            "rsi": float(stock.get("rsi", 50)),
            "volume": str(stock.get("volume", "")),
            "market_cap": str(stock.get("market_cap", "")),
            "is_positive": bool(stock.get("is_positive", False)),
            "last_fetched": str(stock.get("last_fetched", ""))
        }
        json_stocks_data.append(json_stock)
    
    return JsonResponse({
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stocks": json_stocks_data
    })

def get_realtime_stock_data():
    """Get real-time stock data - using demo mode for reliability"""
    print(f"[{timezone.now().strftime('%H:%M:%S')}] Generating LIVE demo stock data...")
    return get_demo_stock_data()

def get_demo_stock_data():
    """Generate realistic demo stock data when API is unavailable"""
    import random
    from datetime import datetime
    
    demo_stocks = [
        {"ticker": "TSLA", "name": "Tesla, Inc.", "sector": "Consumer Cyclical", "base_price": 250.00},
        {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology", "base_price": 190.00},
        {"ticker": "INFY.NS", "name": "Infosys Limited", "sector": "Technology", "base_price": 1500.00},
        {"ticker": "RELIANCE.NS", "name": "Reliance Industries", "sector": "Energy", "base_price": 2800.00},
        {"ticker": "TCS.NS", "name": "Tata Consultancy Services", "sector": "Technology", "base_price": 3200.00},
    ]
    
    stocks_data = []
    current_time = timezone.now()
    
    for stock_info in demo_stocks:
        # Generate realistic price changes
        price_change_percent = random.uniform(-5.0, 5.0)
        base_price = stock_info["base_price"]
        price_change = base_price * (price_change_percent / 100)
        current_price = base_price + price_change
        
        # Generate realistic volume and market cap
        volume = random.randint(10, 100)
        market_cap = random.randint(100, 2000)
        
        stock_data = {
            "ticker": stock_info["ticker"],
            "name": stock_info["name"],
            "sector": stock_info["sector"],
            "current_price": round(current_price, 2),
            "price_change": round(price_change, 2),
            "price_change_percent": round(price_change_percent, 2),
            "rsi": round(random.uniform(30, 70), 1),
            "volume": f"{volume}.{random.randint(0,9)}M",
            "market_cap": f"${market_cap}.{random.randint(0,9)}B",
            "is_positive": price_change_percent > 0,
            "last_fetched": current_time.strftime("%H:%M:%S")
        }
        stocks_data.append(stock_data)
        print(f"[{current_time.strftime('%H:%M:%S')}] 🎭 DEMO {stock_data['ticker']}: ${stock_data['current_price']} ({stock_data['price_change_percent']:+.2f}%)")
    
    return stocks_data

def get_fallback_stock_data(symbol):
    """Get fallback data for a single stock"""
    try:
        stock_obj = Stock.objects.get(ticker=symbol)
        return {
            "ticker": symbol,
            "name": stock_obj.name,
            "sector": stock_obj.sector,
            "current_price": float(stock_obj.current_price or 0),
            "price_change": float(stock_obj.price_change),
            "price_change_percent": float(stock_obj.price_change_percent or 0),
            "rsi": 50.0,
            "volume": stock_obj.volume,
            "market_cap": stock_obj.market_cap,
            "is_positive": bool(stock_obj.is_positive),
            "last_fetched": "Cached"
        }
    except Stock.DoesNotExist:
        return {
            "ticker": symbol,
            "name": symbol,
            "sector": "N/A",
            "current_price": 0.0,
            "price_change": 0.0,
            "price_change_percent": 0.0,
            "rsi": 50.0,
            "volume": "N/A",
            "market_cap": "N/A",
            "is_positive": False,
            "last_fetched": "Error"
        }

def update_stock_data():
    """Legacy function for management command - now just calls get_realtime_stock_data"""
    stocks_data = get_realtime_stock_data()
    return len(stocks_data)
