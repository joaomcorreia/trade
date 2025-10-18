#!/usr/bin/env python3

# Quick manual test to simulate what the frontend should see
import requests
import json

def quick_test():
    """Simulate exactly what the frontend fetch should see"""
    try:
        print("🚀 Starting backend test...")
        
        # First start backend (you need to run this separately)
        print("📡 Testing news API...")
        
        response = requests.get('http://localhost:8002/api/v1/news/positive', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📰 Total news items: {len(data['news'])}")
            
            for i, item in enumerate(data['news'][:3]):
                print(f"\n--- News Item {i+1} ---")
                print(f"Headline: {item['headline']}")
                print(f"Source: {item['source']}")
                print(f"Timestamp: {item['timestamp']}")
                
                # Check if this contains actual market data
                headline = item['headline']
                if any(indicator in headline for indicator in ['$', '€', '%', 'Bitcoin', 'Ethereum', 'BTC', 'ETH']):
                    print("✅ Contains real market data!")
                else:
                    print("⚠️  May be demo data")
                    
            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running! Start with: python complete_ai_backend.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    quick_test()