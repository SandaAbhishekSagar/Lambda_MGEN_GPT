#!/bin/bash

# Fix HuggingFace Hub Compatibility Issue
# Northeastern University Chatbot - Lambda GPU

echo "🔧 FIXING HUGGINGFACE HUB COMPATIBILITY ISSUE"
echo "============================================="

# Activate virtual environment
source lambda_gpu_env/bin/activate

echo "📦 Installing compatible versions..."

# Uninstall problematic packages
pip uninstall -y huggingface-hub transformers sentence-transformers

# Install compatible versions
pip install "huggingface-hub>=0.16.4,<0.20.0"
pip install "transformers>=4.36.0,<4.40.0"
pip install "sentence-transformers==2.2.2"

# Install additional compatibility packages
pip install "tokenizers>=0.13.2,<0.16.0"
pip install "safetensors>=0.3.0"

echo "✅ HuggingFace compatibility fix applied"
echo ""
echo "🧪 Testing the fix..."

# Test the import
python3 -c "
try:
    from sentence_transformers import SentenceTransformer
    print('✅ SentenceTransformer import successful')
    
    from transformers import AutoTokenizer
    print('✅ Transformers import successful')
    
    from huggingface_hub import hf_hub_download
    print('✅ HuggingFace Hub import successful')
    
    print('🎉 All imports working correctly!')
except Exception as e:
    print(f'❌ Import failed: {e}')
"

echo ""
echo "🚀 You can now restart your chatbot:"
echo "   ./start_chatbot.sh"
