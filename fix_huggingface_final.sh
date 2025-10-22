#!/bin/bash

# Final Fix for HuggingFace Hub Compatibility Issue
# Fixes: cannot import name 'split_torch_state_dict_into_shards' from 'huggingface_hub'

echo "🔧 FINAL FIX FOR HUGGINGFACE HUB COMPATIBILITY"
echo "==============================================="

# Activate virtual environment
source lambda_gpu_env/bin/activate

echo "📦 Step 1: Completely removing problematic packages..."

# Remove all HuggingFace related packages
pip uninstall -y huggingface-hub transformers sentence-transformers tokenizers accelerate safetensors 2>/dev/null || true

echo "✅ Problematic packages removed"

echo ""
echo "📦 Step 2: Installing compatible versions in correct order..."

# Install in specific order to avoid conflicts
pip install "huggingface-hub==0.16.4" --force-reinstall --no-deps
pip install "tokenizers==0.15.2" --force-reinstall --no-deps
pip install "safetensors==0.4.0" --force-reinstall --no-deps
pip install "transformers==4.36.0" --force-reinstall --no-deps
pip install "sentence-transformers==2.2.2" --force-reinstall --no-deps
pip install "accelerate==0.24.0" --force-reinstall --no-deps

echo "✅ Compatible versions installed"

echo ""
echo "📦 Step 3: Installing additional compatibility packages..."

# Install additional packages for compatibility
pip install "torch>=2.0.0" --force-reinstall
pip install "numpy<2.0.0" --force-reinstall
pip install "tqdm>=4.65.0" --force-reinstall

echo "✅ Additional packages installed"

echo ""
echo "🧪 Step 4: Testing the fix..."

# Test the imports step by step
python3 -c "
import sys
try:
    print('Testing HuggingFace Hub...')
    from huggingface_hub import hf_hub_download
    print('✅ HuggingFace Hub import successful')
    
    print('Testing tokenizers...')
    from tokenizers import Tokenizer
    print('✅ Tokenizers import successful')
    
    print('Testing safetensors...')
    import safetensors
    print('✅ Safetensors import successful')
    
    print('Testing transformers...')
    from transformers import AutoTokenizer, AutoModel
    print('✅ Transformers import successful')
    
    print('Testing sentence-transformers...')
    from sentence_transformers import SentenceTransformer
    print('✅ SentenceTransformer import successful')
    
    print('🎉 All imports successful!')
    
except Exception as e:
    print(f'❌ Import test failed: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Import tests failed"
    exit 1
fi

echo ""
echo "🧪 Step 5: Testing model loading..."

# Test model loading
python3 -c "
import sys
try:
    print('Testing model loading...')
    from sentence_transformers import SentenceTransformer
    
    # Test with a small model first
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print('✅ Model loading successful')
    
    # Test encoding
    embeddings = model.encode(['test sentence'])
    print(f'✅ Encoding successful: {len(embeddings[0])} dimensions')
    
    print('🎉 Model loading test passed!')
    
except Exception as e:
    print(f'❌ Model loading test failed: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Model loading tests failed"
    exit 1
fi

echo ""
echo "✅ ALL TESTS PASSED!"
echo "===================="
echo ""
echo "🎉 HuggingFace Hub compatibility issue has been resolved!"
echo ""
echo "🚀 You can now start your chatbot:"
echo "   ./start_chatbot.sh"
echo ""
echo "Or test the API:"
echo "   curl http://localhost:8000/health"
