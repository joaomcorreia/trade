"""
Quick Status Check & Restart Script
===================================
Use this to check if your platform is running and restart if needed
"""

import requests
import subprocess
import time
import os

def check_server_status():
    """Check if servers are running"""
    backend_running = False
    frontend_running = False
    
    try:
        response = requests.get("http://localhost:8001/", timeout=2)
        if response.status_code == 200:
            backend_running = True
            print("✅ Backend server: RUNNING (port 8001)")
        else:
            print("❌ Backend server: NOT RESPONDING")
    except:
        print("❌ Backend server: OFFLINE")
    
    try:
        response = requests.get("http://localhost:3000/", timeout=2)
        if response.status_code == 200:
            frontend_running = True
            print("✅ Frontend server: RUNNING (port 3000)")
        else:
            print("❌ Frontend server: NOT RESPONDING")
    except:
        print("❌ Frontend server: OFFLINE")
    
    return backend_running, frontend_running

def start_servers():
    """Start the servers if they're not running"""
    print("🚀 Starting AI Trading Platform servers...")
    
    # Start backend
    print("📊 Starting backend server...")
    subprocess.Popen(["python", "complete_ai_backend.py"], 
                    creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    # Wait a bit for backend to start
    time.sleep(3)
    
    # Start frontend
    print("🌐 Starting frontend server...")
    subprocess.Popen(["python", "-m", "http.server", "3000"], 
                    creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    # Wait for everything to initialize
    time.sleep(2)

def main():
    print("🔍 AI Trading Platform - Status Check")
    print("=" * 50)
    
    backend_running, frontend_running = check_server_status()
    
    if backend_running and frontend_running:
        print("\n🎉 Platform is FULLY OPERATIONAL!")
        print("\n🔗 Access your platform:")
        print("   📊 Trading Dashboard: http://localhost:3000/ai_trading_dashboard.html")
        print("   📚 API Documentation: http://localhost:8001/docs")
        print("   ⚡ WebSocket: ws://localhost:8001/ws")
    
    elif not backend_running or not frontend_running:
        print(f"\n⚠️  Platform Status: PARTIALLY OFFLINE")
        
        restart = input("\n🔄 Would you like to restart the servers? (y/n): ").lower()
        if restart == 'y':
            start_servers()
            
            print("\n⏱️  Checking status after restart...")
            time.sleep(5)
            
            backend_running, frontend_running = check_server_status()
            
            if backend_running and frontend_running:
                print("\n✅ Platform successfully restarted!")
                print("\n🔗 Access your platform:")
                print("   📊 Trading Dashboard: http://localhost:3000/ai_trading_dashboard.html")
                print("   📚 API Documentation: http://localhost:8001/docs")
            else:
                print("\n❌ Some servers failed to start. Check for errors in the console windows.")

if __name__ == "__main__":
    main()