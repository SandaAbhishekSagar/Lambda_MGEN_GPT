#!/bin/bash
# Quick start script for Lambda GPU deployment

echo "🚀 Starting Lambda GPU Chatbot..."

# Activate virtual environment
source lambda_gpu_env/bin/activate

# Set PYTHONPATH to include the project root
export PYTHONPATH="${PWD}:${PYTHONPATH}"
echo "PYTHONPATH set to: ${PYTHONPATH}"

# Start the Lambda GPU API
echo "Starting Lambda GPU API server..."
python services/chat_service/lambda_gpu_api.py
