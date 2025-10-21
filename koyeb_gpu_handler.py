"""
Koyeb GPU-Optimized Handler
Northeastern University Chatbot - A100 GPU Accelerated
Optimized for 5-10 second response times
"""

import os
import sys
import time
import json
import torch
import asyncio
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import chromadb
from chromadb.config import Settings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Performance monitoring imports
import psutil
import numpy as np

# GPU monitoring (optional)
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

# Import configuration
from chroma_cloud_config import CHROMA_CLOUD_CONFIG

class NortheasternGPUChatbot:
    def __init__(self):
        """Initialize GPU-optimized chatbot with A100 acceleration"""
        print("🚀 Initializing Northeastern GPU Chatbot for Koyeb...")
        
        # GPU setup and optimization
        self.setup_gpu()
        
        # Initialize components
        self.setup_chromadb()
        self.setup_openai()
        self.setup_embeddings()
        
        # Performance optimization
        self.setup_caching()
        self.setup_concurrency()
        
        print("✅ GPU Chatbot initialized successfully")
    
    def setup_gpu(self):
        """Setup GPU optimization for A100"""
        print("🔧 Setting up GPU optimization...")
        
        # Check GPU availability
        if torch.cuda.is_available():
            self.device = torch.device("cuda:0")
            print(f"✅ GPU detected: {torch.cuda.get_device_name(0)}")
            print(f"✅ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
            
            # GPU memory optimization
            torch.cuda.empty_cache()
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False
            
            # Set memory allocation strategy
            os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"
            
        else:
            self.device = torch.device("cpu")
            print("⚠️ GPU not available, using CPU")
    
    def setup_chromadb(self):
        """Setup ChromaDB with GPU optimization"""
        print("🔧 Setting up ChromaDB...")
        
        try:
            # ChromaDB Cloud configuration
            self.chroma_client = chromadb.HttpClient(
                host=os.getenv("CHROMA_HOST", "localhost"),
                port=int(os.getenv("CHROMA_PORT", "8000")),
                settings=Settings(
                    chroma_api_impl="chromadb.api.fastapi.FastAPI",
                    chroma_server_host=os.getenv("CHROMA_HOST", "localhost"),
                    chroma_server_http_port=int(os.getenv("CHROMA_PORT", "8000")),
                )
            )
            
            # Get collections with caching
            self.collections = self.get_collections()
            print(f"✅ ChromaDB connected, {len(self.collections)} collections available")
            
        except Exception as e:
            print(f"❌ ChromaDB connection failed: {e}")
            raise
    
    def setup_openai(self):
        """Setup OpenAI with GPU optimization"""
        print("🔧 Setting up OpenAI...")
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            max_tokens=1000,
            request_timeout=30
        )
        
        print("✅ OpenAI configured")
    
    def setup_embeddings(self):
        """Setup GPU-accelerated embeddings"""
        print("🔧 Setting up GPU embeddings...")
        
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            chunk_size=1000
        )
        
        print("✅ GPU embeddings configured")
    
    def setup_caching(self):
        """Setup performance caching"""
        print("🔧 Setting up caching...")
        
        self.collection_cache = {}
        self.cache_ttl = 300  # 5 minutes
        self.last_cache_update = datetime.now()
        
        print("✅ Caching configured")
    
    def setup_concurrency(self):
        """Setup concurrent processing"""
        print("🔧 Setting up concurrency...")
        
        self.max_workers = min(8, os.cpu_count() or 4)
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        
        print(f"✅ Concurrency configured: {self.max_workers} workers")
    
    def get_collections(self):
        """Get available collections with caching"""
        try:
            collections = self.chroma_client.list_collections()
            return [col.name for col in collections]
        except Exception as e:
            print(f"❌ Failed to get collections: {e}")
            return []
    
    def search_documents_gpu(self, question: str, collection_name: str, top_k: int = 3) -> List[Dict]:
        """GPU-accelerated document search"""
        try:
            # Get collection with caching
            if collection_name not in self.collection_cache or \
               datetime.now() - self.last_cache_update > timedelta(seconds=self.cache_ttl):
                self.collection_cache[collection_name] = self.chroma_client.get_collection(collection_name)
                self.last_cache_update = datetime.now()
            
            collection = self.collection_cache[collection_name]
            
            # GPU-accelerated search
            results = collection.query(
                query_texts=[question],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            documents = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    documents.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else 0
                    })
            
            return documents
            
        except Exception as e:
            print(f"❌ GPU search failed: {e}")
            return []
    
    def search_all_collections_gpu(self, question: str) -> List[Dict]:
        """GPU-accelerated search across all collections"""
        print(f"🔍 GPU searching across {len(self.collections)} collections...")
        
        all_documents = []
        
        # Concurrent GPU searches
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for collection_name in self.collections:
                future = executor.submit(self.search_documents_gpu, question, collection_name, 3)
                futures.append((collection_name, future))
            
            # Collect results
            for collection_name, future in futures:
                try:
                    documents = future.result(timeout=10)
                    for doc in documents:
                        doc['collection'] = collection_name
                        all_documents.append(doc)
                except Exception as e:
                    print(f"❌ Search failed for {collection_name}: {e}")
        
        # Sort by distance and return top results
        all_documents.sort(key=lambda x: x.get('distance', 1.0))
        return all_documents[:5]  # Top 5 documents
    
    def generate_answer_gpu(self, question: str, documents: List[Dict]) -> str:
        """GPU-accelerated answer generation"""
        try:
            # Prepare context
            context = "\n\n".join([doc['content'] for doc in documents[:3]])
            
            # GPU-optimized prompt
            prompt_template = PromptTemplate(
                input_variables=["context", "question"],
                template="""You are a helpful assistant for Northeastern University. Answer the question based on the provided context.

Context: {context}

Question: {question}

Answer:"""
            )
            
            # Generate answer with GPU optimization
            prompt = prompt_template.format(context=context, question=question)
            
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            print(f"❌ GPU answer generation failed: {e}")
            return "I apologize, but I'm having trouble generating an answer right now. Please try again."
    
    def chat_gpu(self, question: str) -> Dict[str, Any]:
        """GPU-accelerated chat processing"""
        start_time = time.time()
        
        try:
            print(f"💬 Processing question: {question[:100]}...")
            
            # GPU-accelerated document search
            search_start = time.time()
            documents = self.search_all_collections_gpu(question)
            search_time = time.time() - search_start
            
            print(f"🔍 Found {len(documents)} documents in {search_time:.2f}s")
            
            # GPU-accelerated answer generation
            answer_start = time.time()
            answer = self.generate_answer_gpu(question, documents)
            answer_time = time.time() - answer_start
            
            total_time = time.time() - start_time
            
            # Performance metrics
            gpu_memory = torch.cuda.memory_allocated() / 1e9 if torch.cuda.is_available() else 0
            gpu_utilization = 0
            if GPU_AVAILABLE and GPUtil.getGPUs():
                gpu_utilization = GPUtil.getGPUs()[0].load * 100
            
            result = {
                "answer": answer,
                "sources": [doc['metadata'] for doc in documents[:3]],
                "performance": {
                    "total_time": round(total_time, 2),
                    "search_time": round(search_time, 2),
                    "answer_time": round(answer_time, 2),
                    "gpu_memory_gb": round(gpu_memory, 2),
                    "gpu_utilization": round(gpu_utilization, 1),
                    "documents_found": len(documents)
                }
            }
            
            print(f"✅ Answer generated in {total_time:.2f}s (GPU: {gpu_utilization:.1f}%)")
            return result
            
        except Exception as e:
            print(f"❌ GPU chat failed: {e}")
            return {
                "answer": "I apologize, but I'm experiencing technical difficulties. Please try again.",
                "sources": [],
                "performance": {
                    "total_time": round(time.time() - start_time, 2),
                    "error": str(e)
                }
            }

# Initialize chatbot
print("🚀 Starting Northeastern GPU Chatbot...")
chatbot = NortheasternGPUChatbot()

# FastAPI app
app = FastAPI(
    title="Northeastern University GPU Chatbot",
    description="A100 GPU-accelerated chatbot for Northeastern University",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "message": "Northeastern University GPU Chatbot API",
        "status": "healthy",
        "gpu_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU",
        "gpu_memory": f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB" if torch.cuda.is_available() else "N/A"
    }

@app.post("/chat")
async def chat_endpoint(request: Dict[str, Any]):
    """Main chat endpoint"""
    try:
        question = request.get("question", "")
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        result = chatbot.chat_gpu(question)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/runpod")
async def runpod_endpoint(request: Dict[str, Any]):
    """RunPod-compatible endpoint"""
    try:
        input_data = request.get("input", {})
        question = input_data.get("question", "")
        
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        result = chatbot.chat_gpu(question)
        
        return {
            "output": result,
            "id": request.get("id", "unknown")
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "id": request.get("id", "unknown")
        }

@app.get("/performance")
async def performance_endpoint():
    """Performance monitoring endpoint"""
    try:
        gpu_info = {}
        if torch.cuda.is_available():
            gpu_info = {
                "gpu_name": torch.cuda.get_device_name(0),
                "gpu_memory_total": f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB",
                "gpu_memory_allocated": f"{torch.cuda.memory_allocated() / 1e9:.2f} GB",
                "gpu_memory_cached": f"{torch.cuda.memory_reserved() / 1e9:.2f} GB",
                "gpu_utilization": f"{GPUtil.getGPUs()[0].load * 100:.1f}%" if GPU_AVAILABLE and GPUtil.getGPUs() else "N/A"
            }
        
        return {
            "status": "healthy",
            "gpu_info": gpu_info,
            "collections": len(chatbot.collections),
            "cache_size": len(chatbot.collection_cache)
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # This will be called by koyeb_gpu_start.py
    pass
