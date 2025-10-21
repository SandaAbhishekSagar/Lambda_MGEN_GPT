"""
Koyeb Startup Script
Simple startup script for Koyeb deployment
"""

import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment variable (Koyeb sets this)
    port = int(os.getenv("PORT", 8000))
    
    print(f"Starting Northeastern Chatbot on port {port}")
    
    uvicorn.run(
        "koyeb_handler:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
