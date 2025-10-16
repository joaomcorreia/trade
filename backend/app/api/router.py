from fastapi import APIRouter
from app.api.endpoints import market, trading, ai, analysis, websocket

router = APIRouter()

# Include all endpoint routers
router.include_router(market.router, prefix="/market", tags=["market"])
router.include_router(trading.router, prefix="/trading", tags=["trading"])
router.include_router(ai.router, prefix="/ai", tags=["ai"])
router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
router.include_router(websocket.router, prefix="/ws", tags=["websocket"])