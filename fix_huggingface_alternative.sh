#!/bin/bash

# Alternative Fix for HuggingFace Hub Compatibility
# Uses a different approach with compatible model

echo "🔧 ALTERNATIVE FIX FOR HUGGINGFACE HUB COMPATIBILITY"
echo "====================================================="

# Activate virtual environment
source lambda_gpu_env/bin/activate

echo "📦 Step 1: Installing alternative compatible packages..."

# Install older, more stable versions
pip uninstall -y huggingface-hub transformers sentence-transformers tokenizers 2>/dev/null || true

# Install very specific compatible versions
pip install "huggingface-hub==0.16.4" --force-reinstall
pip install "tokenizers==0.15.2" --force-reinstall
pip install "transformers==4.35.0" --force-reinstall
pip install "sentence-transformers==2.2.2" --force-reinstall

echo "✅ Alternative packages installed"

echo ""
echo "🧪 Step 2: Testing with alternative approach..."

# Test with a different model loading approach
python3 -c "
import sys
try:
    print('Testing alternative model loading...')
    
    # Try importing without loading the model first
    from sentence_transformers import SentenceTransformer
    print('✅ SentenceTransformer import successful')
    
    # Try with a different model
    print('Loading alternative model...')
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    print('✅ Alternative model loading successful')
    
    # Test encoding
    embeddings = model.encode(['test sentence'])
    print(f'✅ Encoding successful: {len(embeddings[0])} dimensions')
    
    print('🎉 Alternative approach successful!')
    
except Exception as e:
    print(f'❌ Alternative approach failed: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Alternative approach failed"
    exit 1
fi

echo ""
echo "✅ ALTERNATIVE APPROACH SUCCESSFUL!"
echo "===================================="
echo ""
echo "🎉 Using alternative model loading approach!"
echo ""
echo "🚀 You can now start your chatbot:"
echo "   ./start_chatbot.sh"
