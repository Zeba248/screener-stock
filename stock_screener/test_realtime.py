#!/usr/bin/env python3
"""
Simple test script for real-time stock data fetching
"""

import os
import sys
import django
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_screener.settings')
django.setup()

from stocks.views import get_realtime_stock_data

def test_realtime_fetch():
    print("=" * 50)
    print("TESTING REAL-TIME STOCK DATA FETCH")
    print("=" * 50)
    
    start_time = time.time()
    
    try:
        stocks_data = get_realtime_stock_data()
        end_time = time.time()
        
        print(f"\n✅ SUCCESS: Fetched {len(stocks_data)} stocks in {end_time - start_time:.2f} seconds")
        print("\nStock Data:")
        print("-" * 70)
        
        for stock in stocks_data:
            status = "🟢" if stock['is_positive'] else "🔴"
            print(f"{status} {stock['ticker']:8} | ${stock['current_price']:8.2f} | {stock['price_change_percent']:+6.2f}% | {stock['last_fetched']}")
        
        print("-" * 70)
        print(f"Total stocks: {len(stocks_data)}")
        
        # Test if data looks reasonable
        has_prices = sum(1 for s in stocks_data if s['current_price'] > 0)
        print(f"Stocks with prices: {has_prices}/{len(stocks_data)}")
        
        if has_prices > 0:
            print("🎉 REAL-TIME DATA FETCH IS WORKING!")
        else:
            print("⚠️  No live prices found, but function completed")
            
    except Exception as e:
        end_time = time.time()
        print(f"❌ ERROR after {end_time - start_time:.2f} seconds: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_realtime_fetch()