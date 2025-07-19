from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import Stock
import yfinance as yf
import json
from datetime import datetime
import logging

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
    """Fetch real-time stock data from Yahoo Finance"""
    tickers = ['TSLA', 'AAPL', 'INFY.NS', 'RELIANCE.NS', 'TCS.NS']
    stocks_data = []
    current_time = timezone.now()
    
    for symbol in tickers:
        try:
            # Fetch real-time data from Yahoo Finance
            stock = yf.Ticker(symbol)
            
            # Get current price and info
            info = stock.info
            hist = stock.history(period="2d")  # Get last 2 days for price change calculation
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                if len(hist) > 1:
                    previous_price = hist['Close'].iloc[-2]
                    price_change = current_price - previous_price
                    price_change_percent = (price_change / previous_price) * 100
                else:
                    price_change = 0
                    price_change_percent = 0
            else:
                current_price = info.get("currentPrice", 0)
                price_change_percent = info.get("regularMarketChangePercent", 0)
                price_change = info.get("regularMarketChange", 0)
            
            volume = info.get("volume") or info.get("regularMarketVolume")
            market_cap = info.get("marketCap")
            
            stock_data = {
                "ticker": symbol,
                "name": info.get("shortName", symbol),
                "sector": info.get("sector", "N/A"),
                "current_price": round(current_price, 2) if current_price else 0,
                "price_change": round(price_change, 2) if price_change else 0,
                "price_change_percent": round(price_change_percent, 2),
                "rsi": 50,  # Placeholder - would need additional calculation
                "volume": f"{volume/1e6:.1f}M" if volume else "N/A",
                "market_cap": f"${market_cap/1e9:.1f}B" if market_cap else "N/A",
                "is_positive": price_change_percent > 0,
                "last_fetched": current_time.strftime("%H:%M:%S")
            }
            
            stocks_data.append(stock_data)
            
            # Update database record for persistence (optional)
            stock_obj, created = Stock.objects.get_or_create(
                ticker=symbol,
                defaults={
                    'name': stock_data['name'],
                    'sector': stock_data['sector']
                }
            )
            
            # Update with latest data
            stock_obj.name = stock_data['name']
            stock_obj.sector = stock_data['sector']
            stock_obj.current_price = stock_data['current_price']
            stock_obj.price_change = stock_data['price_change']
            stock_obj.price_change_percent = stock_data['price_change_percent']
            stock_obj.volume = stock_data['volume']
            stock_obj.market_cap = stock_data['market_cap']
            stock_obj.is_positive = stock_data['is_positive']
            stock_obj.last_fetched = current_time
            stock_obj.save()
            
            logger.info(f"✅ Fetched real-time data for {symbol}: ${stock_data['current_price']}")
            
        except Exception as e:
            logger.error(f"❌ Error fetching data for {symbol}: {e}")
            
            # Try to get data from database as fallback
            try:
                stock_obj = Stock.objects.get(ticker=symbol)
                stock_data = {
                    "ticker": symbol,
                    "name": stock_obj.name,
                    "sector": stock_obj.sector,
                    "current_price": stock_obj.current_price or 0,
                    "price_change": stock_obj.price_change,
                    "price_change_percent": stock_obj.price_change_percent or 0,
                    "rsi": stock_obj.rsi,
                    "volume": stock_obj.volume,
                    "market_cap": stock_obj.market_cap,
                    "is_positive": stock_obj.is_positive,
                    "last_fetched": stock_obj.last_fetched.strftime("%H:%M:%S") if stock_obj.last_fetched else "N/A"
                }
                stocks_data.append(stock_data)
            except Stock.DoesNotExist:
                # Create placeholder entry
                stock_data = {
                    "ticker": symbol,
                    "name": symbol,
                    "sector": "N/A",
                    "current_price": 0,
                    "price_change": 0,
                    "price_change_percent": 0,
                    "rsi": 50,
                    "volume": "N/A",
                    "market_cap": "N/A",
                    "is_positive": False,
                    "last_fetched": "Error"
                }
                stocks_data.append(stock_data)
    
    return stocks_data

def update_stock_data():
    """Legacy function for management command - now just calls get_realtime_stock_data"""
    stocks_data = get_realtime_stock_data()
    return len(stocks_data)
