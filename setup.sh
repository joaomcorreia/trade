#!/bin/bash

# AI Trading Dashboard Setup Script

echo "Setting up AI Trading Dashboard..."

# Create virtual environment for backend
echo "Creating Python virtual environment..."
cd backend
python -m venv venv

# Activate virtual environment (Windows)
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Copy environment file
echo "Setting up environment variables..."
cp ../.env.example .env

# Setup frontend
echo "Setting up frontend..."
cd ../frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo ""
echo "Setup complete! Here's how to run the application:"
echo ""
echo "Backend (FastAPI):"
echo "1. cd backend"
echo "2. Activate virtual environment:"
echo "   Windows: venv\\Scripts\\activate"
echo "   Linux/Mac: source venv/bin/activate"
echo "3. uvicorn app.main:app --reload"
echo ""
echo "Frontend (React):"
echo "1. cd frontend"
echo "2. npm start"
echo ""
echo "Don't forget to:"
echo "- Add your API keys to backend/.env"
echo "- Install TA-Lib if technical analysis fails"
echo "- The app will run on http://localhost:3000"
echo ""