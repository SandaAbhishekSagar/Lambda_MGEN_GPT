#!/bin/bash

# Comprehensive Fix for HuggingFace Hub Compatibility
# Tries multiple approaches to resolve the compatibility issue

echo "🔧 COMPREHENSIVE FIX FOR HUGGINGFACE HUB COMPATIBILITY"
echo "======================================================="

# Activate virtual environment
source lambda_gpu_env/bin/activate

echo "📦 Step 1: Complete cleanup of HuggingFace packages..."

# Remove all HuggingFace related packages completely
pip uninstall -y huggingface-hub transformers sentence-transformers tokenizers accelerate safetensors 2>/dev/null || true

# Clear pip cache
pip cache purge 2>/dev/null || true

echo "✅ Complete cleanup done"

echo ""
echo "📦 Step 2: Installing compatible versions (Method 1)..."

# Method 1: Install very specific compatible versions
pip install "huggingface-hub==0.16.4" --force-reinstall --no-deps
pip install "tokenizers==0.15.2" --force-reinstall --no-deps
pip install "safetensors==0.4.0" --force-reinstall --no-deps
pip install "transformers==4.35.0" --force-reinstall --no-deps
pip install "sentence-transformers==2.2.2" --force-reinstall --no-deps

echo "✅ Method 1 packages installed"

echo ""
echo "🧪 Step 3: Testing Method 1..."

# Test Method 1
python3 -c "
import sys
try:
    print('Testing Method 1...')
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(['test sentence'])
    print('✅ Method 1 successful!')
    sys.exit(0)
except Exception as e:
    print(f'❌ Method 1 failed: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo "🎉 Method 1 successful! HuggingFace compatibility fixed!"
    exit 0
fi

echo ""
echo "📦 Step 4: Trying Method 2 (Alternative approach)..."

# Method 2: Try with different versions
pip uninstall -y huggingface-hub transformers sentence-transformers tokenizers 2>/dev/null || true

pip install "huggingface-hub==0.17.3" --force-reinstall
pip install "tokenizers==0.15.2" --force-reinstall
pip install "transformers==4.36.0" --force-reinstall
pip install "sentence-transformers==2.2.2" --force-reinstall

echo "✅ Method 2 packages installed"

echo ""
echo "🧪 Step 5: Testing Method 2..."

# Test Method 2
python3 -c "
import sys
try:
    print('Testing Method 2...')
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(['test sentence'])
    print('✅ Method 2 successful!')
    sys.exit(0)
except Exception as e:
    print(f'❌ Method 2 failed: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo "🎉 Method 2 successful! HuggingFace compatibility fixed!"
    exit 0
fi

echo ""
echo "📦 Step 6: Trying Method 3 (Fallback approach)..."

# Method 3: Use compatible chatbot version
if [ -f "services/chat_service/lambda_gpu_chatbot_compatible.py" ]; then
    echo "✅ Using compatible chatbot version..."
    
    # Copy the compatible version
    cp services/chat_service/lambda_gpu_chatbot_compatible.py services/chat_service/lambda_gpu_chatbot.py
    echo "✅ Compatible chatbot version installed"
    
    # Test the compatible version
    python3 -c "
import sys
try:
    print('Testing compatible chatbot...')
    from services.chat_service.lambda_gpu_chatbot import LambdaGPUChatbot
    chatbot = LambdaGPUChatbot()
    print('✅ Compatible chatbot successful!')
    sys.exit(0)
except Exception as e:
    print(f'❌ Compatible chatbot failed: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        echo "🎉 Method 3 successful! Using compatible chatbot version!"
        exit 0
    fi
fi

echo ""
echo "📦 Step 7: Final fallback - Install minimal working versions..."

# Final fallback: Install minimal working versions
pip uninstall -y huggingface-hub transformers sentence-transformers tokenizers 2>/dev/null || true

pip install "huggingface-hub==0.16.4"
pip install "tokenizers==0.15.2"
pip install "transformers==4.35.0"
pip install "sentence-transformers==2.2.2"

echo "✅ Final fallback packages installed"

echo ""
echo "🧪 Step 8: Testing final fallback..."

# Test final fallback
python3 -c "
import sys
try:
    print('Testing final fallback...')
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(['test sentence'])
    print('✅ Final fallback successful!')
    sys.exit(0)
except Exception as e:
    print(f'❌ Final fallback failed: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo "🎉 Final fallback successful! HuggingFace compatibility fixed!"
    exit 0
else
    echo "❌ All methods failed. Please check the error messages above."
    echo ""
    echo "🔧 Manual troubleshooting steps:"
    echo "1. Check if you have the correct Python version (3.10)"
    echo "2. Check if you have the correct CUDA version"
    echo "3. Try running: pip install --upgrade pip"
    echo "4. Try running: pip install --upgrade setuptools wheel"
    echo "5. Check if there are any conflicting packages"
    exit 1
fi
