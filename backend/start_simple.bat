@echo off
cd /d "C:\projects\trade\backend"
call venv\Scripts\activate.bat
echo Starting AI Trading Dashboard Backend Server...
echo Server will be available at http://localhost:8001
echo Press Ctrl+C to stop the server
python simple_server.py
pause