#!/bin/bash

echo "🔧 Activating backend..."
cd backend
echo "➡️  Entered backend directory"

echo "🐍 Activating virtual environment..."
source .venv/bin/activate
echo "✔️  Virtual environment activated"

echo "🚀 Starting backend server in background..."
python -m app.main & 
BACKEND_PID=$!
echo "✔️  Backend running with PID $BACKEND_PID"

echo ""
echo "🌐 Moving to frontend..."
cd ../frontend
echo "➡️  Entered frontend directory"

echo "📦 Installing frontend dependencies..."
npm install
echo "✔️  npm install complete"

echo "🚀 Starting frontend dev server..."
npm run dev
echo "✔️  Frontend is running"

wait
