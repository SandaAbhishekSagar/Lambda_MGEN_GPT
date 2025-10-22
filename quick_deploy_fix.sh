#!/bin/bash

# Quick Deploy Fix for Lambda Labs
# Skip problematic package installations and continue with deployment

set -e  # Exit on any error

echo "🚀 QUICK DEPLOY FIX - Lambda Labs GPU"
echo "====================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check GPU availability
check_gpu() {
    print_status "Checking GPU availability..."
    
    if command -v nvidia-smi &> /dev/null; then
        print_success "NVIDIA drivers detected"
        nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader,nounits
    else
        print_warning "nvidia-smi not found - but GPUs may still work"
    fi
}

# Create Python virtual environment
create_venv() {
    print_status "Creating Python virtual environment..."
    
    # Remove existing environment if it exists
    if [[ -d "lambda_gpu_env" ]]; then
        print_status "Removing existing virtual environment..."
        rm -rf lambda_gpu_env
    fi
    
    # Create new environment
    python3 -m venv lambda_gpu_env
    source lambda_gpu_env/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    print_success "Virtual environment created"
}

# Install PyTorch with CUDA
install_pytorch() {
    print_status "Installing PyTorch with CUDA support..."
    
    source lambda_gpu_env/bin/activate
    
    # Install PyTorch with CUDA 12.1 (compatible with Lambda Labs)
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    
    # Verify CUDA installation
    python3 -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA version: {torch.version.cuda}')
    print(f'GPU count: {torch.cuda.device_count()}')
    for i in range(torch.cuda.device_count()):
        print(f'GPU {i}: {torch.cuda.get_device_name(i)}')
        print(f'GPU {i} memory: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.1f} GB')
"
    
    print_success "PyTorch with CUDA installed"
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    source lambda_gpu_env/bin/activate
    
    # Install requirements
    pip install -r requirements_lambda.txt
    
    # Install additional GPU optimization packages
    pip install flash-attn --no-build-isolation || print_warning "flash-attn installation failed - continuing"
    pip install xformers || print_warning "xformers installation failed - continuing"
    
    print_success "Dependencies installed"
}

# Create environment file
create_env_file() {
    print_status "Creating environment configuration..."
    
    if [[ ! -f ".env" ]]; then
        cat > .env << EOF
# Core API Keys
OPENAI_API_KEY=your_openai_api_key_here

# ChromaDB Cloud (newtest database)
USE_CLOUD_CHROMA=true
CHROMADB_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW
CHROMADB_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130
CHROMADB_DATABASE=newtest

# GPU Configuration (8x A100 optimized)
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
TORCH_CUDA_ARCH_LIST="8.0"
GPU_BATCH_SIZE=128
GPU_MEMORY_FRACTION=0.9
GPU_MIXED_PRECISION=true
LAMBDA_LABS_GPU=true
GPU_TYPE=a100

# API Server
HOST=0.0.0.0
PORT=8000
WORKERS=8
API_TIMEOUT=30
CORS_ORIGINS="*"

# Performance Optimization (A100 optimized)
OMP_NUM_THREADS=16
TOKENIZERS_PARALLELISM=false
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:1024
TRANSFORMERS_CACHE=/runpod-volume/transformers-cache
HF_HOME=/runpod-volume/huggingface
CACHE_TTL=3600
MAX_MEMORY_CACHE_SIZE=8589934592
MAX_DISK_CACHE_SIZE=42949672960

# Database Optimization (8x A100 optimized)
MAX_COLLECTIONS_PER_SEARCH=500
SEARCH_TIMEOUT=10
PARALLEL_WORKERS=32
BATCH_SIZE=128
EOF
        
        print_success "Environment file created (.env)"
        print_warning "Please edit .env file with your OpenAI API key"
    else
        print_status "Environment file already exists"
    fi
}

# Create systemd service
create_systemd_service() {
    print_status "Creating systemd service..."
    
    sudo tee /etc/systemd/system/northeastern-chatbot.service > /dev/null << EOF
[Unit]
Description=Northeastern University Chatbot - Lambda GPU
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/lambda_gpu_env/bin
ExecStart=$(pwd)/lambda_gpu_env/bin/python services/chat_service/lambda_gpu_api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    # Reload systemd and enable service
    sudo systemctl daemon-reload
    sudo systemctl enable northeastern-chatbot
    
    print_success "Systemd service created"
}

# Create monitoring script
create_monitoring_script() {
    print_status "Creating GPU monitoring script..."
    
    cat > monitor_gpu.sh << 'EOF'
#!/bin/bash

# GPU Monitoring Script for Lambda Labs
# Northeastern University Chatbot

echo "🔍 GPU MONITORING - Northeastern Chatbot"
echo "========================================"

# Check if nvidia-smi is available
if command -v nvidia-smi &> /dev/null; then
    echo "📊 GPU Status:"
    nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader,nounits | while read line; do
        echo "  GPU: $line"
    done
    
    echo ""
    echo "📈 Real-time monitoring (Ctrl+C to stop):"
    watch -n 1 nvidia-smi
else
    echo "❌ nvidia-smi not found - GPU monitoring not available"
fi
EOF
    
    chmod +x monitor_gpu.sh
    
    print_success "GPU monitoring script created (monitor_gpu.sh)"
}

# Create quick start script
create_quick_start() {
    print_status "Creating quick start script..."
    
    cat > lambda_quick_start.py << 'EOF'
#!/usr/bin/env python3
"""
Lambda Labs Quick Start and Test Script
Northeastern University Chatbot - GPU Optimized
"""

import os
import sys
import time
import requests
from typing import Dict, Any

def test_gpu_availability():
    """Test GPU availability"""
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        print(f"✅ CUDA available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"✅ GPU count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"✅ GPU {i}: {torch.cuda.get_device_name(i)}")
                print(f"✅ GPU {i} memory: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.1f} GB")
            return True
        else:
            print("⚠️ No GPU available - running on CPU")
            return False
    except Exception as e:
        print(f"❌ GPU test failed: {e}")
        return False

def test_chatbot_import():
    """Test chatbot import"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from services.chat_service.lambda_gpu_chatbot import get_chatbot
        print("✅ Chatbot import successful")
        return True
    except Exception as e:
        print(f"❌ Chatbot import failed: {e}")
        return False

def test_chatbot_initialization():
    """Test chatbot initialization"""
    try:
        from services.chat_service.lambda_gpu_chatbot import get_chatbot
        chatbot = get_chatbot()
        print("✅ Chatbot initialization successful")
        return True
    except Exception as e:
        print(f"❌ Chatbot initialization failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 LAMBDA LABS QUICK START & TEST")
    print("==================================")
    print("")
    
    # Test 1: GPU availability
    print("1. Testing GPU availability...")
    gpu_available = test_gpu_availability()
    print("")
    
    # Test 2: Chatbot import
    print("2. Testing chatbot import...")
    import_success = test_chatbot_import()
    print("")
    
    # Test 3: Chatbot initialization
    print("3. Testing chatbot initialization...")
    init_success = test_chatbot_initialization()
    print("")
    
    # Summary
    print("📊 TEST SUMMARY")
    print("===============")
    print(f"GPU Available: {'✅' if gpu_available else '❌'}")
    print(f"Import Success: {'✅' if import_success else '❌'}")
    print(f"Init Success: {'✅' if init_success else '❌'}")
    print("")
    
    if all([import_success, init_success]):
        print("🎉 Chatbot is ready for deployment!")
        print("")
        print("To start the API server:")
        print("  source lambda_gpu_env/bin/activate")
        print("  python services/chat_service/lambda_gpu_api.py")
        print("")
        print("To test the API:")
        print("  curl http://localhost:8000/health")
    else:
        print("❌ Some tests failed - please check the errors above")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
EOF
    
    chmod +x lambda_quick_start.py
    
    print_success "Quick start script created (lambda_quick_start.py)"
}

# Main deployment function
main() {
    print_status "Starting quick deployment fix..."
    echo ""
    
    # Step 1: Check GPU
    check_gpu
    echo ""
    
    # Step 2: Create virtual environment
    create_venv
    echo ""
    
    # Step 3: Install PyTorch with CUDA
    install_pytorch
    echo ""
    
    # Step 4: Install dependencies
    install_dependencies
    echo ""
    
    # Step 5: Create configuration files
    create_env_file
    create_systemd_service
    create_monitoring_script
    create_quick_start
    echo ""
    
    # Step 6: Final instructions
    print_success "Quick deployment completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "1. Edit .env file with your API keys:"
    echo "   nano .env"
    echo ""
    echo "2. Test the installation:"
    echo "   python3 lambda_quick_start.py"
    echo ""
    echo "3. Start the chatbot:"
    echo "   source lambda_gpu_env/bin/activate"
    echo "   python services/chat_service/lambda_gpu_api.py"
    echo ""
    echo "4. Or start as a service:"
    echo "   sudo systemctl start northeastern-chatbot"
    echo "   sudo systemctl status northeastern-chatbot"
    echo ""
    echo "5. Monitor GPU usage:"
    echo "   ./monitor_gpu.sh"
    echo ""
    print_success "Lambda Labs GPU deployment complete! 🚀"
}

# Run main function
main "$@"
