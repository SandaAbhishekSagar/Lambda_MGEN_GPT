"""
Lambda Labs GPU-Optimized FastAPI Service
Ultra-fast Northeastern University Chatbot API with GPU acceleration
"""

import os
import sys
import time
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Import our GPU-optimized chatbot
from services.chat_service.lambda_gpu_chatbot_optimized import (
    LambdaGPUUniversityRAGChatbot, 
    get_chatbot, 
    clear_gpu_cache,
    ChatResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Northeastern University Chatbot - Lambda GPU",
    description="Ultra-fast GPU-accelerated RAG chatbot for Northeastern University",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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
    clear_cache: Optional[bool] = False

class ChatResponseModel(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    confidence: str
    timing: Dict[str, float]
    gpu_info: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    timestamp: float
    gpu_info: Dict[str, Any]
    performance: Dict[str, Any]

class GPUInfoResponse(BaseModel):
    cuda_available: bool
    device: str
    gpu_name: Optional[str]
    gpu_memory_total: Optional[float]
    gpu_memory_allocated: Optional[float]
    gpu_memory_cached: Optional[float]
    cuda_version: Optional[str]
    batch_size: int

# Global variables
chatbot = None
startup_time = time.time()

@app.on_event("startup")
async def startup_event():
    """Initialize the chatbot on startup"""
    global chatbot
    logger.info("[LAMBDA GPU API] Starting up...")
    
    try:
        chatbot = get_chatbot()
        logger.info("[LAMBDA GPU API] Chatbot initialized successfully")
    except Exception as e:
        logger.error(f"[LAMBDA GPU API] Failed to initialize chatbot: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global chatbot
    if chatbot:
        # Clear GPU cache
        clear_gpu_cache()
        logger.info("[LAMBDA GPU API] Shutdown complete")

@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint with basic info"""
    return {
        "message": "Northeastern University Chatbot - Lambda GPU",
        "version": "2.0.0",
        "status": "running",
        "gpu_accelerated": True,
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "gpu-info": "/gpu-info",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with GPU info"""
    try:
        if not chatbot:
            raise HTTPException(status_code=503, detail="Chatbot not initialized")
        
        gpu_info = chatbot.get_gpu_info()
        
        # Calculate uptime
        uptime = time.time() - startup_time
        
        # Performance metrics
        performance = {
            "uptime_seconds": round(uptime, 2),
            "status": "healthy",
            "gpu_optimized": gpu_info.get('cuda_available', False),
            "device": gpu_info.get('device', 'unknown'),
            "batch_size": gpu_info.get('batch_size', 0)
        }
        
        return HealthResponse(
            status="healthy",
            timestamp=time.time(),
            gpu_info=gpu_info,
            performance=performance
        )
        
    except Exception as e:
        logger.error(f"[LAMBDA GPU API] Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/gpu-info", response_model=GPUInfoResponse)
async def get_gpu_info():
    """Get detailed GPU information"""
    try:
        if not chatbot:
            raise HTTPException(status_code=503, detail="Chatbot not initialized")
        
        gpu_info = chatbot.get_gpu_info()
        
        return GPUInfoResponse(
            cuda_available=gpu_info.get('cuda_available', False),
            device=gpu_info.get('device', 'unknown'),
            gpu_name=gpu_info.get('gpu_name'),
            gpu_memory_total=gpu_info.get('gpu_memory_total'),
            gpu_memory_allocated=gpu_info.get('gpu_memory_allocated'),
            gpu_memory_cached=gpu_info.get('gpu_memory_cached'),
            cuda_version=gpu_info.get('cuda_version'),
            batch_size=gpu_info.get('batch_size', 0)
        )
        
    except Exception as e:
        logger.error(f"[LAMBDA GPU API] GPU info failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def get_document_stats():
    """Get document statistics"""
    try:
        if not chatbot:
            raise HTTPException(status_code=503, detail="Chatbot not initialized")
        
        # Get collection info and count documents
        collections = chatbot.chroma_service.get_batch_collections()
        total_documents = 0
        
        logger.info(f"[LAMBDA GPU API] Found {len(collections)} collections to count")
        
        # Count documents in each collection (limit to first 100 for performance)
        for i, collection_name in enumerate(collections[:100]):  # Limit to first 100 collections for performance
            try:
                collection = chatbot.chroma_service.client.get_collection(collection_name)
                count = collection.count()
                total_documents += count
                if i < 5:  # Log first 5 for debugging
                    logger.info(f"[LAMBDA GPU API] Collection {collection_name}: {count} documents")
            except Exception as e:
                logger.warning(f"Could not count collection {collection_name}: {e}")
                continue
        
        # If we only counted first 100, estimate total
        if len(collections) > 100:
            avg_docs_per_collection = total_documents / 100
            estimated_total = int(avg_docs_per_collection * len(collections))
            logger.info(f"[LAMBDA GPU API] Estimated total documents: {estimated_total} (based on {total_documents} from first 100 collections)")
            total_documents = estimated_total
        
        return {
            "total_documents": total_documents,
            "total_collections": len(collections),
            "total_universities": 1,  # Northeastern University
            "collections": collections[:10],  # Show first 10
            "cache_status": {
                "query_cache_size": len(chatbot.embedding_manager.embeddings_cache),
                "document_cache_size": len(chatbot.embedding_manager.document_embeddings)
            }
        }
        
    except Exception as e:
        logger.error(f"[LAMBDA GPU API] Document stats failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponseModel)
async def chat(request: ChatRequest):
    """Main chat endpoint with GPU acceleration"""
    try:
        if not chatbot:
            raise HTTPException(status_code=503, detail="Chatbot not initialized")
        
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Clear cache if requested
        if request.clear_cache:
            chatbot.clear_cache()
            logger.info("[LAMBDA GPU API] Cache cleared by request")
        
        # Process the question
        start_time = time.time()
        response = chatbot.chat(request.question)
        processing_time = time.time() - start_time
        
        logger.info(f"[LAMBDA GPU API] Question processed in {processing_time:.2f}s")
        
        return ChatResponseModel(
            answer=response.answer,
            sources=response.sources,
            confidence=response.confidence,
            timing=response.timing,
            gpu_info=response.gpu_info
        )
        
    except Exception as e:
        logger.error(f"[LAMBDA GPU API] Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear-cache")
async def clear_cache(background_tasks: BackgroundTasks):
    """Clear GPU cache and embeddings cache"""
    try:
        if not chatbot:
            raise HTTPException(status_code=503, detail="Chatbot not initialized")
        
        # Clear caches
        chatbot.clear_cache()
        clear_gpu_cache()
        
        logger.info("[LAMBDA GPU API] All caches cleared")
        
        return {
            "status": "success",
            "message": "All caches cleared successfully",
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"[LAMBDA GPU API] Clear cache failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/performance")
async def get_performance_metrics():
    """Get performance metrics"""
    try:
        if not chatbot:
            raise HTTPException(status_code=503, detail="Chatbot not initialized")
        
        gpu_info = chatbot.get_gpu_info()
        
        return {
            "gpu_info": gpu_info,
            "uptime": time.time() - startup_time,
            "cache_status": {
                "query_cache_size": len(chatbot.embedding_manager.embeddings_cache),
                "document_cache_size": len(chatbot.embedding_manager.document_embeddings)
            },
            "collections": {
                "total": len(chatbot.chroma_service.get_batch_collections()),
                "cached": len(chatbot.chroma_service.collections_cache)
            }
        }
        
    except Exception as e:
        logger.error(f"[LAMBDA GPU API] Performance metrics failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
async def test_endpoint():
    """Test endpoint for quick verification"""
    try:
        if not chatbot:
            raise HTTPException(status_code=503, detail="Chatbot not initialized")
        
        # Simple test question
        test_question = "What is Northeastern University?"
        response = chatbot.chat(test_question)
        
        return {
            "status": "success",
            "test_question": test_question,
            "response_time": response.timing['total'],
            "gpu_working": response.gpu_info.get('cuda_available', False),
            "answer_length": len(response.answer),
            "sources_count": len(response.sources)
        }
        
    except Exception as e:
        logger.error(f"[LAMBDA GPU API] Test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "available_endpoints": ["/", "/health", "/chat", "/gpu-info", "/docs"]}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": str(exc)}
    )

if __name__ == "__main__":
    # Run the server
    logger.info("[LAMBDA GPU API] Starting server...")
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    workers = int(os.getenv("WORKERS", "1"))
    
    logger.info(f"[LAMBDA GPU API] Starting on {host}:{port} with {workers} workers")
    
    uvicorn.run(
        "lambda_gpu_api_optimized:app",
        host=host,
        port=port,
        workers=workers,
        log_level="info",
        access_log=True
    )
