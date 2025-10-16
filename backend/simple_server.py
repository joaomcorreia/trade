from fastapi import FastAPI
import asyncio

# Simple FastAPI app for testing
app = FastAPI(
    title="AI Trading Dashboard",
    description="Autonomous trading system with AI assistant",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "AI Trading Dashboard is running!", "status": "success"}

@app.get("/health")
async def health():
    return {"status": "healthy", "server": "FastAPI", "port": 8001}

@app.get("/api/test")
async def test_api():
    return {"message": "API is working!", "endpoints": ["/ ", "/health", "/api/test"]}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI Trading Dashboard Backend...")
    print("📡 Server will be available at: http://127.0.0.1:8001")
    print("📝 API Documentation: http://127.0.0.1:8001/docs")
    print("💡 Press Ctrl+C to stop the server")
    
    try:
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8001,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        input("Press Enter to exit...")