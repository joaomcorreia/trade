from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
from typing import List
import logging
from app.services.market_data import MarketDataService
from app.ai.trading_ai import TradingAI

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.market_service = MarketDataService()
        self.trading_ai = TradingAI()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connection established. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket connection closed. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

    async def send_market_update(self, symbol: str, data: dict):
        message = {
            "type": "market_update",
            "symbol": symbol,
            "data": data,
            "timestamp": data.get("timestamp")
        }
        await self.broadcast(json.dumps(message))

    async def send_trade_notification(self, trade_data: dict):
        message = {
            "type": "trade_notification",
            "data": trade_data
        }
        await self.broadcast(json.dumps(message))

    async def send_ai_alert(self, alert_data: dict):
        message = {
            "type": "ai_alert",
            "data": alert_data
        }
        await self.broadcast(json.dumps(message))

    async def start_market_data_stream(self):
        """Start streaming market data updates"""
        watchlist = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
        
        while True:
            try:
                for symbol in watchlist:
                    if self.active_connections:  # Only fetch if there are active connections
                        try:
                            # Get current price data
                            price_data = await self.market_service.get_current_price(symbol)
                            await self.send_market_update(symbol, price_data)
                            
                            # Get AI analysis periodically (every 5th update)
                            if hash(symbol) % 5 == 0:
                                try:
                                    ai_decision = await self.trading_ai.make_trading_decision(symbol)
                                    if ai_decision["confidence"] > 0.7:
                                        await self.send_ai_alert({
                                            "symbol": symbol,
                                            "decision": ai_decision["decision"],
                                            "confidence": ai_decision["confidence"],
                                            "reasoning": ai_decision["reasoning"]
                                        })
                                except Exception as e:
                                    logger.warning(f"Error getting AI decision for {symbol}: {e}")
                            
                            await asyncio.sleep(2)  # Delay between symbols
                        except Exception as e:
                            logger.error(f"Error fetching data for {symbol}: {e}")
                
                await asyncio.sleep(30)  # Wait 30 seconds before next full cycle
                
            except Exception as e:
                logger.error(f"Error in market data stream: {e}")
                await asyncio.sleep(60)  # Wait longer on error

manager = ConnectionManager()