#!/bin/bash

# Fix NVIDIA Driver/Library Version Mismatch
# Lambda Labs GPU - Northeastern University Chatbot

set -e  # Exit on any error

echo "🔧 FIXING NVIDIA DRIVER VERSION MISMATCH"
echo "======================================="
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
    echo -e "${RED}[ERROR]${NC} $1
}

# Check current driver status
check_driver_status() {
    print_status "Checking current NVIDIA driver status..."
    
    # Check if nvidia-smi works
    if nvidia-smi > /dev/null 2>&1; then
        print_success "nvidia-smi is working"
        nvidia-smi --query-gpu=name,driver_version --format=csv,noheader,nounits
    else
        print_warning "nvidia-smi failed - driver issue detected"
    fi
    
    # Check kernel modules
    if lsmod | grep nvidia > /dev/null; then
        print_success "NVIDIA kernel modules loaded"
        lsmod | grep nvidia
    else
        print_warning "NVIDIA kernel modules not loaded"
    fi
}

# Stop NVIDIA services
stop_nvidia_services() {
    print_status "Stopping NVIDIA services..."
    
    # Stop NVIDIA services
    sudo systemctl stop nvidia-persistenced 2>/dev/null || true
    sudo systemctl stop nvidia-fabricmanager 2>/dev/null || true
    
    # Unload NVIDIA kernel modules
    sudo rmmod nvidia_uvm 2>/dev/null || true
    sudo rmmod nvidia_drm 2>/dev/null || true
    sudo rmmod nvidia_modeset 2>/dev/null || true
    sudo rmmod nvidia 2>/dev/null || true
    
    print_success "NVIDIA services stopped and modules unloaded"
}

# Update system packages
update_system() {
    print_status "Updating system packages..."
    
    sudo apt update -y
    sudo apt upgrade -y
    
    print_success "System packages updated"
}

# Install/update NVIDIA drivers
install_nvidia_drivers() {
    print_status "Installing/updating NVIDIA drivers..."
    
    # Remove existing NVIDIA packages
    sudo apt remove --purge nvidia-* libnvidia-* -y 2>/dev/null || true
    
    # Clean up
    sudo apt autoremove -y
    sudo apt autoclean
    
    # Add NVIDIA repository
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
    sudo dpkg -i cuda-keyring_1.0-1_all.deb
    sudo apt update
    
    # Install latest NVIDIA drivers
    sudo apt install nvidia-driver-535 nvidia-utils-535 -y
    
    print_success "NVIDIA drivers installed"
}

# Install CUDA toolkit
install_cuda_toolkit() {
    print_status "Installing CUDA toolkit..."
    
    # Install CUDA toolkit
    sudo apt install cuda-toolkit-12-1 -y
    
    # Add CUDA to PATH
    echo 'export PATH=/usr/local/cuda-12.1/bin:$PATH' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.1/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
    source ~/.bashrc
    
    print_success "CUDA toolkit installed"
}

# Reboot system
reboot_system() {
    print_status "Reboot required to complete driver installation..."
    print_warning "The system will reboot in 10 seconds. Press Ctrl+C to cancel."
    
    sleep 10
    
    print_status "Rebooting system..."
    sudo reboot
}

# Test GPU after reboot
test_gpu_after_reboot() {
    print_status "Testing GPU after reboot..."
    
    # Check nvidia-smi
    if nvidia-smi > /dev/null 2>&1; then
        print_success "nvidia-smi is working"
        nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader,nounits
    else
        print_error "nvidia-smi still not working"
        return 1
    fi
    
    # Check CUDA
    if nvcc --version > /dev/null 2>&1; then
        print_success "CUDA compiler is working"
        nvcc --version
    else
        print_warning "CUDA compiler not found"
    fi
    
    # Test PyTorch CUDA
    python3 -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA version: {torch.version.cuda}')
    print(f'GPU name: {torch.cuda.get_device_name(0)}')
    print(f'GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB')
"
    
    print_success "GPU test completed"
}

# Main function
main() {
    print_status "Starting NVIDIA driver fix process..."
    echo ""
    
    # Step 1: Check current status
    check_driver_status
    echo ""
    
    # Step 2: Stop NVIDIA services
    stop_nvidia_services
    echo ""
    
    # Step 3: Update system
    update_system
    echo ""
    
    # Step 4: Install/update drivers
    install_nvidia_drivers
    echo ""
    
    # Step 5: Install CUDA toolkit
    install_cuda_toolkit
    echo ""
    
    # Step 6: Reboot system
    reboot_system
}

# Handle command line arguments
case "${1:-}" in
    "check")
        check_driver_status
        ;;
    "stop")
        stop_nvidia_services
        ;;
    "install")
        install_nvidia_drivers
        ;;
    "test")
        test_gpu_after_reboot
        ;;
    *)
        main
        ;;
esac