@echo off
REM Setup script for fast performance mode

echo Setting up fast performance mode...

REM Set performance mode to fast
set PERFORMANCE_MODE=fast
set SEARCH_ALL_COLLECTIONS=false
set MAX_COLLECTIONS=200

REM Optimize OpenAI settings for speed
set OPENAI_MAX_TOKENS=600
set OPENAI_TEMPERATURE=0.3
set OPENAI_MODEL=gpt-4o-mini

REM Optimize search settings
set MAX_WORKERS=20
set TIMEOUT_PER_COLLECTION=3
set RESULTS_PER_COLLECTION=20

echo Fast mode configuration:
echo PERFORMANCE_MODE=%PERFORMANCE_MODE%
echo MAX_COLLECTIONS=%MAX_COLLECTIONS%
echo OPENAI_MAX_TOKENS=%OPENAI_MAX_TOKENS%
echo MAX_WORKERS=%MAX_WORKERS%

echo Starting chatbot in fast mode...
python services/chat_service/lambda_gpu_chatbot_optimized.py
