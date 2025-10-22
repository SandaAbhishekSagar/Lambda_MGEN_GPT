#!/bin/bash

# Lambda Labs GPU Deployment Script
# Northeastern University Chatbot - Ultra-Fast GPU Deployment

set -e  # Exit on any error

echo "🚀 LAMBDA LABS GPU DEPLOYMENT"
echo "=============================="
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

# Check if running on Lambda Labs
check_lambda_labs() {
    print_status "Checking Lambda Labs environment..."
    
    # Check for Lambda Labs specific indicators
    if [[ -f "/etc/lambda-labs" ]] || [[ -n "$LAMBDA_LABS" ]]; then
        print_success "Running on Lambda Labs infrastructure"
    else
        print_warning "Not detected as Lambda Labs environment - continuing anyway"
    fi
}

# Check system requirements
check_system() {
    print_status "Checking system requirements..."
    
    # Check Ubuntu version
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        if [[ "$ID" == "ubuntu" ]]; then
            print_success "Ubuntu $VERSION detected"
        else
            print_warning "Non-Ubuntu system detected: $ID"
        fi
    fi
    
    # Check available memory
    MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
    if [[ $MEMORY_GB -ge 16 ]]; then
        print_success "Sufficient memory: ${MEMORY_GB}GB"
    else
        print_warning "Low memory: ${MEMORY_GB}GB (recommended: 16GB+)"
    fi
    
    # Check disk space
    DISK_GB=$(df -BG . | awk 'NR==2{print $4}' | sed 's/G//')
    if [[ $DISK_GB -ge 50 ]]; then
        print_success "Sufficient disk space: ${DISK_GB}GB"
    else
        print_warning "Low disk space: ${DISK_GB}GB (recommended: 50GB+)"
    fi
}

# Check GPU availability
check_gpu() {
    print_status "Checking GPU availability..."
    
    if command -v nvidia-smi &> /dev/null; then
        print_success "NVIDIA drivers detected"
        nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader,nounits
    else
        print_error "NVIDIA drivers not found - GPU acceleration will not be available"
        print_status "Installing NVIDIA drivers..."
        install_nvidia_drivers
    fi
}

# Install NVIDIA drivers
install_nvidia_drivers() {
    print_status "Installing NVIDIA drivers..."
    
    # Update package list
    sudo apt update
    
    # Install NVIDIA drivers
    sudo apt install -y nvidia-driver-535 nvidia-utils-535
    
    print_warning "NVIDIA drivers installed - reboot may be required"
}

# Update system packages
update_system() {
    print_status "Updating system packages..."
    
    sudo apt update -y
    sudo apt upgrade -y
    
    # Install essential packages
    sudo apt install -y \
        python3-pip \
        python3-venv \
        python3-dev \
        git \
        curl \
        wget \
        build-essential \
        htop \
        nvtop \
        nvidia-smi \
        vim \
        unzip \
        software-properties-common
    
    print_success "System packages updated"
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
    print(f'GPU name: {torch.cuda.get_device_name(0)}')
    print(f'GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB')
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
# Lambda Labs GPU Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# GPU Configuration
CUDA_VISIBLE_DEVICES=0
TORCH_CUDA_ARCH_LIST="7.5;8.0;8.6"
OMP_NUM_THREADS=4
TOKENIZERS_PARALLELISM=false

# ChromaDB Configuration
CHROMADB_HOST=your_chromadb_host_here
CHROMADB_PORT=8000
CHROMADB_API_KEY=your_chromadb_api_key_here

# API Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=1

# Performance Optimization
BATCH_SIZE=32
MAX_COLLECTIONS=150
CACHE_TTL=300
EOF
        
        print_success "Environment file created (.env)"
        print_warning "Please edit .env file with your API keys"
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
import asyncio
import requests
from typing import Dict, Any

def test_gpu_availability():
    """Test GPU availability"""
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        print(f"✅ CUDA available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"✅ GPU name: {torch.cuda.get_device_name(0)}")
            print(f"✅ GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
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

def test_api_endpoints():
    """Test API endpoints"""
    try:
        base_url = "http://localhost:8000"
        
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test GPU info endpoint
        response = requests.get(f"{base_url}/gpu-info", timeout=10)
        if response.status_code == 200:
            print("✅ GPU info endpoint working")
        else:
            print(f"❌ GPU info endpoint failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_chat_functionality():
    """Test chat functionality"""
    try:
        base_url = "http://localhost:8000"
        
        test_question = "What programs does Northeastern University offer?"
        
        response = requests.post(
            f"{base_url}/chat",
            json={"question": test_question},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat test successful")
            print(f"   Response time: {data.get('timing', {}).get('total', 'N/A')}s")
            print(f"   Answer length: {len(data.get('answer', ''))}")
            print(f"   Sources: {len(data.get('sources', []))}")
            return True
        else:
            print(f"❌ Chat test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
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
    
    # Test 4: API endpoints (if server is running)
    print("4. Testing API endpoints...")
    api_success = test_api_endpoints()
    print("")
    
    # Test 5: Chat functionality (if server is running)
    print("5. Testing chat functionality...")
    chat_success = test_chat_functionality()
    print("")
    
    # Summary
    print("📊 TEST SUMMARY")
    print("===============")
    print(f"GPU Available: {'✅' if gpu_available else '❌'}")
    print(f"Import Success: {'✅' if import_success else '❌'}")
    print(f"Init Success: {'✅' if init_success else '❌'}")
    print(f"API Success: {'✅' if api_success else '❌'}")
    print(f"Chat Success: {'✅' if chat_success else '❌'}")
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
        print("  curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{\"question\": \"What programs does Northeastern offer?\"}'")
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
    print_status "Starting Lambda Labs GPU deployment..."
    echo ""
    
    # Step 1: Check environment
    check_lambda_labs
    check_system
    check_gpu
    echo ""
    
    # Step 2: Update system
    update_system
    echo ""
    
    # Step 3: Create virtual environment
    create_venv
    echo ""
    
    # Step 4: Install PyTorch with CUDA
    install_pytorch
    echo ""
    
    # Step 5: Install dependencies
    install_dependencies
    echo ""
    
    # Step 6: Create configuration files
    create_env_file
    create_systemd_service
    create_monitoring_script
    create_quick_start
    echo ""
    
    # Step 7: Final instructions
    print_success "Deployment completed successfully!"
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