#!/bin/bash

# Aggressive Fix for HuggingFace Hub Compatibility Issue
# Northeastern University Chatbot - Lambda Labs

echo "🔧 AGGRESSIVE FIX FOR HUGGINGFACE HUB COMPATIBILITY ISSUE"
echo "========================================================="
echo ""

# Activate virtual environment
source lambda_gpu_env/bin/activate

echo "1. Completely removing all problematic packages..."
echo "================================================="

# Remove all packages that might cause conflicts
pip uninstall -y huggingface-hub transformers sentence-transformers torch torchvision torchaudio accelerate bitsandbytes flash-attn xformers || true

echo ""
echo "2. Clearing pip cache..."
echo "======================="
pip cache purge || true

echo ""
echo "3. Installing compatible versions in correct order..."
echo "===================================================="

# Install in the correct order to avoid conflicts
pip install --no-cache-dir --force-reinstall huggingface-hub==0.19.4
pip install --no-cache-dir --force-reinstall transformers==4.35.2
pip install --no-cache-dir --force-reinstall sentence-transformers==2.2.2

echo ""
echo "4. Testing the fix..."
echo "==================="
python3 -c "
try:
    import huggingface_hub
    print(f'✅ HuggingFace Hub version: {huggingface_hub.__version__}')
    
    import transformers
    print(f'✅ Transformers version: {transformers.__version__}')
    
    import sentence_transformers
    print(f'✅ Sentence Transformers version: {sentence_transformers.__version__}')
    
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print('✅ HuggingFace Hub compatibility test successful')
except Exception as e:
    print(f'❌ HuggingFace Hub compatibility test failed: {e}')
    exit(1)
"

echo ""
echo "✅ Aggressive HuggingFace Hub compatibility fix completed!"
echo ""
echo "Now restart your chatbot:"
echo "./start_chatbot.sh"
