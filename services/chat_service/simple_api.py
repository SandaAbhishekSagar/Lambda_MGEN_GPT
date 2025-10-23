"""
Simple API server for Northeastern University Chatbot
This version works without all dependencies for testing
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("Warning: FastAPI not available, using fallback mode")

# Simple fallback if FastAPI is not available
if not FASTAPI_AVAILABLE:
    print("FastAPI not available. Please install with: pip install fastapi uvicorn")
    sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="Northeastern University Chatbot - Simple API",
    description="Simple API for Northeastern University Chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    question: str
    n_results: Optional[int] = 10

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    confidence: str
    status: str

@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "message": "Northeastern University Chatbot - Simple API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is running",
        "dependencies": {
            "fastapi": FASTAPI_AVAILABLE
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Simple chat endpoint"""
    try:
        # Simple response for testing
        response = {
            "answer": f"I received your question: '{request.question}'. This is a simple test response. The full chatbot functionality requires additional dependencies.",
            "sources": [
                {
                    "title": "Test Source",
                    "similarity": 0.95,
                    "url": "https://example.com"
                }
            ],
            "confidence": "medium",
            "status": "success"
        }
        
        return ChatResponse(**response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting Simple API server...")
    uvicorn.run(
        "simple_api:app",
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
