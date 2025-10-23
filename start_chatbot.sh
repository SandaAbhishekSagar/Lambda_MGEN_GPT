#!/bin/bash

echo "🚀 Starting Northeastern University Chatbot..."
echo "============================================="

# Check if we're in the right directory
if [ ! -f "services/chat_service/lambda_gpu_api.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Load environment variables if .env file exists
if [ -f ".env" ]; then
    echo "✅ Environment variables loaded"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  Warning: No .env file found. Make sure environment variables are set."
fi

# Set PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# Start the API server
echo "🌐 Starting API server on port 8000..."
python services/chat_service/lambda_gpu_api.py
