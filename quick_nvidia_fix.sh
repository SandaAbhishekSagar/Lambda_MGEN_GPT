#!/bin/bash
# Quick Fix for NVML Driver/Library Version Mismatch
# Run this first to fix the NVIDIA issue before deployment

echo "🔧 Quick NVIDIA Driver Fix for Lambda Labs"
echo "=========================================="

# Stop any processes using GPU
echo "Stopping processes using GPU..."
sudo pkill -f python || true
sudo pkill -f nvidia || true

# Update system
echo "Updating system..."
sudo apt update

# Install/update NVIDIA drivers
echo "Installing compatible NVIDIA drivers..."
sudo apt install -y nvidia-driver-525 nvidia-utils-525

# Alternative: Try Lambda Labs specific fix
echo "Trying Lambda Labs specific NVIDIA fix..."
if command -v lambda-install-nvidia-drivers &> /dev/null; then
    sudo lambda-install-nvidia-drivers
fi

# Update initramfs
echo "Updating initramfs..."
sudo update-initramfs -u

echo ""
echo "⚠️  IMPORTANT: REBOOT REQUIRED"
echo "============================="
echo "Please run: sudo reboot"
echo "After reboot, test with: nvidia-smi"
echo ""
echo "If nvidia-smi works after reboot, then run:"
echo "./lambda_deploy_fixed.sh"
