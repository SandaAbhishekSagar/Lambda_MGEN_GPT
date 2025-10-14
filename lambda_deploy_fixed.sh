#!/bin/bash
# Lambda Labs GPU Deployment Script - Fixed for NVIDIA Driver Issues
# Handles driver/library version mismatch automatically

set -e

echo "🚀 Starting Lambda Labs GPU Deployment (Fixed Version)..."
echo "========================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# Check NVIDIA driver and fix if needed
check_and_fix_nvidia() {
    print_status "Checking NVIDIA driver status..."
    
    # Test nvidia-smi
    if nvidia-smi > /dev/null 2>&1; then
        print_success "✅ NVIDIA driver is working correctly"
        nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader,nounits
        return 0
    else
        print_warning "⚠️ NVIDIA driver issue detected"
        
        # Check for driver/library mismatch
        if nvidia-smi 2>&1 | grep -q "Driver/library version mismatch"; then
            print_warning "Detected driver/library version mismatch"
            fix_nvidia_mismatch
        else
            print_error "Unknown NVIDIA driver issue"
            return 1
        fi
    fi
}

# Fix NVIDIA driver/library mismatch
fix_nvidia_mismatch() {
    print_status "Fixing NVIDIA driver/library mismatch..."
    
    # Stop any processes using GPU
    print_status "Stopping processes using GPU..."
    sudo pkill -f python || true
    
    # Update system
    print_status "Updating system packages..."
    sudo apt update
    
    # Install/update NVIDIA drivers
    print_status "Installing compatible NVIDIA drivers..."
    sudo apt install -y nvidia-driver-525 nvidia-utils-525
    
    # Alternative: Use Lambda Labs specific drivers
    if [ -f /usr/bin/lambda-install-nvidia-drivers ]; then
        print_status "Using Lambda Labs NVIDIA driver installer..."
        sudo /usr/bin/lambda-install-nvidia-drivers
    fi
    
    # Update initramfs
    print_status "Updating initramfs..."
    sudo update-initramfs -u
    
    print_warning "NVIDIA driver fix applied. REBOOT REQUIRED."
    print_status "Please run: sudo reboot"
    print_status "After reboot, run this script again"
    
    # Ask user to reboot
    read -p "Reboot now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo reboot
    else
        print_warning "Please reboot manually and run this script again"
        exit 1
    fi
}

# Check if we're on Lambda Labs instance
check_lambda_environment() {
    print_status "Checking Lambda Labs environment..."
    
    # Check Ubuntu version
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        print_status "Running on Ubuntu $VERSION_ID"
    fi
    
    # Check for GPU
    if lspci | grep -i nvidia > /dev/null; then
        print_success "NVIDIA GPU detected"
    else
        print_error "No NVIDIA GPU detected"
        exit 1
    fi
    
    # Check CUDA
    if command -v nvcc &> /dev/null; then
        print_success "CUDA compiler found"
    else
        print_warning "CUDA compiler not found - will install"
    fi
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
        git \
        curl \
        wget \
        build-essential \
        htop \
        nvtop \
        nvidia-driver-525 \
        nvidia-utils-525
    
    print_success "System packages updated"
}

# Setup Python environment
setup_python_environment() {
    print_status "Setting up Python environment..."
    
    # Create virtual environment
    python3 -m venv lambda_gpu_env
    source lambda_gpu_env/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    print_success "Python environment created"
}

# Install Python dependencies with NVIDIA driver check
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    source lambda_gpu_env/bin/activate
    
    # Install PyTorch with CUDA support first
    print_status "Installing PyTorch with CUDA support..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    
    # Verify PyTorch CUDA installation
    print_status "Verifying PyTorch CUDA installation..."
    python3 -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA version: {torch.version.cuda}')
    print(f'GPU name: {torch.cuda.get_device_name(0)}')
else:
    print('CUDA not available - check NVIDIA driver')
    exit(1)
"
    
    if [ $? -ne 0 ]; then
        print_error "PyTorch CUDA verification failed"
        print_status "This usually indicates an NVIDIA driver issue"
        return 1
    fi
    
    # Install other dependencies
    print_status "Installing other dependencies..."
    if [ -f "requirements_lambda.txt" ]; then
        pip install -r requirements_lambda.txt
    else
        print_warning "requirements_lambda.txt not found, using basic dependencies"
        pip install fastapi uvicorn openai langchain chromadb sentence-transformers
    fi
    
    # Install GPU optimization packages (optional)
    print_status "Installing GPU optimization packages..."
    pip install flash-attn --no-build-isolation || print_warning "flash-attn installation failed - continuing without it"
    pip install xformers || print_warning "xformers installation failed - continuing without it"
    
    print_success "Dependencies installed"
}

# Setup environment variables
setup_environment() {
    print_status "Setting up environment variables..."
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Lambda Labs GPU Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# ChromaDB Configuration (using cloud)
CHROMADB_HOST=your_chromadb_host_here
CHROMADB_PORT=8000

# GPU Configuration
CUDA_VISIBLE_DEVICES=0
TORCH_CUDA_ARCH_LIST="7.5;8.0;8.6"

# Performance Optimization
OMP_NUM_THREADS=4
TOKENIZERS_PARALLELISM=false
EOF
        print_warning "Created .env file - please update with your actual API keys"
    else
        print_success ".env file already exists"
    fi
}

# Test GPU functionality
test_gpu() {
    print_status "Testing GPU functionality..."
    
    source lambda_gpu_env/bin/activate
    
    python3 -c "
import torch
import torch.nn as nn

print('Testing GPU functionality...')
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')

if torch.cuda.is_available():
    print(f'GPU count: {torch.cuda.device_count()}')
    print(f'Current GPU: {torch.cuda.current_device()}')
    print(f'GPU name: {torch.cuda.get_device_name(0)}')
    
    # Test tensor operations
    x = torch.randn(1000, 1000).cuda()
    y = torch.randn(1000, 1000).cuda()
    z = torch.mm(x, y)
    print(f'GPU tensor operation successful: {z.shape}')
    
    # Test memory
    print(f'GPU memory allocated: {torch.cuda.memory_allocated() / 1024**3:.2f} GB')
    print(f'GPU memory reserved: {torch.cuda.memory_reserved() / 1024**3:.2f} GB')
    
    print('✅ GPU test passed!')
else:
    print('❌ GPU not available - will use CPU')
"
    
    if [ $? -eq 0 ]; then
        print_success "GPU test completed successfully"
    else
        print_error "GPU test failed"
        return 1
    fi
}

# Start the application
start_application() {
    print_status "Starting the application..."
    
    source lambda_gpu_env/bin/activate
    
    # Check if Lambda GPU API exists
    if [ -f "services/chat_service/lambda_gpu_api.py" ]; then
        print_status "Starting Lambda GPU API server..."
        python services/chat_service/lambda_gpu_api.py &
    else
        print_warning "Lambda GPU API not found, starting basic server..."
        python -m uvicorn services.chat_service.enhanced_openai_api:app --host 0.0.0.0 --port 8000 &
    fi
    
    # Wait a moment for startup
    sleep 5
    
    # Test the API
    if curl -s http://localhost:8000/health > /dev/null; then
        print_success "Application started successfully!"
        print_status "API is running at: http://localhost:8000"
        print_status "Health check: http://localhost:8000/health"
    else
        print_error "Application failed to start"
        return 1
    fi
}

# Create monitoring script
create_monitoring_script() {
    print_status "Creating monitoring script..."
    
    cat > monitor_gpu.sh << 'EOF'
#!/bin/bash
# GPU Monitoring Script for Lambda Labs

echo "🔍 GPU Monitoring Dashboard"
echo "=========================="

while true; do
    clear
    echo "🕐 $(date)"
    echo ""
    
    # GPU Status
    if command -v nvidia-smi &> /dev/null; then
        echo "🖥️  GPU Status:"
        nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader,nounits | while read line; do
            echo "   $line"
        done
        echo ""
    fi
    
    # System Memory
    echo "💾 System Memory:"
    free -h | grep Mem
    echo ""
    
    # Application Status
    if pgrep -f "lambda_gpu_api.py\|enhanced_openai_api.py" > /dev/null; then
        echo "✅ Application: Running"
    else
        echo "❌ Application: Not running"
    fi
    
    echo ""
    echo "Press Ctrl+C to exit"
    sleep 5
done
EOF
    
    chmod +x monitor_gpu.sh
    print_success "Monitoring script created: ./monitor_gpu.sh"
}

# Main deployment function
main() {
    echo "🎯 Lambda Labs GPU Deployment for Northeastern University Chatbot"
    echo "=================================================================="
    
    # Check environment
    check_lambda_environment
    
    # Check and fix NVIDIA driver
    if ! check_and_fix_nvidia; then
        print_error "NVIDIA driver issues detected and fix attempted"
        print_status "Please reboot and run this script again"
        exit 1
    fi
    
    # Update system
    update_system
    
    # Setup Python environment
    setup_python_environment
    
    # Install dependencies
    install_dependencies
    
    # Setup environment variables
    setup_environment
    
    # Test GPU
    test_gpu
    
    # Create monitoring script
    create_monitoring_script
    
    # Start application
    start_application
    
    print_success "Deployment completed successfully!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Update .env file with your API keys"
    echo "2. Run: source lambda_gpu_env/bin/activate"
    echo "3. Test application: python3 lambda_quick_start.py"
    echo "4. Monitor GPU: ./monitor_gpu.sh"
    echo ""
    echo "🌐 API Endpoints:"
    echo "- Health: http://localhost:8000/health"
    echo "- Chat: http://localhost:8000/chat"
    echo "- GPU Info: http://localhost:8000/gpu-info"
    echo ""
    print_success "Ready for Lambda Labs GPU deployment! 🚀"
}

# Run main function
main "$@"
