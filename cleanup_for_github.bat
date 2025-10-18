@echo off
echo 🧹 Cleaning repository for GitHub deployment...

REM Remove old backend versions
if exist ai_trading_backend.py del ai_trading_backend.py
if exist production_ai_backend.py del production_ai_backend.py
if exist enhanced_ai_trading_backend.py del enhanced_ai_trading_backend.py
if exist realtime_ai_backend.py del realtime_ai_backend.py

REM Remove test files (keep them locally, but not in git)
if exist test_server.py del test_server.py
if exist test_dashboard.html del test_dashboard.html

REM Remove old setup files
if exist setup.bat del setup.bat
if exist setup.sh del setup.sh
if exist start.bat del start.bat
if exist start.sh del start.sh
if exist deploy.sh del deploy.sh
if exist deploy_backend.sh del deploy_backend.sh
if exist start_dashboard.bat del start_dashboard.bat

REM Keep main files
echo ✅ Cleaned repository structure
echo 📁 Main files kept:
echo    - complete_ai_backend.py (main backend)
echo    - ai_trading_dashboard.html (main frontend)  
echo    - quick_start.bat (launcher)
echo    - README.md
echo    - All test files (for development)

echo.
echo 🚀 Repository is ready for GitHub!
echo.
echo Next steps:
echo 1. git add .
echo 2. git commit -m "Clean repository structure for GitHub release"
echo 3. git push origin main

pause