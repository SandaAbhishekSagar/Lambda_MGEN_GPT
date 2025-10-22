"""
Lambda Labs GPU-Optimized Chatbot
Ultra-fast Northeastern University RAG chatbot with GPU acceleration
"""

import os
import sys
import time
import logging
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import torch
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.shared.lambda_chroma_service import LambdaGPUChromaService
from services.shared.lambda_cache_manager import LambdaGPUCacheManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ChatResponse:
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float
    timing: Dict[str, float]
    gpu_info: Dict[str, Any]

class LambdaGPUUniversityRAGChatbot:
    """Ultra-optimized Northeastern University RAG chatbot for Lambda Labs GPU"""
    
    def __init__(self, cache_file: str = "lambda_gpu_embeddings_cache.pkl"):
        self.chroma_service = LambdaGPUChromaService()
        self.embedding_manager = LambdaGPUCacheManager()
        self.cache_file = cache_file
        self.embeddings_cache = {}
        self.document_embeddings = {}
        self.model = None
        self.device = self._get_optimal_device()
        self.batch_size = 32  # Optimized for GPU memory
        self.load_cache()
        
        logger.info(f"[LAMBDA GPU] Initialized on device: {self.device}")
    
    def _get_optimal_device(self) -> str:
        """Get optimal device for Lambda Labs GPU"""
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            logger.info(f"[LAMBDA GPU] GPU: {gpu_name}, Memory: {gpu_memory:.1f}GB")
            
            # Optimize for Lambda Labs GPUs
            if "A100" in gpu_name or "H100" in gpu_name:
                self.batch_size = 64
            elif "4090" in gpu_name or "3090" in gpu_name:
                self.batch_size = 48
            elif "3080" in gpu_name:
                self.batch_size = 32
            else:
                self.batch_size = 24
                
            return "cuda"
        else:
            logger.warning("[LAMBDA GPU] No GPU available, using CPU")
            self.batch_size = 16
            return "cpu"
    
    def load_cache(self):
        """Load embeddings cache with error handling"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                    self.embeddings_cache = cache_data.get('embeddings', {})
                    self.document_embeddings = cache_data.get('documents', {})
                logger.info(f"[LAMBDA GPU] Loaded cache: {len(self.embeddings_cache)} queries, {len(self.document_embeddings)} documents")
        except Exception as e:
            logger.warning(f"[LAMBDA GPU] Cache load failed: {e}")
            self.embeddings_cache = {}
            self.document_embeddings = {}
    
    def save_cache(self):
        """Save embeddings cache"""
        try:
            cache_data = {
                'embeddings': self.embeddings_cache,
                'documents': self.document_embeddings
            }
            with open(self.cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            logger.info(f"[LAMBDA GPU] Cache saved: {len(self.embeddings_cache)} queries, {len(self.document_embeddings)} documents")
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Cache save failed: {e}")
    
    def get_embedding_model(self):
        """Get or create embedding model with GPU optimization"""
        if self.model is None:
            try:
                # Use GPU-optimized model
                self.model = SentenceTransformer(
                    'all-MiniLM-L6-v2',
                    device=self.device,
                    cache_folder='/tmp/sentence_transformers'
                )
                
                # Optimize for GPU
                if self.device == 'cuda':
                    self.model = self.model.half()  # Use half precision for speed
                    
                logger.info(f"[LAMBDA GPU] Embedding model loaded on {self.device}")
            except Exception as e:
                logger.error(f"[LAMBDA GPU] Model loading failed: {e}")
                raise
        return self.model
    
    def get_query_embedding(self, query: str) -> np.ndarray:
        """Get query embedding with caching"""
        if query in self.embeddings_cache:
            return self.embeddings_cache[query]
        
        model = self.get_embedding_model()
        embedding = model.encode([query], convert_to_tensor=True, show_progress_bar=False)
        
        if self.device == 'cuda':
            embedding = embedding.cpu().numpy()
        else:
            embedding = embedding.numpy()
        
        # Cache the embedding
        self.embeddings_cache[query] = embedding[0]
        return embedding[0]
    
    def get_client(self):
        """Get ChromaDB client"""
        return self.chroma_service.get_client()
    
    def get_batch_collections(self, force_refresh: bool = False) -> List[str]:
        """Get batch collections with caching"""
        current_time = time.time()
        
        if not force_refresh and self.collections_cache and (current_time - self.last_cache_update) < self.cache_ttl:
            return self.collections_cache
        
        try:
            client = self.get_client()
            all_collections = []
            offset = 0
            limit = 1000
            
            # Get all collections with pagination
            while True:
                try:
                    collections_batch = client.list_collections(limit=limit, offset=offset)
                    if not collections_batch or len(collections_batch) == 0:
                        break
                    all_collections.extend(collections_batch)
                    if len(collections_batch) < limit:
                        break
                    offset += limit
                except Exception as e:
                    logger.warning(f"[LAMBDA GPU] Error fetching collections batch: {e}")
                    break
            
            # Filter for batch collections
            batch_collections = [
                col.name for col in all_collections
                if 'batch' in col.name.lower() or 'ultra_optimized' in col.name.lower()
            ]
            
            self.collections_cache = batch_collections
            self.last_cache_update = current_time
            
            logger.info(f"[LAMBDA GPU] Found {len(batch_collections)} batch collections")
            return batch_collections
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error getting collections: {e}")
            # Fallback: Generate collection names based on known pattern
            logger.warning("[LAMBDA GPU] Using fallback collection names due to error")
            fallback_collections = []
            for i in range(1, 1001):  # Generate 1000 collection names
                fallback_collections.append(f"documents_ultra_optimized_batch_{i}")
            
            # Update cache
            self.collections_cache = fallback_collections
            self.last_cache_update = current_time
            logger.info(f"[LAMBDA GPU] Using fallback: {len(fallback_collections)} collections")
            return fallback_collections
    
    def search_documents_parallel(self, query_embedding: np.ndarray, n_results: int = 10) -> List[Dict[str, Any]]:
        """Parallel search across collections for maximum speed"""
        try:
            collections = self.get_batch_collections()
            if not collections:
                return []
            
            # Limit collections for performance
            max_collections = min(len(collections), self.max_collections_per_search)
            search_collections = collections[:max_collections]
            
            all_results = []
            
            # Parallel search across collections
            with ThreadPoolExecutor(max_workers=self.parallel_workers) as executor:
                future_to_collection = {
                    executor.submit(self._search_single_collection, collection_name, query_embedding, n_results): collection_name
                    for collection_name in search_collections
                }
                
                for future in as_completed(future_to_collection, timeout=self.search_timeout):
                    collection_name = future_to_collection[future]
                    try:
                        results = future.result(timeout=self.search_timeout)
                        all_results.extend(results)
                    except Exception as e:
                        logger.warning(f"[LAMBDA GPU] Search failed for {collection_name}: {e}")
                        continue
            
            # Sort by similarity and return top results
            all_results.sort(key=lambda x: x.get('similarity', 0), reverse=True)
            return all_results[:n_results]
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Parallel search failed: {e}")
            return []
    
    def _search_single_collection(self, collection_name: str, query_embedding: np.ndarray, n_results: int) -> List[Dict[str, Any]]:
        """Search a single collection"""
        try:
            client = self.get_client()
            collection = client.get_collection(collection_name)
            
            results = collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {},
                        'similarity': results['distances'][0][i] if results['distances'] and results['distances'][0] else 0.0,
                        'collection': collection_name
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.warning(f"[LAMBDA GPU] Single collection search failed for {collection_name}: {e}")
            return []
    
    def chat(self, question: str) -> ChatResponse:
        """Main chat method with GPU optimization"""
        start_time = time.time()
        
        try:
            # Get query embedding
            query_start = time.time()
            query_embedding = self.get_query_embedding(question)
            query_time = time.time() - query_start
            
            # Search documents
            search_start = time.time()
            search_results = self.search_documents_parallel(query_embedding, n_results=10)
            search_time = time.time() - search_start
            
            # Generate response (simplified for now)
            if search_results:
                # Use the most relevant document as context
                context = search_results[0]['content']
                answer = f"Based on the Northeastern University information: {context[:500]}..."
                confidence = search_results[0]['similarity']
            else:
                answer = "I don't have enough information to answer this question about Northeastern University."
                confidence = 0.0
            
            # Get GPU info
            gpu_info = self.get_gpu_info()
            
            # Calculate timing
            total_time = time.time() - start_time
            timing = {
                'query_embedding': query_time,
                'search': search_time,
                'generation': 0.0,  # Simplified for now
                'total': total_time
            }
            
            return ChatResponse(
                answer=answer,
                sources=search_results[:5],  # Top 5 sources
                confidence=confidence,
                timing=timing,
                gpu_info=gpu_info
            )
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Chat failed: {e}")
            return ChatResponse(
                answer="I'm sorry, I encountered an error processing your question.",
                sources=[],
                confidence=0.0,
                timing={'total': time.time() - start_time},
                gpu_info=self.get_gpu_info()
            )
    
    def get_gpu_info(self) -> Dict[str, Any]:
        """Get GPU information"""
        gpu_info = {
            'cuda_available': torch.cuda.is_available(),
            'device': self.device,
            'batch_size': self.batch_size
        }
        
        if torch.cuda.is_available():
            gpu_info.update({
                'gpu_name': torch.cuda.get_device_name(0),
                'gpu_memory_total': torch.cuda.get_device_properties(0).total_memory / 1024**3,
                'gpu_memory_allocated': torch.cuda.memory_allocated(0) / 1024**3,
                'gpu_memory_cached': torch.cuda.memory_reserved(0) / 1024**3,
                'cuda_version': torch.version.cuda
            })
        
        return gpu_info
    
    def clear_cache(self):
        """Clear all caches"""
        self.embeddings_cache.clear()
        self.document_embeddings.clear()
        self.collections_cache = []
        logger.info("[LAMBDA GPU] All caches cleared")

# Global chatbot instance
_chatbot = None

def get_chatbot() -> LambdaGPUUniversityRAGChatbot:
    """Get or create chatbot instance"""
    global _chatbot
    if _chatbot is None:
        _chatbot = LambdaGPUUniversityRAGChatbot()
    return _chatbot

def clear_gpu_cache():
    """Clear GPU cache"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        logger.info("[LAMBDA GPU] GPU cache cleared")

