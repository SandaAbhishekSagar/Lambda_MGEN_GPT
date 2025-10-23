#!/bin/bash

# Lambda Labs Quick Start Script
# Northeastern University Chatbot - GPU Optimized

echo "🚀 LAMBDA LABS QUICK START"
echo "=========================="
echo ""

# Check if we're in the right directory
if [ ! -f "services/chat_service/lambda_gpu_api_optimized.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   Make sure you're in the Lambda_MGEN_GPT directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "lambda_gpu_env" ]; then
    echo "❌ Virtual environment not found. Please run deployment first:"
    echo "   ./deploy_lambda_labs_optimized.sh"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source lambda_gpu_env/bin/activate

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded"
else
    echo "⚠️  Warning: .env file not found"
    echo "   Please create .env file with your API keys"
    exit 1
fi

# Set PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# Check GPU availability
echo "🔍 Checking GPU availability..."
python3 -c "
import torch
if torch.cuda.is_available():
    print(f'✅ GPU: {torch.cuda.get_device_name(0)}')
    print(f'✅ Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB')
else:
    print('⚠️  No GPU available - running on CPU')
"

# Start the API server
echo ""
echo "🌐 Starting API server on port 8000..."
echo "   API Documentation: http://localhost:8000/docs"
echo "   Health Check: http://localhost:8000/health"
echo "   Chat Endpoint: http://localhost:8000/chat"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python services/chat_service/lambda_gpu_api_optimized.py
