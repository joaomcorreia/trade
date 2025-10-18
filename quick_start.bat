@echo off
echo Starting AI Trading Platform...

REM Kill any existing Python processes to avoid conflicts
taskkill /f /im python.exe >nul 2>&1

REM Start backend server
echo Starting backend on port 8001...
start "Backend" cmd /c "python complete_ai_backend.py"

REM Wait for backend to initialize
timeout /t 3 /nobreak >nul

REM Start frontend server
echo Starting frontend on port 3000...
start "Frontend" cmd /c "python -m http.server 3000"

REM Wait for frontend to initialize
timeout /t 2 /nobreak >nul

echo.
echo ================================
echo  Platform Started Successfully!
echo ================================
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:3000
echo Dashboard: http://localhost:3000/ai_trading_dashboard.html
echo.

REM Open dashboard
start http://localhost:3000/ai_trading_dashboard.html

echo Platform is running in separate windows.
echo Close this window when done.
pause