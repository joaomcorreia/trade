#!/usr/bin/env python3
"""Test if frontend can reach backend - CORS test"""

import requests

def test_cors():
    """Test CORS headers and connectivity"""
    try:
        print("🔍 Testing CORS and connectivity...")
        
        # Test with browser-like headers
        headers = {
            'Origin': 'http://localhost:3000',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        response = requests.get('http://localhost:8002/api/v1/news/positive', headers=headers)
        
        print(f"✅ Response Status: {response.status_code}")
        print(f"✅ CORS Headers:")
        print(f"   Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin', 'NOT SET')}")
        print(f"   Access-Control-Allow-Methods: {response.headers.get('access-control-allow-methods', 'NOT SET')}")
        print(f"   Content-Type: {response.headers.get('content-type', 'NOT SET')}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ News Data Available: {len(data.get('news', []))} articles")
            print(f"✅ Sample Headline: {data['news'][0]['headline'][:80]}...")
            
            # Check if market data is embedded
            if 'market_context' in data:
                print(f"✅ Real Market Data: BTC=${data['market_context']['btc_price']}")
            else:
                print("⚠️  No market context found")
        else:
            print(f"❌ API request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_frontend_server():
    """Test if frontend server is accessible"""
    try:
        response = requests.get('http://localhost:3000/ai_trading_dashboard.html')
        print(f"✅ Frontend Server: {response.status_code}")
        print(f"   Content Length: {len(response.text)} characters")
    except Exception as e:
        print(f"❌ Frontend Error: {str(e)}")

if __name__ == "__main__":
    test_frontend_server()
    print()
    test_cors()