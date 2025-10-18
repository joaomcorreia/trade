#!/usr/bin/env python3

import requests
import time
import json

def test_news_api():
    try:
        # Test positive news
        print("🔍 Testing News API...")
        response = requests.get('http://localhost:8002/api/v1/news/positive', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {response.status_code}")
            print(f"📰 Sample Headline: {data['news'][0]['headline']}")
            print(f"📍 Source: {data['news'][0]['source']}")
            print(f"🕒 Timestamp: {data['news'][0]['timestamp']}")
            
            # Check if it contains real market data
            headline = data['news'][0]['headline']
            if any(price in headline for price in ['$', '€', '%']) and not headline.startswith('Tech Giants'):
                print("✅ Real market data detected in headline!")
            else:
                print("❌ Possible demo data detected")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_news_api()