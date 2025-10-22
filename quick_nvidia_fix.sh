#!/bin/bash

# Quick NVIDIA Driver Fix for Lambda Labs
# Fix driver/library version mismatch

echo "🔧 QUICK NVIDIA DRIVER FIX"
echo "=========================="
echo ""

# Check current status
echo "Current NVIDIA status:"
nvidia-smi 2>&1 || echo "nvidia-smi failed"

echo ""
echo "Fixing driver/library version mismatch..."

# Stop NVIDIA services
sudo systemctl stop nvidia-persistenced 2>/dev/null || true
sudo systemctl stop nvidia-fabricmanager 2>/dev/null || true

# Unload NVIDIA modules
sudo rmmod nvidia_uvm 2>/dev/null || true
sudo rmmod nvidia_drm 2>/dev/null || true
sudo rmmod nvidia_modeset 2>/dev/null || true
sudo rmmod nvidia 2>/dev/null || true

echo "NVIDIA modules unloaded"

# Update system
sudo apt update -y

# Install latest NVIDIA drivers
sudo apt install nvidia-driver-535 nvidia-utils-535 -y

echo "NVIDIA drivers installed"

# Install CUDA toolkit
sudo apt install cuda-toolkit-12-1 -y

# Add CUDA to PATH
echo 'export PATH=/usr/local/cuda-12.1/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.1/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc

echo "CUDA toolkit installed"

echo ""
echo "⚠️  REBOOT REQUIRED"
echo "=================="
echo "The system needs to reboot to complete the driver installation."
echo "After reboot, run: ./lambda_deploy.sh"
echo ""
echo "Rebooting in 10 seconds... (Press Ctrl+C to cancel)"
sleep 10

sudo reboot