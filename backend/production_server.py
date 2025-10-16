#!/usr/bin/env python3
"""
Production server for JCW Trade Hub
Optimized for CyberPanel deployment
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Set environment variables
os.environ['PYTHONPATH'] = str(current_dir)

def main():
    """Main entry point for production server"""
    try:
        # Import the FastAPI app
        from app.main import app
        
        # Production server configuration
        import uvicorn
        
        # Get configuration from environment
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 8001))
        
        print(f"🚀 Starting JCW Trade Hub Production Server")
        print(f"🌐 Host: {host}:{port}")
        print(f"📡 Environment: {os.getenv('ENVIRONMENT', 'production')}")
        print(f"🎯 Domain: jcwtradehub.com")
        
        # Start the production server
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True,
            reload=False  # Disabled in production
        )
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Server Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()