"""
Lambda GPU API Service for Northeastern University Chatbot
Optimized for Lambda Labs cloud GPU deployment
"""

import os
import time
import uuid
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import psutil

from services.chat_service.lambda_gpu_chatbot import LambdaGPUUniversityRAGChatbot
from services.shared.config import config


# Initialize FastAPI app
app = FastAPI(
    title="Northeastern University Chatbot - Lambda GPU API",
    description="GPU-accelerated RAG chatbot deployed on Lambda Labs infrastructure",
    version="2.0.0-lambda-gpu"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
lambda_gpu_chatbot: Optional[LambdaGPUUniversityRAGChatbot] = None
startup_time = time.time()


class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: list
    confidence: float
    response_time: float
    search_time: float
    context_time: float
    llm_time: float
    documents_analyzed: int
    model: str
    device: str
    query_expansions: bool
    session_id: str
    gpu_memory_used: Optional[str] = None
    gpu_utilization: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    message: str
    response_time: float
    model: str
    device: str
    gpu_available: bool
    gpu_memory: Optional[str] = None
    system_memory: str
    uptime: float
    version: str


class StatsResponse(BaseModel):
    total_documents: int
    total_universities: int
    gpu_memory_usage: str
    system_memory_usage: str
    model_info: Dict[str, Any]


@app.on_event("startup")
async def startup_event():
    """Initialize the Lambda GPU chatbot on startup"""
    global lambda_gpu_chatbot
    
    print("🚀 Starting Lambda GPU Northeastern University Chatbot...")
    print("=" * 60)
    
    try:
        # Check GPU availability
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"✅ CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            print(f"✅ CUDA version: {torch.version.cuda}")
        else:
            print("⚠️ CUDA not available, using CPU")
        
        # Initialize Lambda GPU chatbot
        lambda_gpu_chatbot = LambdaGPUUniversityRAGChatbot(
            model_name=config.OPENAI_MODEL,
            openai_api_key=config.OPENAI_API_KEY
        )
        
        print("✅ Lambda GPU chatbot initialized successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Failed to initialize Lambda GPU chatbot: {e}")
        raise


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with health information"""
    global lambda_gpu_chatbot, startup_time
    
    response_time = time.time()
    
    # GPU information
    gpu_available = torch.cuda.is_available()
    gpu_memory = None
    if gpu_available:
        gpu_memory = f"{torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB"
    
    # System memory
    system_memory = f"{psutil.virtual_memory().total / 1024**3:.1f} GB"
    
    return HealthResponse(
        status="healthy",
        message="Lambda GPU Northeastern University Chatbot API is running",
        response_time=time.time() - response_time,
        model=lambda_gpu_chatbot.model_name if lambda_gpu_chatbot else "not_initialized",
        device=lambda_gpu_chatbot.embedding_manager.device if lambda_gpu_chatbot else "unknown",
        gpu_available=gpu_available,
        gpu_memory=gpu_memory,
        system_memory=system_memory,
        uptime=time.time() - startup_time,
        version="2.0.0-lambda-gpu"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return await root()


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint using Lambda GPU RAG pipeline"""
    global lambda_gpu_chatbot
    
    try:
        if not lambda_gpu_chatbot:
            raise HTTPException(status_code=500, detail="Lambda GPU chatbot not initialized")
        
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        print(f"[LAMBDA GPU API] Processing question: {request.question[:50]}...")
        print(f"[LAMBDA GPU API] Session ID: {session_id}")
        print(f"[LAMBDA GPU API] Model: {lambda_gpu_chatbot.model_name}")
        print(f"[LAMBDA GPU API] Device: {lambda_gpu_chatbot.embedding_manager.device}")
        
        # Generate response using Lambda GPU RAG pipeline
        response = lambda_gpu_chatbot.generate_lambda_gpu_response(
            question=request.question,
            session_id=session_id
        )
        
        # Add session ID and GPU info to response
        response['session_id'] = session_id
        
        # GPU memory usage
        if torch.cuda.is_available():
            gpu_memory_allocated = torch.cuda.memory_allocated() / 1024**3
            gpu_memory_reserved = torch.cuda.memory_reserved() / 1024**3
            response['gpu_memory_used'] = f"{gpu_memory_allocated:.2f} GB allocated, {gpu_memory_reserved:.2f} GB reserved"
            
            # Try to get GPU utilization (requires nvidia-ml-py3)
            try:
                import pynvml
                pynvml.nvmlInit()
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                response['gpu_utilization'] = f"{util.gpu}% GPU, {util.memory}% memory"
            except:
                response['gpu_utilization'] = "N/A"
        
        print(f"[LAMBDA GPU API] Response generated in {response.get('response_time', 0):.2f}s")
        print(f"[LAMBDA GPU API] Documents analyzed: {response.get('documents_analyzed', 0)}")
        print(f"[LAMBDA GPU API] Confidence: {response.get('confidence', 0):.2f}")
        
        return ChatResponse(**response)
        
    except Exception as e:
        print(f"[LAMBDA GPU API] Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str, limit: int = 10):
    """Get conversation history for a session"""
    # Simplified implementation - in production, use Redis or database
    return {"session_id": session_id, "history": [], "message": "History storage not implemented"}


@app.get("/documents", response_model=StatsResponse)
async def get_documents():
    """Get document statistics"""
    global lambda_gpu_chatbot
    
    try:
        if not lambda_gpu_chatbot:
            raise HTTPException(status_code=500, detail="Lambda GPU chatbot not initialized")
        
        # Get document count from ChromaDB
        doc_count = lambda_gpu_chatbot.chroma_service.get_collection_count()
        
        # GPU memory usage
        gpu_memory_usage = "N/A"
        if torch.cuda.is_available():
            gpu_memory_allocated = torch.cuda.memory_allocated() / 1024**3
            gpu_memory_reserved = torch.cuda.memory_reserved() / 1024**3
            gpu_memory_usage = f"{gpu_memory_allocated:.2f} GB / {gpu_memory_reserved:.2f} GB"
        
        # System memory usage
        memory = psutil.virtual_memory()
        system_memory_usage = f"{memory.used / 1024**3:.1f} GB / {memory.total / 1024**3:.1f} GB ({memory.percent:.1f}%)"
        
        # Model information
        model_info = {
            "name": lambda_gpu_chatbot.model_name,
            "device": lambda_gpu_chatbot.embedding_manager.device,
            "embedding_model": lambda_gpu_chatbot.embedding_manager.model_name,
            "gpu_available": torch.cuda.is_available(),
            "cuda_version": torch.version.cuda if torch.cuda.is_available() else None
        }
        
        return StatsResponse(
            total_documents=doc_count,
            total_universities=1,
            gpu_memory_usage=gpu_memory_usage,
            system_memory_usage=system_memory_usage,
            model_info=model_info
        )
        
    except Exception as e:
        print(f"[LAMBDA GPU API] Error getting documents: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting document stats: {str(e)}")


@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    return await get_documents()


@app.post("/clear-cache")
async def clear_cache():
    """Clear embedding cache"""
    global lambda_gpu_chatbot
    
    try:
        if not lambda_gpu_chatbot:
            raise HTTPException(status_code=500, detail="Lambda GPU chatbot not initialized")
        
        # Clear embedding cache
        lambda_gpu_chatbot.embedding_manager.embedding_cache.clear()
        
        # Clear GPU cache if available
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        return {"message": "Cache cleared successfully", "gpu_cache_cleared": torch.cuda.is_available()}
        
    except Exception as e:
        print(f"[LAMBDA GPU API] Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")


@app.get("/gpu-info")
async def get_gpu_info():
    """Get detailed GPU information"""
    if not torch.cuda.is_available():
        return {"gpu_available": False, "message": "No GPU available"}
    
    try:
        gpu_info = {
            "gpu_available": True,
            "device_count": torch.cuda.device_count(),
            "current_device": torch.cuda.current_device(),
            "device_name": torch.cuda.get_device_name(0),
            "cuda_version": torch.version.cuda,
            "cudnn_version": torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else None,
            "memory_total": f"{torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB",
            "memory_allocated": f"{torch.cuda.memory_allocated() / 1024**3:.2f} GB",
            "memory_reserved": f"{torch.cuda.memory_reserved() / 1024**3:.2f} GB",
            "memory_free": f"{(torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_reserved()) / 1024**3:.2f} GB"
        }
        
        # Try to get utilization info
        try:
            import pynvml
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            
            gpu_info.update({
                "gpu_utilization": f"{util.gpu}%",
                "memory_utilization": f"{util.memory}%",
                "temperature": f"{temp}°C"
            })
        except:
            gpu_info["utilization_info"] = "N/A (nvidia-ml-py3 not available)"
        
        return gpu_info
        
    except Exception as e:
        return {"gpu_available": True, "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting Lambda GPU API on port {port}...")
    uvicorn.run(
        "lambda_gpu_api:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload for production
        workers=1,     # Single worker for GPU memory efficiency
        log_level="info"
    )
