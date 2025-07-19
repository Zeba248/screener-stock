# Django Stock Screener (Real-time)

This is a Django-based stock screener application with **REAL-TIME** stock data fetching. Every page load retrieves fresh data from Yahoo Finance, ensuring you always see the latest stock prices and changes.

## ✨ Key Features

- **🔴 REAL-TIME DATA**: Fresh stock data on every page load (no caching)
- **💹 Current Prices**: Live stock prices with price change calculations
- **⏱️ Timestamps**: Individual "last fetched" time for each stock
- **🎯 Smart Sorting**: Sort by price change, current price, volume, or market cap
- **📱 Modern UI**: Bootstrap 5 responsive design with live indicators
- **🔧 Admin Interface**: Django admin for data management
- **🚀 Performance**: Optimized real-time fetching with fallback handling

## 🚀 Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Setup database:**
```bash
python manage.py migrate
```

3. **Start with real-time data:**
```bash
python run_django.py
```
*OR manually:*
```bash
python manage.py runserver
```

4. **Open your browser:** `http://127.0.0.1:8000/`

## 📊 Real-time Behavior

- **No Caching**: Data is fetched fresh from Yahoo Finance on every request
- **Live Updates**: Each page refresh shows the latest prices
- **Individual Timestamps**: See when each stock was last fetched
- **Fallback System**: Uses database data if API fails
- **Performance**: Optimized to handle real-time requests efficiently

## 🎛️ Usage

### Web Interface
- **Main Page**: Real-time stock data with live indicators
- **Refresh Button**: Manual refresh for latest data
- **Sorting**: Click dropdown to sort by different metrics
- **Live Badge**: Animated indicator showing real-time status

### API Endpoints
- `/` - Real-time stock screener page
- `/stocks.json` - JSON API with live stock data
- `/admin/` - Django admin interface

### Management Commands
```bash
# Fetch and display real-time data
python manage.py update_stocks

# Standard Django commands
python manage.py createsuperuser
python manage.py shell
```

## 📈 Stock Data Fields

Each stock displays:
- **Current Price**: Live price in USD
- **Price Change**: Absolute change from previous close
- **Price Change %**: Percentage change (with color coding)
- **Volume**: Trading volume (formatted as M/B)
- **Market Cap**: Market capitalization
- **Last Fetched**: Individual timestamp per stock
- **RSI**: Relative Strength Index (placeholder: 50)

## 🎨 UI Features

- **Live Badge**: Animated "🔴 LIVE" indicator
- **Color Coding**: Green for gains, red for losses
- **Refresh Button**: Manual data refresh option
- **Responsive Design**: Works on desktop and mobile
- **Loading States**: Graceful handling of API delays
- **Error Handling**: Fallback to cached data when needed

## ⚡ Performance Considerations

### Optimizations:
- **Concurrent Fetching**: Parallel API calls for multiple stocks
- **Database Fallback**: Uses cached data if API fails
- **Error Handling**: Graceful degradation for failed requests
- **Efficient Queries**: Optimized database operations

### Real-time vs Performance:
- Each page load = ~2-3 seconds (API dependent)
- Database fallback for reliability
- No background tasks needed
- Scales well for small-medium traffic

## 🛠️ Technical Architecture

- **Django 5.2.4**: Web framework and ORM
- **yfinance**: Real-time Yahoo Finance API
- **SQLite**: Database with fallback data
- **Bootstrap 5**: Modern UI components
- **Server-side Rendering**: No JavaScript required for data

## 📝 Stock Tickers

Currently tracking:
- **TSLA** - Tesla, Inc. (NASDAQ)
- **AAPL** - Apple Inc. (NASDAQ)
- **INFY.NS** - Infosys Limited (NSE)
- **RELIANCE.NS** - Reliance Industries (NSE)
- **TCS.NS** - Tata Consultancy Services (NSE)

## 🔄 Real-time vs Original Flask

### Improvements over Flask version:
1. **True Real-time**: No 30-minute caching
2. **Individual Timestamps**: Per-stock fetch times
3. **Current Prices**: Live price display
4. **Better Error Handling**: Fallback mechanisms
5. **Performance Optimized**: Efficient real-time fetching
6. **Enhanced UI**: Live indicators and better UX

### Performance Impact:
- **Flask**: Static JSON file (fast, outdated)
- **Django Real-time**: Live API calls (2-3s, always fresh)

## 🚨 Important Notes

- **API Limits**: Yahoo Finance has rate limits
- **Market Hours**: Some data may be delayed outside trading hours
- **Network Dependent**: Requires internet for real-time data
- **Fallback Available**: Uses database if API fails

## 🎯 Development

```bash
# Run in development with debug info
python manage.py runserver --verbosity=2

# Test real-time fetching
python manage.py update_stocks

# Check database content
python manage.py shell
>>> from stocks.models import Stock
>>> Stock.objects.all()
```

---

**🔴 LIVE DATA GUARANTEE**: This application fetches fresh stock data on every page load, ensuring you always see the most current market information available through Yahoo Finance.