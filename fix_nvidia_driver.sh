#!/bin/bash
# Fix NVIDIA Driver/Library Version Mismatch on Lambda Labs
# This script resolves the NVML initialization error

set -e

echo "🔧 Fixing NVIDIA Driver/Library Version Mismatch..."
echo "=================================================="

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

# Check if running on Lambda Labs
check_lambda_environment() {
    print_status "Checking Lambda Labs environment..."
    
    # Check if we're on Ubuntu
    if [ ! -f /etc/os-release ]; then
        print_error "Not running on Ubuntu - this script is for Lambda Labs Ubuntu instances"
        exit 1
    fi
    
    # Check Ubuntu version
    . /etc/os-release
    print_status "Running on Ubuntu $VERSION_ID"
    
    # Check if NVIDIA GPU is present
    if ! lspci | grep -i nvidia > /dev/null; then
        print_error "No NVIDIA GPU detected"
        exit 1
    fi
    
    print_success "NVIDIA GPU detected"
}

# Check current NVIDIA driver status
check_nvidia_status() {
    print_status "Checking NVIDIA driver status..."
    
    # Check if nvidia-smi works
    if nvidia-smi > /dev/null 2>&1; then
        print_success "nvidia-smi is working"
        nvidia-smi --query-gpu=name,driver_version --format=csv,noheader,nounits
        return 0
    else
        print_warning "nvidia-smi failed - driver issue detected"
        return 1
    fi
}

# Fix driver/library mismatch
fix_driver_mismatch() {
    print_status "Fixing NVIDIA driver/library mismatch..."
    
    # Stop any running processes that might be using the GPU
    print_status "Stopping processes using GPU..."
    sudo pkill -f python || true
    sudo pkill -f nvidia || true
    
    # Update package lists
    print_status "Updating package lists..."
    sudo apt update
    
    # Install NVIDIA driver management tools
    print_status "Installing NVIDIA driver management tools..."
    sudo apt install -y nvidia-driver-545 nvidia-utils-545
    
    # Alternative: Install latest NVIDIA driver
    print_status "Installing latest NVIDIA driver..."
    sudo apt install -y nvidia-driver-525 nvidia-utils-525
    
    # Update initramfs
    print_status "Updating initramfs..."
    sudo update-initramfs -u
    
    print_warning "Driver installation completed. REBOOT REQUIRED."
    print_status "Please run: sudo reboot"
    print_status "After reboot, run this script again to verify the fix"
}

# Alternative fix: Reinstall NVIDIA drivers
reinstall_nvidia_drivers() {
    print_status "Reinstalling NVIDIA drivers..."
    
    # Remove existing NVIDIA packages
    print_status "Removing existing NVIDIA packages..."
    sudo apt remove --purge -y nvidia-* libnvidia-*
    sudo apt autoremove -y
    
    # Clean package cache
    sudo apt autoclean
    
    # Install fresh NVIDIA drivers
    print_status "Installing fresh NVIDIA drivers..."
    sudo apt update
    sudo apt install -y nvidia-driver-525 nvidia-utils-525
    
    # Update initramfs
    sudo update-initramfs -u
    
    print_warning "Fresh driver installation completed. REBOOT REQUIRED."
}

# Verify fix after reboot
verify_fix() {
    print_status "Verifying NVIDIA driver fix..."
    
    # Wait a moment for driver to initialize
    sleep 3
    
    # Test nvidia-smi
    if nvidia-smi > /dev/null 2>&1; then
        print_success "✅ NVIDIA driver is working correctly!"
        print_status "GPU Information:"
        nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader,nounits
        
        # Test CUDA
        print_status "Testing CUDA..."
        if python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')" 2>/dev/null; then
            print_success "✅ CUDA is working correctly!"
        else
            print_warning "CUDA test failed - may need PyTorch reinstallation"
        fi
        
        return 0
    else
        print_error "❌ NVIDIA driver still not working"
        return 1
    fi
}

# Install CUDA toolkit if needed
install_cuda_toolkit() {
    print_status "Installing CUDA toolkit..."
    
    # Download and install CUDA toolkit
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
    sudo dpkg -i cuda-keyring_1.0-1_all.deb
    sudo apt update
    sudo apt install -y cuda-toolkit-12-1
    
    # Add CUDA to PATH
    echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
    source ~/.bashrc
    
    print_success "CUDA toolkit installed"
}

# Main function
main() {
    echo "🔧 NVIDIA Driver/Library Mismatch Fix"
    echo "====================================="
    
    # Check environment
    check_lambda_environment
    
    # Check if we need to reboot
    if [ "$1" = "--verify" ]; then
        verify_fix
        exit $?
    fi
    
    # Check current status
    if check_nvidia_status; then
        print_success "NVIDIA driver is already working correctly!"
        exit 0
    fi
    
    print_warning "NVIDIA driver/library mismatch detected"
    print_status "Attempting to fix..."
    
    # Try the fix
    fix_driver_mismatch
    
    print_status "Fix applied. Please reboot and run:"
    print_status "./fix_nvidia_driver.sh --verify"
}

# Run main function
main "$@"
