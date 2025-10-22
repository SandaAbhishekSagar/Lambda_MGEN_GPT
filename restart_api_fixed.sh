#!/bin/bash

# Restart API with ChromaDB fixes
echo "🔧 Restarting API with ChromaDB fixes..."

# Stop existing API
echo "🛑 Stopping existing API..."
pkill -f "lambda_gpu_api" || true
sleep 3

# Load environment variables
echo "🔑 Loading environment variables..."
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded"
else
    echo "⚠️  No .env file found, using system environment"
fi

# Set ChromaDB Cloud environment variables
export USE_CLOUD_CHROMA=true
export CHROMADB_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW
export CHROMADB_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130
export CHROMADB_DATABASE=newtest

# Test ChromaDB connection
echo "🧪 Testing ChromaDB connection..."
python3 test_chromadb_connection.py

# Start the API
echo "🚀 Starting fixed API..."
python3 services/chat_service/lambda_gpu_api_final.py &

# Wait for startup
echo "⏳ Waiting for API to start..."
sleep 5

# Test endpoints
echo "🧪 Testing endpoints..."

# Test health
echo "Testing health endpoint..."
curl -s http://localhost:8000/health | head -c 100
echo ""

# Test documents
echo "Testing documents endpoint..."
curl -s http://localhost:8000/documents | head -c 200
echo ""

echo "✅ API restarted with ChromaDB fixes!"
echo "🌐 API available at: http://localhost:8000"
echo "📊 Documents endpoint: http://localhost:8000/documents"
echo "💬 Chat endpoint: http://localhost:8000/chat"
