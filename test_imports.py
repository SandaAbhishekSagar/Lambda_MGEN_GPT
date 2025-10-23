#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    
    try:
        # Test chatbot import
        from services.chat_service.lambda_gpu_chatbot import LambdaGPUUniversityRAGChatbot
        print("[OK] LambdaGPUUniversityRAGChatbot import successful")
    except ImportError as e:
        print(f"[ERROR] LambdaGPUUniversityRAGChatbot import failed: {e}")
        return False
    
    try:
        # Test API import
        from services.chat_service.lambda_gpu_api import app
        print("[OK] FastAPI app import successful")
    except ImportError as e:
        print(f"[ERROR] FastAPI app import failed: {e}")
        return False
    
    print("All imports successful!")
    return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
