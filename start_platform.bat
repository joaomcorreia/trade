@echo off
echo 🚀 Starting AI Trading Platform...
echo.

echo 📊 Starting Backend Server...
start "AI Trading Backend" cmd /c "python complete_ai_backend.py"

echo ⏱️ Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

echo 🌐 Starting Frontend Dashboard...
start "AI Trading Frontend" cmd /c "python -m http.server 3000"

echo ⏱️ Waiting for frontend to initialize...
timeout /t 3 /nobreak > nul

echo.
echo ✅ AI Trading Platform is now running!
echo.
echo 🔗 Access your platform:
echo    📊 Trading Dashboard: http://localhost:3000/ai_trading_dashboard.html
echo    📚 API Documentation: http://localhost:8001/docs
echo    ⚡ WebSocket: ws://localhost:8001/ws
echo    🔧 Admin Panel: http://localhost:8001/redoc
echo.
echo 💡 To stop: Close the terminal windows or press Ctrl+C
echo.
pause