@echo off
echo ====================================
echo   AI Trading Dashboard - Startup
echo ====================================
echo.
echo Starting Backend Server (FastAPI)...
echo Server will be available at: http://localhost:8001
echo API Documentation at: http://localhost:8001/docs
echo.

cd /d "C:\projects\trade\backend"
call venv\Scripts\activate.bat

start "AI Trading Backend" cmd /k "python simple_server.py"

timeout /t 3 /nobreak > nul

echo.
echo Starting Frontend Server (React)...
echo Dashboard will be available at: http://localhost:3000
echo.

cd /d "C:\projects\trade\frontend"
start "AI Trading Frontend" cmd /k "npm start"

echo.
echo ====================================
echo   🚀 AI Trading Dashboard Started!
echo ====================================
echo.
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8001/docs
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
pause