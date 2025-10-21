"""
Koyeb GPU Startup Script
A100 GPU-optimized startup for Koyeb deployment
"""

import os
import uvicorn
import torch

if __name__ == "__main__":
    # Get port from environment variable (Koyeb sets this)
    port = int(os.getenv("PORT", 8000))
    
    print("🚀 Starting Northeastern GPU Chatbot on Koyeb...")
    print(f"🔧 Port: {port}")
    print(f"🔧 GPU Available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"🔧 GPU: {torch.cuda.get_device_name(0)}")
        print(f"🔧 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    
    uvicorn.run(
        "koyeb_gpu_handler:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        workers=1,  # Single worker for GPU optimization
        loop="asyncio"
    )
