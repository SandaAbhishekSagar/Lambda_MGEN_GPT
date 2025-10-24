#!/bin/bash

# Fix PyTorch Version Conflict
# Northeastern University Chatbot - Lambda Labs

echo "🔧 FIXING PYTORCH VERSION CONFLICT"
echo "=================================="
echo ""

# Activate virtual environment
source lambda_gpu_env/bin/activate

echo "1. Removing conflicting packages..."
echo "================================="

# Remove all packages that might cause conflicts
pip uninstall -y torch torchvision torchaudio xformers huggingface-hub transformers sentence-transformers || true

echo ""
echo "2. Clearing pip cache..."
echo "======================="
pip cache purge || true

echo ""
echo "3. Installing compatible PyTorch version..."
echo "=========================================="

# Install PyTorch with CUDA support
pip install --no-cache-dir torch==2.5.1+cu121 torchvision==0.20.1+cu121 torchaudio==2.5.1+cu121 --index-url https://download.pytorch.org/whl/cu121

echo ""
echo "4. Installing HuggingFace packages..."
echo "==================================="

# Install HuggingFace packages
pip install --no-cache-dir huggingface-hub==0.19.4
pip install --no-cache-dir transformers==4.35.2
pip install --no-cache-dir sentence-transformers==2.2.2

echo ""
echo "5. Installing compatible xformers..."
echo "==================================="

# Install compatible xformers
pip install --no-cache-dir xformers==0.0.29.post1 --index-url https://download.pytorch.org/whl/cu121 || true

echo ""
echo "6. Testing the fix..."
echo "==================="
python3 -c "
try:
    import torch
    print(f'✅ PyTorch version: {torch.__version__}')
    print(f'✅ CUDA available: {torch.cuda.is_available()}')
    
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
echo "✅ PyTorch version conflict fixed!"
echo ""
echo "Now restart your chatbot:"
echo "./start_chatbot.sh"
