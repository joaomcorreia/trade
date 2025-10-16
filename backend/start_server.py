#!/usr/bin/env python3
"""
Startup script for the trading dashboard backend.
This script directly imports and runs the FastAPI application.
"""

import sys
import os
import uvicorn

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the FastAPI app
from app.main import app

if __name__ == "__main__":
    # Start the server
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[current_dir]
    )