@echo off
echo ========================================
echo    AI Trading Platform Launcher
echo ========================================
echo Starting AI Trading Platform...
echo.

REM Check if we're in the right directory
if not exist "complete_ai_backend.py" (
    echo Error: complete_ai_backend.py not found!
    echo Please run this from the C:\projects\trade directory
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
python -c "import fastapi, uvicorn, yfinance, sqlalchemy, databases, aiosqlite" 2>nul
if errorlevel 1 (
    echo Installing missing dependencies...
    pip install fastapi uvicorn yfinance sqlalchemy databases aiosqlite websockets requests
)

echo [2/3] Starting Backend Server (Port 8001)...
start "AI Trading Backend" cmd /k "python complete_ai_backend.py"

REM Wait for backend to start
timeout /t 5 /nobreak >nul

echo [3/3] Starting Frontend Dashboard (Port 3000)...
start "AI Trading Frontend" cmd /k "python -m http.server 3000"

REM Wait a moment for servers to initialize
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   AI Trading Platform Started!
echo ========================================
echo.
echo Backend API:    http://localhost:8001
echo API Docs:       http://localhost:8001/docs
echo WebSocket:      ws://localhost:8001/ws
echo Frontend:       http://localhost:3000
echo Dashboard:      http://localhost:3000/ai_trading_dashboard.html
echo.
echo Press any key to open the dashboard...
pause >nul

REM Open the dashboard in default browser
start http://localhost:3000/ai_trading_dashboard.html

echo.
echo Platform is running! Press any key to stop all services...
pause >nul

echo.
echo Stopping services...
taskkill /f /im python.exe >nul 2>&1
echo All services stopped.
pause