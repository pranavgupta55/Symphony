#!/bin/bash

echo "🎵 Starting Symphony AI Backend..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source backend/venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies (this may take a few minutes on first run)..."
cd backend
pip install -r requirements.txt --quiet

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Please create one from .env.example"
    echo "   You need to add your ANTHROPIC_API_KEY and OPENAI_API_KEY"
    exit 1
fi

# Check if API keys are set
if grep -q "your-anthropic-api-key-here" .env || grep -q "your-openai-api-key-here" .env; then
    echo "⚠️  Warning: Please update your API keys in backend/.env"
    echo "   Current keys are placeholder values"
fi

# Start FastAPI server
echo ""
echo "🚀 Starting FastAPI server on http://localhost:8000"
echo "   Press Ctrl+C to stop the server"
echo ""
python -m app.main

# Alternative: Use uvicorn directly
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
