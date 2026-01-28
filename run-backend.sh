#!/bin/bash

# Kill any existing process on port 8000
echo "Checking for processes on port 8000..."
fuser -k 8000/tcp 2>/dev/null || echo "No process found on port 8000"
sleep 2

# Start backend
echo "Starting backend server..."
cd /workspaces/Algorithmic-Auditor
/workspaces/Algorithmic-Auditor/.venv/bin/python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 5

# Test if backend is responding
echo "Testing backend connectivity..."
curl -s http://localhost:8000/ && echo -e "\n✅ Backend is running!" || echo -e "\n❌ Backend failed to start"

echo "Backend PID: $BACKEND_PID"
echo "To stop the backend, run: kill $BACKEND_PID"
