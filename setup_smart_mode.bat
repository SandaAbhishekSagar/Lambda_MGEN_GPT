@echo off
REM Smart collection targeting mode setup

echo Setting up smart collection targeting mode...

REM Set performance mode to smart with query-based targeting
set PERFORMANCE_MODE=smart
set SEARCH_ALL_COLLECTIONS=false
set MAX_COLLECTIONS=30

REM Optimize OpenAI settings for speed
set OPENAI_MAX_TOKENS=300
set OPENAI_TEMPERATURE=0.2
set OPENAI_MODEL=gpt-4o-mini

REM Optimize search settings for smart targeting
set MAX_WORKERS=10
set TIMEOUT_PER_COLLECTION=1
set RESULTS_PER_COLLECTION=3

echo Smart mode configuration:
echo PERFORMANCE_MODE=%PERFORMANCE_MODE%
echo MAX_COLLECTIONS=%MAX_COLLECTIONS%
echo OPENAI_MAX_TOKENS=%OPENAI_MAX_TOKENS%
echo MAX_WORKERS=%MAX_WORKERS%
echo TIMEOUT_PER_COLLECTION=%TIMEOUT_PER_COLLECTION%

echo Starting chatbot in smart targeting mode...
echo This mode will automatically select relevant collections based on your query!
python services/chat_service/lambda_gpu_chatbot_optimized.py
