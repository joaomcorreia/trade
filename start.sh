#!/bin/bash

echo "Starting AI Trading Dashboard..."
echo

echo "[1/2] Starting Backend Server..."
python3 ai_trading_backend.py &
BACKEND_PID=$!

sleep 3

echo "[2/2] Starting Dashboard..."
python3 -m http.server 3000 &
FRONTEND_PID=$!

echo
echo "Dashboard available at: http://localhost:3000/ai_trading_dashboard.html"
echo "Backend API at: http://localhost:8000"
echo
echo "Press Ctrl+C to stop all services"

# Trap Ctrl+C and kill background processes
trap 'echo "Stopping services..."; kill $BACKEND_PID $FRONTEND_PID; exit' INT

# Wait for background processes
wait