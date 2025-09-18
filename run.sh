#!/bin/bash

# Development and Production startup script

echo "🚀 Starting TikTok Symphony AI Studio..."

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set environment variables if .env exists
if [ -f ".env" ]; then
    echo "🔧 Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Determine run mode
MODE=${1:-development}

if [ "$MODE" = "production" ]; then
    echo "🏭 Starting in PRODUCTION mode with Gunicorn..."
    echo "🌐 Server will be available at http://0.0.0.0:${PORT:-5000}"

    # Run with gunicorn using config file
    gunicorn app:app --config gunicorn_config.py

elif [ "$MODE" = "development" ]; then
    echo "🔧 Starting in DEVELOPMENT mode with Flask..."
    echo "🌐 Server will be available at http://localhost:5000"
    echo "⚠️  This mode is for development only. Use 'production' for deployment."

    # Run with Flask development server
    export FLASK_ENV=development
    export FLASK_DEBUG=True
    python app.py

else
    echo "❌ Invalid mode: $MODE"
    echo "Usage: ./run.sh [development|production]"
    exit 1
fi