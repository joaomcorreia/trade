"""
Test Yahoo Finance Integration
"""
import asyncio
import yfinance as yf
import requests
import json
from datetime import datetime

async def test_yahoo_finance_direct():
    """Test Yahoo Finance API directly"""
    print("🧪 Testing Yahoo Finance Direct API...")
    
    try:
        ticker = yf.Ticker("AAPL")
        info = ticker.info
        hist = ticker.history(period="2d")
        
        if len(hist) >= 2:
            current_price = hist['Close'].iloc[-1]
            previous_price = hist['Close'].iloc[-2]
            change = current_price - previous_price
            change_percent = (change / previous_price) * 100
            
            print(f"✅ AAPL Real Price: ${current_price:.2f}")
            print(f"📈 Change: ${change:.2f} ({change_percent:.2f}%)")
            print(f"🏢 Company: {info.get('longName', 'Apple Inc.')}")
            return True
        else:
            print("❌ Not enough historical data")
            return False
            
    except Exception as e:
        print(f"❌ Yahoo Finance Error: {e}")
        return False

def test_backend_api():
    """Test our enhanced backend API"""
    print("\n🧪 Testing Enhanced Backend API...")
    
    try:
        # Test market price endpoint
        response = requests.get("http://localhost:8000/api/v1/market/price/AAPL", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend AAPL Price: ${data['price']:.2f}")
            print(f"📊 Source: {data['source']}")
            print(f"📈 Change: {data['change']:.2f} ({data['change_percent']:.2f}%)")
            
            # Test AI signals
            signals_response = requests.get("http://localhost:8000/api/v1/trading/ai-signals", timeout=10)
            if signals_response.status_code == 200:
                signals_data = signals_response.json()
                print(f"🤖 AI Signals: {len(signals_data['signals'])} generated")
                for signal in signals_data['signals'][:2]:
                    print(f"   📊 {signal['symbol']}: {signal['action'].upper()} (confidence: {signal['confidence']:.1%})")
            
            return True
        else:
            print(f"❌ Backend API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Backend Test Error: {e}")
        return False

async def main():
    print("🚀 Testing Real Market Data Integration\n")
    
    # Test Yahoo Finance directly
    yf_success = await test_yahoo_finance_direct()
    
    # Test our backend API
    backend_success = test_backend_api()
    
    print(f"\n📊 Test Results:")
    print(f"   Yahoo Finance: {'✅ Working' if yf_success else '❌ Failed'}")
    print(f"   Backend API: {'✅ Working' if backend_success else '❌ Failed'}")
    
    if yf_success and backend_success:
        print("\n🎉 Real Market Data Integration is working!")
    else:
        print("\n⚠️  Some components need attention")

if __name__ == "__main__":
    asyncio.run(main())