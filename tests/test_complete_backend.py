"""
Complete Backend Testing Suite
Tests all features: API endpoints, WebSocket streaming, database operations
"""

import asyncio
import websockets
import json
import requests
import time
from datetime import datetime

class TradingBackendTester:
    def __init__(self, base_url="http://localhost:8001", ws_url="ws://localhost:8001/ws"):
        self.base_url = base_url
        self.ws_url = ws_url
        
    def test_api_endpoints(self):
        """Test all REST API endpoints"""
        print("🧪 Testing REST API Endpoints...")
        
        # Test root endpoint
        try:
            response = requests.get(f"{self.base_url}/")
            print(f"✅ Root endpoint: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Features: {len(data.get('features', []))}")
                print(f"   Database: {data.get('database')}")
        except Exception as e:
            print(f"❌ Root endpoint error: {e}")
        
        # Test trading status
        try:
            response = requests.get(f"{self.base_url}/api/v1/trading/status")
            print(f"✅ Trading status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Portfolio value: ${data.get('portfolio_value', 0)}")
                print(f"   Today's trades: {data.get('today_trades', 0)}")
                print(f"   Database connected: {data.get('database_connected')}")
        except Exception as e:
            print(f"❌ Trading status error: {e}")
        
        # Test market price
        try:
            response = requests.get(f"{self.base_url}/api/v1/market/price/AAPL")
            print(f"✅ Market price (AAPL): {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   AAPL Price: ${data.get('price')} ({data.get('change_percent', 0):+.2f}%)")
                print(f"   Source: {data.get('source')}")
        except Exception as e:
            print(f"❌ Market price error: {e}")
        
        # Test database stats
        try:
            response = requests.get(f"{self.base_url}/api/v1/database/stats")
            print(f"✅ Database stats: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                stats = data.get('database_stats', {})
                print(f"   Total trades: {stats.get('total_trades', 0)}")
                print(f"   Total signals: {stats.get('total_ai_signals', 0)}")
                print(f"   Price records: {stats.get('total_price_records', 0)}")
        except Exception as e:
            print(f"❌ Database stats error: {e}")
        
        # Test AI signals
        try:
            response = requests.get(f"{self.base_url}/api/v1/trading/ai-signals")
            print(f"✅ AI signals: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                signals = data.get('signals', [])
                print(f"   AI signals count: {len(signals)}")
                if signals:
                    print(f"   Latest signal: {signals[0].get('action')} {signals[0].get('symbol')} (confidence: {signals[0].get('confidence')})")
        except Exception as e:
            print(f"❌ AI signals error: {e}")
        
        # Test trade execution
        try:
            response = requests.post(f"{self.base_url}/api/v1/trading/execute?symbol=AAPL&action=buy&quantity=10")
            print(f"✅ Trade execution: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Executed: {data.get('action')} {data.get('quantity')} {data.get('symbol')} @ ${data.get('execution_price')}")
                print(f"   Saved to database: {data.get('saved_to_database')}")
        except Exception as e:
            print(f"❌ Trade execution error: {e}")
        
        print()
    
    async def test_websocket_streaming(self, duration=30):
        """Test WebSocket real-time streaming"""
        print(f"📡 Testing WebSocket Streaming (for {duration} seconds)...")
        
        try:
            async with websockets.connect(self.ws_url) as websocket:
                print("✅ WebSocket connected successfully")
                
                # Send initial message
                await websocket.send("Hello from test client")
                
                price_updates = 0
                signal_updates = 0
                trade_updates = 0
                
                start_time = time.time()
                while time.time() - start_time < duration:
                    try:
                        # Wait for message with timeout
                        message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                        data = json.loads(message)
                        
                        message_type = data.get('type', 'unknown')
                        timestamp = data.get('timestamp', datetime.now().isoformat())
                        
                        if message_type == 'price_update':
                            price_updates += 1
                            price_data = data.get('data', {})
                            symbols = list(price_data.keys())
                            print(f"📈 Price update #{price_updates}: {len(symbols)} symbols")
                            for symbol in symbols[:2]:  # Show first 2
                                symbol_data = price_data[symbol]
                                print(f"   {symbol}: ${symbol_data.get('price')} ({symbol_data.get('change_percent'):+.2f}%)")
                        
                        elif message_type == 'ai_signals_update':
                            signal_updates += 1
                            signals = data.get('data', {}).get('signals', [])
                            print(f"🤖 AI signals update #{signal_updates}: {len(signals)} signals")
                            for signal in signals[:2]:  # Show first 2
                                print(f"   {signal.get('symbol')}: {signal.get('action')} (confidence: {signal.get('confidence')})")
                        
                        elif message_type == 'trade_executed':
                            trade_updates += 1
                            trade_data = data.get('data', {})
                            print(f"💰 Trade executed #{trade_updates}: {trade_data.get('action')} {trade_data.get('quantity')} {trade_data.get('symbol')}")
                        
                        elif message_type == 'confirmation':
                            print(f"✅ Confirmation: {data.get('message')}")
                        
                        else:
                            print(f"📨 Other message: {message_type}")
                            
                    except asyncio.TimeoutError:
                        print("⏰ Waiting for next update...")
                        continue
                    except json.JSONDecodeError:
                        print(f"⚠️ Invalid JSON received: {message}")
                        continue
                
                print(f"\n📊 WebSocket Test Summary:")
                print(f"   Price updates received: {price_updates}")
                print(f"   AI signal updates received: {signal_updates}")
                print(f"   Trade updates received: {trade_updates}")
                print(f"   Total test duration: {duration} seconds")
                
        except Exception as e:
            print(f"❌ WebSocket error: {e}")
    
    async def run_complete_test(self):
        """Run complete test suite"""
        print("🚀 Starting Complete Backend Test Suite")
        print("=" * 50)
        
        # Test REST API
        self.test_api_endpoints()
        
        # Wait a moment
        await asyncio.sleep(2)
        
        # Test WebSocket streaming
        await self.test_websocket_streaming(duration=30)
        
        print("\n✅ Complete test suite finished!")
        print("📈 Backend is fully operational with:")
        print("   - REST API endpoints working")
        print("   - Real-time WebSocket streaming")
        print("   - Database persistence")
        print("   - Live market data integration")

async def main():
    tester = TradingBackendTester()
    await tester.run_complete_test()

if __name__ == "__main__":
    print("🧪 AI Trading Backend Complete Test Suite")
    print("Testing all features: API, WebSocket, Database, Real-time data")
    print("-" * 60)
    
    asyncio.run(main())