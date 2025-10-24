#!/bin/bash
# Setup script for fast performance mode

echo "Setting up fast performance mode..."

# Set performance mode to fast
export PERFORMANCE_MODE=fast
export SEARCH_ALL_COLLECTIONS=false
export MAX_COLLECTIONS=200

# Optimize OpenAI settings for speed
export OPENAI_MAX_TOKENS=600
export OPENAI_TEMPERATURE=0.3
export OPENAI_MODEL=gpt-4o-mini

# Optimize search settings
export MAX_WORKERS=20
export TIMEOUT_PER_COLLECTION=3
export RESULTS_PER_COLLECTION=20

echo "Fast mode configuration:"
echo "PERFORMANCE_MODE=$PERFORMANCE_MODE"
echo "MAX_COLLECTIONS=$MAX_COLLECTIONS"
echo "OPENAI_MAX_TOKENS=$OPENAI_MAX_TOKENS"
echo "MAX_WORKERS=$MAX_WORKERS"

echo "Starting chatbot in fast mode..."
python services/chat_service/lambda_gpu_chatbot_optimized.py
