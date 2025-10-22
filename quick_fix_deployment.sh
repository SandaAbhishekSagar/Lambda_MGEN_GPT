#!/bin/bash

# Quick Fix for Lambda Labs GPU Deployment Issues
# Fixes HuggingFace Hub compatibility and Pydantic validation errors

echo "🔧 QUICK FIX FOR LAMBDA LABS GPU DEPLOYMENT"
echo "============================================"

# Activate virtual environment
source lambda_gpu_env/bin/activate

echo "📦 Step 1: Fixing HuggingFace Hub compatibility..."

# Uninstall problematic packages
pip uninstall -y huggingface-hub transformers sentence-transformers tokenizers

# Install compatible versions
pip install "huggingface-hub>=0.16.4,<0.20.0" --force-reinstall
pip install "transformers>=4.36.0,<4.40.0" --force-reinstall
pip install "sentence-transformers==2.2.2" --force-reinstall
pip install "tokenizers>=0.13.2,<0.16.0" --force-reinstall

echo "✅ HuggingFace packages fixed"

echo ""
echo "📦 Step 2: Installing additional compatibility packages..."

# Install additional packages for compatibility
pip install "safetensors>=0.3.0"
pip install "accelerate>=0.24.0"
pip install "bitsandbytes>=0.41.0"

echo "✅ Compatibility packages installed"

echo ""
echo "🧪 Step 3: Testing the fixes..."

# Test the imports
python3 -c "
import sys
try:
    print('Testing imports...')
    
    # Test sentence transformers
    from sentence_transformers import SentenceTransformer
    print('✅ SentenceTransformer import successful')
    
    # Test transformers
    from transformers import AutoTokenizer, AutoModel
    print('✅ Transformers import successful')
    
    # Test huggingface hub
    from huggingface_hub import hf_hub_download
    print('✅ HuggingFace Hub import successful')
    
    # Test model loading
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print('✅ Model loading successful')
    
    print('🎉 All tests passed!')
    
except Exception as e:
    print(f'❌ Test failed: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
    echo ""
    echo "🚀 You can now restart your chatbot:"
    echo "   ./start_chatbot.sh"
    echo ""
    echo "Or test the API:"
    echo "   curl http://localhost:8000/health"
else
    echo "❌ Tests failed - please check the errors above"
    exit 1
fi
