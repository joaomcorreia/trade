#!/usr/bin/env python3
"""Test commodities data and fix gold price"""

import requests
import json

def test_commodities():
    try:
        response = requests.get('http://localhost:8002/api/v1/market/prices/commodities?limit=5')
        if response.status_code == 200:
            data = response.json()
            print("✅ Commodities Data:")
            for symbol, info in data['prices'].items():
                price = info['price']
                print(f"   {symbol}: ${price:,.2f}")
                if 'Gold' in symbol or 'GC=' in symbol:
                    if price > 3000:  # Gold should be around $2000-2100
                        print(f"   ⚠️  INCORRECT: Gold price {price} is too high!")
        else:
            print(f"❌ Failed to get commodities: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_commodities()