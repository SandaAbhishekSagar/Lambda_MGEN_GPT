#!/usr/bin/env python3
"""
Lambda Labs GPU Chatbot - HuggingFace Hub Compatible Version
Northeastern University Chatbot with GPU acceleration
Fixed for HuggingFace Hub compatibility issues
"""

import os
import sys
import time
import json
import logging
import pickle
import hashlib
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import torch
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ChatResponse:
    """Structured response from the chatbot"""
    answer: str
    sources: List[Dict[str, Any]]
    confidence: str
    timing: Dict[str, float]
    gpu_info: Dict[str, Any]

class LambdaGPUEmbeddingManager:
    """GPU-optimized embedding manager with compatibility fixes"""
    
    def __init__(self):
        self.device = self._get_optimal_device()
        self.model = None
        self.embeddings_cache = {}
        self.batch_size = 32
        
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
    
    def get_embedding_model(self):
        """Get or create embedding model with compatibility fixes"""
        if self.model is None:
            try:
                logger.info("[LAMBDA GPU] Loading embedding model...")
                
                # Try multiple models in order of preference
                models_to_try = [
                    'paraphrase-MiniLM-L6-v2',  # More compatible
                    'all-MiniLM-L6-v2',
                    'all-mpnet-base-v2'
                ]
                
                for model_name in models_to_try:
                    try:
                        logger.info(f"[LAMBDA GPU] Trying model: {model_name}")
                        self.model = SentenceTransformer(model_name, device=self.device)
                        logger.info(f"[LAMBDA GPU] Successfully loaded: {model_name}")
                        break
                    except Exception as e:
                        logger.warning(f"[LAMBDA GPU] Failed to load {model_name}: {e}")
                        continue
                
                if self.model is None:
                    raise Exception("Failed to load any embedding model")
                    
            except Exception as e:
                logger.error(f"[LAMBDA GPU] Error loading embedding model: {e}")
                raise
        
        return self.model
    
    def get_document_hash(self, content: str) -> str:
        """Generate hash for document content"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_query_embedding(self, content: str) -> np.ndarray:
        """Get embedding for query content with GPU acceleration"""
        doc_hash = self.get_document_hash(content)
        
        if doc_hash in self.embeddings_cache:
            return self.embeddings_cache[doc_hash]
        
        model = self.get_embedding_model()
        
        try:
            # GPU-optimized embedding generation
            with torch.cuda.amp.autocast() if self.device == "cuda" else torch.no_grad():
                embedding = model.encode([content], convert_to_tensor=True, show_progress_bar=False)
                if self.device == "cuda":
                    embedding = embedding.cpu().numpy()[0]
                else:
                    embedding = embedding.numpy()[0]
            
            self.embeddings_cache[doc_hash] = embedding
            return embedding
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error generating embedding: {e}")
            # Fallback to CPU if GPU fails
            if self.device == "cuda":
                logger.info("[LAMBDA GPU] Falling back to CPU for embeddings")
                self.device = "cpu"
                model = SentenceTransformer('paraphrase-MiniLM-L6-v2', device='cpu')
                embedding = model.encode([content], convert_to_tensor=False, show_progress_bar=False)
                return embedding[0]
            else:
                raise
    
    def batch_embed_documents(self, documents: List[str]) -> List[np.ndarray]:
        """Batch embed documents for efficiency"""
        if not documents:
            return []
        
        model = self.get_embedding_model()
        embeddings = []
        
        # Process in batches
        for i in range(0, len(documents), self.batch_size):
            batch = documents[i:i + self.batch_size]
            try:
                with torch.cuda.amp.autocast() if self.device == "cuda" else torch.no_grad():
                    batch_embeddings = model.encode(batch, convert_to_tensor=True, show_progress_bar=False)
                    if self.device == "cuda":
                        batch_embeddings = batch_embeddings.cpu().numpy()
                    else:
                        batch_embeddings = batch_embeddings.numpy()
                
                embeddings.extend(batch_embeddings)
                
            except Exception as e:
                logger.error(f"[LAMBDA GPU] Error in batch embedding: {e}")
                # Fallback to individual embedding
                for doc in batch:
                    try:
                        embedding = model.encode([doc], convert_to_tensor=False, show_progress_bar=False)
                        embeddings.append(embedding[0])
                    except Exception as e2:
                        logger.error(f"[LAMBDA GPU] Error embedding individual document: {e2}")
                        # Create zero embedding as fallback
                        embeddings.append(np.zeros(384))  # Standard embedding size
        
        return embeddings

class LambdaGPUChromaService:
    """GPU-optimized ChromaDB service with multiple fallback methods"""
    
    def __init__(self):
        self.client = None
        self.collections_cache = []
        self.cache_timestamp = 0
        self.cache_duration = 300  # 5 minutes
    
    def get_client(self):
        """Get or create ChromaDB client with multiple fallback methods"""
        if self.client is None:
            try:
                # Method 1: Try ChromaDB Cloud with API key
                chroma_api_key = os.getenv('CHROMADB_API_KEY')
                chroma_tenant = os.getenv('CHROMADB_TENANT')
                chroma_database = os.getenv('CHROMADB_DATABASE', 'newtest')
                
                if chroma_api_key and chroma_tenant:
                    logger.info("[LAMBDA GPU] Attempting ChromaDB Cloud connection...")
                    
                    # Try different authentication methods
                    try:
                        # Method 1a: Direct HttpClient with settings
                        self.client = chromadb.HttpClient(
                            host="https://api.trychroma.com",
                            port=8000,
                            settings=Settings(
                                chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
                                chroma_client_auth_credentials=chroma_api_key
                            )
                        )
                        logger.info("[LAMBDA GPU] ChromaDB Cloud connected (Method 1a)")
                        
                    except Exception as e1:
                        logger.warning(f"[LAMBDA GPU] Method 1a failed: {e1}")
                        try:
                            # Method 1b: Try with different settings
                            self.client = chromadb.HttpClient(
                                host="https://api.trychroma.com",
                                port=8000,
                                settings=Settings(
                                    chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
                                    chroma_client_auth_credentials=chroma_api_key,
                                    chroma_client_auth_credentials_provider="chromadb.auth.token.TokenAuthClientProvider"
                                )
                            )
                            logger.info("[LAMBDA GPU] ChromaDB Cloud connected (Method 1b)")
                            
                        except Exception as e2:
                            logger.warning(f"[LAMBDA GPU] Method 1b failed: {e2}")
                            # Method 1c: Try without explicit auth provider
                            self.client = chromadb.HttpClient(
                                host="https://api.trychroma.com",
                                port=8000,
                                settings=Settings(
                                    chroma_client_auth_credentials=chroma_api_key
                                )
                            )
                            logger.info("[LAMBDA GPU] ChromaDB Cloud connected (Method 1c)")
                
                # Method 2: Fallback to local ChromaDB
                if self.client is None:
                    logger.info("[LAMBDA GPU] Falling back to local ChromaDB...")
                    self.client = chromadb.HttpClient(host="localhost", port=8000)
                    logger.info("[LAMBDA GPU] Local ChromaDB connected")
                
            except Exception as e:
                logger.error(f"[LAMBDA GPU] Error connecting to ChromaDB: {e}")
                # Method 3: Create fallback client
                self.client = chromadb.HttpClient(host="localhost", port=8000)
                logger.warning("[LAMBDA GPU] Using fallback ChromaDB connection")
        
        return self.client
    
    def get_batch_collections(self) -> List[str]:
        """Get list of batch collections with fallback mechanism"""
        try:
            # Check cache first
            current_time = time.time()
            if (self.collections_cache and 
                current_time - self.cache_timestamp < self.cache_duration):
                return self.collections_cache
            
            client = self.get_client()
            collections = client.list_collections()
            
            if collections:
                collection_names = [col.name for col in collections]
                self.collections_cache = collection_names
                self.cache_timestamp = current_time
                logger.info(f"[LAMBDA GPU] Found {len(collection_names)} collections")
                return collection_names
            else:
                # Fallback: Generate collection names based on pattern
                logger.warning("[LAMBDA GPU] No collections found, generating fallback names")
                fallback_collections = [f"documents_ultra_optimized_batch_{i:03d}" for i in range(1000)]
                self.collections_cache = fallback_collections
                self.cache_timestamp = current_time
                return fallback_collections
                
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error getting collections: {e}")
            # Fallback: Generate collection names
            fallback_collections = [f"documents_ultra_optimized_batch_{i:03d}" for i in range(1000)]
            self.collections_cache = fallback_collections
            self.cache_timestamp = current_time
            return fallback_collections
    
    def search_single_collection(self, collection_name: str, query_embedding: np.ndarray, n_results: int = 10) -> List[Dict[str, Any]]:
        """Search a single collection"""
        try:
            client = self.get_client()
            collection = client.get_collection(collection_name)
            
            results = collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results
            )
            
            documents = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    documents.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {},
                        'distance': results['distances'][0][i] if results['distances'] and results['distances'][0] else 0.0,
                        'collection': collection_name
                    })
            
            return documents
            
        except Exception as e:
            logger.warning(f"[LAMBDA GPU] Error searching collection {collection_name}: {e}")
            return []
    
    def search_documents_parallel(self, query_embedding: np.ndarray, n_results: int = 10) -> List[Dict[str, Any]]:
        """Parallel search across collections for maximum speed"""
        try:
            collections = self.get_batch_collections()
            if not collections:
                return []
            
            # Limit collections for performance (optimized for Lambda Labs)
            max_collections = 150  # Increased from 100 for better coverage
            collections_to_search = collections[:max_collections]
            
            logger.info(f"[LAMBDA GPU] Searching {len(collections_to_search)} collections in parallel")
            
            all_documents = []
            
            # Use ThreadPoolExecutor for parallel search
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = []
                
                for collection_name in collections_to_search:
                    future = executor.submit(self.search_single_collection, collection_name, query_embedding, n_results * 2)
                    futures.append(future)
                
                # Collect results
                for future in futures:
                    try:
                        results = future.result(timeout=5)  # 5 second timeout per collection
                        if results:
                            all_documents.extend(results)
                    except Exception as e:
                        logger.warning(f"[LAMBDA GPU] Collection search timeout/error: {e}")
                        continue
            
            logger.info(f"[LAMBDA GPU] Found {len(all_documents)} total documents")
            return all_documents[:n_results]
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error in parallel search: {e}")
            return []

class LambdaGPUChatbot:
    """Main chatbot class with GPU acceleration and compatibility fixes"""
    
    def __init__(self):
        self.embedding_manager = LambdaGPUEmbeddingManager()
        self.chroma_service = LambdaGPUChromaService()
        self.openai_client = None
        self._initialize_openai()
        
        logger.info("[LAMBDA GPU] Chatbot initialized with compatibility fixes")
    
    def _initialize_openai(self):
        """Initialize OpenAI client"""
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
            
            self.openai_client = OpenAI(api_key=api_key)
            logger.info("[LAMBDA GPU] OpenAI client initialized")
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error initializing OpenAI: {e}")
            raise
    
    def search_documents(self, question: str, n_results: int = 10) -> List[Dict[str, Any]]:
        """Search for relevant documents with timing"""
        try:
            start_time = time.time()
            
            # Get query embedding
            embedding_start = time.time()
            query_embedding = self.embedding_manager.get_query_embedding(question)
            embedding_time = time.time() - embedding_start
            
            # Search documents
            search_start = time.time()
            documents = self.chroma_service.search_documents_parallel(query_embedding, n_results)
            search_time = time.time() - search_start
            
            total_time = time.time() - start_time
            
            logger.info(f"[LAMBDA GPU] Search completed in {total_time:.2f}s (embedding: {embedding_time:.2f}s, search: {search_time:.2f}s)")
            
            return documents
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error in document search: {e}")
            return []
    
    def generate_answer(self, question: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate answer using optimized LLM"""
        try:
            if not context_docs:
                return {
                    'answer': "I don't have enough information to answer this question about Northeastern University.",
                    'sources': [],
                    'confidence': 'low'
                }
            
            # Build optimized context
            context_parts = []
            sources = []
            
            for doc in context_docs[:5]:  # Limit to top 5 documents
                content = doc.get('content', '')
                metadata = doc.get('metadata', {})
                collection = doc.get('collection', 'unknown')
                
                if content:
                    context_parts.append(content)
                    sources.append({
                        'content': content[:200] + "..." if len(content) > 200 else content,
                        'metadata': metadata,
                        'collection': collection
                    })
            
            context = "\n\n".join(context_parts)
            
            # Create optimized prompt
            prompt = f"""Based on the following information about Northeastern University, answer the question: {question}

Context:
{context}

Please provide a comprehensive answer based on the information above. If the information doesn't contain enough details to answer the question, please say so."""

            # Generate answer with OpenAI
            response = self.openai_client.chat.completions.create(
                model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for Northeastern University. Provide accurate, helpful information based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=int(os.getenv('OPENAI_MAX_TOKENS', '1000')),
                temperature=float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
            )
            
            answer = response.choices[0].message.content
            
            # Calculate confidence based on document quality
            confidence = 'high' if len(context_docs) >= 3 else 'medium' if len(context_docs) >= 1 else 'low'
            
            return {
                'answer': answer,
                'sources': sources,
                'confidence': confidence,
                'documents_searched': len(context_docs)
            }
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error generating answer: {e}")
            return {
                'answer': f"I encountered an error generating the answer: {str(e)}",
                'sources': [],
                'confidence': 'low'
            }
    
    def chat(self, question: str) -> ChatResponse:
        """Main chat function with comprehensive timing"""
        start_time = time.time()
        
        logger.info(f"[LAMBDA GPU] Processing question: {question[:100]}...")
        
        # Search for relevant documents
        search_start = time.time()
        documents = self.search_documents(question, n_results=10)
        search_time = time.time() - search_start
        
        # Generate answer
        generation_start = time.time()
        result = self.generate_answer(question, documents)
        generation_time = time.time() - generation_start
        
        total_time = time.time() - start_time
        
        logger.info(f"[LAMBDA GPU] Total response time: {total_time:.2f}s (search: {search_time:.2f}s, generation: {generation_time:.2f}s)")
        
        # Add timing information
        timing = {
            'search': round(search_time, 2),
            'generation': round(generation_time, 2),
            'total': round(total_time, 2)
        }
        
        # Get GPU info
        gpu_info = self.get_gpu_info()
        
        return ChatResponse(
            answer=result['answer'],
            sources=result['sources'],
            confidence=result['confidence'],
            timing=timing,
            gpu_info=gpu_info
        )
    
    def get_gpu_info(self) -> Dict[str, Any]:
        """Get GPU information"""
        try:
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                gpu_utilization = torch.cuda.utilization(0) if hasattr(torch.cuda, 'utilization') else 0
                
                return {
                    'gpu_available': True,
                    'gpu_name': gpu_name,
                    'gpu_memory_gb': round(gpu_memory, 2),
                    'gpu_utilization': gpu_utilization,
                    'device': self.embedding_manager.device
                }
            else:
                return {
                    'gpu_available': False,
                    'device': 'cpu'
                }
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error getting GPU info: {e}")
            return {
                'gpu_available': False,
                'device': 'cpu',
                'error': str(e)
            }

# Global chatbot instance
chatbot = None

def initialize_chatbot():
    """Initialize the chatbot"""
    global chatbot
    try:
        chatbot = LambdaGPUChatbot()
        logger.info("[LAMBDA GPU] Chatbot initialized successfully")
        return True
    except Exception as e:
        logger.error(f"[LAMBDA GPU] Chatbot initialization failed: {e}")
        return False

if __name__ == "__main__":
    # Test the chatbot
    if initialize_chatbot():
        test_question = "What programs does Northeastern University offer?"
        response = chatbot.chat(test_question)
        print(f"Question: {test_question}")
        print(f"Answer: {response.answer}")
        print(f"Confidence: {response.confidence}")
        print(f"Timing: {response.timing}")
        print(f"GPU Info: {response.gpu_info}")
    else:
        print("Failed to initialize chatbot")
