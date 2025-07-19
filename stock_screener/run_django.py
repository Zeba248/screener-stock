#!/usr/bin/env python3
"""
Simple startup script for the Django Stock Screener (Real-time)
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and print status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Starting Django Stock Screener (Real-time) Setup...")
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the Django project directory.")
        sys.exit(1)
    
    # Run migrations
    if not run_command("python3 manage.py migrate", "Running database migrations"):
        sys.exit(1)
    
    # Test real-time data fetch (optional)
    print("🔄 Testing real-time stock data fetch...")
    if run_command("python3 manage.py update_stocks", "Fetching real-time stock data"):
        print("✅ Real-time data fetch successful!")
    else:
        print("⚠️  Warning: Real-time data fetch failed, but continuing...")
    
    # Start the development server
    print("\n🎯 Starting Django development server with REAL-TIME stock data...")
    print("📱 Open your browser and go to: http://127.0.0.1:8000/")
    print("🔧 Admin interface available at: http://127.0.0.1:8000/admin/")
    print("🔴 LIVE DATA: Each page refresh fetches fresh data from Yahoo Finance")
    print("🛑 Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run("python3 manage.py runserver", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 Django server stopped. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()