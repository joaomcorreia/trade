#!/usr/bin/env python3
"""Test script to verify news API is working"""

import requests
import json

def test_news_api():
    try:
        print("🔍 Testing News API...")
        
        # Test positive news
        response = requests.get('http://localhost:8002/api/v1/news/positive')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Positive News API: {response.status_code}")
            print(f"   📰 Headlines ({len(data['news'])} total):")
            for i, news in enumerate(data['news'][:3]):
                print(f"   {i+1}. {news['headline']}")
                print(f"      Source: {news['source']} | Time: {news['timestamp'][:19]}")
            
            # Check market context
            if 'market_context' in data:
                ctx = data['market_context']
                print(f"   💰 Market Context: BTC=${ctx.get('btc_price', 'N/A')}, ETH=${ctx.get('eth_price', 'N/A')}")
                print(f"   📊 Data Source: {ctx.get('data_source', 'Unknown')}")
        else:
            print(f"❌ Positive News API failed: {response.status_code}")
            
        # Test negative news
        response = requests.get('http://localhost:8002/api/v1/news/negative')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Negative News API: {response.status_code}")
            print(f"   📉 Sample headline: {data['news'][0]['headline'][:60]}...")
        else:
            print(f"❌ Negative News API failed: {response.status_code}")
            
        # Test general news
        response = requests.get('http://localhost:8002/api/v1/news/general')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ General News API: {response.status_code}")
            print(f"   📊 Sample headline: {data['news'][0]['headline'][:60]}...")
        else:
            print(f"❌ General News API failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server on port 8002")
        print("   Make sure the backend is running: python complete_ai_backend.py")
    except Exception as e:
        print(f"❌ Error testing API: {str(e)}")

if __name__ == "__main__":
    test_news_api()