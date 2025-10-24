@echo off
REM Ultra-fast performance mode setup

echo Setting up ultra-fast performance mode...

REM Set performance mode to fast with minimal collections
set PERFORMANCE_MODE=fast
set SEARCH_ALL_COLLECTIONS=false
set MAX_COLLECTIONS=50

REM Optimize OpenAI settings for maximum speed
set OPENAI_MAX_TOKENS=300
set OPENAI_TEMPERATURE=0.2
set OPENAI_MODEL=gpt-4o-mini

REM Optimize search settings for speed
set MAX_WORKERS=10
set TIMEOUT_PER_COLLECTION=1
set RESULTS_PER_COLLECTION=3

echo Ultra-fast mode configuration:
echo PERFORMANCE_MODE=%PERFORMANCE_MODE%
echo MAX_COLLECTIONS=%MAX_COLLECTIONS%
echo OPENAI_MAX_TOKENS=%OPENAI_MAX_TOKENS%
echo MAX_WORKERS=%MAX_WORKERS%
echo TIMEOUT_PER_COLLECTION=%TIMEOUT_PER_COLLECTION%

echo Starting chatbot in ultra-fast mode...
python services/chat_service/lambda_gpu_chatbot_optimized.py
