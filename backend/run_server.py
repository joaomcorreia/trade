"""
Simple server runner for the trading dashboard
"""

import os
import sys

if __name__ == "__main__":
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current directory: {current_dir}")

    # Add current directory to Python path
    sys.path.insert(0, current_dir)
    print(f"Python path: {sys.path}")

    # Set environment variable
    os.environ['PYTHONPATH'] = current_dir

    # Change to the backend directory
    os.chdir(current_dir)
    print(f"Working directory: {os.getcwd()}")

    # Check if app directory exists
    app_dir = os.path.join(current_dir, 'app')
    print(f"App directory exists: {os.path.exists(app_dir)}")

    if os.path.exists(app_dir):
        print("Contents of app directory:")
        for item in os.listdir(app_dir):
            print(f"  {item}")

    # Try to import the app
    try:
        print("Attempting to import app.main...")
        from app.main import app as fastapi_app
        print("Successfully imported FastAPI app!")
        
        # Run with uvicorn using import string - no reload on Windows
        import uvicorn
        print("Starting uvicorn server...")
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8001,
            reload=False  # Disable reload on Windows to avoid multiprocessing issues
        )
        
    except Exception as e:
        print(f"Error importing or running app: {e}")
        import traceback
        traceback.print_exc()