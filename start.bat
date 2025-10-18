@echo off
echo Starting AI Trading Dashboard...
echo.

echo [1/2] Starting Backend Server...
start "AI Trading Backend" cmd /k "python ai_trading_backend.py"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Dashboard...
start "AI Trading Dashboard" cmd /k "python -m http.server 3000"

echo.
echo Dashboard will be available at: http://localhost:3000/ai_trading_dashboard.html
echo Backend API at: http://localhost:8000
echo.
echo Press any key to exit...
pause >nul