"""
Test WebSocket Real-time Connection
"""
import asyncio
import websockets
import json
from datetime import datetime

async def test_websocket():
    """Test the WebSocket connection for real-time updates"""
    uri = "ws://localhost:8000/ws"
    
    try:
        print("🔌 Connecting to WebSocket...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to real-time trading WebSocket!")
            
            # Send a test message
            await websocket.send("Hello WebSocket!")
            
            # Listen for updates for 30 seconds
            start_time = datetime.now()
            while (datetime.now() - start_time).seconds < 30:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(message)
                    
                    if data['type'] == 'price_update':
                        print(f"📊 Price Update: {len(data['data'])} symbols")
                        for symbol, price_data in data['data'].items():
                            print(f"   💰 {symbol}: ${price_data['price']} ({price_data['change_percent']:+.2f}%)")
                    
                    elif data['type'] == 'portfolio_update':
                        portfolio_value = data['data']['portfolio_value']
                        today_pnl = data['data']['today_pnl']
                        print(f"💼 Portfolio: ${portfolio_value:,.2f} (P&L: ${today_pnl:+,.2f})")
                    
                    elif data['type'] == 'ai_signals_update':
                        signals = data['data']['signals']
                        print(f"🤖 AI Signals: {len(signals)} new signals")
                        for signal in signals:
                            action = signal['action'].upper()
                            confidence = signal['confidence']
                            print(f"   📈 {signal['symbol']}: {action} ({confidence:.1%} confidence)")
                    
                    elif data['type'] == 'confirmation':
                        print(f"✅ {data['message']}")
                    
                except asyncio.TimeoutError:
                    print("⏱️  Waiting for updates...")
                    continue
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON: {message}")
                    continue
            
            print("🔚 Test completed!")
            
    except ConnectionRefusedError:
        print("❌ Could not connect to WebSocket. Is the server running?")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Real-time WebSocket Connection...")
    asyncio.run(test_websocket())