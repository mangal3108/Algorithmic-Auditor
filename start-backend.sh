#!/bin/bash
cd /workspaces/Algorithmic-Auditor
# Kill any existing uvicorn processes on port 8000
fuser -k 8000/tcp 2>/dev/null || true
sleep 1
# Start the backend server
/workspaces/Algorithmic-Auditor/.venv/bin/python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
