"""
Simple Platform Status Checker
Just checks if servers are responding
"""
import requests
import json

def check_status():
    print("🔍 AI Trading Platform Status Check")
    print("=" * 40)
    
    # Check Backend
    try:
        r = requests.get("http://localhost:8002/", timeout=3)
        print("✅ Backend Server: RUNNING (Port 8002)")
        print(f"   Status: {r.status_code}")
    except:
        print("❌ Backend Server: OFFLINE")
    
    # Check Frontend  
    try:
        r = requests.get("http://localhost:3000/", timeout=3)
        print("✅ Frontend Server: RUNNING (Port 3000)")
        print(f"   Status: {r.status_code}")
    except:
        print("❌ Frontend Server: OFFLINE")
    
    print()
    print("🔗 Access Links:")
    print("   📊 API Docs: http://localhost:8002/docs")
    print("   📈 Dashboard: http://localhost:3000/ai_trading_dashboard.html")
    print("   ⚡ WebSocket: ws://localhost:8002/ws")

if __name__ == "__main__":
    check_status()