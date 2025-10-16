@echo off
REM AI Trading Dashboard Setup Script for Windows

echo Setting up AI Trading Dashboard...

REM Create virtual environment for backend
echo Creating Python virtual environment...
cd backend
python -m venv venv

REM Activate virtual environment (Windows)
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Copy environment file
echo Setting up environment variables...
copy ..\env.example .env

REM Setup frontend
echo Setting up frontend...
cd ..\frontend

REM Install Node.js dependencies
echo Installing Node.js dependencies...
npm install

echo.
echo Setup complete! Here's how to run the application:
echo.
echo Backend (FastAPI):
echo 1. cd backend
echo 2. venv\Scripts\activate.bat
echo 3. uvicorn app.main:app --reload
echo.
echo Frontend (React):
echo 1. cd frontend
echo 2. npm start
echo.
echo Don't forget to:
echo - Add your API keys to backend\.env
echo - Install TA-Lib if technical analysis fails
echo - The app will run on http://localhost:3000
echo.
pause