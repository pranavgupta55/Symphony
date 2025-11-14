#!/bin/bash

echo "🎵 Starting Symphony AI Frontend..."

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node dependencies..."
    npm install
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    echo "VITE_API_URL=http://localhost:8000" > .env
fi

# Start Vite dev server
echo "🚀 Starting Vite development server..."
npm run dev
