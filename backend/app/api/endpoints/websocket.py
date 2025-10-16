from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket import manager
import asyncio
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    # Start market data stream if this is the first connection
    if len(manager.active_connections) == 1:
        asyncio.create_task(manager.start_market_data_stream())
    
    try:
        while True:
            # Keep connection alive and handle client messages
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "subscribe":
                    # Client wants to subscribe to specific symbols
                    symbols = message.get("symbols", [])
                    response = {
                        "type": "subscription_confirmed",
                        "symbols": symbols
                    }
                    await manager.send_personal_message(json.dumps(response), websocket)
                
                elif message.get("type") == "ping":
                    # Heartbeat
                    await manager.send_personal_message('{"type": "pong"}', websocket)
                
            except json.JSONDecodeError:
                await manager.send_personal_message('{"type": "error", "message": "Invalid JSON"}', websocket)
            except Exception as e:
                logger.error(f"Error handling WebSocket message: {e}")
                await manager.send_personal_message(f'{{"type": "error", "message": "{str(e)}"}}', websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)